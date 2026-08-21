import json
import joblib
import mlflow
import mlflow.sklearn

# 1. Dire à MLflow où enregistrer
mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("university-dropout-prediction")

# 2. Charger le modèle et les fichiers déjà produits par Hasnaa
model = joblib.load("ml/models/best_model.pkl")
feature_names = joblib.load("ml/models/feature_names.pkl")

with open("ml/models/model_version.json", "r") as f:
    metadata = json.load(f)

print("Contenu du fichier :", metadata)

# 3. Démarrer un run MLflow
with mlflow.start_run(run_name="dropout-model-v1"):

    # --- Paramètres (SCRUM-81 Experiment Tracking) ---
    mlflow.log_param("model_name", metadata.get("model_name"))
    mlflow.log_param("model_version", metadata.get("model_version"))
    mlflow.log_param("dataset", metadata.get("dataset"))
    mlflow.log_param("target", metadata.get("target"))
    mlflow.log_param("training_date", metadata.get("training_date"))
    mlflow.log_param("selection_metric", metadata.get("selection_metric"))
    mlflow.log_param("status", metadata.get("status"))
    mlflow.log_param("n_features", len(feature_names))

    # --- Métriques (SCRUM-82 Metrics) ---
    mlflow.log_metric("validation_accuracy", metadata.get("validation_accuracy"))
    mlflow.log_metric("test_accuracy", metadata.get("test_accuracy"))
    mlflow.log_metric("test_f1_macro", metadata.get("test_f1_macro"))

    # --- Artefacts (SCRUM-83 Artifacts) ---
    mlflow.log_artifact("ml/evaluation/confusion_matrix.png")
    mlflow.log_artifact("ml/models/feature_names.pkl")
    mlflow.log_artifact("ml/models/model_version.json")

    # Enregistrer le modèle lui-même comme artefact MLflow
    mlflow.sklearn.log_model(model, "model")

    print("✅ Run enregistré dans MLflow avec succès.")

    # --- Model Registry (SCRUM-84) ---
    run_id = mlflow.active_run().info.run_id
    model_uri = f"runs:/{run_id}/model"
    mlflow.register_model(model_uri, "dropout-predictor")
    print("✅ Modèle enregistré dans le Model Registry.")