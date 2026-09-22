# 🎓 University Dropout Prediction — MLOps & DataOps

> **Projet terminé et fonctionnel ✅**
> Système complet de prédiction du risque de décrochage universitaire, industrialisé selon une approche **DataOps + Machine Learning + MLOps + DevOps**.


## 📖 Description du projet

Ce projet a été réalisé dans le cadre du module **MLOps & DataOps**.

L'objectif est de construire un système intelligent capable de **prédire le niveau de risque de décrochage universitaire** d'un étudiant à partir de ses caractéristiques :

* académiques ;
* comportementales ;
* démographiques.

Le système classe chaque étudiant dans l'une des trois catégories suivantes :

| Classe | Signification              |
| ------ | -------------------------- |
| `L`    | Low Risk — faible risque   |
| `M`    | Medium Risk — risque moyen |
| `H`    | High Risk — risque élevé   |

Le projet utilise le dataset **xAPI-Edu-Data**, contenant **480 observations et 17 variables**.

L'objectif ne se limite pas à entraîner un modèle de Machine Learning. Le projet met en place une chaîne complète permettant de passer de la donnée brute jusqu'à un service de prédiction déployé :

```text
Données brutes
     │
     ▼
   dlt
     │
     ▼
  DuckDB
     │
     ▼
   dbt
     │
     ▼
Data Quality
Data Contract
Data Lineage
     │
     ▼
 Préparation ML
     │
     ▼
Entraînement
     │
     ▼
  MLflow
Tracking + Registry
     │
     ▼
  FastAPI
     │
     ▼
   Docker
     │
     ▼
  Komodo
     │
     ▼
Déploiement Cloud
     │
     ▼
 Monitoring
```



# ✅ État final du projet

Le projet est **terminé et fonctionnel**.

Les différents composants prévus ont été implémentés et intégrés dans une chaîne cohérente :

| Composant                | Technologie                      | État                   |
| ------------------------ | -------------------------------- | ---------------------- |
| 📥 Ingestion des données | dlt                              | ✅ Terminé              |
| 🗄️ Stockage             | DuckDB                           | ✅ Terminé              |
| 🔄 Transformation        | dbt                              | ✅ Terminé              |
| 🧹 Data Quality          | Python + dbt                     | ✅ Terminé              |
| 📋 Data Contract         | YAML                             | ✅ Terminé              |
| 🔗 Data Lineage          | Documentation + dbt              | ✅ Terminé              |
| ⚙️ Orchestration         | Dagster                          | ✅ Terminé              |
| 🤖 Machine Learning      | Scikit-Learn + XGBoost           | ✅ Terminé              |
| 📊 Experiment Tracking   | MLflow                           | ✅ Terminé              |
| 📦 Model Registry        | MLflow                           | ✅ Terminé              |
| 🔢 Versionnement modèle  | JSON + MLflow                    | ✅ Terminé              |
| 🚀 API REST              | FastAPI                          | ✅ Terminé              |
| 🐳 Conteneurisation      | Docker / Docker Compose          | ✅ Terminé              |
| ⚙️ CI/CD                 | GitHub Actions                   | ✅ Terminé              |
| ☁️ Déploiement Cloud     | Komodo                           | ✅ Terminé              |
| 📈 Monitoring ML         | MLflow + scripts Python          | ✅ Terminé              |
| ❤️ Monitoring API        | Health monitoring                | ✅ Implémenté et validé |
| 📋 Gestion Agile         | Jira / Scrum                     | ✅ 3 sprints terminés   |
| 📚 Documentation         | README + documentation technique | ✅ Terminé              |


# 🎯 Objectifs du projet

Les objectifs initiaux étaient de construire une chaîne complète de traitement et d'exploitation des données.

## Objectifs atteints

1. ✅ Collecter automatiquement les données avec **dlt**.
2. ✅ Stocker les données brutes dans **DuckDB**.
3. ✅ Transformer les données avec **dbt**.
4. ✅ Contrôler la qualité des données.
5. ✅ Définir un **Data Contract**.
6. ✅ Documenter le **Data Lineage**.
7. ✅ Préparer les données pour le Machine Learning.
8. ✅ Développer plusieurs modèles de classification.
9. ✅ Comparer les modèles sur un jeu de validation.
10. ✅ Sélectionner le meilleur modèle.
11. ✅ Évaluer le modèle sur un jeu de test indépendant.
12. ✅ Versionner les modèles.
13. ✅ Suivre les expériences avec **MLflow**.
14. ✅ Enregistrer le modèle dans le **Model Registry**.
15. ✅ Exposer le modèle via une API **FastAPI**.
16. ✅ Conteneuriser l'application avec **Docker**.
17. ✅ Mettre en place une pipeline **CI/CD**.
18. ✅ Déployer l'application dans le Cloud avec **Komodo**.
19. ✅ Mettre en place le monitoring du modèle.
20. ✅ Mettre en place le monitoring de la disponibilité de l'API.


# 🏗️ Architecture globale

