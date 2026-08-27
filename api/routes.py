import os
import joblib
import pandas as pd
from fastapi import APIRouter, HTTPException
from schemas import StudentData, PredictionResponse

router = APIRouter()

# ============================================================
# Chargement du modèle, du scaler et des features au démarrage
# ============================================================

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MODEL_PATH = os.path.join(ROOT_DIR, "ml", "models", "best_model.pkl")
SCALER_PATH = os.path.join(ROOT_DIR, "ml", "models", "scaler.pkl")
FEATURES_PATH = os.path.join(ROOT_DIR, "ml", "models", "feature_names.pkl")

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

# Prefer the feature names stored by scikit-learn in the fitted scaler.
# This avoids loading an old pandas Index pickle created by another pandas version.
if hasattr(scaler, "feature_names_in_"):
    feature_names = list(scaler.feature_names_in_)
else:
    feature_names = list(joblib.load(FEATURES_PATH))

RISK_LABELS = {0: "Low Risk", 1: "Medium Risk", 2: "High Risk"}
CLASS_LETTERS = {0: "L", 1: "M", 2: "H"}

CATEGORICAL_COLS = [
    "gender", "NationalITy", "PlaceofBirth", "StageID",
    "GradeID", "SectionID", "Topic", "Semester",
    "Relation", "ParentAnsweringSurvey",
    "ParentschoolSatisfaction", "StudentAbsenceDays"
]


def preprocess_input(data: StudentData) -> pd.DataFrame:
    df = pd.DataFrame([data.dict()])

    # Même one-hot encoding que lors de l'entraînement
    df_encoded = pd.get_dummies(df, columns=CATEGORICAL_COLS, drop_first=True)

    # Aligner exactement sur les colonnes vues à l'entraînement
    # (colonnes manquantes -> 0, colonnes en trop -> supprimées)
    df_aligned = df_encoded.reindex(columns=feature_names, fill_value=0)

    return df_aligned


@router.get("/health")
def health():
    return {"status": "ok"}


@router.post("/predict", response_model=PredictionResponse)
def predict(data: StudentData):
    try:
        X = preprocess_input(data)
        X_scaled = scaler.transform(X)
        pred = model.predict(X_scaled)[0]

        return PredictionResponse(
            prediction=CLASS_LETTERS[pred],
            risk_label=RISK_LABELS[pred]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))