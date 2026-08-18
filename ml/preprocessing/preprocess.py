import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def load_and_preprocess(file_path):
    # Vérification de sécurité
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"ERREUR : Le fichier est introuvable ici : {file_path}")

    df = pd.read_csv(file_path)
    
    # --- CORRECTION POUR PANDAS RÉCENT ---
    # Au lieu de df.fillna(method='ffill'), on utilise directement df.ffill()
    df = df.ffill() 

    # Encodage de la cible
    target_map = {'L': 0, 'M': 1, 'H': 2}
    df['Class'] = df['Class'].map(target_map)

    # Liste des colonnes catégorielles
    categorical_cols = ['gender', 'NationalITy', 'PlaceofBirth', 'StageID', 
                        'GradeID', 'SectionID', 'Topic', 'Semester', 
                        'Relation', 'ParentAnsweringSurvey', 
                        'ParentschoolSatisfaction', 'StudentAbsenceDays']
    
    # Encodage One-Hot
    df_final = pd.get_dummies(df, columns=categorical_cols, drop_first=True)

    X = df_final.drop('Class', axis=1)
    y = df_final['Class']

    # Séparation Train/Test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    # Normalisation
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    return X_train, X_test, y_train, y_test, X.columns