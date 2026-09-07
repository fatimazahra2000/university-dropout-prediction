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
| Branche |`develop` (temporaire — sera basculé sur `main` une fois le lien Git validé par l'équipe) |
| Fichier compose | `docker-compose.yml` (racine du repo) |
| Account (auth GitHub) | Aucun requis (dépôt public) |

### Options de build activées

| Option | État | Raison |
|---|---|---|
| `run_build` (Pre Build Images) | ✅ Activé | Le compose n'utilise que des directives `build:` ; sans cette option, Komodo ne reconstruirait pas les images à jour avant chaque déploiement |
| Pre Pull Images | ✅ Activé (par défaut) | Sans effet direct ici (pas d'`image:` distante), laissé tel quel |
| Destroy Before Deploy | ⬜ Désactivé | Pas nécessaire pour un premier déploiement propre |
| Auto Update / Poll for Updates | ⬜ Désactivé (définitif) | Décision du professeur : le déploiement doit rester manuel, jamais automatique |
| Webhook GitHub | ⬜ Supprimé (définitif) | Un webhook avait été créé puis testé, mais supprimé sur consigne du professeur : le déploiement doit être déclenché uniquement manuellement, pas à chaque push |

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

### Choix : déploiement manuel (pas de webhook)

Un webhook de déploiement automatique avait initialement été testé (ajouté
côté GitHub, pointant vers l'URL générée par Komodo). Le test a révélé une
erreur 401 (absence de signature/secret non aligné entre GitHub et Komodo).

Avant de corriger ce point, le professeur a précisé que le déploiement doit
rester **manuel** : chaque mise en production doit être déclenchée
volontairement via le bouton **Deploy** dans Komodo, jamais automatiquement
suite à un push.

En conséquence :
- Le webhook a été **désactivé côté Komodo** (`Webhook Enabled: Disabled`)
- Le webhook a été **supprimé côté GitHub** (`Settings > Webhooks`)
- Les options `Poll for Updates`, `Auto Update` et `Full Stack Auto Update`
  restent désactivées de façon définitive


## Historique de configuration

- Configuration initiale : branche `main` (cohérente avec les règles Git du projet, `main` = versions stables).
- Correction : branche changée pour `develop`, sur demande de la responsable du groupe, tant que le lien GitHub <-> Komodo n'a pas encore été testé en conditions réelles. Le passage à `main` sera fait une fois ce lien validé.

## Procédure de déploiement manuel

Le déploiement est déclenché exclusivement par une action humaine, selon
la procédure suivante :

1. S'assurer que la branche `develop` est à jour et stable (toutes les
   Pull Requests concernées ont été relues et fusionnées).
2. Prévenir l'équipe (notamment Hiba, responsable de l'API/Docker) avant
   de déclencher le déploiement, pour éviter tout conflit avec un travail
   en cours.
3. Se connecter à Komodo (`komodo.s3.fsbm.ma`), ouvrir le stack
   `prediction_de_l_abandon_universitaire`.
4. Vérifier dans l'onglet **Config** que la branche pointée est bien
   `develop` (ou `main`, une fois le passage en production validé).
5. Cliquer sur **Deploy**.
6. Suivre la progression dans l'onglet **Log**.
7. Une fois le déploiement terminé, vérifier dans l'onglet **Services**
   que les 4 services (`api`, `mlflow`, `dagster-webserver`,
   `dagster-daemon`) sont bien à l'état `Running`.
8. Vérifier manuellement l'endpoint de santé de l'API
   (`GET /health`) pour confirmer le bon fonctionnement.

## État actuel

- ✅ Configuration Git Repo sauvegardée dans Komodo (`Save`)
- ✅ Webhook testé, puis désactivé/supprimé sur consigne du professeur
  (déploiement manuel exclusivement)
- ✅ **Premier déploiement manuel réussi** (06/09/2026, commit `fcc1dcb`,
  branche `develop`) : les 4 services (`api`, `mlflow`,
  `dagster-webserver`, `dagster-daemon`) sont à l'état `RUNNING`.
- ✅ Vérification interne de l'API : `GET /health` répond
  `{"status":"ok"}` (testé via le terminal Komodo, directement dans le
  conteneur `api`, sur le port interne 8000).
- ⚠️ **Accès externe non fonctionnel** : l'adresse publique
  (`41.250.197.226:3501`) n'est pas joignable depuis l'extérieur du
  réseau de l'école (timeout de connexion). L'application fonctionne
  correctement ; il s'agit d'une restriction réseau/pare-feu côté
  infrastructure, à clarifier avec l'administrateur du serveur `vh3`.

## Prochaines étapes

1. Clarifier avec l'administrateur si le serveur `vh3` est accessible
   uniquement depuis le réseau de l'école, ou si une ouverture de port
   est nécessaire pour un accès externe au port 3501.
2. Une fois l'accès externe confirmé ou configuré, valider `GET /health`
   depuis l'extérieur du réseau.
3. Basculer la configuration de la branche `develop` vers `main` une
   fois le fonctionnement validé en conditions réelles par l'équipe.
