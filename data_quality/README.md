# Data Quality — University Dropout Prediction

## 1. Présentation

Le dossier `data_quality/` regroupe les composants dédiés au contrôle et à la
validation de la qualité des données du projet **University Dropout Prediction**.

L'objectif est de vérifier que les données sont suffisamment fiables et
cohérentes avant leur utilisation par les étapes de transformation et de
Machine Learning.

La démarche Data Quality est appliquée à deux niveaux :

- **RAW** : données directement issues de l'ingestion ;
- **PREPARED** : données après transformation et déduplication.

Cette distinction est importante car elle permet de détecter les anomalies
présentes dans les données sources avant qu'elles ne soient éventuellement
modifiées par les transformations.

Le flux de données concerné est :

```text
xAPI-Edu-Data.csv
        │
        ▼
       DLT
        │
        ▼
DuckDB / raw_data.students_raw
        │
        ├──────────────► Data Quality RAW
        │
        ▼
       dbt
        │
        ▼
main.stg_students
        │
        ▼
main.prepared_students
        │
        ├──────────────► Data Quality PREPARED
        │
        └──────────────► Règles métier
```

L'orchestration de ces différentes étapes est réalisée séparément dans le
projet.

---

## 2. Objectifs

La démarche Data Quality permet de :

* vérifier que le dataset n'est pas vide ;
* vérifier la présence des colonnes attendues ;
* contrôler la complétude des données ;
* détecter les valeurs NULL interdites ;
* vérifier les valeurs catégorielles autorisées ;
* contrôler les plages des variables numériques ;
* vérifier l'unicité des identifiants techniques ;
* détecter les doublons de lignes exactes ;
* détecter les doublons métier ;
* vérifier la qualité des données préparées ;
* vérifier certaines règles métier ;
* produire un statut global `PASS`, `PASS_WITH_WARNINGS` ou `FAIL`.

L'objectif final est de fournir des données fiables pour les étapes
suivantes du pipeline.

---

## 3. Organisation du dossier

```text
data_quality/
│
├── data_contract.yaml
├── quality_checks.py
├── check_business_rule.py
├── lineage.md
└── README.md
```

### `data_contract.yaml`

Le fichier `data_contract.yaml` formalise les contraintes attendues sur les
données.

Il définit notamment :

* les colonnes obligatoires ;
* les contraintes de complétude ;
* les valeurs autorisées ;
* les plages numériques ;
* les contraintes d'unicité ;
* l'unicité métier RAW ;
* l'unicité métier PREPARED ;
* certaines règles métier.

Le Data Contract constitue donc la référence des règles de qualité utilisées
par les contrôles.

---

### `quality_checks.py`

Le fichier `quality_checks.py` contient les contrôles techniques de qualité.

Il peut être utilisé sur différents types de données :

```python
run_quality_checks(df, dataset_type="raw")
```

ou :

```python
run_quality_checks(df, dataset_type="prepared")
```

Les contrôles couvrent notamment :

* volume ;
* présence des colonnes ;
* valeurs NULL ;
* valeurs autorisées ;
* plages numériques ;
* doublons exacts ;
* unicité de `_dlt_id` ;
* doublons métier.

Le script retourne un rapport contenant notamment :

```text
row_count
column_count
completeness
duplicates
duplicate_ids
business_duplicates
business_duplicate_groups
errors
warnings
status
```

---

### `check_business_rule.py`

Le fichier `check_business_rule.py` contient les contrôles de cohérence
métier appliqués aux données préparées.

Deux règles principales sont actuellement contrôlées :

```text
absence_risk
risk_class
```

La première vérifie la cohérence entre :

```text
studentabsencedays
absence_risk
```

avec la règle :

```text
Under-7  → absence_risk = 0
Above-7  → absence_risk = 1
```

La seconde vérifie la cohérence entre :

```text
risk_class
class
```

Ces contrôles sont séparés des contrôles techniques afin de distinguer la
qualité structurelle des données de leur cohérence métier.

---

### `lineage.md`

Le fichier `lineage.md` documente la traçabilité des données dans le projet.

Il permet notamment de suivre le parcours :

```text
xAPI-Edu-Data.csv
        ↓
DLT
        ↓
raw_data.students_raw
        ↓
Data Quality
        ↓
stg_students
        ↓
prepared_students
        ↓
Machine Learning
        ↓
MLflow
        ↓
FastAPI
```

