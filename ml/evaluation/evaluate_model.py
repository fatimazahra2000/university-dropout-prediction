import sys
import os
import joblib
import pandas as pd
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay
)
import matplotlib.pyplot as plt

# ============================================================
# Chemins du projet
# ============================================================

root_dir = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../")
)

data_path = os.path.join(
    root_dir,
    "data",
    "raw",
    "xAPI-Edu-Data.csv"
)

model_path = os.path.join(
    root_dir,
    "ml",
    "models",
    "best_model.pkl"
)

feature_path = os.path.join(
    root_dir,
    "ml",
    "models",
    "feature_names.pkl"
)

# Ajouter le dossier ml au PYTHONPATH
sys.path.append(
    os.path.join(root_dir, "ml")
)

from preprocessing.preprocess import load_and_preprocess


def evaluate():

    print(
        "--- Évaluation Finale sur le Set de TEST "
        "(Données Inconnues) ---"
    )

    # ========================================================
    # Vérification de l'existence du modèle
    # ========================================================

    if not os.path.exists(model_path):
        print("Erreur : Modèle introuvable.")
        return

    # ========================================================
    # Préparation des données
    # ========================================================

    # On récupère les trois ensembles mais on utilise
    # uniquement le jeu de TEST pour l'évaluation finale.
    _, _, X_test, _, _, y_test, _ = load_and_preprocess(
        data_path
    )

    # ========================================================
    # Chargement du modèle
    # ========================================================

    model = joblib.load(model_path)
    feature_names = joblib.load(feature_path)

    # ========================================================
    # Prédictions
    # ========================================================

    y_pred = model.predict(X_test)

    # ========================================================
    # Matrice de confusion
    # ========================================================

    cm = confusion_matrix(y_test, y_pred)

    print("\nMATRICE DE CONFUSION")
    print(cm)

    # Noms des classes
    target_names = [
        "Low Risk (L)",
        "Medium Risk (M)",
        "High Risk (H)"
    ]

    # Création de l'affichage
    disp = ConfusionMatrixDisplay(
        confusion_matrix=cm,
        display_labels=target_names
    )

    disp.plot()

    plt.title(
        "Matrice de confusion - Random Forest"
    )

    plt.tight_layout()

    # ========================================================
    # Sauvegarde de la figure
    # ========================================================

    # La figure sera sauvegardée dans :
    # ml/evaluation/confusion_matrix.png

    evaluation_dir = os.path.dirname(__file__)

    figure_path = os.path.join(
        evaluation_dir,
        "confusion_matrix.png"
    )

    plt.savefig(
        figure_path,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print(
        f"\nMatrice de confusion sauvegardée dans : "
        f"{figure_path}"
    )

    # ========================================================
    # Rapport de classification
    # ========================================================

    print("\n" + "=" * 40)
    print("   RAPPORT FINAL (SUR TEST SET)")
    print("=" * 40)

    print(
        classification_report(
            y_test,
            y_pred,
            target_names=target_names
        )
    )

    # ========================================================
    # Importance des variables
    # ========================================================

    if hasattr(model, "feature_importances_"):

        print("\nTOP 5 DES FACTEURS PRÉDICTIFS :")

        feat_imp = pd.Series(
            model.feature_importances_,
            index=feature_names
        ).sort_values(
            ascending=False
        )

        print(feat_imp.head(5))


# ============================================================
# Point d'entrée
# ============================================================

if __name__ == "__main__":
    evaluate()