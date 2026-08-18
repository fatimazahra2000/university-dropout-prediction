# dataops/dagster/pipeline.py

from dagster import asset, job, op, Definitions, ScheduleDefinition


@op
def run_ingestion():
    """Etape 1 : Ingestion des donnees brutes (dlt) - Doaa"""
    from dataops.dlt.ingestion import run
    run()


@op
def run_transformation(start_after):
    """Etape 2 : Transformation des donnees (dbt) - Hasna"""
    import subprocess
    subprocess.run(["dbt", "run"], cwd="dataops/dbt", check=True)


@op
def run_quality_checks(start_after):
    """Etape 3 : Controle qualite des donnees - Hasna"""
    from data_quality.quality_checks import run_checks
    run_checks()


@job
def dropout_pipeline():
    """Pipeline complet : ingestion -> transformation -> controle qualite"""
    ingestion_result = run_ingestion()
    transformation_result = run_transformation(ingestion_result)
    run_quality_checks(transformation_result)


# Planification automatique : tous les jours a 2h du matin
daily_schedule = ScheduleDefinition(
    job=dropout_pipeline,
    cron_schedule="0 2 * * *"
)


defs = Definitions(
    jobs=[dropout_pipeline],
    schedules=[daily_schedule]
)