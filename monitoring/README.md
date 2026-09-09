# Monitoring du modèle

Ce module surveille les performances du modèle `dropout-predictor` une fois
déployé, afin de détecter une dégradation dans le temps (data drift), et
fournit un dashboard visuel de suivi.

## Fichiers

### `model_monitor.py`

- Charge le modèle depuis le MLflow Model Registry (`dropout-predictor`,
  version en production)
- Applique le scaler sauvegardé (`ml/models/scaler.pkl`) pour normaliser les
  nouvelles données de la même façon que lors de l'entraînement
- Calcule accuracy et F1-score (macro) sur un jeu de données "nouvelles"
  (ici : `data/processed/test_data.csv`, en attendant un vrai flux de
  production)
- Compare la distribution des variables (moyennes) entre les données
  d'entraînement (`train_data.csv`) et les nouvelles données pour détecter
  une dérive (drift)
- Log les résultats dans MLflow (expérience "university-dropout-prediction",
  run "monitoring-check") pour garder un historique consultable dans l'UI

### `service_monitor.py`

- Récupère tous les runs "monitoring-check" déjà loggés dans MLflow
- Génère un dashboard visuel (`dashboard.png`) avec :
  - l'évolution de l'accuracy et du F1-score dans le temps
  - l'évolution de la dérive maximale détectée (drift)

## Utilisation

1. Lancer le serveur MLflow (dans un terminal séparé, si pas déjà lancé) :
```bash
   mlflow ui
```
2. Lancer le monitoring (depuis la racine du projet) :
```bash
   python monitoring/model_monitor.py
```
3. Générer/mettre à jour le dashboard :
```bash
   python monitoring/service_monitor.py
```
4. Consulter les métriques détaillées sur http://localhost:5000, ou l'image
   `monitoring/dashboard.png` pour une vue synthétique.

## Historique — problème détecté et corrigé

Lors des premiers tests de monitoring, l'accuracy mesurée était anormalement
basse (0.29 au lieu de 0.76 attendu). La cause : le `StandardScaler` utilisé
lors du preprocessing (`ml/preprocessing/preprocess.py`) n'était pas
sauvegardé, empêchant la reproduction correcte des transformations sur de
nouvelles données. Une fois le scaler sauvegardé (`ml/models/scaler.pkl`) et
intégré dans `model_monitor.py`, l'accuracy est repassée à 0.7639, cohérente
avec le `test_accuracy` du modèle entraîné. Ce cas est visible sur le
dashboard généré (`dashboard.png`), qui montre la chute puis la correction
du drift détecté.



---

# Monitoring du service (API)

**Responsable : Soukaina**

À distinguer du monitoring du modèle ci-dessus (responsabilité de
Wijdane) : cette partie surveille la santé technique du service API
(disponibilité, temps de réponse, erreurs) — pas les performances du
modèle ML.

## Fichiers

### `api_health_monitor.py`

- Interroge l'endpoint `GET /health` de l'API
- Mesure le temps de réponse (latence) de chaque requête
- Détecte les erreurs (code HTTP différent de 200, timeout, connexion
  refusée)
- Journalise chaque vérification dans `service_metrics.csv`
  (timestamp, status_code, response_time_ms, success, error)

### `service_dashboard.py`

- Lit `service_metrics.csv`
- Génère un dashboard visuel (`service_dashboard.png`) avec :
  - l'évolution du temps de réponse dans le temps
  - l'évolution de la disponibilité (succès/échec) dans le temps
- Affiche un résumé chiffré dans le terminal (disponibilité en %,
  latence moyenne)

## Utilisation

1. S'assurer que l'API tourne (localement via Docker Compose, ou en
   production sur Komodo) :
```bash
   docker compose up -d --build api
```
2. Lancer une vérification :
```bash
   python monitoring/api_health_monitor.py
```
3. Générer/mettre à jour le dashboard :
```bash
   python monitoring/service_dashboard.py
```

## Automatisation

Un workflow GitHub Actions (`.github/workflows/service-monitoring.yml`)
exécute automatiquement `api_health_monitor.py` toutes les 15 minutes,
et conserve l'historique des métriques comme artifact téléchargeable.

L'URL de l'API à surveiller est définie via la variable de repo GitHub
`API_URL` (`Settings > Secrets and variables > Actions > Variables`).
Tant que le déploiement Cloud réel n'est pas confirmé, cette variable
n'est pas encore définie et le workflow utilise une valeur par défaut
(`http://localhost:3501`), inaccessible depuis les runners GitHub — les
exécutions échoueront donc normalement jusqu'à la mise à jour de cette
variable après déploiement (voir `docs/architecture/deploiement_cloud.md`).

## Résultats observés (tests locaux)

Lors des tests effectués en local (conteneur Docker de l'API) :
- Disponibilité mesurée : 100 % (5/5 vérifications)
- Latence moyenne : ~32 ms