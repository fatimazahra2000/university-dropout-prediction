Sprint Review

À l'issue du Sprint 2, l'équipe a présenté les fonctionnalités relatives à la construction et à l'évaluation du modèle de Machine Learning. Le Sprint avait pour objectif de transformer les données préparées en un modèle capable de classifier le risque de décrochage universitaire.

Les données ont été préparées pour l'entraînement et séparées en jeux Train, Validation et Test. Plusieurs algorithmes de classification ont ensuite été comparés, notamment la Logistic Regression, le Random Forest et XGBoost.

Les résultats obtenus sur le jeu de validation montrent que le Random Forest présente les meilleures performances avec une Accuracy de 81,94 %, contre 80,56 % pour XGBoost et 69,44 % pour la Logistic Regression. Le Random Forest a donc été retenu comme modèle candidat.

Une évaluation finale sur le jeu de test a ensuite été réalisée. Le modèle sélectionné obtient une Accuracy de 76 %. La matrice de confusion et les différentes métriques d'évaluation ont également été utilisées afin d'analyser les erreurs de classification entre les trois catégories de risque.

Le Sprint a également préparé l'intégration du modèle dans la partie MLOps, notamment à travers la sauvegarde des artefacts nécessaires à sa reproductibilité et l'intégration avec MLflow, le modèle Random Forest a été identifié comme le meilleur modèle sur le jeu de validation et les résultats obtenus ont permis de préparer son intégration dans le pipeline MLOps.