Le fichier permet donc de comprendre l'origine des données, leurs
transformations et leur destination.

---

### `README.md`

Ce fichier documente :

* l'objectif de la Data Quality ;
* les fichiers du module ;
* les contrôles réalisés ;
* les résultats obtenus ;
* les commandes permettant de reproduire les vérifications.

---

# 4. Source des données

Le projet utilise le dataset :

```text
xAPI-Edu-Data.csv
```

Le fichier est situé dans :

```text
data/
└── raw/
    └── xAPI-Edu-Data.csv
```

Les données contiennent différentes caractéristiques liées aux étudiants,
à leur environnement académique et à leurs interactions avec les ressources
pédagogiques.

---

# 5. Données RAW

Après ingestion, les données sont disponibles dans DuckDB sous :

```text
raw_data.students_raw
```

La table contient les données du dataset ainsi que les informations
techniques générées par dlt, notamment :

```text
_dlt_id
_dlt_load_id
```

La couche RAW constitue le premier niveau contrôlé par la démarche Data
Quality.

L'objectif est de mesurer la qualité réelle des données reçues avant toute
transformation.

---

# 6. Contrôles Data Quality RAW

## 6.1 Dataset non vide

Le premier contrôle vérifie que le dataset contient des enregistrements.

Résultat actuel :

```text
Nombre de lignes : 480
```

Le dataset n'est donc pas vide.

---

## 6.2 Nombre de colonnes

Le dataset RAW contrôlé contient :

```text
19 colonnes
```

Les colonnes attendues sont notamment :

```text
_dlt_id
gender
nationality
placeofbirth
stageid
gradeid
sectionid
topic
semester
relation
raisedhands
visitedresources
announcementsview
discussion
parentansweringsurvey
parentschoolsatisfaction
studentabsencedays
class
```

---

## 6.3 Complétude

Les colonnes soumises à une contrainte de non-nullité sont contrôlées afin
de détecter les valeurs manquantes.

Résultat actuel :

```text
Complétude : 100.00%
```

Aucune anomalie de complétude n'a donc été détectée.

---

## 6.4 Valeurs catégorielles

Le contrôle vérifie que les valeurs des variables catégorielles respectent
les valeurs autorisées définies dans le Data Contract.

Les contrôles concernent notamment :

```text
gender
stageid
sectionid
semester
relation
parentansweringsurvey
parentschoolsatisfaction
studentabsencedays
class
```

Une valeur qui ne correspondrait pas aux modalités attendues serait
considérée comme une anomalie de qualité.

---

## 6.5 Plages numériques

Les variables numériques sont contrôlées afin de vérifier qu'elles restent
dans les plages attendues.

Les principales variables concernées sont :

```text
raisedhands
visitedresources
announcementsview
discussion
```

Les valeurs sont contrôlées par rapport aux bornes définies dans le Data
Contract.

---

# 7. Contrôle des identifiants

L'identifiant technique `_dlt_id` est soumis à une contrainte d'unicité.

Une vérification spécifique a été réalisée :

```text
Nombre total de lignes        : 480
Nombre d'identifiants uniques : 480
```

Ainsi :

```text
480 = 480
```

Aucun `_dlt_id` dupliqué n'a été détecté.

---

# 8. Doublons de lignes exactes

Un contrôle des doublons sur l'ensemble des colonnes permet de détecter les
lignes strictement identiques.

Résultat :

```text
Doublons de lignes : 0
```

Il n'existe donc aucun doublon exact dans les données RAW.

Cependant, l'absence de doublons exacts ne signifie pas nécessairement
l'absence de doublons du point de vue métier.

---

# 9. Détection des doublons métier

Une deuxième vérification a donc été mise en place pour détecter les
doublons métier.

Une observation est considérée comme doublon métier lorsque plusieurs
lignes possèdent les mêmes caractéristiques métier, même si leur identifiant
technique `_dlt_id` est différent.

La clé métier utilisée repose notamment sur :

```text
gender
nationality
placeofbirth
stageid
gradeid
sectionid
topic
semester
relation
raisedhands
visitedresources
announcementsview
discussion
parentansweringsurvey
parentschoolsatisfaction
studentabsencedays
class
```

Le contrôle a détecté :

```text
Doublons métier              : 4 lignes
Groupes de doublons métier   : 2
```

Les quatre lignes correspondent donc à deux groupes, chaque groupe
comportant deux observations.

---

