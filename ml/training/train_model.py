import sys
import os
import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
data_path = os.path.join(root_dir, "data", "raw", "xAPI-Edu-Data.csv")
model_dir = os.path.join(root_dir, "ml", "models")

sys.path.append(os.path.join(root_dir, "ml"))
from preprocessing.preprocess import load_and_preprocess

def train_best_model():
    os.makedirs(model_dir, exist_ok=True)

    # On récupère les 3 sets
    X_train, X_val, X_test, y_train, y_val, y_test, feature_names = load_and_preprocess(data_path)

    models = {
        "Logistic_Regression": LogisticRegression(max_iter=1000, class_weight='balanced'),
        "Random_Forest": RandomForestClassifier(n_estimators=200, random_state=42),
        "XGBoost": XGBClassifier(random_state=42)
    }

    best_acc = 0
    best_model = None
    best_name = ""

    print("\n--- Benchmark : Entraînement sur Train / Validation sur Val ---")
    for name, model in models.items():
        model.fit(X_train, y_train)
        # On évalue sur le set de VALIDATION pour choisir le meilleur
        val_acc = accuracy_score(y_val, model.predict(X_val))
        print(f"{name:18} | Val Accuracy: {val_acc:.4f}")

        if val_acc > best_acc:
            best_acc = val_acc
            best_model = model
            best_name = name

    # Sauvegarde
    joblib.dump(best_model, os.path.join(model_dir, "best_model.pkl"))
    joblib.dump(feature_names, os.path.join(model_dir, "feature_names.pkl"))
    
    print(f"\nRESULTAT : Meilleur modèle '{best_name}' sauvegardé avec {best_acc:.2f} sur Val.")

if __name__ == "__main__":
    train_best_model()