"""
Point d'entrée Dagster du projet — PARTIE DONNÉES (ingestion + dbt + qualité).

Lancer l'UI en local :
    dagster dev -f dataops/dagster/definitions.py

(depuis la racine du repo, avec le venv activé et DUCKDB_PATH défini si besoin,
cf. .env.example)

Note : les assets ML existent dans assets_ml.py mais ne sont volontairement pas
importés ici — ce scope se limite à la partie données. Pour les rebrancher plus
tard, voir le commentaire en haut de assets_ml.py.
"""

from dagster import Definitions

from dataops.dagster.assets import (
    raw_students_data,
    dbt_transformed_data,
    data_quality_report,
)
from dataops.dagster.resources import DuckDBResource
from dataops.dagster.jobs_schedules import (
    data_pipeline_job,
    daily_pipeline_schedule,
    new_raw_file_sensor,
)

defs = Definitions(
    assets=[
        raw_students_data,
        dbt_transformed_data,
        data_quality_report,
    ],
    resources={
        "duckdb": DuckDBResource(),
    },
    jobs=[data_pipeline_job],
    schedules=[daily_pipeline_schedule],
    sensors=[new_raw_file_sensor],
)
