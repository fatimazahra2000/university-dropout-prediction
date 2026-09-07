Bien sûr. Voici le `lineage.md` **complet, corrigé et prêt à copier-coller en une seule fois** :

````markdown
# Data Lineage — University Dropout Prediction

## 1. Vue d'ensemble

Le Data Lineage décrit le parcours des données depuis le dataset
`xAPI-Edu-Data.csv` jusqu'à leur utilisation dans le système de
prédiction de l'abandon universitaire.

Le flux principal des données est :

```text
xAPI-Edu-Data.csv
        │
        ▼
       DLT
        │
        ▼
raw_data.students_raw
        │
        ▼
       dbt
        │
        ▼
main.stg_students
        │
        ▼
main.prepared_students
        │
        ├──────────────► Data Quality
        │                    │
        │                    ▼
        │              Business Rules
        │                    │
        │                    ▼
        │              absence_risk
        │
        ▼
Machine Learning
        │
        ▼
      MLflow
        │
        ▼
     FastAPI
```

**Dagster** constitue la couche d'orchestration du pipeline.

Il coordonne les différentes étapes, leurs dépendances et leur ordre
d'exécution. Dagster ne réalise pas lui-même les transformations de
données.

---

## 2. Source des données

Les données proviennent du fichier :

```text
data/raw/xAPI-Edu-Data.csv
```

Ce dataset contient les informations relatives aux étudiants et à leurs
interactions avec leur environnement pédagogique.

Le fichier CSV constitue le point de départ du pipeline de données.

---

## 3. Ingestion des données avec DLT

L'ingestion est réalisée avec **DLT**.

Le script d'ingestion se trouve dans :

```text
dataops/dlt/ingest_data.py
```

DLT charge les données du fichier CSV dans une base DuckDB.

La configuration actuelle est :

```text
Pipeline    : student_pipeline
Destination : DuckDB
Dataset     : raw_data
Table       : students_raw
```

La table obtenue est :

```text
raw_data.students_raw
```

La base DuckDB utilisée localement est :

```text
data/duckdb/university.duckdb
```

Le nom `student_pipeline` correspond au nom du pipeline DLT et non au nom
du fichier DuckDB.

Le fichier DuckDB n'est pas versionné dans Git car il est exclu par le
`.gitignore`.

L'ingestion actuelle produit :

```text
480 lignes
```

---

## 4. Data Quality

Les données brutes font l'objet de contrôles de qualité.

Les principaux éléments du module Data Quality sont :

```text
data_quality/
├── data_contract.yaml
├── quality_checks.py
├── check_business_rule.py
├── lineage.md
└── README.md
```

### 4.1 Data Contract

Les règles de qualité sont décrites dans :

```text
data_quality/data_contract.yaml
```

Le Data Contract définit notamment :

- les colonnes attendues ;
- les colonnes obligatoires ;
- les valeurs autorisées ;
- les plages des variables numériques ;
- les règles d'unicité ;
- les règles de volume ;
- les règles métier.

### 4.2 Contrôles de qualité

Le script principal est :

```text
data_quality/quality_checks.py
```

Il contrôle notamment les données présentes dans :

```text
raw_data.students_raw
```

Les contrôles portent notamment sur :

- la présence des colonnes attendues ;
- l'absence de valeurs NULL ;
- la validité des valeurs catégorielles ;
- les plages des variables numériques ;
- les doublons ;
- l'unicité des identifiants `_dlt_id` ;
- le volume minimal de données.

Le dernier contrôle réalisé a donné :

```text
RESULT: PASS
```

avec :

```text
480 lignes
480 identifiants _dlt_id distincts
```

---

## 5. Règle métier `absence_risk`

Une règle métier importante concerne la variable :

```text
absence_risk
```

Cette variable est construite à partir de :

```text
studentabsencedays
```

La correspondance attendue est :

```text
Under-7  → 0
Above-7  → 1
```

La règle est vérifiée par le script :

```text
data_quality/check_business_rule.py
```

Le contrôle est effectué sur :

```text
main.prepared_students
```

La requête vérifie notamment que :

```text
studentabsencedays = 'Under-7'  → absence_risk = 0
studentabsencedays = 'Above-7'  → absence_risk = 1
```

