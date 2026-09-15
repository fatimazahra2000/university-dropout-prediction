import sys
import os

# Permet d'importer les modules du dossier api/ (main.py, routes.py, schemas.py)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "api"))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health():
    """Vérifie que l'endpoint /health répond correctement."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_predict_valid_input():
    """Vérifie que /predict renvoie une prédiction valide pour un payload correct."""
    payload = {
        "gender": "M",
        "NationalITy": "Morocco",
        "PlaceofBirth": "Morocco",
        "StageID": "MiddleSchool",
        "GradeID": "G-08",
        "SectionID": "A",
        "Topic": "Math",
        "Semester": "F",
        "Relation": "Father",
        "raisedhands": 50,
        "VisITedResources": 60,
        "AnnouncementsView": 20,
        "Discussion": 30,
        "ParentAnsweringSurvey": "Yes",
        "ParentschoolSatisfaction": "Good",
        "StudentAbsenceDays": "Under-7",
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["prediction"] in ["L", "M", "H"]
    assert data["risk_label"] in ["Low Risk", "Medium Risk", "High Risk"]


def test_predict_missing_field():
    """Vérifie que /predict rejette un payload incomplet (validation Pydantic)."""
    payload = {"gender": "F"}  # il manque presque tous les champs obligatoires
    response = client.post("/predict", json=payload)
    assert response.status_code == 422  # erreur de validation FastAPI/Pydantic