```text
                         ┌──────────────────────┐
                         │   xAPI-Edu-Data.csv  │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │         dlt          │
                         │      Ingestion       │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │       DuckDB         │
                         │      Raw Data        │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │         dbt          │
                         │   Transformation     │
                         │ stg → prepared      │
                         └──────────┬───────────┘
                                    │
                                    ▼
                 ┌─────────────────────────────────────┐
                 │         Data Quality                 │
                 │                                     │
                 │ • Quality Checks                     │
                 │ • Data Contract                     │
                 │ • Business Rules                    │
                 │ • Data Lineage                      │
                 └──────────────────┬──────────────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │   Préprocessing ML   │
                         │                      │
                         │ • Encoding           │
                         │ • Scaling            │
                         │ • Train / Val / Test │
                         └──────────┬───────────┘
                                    │
                                    ▼
                 ┌─────────────────────────────────────┐
                 │       Entraînement ML               │
                 │                                     │
                 │ • Logistic Regression               │
                 │ • Random Forest                     │
                 │ • XGBoost                           │
                 └──────────────────┬──────────────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │       MLflow         │
                         │                      │
                         │ • Tracking           │
                         │ • Metrics             │
                         │ • Parameters          │
                         │ • Artifacts           │
                         │ • Model Registry      │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │       FastAPI        │
                         │                      │
                         │ GET  /health         │
                         │ POST /predict        │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │        Docker        │
                         │   Docker Compose     │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │       Komodo         │
                         │    Cloud / GitOps    │
                         └──────────┬───────────┘
                                    │
                                    ▼
                    ┌──────────────────────────────┐
                    │         Monitoring           │
                    │                              │
                    │ • Model Drift                │
                    │ • Accuracy / F1              │
                    │ • API Health                 │
                    │ • Response Time              │
                    └──────────────────────────────┘


          ┌──────────────────────────────────────────┐
          │            GitHub Actions                 │
          │                                          │
          │ Tests → Docker Build → API → /health    │
          └──────────────────────────────────────────┘


          ┌──────────────────────────────────────────┐
          │                Dagster                   │
          │                                          │
          │ Raw → dbt → Quality → ML → MLflow       │
          │ → Evaluation → Model Registry           │
          └──────────────────────────────────────────┘
```


# 🛠️ Stack technique

| Domaine              | Technologie                                 |
| -------------------- | ------------------------------------------- |
| Dataset              | xAPI-Edu-Data — Kaggle                      |
| Langage              | Python 3.11                                 |
| Ingestion            | dlt                                         |
| Stockage             | DuckDB                                      |
| Transformation       | dbt                                         |
| Orchestration        | Dagster                                     |
| Data Quality         | Python + dbt                                |
| Data Contract        | YAML                                        |
| Data Lineage         | dbt + documentation                         |
| Machine Learning     | Scikit-Learn                                |
| Modèles              | Logistic Regression, Random Forest, XGBoost |
| Experiment Tracking  | MLflow                                      |
| Model Registry       | MLflow                                      |
| API                  | FastAPI + Pydantic                          |
| Conteneurisation     | Docker                                      |
| Orchestration Docker | Docker Compose                              |
| CI/CD                | GitHub Actions                              |
| Cloud                | Komodo                                      |
| Monitoring ML        | MLflow + Python                             |
| Monitoring API       | Python + GitHub Actions                     |
| Versionnement        | Git + GitHub                                |
| Gestion Agile        | Jira / Scrum                                |


# 📊 Dataset

Le projet utilise le dataset :

**xAPI-Edu-Data**

Le dataset contient :

* **480 observations**
* **17 variables**
* des informations académiques ;
* des informations comportementales ;
* des informations démographiques ;
* la variable cible `Class`.

La variable cible permet de déterminer le niveau de risque :

```text
L → Low Risk
M → Medium Risk
H → High Risk
```

Le fichier est stocké dans :

```text
data/raw/xAPI-Edu-Data.csv
```


# 📥 1. Data Ingestion — dlt

## Objectif

La première étape consiste à récupérer les données brutes et à les charger automatiquement dans DuckDB.

Le composant utilisé est :

```text
dlt
```

Pipeline :

```text
xAPI-Edu-Data.csv
        │
        ▼
       dlt
        │
        ▼
     DuckDB
```

Le script principal est :

```text
dataops/dlt/ingest_data.py
```

L'ingestion :

1. charge le fichier CSV ;
2. nettoie les noms de colonnes ;
3. initialise le pipeline dlt ;
4. crée la destination DuckDB ;
5. charge les données dans la table :

```text
raw_data.students_raw
```


# 🗄️ 2. Stockage — DuckDB

DuckDB est utilisé comme base de données analytique locale.

La base est située dans :

```text
data/duckdb/university.duckdb
```

La table brute principale est :

```text
raw_data.students_raw
```

DuckDB permet de conserver une séparation claire entre :

```text
RAW DATA
   ↓
TRANSFORMED DATA
   ↓
PREPARED DATA
```



