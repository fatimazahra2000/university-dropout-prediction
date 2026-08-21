# Data Lineage — University Dropout Prediction

## 1. Vue d'ensemble

Le Data Lineage décrit le parcours des données depuis le dataset
`xAPI-Edu-Data.csv` jusqu'à leur utilisation dans le système de
prédiction.

Le flux global du projet est :

```text
xAPI-Edu-Data.csv
        ↓
       DLT
        ↓
     DuckDB
        ↓
Data Quality
        ↓
       dbt
        ↓
stg_students
        ↓
prepared_students
        ↓
     Dagster
        ↓
Machine Learning
        ↓
     MLflow
        ↓
    FastAPI
```

Dagster assure l'orchestration des différentes étapes du pipeline.
Il coordonne l'exécution des traitements mais ne réalise pas lui-même
les transformations de données.

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

## 3. Ingestion des données

L'ingestion est réalisée avec **DLT**.

Le script d'ingestion se trouve dans :

```text
dataops/dlt/ingest_data.py
```

DLT charge les données du fichier CSV dans une base DuckDB.

La configuration actuelle est :

```text
Pipeline : student_pipeline
Destination : DuckDB
Dataset : raw_data
Table : students_raw
```

La table obtenue est :

```text
raw_data.students_raw
```

La base DuckDB utilisée localement est :

```text
student_pipeline.duckdb
```

Le fichier DuckDB n'est pas versionné dans Git car il est exclu par le
`.gitignore`.

---

## 4. Data Quality

Après l'ingestion, les données font l'objet de contrôles de qualité.

Les principaux éléments du module Data Quality sont :

```text
data_quality/
├── data_contract.yaml
├── quality_checks.py
├── lineage.md
└── README.md
```

Les contrôles portent notamment sur :

- la présence des colonnes ;
- l'absence de valeurs NULL ;
- l'unicité des identifiants ;
- la validité des valeurs catégorielles ;
- les plages des variables numériques ;
- la conformité aux règles définies.

Le script principal de contrôle est :

```text
data_quality/quality_checks.py
```

Il vérifie notamment les données présentes dans :

```text
raw_data.students_raw
```

Le dernier contrôle réalisé a donné :

```text
RESULT: PASS
```

avec 480 lignes et 480 identifiants `_dlt_id` distincts.

---

## 5. Transformation avec dbt

Après l'ingestion et les contrôles initiaux, les données sont transformées
avec **dbt**.

Le projet dbt se trouve dans :

```text
dataops/dbt/university_dropout_dbt/
```

La chaîne de transformation est :

```text
raw_data.students_raw
        ↓
stg_students
        ↓
prepared_students
```

### 5.1 `stg_students`

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

---

### 5.2 `prepared_students`

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

---

## 6. Tests dbt

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
TOTAL=9
```

Les données transformées respectent donc les règles de qualité actuellement
définies.

---

## 7. Orchestration avec Dagster

**Dagster** constitue la couche d'orchestration du pipeline.

Son rôle est de coordonner les différentes étapes et leurs dépendances.

Le flux d'orchestration prévu est :

```text
DLT
 ↓
Data Quality
 ↓
dbt
 ↓
Machine Learning
```

Dagster permet notamment de :

- définir les dépendances entre les étapes ;
- contrôler l'ordre d'exécution ;
- automatiser les traitements ;
- suivre les exécutions ;
- faciliter la reproductibilité du pipeline.

Dagster ne remplace pas les outils spécialisés.

Il orchestre les composants du pipeline.

---

## 8. Machine Learning

Après la transformation et la validation des données, les données
préparées sont utilisées pour l'étape de Machine Learning.

La source principale pour cette étape est :

```text
prepared_students
```

Le flux est :

```text
prepared_students
        ↓
Machine Learning
```

Le code Machine Learning est situé dans :

```text
ml/
```

Cette étape permettra d'entraîner et d'évaluer le modèle de prédiction
de l'abandon universitaire.

---

## 9. MLflow

**MLflow** intervient après l'entraînement du modèle.

Son rôle est d'assurer :

- le suivi des expériences ;
- l'enregistrement des paramètres ;
- le suivi des métriques ;
- la gestion des artefacts ;
- la gestion des versions des modèles.

Le flux est :

```text
Machine Learning
        ↓
     MLflow
        ↓
Model Registry
```

Les éléments liés à MLflow sont prévus dans :

```text
mlflow/
```

---

## 10. FastAPI

Une fois le modèle entraîné et enregistré, il pourra être exposé via
**FastAPI**.

Le code de l'API est prévu dans :

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
```

FastAPI permettra de rendre le modèle accessible à travers une API de
prédiction.

---

## 11. Lineage global

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
│ Data Quality                 │
│ Contract + Quality Checks    │
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
│ stg_students                 │
│ Staging                      │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ prepared_students            │
│ Données préparées            │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ Dagster                      │
│ Orchestration                │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ Machine Learning             │
│ Entraînement / évaluation    │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ MLflow                       │
│ Tracking / Registry          │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ FastAPI                      │
│ API de prédiction            │
└──────────────────────────────┘
```

---

## 12. Traçabilité et reproductibilité

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
student_pipeline.duckdb
        ↓
raw_data.students_raw
```

Cette organisation permet de conserver la traçabilité des données tout en
évitant de versionner directement les fichiers de base de données.

---

## 13. Résumé du lineage

Le Data Lineage du projet peut être résumé par la chaîne suivante :

```text
Source
  ↓
DLT
  ↓
DuckDB
  ↓
Data Quality
  ↓
dbt
  ↓
stg_students
  ↓
prepared_students
  ↓
Dagster
  ↓
Machine Learning
  ↓
MLflow
  ↓
FastAPI
```

Chaque étape possède un rôle spécifique :

| Étape | Rôle |
|---|---|
| xAPI-Edu-Data | Source des données |
| DLT | Ingestion |
| DuckDB | Stockage des données brutes |
| Data Quality | Validation de la qualité |
| dbt | Transformation |
| stg_students | Données de staging |
| prepared_students | Données préparées pour le ML |
| Dagster | Orchestration |
| Machine Learning | Entraînement et évaluation |
| MLflow | Tracking et gestion des modèles |
| FastAPI | Exposition du modèle |
