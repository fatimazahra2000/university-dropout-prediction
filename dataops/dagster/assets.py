"""
Assets Dagster du pipeline University Dropout Prediction — PARTIE DONNÉES.

Scope de cette orchestration :
    ingestion -> transformation -> qualité

Dagster orchestre le pipeline :
    - dépendances
    - lineage
    - exécution
    - logs
    - retries
    - planification

La logique métier reste dans :
    - dlt
    - dbt
    - data_quality
    - check_business_rule

Graphe de dépendances :

    raw_students_data
            |
            v
    dbt_transformed_data
            |
            v
    data_quality_report

Contrôles qualité :
    RAW
        - complétude
        - valeurs autorisées
        - plages numériques
        - unicité _dlt_id
        - doublons métier

    PREPARED
        - complétude
        - valeurs autorisées
        - unicité métier finale

Règles métier :
    PREPARED
        - absence_risk
        - risk_class
"""


import subprocess

from dagster import (
    asset,
    AssetExecutionContext,
    MetadataValue,
    Output,
    Failure,
)

from dataops.dagster.resources import DuckDBResource


# ---------------------------------------------------------------------------
# 1. Ingestion (dlt) -> DuckDB brute
# ---------------------------------------------------------------------------

@asset(
    group_name="ingestion",
    compute_kind="dlt",
    description=(
        "Ingestion du dataset xAPI-Edu-Data dans DuckDB "
        "via dlt (dataops/dlt/ingest_data.py)."
    ),
)
def raw_students_data(
    context: AssetExecutionContext,
    duckdb: DuckDBResource,
) -> Output[None]:

    # Import différé pour ne pas bloquer si le module dlt
    # n'est pas encore prêt.
    from dataops.dlt.ingest_data import (
        ingest_student_data,
    )

    n_rows = ingest_student_data(
        database_path=duckdb.database_path
    )

    with duckdb.get_connection() as conn:

        row_count = conn.execute(
            "SELECT COUNT(*) "
            "FROM raw_data.students_raw"
        ).fetchone()[0]

    context.log.info(
        f"RAW rows ingested: {row_count}"
    )

    return Output(
        None,
        metadata={
            "rows_ingested": (
                n_rows
                if n_rows is not None
                else row_count
            ),
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
    description=(
        "Exécute dbt run sur les modèles "
        "staging/marts (dataops/dbt)."
    ),
)
def dbt_transformed_data(
    context: AssetExecutionContext,
) -> Output[None]:

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

    context.log.info(
        result.stdout
    )

    if result.returncode != 0:

        raise Failure(
            description="dbt run a échoué",
            metadata={
                "stdout": MetadataValue.text(
                    result.stdout
                ),
                "stderr": MetadataValue.text(
                    result.stderr
                ),
            },
        )

    return Output(
        None,
        metadata={
            "dbt_stdout": MetadataValue.text(
                result.stdout[-2000:]
            )
        },
    )


# ---------------------------------------------------------------------------
# 3. Qualité des données
# ---------------------------------------------------------------------------

@asset(
    deps=[dbt_transformed_data],
    group_name="quality",
    compute_kind="python",
    description=(
        "Contrôles qualité sur les données RAW et PREPARED, "
        "puis vérification des règles métier."
    ),
)
def data_quality_report(
    context: AssetExecutionContext,
    duckdb: DuckDBResource,
) -> Output[dict]:

    from data_quality.quality_checks import (
        run_quality_checks,
    )

    from data_quality.check_business_rule import (
        run_business_rules,
    )

    # ========================================================
    # 1. Lecture des données RAW et PREPARED
    # ========================================================

    with duckdb.get_connection() as conn:

        raw_df = conn.execute(
            "SELECT * "
            "FROM raw_data.students_raw"
        ).fetchdf()

        prepared_df = conn.execute(
            "SELECT * "
            "FROM main.prepared_students"
        ).fetchdf()

    context.log.info(
        f"RAW rows: {len(raw_df)}"
    )

    context.log.info(
        f"PREPARED rows: {len(prepared_df)}"
    )

    # ========================================================
    # 2. Data Quality sur RAW
    # ========================================================

    raw_quality_report = run_quality_checks(
        raw_df,
        dataset_type="raw",
    )

    context.log.info(
        "RAW Data Quality report: "
        f"{raw_quality_report}"
    )

    # ========================================================
    # 3. Data Quality sur PREPARED
    # ========================================================

    prepared_quality_report = run_quality_checks(
        prepared_df,
        dataset_type="prepared",
    )

    context.log.info(
        "PREPARED Data Quality report: "
        f"{prepared_quality_report}"
    )

    # ========================================================
    # 4. Règles métier
    # ========================================================

    business_report = run_business_rules()

    context.log.info(
        f"Business rules report: "
        f"{business_report}"
    )

    # ========================================================
    # 5. Erreurs bloquantes
    # ========================================================

    errors = []

    # Erreurs RAW
    errors.extend(
        raw_quality_report.get(
            "errors",
            [],
        )
    )

    # Erreurs PREPARED
    errors.extend(
        prepared_quality_report.get(
            "errors",
            [],
        )
    )

    # Erreurs règles métier
    total_business_violations = (
        business_report[
            "absence_risk_violations"
        ]
        + business_report[
            "risk_class_violations"
        ]
    )

    if total_business_violations > 0:

        errors.append(
            "Des violations de règles métier "
            "ont été détectées."
        )

    # ========================================================
    # 6. Warnings
    # ========================================================

    warnings = []

    # Warnings RAW
    warnings.extend(
        raw_quality_report.get(
            "warnings",
            [],
        )
    )

    # Warnings PREPARED éventuels
    warnings.extend(
        prepared_quality_report.get(
            "warnings",
            [],
        )
    )

    # ========================================================
    # 7. Statut global
    # ========================================================

    if errors:

        status = "FAIL"

    elif warnings:

        status = "PASS_WITH_WARNINGS"

    else:

        status = "PASS"

    # ========================================================
    # 8. Rapport global
    # ========================================================

    report = {
        "raw": raw_quality_report,
        "prepared": prepared_quality_report,

        "raw_row_count": raw_quality_report[
            "row_count"
        ],

        "prepared_row_count": prepared_quality_report[
            "row_count"
        ],

        "raw_business_duplicates": raw_quality_report[
            "business_duplicates"
        ],

        "raw_business_duplicate_groups": (
            raw_quality_report[
                "business_duplicate_groups"
            ]
        ),

        "prepared_business_duplicates": (
            prepared_quality_report[
                "business_duplicates"
            ]
        ),

        **business_report,

        "errors": errors,
        "warnings": warnings,
        "status": status,

        # Compatibilité avec l'ancien rapport.
        # Le row_count principal correspond à PREPARED.
        "row_count": prepared_quality_report[
            "row_count"
        ],

        "column_count": prepared_quality_report[
            "column_count"
        ],

        "completeness": prepared_quality_report[
            "completeness"
        ],

        "duplicates": prepared_quality_report[
            "duplicates"
        ],

        "duplicate_ids": raw_quality_report[
            "duplicate_ids"
        ],
    }

    context.log.info(
        f"GLOBAL DATA QUALITY REPORT: {report}"
    )

    # ========================================================
    # 9. Affichage des warnings
    # ========================================================

    if warnings:

        context.log.warning(
            "Data Quality warnings detected: "
            f"{warnings}"
        )

    # ========================================================
    # 10. Échec uniquement pour les erreurs
    # ========================================================

    if errors:

        raise Failure(
            description=(
                "Les contrôles qualité ou les "
                "règles métier ont échoué."
            ),
            metadata={
                "errors": MetadataValue.json(
                    errors
                ),
                "warnings": MetadataValue.json(
                    warnings
                ),
            },
        )

    # ========================================================
    # 11. Matérialisation Dagster
    # ========================================================

    return Output(
        report,
        metadata={

            # ------------------------------
            # RAW
            # ------------------------------

            "raw_row_count": MetadataValue.int(
                raw_quality_report[
                    "row_count"
                ]
            ),

            "raw_column_count": MetadataValue.int(
                raw_quality_report[
                    "column_count"
                ]
            ),

            "raw_completeness": MetadataValue.float(
                raw_quality_report[
                    "completeness"
                ]
            ),

            "raw_duplicates": MetadataValue.int(
                raw_quality_report[
                    "duplicates"
                ]
            ),

            "raw_duplicate_ids": MetadataValue.int(
                raw_quality_report[
                    "duplicate_ids"
                ]
            ),

            "raw_business_duplicates": (
                MetadataValue.int(
                    raw_quality_report[
                        "business_duplicates"
                    ]
                )
            ),

            "raw_business_duplicate_groups": (
                MetadataValue.int(
                    raw_quality_report[
                        "business_duplicate_groups"
                    ]
                )
            ),

            # ------------------------------
            # PREPARED
            # ------------------------------

            "prepared_row_count": MetadataValue.int(
                prepared_quality_report[
                    "row_count"
                ]
            ),

            "prepared_column_count": (
                MetadataValue.int(
                    prepared_quality_report[
                        "column_count"
                    ]
                )
            ),

            "prepared_completeness": (
                MetadataValue.float(
                    prepared_quality_report[
                        "completeness"
                    ]
                )
            ),

            "prepared_duplicates": (
                MetadataValue.int(
                    prepared_quality_report[
                        "duplicates"
                    ]
                )
            ),

            "prepared_business_duplicates": (
                MetadataValue.int(
                    prepared_quality_report[
                        "business_duplicates"
                    ]
                )
            ),

            # ------------------------------
            # Business rules
            # ------------------------------

            "absence_risk_violations": (
                MetadataValue.int(
                    business_report[
                        "absence_risk_violations"
                    ]
                )
            ),

            "risk_class_violations": (
                MetadataValue.int(
                    business_report[
                        "risk_class_violations"
                    ]
                )
            ),

            # ------------------------------
            # Global
            # ------------------------------

            "warning_count": MetadataValue.int(
                len(warnings)
            ),

            "error_count": MetadataValue.int(
                len(errors)
            ),

            "status": MetadataValue.text(
                status
            ),
        },
    )