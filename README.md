# 🎓 University Dropout Prediction — MLOps & DataOps

## 📖 Description

Ce projet est réalisé dans le cadre du module **MLOps & DataOps**.

L'objectif est de développer un système intelligent permettant de **prédire le risque de décrochage universitaire** à partir des caractéristiques académiques, comportementales et démographiques des étudiants.

Le projet utilise le dataset **xAPI-Edu-Data**, disponible sur Kaggle.

Le système vise à mettre en place une chaîne complète **DataOps / MLOps**, depuis l'ingestion et la transformation des données jusqu'à l'entraînement, au versionnement, au déploiement et au monitoring du modèle.

Le projet couvre notamment :

- 📥 Ingestion automatisée avec **dlt**
- 🗄️ Stockage local avec **DuckDB**
- 🔄 Transformation avec **dbt**
- ⚙️ Orchestration avec **Dagster**
- ✅ Qualité des données et Data Contracts
- 🔗 Data Lineage
- 🤖 Machine Learning avec Scikit-Learn
- 📊 Experiment Tracking avec **MLflow**
- 📦 Versionnement du modèle
- 🚀 API REST avec **FastAPI**
- 🐳 Conteneurisation avec **Docker**
- ⚙️ CI/CD avec **GitHub Actions**
- ☁️ Déploiement Cloud
- 📈 Monitoring et observabilité

> ⚠️ **État actuel :** le projet est en phase de démarrage. Les différents composants seront développés progressivement selon les sprints Agile.

# 🛠️ Stack technique

| Domaine | Technologie |
|---|---|
| Dataset | xAPI-Edu-Data |
| Langage | Python |
| Data Ingestion | dlt |
| Stockage | DuckDB |
| Transformation | dbt |
| Orchestration | Dagster |
| Data Quality | Tests automatisés + Data Contracts |
| Data Lineage | dbt / documentation |
| Machine Learning | Scikit-Learn |
| Experiment Tracking | MLflow |
| Model Registry | MLflow Model Registry |
| API | FastAPI |
| Conteneurisation | Docker |
| CI/CD | GitHub Actions |
| Cloud | Komodo / environnement Cloud à définir |
| Versionnement | Git + GitHub |
| Gestion Agile | Jira |

# 🎯 Objectifs du projet

Le projet a pour objectifs de :

1. Collecter automatiquement les données du dataset xAPI-Edu-Data.
2. Stocker les données brutes dans DuckDB.
3. Transformer les données avec dbt.
4. Mettre en place des contrôles de qualité.
5. Définir des Data Contracts.
6. Assurer la traçabilité des données avec le Data Lineage.
7. Préparer les données pour le Machine Learning.
8. Développer un modèle de classification du risque de décrochage.
9. Évaluer les performances du modèle.
10. Versionner les modèles entraînés.
11. Suivre les expérimentations avec MLflow.
12. Exposer le modèle via une API FastAPI.
13. Conteneuriser l'application avec Docker.
14. Automatiser les tests et le build avec GitHub Actions.
15. Déployer la solution dans un environnement Cloud.
16. Mettre en place un monitoring du service et du modèle.

# 🏗️ Architecture prévue

