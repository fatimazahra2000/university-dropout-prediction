"""
Point d'entree Dagster du projet — pipeline complet Data + ML + MLflow.

Lancer Dagster en local (depuis la racine du repo) :
    dagster dev -f dataops/dagster/definitions.py

MLflow reste un service separe :
    - en Docker Compose, le service `mlflow` est demarre avec les autres services ;
    - en local, lancer d'abord un serveur MLflow sur http://127.0.0.1:5000.

Le job existant `data_pipeline_job` utilise AssetSelection.all(). En enregistrant
les assets ML ici, le job, le schedule et le sensor existants couvrent donc
maintenant automatiquement le pipeline complet.
"""

import os

from dagster import Definitions

from dataops.dagster.assets import (
    raw_students_data,
    dbt_transformed_data,
    data_quality_report,
)
from dataops.dagster.assets_ml import (
    ml_training_dataset,
    trained_model,
    model_evaluation,
)
from dataops.dagster.resources import DuckDBResource, MLflowResource
from dataops.dagster.jobs_schedules import (
    data_pipeline_job,
    daily_pipeline_schedule,
    new_raw_file_sensor,
)


# Dans Docker Compose, le hostname du service est `mlflow`.
# En execution locale, MLflow est accessible via localhost.
_default_mlflow_uri = (
    "http://mlflow:5000" if os.path.exists("/.dockerenv") else "http://127.0.0.1:5000"
)


defs = Definitions(
    assets=[
        # Data pipeline
        raw_students_data,
        dbt_transformed_data,
        data_quality_report,
        # ML pipeline
        ml_training_dataset,
        trained_model,
        model_evaluation,
    ],
    resources={
        "duckdb": DuckDBResource(),
        "mlflow_resource": MLflowResource(
            tracking_uri=os.getenv("MLFLOW_TRACKING_URI", _default_mlflow_uri),
            experiment_name=os.getenv(
                "MLFLOW_EXPERIMENT_NAME", "university-dropout-prediction"
            ),
        ),
    },
    jobs=[data_pipeline_job],
    schedules=[daily_pipeline_schedule],
    sensors=[new_raw_file_sensor],
)
