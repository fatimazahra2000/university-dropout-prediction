# Déploiement — API de prédiction du décrochage universitaire

Ce module expose le modèle de prédiction (`ml/models/best_model.pkl`) via une
API REST FastAPI, conteneurisée avec Docker.

## Structure

- `Dockerfile` — construit l'image de l'API (Python 3.11-slim + dépendances +
  code de `api/` + artefacts du modèle depuis `ml/models/`)
- `docker-compose.yml` — orchestre le conteneur de l'API (build + run)

## Endpoints exposés

- `GET /health` — vérifie que le service est en ligne
- `POST /predict` — reçoit les données d'un étudiant, retourne une prédiction
  de risque de décrochage (`L` = Low, `M` = Medium, `H` = High)

## Prérequis

- Docker Desktop installé et lancé
- Le modèle entraîné doit exister dans `ml/models/` (`best_model.pkl`,
  `scaler.pkl`, `feature_names.pkl`) — voir le module `ml/` pour l'entraînement

## Lancer l'API

Depuis la racine du projet :

```bash
docker compose -f deployment/docker-compose.yml up --build
```

L'API est alors accessible sur `http://localhost:8000`.
Documentation interactive (Swagger) : `http://localhost:8000/docs`

Pour arrêter :

```bash
docker compose -f deployment/docker-compose.yml down
```

## Exemple de requête

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
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
  }'
```

Réponse attendue :

```json
{
  "prediction": "L",
  "risk_label": "Low Risk"
}
```

## Notes techniques

- Le modèle a été entraîné sur des données normalisées avec un
  `StandardScaler` (`ml/models/scaler.pkl`) — l'API applique ce même scaler
  avant chaque prédiction pour garantir la cohérence avec l'entraînement.
- Les variables catégorielles brutes envoyées à l'API sont encodées en
  one-hot puis alignées sur les 60 colonnes vues à l'entraînement
  (`ml/models/feature_names.pkl`) ; toute colonne manquante est complétée
  à 0.
- Les versions de `pandas`, `scikit-learn`, `joblib`, `fastapi` et `uvicorn`
  sont figées dans `requirements.txt` pour éviter les incompatibilités de
  désérialisation du modèle (`.pkl`).

## Déploiement cloud

Le déploiement sur l'infrastructure cloud partagée du projet (via Komodo)
est géré au niveau du Chapitre 8 (CI/CD & Observabilité).