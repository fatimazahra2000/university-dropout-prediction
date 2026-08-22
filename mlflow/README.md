# MLflow — Experiment Tracking & Model Registry

Ce module gère le suivi des expériences (experiment tracking) et le
versionnement du modèle de prédiction du décrochage universitaire.

## Structure

- `log_to_mlflow.py` — charge le modèle et les artefacts produits par le
  module ML (`ml/models/`), les enregistre dans MLflow, puis enregistre le
  modèle dans le Model Registry
- `experiments/` — stockage local des runs MLflow (généré automatiquement,
  ignoré par Git)
- `registry/` — stockage local du Model Registry (généré automatiquement,
  ignoré par Git)

## Ce qui est loggé

**Paramètres** : nom du modèle, version, dataset, cible, date d'entraînement,
métrique de sélection, statut, nombre de features

**Métriques** : validation_accuracy, test_accuracy, test_f1_macro

**Artefacts** : matrice de confusion, feature_names.pkl, model_version.json,
le modèle sérialisé lui-même

**Registry** : le modèle est enregistré sous le nom `dropout-predictor`,
avec versionnement automatique (v1, v2, ...) à chaque nouvel enregistrement

## Utilisation

1. Lancer le serveur MLflow (dans un terminal séparé) :
   \`\`\`bash
   mlflow ui
   \`\`\`
2. Lancer le script de tracking (depuis la racine du projet) :
   \`\`\`bash
   python mlflow/log_to_mlflow.py
   \`\`\`
3. Consulter les résultats sur http://localhost:5000

## Dépendance importante

Le modèle a été entraîné sur des données normalisées avec un `StandardScaler`
(voir `ml/models/scaler.pkl`). Tout script qui charge ce modèle pour faire des
prédictions (monitoring, API...) doit appliquer ce même scaler aux nouvelles
données avant de prédire — voir `monitoring/model_monitor.py` pour un exemple.