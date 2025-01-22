## Instructions de Vérification de l'Installation

### 1. Vérification de l'environnement

1. **Vérifier les versions des outils** :
   ```bash
   python --version  # Python 3.8 ou supérieur
   node --version   # Node.js 14 ou supérieur
   npm --version    # NPM 6 ou supérieur
   psql --version   # PostgreSQL 12 ou supérieur
   ```

2. **Vérifier les variables d'environnement** :
   ```bash
   # Vérifier que le fichier .env existe et contient toutes les variables nécessaires
   cat .env
   ```
   Variables requises :
   - DATABASE_URL
   - OPENWEATHER_API_KEY
   - IOT_API_KEY
   - ADMIN_USERNAME
   - ADMIN_PASSWORD
   - ADMIN_EMAIL
   - BACKEND_URL

### 2. Vérification de la Base de Données

1. **Vérifier la connexion à la base de données** :
   ```bash
   psql -d erp_db -c "\dt"  # Liste toutes les tables
   ```

2. **Vérifier l'état des migrations** :
   ```bash
   alembic current  # Affiche la révision actuelle
   alembic history  # Affiche l'historique des migrations
   ```

### 3. Vérification des API Externes

1. **Vérifier l'API OpenWeather** :
   ```bash
   curl "http://api.openweathermap.org/data/2.5/weather?q=Paris&appid=VOTRE_CLE_API"
   ```
   Consultez `userInstructions/obtenir_cles_api.md` pour obtenir une clé API.

2. **Vérifier l'API IoT** :
   ```bash
   # Utilisez la commande fournie dans la documentation IoT
   curl "https://api.iot-platform.com/status?key=VOTRE_CLE_API"
   ```
   Consultez `userInstructions/obtenir_cles_api.md` pour obtenir une clé API.

### 4. Exécution des Tests

1. **Tests Unitaires** :
   ```bash
   # Backend
   pytest tests/  # Tous les tests
   pytest tests/test_tache_service.py  # Test spécifique
   
   # Frontend
   cd frontend
   npm run test
   ```

2. **Tests d'Intégration** :
   ```bash
   pytest tests/integration/  # Tous les tests d'intégration
   pytest tests/integration/test_tache_integration.py  # Test spécifique
   ```

3. **Tests End-to-End** :
   ```bash
   # Installation de Playwright
   cd tests/e2e
   npm install @playwright/test
   npx playwright install

   # Exécution des tests
   npm run test:e2e  # Tous les tests e2e
   npx playwright test test_gestion_agricole.py  # Test spécifique
   ```

### 5. Vérification du Démarrage

1. **Backend** :
   ```bash
   python main.py
   # Vérifier que le serveur démarre sur http://localhost:8000
   # Vérifier les logs pour d'éventuelles erreurs
   ```

2. **Frontend** :
   ```bash
   cd frontend
   npm run dev
   # Vérifier que l'application démarre sur http://localhost:3000
   ```

3. **Vérifier l'Interface Utilisateur** :
   - Accéder à http://localhost:3000
   - Se connecter avec les identifiants administrateur
   - Vérifier que le tableau de bord s'affiche correctement
   - Vérifier que les données météo sont chargées
   - Vérifier que les capteurs IoT sont connectés

### 6. Résolution des Problèmes Courants

1. **Erreur de Base de Données** :
   - Vérifier que PostgreSQL est en cours d'exécution
   - Vérifier les permissions de l'utilisateur
   - Consulter `userInstructions/grant_alembic_permissions.md`

2. **Erreur d'API** :
   - Vérifier la validité des clés API
   - Consulter `userInstructions/obtenir_cles_api_gratuites.md`

3. **Erreur de Migration** :
   - Réinitialiser la base de données si nécessaire
   - Consulter `userInstructions/reexecuter_creation_admin.md`

4. **Erreur de Dépendances** :
   - Mettre à jour les dépendances :
     ```bash
     pip install -r requirements.txt --upgrade
     cd frontend && npm update
     ```

### 7. Vérification de la Sécurité

1. **Vérifier HTTPS** (en production) :
   - Certificat SSL valide
   - Redirection HTTP vers HTTPS

2. **Vérifier l'Authentification** :
   - Test de création de compte
   - Test de connexion/déconnexion
   - Test de réinitialisation de mot de passe

3. **Vérifier les Autorisations** :
   - Test des rôles utilisateur
   - Test des restrictions d'accès
   - Test des permissions sur les ressources

### 8. Documentation

Consulter les fichiers suivants pour plus d'informations :
- `docs/README.md` - Documentation générale
- `docs/developpement_futur.md` - Prochaines étapes
- `docs/tests.md` - Documentation détaillée des tests
- `cline_docs/mvpAcceptanceCriteria.md` - Critères d'acceptation MVP