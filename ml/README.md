# 🎓 Machine Learning — Prédiction du risque de décrochage étudiant

Cette partie du projet est consacrée au composant **Machine Learning** du système de prédiction du risque de décrochage étudiant.

L'objectif est de construire un modèle de **classification du niveau de risque** à partir des données du dataset **xAPI-Edu-Data**, après leur ingestion et leur transformation dans le pipeline de données.

Le module ML couvre la préparation des données, le prétraitement, la séparation des jeux de données, l'entraînement de plusieurs modèles, la sélection du meilleur modèle, l'évaluation finale et la sauvegarde des artefacts nécessaires à la reproductibilité.

---

## 🎯 Objectifs

Le système a pour objectif de prédire le niveau de risque associé à un étudiant à partir de différentes caractéristiques académiques, comportementales et personnelles.

Le pipeline ML permet de :

* Préparer les données issues du pipeline de données
* Effectuer le prétraitement des variables
* Effectuer une analyse exploratoire des données (EDA)
* Séparer les données en ensembles Train / Validation / Test
* Entraîner plusieurs algorithmes de classification
* Comparer leurs performances
* Sélectionner le meilleur modèle sur l'ensemble de validation
* Évaluer le modèle final sur un jeu de test indépendant
* Générer une matrice de confusion
* Analyser les facteurs les plus prédictifs
* Sauvegarder le modèle entraîné
* Sauvegarder les noms des variables utilisées
* Conserver les éléments nécessaires à la reproductibilité et au déploiement

---

# 📊 Dataset

Le projet utilise le dataset **xAPI-Edu-Data**.

Cependant, le modèle ML **n'utilise pas directement le fichier CSV original**.

Les données suivent d'abord le pipeline de données :

```text
xAPI-Edu-Data.csv
        │
        ▼
     Ingestion
        │
        ▼
      DuckDB
        │
        ▼
   Transformations dbt
        │
        ▼
prepared_students
        │
        ▼
  Preprocessing ML
        │
        ├──────────────┐
        ▼              ▼
   train_data.csv  val_data.csv
        │
        ▼
   test_data.csv
        │
        ▼
    Entraînement
```

Le dataset original contient **480 observations et 17 variables**.

Après le prétraitement et la séparation, le fichier `train_data.csv` contient **336 observations**, correspondant à 70 % du dataset.

Le prétraitement transforme notamment les variables catégorielles en variables numériques à l'aide du **One-Hot Encoding**.

---

# 🏗️ Architecture du module ML

```text
ml/
│
├── preprocessing/
│   └── preprocess.py
│
├── training/
│   └── train_model.py
│
├── evaluation/
│   ├── evaluate_model.py
│   └── confusion_matrix.png
│
├── models/
│   ├── best_model.pkl
│   ├── feature_names.pkl
│   ├── scaler.pkl
│   └── model_version.json
│
├── notebooks/
│   └── EDA
│
└── README.md
```

---

# 🔄 Pipeline Machine Learning

Le pipeline ML repose sur les données produites après ingestion et transformation.

```text
Dataset original
       │
       ▼
     Ingestion
       │
       ▼
     DuckDB
       │
       ▼
  Transformations dbt
       │
       ▼
prepared_students
       │
       ▼
ml_training_dataset
       │
       ▼
preprocess.py
       │
       ├───────────────┬───────────────┐
       ▼               ▼               ▼
 train_data.csv    val_data.csv    test_data.csv
       │               │               │
       └───────┬───────┘               │
               ▼                       │
        train_model.py                 │
               │                       │
               ▼                       │
      Comparaison des modèles          │
               │                       │
               ▼                       │
        Meilleur modèle                │
               │                       │
               ▼                       │
        best_model.pkl                 │
               │                       │
               └───────────────┐       │
                               ▼       ▼
                         evaluate_model.py
                               │
                               ▼
                         Évaluation Test
                               │
                ┌──────────────┼──────────────┐
                ▼              ▼              ▼
            Accuracy       F1-score      Confusion Matrix
```