# 🔄 3. Transformation — dbt

Après l'ingestion, les données sont transformées avec **dbt**.

Le projet dbt se trouve dans :

```text
dataops/dbt/university_dropout_dbt/
```

Les principaux modèles sont :

```text
stg_students
prepared_students
```

Pipeline :

```text
students_raw
     │
     ▼
stg_students
     │
     ▼
prepared_students
```

Les transformations permettent notamment de préparer les données pour les étapes de Data Quality et de Machine Learning.

## Tests dbt

Les tests dbt ont été exécutés avec succès :

```text
9 / 9 tests réussis ✅
```


# 🧹 4. Data Quality

La qualité des données est vérifiée avant leur utilisation par le Machine Learning.

Le dossier concerné est :

```text
data_quality/
```

Il contient notamment :

```text
data_quality/
├── data_contract.yaml
├── quality_checks.py
├── check_business_rule.py
├── lineage.md
└── README.md
```

## Contrôles réalisés

Les contrôles couvrent notamment :

* complétude ;
* valeurs NULL ;
* types de données ;
* valeurs catégorielles autorisées ;
* plages numériques ;
* unicité ;
* doublons exacts ;
* doublons métier ;
* identifiants techniques ;
* règles métier.

Le système produit un statut global :

```text
PASS
PASS_WITH_WARNINGS
FAIL
```


# 📋 5. Data Contract

Les contraintes attendues sur les données sont définies dans :

```text
data_quality/data_contract.yaml
```

Le Data Contract permet de formaliser :

* les colonnes obligatoires ;
* les types attendus ;
* les valeurs autorisées ;
* les règles de qualité ;
* les contraintes d'unicité ;
* les règles sur le volume des données.

Ainsi, le pipeline peut vérifier automatiquement que les données respectent le contrat défini.


# 🔗 6. Data Lineage

Le Data Lineage permet de suivre le cheminement des données à travers les différentes étapes du pipeline.

La documentation se trouve dans :

```text
data_quality/lineage.md
```

Vue simplifiée :

```text
xAPI-Edu-Data.csv
        │
        ▼
students_raw
        │
        ▼
stg_students
        │
        ▼
prepared_students
        │
        ▼
Dataset ML
        │
        ▼
Modèle
```


# ⚙️ 7. Orchestration — Dagster

Dagster est utilisé pour orchestrer le pipeline complet.

Contrairement à la version initiale du projet, Dagster ne se limite plus au pipeline DataOps.

Il orchestre également :

* la préparation ML ;
* l'entraînement ;
* l'évaluation ;
* l'intégration MLflow ;
* la promotion du modèle.

Le pipeline complet est donc :

```text
RAW
 ↓
dlt
 ↓
DuckDB
 ↓
dbt
 ↓
Data Quality
 ↓
ML Dataset
 ↓
Training
 ↓
Evaluation
 ↓
MLflow
 ↓
Model Registry
```

Les fichiers principaux sont :

```text
dataops/dagster/
├── assets.py
├── assets_ml.py
├── definitions.py
├── jobs_schedules.py
├── resources.py
└── Dockerfile
```

## Schedule

Un schedule quotidien est configuré :

```text
0 2 * * *
```

Le pipeline peut également être déclenché lorsqu'un nouveau fichier apparaît dans :

```text
data/raw/
```

Un sensor Dagster est utilisé pour détecter ces nouveaux fichiers.


# 🤖 8. Machine Learning

## Problème

Le problème est formulé comme un problème de **classification multiclasses**.

La cible est :

```text
Class
```

avec trois classes :

```text
L = Low Risk
M = Medium Risk
H = High Risk
```


# 🔬 9. Préprocessing

Le preprocessing est réalisé dans :

```text
ml/preprocessing/preprocess.py
```

Les principales étapes sont :

1. chargement des données préparées ;
2. séparation des variables explicatives et de la cible ;
3. suppression des variables pouvant provoquer une fuite de données ;
4. encodage des variables catégorielles ;
5. séparation Train / Validation / Test ;
6. normalisation avec `StandardScaler` ;
7. sauvegarde du scaler ;
8. sauvegarde des noms de variables.

## Séparation des données

```text
Train       → 70 % → 336 observations
Validation  → 15 % → 72 observations
Test        → 15 % → 72 observations
```

Le split utilise :

```python
random_state=42
```

et :

```python
stratify=y
```

afin de garantir la reproductibilité et de préserver la distribution des classes.


# 🔐 Prévention de la fuite de données

Une attention particulière a été portée à la **data leakage**.

La variable :

```text
risk_class
```

est retirée des variables explicatives avant l'entraînement.

Elle ne doit pas être utilisée comme feature puisqu'elle est directement liée à la variable cible.


# 🧠 10. Modèles entraînés

Trois modèles ont été comparés :

```text
Logistic Regression
Random Forest
XGBoost
```

Le meilleur modèle est sélectionné sur le jeu de **validation**.

Le jeu de test est conservé séparément et utilisé uniquement pour l'évaluation finale.


