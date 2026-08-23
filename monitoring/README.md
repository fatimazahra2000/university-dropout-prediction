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