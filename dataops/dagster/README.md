# Orchestration - Dagster

Responsable : Hajar

## Role

Dagster enchaine automatiquement les etapes du pipeline de donnees, dans l'ordre, et permet de suivre leur execution.

## Etapes orchestrees

1. Ingestion (dlt) - Doaa
2. Stockage (DuckDB) - Doaa
3. Transformation (dbt) - Hasna
4. Controle qualite - Hasna

Chaque etape depend du succes de la precedente.

## Fichiers

- pipeline.py : contient les operations, le job et les definitions Dagster.

## Lancer le pipeline

```bash
pip install dagster dagster-webserver
cd dataops/dagster
dagster dev -f pipeline.py
```

Interface disponible sur : http://localhost:3000

## Etat actuel

| Etape | Script | Statut |
|---|---|---|
| Ingestion | dataops/dlt/ingestion.py | En cours (Doaa) |
| Transformation | dataops/dbt/ | En cours (Hasna) |
| Controle qualite | data_quality/quality_checks.py | En cours (Hasna) |

Le pipeline peut echouer sur ces etapes tant qu'elles ne sont pas terminees.

## Prochaines etapes

- Gestion des erreurs et retries
- Scheduler pour execution automatique
- Assets Dagster pour le data lineage