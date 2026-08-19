import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def load_and_preprocess(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"ERREUR : Fichier introuvable à : {file_path}")

    df = pd.read_csv(file_path)
    df = df.ffill() # Compatibilité Pandas 3.0+

    # Encodage de la cible
    target_map = {'L': 0, 'M': 1, 'H': 2}
    df['Class'] = df['Class'].map(target_map)

    # Encodage One-Hot des variables catégorielles
    categorical_cols = ['gender', 'NationalITy', 'PlaceofBirth', 'StageID', 
                        'GradeID', 'SectionID', 'Topic', 'Semester', 
                        'Relation', 'ParentAnsweringSurvey', 
                        'ParentschoolSatisfaction', 'StudentAbsenceDays']
    df_final = pd.get_dummies(df, columns=categorical_cols, drop_first=True)

    X = df_final.drop('Class', axis=1)
    y = df_final['Class']

    # --- SÉPARATION EN 3 SETS (TRAIN 70%, VAL 15%, TEST 15%) ---
    # 1. On sépare le Train (70%) et le Reste (30%)
    X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.30, random_state=42, stratify=y)
    
    # 2. On divise le Reste en deux : Validation (15%) et Test (15%)
    X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.50, random_state=42, stratify=y_temp)

    # --- SAUVEGARDE DES DATASETS EN CSV ---
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    processed_dir = os.path.join(root_dir, "data", "processed")
    os.makedirs(processed_dir, exist_ok=True)

    def save_as_csv(X_data, y_data, filename):
        temp_df = X_data.copy()
        temp_df['Target'] = y_data.values
        temp_df.to_csv(os.path.join(processed_dir, filename), index=False)

    save_as_csv(X_train, y_train, "train_data.csv")
    save_as_csv(X_val, y_val, "val_data.csv")
    save_as_csv(X_test, y_test, "test_data.csv")
    
    print(f"Datasets (Train, Val, Test) sauvegardés dans : {processed_dir}")

    # Normalisation
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_val_scaled = scaler.transform(X_val)
    X_test_scaled = scaler.transform(X_test)

    return X_train_scaled, X_val_scaled, X_test_scaled, y_train, y_val, y_test, X.columns