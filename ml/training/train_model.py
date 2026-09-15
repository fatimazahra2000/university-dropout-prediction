import sys
import os
import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score
import pandas as pd

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))

model_dir = os.path.join(root_dir, "ml", "models")

sys.path.append(os.path.join(root_dir, "ml"))


def train_best_model(train_csv, val_csv):
    os.makedirs(model_dir, exist_ok=True)

    # Charger les datasets préparés par ml_training_dataset
    train_df = pd.read_csv(train_csv)
    print("TRAINING DATASET :", train_csv)
    val_df = pd.read_csv(val_csv)

    # Séparer les variables explicatives et la cible
    X_train = train_df.drop(columns=["Target"])
    y_train = train_df["Target"]

    X_val = val_df.drop(columns=["Target"])
    y_val = val_df["Target"]

    # Charger le scaler créé pendant le preprocessing
    scaler_path = os.path.join(model_dir, "scaler.pkl")
    scaler = joblib.load(scaler_path)

    # Appliquer le même scaler au train et à la validation
    X_train = scaler.transform(X_train)
    X_val = scaler.transform(X_val)

    models = {
        "Logistic_Regression": LogisticRegression(
            max_iter=1000,
            class_weight='balanced'
        ),
        "Random_Forest": RandomForestClassifier(
            n_estimators=200,
            random_state=42
        ),
        "XGBoost": XGBClassifier(
            random_state=42
        )
    }

    best_acc = 0
    best_model = None
    best_name = ""

    print("\n--- Benchmark : Entraînement sur Train / Validation sur Val ---")

    for name, model in models.items():

        model.fit(X_train, y_train)

        val_acc = accuracy_score(
            y_val,
            model.predict(X_val)
        )

        print(f"{name:18} | Val Accuracy: {val_acc:.4f}")

        if val_acc > best_acc:
            best_acc = val_acc
            best_model = model
            best_name = name

    # Sauvegarde du meilleur modèle
    joblib.dump(
        best_model,
        os.path.join(model_dir, "best_model.pkl")
    )

    # Sauvegarde des noms des features
    joblib.dump(
        list(train_df.drop(columns=["Target"]).columns),
        os.path.join(model_dir, "feature_names.pkl")
    )

    print(
        f"\nRESULTAT : Meilleur modèle '{best_name}' "
        f"sauvegardé avec {best_acc:.2f} sur Val."
    )