---

# 📁 Description des fichiers

## `preprocessing/preprocess.py`

Ce fichier réalise le prétraitement des données provenant de `prepared_students`.

Il est responsable de :

* Encoder la variable cible
* Transformer les variables catégorielles
* Effectuer le One-Hot Encoding
* Séparer les variables explicatives `X` et la cible `y`
* Diviser les données en Train / Validation / Test
* Générer les fichiers CSV utilisés par l'entraînement
* Normaliser les variables numériques
* Sauvegarder le scaler utilisé pendant l'entraînement

### Encodage de la cible

La variable `class` est transformée en valeur numérique :

```text
L → 0
M → 1
H → 2
```

La colonne `risk_class`, qui est une copie de `class` dans `prepared_students`, n'est pas utilisée comme variable explicative afin d'éviter une fuite de données.

Les variables `class` et `risk_class` sont donc retirées des features :

```python
X = df_final.drop(['class', 'risk_class'], axis=1)
y = df_final['class']
```

### One-Hot Encoding

Les variables catégorielles sont transformées en variables binaires avec :

```python
pd.get_dummies(
    df,
    columns=categorical_cols,
    drop_first=True
)
```

Par exemple, une variable catégorielle comme `Topic` peut être transformée en plusieurs variables :

```text
Topic_Biology
Topic_Chemistry
Topic_English
Topic_French
...
```

### Génération des jeux de données

Les données sont séparées en :

```text
70 % → Train
15 % → Validation
15 % → Test
```

Le découpage est reproductible grâce à :

```python
random_state=42
```

et utilise :

```python
stratify=y
```

afin de conserver une répartition similaire des classes.

Les fichiers produits sont :

```text
data/processed/
├── train_data.csv
├── val_data.csv
└── test_data.csv
```

Chaque fichier contient les features transformées ainsi qu'une colonne :

```text
Target
```

---

# 🔍 Analyse exploratoire des données — EDA

L'analyse exploratoire permet de comprendre les caractéristiques des données avant l'entraînement.

Les analyses peuvent notamment inclure :

* Dimensions du dataset
* Types des variables
* Valeurs manquantes
* Distribution de la cible
* Distribution des variables numériques
* Répartition des variables catégorielles
* Corrélations
* Détection de valeurs aberrantes
* Relations entre variables et cible

Exemples :

```python
df.head()
```

```python
df.info()
```

```python
df.describe()
```

```python
df.isnull().sum()
```

```python
df["class"].value_counts()
```

L'EDA est principalement utilisée pour comprendre la structure et la qualité des données avant leur utilisation dans le modèle.

---

# ✂️ Séparation des données

Pour éviter d'évaluer un modèle sur les données utilisées pour son apprentissage, les observations sont réparties en trois ensembles :

| Ensemble   | Rôle                                             |
| ---------- | ------------------------------------------------ |
| Train      | Entraîner les modèles                            |
| Validation | Comparer les modèles et sélectionner le meilleur |
| Test       | Évaluation finale indépendante                   |

La répartition utilisée est :

```text
70 % → Train
15 % → Validation
15 % → Test
```

Le nombre total d'observations étant de 480 :

```text
Train      → 336 observations
Validation → 72 observations
Test       → 72 observations
```

La séparation utilise :

```python
train_test_split(
    X,
    y,
    test_size=0.30,
    random_state=42,
    stratify=y
)
```

puis :

```python
train_test_split(
    X_temp,
    y_temp,
    test_size=0.50,
    random_state=42,
    stratify=y_temp
)
```

---

# 🤖 Modèles entraînés

Plusieurs algorithmes de classification sont entraînés afin de comparer leurs performances.

Les modèles actuellement utilisés sont :

### Logistic Regression

```python
LogisticRegression(
    max_iter=1000,
    class_weight="balanced"
)
```

### Random Forest

```python
RandomForestClassifier(
    n_estimators=200,
    random_state=42
)
```

### XGBoost