# 🏆 11. Résultats du Machine Learning

## Comparaison sur Validation

| Modèle              | Accuracy Validation |
| ------------------- | ------------------: |
| Logistic Regression |              0.6944 |
| **Random Forest**   |          **0.8194** |
| XGBoost             |              0.8056 |

Le modèle retenu est donc :

```text
Random Forest
```

avec :

```text
Validation Accuracy = 0.8194
```


# 🧪 12. Évaluation finale

Après sélection du modèle sur Validation, le modèle est évalué sur le jeu de **Test indépendant**.

Résultats :

| Métrique            | Résultat |
| ------------------- | -------: |
| Test Accuracy       | **0.76** |
| Test F1-score Macro | **0.77** |

Une matrice de confusion est également générée :

```text
ml/evaluation/confusion_matrix.png
```

L'évaluation complète est réalisée par :

```text
ml/evaluation/evaluate_model.py
```


# 📦 13. Versionnement du modèle

Les artefacts du modèle sont stockés dans :

```text
ml/models/
```

On y trouve notamment :

```text
best_model.pkl
scaler.pkl
feature_names.pkl
model_version.json
```

Le fichier :

```text
model_version.json
```

contient les informations de version du modèle.

Exemple :

```json
{
    "model_name": "Random Forest",
    "model_version": "1.0.0",
    "dataset": "xAPI-Edu-Data",
    "target": "Class",
    "training_date": "2026-08-19",
    "selection_metric": "validation_accuracy",
    "validation_accuracy": 0.8194,
    "test_accuracy": 0.76,
    "test_f1_macro": 0.77,
    "status": "validated"
}
```


# 📊 14. MLflow — Experiment Tracking

MLflow est utilisé pour assurer la traçabilité des expérimentations.

Il permet d'enregistrer :

* les paramètres ;
* les métriques ;
* les artefacts ;
* les modèles ;
* les runs ;
* les informations de version.

Le script historique de logging est :

```text
mlflow/log_to_mlflow.py
```

L'intégration Dagster → MLflow est également réalisée directement dans :

```text
dataops/dagster/assets_ml.py
```


# 📦 15. MLflow Model Registry

Le modèle validé est enregistré dans le Model Registry sous le nom :

```text
dropout-predictor
```

Le pipeline Dagster applique également un seuil de qualité sur l'accuracy de test.

Par défaut :

```text
MODEL_ACCURACY_THRESHOLD = 0.75
```

Le modèle est promu lorsque :

```text
test_accuracy >= threshold
```

Dans notre cas :

```text
0.76 >= 0.75
```

Le modèle satisfait donc le seuil de validation.


# 🔁 16. Pipeline MLflow avec Dagster

Le flux MLOps est :

```text
prepared_students
       │
       ▼
Préprocessing
       │
       ▼
Train / Validation / Test
       │
       ▼
Entraînement
       │
       ├── Logistic Regression
       ├── Random Forest
       └── XGBoost
       │
       ▼
Sélection du meilleur modèle
       │
       ▼
Random Forest
       │
       ▼
Évaluation Test
       │
       ▼
MLflow Tracking
       │
       ▼
Quality Threshold
       │
       ▼
Model Registry
       │
       ▼
dropout-predictor
```


# 🚀 17. API REST — FastAPI

Le modèle est exposé sous forme d'une API REST avec **FastAPI**.

Le code se trouve dans :

```text
api/
├── main.py
├── routes.py
├── schemas.py
└── README.md
```


## Endpoint `/health`

Méthode :

```http
GET /health
```

Rôle :

```text
Vérifier que l'API est disponible.
```

Réponse :

```json
{
  "status": "ok"
}
```


## Endpoint `/predict`

Méthode :

```http
POST /predict
```

Rôle :

```text
Prédire le niveau de risque d'un étudiant.
```

Le système reçoit les caractéristiques d'un étudiant et retourne :

```json
{
  "prediction": "L",
  "risk_label": "Low Risk"
}
```

Les trois résultats possibles sont :

```text
L → Low Risk
M → Medium Risk
H → High Risk
```


# 🔧 18. Préparation des données dans l'API

L'API utilise les mêmes éléments de preprocessing que le modèle.

Elle recharge :

```text
best_model.pkl
scaler.pkl
feature_names.pkl
```

Le même `StandardScaler` utilisé lors de l'entraînement est réutilisé au moment de l'inférence.

Cela garantit que les nouvelles données sont transformées de la même manière que les données d'entraînement.


# 🐛 19. Incident de reproductibilité corrigé

Un problème important a été identifié pendant la phase de monitoring.

Initialement, le `StandardScaler` utilisé pendant l'entraînement n'était pas correctement sauvegardé/réutilisé.

Lorsqu'une nouvelle donnée était envoyée au modèle, l'accuracy observée pouvait chuter jusqu'à :

```text
0.29
```

Après correction :

```text
scaler.pkl
```

est sauvegardé pendant le preprocessing puis réutilisé systématiquement :

