 Sprint Retrospective
Points positifs
-	Les données nécessaires à l'entraînement étaient disponibles. 
-	Plusieurs modèles ont pu être comparés selon les mêmes critères. 
-	La séparation entre Train, Validation et Test a permis d'évaluer correctement la généralisation du modèle. 
-	Le Random Forest a obtenu les meilleures performances sur le jeu de validation. 
-	Les artefacts nécessaires à la réutilisation du modèle ont été sauvegardés. 
Difficultés rencontrées
-	La préparation des données devait rester cohérente entre l'entraînement et les futures prédictions. 
-	Une attention particulière a été nécessaire concernant l'utilisation du scaler afin d'éviter les fuites de données. 
-	Les performances sur le jeu de test sont inférieures à celles observées sur la validation. 
-	L'interprétation du Recall de la classe High Risk reste importante, celui-ci étant actuellement de 0,62. 
-	L'intégration du modèle avec MLflow nécessite une coordination avec les composants MLOps. 
Actions d'amélioration
-	Vérifier systématiquement le pipeline de prétraitement avant chaque entraînement. 
-	Conserver les mêmes artefacts de prétraitement pour les futures prédictions. 
-	Suivre plusieurs métriques au lieu de se limiter à l'Accuracy. 
-	Améliorer progressivement le suivi des expériences avec MLflow. 
-	Préparer l'intégration du modèle avec l'API avant le Sprint de déploiement.