```python
XGBClassifier(
    random_state=42
)
```

Les modèles sont entraînés sur le jeu **Train** et comparés sur le jeu **Validation**.

Le jeu de Test n'intervient pas dans la sélection du meilleur modèle.

---

# 📈 Évaluation des modèles

La comparaison des modèles est effectuée sur le jeu de validation.

La métrique principale actuellement utilisée pour sélectionner le meilleur modèle est :

```text
Validation Accuracy
```

La fonction calcule :

```python
accuracy_score(
    y_val,
    model.predict(X_val)
)
```

Les modèles sont comparés et celui ayant la meilleure accuracy sur la validation est sélectionné.

Exemple d'exécution :

```text
--- Benchmark : Entraînement sur Train / Validation sur Val ---
Logistic_Regression | Val Accuracy: 0.6944
Random_Forest       | Val Accuracy: 0.8194
XGBoost             | Val Accuracy: 0.8056

RESULTAT : Meilleur modèle 'Random_Forest' sauvegardé avec 0.82 sur Val.
```

Dans cet exemple, **Random Forest** est sélectionné comme meilleur modèle.

---

# 🏆 Sélection du meilleur modèle

Le modèle ayant obtenu la meilleure performance sur le jeu de validation est sauvegardé dans :

```text
ml/models/best_model.pkl
```

La sélection est effectuée avec :

```python
if val_acc > best_acc:
    best_acc = val_acc
    best_model = model
    best_name = name
```

Cette méthode garantit que le jeu de test reste indépendant de la sélection du modèle.

---

# 🧪 Évaluation finale sur le Test Set

Une fois le meilleur modèle sélectionné, il est évalué sur :

```text
data/processed/test_data.csv
```

Le test set n'intervient pas dans la sélection du modèle.

Le fichier est chargé avec :

```python
test_df = pd.read_csv(test_path)
```

La cible est séparée :

```python
X_test = test_df.drop(columns=["Target"])
y_test = test_df["Target"]
```

Le même scaler que celui utilisé lors de l'entraînement est ensuite chargé :

```python
scaler = joblib.load(scaler_path)
```

et appliqué au test :

```python
X_test = scaler.transform(X_test)
```

Enfin, les prédictions sont réalisées avec :

```python
y_pred = model.predict(X_test)
```

Cette étape permet d'obtenir une estimation des performances du modèle sur des données qui n'ont pas été utilisées pendant son entraînement ou sa sélection.

---

# 📊 Métriques d'évaluation

Les performances finales sont évaluées avec plusieurs métriques.

## Accuracy

```python
accuracy_score(
    y_test,
    y_pred
)
```

Elle mesure la proportion globale de prédictions correctes.

## Precision

La précision mesure, pour une classe donnée, la proportion de prédictions positives correctes.

## Recall

Le recall mesure la capacité du modèle à identifier correctement les observations appartenant à une classe.

## F1-score

Le F1-score combine precision et recall.

Le rapport de classification est généré avec :

```python
classification_report(
    y_test,
    y_pred,
    target_names=target_names
)
```

---

# 📊 Matrice de confusion

La matrice de confusion permet d'analyser les prédictions correctes et les erreurs de classification pour chaque classe.

Elle est calculée avec :

```python
cm = confusion_matrix(
    y_test,
    y_pred
)
```

et affichée avec :

```python
ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=target_names
)
```

Les classes utilisées sont :

```text
Low Risk (L)
Medium Risk (M)
High Risk (H)
```

La matrice est sauvegardée dans :

```text
ml/evaluation/confusion_matrix.png
```

Cette visualisation permet notamment d'identifier les classes qui sont le plus souvent confondues par le modèle.

---

# 🔎 Analyse des facteurs prédictifs

Lorsque le modèle sélectionné possède l'attribut `feature_importances_`, comme Random Forest, il est possible d'analyser l'importance des variables.

```python
feat_imp = pd.Series(
    model.feature_importances_,
    index=feature_names
).sort_values(
    ascending=False
)
```

