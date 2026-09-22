Sprint 1 — DataOps & Qualité

SCRUM-48 — Gérer les branches et Pull Requests

Critères d’acceptation :

  - Une branche dédiée est créée pour chaque fonctionnalité développée.
 - Les développements sont réalisés sur les branches feature/* et non directement sur main.
 - Une Pull Request est créée pour intégrer une fonctionnalité dans develop.
 - La Pull Request est revue avant sa fusion.
 - Les modifications validées sont fusionnées dans develop.
 - La branche main reste réservée aux versions stables.

SCRUM-21 — Ingestion automatique du dataset

Critères d’acceptation :

  - Le dataset xAPI-Edu-Data.csv est correctement chargé par le pipeline d’ingestion.
 - Les données sont lues sans erreur.
 - Les colonnes du dataset sont correctement standardisées.
 - Les données sont chargées automatiquement dans la source de données RAW.
 - Le pipeline d’ingestion s’exécute sans erreur.
 - Le nombre de lignes ingérées est vérifiable après l'exécution.

SCRUM-22 — Stockage des données brutes

Critères d’acceptation :

  - Les données brutes sont stockées dans la base DuckDB du projet.
 - Les données sont accessibles dans la table RAW dédiée.
 -	La structure de la table correspond aux données ingérées.
 - Les identifiants _dlt_id sont conservés.
 - Les données stockées peuvent être utilisées par les étapes suivantes du pipeline.
 - Le nombre de lignes stockées peut être vérifié après l’ingestion.

SCRUM-24 — Transformation des données brutes

Critères d’acceptation :
 
 - Les données RAW sont correctement récupérées depuis DuckDB.
 - Les transformations sont réalisées avec dbt.
 - Les modèles dbt sont exécutés sans erreur.
 - Les données transformées sont disponibles dans le schéma main.
 - Les doublons métier identifiés dans les données sont traités lors de la préparation des données.
 - Les données préparées sont exploitables par les étapes Machine Learning.


SCRUM-27 — Contrôle de la qualité des données

User Story :

En tant que membre de l'équipe DataOps, je veux contrôler la qualité des données afin de garantir que les données utilisées par le Machine Learning sont fiables.

Critères d’acceptation :

 - Les colonnes obligatoires sont présentes.
 - Les valeurs nulles sont contrôlées conformément au Data Contract.
 - Les valeurs autorisées et les plages numériques sont vérifiées.
 - Les doublons de lignes sont détectés.
 - L’unicité des identifiants _dlt_id est vérifiée.
 - Les doublons métier sont détectés dans les données RAW.
 - Les règles métier sont vérifiées sur les données préparées.
 - Les anomalies bloquantes sont signalées comme des erreurs.
 - Les anomalies non bloquantes sont signalées comme des warnings.
 - Un statut global PASS, PASS_WITH_WARNINGS ou FAIL est généré.


SCRUM-29 — Orchestration du pipeline avec Dagster

Critères d’acceptation :

 - Les différentes étapes du pipeline sont définies comme des assets Dagster.
 - Les dépendances entre les étapes sont correctement définies.
 - L’ingestion peut être exécutée depuis Dagster.
 - La transformation peut être exécutée depuis Dagster.
 - Le contrôle de qualité peut être exécuté depuis Dagster.
 - L’exécution du pipeline est visible depuis l’interface Dagster.
 - Les erreurs d’exécution sont identifiables depuis Dagster.
 - Le pipeline respecte l’ordre logique des dépendances entre les différentes étapes.

-----------------
Sprint 2 — ML & MLOps

SCRUM-28 — Préparation des données ML

User Story :

En tant que ML Engineer, je veux préparer les données pour l'entraînement afin de disposer de jeux de données propres et adaptés aux modèles de Machine Learning.

Critères d’acceptation
 - Les données validées sont récupérées depuis la source préparée.
 - Les variables catégorielles sont correctement traitées.
 - Les variables numériques sont correctement préparées.
 - Les données sont séparées en jeux Train, Validation et Test.
 - Le prétraitement est appliqué de manière cohérente aux différents jeux de données.
 - Le scaler est ajusté (fit) uniquement sur le jeu d'entraînement.
 - Le scaler est ensuite appliqué (transform) aux jeux de validation et de test.
 - Les données préparées sont sauvegardées dans data/processed/.
 - Les noms des features utilisés par le modèle sont conservés.

SCRUM-30 — Entraîner le modèle

User Story :

En tant que ML Engineer, je veux entraîner plusieurs modèles de classification afin de sélectionner celui qui prédit le mieux le risque de décrochage universitaire.

Critères d’acceptation
 - Plusieurs algorithmes de classification sont entraînés.
 - Les modèles utilisés comprennent Logistic Regression, Random Forest et XGBoost.
 - Chaque modèle est entraîné uniquement sur le jeu d'entraînement.
 - Les performances des modèles sont mesurées sur le jeu de validation.
 - Les résultats des modèles sont comparables à l'aide des mêmes métriques.
 - Le meilleur modèle est sélectionné sur la base des performances de validation.
 - Le modèle sélectionné est sauvegardé dans ml/models/.
 - Le modèle entraîné peut être rechargé pour effectuer des prédictions.


SCRUM-31 — Évaluation et validation du modèle

User Story :

En tant que ML Engineer, je veux évaluer le modèle sélectionné afin de vérifier sa capacité à généraliser sur des données non utilisées pendant l'entraînement.

Critères d’acceptation
 - Le meilleur modèle est évalué sur le jeu de test.
 -	L'Accuracy est calculée sur le jeu de test.
 -	La Precision est calculée.
 -	Le Recall est calculé.
 -	Le F1-score est calculé.
 -	Une matrice de confusion est générée.
 -	Les performances du modèle sont comparées entre validation et test.
 -	Les résultats sont documentés dans le projet.
 -	Le modèle est considéré comme acceptable si ses performances respectent le seuil défini dans le projet.


SCRUM-32 — Versionner le modèle avec MLflow

User Story :

En tant que MLOps Engineer, je veux versionner et tracer les modèles avec MLflow afin d'assurer la reproductibilité et la traçabilité des expériences.

Critères d’acceptation
 -	Une expérience MLflow dédiée au projet est disponible.
 -	Chaque entraînement peut être associé à un Run MLflow.
 - Les paramètres importants de l'entraînement sont  enregistrés.
 -	Les métriques d'évaluation sont enregistrées.
 -	Les artefacts nécessaires au modèle sont enregistrés.
 -	Le modèle entraîné peut être identifié à partir de son Run.
 -	Les versions du modèle peuvent être distinguées.
 -	Le modèle sélectionné peut être enregistré dans le Model Registry.
 -	Les informations de versionnement sont conservées pour permettre la reproductibilité.


SCRUM-33 — Monitoring du modèle

User Story :

En tant que MLOps Engineer, je veux surveiller les performances du modèle afin de détecter une éventuelle dégradation de ses performances.

Critères d’acceptation
 -	Les métriques du modèle peuvent être consultées après chaque exécution.
-	Les performances du modèle sont suivies dans le temps.
-	Une dégradation des performances peut être identifiée.
-	Un seuil minimal de performance est défini.
-	Une alerte ou un signal est généré lorsque les performances passent sous le seuil défini.
-	Les informations de monitoring sont accessibles à l'équipe.

 ------------------

 Sprint 3 — Déploiement & Industrialisation

 SCRUM-39 — Développer une API REST

User Story :

En tant qu'utilisateur, je veux accéder au modèle de prédiction à travers une API REST afin de pouvoir obtenir une prédiction de risque de décrochage universitaire.

Critères d’acceptation
-	Une API REST est développée avec FastAPI.
-	L'API peut démarrer sans erreur.
-	Un endpoint de prédiction est disponible.
-	L'API accepte les caractéristiques nécessaires à une prédiction.
-	Les données reçues sont validées avant la prédiction.
-	Le modèle et le scaler sont correctement chargés.
-	L'API retourne une prédiction exploitable.
-	Les erreurs de données entrantes sont correctement gérées.
-	L'API est accessible depuis l'extérieur du conteneur.
-	La documentation interactive de l'API est accessible via Swagger.


 SCRUM-40 — Conteneuriser l'application

User Story :

En tant que Deployment Engineer, je veux conteneuriser l'application afin de garantir une exécution reproductible de l'API.

Critères d’acceptation
-	Un Dockerfile est disponible pour l'API.
-	L'image Docker de l'API peut être construite sans erreur.
-	Les dépendances Python nécessaires sont installées dans l'image.
-	Le modèle et les artefacts nécessaires sont accessibles par l'application.
-	Le conteneur démarre correctement.
-	L'API écoute sur le port prévu dans le conteneur.
-	L'API est accessible depuis l'extérieur du conteneur.
-	Le conteneur peut être recréé à partir du Dockerfile sans configuration manuelle supplémentaire.

 SCRUM-41 — Orchestrer les services avec Docker

User Story :

En tant que Deployment Engineer, je veux orchestrer les différents services avec Docker Compose afin de pouvoir démarrer l'ensemble de la solution de manière cohérente.

Critères d’acceptation
-	Un fichier docker-compose.yml permet de définir les différents services.
-	Le service API est défini dans le fichier Compose.
-	Le service MLflow est défini dans le fichier Compose.
-	Les services Dagster nécessaires sont définis dans le fichier Compose.
-	Les volumes nécessaires sont configurés.
-	Les dépendances et configurations nécessaires sont définies.
-	Les services peuvent être démarrés avec une seule commande Docker Compose.
-	Les services démarrent sans erreur bloquante.
-	Les ports utilisés par le projet sont correctement configurés.


 SCRUM-42 — Mettre en place un pipeline CI/CD

User Story :

En tant que DevOps Engineer, je veux mettre en place un pipeline CI/CD afin d'automatiser les vérifications et la préparation du déploiement de l'application.

Critères d’acceptation
-	Un workflow GitHub Actions est configuré.
-	Le workflow se déclenche automatiquement lors des événements Git définis.
-	L'environnement Python est correctement configuré.
-	Les dépendances du projet sont installées automatiquement.
-	Les tests sont exécutés automatiquement.
-	Une erreur de test entraîne l'échec du pipeline.
-	Le pipeline permet de vérifier que le projet est prêt à être déployé.
-	Le statut de l'exécution est visible dans GitHub Actions.

 SCRUM-44 — Déploiement automatisé

User Story :

En tant que DevOps Engineer, je veux automatiser le déploiement de l'application afin de rendre la mise en production reproductible.

Critères d’acceptation
-	Le déploiement de l'application peut être déclenché automatiquement.
-	La version à déployer provient du dépôt Git configuré.
-	Le déploiement utilise la configuration Docker Compose prévue pour le projet.
-	Les images nécessaires sont construites ou récupérées correctement.
-	Les services sont démarrés après le déploiement.
-	L'API est accessible après le déploiement.
-	Une vérification permet de confirmer que le service fonctionne.
-	Le Stack du projet est correctement configuré dans Komodo.
-	Le dépôt Git utilisé par le Stack pointe vers la branche develop.
-	Le docker-compose.yml utilisé est celui du projet.
-	Le déploiement est limité aux ressources du groupe.


 SCRUM-45 — Monitoring du service déployé

User Story :

En tant que DevOps Engineer, je veux surveiller le service déployé afin de détecter rapidement les problèmes de disponibilité ou de fonctionnement.

Critères d’acceptation
 -	L'état des conteneurs peut être vérifié.
-	La disponibilité de l'API peut être vérifiée.
-	Les logs du service sont accessibles.
-	Une erreur de démarrage du service peut être identifiée.
-	Les problèmes liés au conteneur peuvent être diagnostiqués à partir des logs.
-	Un contrôle de santé de l'API est disponible.
-	Le fonctionnement du service après déploiement peut être vérifié.
