# 🎓 Machine Learning — Prédiction de l'abandon universitaire

Cette partie du projet est consacrée au composant **Machine Learning** du projet :

> **Prédiction de l'abandon universitaire**

L'objectif est de construire un modèle de **classification des risques de décrochage universitaire** à partir du dataset **xAPI-Edu-Data**.

Le module ML couvre l'ensemble du pipeline de Machine Learning, depuis la préparation des données jusqu'à la sauvegarde et au versionnement du meilleur modèle.


## 🎯 Objectifs

Le système a pour objectif de prédire le risque d'abandon universitaire d'un étudiant à partir de différentes caractéristiques académiques, comportementales et personnelles.

Le pipeline ML permet de :

* Préparer et nettoyer les données
* Effectuer le prétraitement des variables
* Réaliser une analyse exploratoire des données (**EDA**)
* Séparer les données en ensembles **Train / Validation / Test**
* Entraîner plusieurs algorithmes de classification
* Comparer leurs performances
* Sélectionner le meilleur modèle
* Évaluer le modèle final sur un jeu de test indépendant
* Générer une matrice de confusion
* Analyser les facteurs les plus prédictifs
* Sauvegarder le modèle entraîné
* Sauvegarder les noms des variables utilisées
* Versionner les métadonnées du modèle


## 📊 Dataset

Le projet utilise le dataset **xAPI-Edu-Data**, qui contient des informations relatives au comportement et aux performances des étudiants.

Les variables peuvent notamment représenter :

* Les informations démographiques
* La participation en classe
* Le temps passé sur les ressources pédagogiques
* Les interactions avec la plateforme d'apprentissage
* Les absences
* Les performances académiques
* Les comportements d'apprentissage

La variable cible correspond au niveau de risque ou à la catégorie académique de l'étudiant selon la définition utilisée dans le projet.


## 🏗️ Architecture du module

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
│   └── model_version.json
│
├── notebooks/
│   └── EDA
│
└── README.md
```


## 🔄 Pipeline Machine Learning

Le fonctionnement général du module est le suivant :

```text
Dataset xAPI-Edu-Data
        │
        ▼
Prétraitement des données
        │
        ▼
Analyse exploratoire (EDA)
        │
        ▼
Séparation Train / Validation / Test
        │
        ▼
Entraînement des modèles
        │
        ├── Random Forest
        ├── XGBoost
        └── autres modèles
        │
        ▼
Comparaison des performances
        │
        ▼
Sélection du meilleur modèle
        │
        ▼
Évaluation sur le Test Set
        │
        ├── Accuracy
        ├── Precision
        ├── Recall
        ├── F1-score
        └── Matrice de confusion
        │
        ▼
Analyse des facteurs prédictifs
        │
        ▼
Sauvegarde du modèle
        │
        ▼
Versionnement des métadonnées
```


# 📁 Description des fichiers

## `preprocessing/preprocess.py`

Ce fichier est responsable de la préparation des données avant l'entraînement.

Les principales opérations sont :

* Chargement du dataset
* Nettoyage des données
* Gestion des valeurs manquantes
* Transformation des variables catégorielles
* Encodage des catégories
* Séparation des variables explicatives `X` et de la variable cible `y`
* Préparation des données pour les modèles ML
* Séparation en ensembles d'entraînement, validation et test

Exemple :

```python
import pandas as pd
from sklearn.model_selection import train_test_split

df = pd.read_csv("xAPI-Edu-Data.csv")

X = df.drop("target", axis=1)
y = df["target"]

X_train, X_temp, y_train, y_temp = train_test_split(
    X,
    y,
    test_size=0.30,
    random_state=42,
    stratify=y
)

X_val, X_test, y_val, y_test = train_test_split(
    X_temp,
    y_temp,
    test_size=0.50,
    random_state=42,
    stratify=y_temp
)
```


# 🔍 Analyse exploratoire des données — EDA

L'EDA permet de mieux comprendre le dataset avant de commencer l'entraînement.

Les analyses peuvent inclure :

* Dimensions du dataset
* Types des variables
* Valeurs manquantes
* Distribution de la variable cible
* Distribution des variables numériques
* Répartition des variables catégorielles
* Corrélations
* Détection des valeurs aberrantes
* Analyse de la relation entre les variables et la cible

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
df["target"].value_counts()
```


# ✂️ Séparation des données

Pour éviter d'évaluer le modèle sur les données utilisées pendant son apprentissage, les données sont séparées en trois parties :

| Ensemble   | Rôle                                 |
| ---------- | ------------------------------------ |
| Train      | Entraîner le modèle                  |
| Validation | Comparer et sélectionner les modèles |
| Test       | Évaluation finale indépendante       |

Une séparation possible est :

```text
70 % → Train
15 % → Validation
15 % → Test
```

L'utilisation de `random_state=42` permet d'obtenir une séparation reproductible.

```python
train_test_split(
    X,
    y,
    test_size=0.30,
    random_state=42,
    stratify=y
)
```

