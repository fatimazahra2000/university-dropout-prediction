"""
Assets Dagster du pipeline University Dropout Prediction — PARTIE DONNÉES.

Scope de cette orchestration : ingestion -> transformation -> qualité.
(La partie ML, si besoin plus tard, est dans dataops/dagster/assets_ml.py — non
branchée par défaut dans definitions.py.)

Chaque asset appelle le code métier écrit par le membre de l'équipe responsable
(dlt -> Doaa, dbt -> Hasna, qualité -> Hasna). Dagster n'implémente PAS la logique
métier : il l'orchestre, gère les dépendances, le lineage, les retries et la
planification.

Graphe de dépendances :

    raw_students_data (dlt -> DuckDB, table raw)
            |
            v
    dbt_transformed_data (dbt run -> tables staging/marts)
            |
            v
    data_quality_report (checks de complétude/validité/unicité)
"""

import subprocess
from dagster import asset, AssetExecutionContext, MetadataValue, Output, Failure

from dataops.dagster.resources import DuckDBResource


# ---------------------------------------------------------------------------
# 1. Ingestion (dlt) -> DuckDB brute
# ---------------------------------------------------------------------------
@asset(
    group_name="ingestion",
    compute_kind="dlt",
    description="Ingestion du dataset xAPI-Edu-Data dans DuckDB via dlt (dataops/dlt/ingest_data.py).",
)
def raw_students_data(context: AssetExecutionContext, duckdb: DuckDBResource) -> Output[None]:
    # Import différé pour ne pas bloquer si le module dlt n'est pas encore prêt
    from dataops.dlt.ingest_data import ingest_student_data

    n_rows = ingest_student_data(
        database_path=duckdb.database_path
    )

    with duckdb.get_connection() as conn:
        row_count = conn.execute(
            "SELECT count(*) FROM raw_data.students_raw"
        ).fetchone()[0]

    return Output(
        None,
        metadata={
            "rows_ingested": n_rows if n_rows is not None else row_count,
            "table": "raw_data.students_raw",
        },
    )


# ---------------------------------------------------------------------------
# 2. Transformation (dbt)
# ---------------------------------------------------------------------------
@asset(
    deps=[raw_students_data],
    group_name="transformation",
    compute_kind="dbt",
    description="Exécute `dbt run` sur les modèles staging/marts (dataops/dbt).",
)
def dbt_transformed_data(context: AssetExecutionContext) -> Output[None]:
    result = subprocess.run(
        [
            "dbt",
            "run",
            "--project-dir",
            "dataops/dbt/university_dropout_dbt",
            "--profiles-dir",
            "dataops/dbt",
        ],
        capture_output=True,
        text=True,
    )
    context.log.info(result.stdout)
    if result.returncode != 0:
        raise Failure(
            description="dbt run a échoué",
            metadata={
                "stdout": MetadataValue.text(result.stdout),
                "stderr": MetadataValue.text(result.stderr),
            },
        )

    return Output(None, metadata={"dbt_stdout": MetadataValue.text(result.stdout[-2000:])})


# ---------------------------------------------------------------------------
# 3. Qualité des données
# ---------------------------------------------------------------------------
@asset(
    deps=[dbt_transformed_data],
    group_name="quality",
    compute_kind="python",
    description="Contrôles qualité (complétude, validité, unicité) sur les tables marts (data_quality/quality_checks.py).",
)
def data_quality_report(context: AssetExecutionContext, duckdb: DuckDBResource) -> Output[dict]:
    from data_quality.quality_checks import run_quality_checks

    with duckdb.get_connection() as conn:
        df = conn.execute("SELECT * FROM main.prepared_students").fetchdf()

    report = run_quality_checks(df)  # ex: {"completeness": 0.98, "duplicates": 0, "errors": []}
    print(report)

    if report.get("errors"):
        raise Failure(
            description="Contrôles qualité échoués",
            metadata={"errors": MetadataValue.json(report["errors"])},
        )

    return Output(report, metadata={k: v for k, v in report.items() if k != "errors"})