```text
Training
   │
   ▼
StandardScaler
   │
   └──→ scaler.pkl
             │
             ▼
        API /predict
             │
             ▼
       scaler.transform()
             │
             ▼
          Model
```

Après correction, l'accuracy mesurée est remontée à environ :

```text
0.7639
```

ce qui est cohérent avec l'accuracy obtenue sur le jeu de test.

Cette correction améliore fortement la **reproductibilité entre entraînement et inférence**.


# 🐳 20. Docker

Le projet est entièrement conteneurisé avec Docker.

Les services principaux sont :

```text
API
MLflow
Dagster Webserver
Dagster Daemon
```

Le fichier principal est :

```text
docker-compose.yml
```

Architecture :

```text
Docker Compose
│
├── api
│
├── mlflow
│
├── dagster-webserver
│
└── dagster-daemon
```


# 🌐 21. Ports locaux

## API

```text
http://localhost:3501
```

Swagger :

```text
http://localhost:3501/docs
```

## Dagster

```text
http://localhost:3502
```

## MLflow

Le serveur MLflow utilise le port interne :

```text
5000
```


# ⚙️ 22. CI/CD — GitHub Actions

Deux workflows GitHub Actions sont présents.

```text
.github/workflows/
├── ci.yml
└── service-monitoring.yml
```


## Workflow CI

Le workflow :

```text
ci.yml
```

est déclenché lors des :

* push ;
* Pull Requests.

Il réalise notamment :

```text
Checkout
   ↓
Installation Python
   ↓
Installation dépendances
   ↓
Tests pytest
   ↓
Build Docker
   ↓
Lancement du conteneur
   ↓
Test /health
```

Le build Docker de l'API est donc également vérifié automatiquement.


# ❤️ 23. Monitoring du service

Le fichier :

```text
monitoring/api_health_monitor.py
```

permet de surveiller la santé de l'API.

Il mesure notamment :

* disponibilité ;
* code HTTP ;
* temps de réponse ;
* erreurs.

Les métriques sont enregistrées dans :

```text
monitoring/service_metrics.csv
```


# 📈 24. Monitoring du modèle

Le monitoring ML se trouve notamment dans :

```text
monitoring/model_monitor.py
```

Il permet de suivre :

* accuracy ;
* F1-score ;
* évolution des performances ;
* drift des données.

Les métriques sont également envoyées vers MLflow.

Le dashboard généré est disponible dans :

```text
monitoring/dashboard.png
```


# 📊 25. Monitoring du service

Le projet contient également :

```text
monitoring/service_monitor.py
monitoring/service_dashboard.py
monitoring/api_health_monitor.py
```

Les éléments suivis comprennent :

```text
Disponibilité
Temps de réponse
Erreurs
État du service
```

Un dashboard est disponible dans :

```text
monitoring/service_dashboard.png
```

---

# ☁️ 26. Déploiement Cloud — Komodo

Le déploiement Cloud est réalisé avec **Komodo**.

Le déploiement utilise :

```text
Git Repository
       │
       ▼
   docker-compose.yml
       │
       ▼
     Komodo
       │
       ▼
Docker Build
       │
       ▼
Services Cloud
```

Les services déployés sont :

```text
API FastAPI
MLflow
Dagster Webserver
Dagster Daemon
```

Le déploiement est volontairement **manuel**, conformément à la consigne pédagogique.

Il n'y a pas de déploiement automatique à chaque push.


# 🚀 27. Déploiement Cloud validé

Le premier déploiement manuel a été réalisé avec succès.

Les quatre services sont opérationnels :

```text
api
mlflow
dagster-webserver
dagster-daemon
```

L'API a été vérifiée avec :

```http
GET /health
```

et retourne :

```json
{
  "status": "ok"
}
```

L'accès externe validé utilise :

```text
http://exp.s3.fsbm.ma:3501
```


# ⚠️ 28. Monitoring automatisé — précision importante

Le script de monitoring fonctionne et a été validé.

Cependant, l'automatisation complète du workflow GitHub Actions de monitoring dépend de la présence du workflow sur la **branche par défaut `main`**.

Le workflow :

```text
service-monitoring.yml
```

est actuellement présent dans la branche de développement.

Par conséquent :

```text
Monitoring script
       │
       ▼
       ✅ Fonctionnel
```

mais :

```text
GitHub Actions Scheduled Monitoring
       │
       ▼
       ⚠️ Dépend de la fusion/présence sur main
```

Cette situation ne remet pas en cause le fonctionnement du monitoring lui-même.



# 📋 29. Gestion Agile — Scrum

Le projet a été organisé selon une méthodologie **Agile Scrum**.

La gestion des tâches a été réalisée avec :

```text
Jira
```

Le projet a été organisé en **3 sprints**.



# 🏃 Sprint 1 — DataOps & Data Quality

## Objectif

Construire la base du pipeline de données.

### Travaux réalisés

