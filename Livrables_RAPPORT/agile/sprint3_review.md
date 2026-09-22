À l'issue du Sprint 3, l'équipe a évalué les fonctionnalités liées à l'industrialisation et au déploiement de la solution. L'objectif est de rendre le modèle accessible à travers une API REST et de préparer son exécution dans un environnement conteneurisé et reproductible.

L'API FastAPI permet d'exposer le modèle de prédiction à travers un endpoint dédié. L'application est ensuite conteneurisée avec Docker afin de garantir un environnement d'exécution reproductible.

Les différents services nécessaires au fonctionnement de la solution sont regroupés à l'aide de Docker Compose. Le déploiement été ensuite préparé sur Komodo.

Enfin, des mécanismes de vérification du fonctionnement du service et d'accès aux logs sont utilisés afin de faciliter le suivi de l'application après son déploiement.