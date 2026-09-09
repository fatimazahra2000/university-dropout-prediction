"""
Assets Dagster pour la partie ML.

Ce module orchestre le code ML deja present dans le projet sans le reecrire :
    ml/preprocessing/preprocess.py
    ml/training/train_model.py
    ml/evaluation/evaluate_model.py

Graphe ML :
    data_quality_report
            |
            v
    ml_training_dataset
            |
            v
       trained_model  ---> run MLflow
            |
            v
      model_evaluation ---> promotion conditionnelle dans le Model Registry
"""

import json
import os
import tempfile
from pathlib import Path

import joblib
import pandas as pd
from dagster import AssetExecutionContext, Failure, MetadataValue, Output, asset
from sklearn.metrics import accuracy_score, f1_score

from dataops.dagster.assets import data_quality_report
from dataops.dagster.resources import DuckDBResource, MLflowResource


PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "xAPI-Edu-Data.csv"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
MODEL_DIR = PROJECT_ROOT / "ml" / "models"
EVALUATION_DIR = PROJECT_ROOT / "ml" / "evaluation"


def _load_split(csv_path: Path):
    """Charge un split CSV produit par preprocess.py."""
    df = pd.read_csv(csv_path)
    if "Target" not in df.columns:
        raise Failure(description=f"Colonne Target absente de {csv_path}")
    return df.drop(columns=["Target"]), df["Target"]


@asset(
    deps=[data_quality_report],
    group_name="machine_learning",
    compute_kind="scikit-learn",
    description=(
        "Prepare les jeux train/validation/test avec le preprocessing ML existant. "
        "Depend du rapport qualite afin que le ML s'execute apres le pipeline data."
    ),
)
def ml_training_dataset(
    context: AssetExecutionContext,
    duckdb: DuckDBResource,
) -> Output[dict]:
    from ml.preprocessing.preprocess import load_and_preprocess

    with duckdb.get_connection() as conn:
       prepared_df = conn.execute(
        "SELECT * FROM main.prepared_students"
    ).fetchdf()
    context.log.info(f"Nombre de lignes prepared_students : {len(prepared_df)}")
    context.log.info(f"Colonnes : {list(prepared_df.columns)}")
    context.log.info(f"Premières lignes :\n{prepared_df.head()}")
    
    X_train, X_val, X_test, y_train, y_val, y_test, feature_names = (
    load_and_preprocess(prepared_df))

    result = {
        "train_csv": str(PROCESSED_DIR / "train_data.csv"),
        "val_csv": str(PROCESSED_DIR / "val_data.csv"),
        "test_csv": str(PROCESSED_DIR / "test_data.csv"),
        "n_features": int(len(feature_names)),
    }

    return Output(
        result,
        metadata={
            "train_rows": int(len(y_train)),
            "validation_rows": int(len(y_val)),
            "test_rows": int(len(y_test)),
            "num_features": int(len(feature_names)),
            "train_csv": MetadataValue.path(result["train_csv"]),
            "validation_csv": MetadataValue.path(result["val_csv"]),
            "test_csv": MetadataValue.path(result["test_csv"]),
        },
    )