* dlt ;
* DuckDB ;
* dbt ;
* transformation des données ;
* Data Quality ;
* Data Contract ;
* Data Lineage ;
* orchestration Dagster de la partie DataOps.

### Résultat

```text
Sprint 1 → ✅ Terminé
```



# 🏃 Sprint 2 — Machine Learning & MLOps

## Objectif

Construire et industrialiser la partie Machine Learning.

### Travaux réalisés

* préparation des données ;
* Feature Engineering ;
* Train / Validation / Test ;
* entraînement ;
* comparaison des modèles ;
* sélection du meilleur modèle ;
* évaluation ;
* sauvegarde du modèle ;
* MLflow Tracking ;
* Model Registry ;
* versionnement ;
* monitoring ML.

### Résultat

```text
Sprint 2 → ✅ Terminé
```


# 🏃 Sprint 3 — Déploiement & Industrialisation

## Objectif

Transformer le modèle en service exploitable.

### Travaux réalisés

* FastAPI ;
* `/predict` ;
* `/health` ;
* Docker ;
* Docker Compose ;
* GitHub Actions ;
* tests automatisés ;
* monitoring API ;
* déploiement Cloud ;
* validation de l'environnement Cloud.

### Résultat

```text
Sprint 3 → ✅ Terminé
```


# 📊 30. Avancement global

| Sprint            | Domaine                         | État           |
| ----------------- | ------------------------------- | -------------- |
| Sprint 1          | DataOps & Data Quality          | 🟢 100 %       |
| Sprint 2          | ML & MLOps                      | 🟢 100 %       |
| Sprint 3          | Déploiement & Industrialisation | 🟢 100 %       |
| **Projet global** | **Data → Production**           | **🟢 Terminé** |



# 👥 31. Équipe

| Membre       | Responsabilité principale                                     |
| ------------ | ------------------------------------------------------------- |
| **Hajar**    | Product Owner, vision du projet, orchestration Dagster        |
| **Fatima**   | Scrum Master, GitHub, README, support ML & Data Quality       |
| **Doaa**     | Data Engineer — dlt + DuckDB                                  |
| **Yousra**   | Analytics/ML Engineer — dbt + contrôle qualité |
| **Hasnaa**   | Data/ML Engineer — Machine Learning                           |
| **Wijdane**  | MLOps Engineer — MLflow + Monitoring ML                       |
| **Hiba**     | Deployment Engineer — FastAPI + Docker                        |
| **Soukaina** | DevOps Engineer — CI/CD + Monitoring Service + Cloud          |



# 🌿 32. Organisation Git

Le projet utilise une organisation Git basée sur :

```text
main
 │
 └── develop
      │
      ├── feature/hajar-orchestration
      ├── feature/douaa-ingestion
      ├── feature/hasnaa-ml
      ├── feature/yousra-data
      ├── feature/wijdane-mlflow
      ├── deploiement-hiba
      ├── feature/soukaiana-cicd
      ├──feature/fatima-data-quality
      └── feature/fatima-agile-ml
```

## `main`

Contient les versions stables.

Aucun développement direct n'est réalisé sur cette branche.

## `develop`

Branche principale d'intégration.

Les fonctionnalités sont fusionnées après Pull Request et vérification.

## `feature/*`

Branches dédiées au développement de fonctionnalités.



# 🔀 33. Workflow Git

Le workflow standard est :

```text
develop
   │
   ▼
Créer / mettre à jour sa branche feature
   │
   ▼
Développement
   │
   ▼
Tests
   │
   ▼
Commit
   │
   ▼
Push
   │
   ▼
Pull Request
   │
   ▼
Code Review
   │
   ▼
GitHub Actions
   │
   ▼
develop
   │
   ▼
main
```

Commandes principales :

```bash
git checkout develop
git pull origin develop

git checkout feature/ma-feature

git status

git add .

git commit -m "feat: description de la fonctionnalité"

git push origin feature/ma-feature
```

Puis création d'une Pull Request :

```text
feature/ma-feature
        ↓
     develop
```


# 📁 34. Structure finale du projet