Les valeurs NULL de `studentabsencedays` ou `absence_risk` sont également
considérées comme des violations.

Le dernier contrôle réalisé a donné :

```text
BUSINESS RULE CHECK

Violations absence_risk : 0
Statut                  : PASS
```

La règle métier `absence_risk` est donc actuellement respectée.

---

## 6. Transformation avec dbt

Après l'ingestion, les données sont transformées avec **dbt**.

Le projet dbt se trouve dans :

```text
dataops/dbt/university_dropout_dbt/
```

La chaîne de transformation est :

```text
raw_data.students_raw
        ↓
main.stg_students
        ↓
main.prepared_students
```

### 6.1 `stg_students`

Le modèle :

```text
models/stg_students.sql
```

récupère les données depuis la source DLT :

```text
raw_data.students_raw
```

La source est déclarée dans :

```text
models/sources.yml
```

Le modèle `stg_students` constitue la première étape de transformation
dans dbt.

### 6.2 `prepared_students`

Le modèle :

```text
models/prepared_students.sql
```

utilise le modèle précédent :

```text
{{ ref('stg_students') }}
```

Il prépare les données pour les étapes suivantes du pipeline.

Une transformation importante consiste à créer :

```text
absence_risk
```

à partir de :

```text
studentabsencedays
```

avec la correspondance :

```text
Under-7  → 0
Above-7  → 1
```

Le modèle produit également :

```text
risk_class
```

à partir de la variable :

```text
class
```

La table préparée utilisée par les étapes suivantes est :

```text
main.prepared_students
```

---

## 7. Tests dbt

La qualité des données transformées est également contrôlée avec les
tests dbt définis dans :

```text
models/schema.yml
```

Les tests comprennent notamment :

- `not_null` ;
- `accepted_values`.

Les modèles concernés sont :

```text
stg_students
prepared_students
```

Le dernier résultat obtenu est :

```text
PASS=9
WARN=0
ERROR=0
SKIP=0
NO-OP=0
REUSED=0
TOTAL=9
```

Les 9 tests dbt sont donc actuellement en succès.

---

## 8. Orchestration avec Dagster

**Dagster** constitue la couche d'orchestration du pipeline.

Son rôle est de coordonner les différents composants du système et leurs
dépendances.

Les principaux traitements orchestrés sont :

```text
DLT
 ↓
dbt
 ↓
Data Quality
 ↓
Machine Learning
 ↓
MLflow
```

Dagster permet notamment de :

- définir les dépendances entre les étapes ;
- contrôler l'ordre d'exécution ;
- automatiser les traitements ;
- suivre les exécutions ;
- gérer les ressources utilisées par les traitements ;
- faciliter la reproductibilité du pipeline.

Dagster ne remplace pas DLT, dbt, les contrôles Data Quality ou les outils
Machine Learning.

Il assure leur orchestration.

---

## 9. Machine Learning

Après la transformation et la validation des données, les données
préparées sont utilisées pour l'étape de Machine Learning.

La source principale pour cette étape est :

```text
main.prepared_students
```

Le flux est :

```text
main.prepared_students
        ↓
Machine Learning
        ↓
Entraînement
        ↓
Évaluation
```

Le code Machine Learning est situé dans :

```text
ml/
```

Cette étape permet d'entraîner et d'évaluer le modèle de prédiction de
l'abandon universitaire.

---

## 10. MLflow

**MLflow** intervient dans le suivi du Machine Learning.

Son rôle est notamment d'assurer :

- le suivi des expériences ;
- l'enregistrement des paramètres ;
- le suivi des métriques ;
- la gestion des artefacts ;
- la gestion des modèles.

Le flux est :

```text
Machine Learning
        ↓
     MLflow
        ↓
Modèle enregistré
```

Les éléments liés à MLflow sont prévus dans :

```text
mlflow/
```

---

## 11. FastAPI

Une fois le modèle entraîné et disponible, il est exposé via **FastAPI**.

Le code de l'API est situé dans :

```text
api/
```

Le flux final est :

```text
Machine Learning
        ↓
     MLflow
        ↓
Modèle enregistré
        ↓
     FastAPI
        ↓
API de prédiction
```

