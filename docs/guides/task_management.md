# Guide de Gestion des Tâches

## Vue d'ensemble

Le module de gestion des tâches permet de planifier, suivre et gérer les tâches du projet agricole. Il intègre des fonctionnalités avancées comme la gestion des ressources, le suivi météorologique et la gestion des dépendances entre tâches.

## Fonctionnalités Principales

### 1. Liste des Tâches

La page principale affiche la liste des tâches avec :
- Filtrage par statut et catégorie
- Pagination des résultats
- Indicateurs de progression
- Accès rapide aux actions (édition, suppression, météo)

Pour accéder à la liste :
1. Cliquez sur "Projets" dans le menu principal
2. Sélectionnez un projet
3. La liste des tâches s'affiche automatiquement

### 2. Création d'une Tâche

Pour créer une nouvelle tâche :
1. Cliquez sur le bouton "Nouvelle Tâche"
2. Remplissez les informations générales :
   - Titre et description
   - Statut et priorité
   - Catégorie
   - Dates de début et fin
   - Progression

3. Configuration météorologique (optionnel) :
   - Activez "Tâche dépendante de la météo"
   - Définissez les contraintes :
     - Température min/max
     - Vitesse du vent maximale
     - Précipitations maximales

4. Gestion des ressources :
   - Cliquez sur "Ajouter une ressource"
   - Sélectionnez une ressource dans la liste
   - Indiquez la quantité requise

5. Gestion des dépendances :
   - Cliquez sur "Ajouter une dépendance"
   - Sélectionnez une tâche existante
   - Choisissez le type de dépendance :
     - Fin pour début : la tâche dépendante ne peut commencer qu'après la fin de la tâche requise
     - Début pour début : les tâches doivent commencer ensemble
     - Fin pour fin : les tâches doivent se terminer ensemble

### 3. Suivi Météorologique

Pour les tâches dépendantes de la météo :
1. Un icône météo apparaît dans la liste des tâches
2. Cliquez sur l'icône pour accéder aux DétailsMétéoTâche qui affichent :
   - Conditions météo actuelles détaillées
   - Statut de compatibilité avec les contraintes définies
   - Alertes et avertissements spécifiques
   - Recommandations pour l'exécution
   - Historique météo récent
   - Prévisions pour les prochaines heures

Le système analyse automatiquement :
- La compatibilité des conditions actuelles
- Les risques potentiels
- Les périodes optimales d'exécution
- Les ajustements recommandés

Intégration avec le TableauMeteoParcelleaire :
- Vue consolidée des conditions par parcelle
- Alertes spécifiques aux zones de travail
- Données des capteurs IoT locaux
- Tendances et prévisions localisées

### 4. Gestion des Ressources

Le système gère automatiquement :
- La réservation des ressources à la création
- Le suivi de l'utilisation
- La libération des ressources à la fin

Pour mettre à jour l'utilisation :
1. Ouvrez la tâche en édition
2. Dans la section ressources
3. Mettez à jour la quantité utilisée

### 5. Statuts et Progression

Les statuts disponibles :
- À FAIRE : tâche créée mais non démarrée
- EN COURS : tâche en cours de réalisation
- EN ATTENTE : tâche suspendue temporairement
- TERMINÉE : tâche complétée
- ANNULÉE : tâche abandonnée

La progression :
- Mise à jour manuelle (0-100%)
- Mise à jour automatique à 100% quand terminée

### 6. Dépendances

Points importants :
- Une tâche peut dépendre de plusieurs autres
- Les dépendances circulaires sont empêchées
- Le système vérifie la cohérence des dates

## Bonnes Pratiques

1. Planification :
   - Définissez clairement les objectifs
   - Estimez réalistement les durées
   - Identifiez les dépendances en amont

2. Ressources :
   - Vérifiez la disponibilité avant création
   - Mettez à jour régulièrement l'utilisation
   - Libérez les ressources non utilisées

3. Météo :
   - Définissez des contraintes réalistes
   - Consultez les prévisions avant planification
   - Prévoyez des alternatives si nécessaire
   - Utilisez les données des capteurs IoT locaux
   - Tenez compte des spécificités des parcelles

4. Suivi :
   - Mettez à jour régulièrement les statuts
   - Documentez les problèmes rencontrés
   - Ajustez les estimations si nécessaire

## Résolution des Problèmes

### Problèmes Courants

1. "Impossible de créer une dépendance"
   - Vérifiez qu'il n'y a pas de dépendance circulaire
   - Vérifiez la cohérence des dates

2. "Ressources insuffisantes"
   - Vérifiez la disponibilité actuelle
   - Ajustez la quantité requise
   - Planifiez pour une date ultérieure

3. "Conditions météo défavorables"
   - Vérifiez les contraintes définies
   - Consultez les prévisions détaillées
   - Utilisez le TableauMeteoParcelleaire
   - Envisagez un report ou une adaptation

### Support

Pour toute assistance :
1. Consultez la documentation technique
2. Contactez l'équipe support
3. Signalez les bugs via le système de tickets

## Intégration avec Autres Modules

Le module de tâches s'intègre avec :

1. Production :
   - Suivi des cycles de culture
   - Planification des récoltes
   - Gestion des parcelles

2. Ressources Humaines :
   - Attribution des tâches
   - Planification des équipes
   - Suivi des compétences

3. Inventaire :
   - Gestion des stocks
   - Réservation des ressources
   - Suivi des consommations

4. Finance :
   - Suivi des coûts
   - Budgétisation
   - Analyses de rentabilité

## Mises à Jour à Venir

Prochaines fonctionnalités prévues :
1. Tableaux de bord avancés
2. Rapports personnalisés
3. Notifications automatiques
4. Application mobile
5. Intégration calendrier

## Annexes

### A. Types de Dépendances

1. Fin pour début (FS) :
   - La plus commune
   - B ne peut commencer qu'après A
   - Exemple : préparation sol → plantation

2. Début pour début (SS) :
   - Démarrage simultané
   - Exemple : irrigation → fertilisation

3. Fin pour fin (FF) :
   - Fin simultanée requise
   - Exemple : récolte → transport

### B. Contraintes Météo

Paramètres configurables :
1. Température :
   - Minimale : seuil bas acceptable
   - Maximale : seuil haut acceptable
   - Impact sur la sécurité et l'efficacité

2. Vent :
   - Vitesse maximale en km/h
   - Important pour traitements
   - Sécurité des opérateurs

3. Précipitations :
   - Quantité maximale en mm
   - Critique pour travaux extérieurs
   - Impact sur la qualité du travail

Intégration IoT :
- Données en temps réel des capteurs
- Alertes automatiques
- Historique détaillé
- Prévisions localisées

### C. Raccourcis Clavier

- Ctrl + N : Nouvelle tâche
- Ctrl + E : Éditer la tâche sélectionnée
- Ctrl + D : Dupliquer la tâche
- Ctrl + Del : Supprimer la tâche
- F5 : Rafraîchir la liste
- F2 : Ouvrir les détails météo
