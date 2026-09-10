"""
Jobs, schedule et sensor pour piloter le pipeline de données
(ingestion -> dbt -> qualité).

Le schedule et le sensor sont activés PAR DÉFAUT (default_status=RUNNING) :
dès que le dagster-daemon tourne, ils s'exécutent automatiquement, sans avoir
besoin d'aller les activer manuellement dans l'UI.
"""

from dagster import (
    define_asset_job,
    AssetSelection,
    ScheduleDefinition,
    DefaultScheduleStatus,
    sensor,
    RunRequest,
    SensorEvaluationContext,
    DefaultSensorStatus,
)

# Job qui matérialise tout le pipeline de données
data_pipeline_job = define_asset_job(
    name="data_pipeline_job",
    selection=AssetSelection.all(),
)

# Exécution planifiée : tous les jours à 2h du matin (adapter au besoin)
# default_status=RUNNING -> actif dès le démarrage du dagster-daemon, pas besoin
# de toggle manuel dans l'UI.
daily_pipeline_schedule = ScheduleDefinition(
    job=data_pipeline_job,
    cron_schedule="0 2 * * *",
    default_status=DefaultScheduleStatus.RUNNING,
)


# Sensor : si un nouveau fichier brut arrive dans data/raw/, on relance l'ingestion
# default_status=RUNNING -> actif dès le démarrage du dagster-daemon.
@sensor(
    job=data_pipeline_job,
    minimum_interval_seconds=60,
    default_status=DefaultSensorStatus.RUNNING,
)
def new_raw_file_sensor(context: SensorEvaluationContext):
    import os

    raw_dir = "data/raw"
    if not os.path.isdir(raw_dir):
        return

    current_files = set(os.listdir(raw_dir))
    last_seen = set(context.cursor.split(",")) if context.cursor else set()

    new_files = current_files - last_seen
    if new_files:
        context.update_cursor(",".join(current_files))
        yield RunRequest(run_key=f"new-files-{len(new_files)}-{context.cursor}")

