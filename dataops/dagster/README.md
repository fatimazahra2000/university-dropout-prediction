# ⚙️ Orchestration — Dagster

Responsable : **Hajar**

> **Scope** : cette orchestration couvre la partie données —
> ingestion (dlt) → transformation (dbt) → qualité — **et** la partie ML/MLOps —
> préparation du jeu d'entraînement → entraînement + tracking MLflow →
> évaluation et promotion dans le Model Registry. Les deux chaînes sont
> enregistrées dans `definitions.py` et couvertes par le même job/schedule/sensor.

## Pourquoi des "Software-Defined Assets" plutôt que des `@op`/`@job` ?

Ce pipeline est fondamentalement une chaîne de **données** (raw → staging → marts)
qui se prolonge par une chaîne de **ML** (dataset → modèle → décision de promotion).
Dagster recommande dans ce cas de modéliser chaque étape comme un **asset** (une
table, un fichier, un modèle) plutôt que comme une simple tâche. Bénéfices :
- lineage visuel automatique dans l'UI, de la donnée brute jusqu'au modèle promu
- ré-exécution ciblée d'un asset et de ses dépendants uniquement
- métadonnées et aperçus attachés à chaque étape (y compris les métriques ML)

## Graphe du pipeline

```
raw_students_data (dlt → DuckDB)
        │
        ▼
dbt_transformed_data (dbt run)
        │
        ▼
data_quality_report (checks complétude/validité/unicité)
        │
        ▼
ml_training_dataset (preprocessing : split train/val/test)
        │
        ▼
trained_model (entraînement + tracking MLflow)
        │
        ▼
model_evaluation (seuil qualité → promotion dans le Model Registry)
```

## Fichiers

| Fichier | Rôle |
|---|---|
| `assets.py` | Les 3 assets du pipeline de données (ingestion, dbt, qualité) |
| `assets_ml.py` | Les 3 assets ML/MLOps (préparation dataset, entraînement + MLflow, évaluation + promotion) — **branchés dans `definitions.py`** |
| `resources.py` | Connexion DuckDB + config MLflow (tracking URI, nom d'expérience) |
| `jobs_schedules.py` | `data_pipeline_job` (couvre data + ML via `AssetSelection.all()`), schedule quotidien, sensor sur nouveaux fichiers — **actifs par défaut** (`default_status=RUNNING`) |
| `definitions.py` | Point d'entrée qui assemble le tout (data + ML + MLOps) |

---

## Est-ce automatique ?

**Oui, à deux niveaux :**
1. **Enchaînement des étapes** : une fois lancé, ingestion → dbt → qualité →
   préparation ML → entraînement → évaluation/promotion s'exécutent sans
   intervention manuelle.
2. **Déclenchement lui-même** : `daily_pipeline_schedule` et `new_raw_file_sensor`
   sont configurés en `default_status=RUNNING` — pas besoin d'aller les activer à la
   main dans l'UI. Il suffit que le **dagster-daemon** tourne en continu (voir plus
   bas) pour qu'ils se déclenchent tout seuls.

Sans le daemon qui tourne (juste `dagster dev` fermé, ou juste `run_pipeline.py`
one-shot), rien ne se relance tout seul — voir le tableau plus bas.

⚠️ **Point d'attention** : comme `data_pipeline_job` sélectionne `AssetSelection.all()`,
le schedule quotidien et le sensor déclenchent aussi l'entraînement du modèle
(`trained_model`, `model_evaluation`), pas seulement le pipeline de données. **Un
serveur MLflow doit donc être joignable** (voir `MLflowResource` dans
`resources.py`) pour que ces runs planifiés/déclenchés par le sensor réussissent —
sinon `trained_model` échoue avec une erreur explicite (`Failure` : "Serveur MLflow
injoignable"). En Docker Compose, le service `mlflow` doit être démarré avec les
autres services.

---

## Lancer en local

### Option A — un seul script, à la demande

```bash
pip install -r requirements.txt
# télécharger le dataset et le placer dans data/raw/xAPI-Edu-Data.csv
# https://www.kaggle.com/datasets/aljarah/xAPI-Edu-Data

python run_pipeline.py
```

Exécute le pipeline de **données** (ingestion → dbt → qualité) d'un coup, sans
interface. Ce script ne couvre volontairement pas la partie ML (voir Option B/C
pour matérialiser le graphe complet, ML inclus).

### Option B — Dagster avec UI + planification automatique

```bash
export DAGSTER_HOME=$(pwd)/dagster_home
# un serveur MLflow doit tourner (localhost:5000 par défaut) pour que
# trained_model / model_evaluation puissent s'exécuter
dagster dev -f dataops/dagster/definitions.py
```

Ouvre http://localhost:3000. Le schedule et le sensor sont déjà actifs (visible
dans les onglets **Schedules** / **Sensors**) : `dagster dev` fait tourner le
daemon en tâche de fond tant que la commande reste ouverte. Dans l'onglet
**Assets**, cliquer sur **Materialize all** exécute la chaîne complète
data + ML + MLOps. Pratique pour tester, mais se coupe si tu fermes le terminal.