@asset(
    group_name="machine_learning",
    compute_kind="scikit-learn",
    description=(
        "Entraine le meilleur modele avec le code ML existant, evalue validation/test "
        "et enregistre le run, les metriques, le modele et les artefacts dans MLflow."
    ),
)
def trained_model(
    context: AssetExecutionContext,
    ml_training_dataset: dict,
    mlflow_resource: MLflowResource,
) -> Output[dict]:
    import mlflow
    import mlflow.sklearn
    from mlflow.tracking import MlflowClient

    from ml.training.train_model import train_best_model

    tracking_uri = mlflow_resource.tracking_uri
    experiment_name = mlflow_resource.experiment_name

    # Un run Dagster ne demarre pas le serveur MLflow. On verifie donc explicitement
    # qu'il est joignable pour donner une erreur claire si le service n'est pas lance.
    mlflow.set_tracking_uri(tracking_uri)
    try:
        MlflowClient(tracking_uri=tracking_uri).search_experiments(max_results=1)
    except Exception as exc:
        raise Failure(
            description=(
                f"Serveur MLflow injoignable sur {tracking_uri}. "
                "Lance MLflow avant de materialiser les assets ML."
            ),
            metadata={"error": MetadataValue.text(str(exc))},
        ) from exc

    context.log.info("Entrainement des modeles candidats...")
    train_best_model(
    ml_training_dataset["train_csv"],
    ml_training_dataset["val_csv"],
)

    model_path = MODEL_DIR / "best_model.pkl"
    scaler_path = MODEL_DIR / "scaler.pkl"
    feature_names_path = MODEL_DIR / "feature_names.pkl"
    metadata_path = MODEL_DIR / "model_version.json"

    required_files = [model_path, scaler_path, feature_names_path]
    missing = [str(path) for path in required_files if not path.exists()]
    if missing:
        raise Failure(description=f"Fichiers ML manquants apres entrainement: {missing}")

    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    feature_names = joblib.load(feature_names_path)

    X_val, y_val = _load_split(Path(ml_training_dataset["val_csv"]))
    X_test, y_test = _load_split(Path(ml_training_dataset["test_csv"]))

    X_val_scaled = scaler.transform(X_val)
    X_test_scaled = scaler.transform(X_test)
    y_val_pred = model.predict(X_val_scaled)
    y_test_pred = model.predict(X_test_scaled)

    validation_accuracy = float(accuracy_score(y_val, y_val_pred))
    test_accuracy = float(accuracy_score(y_test, y_test_pred))
    test_f1_macro = float(f1_score(y_test, y_test_pred, average="macro"))

    # Produit/actualise la matrice de confusion avec le code d'evaluation existant.
    try:
        from ml.evaluation.evaluate_model import evaluate

        evaluate()
    except Exception as exc:
        # La matrice est utile mais ne doit pas masquer un entrainement valide.
        context.log.warning(f"Evaluation graphique non produite: {exc}")

    project_metadata = {}
    if metadata_path.exists():
        with metadata_path.open("r", encoding="utf-8") as handle:
            project_metadata = json.load(handle)

    # Cree explicitement l'experiment avec une URI proxifiee. C'est important en
    # Docker : Dagster et MLflow n'ont pas le meme filesystem, donc les artefacts
    # doivent transiter par le serveur MLflow.
    client = MlflowClient(tracking_uri=tracking_uri)
    experiment = client.get_experiment_by_name(experiment_name)
    if experiment is None:
        experiment_id = client.create_experiment(
            experiment_name,
            artifact_location=f"mlflow-artifacts:/{experiment_name}",
        )
    else:
        experiment_id = experiment.experiment_id
        if not str(experiment.artifact_location).startswith(
            ("mlflow-artifacts:", "http://", "https://")
        ):
            context.log.warning(
                "L'experiment MLflow existe deja avec un artifact_location local: "
                f"{experiment.artifact_location}. Sur une installation neuve, supprime "
                "cet ancien experiment ou change MLFLOW_EXPERIMENT_NAME afin d'utiliser "
                "le proxy d'artefacts MLflow."
            )

    run_name = f"dagster-{model.__class__.__name__}"

    with mlflow.start_run(experiment_id=experiment_id, run_name=run_name) as run:
        mlflow.log_params(
            {
                "model_class": model.__class__.__name__,
                "dataset": project_metadata.get("dataset", "xAPI-Edu-Data"),
                "target": project_metadata.get("target", "Class"),
                "selection_metric": project_metadata.get(
                    "selection_metric", "validation_accuracy"
                ),
                "n_features": int(len(feature_names)),
                "orchestrator": "dagster",
            }
        )
        mlflow.log_metrics(
            {
                "validation_accuracy": validation_accuracy,
                "test_accuracy": test_accuracy,
                "test_f1_macro": test_f1_macro,
            }
        )

        confusion_matrix_path = EVALUATION_DIR / "confusion_matrix.png"
        if confusion_matrix_path.exists():
            mlflow.log_artifact(str(confusion_matrix_path), artifact_path="evaluation")
        if feature_names_path.exists():
            mlflow.log_artifact(str(feature_names_path), artifact_path="metadata")
        if metadata_path.exists():
            mlflow.log_artifact(str(metadata_path), artifact_path="metadata")

        # Sauvegarde locale au format MLflow puis upload generique des artefacts.
        # Cela evite de dependre des API de "logged model" recentes lorsqu'un
        # client MLflow plus recent parle au serveur 2.14.1 du projet.
        with tempfile.TemporaryDirectory(prefix="dagster-mlflow-model-") as tmp_dir:
            saved_model_dir = Path(tmp_dir) / "model"
            mlflow.sklearn.save_model(model, path=str(saved_model_dir))
            mlflow.log_artifacts(str(saved_model_dir), artifact_path="model")

        run_id = run.info.run_id

    result = {
        "run_id": run_id,
        "tracking_uri": tracking_uri,
        "experiment_name": experiment_name,
        "model_path": str(model_path),
        "model_class": model.__class__.__name__,
        "validation_accuracy": validation_accuracy,
        "test_accuracy": test_accuracy,
        "test_f1_macro": test_f1_macro,
        "model_uri": f"runs:/{run_id}/model",
    }

    return Output(
        result,
        metadata={
            "mlflow_run_id": run_id,
            "mlflow_tracking_uri": MetadataValue.url(tracking_uri),
            "experiment": experiment_name,
            "model_class": model.__class__.__name__,
            "validation_accuracy": validation_accuracy,
            "test_accuracy": test_accuracy,
            "test_f1_macro": test_f1_macro,
            "model_path": MetadataValue.path(str(model_path)),
        },
    )


