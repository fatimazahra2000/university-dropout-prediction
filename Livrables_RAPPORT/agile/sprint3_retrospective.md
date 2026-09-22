Sprint Retrospective
Points positifs
-	La séparation entre le développement de l'application et son déploiement facilite l'industrialisation. 
-	Docker permet de disposer d'un environnement d'exécution reproductible. 
-	Docker Compose permet de centraliser la configuration des différents services. 
-	L'utilisation de GitHub Actions permet d'automatiser les vérifications du projet. 
-	Le déploiement sur l'environnement prévu permet de rapprocher la solution d'un contexte de production. 
Difficultés rencontrées
-	La coordination entre l'API, le modèle et les différents services Docker. 
-	La gestion des dépendances entre les conteneurs. 
-	La configuration des ports et des volumes dans l'environnement de déploiement. 
-	La nécessité de vérifier que les artefacts du modèle sont accessibles par l'API. 
-	La configuration du déploiement et des mécanismes de monitoring. 
Actions d'amélioration
-	Standardiser la configuration Docker. 
-	Ajouter des vérifications automatiques avant chaque déploiement. 
-	Mettre en place un health check de l'API. 
-	Améliorer la gestion des logs. 
-	Automatiser davantage le processus de déploiement. 
-	Documenter la procédure de déploiement et de restauration.
