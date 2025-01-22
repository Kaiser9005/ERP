# Configuration de l'environnement de développement local

Ce guide fournit des instructions étape par étape pour configurer un environnement de développement local pour le projet ERP, sans utiliser Docker.

## Prérequis

-   Python 3.12 ou supérieur
-   Node.js 18 ou supérieur
-   npm 9 ou supérieur
-   PostgreSQL (installé et configuré)

## Configuration du Backend (FastAPI)

1. **Cloner le dépôt Git**

    ```bash
    git clone <URL_du_depot>
    cd ERP
    ```

2. **Créer un environnement virtuel**

    ```bash
    python3 -m venv venv
    ```

3. **Activer l'environnement virtuel**

    -   Sur macOS/Linux :

        ```bash
        source venv/bin/activate
        ``` 

    -   Sur Windows :

        ```bash
        venv\Scripts\activate
        ```

4. **Installer les dépendances**

    ```bash
    pip install -r requirements.txt
    ```

5. **Configurer les variables d'environnement**

    -   Créer un fichier `.env` à la racine du projet.
    -   Ajouter les variables d'environnement nécessaires (voir `example.env` pour un exemple).
    -   Remplacer les valeurs par celles correspondant à votre configuration locale.

    Exemple de fichier `.env` :

    ```
    DATABASE_URL=postgresql://user:password@localhost:5432/erp
    SECRET_KEY=your_secret_key
    ALEMBIC_DATABASE_URL=postgresql://user:password@localhost:5432/erp
    ```

6. **Exécuter les migrations de base de données**

    ```bash
    alembic upgrade head
    ```

7. **Lancer le serveur de développement**

    ```bash
    uvicorn main:app --reload
    ```

    Le serveur sera accessible à l'adresse `http://localhost:8000`.

## Configuration du Frontend (React)

1. **Naviguer vers le dossier frontend**

    ```bash
    cd frontend
    ```

2. **Installer les dépendances**

    ```bash
    npm install
    ```

3. **Configurer les variables d'environnement**

    -   Créer un fichier `.env` dans le dossier `frontend`.
    -   Ajouter les variables d'environnement nécessaires (voir `frontend/example.env` pour un exemple).
    -   Remplacer les valeurs par celles correspondant à votre configuration locale.

    Exemple de fichier `.env` :

    ```
    VITE_API_BASE_URL=http://localhost:8000/api/v1
    ```

4. **Lancer le serveur de développement**

    Depuis la racine du projet, lancer la commande suivante:

    ```bash
    cd frontend && npm run dev
    ```

    L'application sera accessible à l'adresse `http://localhost:5173` (ou un autre port si celui-ci est déjà utilisé).

## Remarques

-   Assurez-vous que PostgreSQL est installé et configuré correctement.
-   Remplacez les valeurs des variables d'environnement par celles correspondant à votre configuration locale.
-   Pour déboguer le backend, vous pouvez utiliser un débogueur Python comme `pdb` ou `ipdb`.
-   Pour déboguer le frontend, vous pouvez utiliser les outils de développement React intégrés aux navigateurs ou des outils de débogage comme `console.log`.