@asset(
    group_name="machine_learning",
    compute_kind="mlflow",
    description=(
        "Applique un seuil de qualite et, si le modele le depasse, cree une nouvelle "
        "version dans le Model Registry MLflow."
    ),
)
def model_evaluation(
    context: AssetExecutionContext,
    trained_model: dict,
    mlflow_resource: MLflowResource,
) -> Output[dict]:
    import mlflow
    from mlflow.tracking import MlflowClient

    accuracy_threshold = float(os.getenv("MODEL_ACCURACY_THRESHOLD", "0.75"))
    test_accuracy = float(trained_model["test_accuracy"])
    promoted = test_accuracy >= accuracy_threshold

    tracking_uri = mlflow_resource.tracking_uri
    mlflow.set_tracking_uri(tracking_uri)
    client = MlflowClient(tracking_uri=tracking_uri)

    registered_model_name = "dropout-predictor"
    registered_model_version = None

    client.set_tag(
        trained_model["run_id"],
        "promotion_decision",
        "promoted" if promoted else "rejected",
    )
    client.set_tag(
        trained_model["run_id"],
        "accuracy_threshold",
        str(accuracy_threshold),
    )

    if promoted:
        try:
            model_version = mlflow.register_model(
                model_uri=trained_model["model_uri"],
                name=registered_model_name,
            )
            registered_model_version = str(model_version.version)
            context.log.info(
                f"Modele promu: {registered_model_name} v{registered_model_version}"
            )
        except Exception as exc:
            # Le tracking reste valide meme si le Registry n'est pas disponible.
            context.log.warning(f"Model Registry non disponible: {exc}")
            promoted = False

    decision = {
        "promoted": promoted,
        "test_accuracy": test_accuracy,
        "threshold": accuracy_threshold,
        "run_id": trained_model["run_id"],
        "registered_model": registered_model_name if promoted else None,
        "registered_model_version": registered_model_version,
    }

    return Output(
        decision,
        metadata={
            "promoted": promoted,
            "test_accuracy": test_accuracy,
            "accuracy_threshold": accuracy_threshold,
            "mlflow_run_id": trained_model["run_id"],
            "registered_model": registered_model_name if promoted else "not promoted",
            "registered_model_version": registered_model_version or "n/a",
        },
    )
