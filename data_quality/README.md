# Data Quality — University Dropout Prediction

## 1. Présentation

Le dossier `data_quality/` regroupe les composants responsables de la
validation et du contrôle de la qualité des données dans le projet
**University Dropout Prediction**.

L'objectif de cette étape est de s'assurer que les données ingérées sont
complètes, cohérentes, conformes aux règles définies et suffisamment
fiables avant leur utilisation par les étapes de transformation et de
Machine Learning.

La Data Quality intervient après l'ingestion des données avec DLT et leur
stockage dans DuckDB.

Le flux général du projet est :

```text
xAPI-Edu-Data.csv
        │
        ▼
       DLT
        │
        ▼
     DuckDB
        │
        ▼
 Data Quality
        │
        ▼
       dbt
        │
        ▼
prepared_students
        │
        ▼
     Dagster
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

> Dagster constitue la couche d'orchestration. Il coordonne les différentes
> étapes du pipeline mais ne remplace ni DLT, ni dbt, ni les contrôles de
> qualité.

---

## 2. Objectifs

La Data Quality permet de :

- vérifier que le dataset n'est pas vide ;
- vérifier la présence des colonnes attendues ;
- détecter les valeurs NULL ;
- vérifier l'unicité des identifiants ;
- contrôler les valeurs catégorielles ;
- contrôler les plages des variables numériques ;
- documenter les contraintes attendues sur les données ;
- vérifier les données transformées avec les tests dbt ;
- détecter les problèmes avant l'étape de Machine Learning.

L'objectif final est de garantir que les données utilisées pour entraîner
le modèle de Machine Learning respectent les règles définies dans le projet.

---

## 3. Organisation du dossier

```text
data_quality/
│
├── data_contract.yaml
├── quality_checks.py
├── lineage.md
└── README.md
```

### `data_contract.yaml`

Le fichier `data_contract.yaml` définit les règles et contraintes attendues
sur les données.

Il permet notamment de documenter :

- les colonnes obligatoires ;
- les valeurs autorisées ;
- les contraintes de complétude ;
- les contraintes d'unicité ;
- les plages de valeurs ;
- certaines règles métier.

Le Data Contract représente donc les règles attendues pour les données.

### `quality_checks.py`

Le fichier `quality_checks.py` contient les contrôles de qualité exécutés
sur les données brutes présentes dans DuckDB.

Il vérifie notamment :

- le volume du dataset ;
- la présence des colonnes ;
- l'absence de valeurs NULL ;
- l'unicité de `_dlt_id` ;
- la validité des valeurs catégorielles ;
- les plages des variables numériques.

Le script produit un rapport indiquant pour chaque règle si elle est
respectée ou non.

### `lineage.md`

Le fichier `lineage.md` documente le parcours des données dans
l'architecture du projet.

Il permet de suivre le chemin :

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
Dagster
  ↓
Machine Learning
  ↓
MLflow
  ↓
FastAPI
```

### `README.md`

Ce fichier présente le module Data Quality, son organisation, les règles
de contrôle et les commandes permettant d'exécuter les vérifications.

---

## 4. Source des données

Le projet utilise le dataset :

```text
xAPI-Edu-Data.csv
```

Le fichier source se trouve dans :

```text
data/
└── raw/
    └── xAPI-Edu-Data.csv
```

Les données représentent différentes informations relatives aux étudiants,
à leur environnement scolaire et à leurs interactions avec les ressources
pédagogiques.

---

## 5. Ingestion des données

L'ingestion est réalisée avec **dlt**.

Le code d'ingestion se trouve dans :

```text
dataops/
└── dlt/
    ├── ingest_data.py
    ├── check_db.py
    └── README.md
```

Le script `ingest_data.py` :

1. lit le fichier CSV ;
2. nettoie les noms des colonnes ;
3. crée le pipeline dlt ;
4. charge les données dans DuckDB ;
5. crée ou remplace la table `students_raw`.

La configuration actuelle du pipeline est :

```text
Pipeline name : student_pipeline
Destination   : duckdb
Dataset       : raw_data
Table         : students_raw
```