```text
                    xAPI-Edu-Data
                          │
                          ▼
                    ┌───────────┐
                    │    dlt    │
                    │ Ingestion │
                    └─────┬─────┘
                          │
                          ▼
                    ┌───────────┐
                    │  DuckDB   │
                    │ Raw Data  │
                    └─────┬─────┘
                          │
                          ▼
                    ┌───────────┐
                    │    dbt    │
                    │Transform. │
                    └─────┬─────┘
                          │
                          ▼
                ┌─────────────────────┐
                │ Data Quality         │
                │ Tests + Contracts    │
                │ Data Lineage         │
                └──────────┬──────────┘
                           │
                           ▼
                    ┌─────────────┐
                    │ Préparation │
                    │     ML      │
                    └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
                    │  Scikit-    │
                    │   Learn     │
                    │Classification│
                    └──────┬──────┘
                           │
                           ▼
                     ┌───────────┐
                     │  MLflow   │
                     │ Tracking  │
                     │ Registry  │
                     └─────┬─────┘
                           │
                           ▼
                     ┌───────────┐
                     │  FastAPI  │
                     │ /predict  │
                     │ /health   │
                     └─────┬─────┘
                           │
                           ▼
                     ┌───────────┐
                     │  Docker   │
                     └─────┬─────┘
                           │
                           ▼
                     ┌───────────┐
                     │   Cloud   │
                     │ / Komodo  │
                     └─────┬─────┘
                           │
                           ▼
                    Monitoring &
                    Observabilité


        ┌─────────────────────────────────────┐
        │           GitHub Actions             │
        │  Tests → Vérification → Build Docker │
        └─────────────────────────────────────┘

                         ▲
                         │
                    Git / GitHub

---

# 👥 Équipe

| Membre | Responsabilité principale |
|---|---|
| **Hajar** | Product Owner + Vision du projet + Dagster |
| **Fatima** | Scrum Master + GitHub + README + support ML |
| **Doaa** | Data Engineer — dlt + DuckDB |
| **Hasna** | Analytics Engineer — dbt + Data Quality |
| **Yousra** | ML Engineer — Machine Learning |
| **Wijdane** | MLOps Engineer — MLflow + Monitoring ML |
| **Hiba** | Deployment Engineer — FastAPI + Docker |
| **Soukaina** | DevOps Engineer — CI/CD + Monitoring Service + Cloud |

# 🌿 Organisation Git

Le projet utilise une stratégie Git basée sur trois niveaux :

```text
main
  │
  └── develop
        │
        ├── feature/hajar-orchestration
        ├── feature/douaa-ingestion
        ├── feature/hasna-data-quality
        ├── feature/yousra-ml
        ├── feature/wijdane-mlflow
        ├── feature/hiba-api
        ├── feature/soukaiana-cicd
        └── feature/fatima-agile-ml

## 📌 Règles Git

### `main`

Contient uniquement les versions stables du projet.

Les membres ne doivent pas pousser directement sur `main`.

### `develop`

Branche principale de développement.

Les fonctionnalités terminées sont intégrées dans `develop` après Pull Request et vérification.

### `feature/*`

Chaque membre développe principalement sur sa branche dédiée.

Exemple :

```bash
git checkout feature/yousra-ml

---

# 🤝 Workflow de collaboration

```markdown
# 🤝 Workflow de collaboration

## 1. Récupérer le projet

```bash
git clone https://github.com/fatimazahra2000/university-dropout-prediction.git
cd university-dropout-prediction
2. Récupérer les dernières modifications
git checkout develop
git pull origin develop
3. Aller sur sa branche

Exemple pour Yousra :

git checkout feature/yousra-ml

Exemple pour Doaa :

git checkout feature/douaa-ingestion
4. Développer

Modifier ou ajouter les fichiers nécessaires.

5. Vérifier les modifications
git status
6. Ajouter les fichiers
git add .
7. Créer un commit
git commit -m "feat: ajout de la préparation des données ML"
8. Envoyer vers GitHub
git push origin feature/yousra-ml
9. Créer une Pull Request

La Pull Request doit être créée :

feature/nom-membre
        ↓
     develop

Après vérification, la Pull Request peut être fusionnée.


---

# 🔀 Pull Requests

```markdown
# 🔀 Pull Requests

Toute fonctionnalité terminée doit passer par une Pull Request.

Workflow :

```text
Feature Branch
      │
      ▼
Pull Request
      │
      ▼
Review
      │
      ▼
Tests CI/CD
      │
      ▼
develop
      │
      ▼
Version stable
      │
      ▼
main

Les Pull Requests permettent :

de vérifier le code ;
d'éviter les conflits ;
de vérifier les tests ;
de conserver un historique Git propre ;
de contrôler les modifications avant intégration.

---

```markdown
# 📋 Livrables

