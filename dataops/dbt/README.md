# Partie DataOps – dbt (Yousra)

## Description

Cette partie consiste à mettre en place et valider la partie **dbt** du projet
pour transformer et contrôler les données déjà disponibles dans DuckDB.

## Travail réalisé

- Configuration du projet **dbt avec DuckDB**.
- Création du modèle `stg_students` pour préparer les données brutes.
- Création du modèle `prepared_students` pour préparer les données utilisées
  dans la suite du projet.
- Transformation de `studentabsencedays` en `absence_risk` :
  - `Under-7` → `0`
  - `Above-7` → `1`
- Création de `risk_class` à partir de `class`.
- Ajout de la source `students_raw` dans `sources.yml`.
- Mise en place de **9 tests de qualité des données**, avec **9/9 tests réussis**.
- Génération de la documentation dbt et du lineage.

## Résultat

La partie dbt est fonctionnelle et produit des données préparées et contrôlées,
prêtes à être utilisées par les étapes suivantes du projet.