Les cinq variables les plus importantes peuvent être affichées :

```python
print(feat_imp.head(5))
```

Cette analyse permet d'identifier les caractéristiques qui contribuent le plus aux prédictions du modèle.

> ⚠️ Une importance élevée ne signifie pas qu'une variable est une cause directe du décrochage. Elle indique uniquement qu'elle contribue fortement aux prédictions du modèle.

---

# 💾 Sauvegarde du modèle

Le meilleur modèle est sauvegardé avec `joblib` :

```python
joblib.dump(
    best_model,
    os.path.join(model_dir, "best_model.pkl")
)
```

Le fichier généré est :

```text
ml/models/best_model.pkl
```

Il peut ensuite être rechargé avec :

```python
model = joblib.load(
    "ml/models/best_model.pkl"
)
```

---

# ⚙️ Sauvegarde du scaler

Le scaler utilisé pour la normalisation est sauvegardé afin d'appliquer exactement la même transformation lors de l'évaluation ou du déploiement.

```text
ml/models/scaler.pkl
```

Le scaler est créé à partir du jeu d'entraînement :

```python
scaler.fit_transform(X_train)
```

puis appliqué aux autres ensembles :

```python
scaler.transform(X_val)
scaler.transform(X_test)
```

Ainsi, la même transformation est conservée entre l'entraînement et l'évaluation.

---

# 🧾 Sauvegarde des noms des variables

Les noms des variables utilisées par le modèle sont sauvegardés dans :

```text
ml/models/feature_names.pkl
```

avec :

```python
joblib.dump(
    list(train_df.drop(columns=["Target"]).columns),
    os.path.join(model_dir, "feature_names.pkl")
)
```

Cela permet de conserver la correspondance entre les données transformées et les variables attendues par le modèle.

---

# 🔢 Versionnement des métadonnées

Les informations relatives au modèle peuvent être conservées dans :

```text
ml/models/model_version.json
```

Les métadonnées peuvent notamment contenir :

```json
{
    "model_name": "RandomForest",
    "version": "1.0",
    "accuracy": 0.82,
    "dataset": "xAPI-Edu-Data",
    "date": "2026-06-22"
}
```

Le versionnement permet de conserver une trace :

* du modèle utilisé ;
* de sa version ;
* du dataset utilisé ;
* des performances obtenues ;
* de la date d'entraînement.

---

# 🔁 Reproductibilité

La reproductibilité des expériences est assurée autant que possible par l'utilisation de graines aléatoires fixes.

Pour la séparation des données :

```python
random_state=42
```

Pour Random Forest :

```python
random_state=42
```

Cette configuration permet de reproduire le même découpage et les mêmes résultats dans les mêmes conditions d'exécution.

---

# 🔐 Prévention des fuites de données

Une attention particulière est portée aux variables susceptibles de provoquer une fuite de données.

Dans `prepared_students`, la colonne :

```text
risk_class
```

est une copie de :

```text
class
```

Elle ne doit donc pas être utilisée comme variable explicative.

Le preprocessing retire explicitement :

```python
X = df_final.drop(
    ['class', 'risk_class'],
    axis=1
)
```

La cible est ensuite stockée dans :

```text
Target
```

Ainsi, le modèle ne reçoit pas directement une copie de la réponse attendue parmi ses variables d'entrée.

---

# 📦 Bibliothèques utilisées

Le module ML utilise principalement :

```text
pandas
numpy
scikit-learn
xgboost
matplotlib
seaborn
joblib
```

Installation :

```bash
pip install pandas numpy scikit-learn xgboost matplotlib seaborn joblib
```

---

# ▶️ Exécution de la partie ML

La préparation des données ML dépend du pipeline de données qui produit la table :

```text
main.prepared_students
```

L'asset `ml_training_dataset` utilise cette table afin de produire :

```text
data/processed/train_data.csv
data/processed/val_data.csv
data/processed/test_data.csv
```

