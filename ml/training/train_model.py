import sys
import os
import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier # Le modèle Elite
from sklearn.metrics import accuracy_score

# =========================================================
# CORRECTION AUTOMATIQUE DES CHEMINS
# =========================================================
# On récupère le chemin du dossier racine du projet (university-dropout-prediction)
# On remonte de 2 niveaux depuis ml/training/train_model.py
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))

# On définit les chemins absolus vers la data et les modèles
data_path = os.path.join(root_dir, "data", "raw", "xAPI-Edu-Data.csv")
model_dir = os.path.join(root_dir, "ml", "models")

# On ajoute le dossier 'ml' au système pour pouvoir importer le preprocessing
sys.path.append(os.path.join(root_dir, "ml"))
from preprocessing.preprocess import load_and_preprocess
# =========================================================

def train_best_model():
    # Création du dossier models s'il n'existe pas
    os.makedirs(model_dir, exist_ok=True)

    print(f"Vérification du fichier de données à : {data_path}")
    
    # Appel du preprocessing avec le chemin absolu
    X_train, X_test, y_train, y_test, feature_names = load_and_preprocess(data_path)

    # Comparaison des meilleurs modèles actuels en Data Science
    models = {
        "Logistic_Regression": LogisticRegression(max_iter=1000, class_weight='balanced'),
        "Random_Forest": RandomForestClassifier(n_estimators=200, random_state=42),
        "XGBoost": XGBClassifier(use_label_encoder=False, eval_metric='mlogloss', random_state=42)
    }

    best_acc = 0
    best_model = None
    best_name = ""

    print("\n--- Benchmark des Modèles de Référence ---")
    for name, model in models.items():
        model.fit(X_train, y_train)
        acc = accuracy_score(y_test, model.predict(X_test))
        print(f"{name:18} | Accuracy: {acc:.4f}")

        if acc > best_acc:
            best_acc = acc
            best_model = model
            best_name = name

    # Sauvegarde du grand gagnant avec des chemins sécurisés
    joblib.dump(best_model, os.path.join(model_dir, "best_model.pkl"))
    joblib.dump(feature_names, os.path.join(model_dir, "feature_names.pkl"))
    
    print(f"\nRESULTAT : Le modèle retenu est {best_name} avec une précision de {best_acc:.2f}")

if __name__ == "__main__":
    # Assure-toi d'avoir fait : pip install xgboost joblib pandas scikit-learn
    train_best_model()