#!/usr/bin/env python3
"""
Lance le pipeline de données complet (ingestion -> dbt -> qualité), sans passer
par l'UI Dagster. Utile pour : automatisation CI/CD, cron job, ou test rapide.

Usage :
    python run_pipeline.py

Pré-requis :
    1. pip install -r requirements.txt
    2. Placer le dataset dans data/raw/xAPI-Edu-Data.csv
       (téléchargement manuel : https://www.kaggle.com/datasets/aljarah/xAPI-Edu-Data)

Pour une planification automatique récurrente, voir plutôt
`dagster dev -f dataops/dagster/definitions.py` + activer le schedule
`daily_pipeline_schedule` dans l'UI — cela gère aussi les retries, l'historique
des runs, et les alertes en cas d'échec, ce que ce script ne fait pas.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

os.environ.setdefault("DUCKDB_PATH", "data/duckdb/university.duckdb")

from dagster import materialize

from dataops.dagster.assets import (
    raw_students_data,
    dbt_transformed_data,
    data_quality_report,
)
from dataops.dagster.resources import DuckDBResource


def main():
    csv_path = "data/raw/xAPI-Edu-Data.csv"
    if not os.path.exists(csv_path):
        print(f"❌ Dataset introuvable : {csv_path}")
        print("   Télécharge-le depuis https://www.kaggle.com/datasets/aljarah/xAPI-Edu-Data")
        print("   et place-le à cet emplacement, puis relance ce script.")
        sys.exit(1)

    print("🚀 Lancement du pipeline de données (ingestion -> dbt -> qualité)...\n")

    result = materialize(
        [raw_students_data, dbt_transformed_data, data_quality_report],
        resources={
            "duckdb": DuckDBResource(database_path=os.environ["DUCKDB_PATH"]),
        },
    )

    if result.success:
        print("\n✅ Pipeline de données exécuté avec succès.")
        quality_output = result.output_for_node("data_quality_report")
        print(f"   Rapport qualité : {quality_output}")
    else:
        print("\n❌ Le pipeline a échoué. Voir les logs ci-dessus.")
        sys.exit(1)


if __name__ == "__main__":
    main()
