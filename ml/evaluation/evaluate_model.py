import sys
import os
import joblib
import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix

# =========================================================
# GESTION AUTOMATIQUE DES CHEMINS (Même logique que le training)
# =========================================================
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))

# Chemins vers les fichiers nécessaires
data_path = os.path.join(root_dir, "data", "raw", "xAPI-Edu-Data.csv")
model_path = os.path.join(root_dir, "ml", "models", "best_model.pkl")
feature_path = os.path.join(root_dir, "ml", "models", "feature_names.pkl")

# Ajout du dossier 'ml' pour importer le preprocessing
sys.path.append(os.path.join(root_dir, "ml"))
from preprocessing.preprocess import load_and_preprocess
# =========================================================

def evaluate():
    print("--- Démarrage de l'Évaluation Finale ---")

    # 1. Vérification de l'existence du modèle
    if not os.path.exists(model_path):
        print(f"ERREUR : Le modèle est introuvable à : {model_path}")
        print("Veuillez d'abord lancer le script de training.")
        return

    # 2. Chargement des données de test
    # On réutilise load_and_preprocess pour avoir les mêmes transformations
    X_train, X_test, y_train, y_test, _ = load_and_preprocess(data_path)

    # 3. Chargement du modèle et des noms des colonnes
    model = joblib.load(model_path)
    feature_names = joblib.load(feature_path)
    
    print(f"Modèle chargé avec succès.")

    # 4. Prédictions
    y_pred = model.predict(X_test)

    # 5. Rapport de performance
    print("\n" + "="*40)
    print("   RAPPORT DE CLASSIFICATION")
    print("="*40)
    target_names = ['Low Risk (L)', 'Medium Risk (M)', 'High Risk (H)']
    print(classification_report(y_test, y_pred, target_names=target_names))

    # 6. Importance des variables (Facteurs d'abandon)
    # C'est la partie la plus importante pour ton PFA !
    if hasattr(model, 'feature_importances_'):
        print("\n" + "="*40)
        print("   TOP 5 DES FACTEURS PRÉDICTIFS")
        print("="*40)
        importances = model.feature_importances_
        feat_imp = pd.Series(importances, index=feature_names).sort_values(ascending=False)
        print(feat_imp.head(5))
        print("\nNote : Ces facteurs expliquent pourquoi un étudiant est à risque.")

if __name__ == "__main__":
    evaluate()