# Déploiement Cloud — Komodo

**Responsable : Soukaina**

## Contexte

Le déploiement de l'application (API FastAPI + MLflow + Dagster) est réalisé
via **Komodo**, une plateforme auto-hébergée de gestion et déploiement de
conteneurs Docker (approche GitOps).

- Instance Komodo utilisée : `komodo.s3.fsbm.ma`
- Serveur cible : `vh3`
- Stack existant : `prediction_de_l_abandon_universitaire`

## Pourquoi Komodo

Komodo a été choisi car il permet de piloter le déploiement Docker Compose
directement depuis le dépôt Git (mode GitOps), sans avoir besoin de gérer
un cluster Kubernetes ni un registre d'images externe : Komodo construit
les images directement sur le serveur à partir du `docker-compose.yml` du
projet (chaque service utilise `build:`, pas `image:`).

## Configuration réalisée

Le stack Komodo a été configuré en mode **Git Repo** (au lieu de `UI Defined`,
qui laissait la configuration vide — cause de l'état `Config Missing` /
`DOWN` initial).

### Paramètres de connexion au dépôt

| Paramètre | Valeur |
|---|---|
| Repo | `fatimazahra2000/university-dropout-prediction` |
| Branche | `main` |
| Fichier compose | `docker-compose.yml` (racine du repo) |
| Account (auth GitHub) | Aucun requis (dépôt public) |

### Options de build activées

| Option | État | Raison |
|---|---|---|
| `run_build` (Pre Build Images) | ✅ Activé | Le compose n'utilise que des directives `build:` ; sans cette option, Komodo ne reconstruirait pas les images à jour avant chaque déploiement |
| Pre Pull Images | ✅ Activé (par défaut) | Sans effet direct ici (pas d'`image:` distante), laissé tel quel |
| Destroy Before Deploy | ⬜ Désactivé | Pas nécessaire pour un premier déploiement propre |
| Auto Update / Poll for Updates | ⬜ Désactivé (pour l'instant) | À activer une fois le premier déploiement manuel validé, pour éviter un redéploiement automatique non contrôlé |

### Variables d'environnement

Définies dans Komodo (section *Environment*, écrites dans un fichier `.env`
généré sur le serveur au moment du déploiement) :

DATA_DIR=data
DUCKDB_PATH=data/university_dropout.duckdb
MLFLOW_TRACKING_URI=http://mlflow:5000
API_HOST=0.0.0.0
API_PORT=8000
CLOUD_ENVIRONMENT=komodo


⚠️ `MLFLOW_TRACKING_URI` pointe vers le **nom du service** Docker Compose
(`mlflow`), pas `localhost`, car les conteneurs communiquent entre eux via
le réseau interne créé par Docker Compose.

### Webhook GitHub

Un webhook de déploiement automatique est déjà configuré et **activé** côté
Komodo (`Webhook Enabled: ENABLED`), pointant vers :https://komodo.s3.fsbm.ma/listener/github/
Ce webhook doit être vérifié côté paramètres GitHub du dépôt
(`Settings > Webhooks`) pour confirmer qu'il est bien enregistré et qu'il
recevra les futurs push sur `main`.

## État actuel

- ✅ Configuration Git Repo sauvegardée dans Komodo (`Save`)
- ⬜ **Déploiement réel non encore déclenché** (`Deploy`) : en attente de
  validation par l'équipe, pour s'assurer que `main` est à jour et que
  personne d'autre n'a un déploiement en cours.

## Prochaines étapes

1. Confirmer avec l'équipe (notamment Hiba, responsable de l'API/Docker)
   que `main` est prêt pour un déploiement.
2. Cliquer sur **Deploy** dans Komodo, ou déclencher via un `push` sur
   `main` (webhook déjà actif).
3. Vérifier le bon démarrage des 4 services (`api`, `mlflow`,
   `dagster-webserver`, `dagster-daemon`) dans l'onglet **Services** du
   stack Komodo.
4. Vérifier `GET /health` sur l'API déployée.
5. Mettre en place le monitoring du service (disponibilité, temps de
   réponse, erreurs) — voir section Monitoring du rapport.