### Option C — daemon en tâche de fond, pour une vraie automatisation continue

```bash
export DAGSTER_HOME=$(pwd)/dagster_home
dagster-daemon run -f dataops/dagster/definitions.py &
```

C'est ce process (`dagster-daemon`) qui exécute réellement les schedules et
sensors en continu, même sans UI ouverte. **Testé** : le sensor détecte un
nouveau fichier dans `data/raw/` et lance un run tout seul en quelques secondes
(ce run couvre aussi l'entraînement ML, voir l'avertissement plus haut).

---

## Déploiement en continu (Docker)

`deployment/docker-compose.yml` définit deux services :

```bash
cd deployment
docker compose up -d
```

- **dagster-webserver** : l'UI, sur `localhost:3000`
- **dagster-daemon** : le process qui fait tourner le schedule quotidien et le
  sensor en continu — **c'est lui la brique qui rend le pipeline automatique**
  en production, indépendamment de toute UI ouverte.

Les deux services partagent le volume `dagster_home/` (historique des runs,
état des schedules) et `data/` (dataset + base DuckDB). Le service `mlflow` doit
également être démarré (voir `docker-compose.yml` à la racine) pour que la partie
ML/MLOps du pipeline fonctionne dans ce déploiement.

⚠️ Docker n'a pas pu être testé dans mon environnement (accès réseau restreint) —
seule la logique `dagster-daemon` a été validée en local, hors conteneur.

---

## Planification

- `daily_pipeline_schedule` : relance tout le pipeline (données + ML/MLOps)
  chaque nuit à 2h (cron `0 2 * * *`). Modifiable directement dans
  `jobs_schedules.py`. Si tu veux que le schedule ne couvre que la partie
  données (par ex. pour ne pas dépendre de MLflow en continu), restreins la
  sélection avec `AssetSelection.groups("ingestion", "transformation", "quality")`
  au lieu de `AssetSelection.all()`.
- `new_raw_file_sensor` : surveille `data/raw/` et déclenche une exécution dès
  qu'un nouveau fichier est déposé (vérifié toutes les 60s) — couvre également
  le ré-entraînement du modèle.

Pour désactiver temporairement l'un des deux sans toucher au code : le faire
depuis l'UI (onglets **Schedules** / **Sensors**), le toggle y prévaut sur le
`default_status` du code une fois modifié une première fois.

## Ce qui reste à faire (dépend des autres modules)

Les assets appellent des fonctions déjà écrites et testées dans ce livrable :

- `dataops/dlt/ingest_data.py::ingest_student_data(database_path: str) -> int`
- `dataops/dbt/` : projet dbt complet (`dbt_project.yml`, modèles `staging`/`marts`)
- `data_quality/quality_checks.py::run_quality_checks(df) -> dict`
- `data_quality/check_business_rule.py::run_business_rules() -> dict`
- `ml/preprocessing/preprocess.py::load_and_preprocess(df)`
- `ml/training/train_model.py::train_best_model(train_csv, val_csv)`
- `ml/evaluation/evaluate_model.py::evaluate()`

Rien à modifier ici pour que le pipeline complet (data + ML + MLOps) tourne,
à condition qu'un serveur MLflow soit joignable pour les assets `trained_model`
et `model_evaluation`.