"""
Assets Dagster pour la partie ML — NON branchés dans definitions.py par défaut.

Ce fichier existe pour que la partie ML (entraînement + MLflow) puisse être
raccordée facilement plus tard, sans avoir à réécrire ce qui a déjà été fait et
testé. Si tu veux l'activer : importe ces assets dans definitions.py et
ajoute-les à la liste `assets=[...]`, comme les autres.

Dépendance : ces assets requièrent que dbt_transformed_data (dans assets.py)
ait déjà été matérialisé, puisqu'ils lisent marts.students_features.
"""

import pandas as pd
from dagster import asset, AssetExecutionContext, MetadataValue, Output

from dataops.dagster.resources import DuckDBResource, MLflowResource


@asset(
    group_name="machine_learning",
    compute_kind="python",
    description="Préparation du dataset d'entraînement (ml/preprocessing).",
)
def ml_training_dataset(context: AssetExecutionContext, duckdb: DuckDBResource) -> Output[pd.DataFrame]:
    from ml.preprocessing.prepare import build_features

    with duckdb.get_connection() as conn:
        raw_df = conn.execute("SELECT * FROM marts.students_features").fetchdf()

    features_df = build_features(raw_df)

    return Output(
        features_df,
        metadata={
            "num_rows": features_df.shape[0],
            "num_columns": features_df.shape[1],
            "preview": MetadataValue.md(features_df.head().to_markdown()),
        },
    )


@asset(
    group_name="machine_learning",
    compute_kind="scikit-learn",
    description="Entraîne le modèle de classification et logge le run dans MLflow.",
)
def trained_model(
    context: AssetExecutionContext,
    ml_training_dataset: pd.DataFrame,
    mlflow_resource: MLflowResource,
) -> Output[dict]:
    from ml.training.train import train_model

    result = train_model(
        ml_training_dataset,
        tracking_uri=mlflow_resource.tracking_uri,
        experiment_name=mlflow_resource.experiment_name,
    )

    return Output(
        result,
        metadata={
            "mlflow_run_id": result.get("run_id"),
            "accuracy": result.get("accuracy"),
            "f1_score": result.get("f1"),
        },
    )


@asset(
    group_name="machine_learning",
    compute_kind="python",
    description="Évalue le modèle et décide s'il doit être promu dans le Model Registry MLflow.",
)
def model_evaluation(context: AssetExecutionContext, trained_model: dict) -> Output[dict]:
    from ml.evaluation.evaluate import evaluate_and_promote

    ACCURACY_THRESHOLD = 0.75
    decision = evaluate_and_promote(trained_model, min_accuracy=ACCURACY_THRESHOLD)

    context.log.info(f"Décision de promotion: {decision}")
    return Output(decision, metadata={"promoted": decision.get("promoted", False)})
