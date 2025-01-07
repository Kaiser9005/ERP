## Aperçu de la Base de Code

### Composants Clés et leurs Interactions

-   **Frontend (React)** : Interface utilisateur, gestion des interactions utilisateur, affichage des données. Utilise Vite pour le build et Vitest pour les tests. Situé dans le répertoire `frontend/`.
-   **Backend (FastAPI)** : API RESTful, logique métier, gestion des données, interactions avec la base de données. Situé dans les répertoires `api/`, `core/`, `db/`, `models/`, `schemas/`, et `services/`.
-   **Base de Données (PostgreSQL)** : Stockage persistant des données. Schémas détaillés dans `docs/diagrammes/db_schema.md`. Accès via l'ORM SQLAlchemy.
-   **Services ML** : Services d'analyse et de prédiction.
-   **Serveurs MCP** : Étendent les capacités de l'application avec des outils et services externes.

### Flux de Données

1. L'utilisateur interagit avec l'interface frontend.
2. Le frontend envoie des requêtes à l'API backend.
3. Le backend traite les requêtes, interagit avec la base de données et les services ML si nécessaire.
4. Le backend renvoie les données au frontend.
5. Le frontend affiche les données à l'utilisateur.

### Dépendances Externes

-   **Bibliothèques Python** : Listées dans `requirements.txt`.
    -   `fastapi` : Framework web pour le backend.
    -   `SQLAlchemy` : ORM pour interagir avec la base de données.
    -   `alembic`: Pour les migrations de base de données.
    -   `requests` : Pour les requêtes HTTP.
    -   `pandas` : Pour la manipulation de données.
    -   `scikit-learn` : Pour les algorithmes de machine learning.
-   **Bibliothèques React** : Listées dans `frontend/package.json`.
    -   `react` : Bibliothèque principale pour la construction de l'interface utilisateur.
    -   `vite` : Outil de build pour le frontend.
    -   `vitest` : Framework de test pour le frontend.
    -   `react-router-dom` : Pour la gestion des routes.
    -   `axios` : Pour les requêtes HTTP.
    -   `react-hook-form` : Pour la gestion des formulaires.
    -   `@tanstack/react-query` : Pour la gestion des données asynchrones.
-   **Services Externes** :
    -   API Météo : Pour les données météorologiques.
    -   API IoT : Pour les données des capteurs.
-   **SDK MCP** : Utilisé pour construire les serveurs MCP.

### Changements Significatifs Récents

-   Configuration initiale de la structure du projet.

### Intégration du Feedback Utilisateur et son Impact sur le Développement

-   Le feedback utilisateur est collecté via différents canaux et utilisé pour informer les priorités de développement et la correction de bugs.

### Notes Additionnelles

-   (Ajouter toute autre information pertinente)