La table obtenue est :

```text
raw_data.students_raw
```

dans la base :

```text
student_pipeline.duckdb
```

---

## 6. Stockage DuckDB

Les données brutes sont stockées dans :

```text
student_pipeline.duckdb
```

La table principale est :

```text
raw_data.students_raw
```

Cette table contient les données après ingestion ainsi que les colonnes
techniques ajoutées par dlt :

```text
_dlt_load_id
_dlt_id
```

Le fichier DuckDB est généré localement et n'est pas versionné dans Git.

Il est exclu du dépôt grâce au `.gitignore`.

La base peut donc être reconstruite à partir du dataset et du code
d'ingestion.

---

## 7. Contrôles de qualité

Les contrôles actuellement implémentés couvrent plusieurs dimensions de la
qualité des données.

### 7.1 Dataset non vide

Le premier contrôle vérifie que le dataset contient effectivement des
enregistrements.

Résultat actuel :

```text
[PASS] Dataset non vide (480 lignes)
```

### 7.2 Présence des colonnes

Le script vérifie que toutes les colonnes nécessaires sont présentes.

Les principales colonnes contrôlées sont :

```text
gender
nationality
placeofbirth
stageid
gradeid
sectionid
topic
semester
relation
raisedhands
visitedresources
announcementsview
discussion
parentansweringsurvey
parentschoolsatisfaction
studentabsencedays
class
```

### 7.3 Complétude

Les colonnes importantes sont contrôlées afin de détecter les valeurs NULL.

Exemple :

```text
[PASS] gender: aucune valeur NULL
[PASS] nationality: aucune valeur NULL
[PASS] class: aucune valeur NULL
```

---

## 8. Contrôle d'unicité

L'identifiant technique généré par dlt :

```text
_dlt_id
```

doit être unique pour chaque enregistrement.

Le dernier contrôle a donné :

```text
Total des lignes       : 480
Identifiants distincts : 480
```

Le contrôle d'unicité est donc validé.

---

## 9. Validation des valeurs catégorielles

Certaines variables sont catégorielles et doivent respecter un ensemble de
valeurs attendues.

Les contrôles concernent notamment :

```text
gender
stageid
sectionid
semester
relation
parentansweringsurvey
parentschoolsatisfaction
studentabsencedays
class
```

Par exemple, `studentabsencedays` possède les valeurs :

```text
Under-7
Above-7
```

Le contrôle vérifie qu'aucune valeur inattendue n'est présente.

---

## 10. Contrôle des variables numériques

Les variables numériques suivantes sont contrôlées :

```text
raisedhands
visitedresources
announcementsview
discussion
```

Les valeurs attendues sont comprises entre :

```text
0 et 100
```

Les valeurs observées dans les données sont :

```text
raisedhands:
    min = 0
    max = 100

visitedresources:
    min = 0
    max = 99

announcementsview:
    min = 0
    max = 98

discussion:
    min = 1
    max = 99
```

Les valeurs observées respectent donc les plages attendues.

---

## 11. Résultat du contrôle Data Quality

Le script :

```text
data_quality/quality_checks.py
```

peut être exécuté depuis la racine du projet avec :

```powershell
py data_quality\quality_checks.py
```

Le dernier contrôle a produit :