Une fois ces fichiers disponibles et `scaler.pkl` généré, l'entraînement peut être exécuté avec :

```python
from ml.training.train_model import train_best_model

train_best_model(
    "data/processed/train_data.csv",
    "data/processed/val_data.csv"
)
```

L'évaluation finale peut ensuite être exécutée avec :

```bash
python ml/evaluation/evaluate_model.py
```

---

# 🧩 Intégration avec Dagster

La partie ML peut être orchestrée par Dagster.

Le flux est :

```text
data_quality_report
        │
        ▼
ml_training_dataset
        │
        ▼
trained_model
        │
        ▼
model_evaluation
```

### `ml_training_dataset`

Cet asset lit la table préparée :

```text
main.prepared_students
```

et appelle :

```python
load_and_preprocess(prepared_df)
```

pour générer les fichiers :

```text
train_data.csv
val_data.csv
test_data.csv
```

### `trained_model`

L'asset d'entraînement appelle :

```python
train_best_model(
    ml_training_dataset["train_csv"],
    ml_training_dataset["val_csv"]
)
```

Le modèle est donc entraîné à partir des données ML préparées et non directement depuis le fichier CSV original.

### `model_evaluation`

Cet asset utilise les résultats obtenus sur le Test Set et applique un seuil de qualité avant une éventuelle promotion du modèle dans le Model Registry MLflow.

---

# 📂 Artefacts produits

Les principaux artefacts du module ML sont :

```text
data/processed/
├── train_data.csv
├── val_data.csv
└── test_data.csv

ml/models/
├── best_model.pkl
├── feature_names.pkl
├── scaler.pkl
└── model_version.json

ml/evaluation/
└── confusion_matrix.png
```

### `train_data.csv`

Jeu utilisé pour entraîner les modèles.

### `val_data.csv`

Jeu utilisé pour comparer les modèles et sélectionner le meilleur.

### `test_data.csv`

Jeu indépendant utilisé pour l'évaluation finale.

### `best_model.pkl`

Contient le meilleur modèle entraîné.

### `feature_names.pkl`

Contient les noms des variables utilisées pendant l'entraînement.

### `scaler.pkl`

Contient le scaler utilisé pour normaliser les données.

### `model_version.json`

Contient les métadonnées et informations de version du modèle.

### `confusion_matrix.png`

Contient la matrice de confusion du modèle final.

---

# 👥 Contribution à la partie Machine Learning

La partie Machine Learning est réalisée en collaboration.

## Hasnaa — ML Engineer

Responsable principalement de :

* préparation des données ML ;
* prétraitement ;
* analyse exploratoire ;
* séparation Train / Validation / Test ;
* entraînement des modèles ;
* comparaison des performances ;
* sélection du meilleur modèle ;
* évaluation finale.

## Fatima — Support ML / Scrum Master / Data Quality

Contribution à la partie ML à travers :

* tests et validation du pipeline ;
* vérification de l'exécution des scripts ;
* validation des résultats ;
* génération et intégration de la matrice de confusion ;
* documentation de la partie ML ;
* mise en place du fichier de versionnement du modèle ;
* intégration des modifications dans GitHub.

Les contributions sont complémentaires et intégrées au dépôt via Git et Pull Requests.

---

# 🚀 Résultat attendu

Le module Machine Learning fournit un modèle capable de prédire le niveau de risque d'un étudiant à partir des caractéristiques disponibles dans les données préparées.

Le pipeline permet également d'assurer :

* une préparation reproductible des données ;
* une séparation claire entre Train, Validation et Test ;
* une comparaison objective des modèles ;
* une sélection du meilleur modèle basée sur la validation ;
* une évaluation indépendante sur le Test Set ;
* une analyse des facteurs prédictifs ;
* la sauvegarde du modèle et du scaler ;
* la conservation des noms de variables ;
* la traçabilité et le versionnement des modèles.

Le composant ML est ainsi intégré au système global tout en respectant la séparation entre le **pipeline de données** et le **pipeline Machine Learning**.