## Livrable 1 — Vision du projet

- Problématique
- Objectifs
- Utilisateurs cibles
- Valeur métier
- Data Strategy

**Responsable : Hajar**

---

## Livrable 2 — Gestion Agile

- Product Backlog
- User Stories
- Sprint Planning
- Sprint Review
- Sprint Retrospective
- Minimum 3 sprints

**Responsable : Fatima**

**Outil : Jira**

---

## Livrable 3 — Pipeline DataOps

- dlt
- DuckDB
- dbt
- Dagster

**Responsables :**

- dlt + DuckDB → Doaa
- dbt + qualité → Hasnaa
- Dagster → Hajar

---

## Livrable 4 — Qualité des données

- Tests de qualité
- Data Contracts
- Data Lineage
- Documentation des données

**Responsable : Hasnaa**

---

## Livrable 5 — Machine Learning

- Préparation des données
- Feature Engineering
- Entraînement
- Évaluation
- Sauvegarde du modèle

**Responsable : Yousra**

**Support : Fatima**

---

## Livrable 6 — MLOps

- Experiment Tracking
- Paramètres
- Métriques
- Artefacts
- Model Registry
- Versionnement
- Monitoring ML

**Responsable : Wijdane**

---

## Livrable 7 — Déploiement

- FastAPI
- `POST /predict`
- `GET /health`
- Docker
- Déploiement Cloud

**Responsable : Hiba**

---

## Livrable 8 — CI/CD

- GitHub Actions
- Tests automatiques
- Vérification du code
- Build Docker

**Responsable : Soukaina**

---

## Livrable 9 — Monitoring

- Disponibilité du service
- Temps de réponse
- Métriques ML
- Dérive simple

**Responsables :**

- Monitoring ML → Wijdane
- Monitoring service → Soukaina

---

## Livrable 10 — Documentation

- README
- Architecture
- Guide d'installation
- Guide d'utilisation
- Documentation Git/GitHub

**Responsable : Fatima**

# 📁 Structure du projet

```text
university-dropout-prediction/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── api/
│   └── ...
│
├── data/
│   └── ...
│
├── data_quality/
│   └── ...
│
├── dataops/
│   └── ...
│
├── deployment/
│   └── ...
│
├── docs/
│   ├── agile/
│   ├── architecture/
│   └── rapport/
│
├── ml/
│   └── ...
│
├── mlflow/
│   └── ...
│
├── monitoring/
│   └── ...
│
├── tests/
│   └── ...
│
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt

# 📥 DataOps

```markdown
# 📥 Pipeline DataOps

Le pipeline DataOps prévu est :

```text
xAPI-Edu-Data
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
      │
      ▼
   Dagster
dlt

Responsable : Doaa

Objectifs :

récupérer les données ;
automatiser l'ingestion ;
gérer le chargement ;
gérer les erreurs d'ingestion.
DuckDB

Responsable : Doaa

Objectifs :

stocker les données brutes ;
permettre leur consultation ;
fournir les données à l'étape de transformation.
dbt

Responsable : Hasna

Objectifs :

transformer les données ;
créer les modèles analytiques ;
documenter les transformations ;
effectuer des tests.
Dagster

Responsable : Hajar

Objectifs :

orchestrer le pipeline ;
organiser les différentes étapes ;
gérer les dépendances ;
suivre l'exécution du pipeline.

---

# 🧹 Qualité des données

```markdown
# 🧹 Qualité des données

Responsable : **Hasnaa**

Les contrôles prévus portent notamment sur :

- Complétude
- Validité
- Cohérence
- Intégrité
- Unicité
- Types de données
- Valeurs autorisées

Le projet intégrera également :

- Data Contracts
- Data Lineage
- Métadonnées
- Tests automatisés
🤖 Machine Learning
# 🤖 Machine Learning

Responsable : **Yousra**