# 10. Gestion des doublons métier

Les doublons métier détectés dans RAW ne sont pas supprimés directement
pendant le contrôle de qualité.

Ils sont conservés afin de garder une vision fidèle des données sources et
sont signalés comme **warnings**.

Le résultat du contrôle est donc :

```text
Nombre de lignes      : 480
Nombre de colonnes    : 19
Complétude            : 100.00%
Doublons de lignes    : 0
IDs DLT dupliqués     : 0
Doublons métier       : 4
Groupes doublons      : 2

WARNINGS :
- 4 ligne(s) impliquée(s) dans 2 groupe(s) de doublons métier RAW

Statut : PASS_WITH_WARNINGS
```

Le statut `PASS_WITH_WARNINGS` signifie qu'aucune erreur bloquante n'a été
détectée, mais qu'une anomalie de qualité a été identifiée et documentée.

---

# 11. Déduplication lors de la préparation

La déduplication métier est ensuite réalisée lors de la préparation des
données.

Le flux est :

```text
RAW
480 lignes
   │
   │ Détection de 2 groupes de doublons métier
   ▼
Déduplication
   │
   ▼
PREPARED
478 lignes
```

La préparation permet ainsi d'éviter que les doublons métier identifiés dans
RAW ne soient transmis aux étapes suivantes.

Cette stratégie permet de conserver la traçabilité du problème dans les
données sources tout en produisant un dataset préparé plus propre.

---

# 12. Contrôles PREPARED

Après transformation, les données sont disponibles dans :

```text
main.prepared_students
```

Les contrôles Data Quality sont également appliqués à cette table.

L'objectif est de vérifier que :

* les transformations ont produit des données cohérentes ;
* les contraintes de qualité sont toujours respectées ;
* les doublons métier ont bien été traités ;
* les variables calculées utilisées par la suite sont correctement produites.

Le nombre de lignes obtenu après déduplication est :

```text
478 lignes
```

---

# 13. Règles métier

Les contrôles techniques ne suffisent pas à garantir la cohérence des
données. Des règles métier spécifiques sont donc implémentées dans :

```text
data_quality/check_business_rule.py
```

## 13.1 Règle `absence_risk`

La variable `absence_risk` est calculée à partir de :

```text
studentabsencedays
```

La règle est :

```text
studentabsencedays = Under-7
        → absence_risk = 0

studentabsencedays = Above-7
        → absence_risk = 1
```

Le contrôle vérifie également l'absence de valeurs NULL.

Résultat :

```text
Violations absence_risk : 0
```

---

## 13.2 Règle `risk_class`

La variable :

```text
risk_class
```

doit être cohérente avec :

```text
class
```

Le contrôle vérifie donc :

```text
risk_class = class
```

ainsi que l'absence de valeurs NULL.

Résultat :

```text
Violations risk_class : 0
```

---

## 13.3 Résultat des règles métier

L'exécution de :

```powershell
python data_quality\check_business_rule.py
```

produit actuellement :

```text
============================================================
        BUSINESS RULE CHECK
============================================================
Violations absence_risk : 0
Violations risk_class  : 0
Groupes doublons métier: 0
Statut                  : PASS
Toutes les règles métier sont respectées.
============================================================
```

Les règles métier appliquées aux données préparées sont donc respectées.

Les doublons métier RAW sont traités séparément par `quality_checks.py`,
avant la préparation.

---

# 14. Validation avec dbt

La qualité des données transformées est également vérifiée avec les tests
dbt.

Les modèles concernés sont :

```text
main.stg_students
main.prepared_students
```

Le flux de transformation est :

```text
raw_data.students_raw
        │
        ▼
main.stg_students
        │
        ▼
main.prepared_students
```

Les tests dbt permettent notamment de contrôler la non-nullité et les
valeurs acceptées pour certaines colonnes.

---

# 15. Résultats des tests dbt

La commande :

```powershell
dbt run
```

a permis de construire les deux modèles avec succès :

```text
PASS=2
WARN=0
ERROR=0
```

Les tests sont ensuite exécutés avec :

```powershell
dbt test
```

Résultat :

```text
PASS=9
WARN=0
ERROR=0
SKIP=0
NO-OP=0
TOTAL=9
```

Les 9 tests dbt ont donc été validés avec succès.

---

# 16. Bilan global de la qualité

Les principaux résultats obtenus sont :

