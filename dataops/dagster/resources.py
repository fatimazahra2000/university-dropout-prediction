"""
Ressources partagées par les assets Dagster.
Centralise les chemins / connexions pour éviter de les recoder dans chaque asset.
"""

import os
import duckdb
from dagster import ConfigurableResource
from contextlib import contextmanager


class DuckDBResource(ConfigurableResource):
    """Donne un accès à la base DuckDB partagée du projet."""
    database_path: str = os.getenv("DUCKDB_PATH", "data/duckdb/university.duckdb")

    @contextmanager
    def get_connection(self):
        conn = duckdb.connect(self.database_path)
        try:
            yield conn
        finally:
            conn.close()


class MLflowResource(ConfigurableResource):
    """Config MLflow pour le tracking des runs d'entraînement.
    Non utilisée dans le scope actuel (partie données uniquement) — conservée
    pour assets_ml.py si la partie ML est rebranchée plus tard."""
    tracking_uri: str = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
    experiment_name: str = "university-dropout-prediction"