Le paramètre `stratify=y` permet de conserver une répartition similaire des classes dans les différents ensembles.


# 🤖 Modèles entraînés

Plusieurs algorithmes de classification peuvent être entraînés afin de comparer leurs performances.

Par exemple :

### Random Forest

```python
from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)
```

### XGBoost

```python
from xgboost import XGBClassifier

model = XGBClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)
```

L'objectif n'est pas simplement de choisir le modèle ayant la meilleure accuracy sur les données d'entraînement, mais de comparer les performances obtenues sur l'ensemble de validation.


# 📈 Évaluation des modèles

Les modèles sont comparés à l'aide de plusieurs métriques.

## Accuracy

L'accuracy mesure la proportion de prédictions correctes :

```python
from sklearn.metrics import accuracy_score

accuracy = accuracy_score(y_val, y_pred)
```

## Precision

La précision mesure, parmi les observations prédites comme appartenant à une classe, combien sont réellement dans cette classe.

```python
from sklearn.metrics import precision_score

precision = precision_score(
    y_val,
    y_pred,
    average="weighted"
)
```

## Recall

Le recall mesure la capacité du modèle à retrouver les observations appartenant réellement à une classe.

```python
from sklearn.metrics import recall_score

recall = recall_score(
    y_val,
    y_pred,
    average="weighted"
)
```

## F1-score

Le F1-score combine la précision et le recall.

```python
from sklearn.metrics import f1_score

f1 = f1_score(
    y_val,
    y_pred,
    average="weighted"
)
```

## Rapport de classification

```python
from sklearn.metrics import classification_report

print(
    classification_report(
        y_val,
        y_pred
    )
)
```


# 🏆 Sélection du meilleur modèle

Après l'entraînement, les différents modèles sont comparés.

Exemple :

```text
Modèle              Accuracy    Precision    Recall    F1-score
----------------------------------------------------------------
Random Forest         0.94        0.94        0.94       0.94
XGBoost               0.93        0.93        0.93       0.93
```

Le meilleur modèle est sélectionné en fonction des performances obtenues sur l'ensemble de validation.

Le critère principal peut être le **F1-score**, particulièrement lorsque les classes ne sont pas parfaitement équilibrées.

Exemple :

```python
if f1_score_model_1 > f1_score_model_2:
    best_model = model_1
else:
    best_model = model_2
```


# 🧪 Évaluation finale sur le Test Set

Une fois le meilleur modèle sélectionné, il est évalué sur le jeu de test.

Le test set ne doit pas être utilisé pour choisir le modèle.

```python
best_model.fit(X_train, y_train)

y_test_pred = best_model.predict(X_test)
```

Puis :

```python
from sklearn.metrics import accuracy_score, classification_report

accuracy = accuracy_score(
    y_test,
    y_test_pred
)

print("Test Accuracy :", accuracy)

print(
    classification_report(
        y_test,
        y_test_pred
    )
)
```

Cette étape fournit une estimation plus fiable des performances du modèle sur de nouvelles données.


# 📊 Matrice de confusion

La matrice de confusion permet d'analyser les erreurs de classification.

```python
from sklearn.metrics import confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

cm = confusion_matrix(
    y_test,
    y_test_pred
)

sns.heatmap(
    cm,
    annot=True,
    fmt="d",
    cmap="Blues"
)

plt.xlabel("Prédiction")
plt.ylabel("Valeur réelle")
plt.title("Matrice de confusion")

plt.savefig(
    "evaluation/confusion_matrix.png"
)

plt.show()
```

La matrice permet d'identifier :

* Les vrais positifs
* Les vrais négatifs
* Les faux positifs
* Les faux négatifs

Dans un problème de prédiction de décrochage, les faux négatifs peuvent être particulièrement importants : un étudiant réellement à risque mais classé comme non à risque pourrait ne pas bénéficier d'une intervention préventive.


# 🔎 Analyse des facteurs prédictifs

Pour les modèles permettant d'obtenir l'importance des variables, comme Random Forest, il est possible d'identifier les caractéristiques les plus importantes.

```python
importances = best_model.feature_importances_

for feature, importance in zip(
    feature_names,
    importances
):
    print(feature, importance)
```

On peut ensuite trier les variables :

```python
import pandas as pd

importance_df = pd.DataFrame({
    "feature": feature_names,
    "importance": importances
})

importance_df = importance_df.sort_values(
    by="importance",
    ascending=False
)

print(importance_df)
```

Cette analyse permet de comprendre quelles variables contribuent le plus aux prédictions du modèle.

> ⚠️ L'importance d'une variable ne signifie pas nécessairement qu'elle est une cause directe de l'abandon. Elle indique qu'elle contribue aux prédictions du modèle.


# 💾 Sauvegarde du modèle

Une fois le meilleur modèle identifié, il est sauvegardé afin de pouvoir être réutilisé sans effectuer à nouveau l'entraînement.

