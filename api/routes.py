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

if hasattr(scaler, "feature_names_in_"):
    feature_names = list(scaler.feature_names_in_)
else:
    feature_names = list(joblib.load(FEATURES_PATH))

RISK_LABELS = {0: "Low Risk", 1: "Medium Risk", 2: "High Risk"}
CLASS_LETTERS = {0: "L", 1: "M", 2: "H"}

# Le pipeline DataOps (dbt) utilise desormais des noms de colonnes
# en minuscules : on les fait correspondre a ceux recus depuis l'API
RENAME_MAP = {
    "NationalITy": "nationality",
    "PlaceofBirth": "placeofbirth",
    "StageID": "stageid",
    "GradeID": "gradeid",
    "SectionID": "sectionid",
    "Topic": "topic",
    "Semester": "semester",
    "Relation": "relation",
    "ParentAnsweringSurvey": "parentansweringsurvey",
    "ParentschoolSatisfaction": "parentschoolsatisfaction",
    "StudentAbsenceDays": "studentabsencedays",
    "VisITedResources": "visitedresources",
    "AnnouncementsView": "announcementsview",
    "Discussion": "discussion",
}

CATEGORICAL_COLS = [
    "gender", "nationality", "placeofbirth", "stageid",
    "gradeid", "sectionid", "topic", "semester",
    "relation", "parentansweringsurvey",
    "parentschoolsatisfaction", "studentabsencedays"
]


def preprocess_input(data: StudentData) -> pd.DataFrame:
    df = pd.DataFrame([data.dict()]).rename(columns=RENAME_MAP)

    # Nouvelle variable engineered ajoutee par le pipeline dbt (prepared_students.sql)
    df["absence_risk"] = (df["studentabsencedays"] == "Above-7").astype(int)

    # Construction directe du vecteur final (plus fiable que pd.get_dummies
    # pour une seule requete, qui ne genere aucune colonne one-hot
    # quand une seule valeur par variable categorielle est presente)
    result = pd.DataFrame(0, index=[0], columns=feature_names)

    for col in feature_names:
        if col in df.columns:
            result[col] = df[col].values

    for col in CATEGORICAL_COLS:
        dummy_col = f"{col}_{df[col].iloc[0]}"
        if dummy_col in result.columns:
            result[dummy_col] = 1

    return result


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