# API — Prédiction du décrochage universitaire

API REST FastAPI qui expose le modèle de Machine Learning (`ml/models/best_model.pkl`)
pour prédire le niveau de risque de décrochage d'un étudiant (Low / Medium / High).

## Structure

- `main.py` — point d'entrée de l'application FastAPI
- `routes.py` — définition des endpoints et logique de prédiction
  (chargement du modèle, préprocessing, scaling)
- `schemas.py` — schémas Pydantic pour valider les requêtes/réponses

## Endpoints

### `GET /health`

Vérifie que le service est en ligne.

**Réponse :**
```json
{"status": "ok"}
```

### `POST /predict`

Prédit le risque de décrochage d'un étudiant à partir de ses données.

**Corps de la requête :**
```json
{
  "gender": "M",
  "NationalITy": "Morocco",
  "PlaceofBirth": "Morocco",
  "StageID": "MiddleSchool",
  "GradeID": "G-08",
  "SectionID": "A",
  "Topic": "Math",
  "Semester": "F",
  "Relation": "Father",
  "raisedhands": 20,
  "VisITedResources": 30,
  "AnnouncementsView": 10,
  "Discussion": 15,
  "ParentAnsweringSurvey": "Yes",
  "ParentschoolSatisfaction": "Good",
  "StudentAbsenceDays": "Under-7"
}
```

**Réponse :**
```json
{
  "prediction": "L",
  "risk_label": "Low Risk"
}
```

`prediction` vaut `"L"`, `"M"` ou `"H"` (Low / Medium / High Risk).

## Lancer l'API en local (sans Docker)

Depuis la racine du projet :

```bash
cd api
uvicorn main:app --reload --port 8000
```

Documentation interactive : `http://127.0.0.1:8000/docs`

## Lancer avec Docker

Voir `deployment/README.md` pour le lancement via Docker / Docker Compose
(recommandé pour un usage autre que le développement local).

## Dépendances du modèle

L'API charge trois fichiers depuis `ml/models/` :

- `best_model.pkl` — le modèle Random Forest entraîné
- `scaler.pkl` — le `StandardScaler` utilisé à l'entraînement, appliqué aux
  nouvelles données avant prédiction
- `feature_names.pkl` — les 60 colonnes attendues par le modèle après
  one-hot encoding ; les données brutes envoyées à l'API sont encodées puis
  alignées sur ces colonnes (colonnes manquantes complétées à 0)