```text
university-dropout-prediction/
│
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── service-monitoring.yml
│
├── api/
│   ├── main.py
│   ├── routes.py
│   ├── schemas.py
│   └── README.md
│
├── data/
│   ├── raw/
│   │   └── xAPI-Edu-Data.csv
│   │
│   ├── processed/
│   │   ├── train_data.csv
│   │   ├── val_data.csv
│   │   └── test_data.csv
│   │
│   └── duckdb/
│       └── university.duckdb
│
├── data_quality/
│   ├── data_contract.yaml
│   ├── quality_checks.py
│   ├── check_business_rule.py
│   ├── lineage.md
│   └── README.md
│
├── dataops/
│   │
│   ├── dlt/
│   │   ├── ingest_data.py
│   │   ├── check_db.py
│   │   └── README.md
│   │
│   ├── dbt/
│   │   ├── profiles.yml
│   │   ├── README.md
│   │   └── university_dropout_dbt/
│   │       ├── dbt_project.yml
│   │       ├── models/
│   │       │   ├── stg_students.sql
│   │       │   ├── prepared_students.sql
│   │       │   ├── schema.yml
│   │       │   └── sources.yml
│   │       └── ...
│   │
│   └── dagster/
│       ├── assets.py
│       ├── assets_ml.py
│       ├── definitions.py
│       ├── jobs_schedules.py
│       ├── resources.py
│       ├── Dockerfile
│       └── README.md
│
├── deployment/
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── README.md
│
├── Livrables_RAPPORT/
│   ├── agile/
│   │   ├── backlog_Jira.csv
│   │   ├── user_stories.md
│   │   ├── sprint1.md
│   │   ├── sprint1_review.md
│   │   ├── sprint1_retrospective.md
│   │   ├── sprint2.md
│   │   ├── sprint2_review.md
│   │   ├── sprint2_retrospective.md
│   │   ├── sprint3.md
│   │   ├── sprint3_review.md
│   │   └── sprint3_retrospective.md
│   │
│   ├── architecture/
│   │   └── deploiement_cloud.md
│   │
│   ├── RapportFinModule.pdf
│   └── University_Dropout_Prediction.pptx
│
├── ml/
│   ├── preprocessing/
│   │   └── preprocess.py
│   │
│   ├── training/
│   │   └── train_model.py
│   │
│   ├── evaluation/
│   │   ├── evaluate_model.py
│   │   └── confusion_matrix.png
│   │
│   ├── models/
│   │   ├── best_model.pkl
│   │   ├── scaler.pkl
│   │   ├── feature_names.pkl
│   │   └── model_version.json
│   │
│   ├── notebooks/
│   │   └── EDA_Visualisation.ipynb
│   │
│   └── README.md
│
├── mlflow/
│   ├── log_to_mlflow.py
│   ├── Dockerfile
│   └── README.md
│
├── monitoring/
│   ├── model_monitor.py
│   ├── service_monitor.py
│   ├── api_health_monitor.py
│   ├── service_dashboard.py
│   ├── dashboard.png
│   ├── service_dashboard.png
│   ├── service_metrics.csv
│   └── README.md
│
├── tests/
│   └── test_api.py
│
├── .env.example
├── .gitignore
├── docker-compose.yml
├── requirements.txt
├── requirements-api.txt
├── run_pipeline.py
└── README.md
```


# ▶️ 35. Installation

## Prérequis

Installer :

* Python 3.11 ;
* Docker ;
* Docker Compose ;
* Git.


## Cloner le projet

```bash
git clone https://github.com/fatimazahra2000/university-dropout-prediction.git

cd university-dropout-prediction
```


## Créer l'environnement Python

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```


## Installer les dépendances

```bash
pip install -r requirements.txt
```


# 📥 36. Exécuter le pipeline DataOps

Le dataset doit être placé dans :

```text
data/raw/xAPI-Edu-Data.csv
```

Puis :

```bash
python run_pipeline.py
```

Le pipeline exécute :

```text
dlt
 ↓
DuckDB
 ↓
dbt
 ↓
Data Quality
```


# ⚙️ 37. Lancer Dagster

Depuis la racine du projet :

```bash
dagster dev -f dataops/dagster/definitions.py
```

Interface :

```text
http://localhost:3000
```

Dagster permet de visualiser les assets, les exécutions et les dépendances du pipeline.


# 📊 38. Lancer MLflow

```bash
mlflow ui
```

Puis :

```bash
python mlflow/log_to_mlflow.py
```

L'interface MLflow est accessible selon la configuration du serveur.

Avec Docker Compose, MLflow utilise le service :

```text
mlflow:5000
```


# 🚀 39. Lancer l'API localement

```bash
cd api

uvicorn main:app --reload --port 8000
```

L'API est alors accessible sur :

```text
http://localhost:8000
```

Swagger :

```text
http://localhost:8000/docs
```


# 🐳 40. Lancer avec Docker Compose

Depuis la racine :

```bash
docker compose up --build
```

Ou avec le fichier de déploiement :

```bash
docker compose -f deployment/docker-compose.yml up --build
```

L'API est exposée sur :

```text
http://localhost:3501
```

Swagger :

```text
http://localhost:3501/docs
```


# 🧪 41. Exécuter les tests

Les tests sont situés dans :

```text
tests/
```

Lancer :

```bash
pytest tests/ -v
```

Les tests vérifient notamment le fonctionnement de l'API et des endpoints :

```text
/health
/predict
```

---

# 📈 42. Lancer le monitoring

## Monitoring du modèle

```bash
python monitoring/model_monitor.py
```

## Monitoring du service

```bash
python monitoring/service_monitor.py
```

## Vérification de santé de l'API

```bash
python monitoring/api_health_monitor.py
```

## Dashboard du service

```bash
python monitoring/service_dashboard.py
```

---

# 🔐 43. Variables d'environnement

Les variables sensibles ne doivent pas être stockées dans Git.

Le fichier :

```text
.env
```

est ignoré par Git.

Un modèle est fourni dans :

```text
.env.example
```

Exemple :

```text
DATA_DIR=data
DUCKDB_PATH=data/university_dropout.duckdb