Avec `joblib` :

```python
import joblib

joblib.dump(
    best_model,
    "models/best_model.pkl"
)
```

Le modèle peut ensuite être chargé :

```python
model = joblib.load(
    "models/best_model.pkl"
)
```

Puis utilisé pour effectuer une prédiction :

```python
prediction = model.predict(
    X_new
)
```


# 🧾 Sauvegarde des noms des variables

Les noms des variables utilisées pendant l'entraînement sont également sauvegardés.

```python
joblib.dump(
    feature_names,
    "models/feature_names.pkl"
)
```

Ils peuvent être récupérés avec :

```python
feature_names = joblib.load(
    "models/feature_names.pkl"
)
```

Cela permet de conserver la correspondance entre les données d'entrée et le modèle.


# 🔢 Versionnement du modèle

Les métadonnées du modèle sont sauvegardées dans :

```text
models/model_version.json
```

Exemple :

```json
{
    "model_name": "RandomForest",
    "version": "1.0",
    "accuracy": 0.94,
    "dataset": "xAPI-Edu-Data",
    "date": "2026-06-22"
}
```

Le versionnement permet de garder une trace des modèles entraînés et de leurs performances.

Il peut notamment permettre de savoir :

* Quel modèle a été utilisé
* Quelle version du modèle est actuellement disponible
* Sur quel dataset le modèle a été entraîné
* Quelle performance a été obtenue
* Quand le modèle a été entraîné


# 🧪 Reproductibilité

Pour garantir la reproductibilité des expériences, les graines aléatoires doivent être fixées lorsque cela est possible.

Exemple :

```python
random_state=42
```

Pour les modèles :

```python
RandomForestClassifier(
    n_estimators=100,
    random_state=42
)
```

Pour la séparation des données :

```python
train_test_split(
    X,
    y,
    random_state=42
)
```


# 📦 Bibliothèques utilisées

Le module ML utilise principalement les bibliothèques Python suivantes :

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


# ▶️ Exécution du pipeline

## 1. Préparer les données

```bash
python preprocessing/preprocess.py
```

## 2. Entraîner les modèles

```bash
python training/train_model.py
```

## 3. Évaluer le meilleur modèle

```bash
python evaluation/evaluate_model.py
```

Après l'exécution, les principaux artefacts sont disponibles dans :

```text
models/
```

et :

```text
evaluation/
```


# 📌 Résumé du workflow

```text
1. Charger les données
        ↓
2. Nettoyer les données
        ↓
3. Effectuer l'EDA
        ↓
4. Préparer X et y
        ↓
5. Train / Validation / Test
        ↓
6. Entraîner plusieurs modèles
        ↓
7. Comparer Accuracy / Precision / Recall / F1
        ↓
8. Sélectionner le meilleur modèle
        ↓
9. Évaluer sur le Test Set
        ↓
10. Générer la matrice de confusion
        ↓
11. Analyser l'importance des variables
        ↓
12. Sauvegarder le modèle
        ↓
13. Sauvegarder les features
        ↓
14. Versionner les métadonnées
```


# 📂 Artefacts produits

À la fin du pipeline, les principaux artefacts sont :

```text
models/
├── best_model.pkl
├── feature_names.pkl
└── model_version.json

evaluation/
└── confusion_matrix.png
```

### `best_model.pkl`

Contient le meilleur modèle entraîné.

### `feature_names.pkl`

Contient les noms des variables utilisées par le modèle.

### `model_version.json`

Contient les métadonnées et informations de version du modèle.

### `confusion_matrix.png`

Contient la visualisation de la matrice de confusion du modèle final.


# 👥 Contribution à la partie Machine Learning

La partie Machine Learning est réalisée en collaboration.

Hasnaa — ML Engineer

Responsable principalement de :

préparation des données ;
prétraitement ;
analyse exploratoire ;
entraînement des modèles ;
comparaison des modèles ;
sélection du meilleur modèle ;
évaluation des performances.

Fatima — Support ML / Scrum Master / Data Quality

Contribution à la partie ML à travers :

tests et validation du pipeline ;
vérification de l'exécution des scripts ;
validation des résultats ;
génération et intégration de la matrice de confusion ;
documentation de la partie ML ;
mise en place du fichier de versionnement du modèle ;
intégration des modifications dans GitHub.

Les contributions sont complémentaires et sont intégrées au dépôt via Git et Pull Requests.


# 🚀 Résultat attendu

Le module Machine Learning fournit un modèle capable de prédire le **risque d'abandon universitaire** à partir des caractéristiques disponibles dans le dataset.

Le pipeline permet également d'assurer :

* Une préparation reproductible des données
* Une comparaison objective des modèles
* Une évaluation indépendante
* Une interprétation des résultats
* La sauvegarde du modèle
* La traçabilité et le versionnement des modèles

Ce composant constitue ainsi la partie **Machine Learning** du système global de prédiction de l'abandon universitaire.