```text
==================================================

       DATA QUALITY REPORT

==================================================

[PASS] Dataset non vide (480 lignes)

[PASS] Colonne présente : gender
[PASS] Colonne présente : nationality
[PASS] Colonne présente : placeofbirth
[PASS] Colonne présente : stageid
[PASS] Colonne présente : gradeid
[PASS] Colonne présente : sectionid
[PASS] Colonne présente : topic
[PASS] Colonne présente : semester
[PASS] Colonne présente : relation
[PASS] Colonne présente : raisedhands
[PASS] Colonne présente : visitedresources
[PASS] Colonne présente : announcementsview
[PASS] Colonne présente : discussion
[PASS] Colonne présente : parentansweringsurvey
[PASS] Colonne présente : parentschoolsatisfaction
[PASS] Colonne présente : studentabsencedays
[PASS] Colonne présente : class

[PASS] _dlt_id unique

[PASS] gender: aucune valeur NULL
[PASS] nationality: aucune valeur NULL
...
[PASS] class: aucune valeur NULL

[PASS] gender: valeurs valides
[PASS] stageid: valeurs valides
[PASS] sectionid: valeurs valides
[PASS] semester: valeurs valides
[PASS] relation: valeurs valides
[PASS] parentansweringsurvey: valeurs valides
[PASS] parentschoolsatisfaction: valeurs valides
[PASS] studentabsencedays: valeurs valides
[PASS] class: valeurs valides

[PASS] raisedhands: valeurs dans [0, 100]
[PASS] visitedresources: valeurs dans [0, 100]
[PASS] announcementsview: valeurs dans [0, 100]
[PASS] discussion: valeurs dans [0, 100]

==================================================

RESULT: PASS

Toutes les règles de qualité sont respectées.

==================================================
```

---

## 12. Tests de qualité avec dbt

La qualité est également vérifiée après la transformation des données avec
dbt.

Le projet dbt se trouve dans :

```text
dataops/
└── dbt/
    └── university_dropout_dbt/
```

Les modèles concernés sont :

```text
stg_students
prepared_students
```

Les tests sont définis dans :

```text
models/schema.yml
```

Les tests actuellement définis comprennent notamment :

- `not_null` ;
- `accepted_values`.

Pour exécuter les tests :

```powershell
cd dataops\dbt\university_dropout_dbt
dbt test
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

Les 9 tests dbt ont donc été validés avec succès.

---

## 13. Transformation et qualité avec dbt

Le flux dbt est basé sur la dépendance suivante :

```text
raw_data.students_raw
        │
        ▼
   stg_students
        │
        ▼
 prepared_students
```

### `stg_students`

Le modèle `stg_students` récupère les données depuis la source déclarée
dans :

```text
models/sources.yml
```

La source est :

```text
raw_data.students_raw
```

### `prepared_students`

Le modèle `prepared_students` utilise :

```text
{{ ref('stg_students') }}
```

Il prépare les données pour les étapes suivantes.

Une transformation importante concerne :

```text
studentabsencedays
```

qui est transformée en :

```text
absence_risk
```

avec :

```text
Under-7  → 0
Above-7  → 1
```

La variable `class` est également utilisée pour créer :

```text
risk_class
```

Ces nouvelles variables sont ensuite contrôlées par les tests dbt.

---

## 14. Data Contract

Le fichier :

```text
data_contract.yaml
```

représente le contrat de données du projet.

Il permet de formaliser les attentes concernant les données avant leur
utilisation dans les étapes suivantes.

Le Data Contract peut notamment définir :

```text
- colonnes obligatoires
- valeurs autorisées
- contraintes de complétude
- contraintes d'unicité
- plages numériques
- règles métier
```

Le Data Contract permet ainsi de transformer les attentes de qualité en
règles documentées et vérifiables.

---

## 15. Position de la Data Quality dans l'architecture

La Data Quality se situe après l'ingestion et avant les étapes suivantes
du pipeline.

```text
┌──────────────────────────────┐
│ xAPI-Edu-Data.csv            │
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
│ prepared_students            │
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
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ MLflow                       │
│ Tracking + Model Registry    │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ FastAPI                      │
│ Model API                    │
└──────────────────────────────┘
```

---

## 16. Rôle de Dagster

Dagster constitue la couche d'orchestration du pipeline.

Son rôle est de coordonner les différentes étapes et leurs dépendances.

Le pipeline prévu est :

```text
DLT
 ↓
Data Quality
 ↓
dbt
 ↓
Machine Learning
 ↓
MLflow
 ↓
FastAPI
```

Dagster permettra notamment de :

- définir les dépendances entre les étapes ;
- contrôler l'ordre d'exécution ;
- automatiser les traitements ;
- suivre l'exécution du pipeline ;
- faciliter la reproductibilité des traitements.

Dagster orchestre les composants existants. Il ne remplace pas les outils
spécialisés comme DLT, dbt ou MLflow.

---

## 17. Machine Learning

Après la validation et la préparation des données, les données produites
par dbt seront utilisées pour le Machine Learning.

Le code ML est situé dans :

```text
ml/
```

Le flux sera :

```text
prepared_students
        │
        ▼