Le problème est formulé comme un problème de :

**Classification du risque de décrochage universitaire.**

Les étapes prévues sont :

1. Analyse exploratoire des données
2. Nettoyage
3. Préparation
4. Feature Engineering
5. Séparation Train/Test
6. Entraînement
7. Comparaison des modèles
8. Évaluation
9. Sélection du meilleur modèle
10. Sauvegarde du modèle

Les métriques seront définies selon le problème et les modèles retenus.

### Support ML

Fatima apporte un support principalement sur :

- tests ;
- documentation ;
- vérification du fonctionnement ;
- organisation du code ML.
📊 MLflow
# 📊 MLflow

Responsable : **Wijdane**

MLflow sera utilisé pour :

- suivre les expériences ;
- enregistrer les paramètres ;
- enregistrer les métriques ;
- sauvegarder les artefacts ;
- enregistrer les modèles ;
- gérer le Model Registry ;
- assurer le versionnement des modèles.
🚀 API et Docker
# 🚀 Déploiement

Responsable : **Hiba**

Le modèle sera exposé via une API REST avec FastAPI.

Endpoints prévus :

```text
POST /predict
GET /health

L'application sera ensuite conteneurisée avec Docker.

Le déploiement final sera réalisé dans un environnement Cloud.


---

# ⚙️ CI/CD et Cloud

```markdown
# ⚙️ CI/CD & Cloud

Responsable : **Soukaina**

GitHub Actions sera utilisé pour automatiser :

1. Vérification du code
2. Installation des dépendances
3. Exécution des tests
4. Build de l'image Docker
5. Vérification de l'image
6. Préparation du déploiement

Le projet prévoit également un déploiement Cloud et un monitoring du service.

L'environnement Cloud sera précisé au cours du projet.
📈 Monitoring
# 📈 Monitoring

Le monitoring couvrira deux dimensions.

## Monitoring ML

Responsable : **Wijdane**

Suivi :

- performances du modèle ;
- métriques ML ;
- évolution des performances ;
- dérive simple.

## Monitoring du service

Responsable : **Soukaina**

Suivi :

- disponibilité ;
- temps de réponse ;
- erreurs du service ;
- état du déploiement.


# 📚 Documentation

La documentation du projet sera organisée dans `docs/`.

```text
docs/
│
├── agile/
│   ├── product_backlog.md
│   ├── user_stories.md
│   ├── sprint_1.md
│   ├── sprint_2.md
│   ├── sprint_3.md
│   ├── sprint_reviews.md
│   └── sprint_retrospectives.md
│
├── architecture/
│   ├── architecture.md
│   ├── data_lineage.md
│   └── data_strategy.md
│
└── rapport/
    └── ...

---

# 📌 État d'avancement

```markdown
# 📌 État d'avancement

| Composant | Responsable | État |
|---|---|---|
| Vision du projet | Hajar | 🟡 En préparation |
| Product Backlog | Fatima + Hajar | 🟢 Initialisé |
| GitHub | Fatima | 🟢 Initialisé |
| dlt | Doaa | 🟡 En préparation |
| DuckDB | Doaa | ⚪ À réaliser |
| dbt | Hasnaa | ⚪ À réaliser |
| Data Quality | Hasnaa | ⚪ À réaliser |
| Data Contracts | Hasnaa | ⚪ À réaliser |
| Data Lineage | Hasnaa | ⚪ À réaliser |
| Dagster | Hajar | ⚪ À réaliser |
| Machine Learning | Yousra | ⚪ À réaliser |
| MLflow | Wijdane | ⚪ À réaliser |
| Monitoring ML | Wijdane | ⚪ À réaliser |
| FastAPI | Hiba | ⚪ À réaliser |
| Docker | Hiba | ⚪ À réaliser |
| GitHub Actions | Soukaina | ⚪ À réaliser |
| Monitoring Service | Soukaina | ⚪ À réaliser |
| Cloud | Soukaina | ⚪ À réaliser |


