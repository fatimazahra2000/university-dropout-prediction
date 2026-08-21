import sys
import os
import joblib
import pandas as pd
from sklearn.metrics import classification_report

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
data_path = os.path.join(root_dir, "data", "raw", "xAPI-Edu-Data.csv")
model_path = os.path.join(root_dir, "ml", "models", "best_model.pkl")
feature_path = os.path.join(root_dir, "ml", "models", "feature_names.pkl")

sys.path.append(os.path.join(root_dir, "ml"))
from preprocessing.preprocess import load_and_preprocess

def evaluate():
    print("--- Évaluation Finale sur le Set de TEST (Données Inconnues) ---")

    if not os.path.exists(model_path):
        print("Erreur : Modèle introuvable.")
        return

    # On récupère les 3 sets mais on n'utilise que le TEST pour l'évaluation
    _, _, X_test, _, _, y_test, _ = load_and_preprocess(data_path)

    model = joblib.load(model_path)
    feature_names = joblib.load(feature_path)
    
    y_pred = model.predict(X_test)

    print("\n" + "="*40)
    print("   RAPPORT FINAL (SUR TEST SET)")
    print("="*40)
    target_names = ['Low Risk (L)', 'Medium Risk (M)', 'High Risk (H)']
    print(classification_report(y_test, y_pred, target_names=target_names))

    if hasattr(model, 'feature_importances_'):
        print("\nTOP 5 DES FACTEURS PRÉDICTIFS :")
        feat_imp = pd.Series(model.feature_importances_, index=feature_names).sort_values(ascending=False)
        print(feat_imp.head(5))

if __name__ == "__main__":
    evaluate()