FastAPI permet de rendre le modèle accessible à travers une API de
prédiction.

---

## 12. Lineage global

Le parcours complet des données peut être représenté ainsi :

```text
┌──────────────────────────────┐
│ xAPI-Edu-Data.csv            │
│ Source                       │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ DLT                          │
│ Ingestion                    │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ DuckDB                       │
│ raw_data.students_raw        │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ dbt                          │
│ Transformations              │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ main.stg_students            │
│ Staging                      │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ main.prepared_students       │
│ Données préparées            │
└──────────────┬───────────────┘
               │
               ├─────────────────────┐
               │                     │
               ▼                     ▼
┌──────────────────────────────┐  ┌──────────────────────────────┐
│ Data Quality                 │  │ Machine Learning             │
│ Contract + Quality Checks    │  │ Entraînement / évaluation    │
└──────────────────────────────┘  └──────────────┬───────────────┘
                                                 │
                                                 ▼
                                  ┌──────────────────────────────┐
                                  │ MLflow                       │
                                  │ Tracking / Modèles           │
                                  └──────────────┬───────────────┘
                                                 │
                                                 ▼
                                  ┌──────────────────────────────┐
                                  │ FastAPI                      │
                                  │ API de prédiction            │
                                  └──────────────────────────────┘
```

**Dagster orchestre l'ensemble de ces étapes.**

Il ne constitue donc pas une étape de transformation située entre
`prepared_students` et le Machine Learning.

---

## 13. Traçabilité et reproductibilité

Les éléments nécessaires à la reconstruction du pipeline sont versionnés
dans Git.

Ils comprennent notamment :

```text
- code d'ingestion DLT
- configuration dbt
- modèles SQL dbt
- sources dbt
- tests dbt
- règles Data Quality
- Data Contract
- contrôle des règles métier
- code Dagster
- code Machine Learning
- configuration MLflow
- code FastAPI
```

Le fichier DuckDB généré localement n'est pas versionné.

Il peut être reconstruit à partir du dataset et du code d'ingestion :

```text
xAPI-Edu-Data.csv
        ↓
dataops/dlt/ingest_data.py
        ↓
data/duckdb/university.duckdb
        ↓
raw_data.students_raw
```

Cette organisation permet de conserver la traçabilité des données tout en
évitant de versionner directement le fichier de base de données.

---

## 14. Résultats de validation actuels

Les contrôles réalisés actuellement donnent les résultats suivants.

### Data Quality

```text
Lignes                          : 480
Identifiants _dlt_id distincts : 480
Statut                          : PASS
```

### Business Rule

```text
Règle absence_risk
Violations                      : 0
Statut                          : PASS
```

### dbt run

```text
PASS=2
WARN=0
ERROR=0
SKIP=0
NO-OP=0
REUSED=0
TOTAL=2
```

### dbt test

```text
PASS=9
WARN=0
ERROR=0
SKIP=0
NO-OP=0
REUSED=0
TOTAL=9
```

Les contrôles de qualité, la règle métier et les tests dbt actuellement
exécutés sont donc en état **PASS**.

---

## 15. Résumé du lineage

Le Data Lineage du projet peut être résumé par :

```text
xAPI-Edu-Data.csv
        ↓
DLT
        ↓
raw_data.students_raw
        ↓
dbt
        ↓
main.stg_students
        ↓
main.prepared_students
        ↓
Machine Learning
        ↓
MLflow
        ↓
FastAPI
```

Les contrôles Data Quality et les règles métier sont appliqués aux données
aux étapes appropriées.

**Dagster orchestre l'ensemble du pipeline.**

| Étape | Rôle |
|---|---|
| xAPI-Edu-Data.csv | Source des données |
| DLT | Ingestion |
| DuckDB | Stockage des données brutes |
| raw_data.students_raw | Données brutes |
| dbt | Transformation |
| main.stg_students | Données de staging |
| main.prepared_students | Données préparées pour le ML |
| Data Quality | Validation de la qualité |
| Business Rules | Validation des règles métier |
| Dagster | Orchestration |
| Machine Learning | Entraînement et évaluation |
| MLflow | Tracking et gestion des modèles |
| FastAPI | Exposition du modèle |
````
