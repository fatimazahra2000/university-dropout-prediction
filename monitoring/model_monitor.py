import pandas as pd
import mlflow
import mlflow.sklearn
import joblib
from sklearn.metrics import accuracy_score, f1_score

mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("university-dropout-prediction")

# Modèle chargé depuis le Registry (pas depuis le .pkl directement)
model = mlflow.sklearn.load_model("models:/dropout-predictor/1")

# --- SCRUM-85 : métriques sur "nouvelles" données (ici : test_data.csv) ---
new_data = pd.read_csv("data/processed/test_data.csv")
X_new = new_data.drop("Target", axis=1)
y_new = new_data["Target"]

# Charger et appliquer le scaler (nécessaire car le modèle a été entraîné sur des données normalisées)
scaler = joblib.load("ml/models/scaler.pkl")
X_new = pd.DataFrame(scaler.transform(X_new), columns=X_new.columns)

y_pred = model.predict(X_new)
acc = accuracy_score(y_new, y_pred)
f1 = f1_score(y_new, y_pred, average="macro")

# --- SCRUM-86 : dérive simple (comparaison train vs "nouvelles" données) ---
reference_data = pd.read_csv("data/processed/train_data.csv").drop("Target", axis=1)
reference_data = pd.DataFrame(scaler.transform(reference_data), columns=reference_data.columns)

drift_report = pd.DataFrame({
    "mean_reference": reference_data.mean(),
    "mean_new": X_new.mean(),
})
drift_report["diff"] = (drift_report["mean_new"] - drift_report["mean_reference"]).abs()
print(drift_report.sort_values("diff", ascending=False).head(10))

# --- Log dans MLflow pour garder un historique (SCRUM-87 dashboard basique) ---
with mlflow.start_run(run_name="monitoring-check"):
    mlflow.log_metric("monitoring_accuracy", acc)
    mlflow.log_metric("monitoring_f1_macro", f1)
    mlflow.log_metric("max_feature_drift", drift_report["diff"].max())

print(f"✅ Monitoring exécuté — Accuracy: {acc:.4f}, F1: {f1:.4f}")