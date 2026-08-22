# ⚙️ Orchestration — Dagster

Responsable : **Hajar**

> **Scope** : cette orchestration couvre uniquement la partie données —
> ingestion (dlt) → transformation (dbt) → qualité. La partie ML existe en
> réserve dans `assets_ml.py` mais n'est pas branchée dans `definitions.py`.

## Pourquoi des "Software-Defined Assets" plutôt que des `@op`/`@job` ?

Ce pipeline est fondamentalement une chaîne de **données** (raw → staging → marts).
Dagster recommande dans ce cas de modéliser chaque étape comme un **asset** (une
table, un fichier) plutôt que comme une simple tâche. Bénéfices :
- lineage visuel automatique dans l'UI
- ré-exécution ciblée d'un asset et de ses dépendants uniquement
- métadonnées et aperçus attachés à chaque étape

## Graphe du pipeline

```
raw_students_data (dlt → DuckDB)
        │
        ▼
dbt_transformed_data (dbt run)
        │
        ▼
data_quality_report (checks complétude/validité/unicité)
```

## Fichiers

| Fichier | Rôle |
|---|---|
| `assets.py` | Les 3 assets du pipeline de données (ingestion, dbt, qualité) |
| `assets_ml.py` | Assets ML en réserve, non branchés par défaut |
| `resources.py` | Connexion DuckDB (+ config MLflow, réservée pour plus tard) |
| `jobs_schedules.py` | `data_pipeline_job`, schedule quotidien, sensor sur nouveaux fichiers — **actifs par défaut** (`default_status=RUNNING`) |
| `definitions.py` | Point d'entrée qui assemble le tout |

---

## Est-ce automatique ?

**Oui, à deux niveaux :**
1. **Enchaînement des étapes** : une fois lancé, ingestion → dbt → qualité s'exécutent
   sans intervention manuelle.
2. **Déclenchement lui-même** : `daily_pipeline_schedule` et `new_raw_file_sensor`
   sont configurés en `default_status=RUNNING` — pas besoin d'aller les activer à la
   main dans l'UI. Il suffit que le **dagster-daemon** tourne en continu (voir plus
   bas) pour qu'ils se déclenchent tout seuls.

Sans le daemon qui tourne (juste `dagster dev` fermé, ou juste `run_pipeline.py`
one-shot), rien ne se relance tout seul — voir le tableau plus bas.

---

## Lancer en local

### Option A — un seul script, à la demande

```bash
pip install -r requirements.txt
# télécharger le dataset et le placer dans data/raw/xAPI-Edu-Data.csv
# https://www.kaggle.com/datasets/aljarah/xAPI-Edu-Data

python run_pipeline.py
```

Exécute tout le graphe (ingestion → dbt → qualité) d'un coup, sans interface,
mais **il faut relancer la commande à chaque fois**.

### Option B — Dagster avec UI + planification automatique

```bash
export DAGSTER_HOME=$(pwd)/dagster_home
dagster dev -f dataops/dagster/definitions.py
```

Ouvre http://localhost:3000. Le schedule et le sensor sont déjà actifs (visible
dans les onglets **Schedules** / **Sensors**) : `dagster dev` fait tourner le
daemon en tâche de fond tant que la commande reste ouverte. Pratique pour tester,
mais se coupe si tu fermes le terminal.

### Option C — daemon en tâche de fond, pour une vraie automatisation continue

```bash
export DAGSTER_HOME=$(pwd)/dagster_home
dagster-daemon run -f dataops/dagster/definitions.py &
```

C'est ce process (`dagster-daemon`) qui exécute réellement les schedules et
sensors en continu, même sans UI ouverte. **Testé** : le sensor détecte un
nouveau fichier dans `data/raw/` et lance un run tout seul en quelques secondes.

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
état des schedules) et `data/` (dataset + base DuckDB).

⚠️ Docker n'a pas pu être testé dans mon environnement (accès réseau restreint) —
seule la logique `dagster-daemon` a été validée en local, hors conteneur.

---

## Planification

- `daily_pipeline_schedule` : relance tout le pipeline chaque nuit à 2h
  (cron `0 2 * * *`). Modifiable directement dans `jobs_schedules.py`.
- `new_raw_file_sensor` : surveille `data/raw/` et déclenche une exécution dès
  qu'un nouveau fichier est déposé (vérifié toutes les 60s).

Pour désactiver temporairement l'un des deux sans toucher au code : le faire
depuis l'UI (onglets **Schedules** / **Sensors**), le toggle y prévaut sur le
`default_status` du code une fois modifié une première fois.

## Ce qui reste à faire (dépend des autres modules)

Les assets appellent des fonctions déjà écrites et testées dans ce livrable :

- `dataops/dlt/ingestion.py::run_ingestion(database_path: str) -> int`
- `dataops/dbt/` : projet dbt complet (`dbt_project.yml`, modèles `staging`/`marts`)
- `data_quality/quality_checks.py::run_quality_checks(df) -> dict`

Rien à modifier ici pour que le pipeline de données tourne. Si la partie ML doit
être rebranchée plus tard, voir `assets_ml.py`.
