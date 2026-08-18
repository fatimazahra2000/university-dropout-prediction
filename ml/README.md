# 🎓 Module de Machine Learning - Prédiction de l'Abandon

Ce dossier contient l'ensemble du pipeline de Machine Learning pour prédire le risque d'abandon des étudiants en utilisant le dataset **xAPI-Edu-Data**.

## 📂 Structure du projet ML
*   **`preprocessing/`** : Scripts de nettoyage, gestion des valeurs manquantes et encodage (One-Hot Encoding).
*   **`training/`** : Comparaison de plusieurs modèles (Régression Logistique, Random Forest, XGBoost) et sélection du meilleur.
*   **`models/`** : Stockage du modèle final entraîné (`.pkl`) prêt à être déployé.
*   **`evaluation/`** : Calcul des métriques de performance (Accuracy, F1-Score) et analyse des facteurs d'abandon.
*   **`notebooks/`** : Analyse exploratoire visuelle (EDA) avec graphiques de corrélation.

## 🚀 Résultats obtenus
*   **Modèle retenu :** Random Forest
*   **Précision (Accuracy) :** 86.46%
*   **Facteurs clés identifiés :** 
    1. Participation active (Mains levées)
    2. Consultation des ressources pédagogiques
    3. Nombre d'absences (Facteur le plus critique)

## 🛠️ Installation et Exécution
1. Installer les dépendances : `pip install -r requirements.txt`
2. Entraîner le modèle : `python ml/training/train_model.py`
3. Évaluer les résultats : `python ml/evaluation/evaluate_model.py`