MLFLOW_TRACKING_URI=http://localhost:5001

API_HOST=0.0.0.0
API_PORT=8000

CLOUD_ENVIRONMENT=komodo
```

En environnement Docker, MLflow est accessible via :

```text
http://mlflow:5000
```

car les conteneurs communiquent via le réseau Docker Compose.


# 📚 44. Documentation du projet

La documentation est organisée dans :

```text
docs/
```

## Documentation Agile

```text
docs/agile/
```

Contient :

* Product Backlog ;
* User Stories ;
* Sprint 1 ;
* Sprint 2 ;
* Sprint 3 ;
* Sprint Reviews ;
* Sprint Retrospectives.

## Documentation Architecture

```text
docs/architecture/
```

Contient notamment la documentation du déploiement Cloud avec Komodo.


# 📌 45. Résumé de l'avancement

```text
                 PROJET UNIVERSITY DROPOUT PREDICTION

                         ┌───────────────┐
                         │   Dataset     │
                         │ xAPI-Edu-Data │
                         └───────┬───────┘
                                 │
                                 ▼
                         ┌───────────────┐
                         │    DataOps    │
                         │               │
                         │ dlt           │
                         │ DuckDB        │
                         │ dbt           │
                         │ Data Quality  │
                         │ Data Contract │
                         │ Data Lineage  │
                         └───────┬───────┘
                                 │
                              ✅ 100%
                                 │
                                 ▼
                         ┌───────────────┐
                         │      ML       │
                         │               │
                         │ Preprocessing │
                         │ Training      │
                         │ Evaluation    │
                         │ Random Forest │
                         └───────┬───────┘
                                 │
                              ✅ 100%
                                 │
                                 ▼
                         ┌───────────────┐
                         │    MLOps      │
                         │               │
                         │ MLflow        │
                         │ Registry      │
                         │ Versioning    │
                         │ Monitoring    │
                         └───────┬───────┘
                                 │
                              ✅ 100%
                                 │
                                 ▼
                         ┌───────────────┐
                         │ Deployment    │
                         │               │
                         │ FastAPI       │
                         │ Docker        │
                         │ CI/CD         │
                         │ Komodo        │
                         └───────┬───────┘
                                 │
                              ✅ 100%
                                 │
                                 ▼
                         ┌───────────────┐
                         │   Production  │
                         │               │
                         │ API            │
                         │ Monitoring     │
                         └───────────────┘
                                 │
                              ✅ VALIDÉ
```


# 🏆 46. Bilan final

Le projet a permis de mettre en œuvre une chaîne complète de Machine Learning industrialisée.

La solution finale couvre :

```text
Data Ingestion
      ↓
Data Storage
      ↓
Data Transformation
      ↓
Data Quality
      ↓
Data Contract
      ↓
Data Lineage
      ↓
Data Preparation
      ↓
Machine Learning
      ↓
Model Evaluation
      ↓
MLflow Tracking
      ↓
Model Registry
      ↓
FastAPI
      ↓
Docker
      ↓
CI/CD
      ↓
Cloud Deployment
      ↓
Monitoring
```

Le modèle final retenu est un :

```text
Random Forest
```

avec :

```text
Validation Accuracy = 0.8194
Test Accuracy       = 0.76
Test F1 Macro       = 0.77
```

Le modèle est versionné et validé, puis exposé à travers une API REST.

L'application a été conteneurisée avec Docker et déployée dans un environnement Cloud via Komodo.


# ⚠️ 47. Points de finalisation

Le cœur fonctionnel du projet est terminé.

# 📝 48. Bonnes pratiques suivies

✔️ Développement sur des branches dédiées.

✔️ Aucun développement direct sur `main`.

✔️ Commits réguliers et explicites.

✔️ Pull Requests avant intégration.

✔️ Revue du code.

✔️ Tests avant intégration.

✔️ Séparation DataOps / Machine Learning.

✔️ Prévention de la fuite de données.

✔️ Reproductibilité avec `random_state=42`.

✔️ Sauvegarde du scaler d'entraînement.

✔️ Versionnement du modèle.

✔️ Tracking des expériences avec MLflow.

✔️ Validation avant promotion du modèle.

✔️ Conteneurisation de l'application.

✔️ Automatisation des tests avec GitHub Actions.


# 🎓 49. Contexte académique

**Module :**

```text
MLOps & DataOps
```

**Sujet :**

```text
Prédiction de l'abandon universitaire
```

**Dataset :**

```text
xAPI-Edu-Data — Kaggle
```

**Technologies principales :**

```text
Python
dlt
DuckDB
dbt
Dagster
Scikit-Learn
XGBoost
MLflow
FastAPI
Docker
GitHub Actions
Komodo
Jira
```


# 📜 Licence

Projet académique réalisé dans le cadre du module **MLOps & DataOps**.
