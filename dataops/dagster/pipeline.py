# dataops/dagster/pipeline.py
from dagster import asset, job, op, Definitions

@op
def run_ingestion():
    # Appelle dataops/dlt/ingestion.py (Doaa)
    from dataops.dlt.ingestion import run
    run()

@op
def run_transformation():
    # Déclenche les modèles dbt (Hasna)
    import subprocess
    subprocess.run(["dbt", "run"], cwd="dataops/dbt", check=True)

@op
def run_quality_checks():
    from data_quality.quality_checks import run_checks
    run_checks()

@job
def dropout_pipeline():
    run_quality_checks_dep = run_transformation()
    run_quality_checks()

defs = Definitions(jobs=[dropout_pipeline])