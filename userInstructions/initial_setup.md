## Instructions de Configuration Initiale

1. **Cloner le dépôt Git** :
    ```bash
    git clone [URL du dépôt]
    cd [nom du dépôt]
    ```
2. **Installer les dépendances du backend** :
    ```bash
    pip install -r requirements.txt
    ```
3. **Installer les dépendances du frontend** :
    ```bash
    cd frontend
    npm install
    ```
3. **Installer les dépendances du frontend (backend)**:
    ```bash
    cd backend
    npm install
    ```
4. **Configurer la base de données** :
    - Assurez-vous que PostgreSQL est installé et en cours d'exécution. Vous pouvez télécharger PostgreSQL depuis [le site officiel](https://www.postgresql.org/download/).
    - Créez une base de données nommée `erp_db`. Vous pouvez utiliser l'interface graphique pgAdmin ou la ligne de commande :
        ```bash
        psql -U postgres
        CREATE DATABASE erp_db;
        \q
        ```
    - Configurez l'URL de la base de données dans votre fichier `.env`. Exemple :
        ```env
        DATABASE_URL=postgresql://votre_utilisateur:votre_mot_de_passe@localhost:5432/erp_db
        ```
    - Exécutez les migrations de la base de données pour créer les tables :
        ```bash
        alembic upgrade head
        ```
5. **Configurer les variables d'environnement** :
    - Créez un fichier `.env` à la racine du projet si ce n'est pas déjà fait.
    - Ajoutez les variables d'environnement nécessaires. Voici un exemple de contenu typique :
        ```env
        DATABASE_URL=postgresql://votre_utilisateur:votre_mot_de_passe@localhost:5432/erp_db
        OPENWEATHER_API_KEY=votre_clé_api_openweather
        IOT_API_KEY=votre_clé_api_iot
        ADMIN_USERNAME=admin
        ADMIN_PASSWORD=password123
        ADMIN_EMAIL=admin@example.com
        BACKEND_URL=http://localhost:8000
        ```
    - **Note** : Remplacez `votre_utilisateur`, `votre_mot_de_passe`, `votre_clé_api_openweather` et `votre_clé_api_iot` par vos valeurs réelles.
6. **Créer le premier utilisateur administrateur** :
    - Après avoir démarré le backend pour la première fois, vous pouvez créer le premier utilisateur administrateur en exécutant le script fourni :
        ```bash
        python scripts/create_admin.py
        ```
    - Ce script utilise l'endpoint `/api/v1/auth/first-admin` pour créer l'utilisateur avec les informations d'identification définies dans votre fichier `.env`.
    - Alternativement, vous pouvez créer l'utilisateur manuellement en utilisant `curl` :
        ```bash
        curl -X POST -H "Content-Type: application/json" -d '{"username": "admin", "email": "admin@example.com", "password": "password123"}' http://localhost:8000/api/v1/auth/first-admin
        ```
    - Veuillez consulter le fichier `userInstructions/creer_premier_admin.md` pour obtenir des instructions détaillées sur la création du premier utilisateur administrateur.
    - **Note** : Assurez-vous que le backend est en cours d'exécution avant d'exécuter le script ou la commande `curl`.
7. **Démarrer le backend** :
    ```bash
    python main.py
    ```
8. **Démarrer le frontend** :
    ```bash
    cd frontend
    npm run dev
    ```

**Note** : Remplacez les valeurs entre crochets par les valeurs appropriées.