🔐 Variables d'environnement

# 🔐 Variables d'environnement

Les variables sensibles ne doivent jamais être publiées sur GitHub.

Le fichier :

```text
.env

est ignoré par Git.

Un fichier :

.env.example

contient uniquement les noms des variables nécessaires, sans secrets réels.

Exemple :

DATA_DIR=data
DUCKDB_PATH=data/university_dropout.duckdb

MLFLOW_TRACKING_URI=http://localhost:5000

API_HOST=0.0.0.0
API_PORT=8000

CLOUD_ENVIRONMENT=

Les valeurs réelles seront définies lorsque les différents composants seront implémentés.


---

# 🧪 Tests

```markdown
# 🧪 Tests

Les tests seront regroupés dans :

```text
tests/

Ils couvriront progressivement :

ingestion ;
transformation ;
qualité des données ;
préparation ML ;
modèle ;
API ;
endpoints /predict et /health ;
intégration Docker.

Les tests seront exécutés automatiquement par GitHub Actions.


---

# 📋 Gestion Agile

```markdown
# 📋 Gestion Agile

Le projet suit une organisation Agile basée sur Scrum.

Les tâches sont gérées dans **Jira**.

Le projet comporte au minimum trois sprints :

### Sprint 1 — DataOps & Qualité

- dlt
- DuckDB
- dbt
- Data Quality
- Data Contracts
- préparation des données
- orchestration Dagster

### Sprint 2 — Machine Learning & MLOps

- Feature Engineering
- entraînement
- évaluation
- sauvegarde
- MLflow
- Model Registry
- monitoring ML


### Sprint 3 — Déploiement & Industrialisation

- FastAPI
- Docker
- CI/CD
- monitoring service
- Cloud
- validation finale

📜 Statut du projet
# 📜 Statut du projet

🚧 **Projet en cours de développement**

Le dépôt GitHub contient actuellement la structure initiale du projet et les dossiers correspondant aux différents composants.

Les prochaines étapes consistent notamment à :

1. Finaliser la configuration Git/GitHub.
2. Mettre en place le pipeline d'ingestion avec dlt.
3. Configurer DuckDB.
4. Mettre en place dbt.
5. Ajouter les tests de qualité.
6. Configurer Dagster.
7. Préparer les données pour le Machine Learning.
8. Développer et évaluer le modèle.
9. Intégrer MLflow.
10. Développer l'API FastAPI.
11. Conteneuriser l'application.
12. Mettre en place GitHub Actions.
13. Déployer dans le Cloud.
14. Mettre en place le monitoring.

🎓 Contexte académique
# 🎓 Contexte académique

Projet réalisé dans le cadre du module :

**MLOps & DataOps**

Sujet :

**Prédiction de l'abandon universitaire**

Dataset :

**xAPI-Edu-Data — Kaggle**

Le projet a pour objectif pédagogique de mettre en pratique les principes de :

- DataOps
- MLOps
- Machine Learning
- Qualité des données
- Orchestration
- CI/CD
- Conteneurisation
- Cloud
- Collaboration Git/GitHub
- Gestion Agile
<<<<<<< HEAD

=======
 📝 Bonnes pratiques
>>>>>>> 8ab946686695dd503e4ac42087b1ae4d10bf3adf
# 📝 Bonnes pratiques

✔️ Toujours travailler sur sa branche.

✔️ Faire des commits réguliers.

✔️ Écrire un message de commit clair.

✔️ Tester son code avant de pousser.

✔️ Ouvrir une Pull Request vers `develop`.

✔️ Attendre la validation avant fusion.

❌ Ne jamais travailler directement sur `main`.

❌ Ne jamais supprimer le travail d'un autre membre.

❌ Ne jamais modifier les fichiers hors de sa responsabilité sans concertation.

---
📜 Licence

# 📜 Licence

Projet académique réalisé dans le cadre du module **MLOps & DataOps**.