| Contrôle | Résultat |
|---|---:|
| Lignes RAW | 480 |
| Colonnes | 19 |
| Complétude | 100 % |
| Doublons exacts | 0 |
| `_dlt_id` dupliqués | 0 |
| Lignes impliquées dans des doublons métier RAW | 4 |
| Groupes de doublons métier RAW | 2 |
| Lignes PREPARED | 478 |
| Violations `absence_risk` | 0 |
| Violations `risk_class` | 0 |
| Tests dbt | 9/9 PASS |
| Statut Data Quality RAW | **PASS_WITH_WARNINGS** |

Le statut `PASS_WITH_WARNINGS` est attendu et documente précisément les
deux groupes de doublons métier détectés dans les données RAW.

---

# 17. Commandes d'exécution

## Contrôle Data Quality RAW

Depuis la racine du projet :

```powershell
python data_quality\quality_checks.py
```

Cette commande permet de générer le rapport de qualité sur les données RAW.

---

## Contrôle des règles métier

```powershell
python data_quality\check_business_rule.py
```

Cette commande vérifie les règles métier appliquées aux données préparées.

---

## Exécution dbt

Depuis :

```text
dataops/dbt/university_dropout_dbt/
```

Exécuter :

```powershell
dbt run
```

Puis :

```powershell
dbt test
```

---

# 18. Reproductibilité

La base DuckDB est générée localement à partir des données sources et du
code d'ingestion.

Elle n'est pas nécessairement versionnée dans Git.

La reconstruction suit le principe :

```text
xAPI-Edu-Data.csv
        │
        ▼
ingest_data.py
        │
        ▼
DuckDB
        │
        ▼
raw_data.students_raw
        │
        ▼
quality_checks.py
```

Les règles de qualité, le Data Contract, les règles métier, les modèles dbt
et la documentation du lineage sont versionnés avec le projet.

Cela permet de reproduire les contrôles de qualité à partir des mêmes
sources et règles.

---

# 19. Lineage et traçabilité

Le fichier `lineage.md` permet de documenter la provenance des données et
leur évolution au cours du pipeline.

Le lineage principal est :

```text
xAPI-Edu-Data.csv
        │
        ▼
       DLT
        │
        ▼
raw_data.students_raw
        │
        ▼
Data Quality RAW
        │
        ▼
stg_students
        │
        ▼
prepared_students
        │
        ▼
Data Quality PREPARED
        │
        ▼
Règles métier
        │
        ▼
Machine Learning
```

Cette traçabilité permet notamment de savoir :

* d'où proviennent les données ;
* quelles transformations leur sont appliquées ;
* où les contrôles de qualité sont effectués ;
* quelles données sont transmises au Machine Learning.

---

# 20. Rôle du module Data Quality dans le projet

Le module `data_quality` constitue une couche de contrôle entre les données
issues de l'ingestion et leur utilisation dans les étapes suivantes.

Il repose sur quatre composants principaux :

```text
data_contract.yaml
        │
        ▼
quality_checks.py
        │
        ├── Qualité RAW
        └── Qualité PREPARED

check_business_rule.py
        │
        ▼
Cohérence métier

lineage.md
        │
        ▼
Traçabilité des données
```

Cette organisation permet de séparer :

* les **contraintes attendues** avec le Data Contract ;
* les **contrôles techniques** avec `quality_checks.py` ;
* les **contrôles métier** avec `check_business_rule.py` ;
* la **traçabilité** avec `lineage.md`.

---

# 21. Conclusion

La démarche Data Quality mise en place permet de sécuriser les données avant
leur utilisation par le Machine Learning.

Les contrôles réalisés montrent que :

* les données RAW contiennent 480 lignes ;
* la complétude est de 100 % ;
* aucun doublon exact n'a été détecté ;
* aucun `_dlt_id` n'est dupliqué ;
* deux groupes de doublons métier ont été identifiés ;
* ces doublons représentent 4 lignes ;
* la préparation produit 478 lignes ;
* les règles `absence_risk` et `risk_class` sont respectées ;
* les 9 tests dbt sont validés.

Le résultat final est donc :

```text
Data Quality RAW : PASS_WITH_WARNINGS
Business Rules   : PASS
dbt tests        : 9/9 PASS
```

La présence du statut `PASS_WITH_WARNINGS` permet de conserver la
transparence sur les anomalies détectées dans les données sources, tandis
que la déduplication permet de fournir des données préparées adaptées aux
étapes suivantes du projet.