Machine Learning
        │
        ▼
     MLflow
```

---

## 18. MLflow

MLflow sera utilisé pour assurer le suivi des expériences et la gestion
des modèles.

Il permettra notamment de suivre :

- les paramètres des modèles ;
- les métriques ;
- les artefacts ;
- les différentes expériences ;
- les versions des modèles.

Le flux prévu est :

```text
Machine Learning
        │
        ▼
      MLflow
        │
        ▼
 Model Registry
```

---

## 19. FastAPI

Après l'entraînement et la validation du modèle, celui-ci sera exposé via
FastAPI.

Le code de l'API est prévu dans :

```text
api/
```

Le flux final sera :

```text
Machine Learning
        │
        ▼
      MLflow
        │
        ▼
Modèle enregistré
        │
        ▼
      FastAPI
```

---

## 20. Reproductibilité

Le fichier DuckDB généré localement n'est pas versionné dans Git.

Il est exclu grâce au `.gitignore`.

La base peut être reconstruite à partir du dataset et du code d'ingestion :

```text
xAPI-Edu-Data.csv
        │
        ▼
dataops/dlt/ingest_data.py
        │
        ▼
student_pipeline.duckdb
        │
        ▼
raw_data.students_raw
```

Les éléments importants du pipeline sont versionnés dans Git :

- code d'ingestion DLT ;
- règles Data Quality ;
- Data Contract ;
- modèles dbt ;
- tests dbt ;
- code d'orchestration ;
- code Machine Learning ;
- configuration MLflow ;
- code FastAPI.

Cette organisation permet aux membres de l'équipe de reconstruire
l'environnement de traitement à partir des éléments versionnés.

---

## 21. Commandes principales

### Recréer la base DuckDB

Depuis la racine du projet :

```powershell
py dataops\dlt\ingest_data.py
```

### Vérifier la base

```powershell
py dataops\dlt\check_db.py
```

### Exécuter les contrôles Data Quality

```powershell
py data_quality\quality_checks.py
```

### Exécuter dbt

Se placer dans le projet dbt :

```powershell
cd dataops\dbt\university_dropout_dbt
```

Puis :

```powershell
dbt debug
```

```powershell
dbt run
```

```powershell
dbt test
```

---

## 22. Résultats actuels

À l'état actuel du projet :

### Ingestion

```text
480 lignes ingérées
```

### Identifiants

```text
480 _dlt_id
480 identifiants distincts
```

### Data Quality

```text
RESULT: PASS
```

### dbt

```text
2 modèles exécutés avec succès
```

### Tests dbt

```text
9 tests
9 PASS
0 WARN
0 ERROR
```

Les contrôles actuels indiquent donc que les données respectent les règles
de qualité définies.

---

## 23. Évolutions prévues

Le module Data Quality pourra être enrichi progressivement avec :

- davantage de règles dans le Data Contract ;
- des contrôles statistiques ;
- des contrôles de distribution ;
- des contrôles de valeurs aberrantes ;
- des contrôles de fraîcheur des données ;
- l'intégration des contrôles dans Dagster ;
- l'intégration des contrôles dans la CI/CD ;
- la génération automatique de rapports de qualité.

---

## 24. Résumé

Le module `data_quality` joue un rôle central dans le pipeline
**University Dropout Prediction**.

Il permet de :

1. définir les règles de qualité avec le Data Contract ;
2. vérifier les données brutes avec `quality_checks.py` ;
3. contrôler les données transformées avec les tests dbt ;
4. documenter le parcours des données avec `lineage.md` ;
5. préparer une base fiable pour l'orchestration et le Machine Learning.

La chaîne de traitement complète est :

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

La Data Quality constitue ainsi une étape essentielle pour garantir la
fiabilité, la cohérence, la traçabilité et la reproductibilité des données
utilisées par le système de prédiction.