# Guide d'Installation FOFAL ERP

## Prérequis

### Backend
- Python 3.10+
- PostgreSQL 14+
- Redis 6+
- Poetry (gestionnaire de dépendances)

### Frontend
- Node.js 16+
- npm 8+
- Yarn (optionnel)

### Outils
- Git
- Docker (optionnel)
- Make (optionnel)

## Installation

### 1. Cloner le Repository
```bash
git clone https://github.com/Kaiser9005/fofal_erp_2024.git
cd fofal_erp_2024
```

### 2. Backend

#### Configuration de l'Environnement Python
```bash
# Créer l'environnement virtuel
python -m venv venv

# Activer l'environnement
source venv/bin/activate  # Linux/Mac
# ou
.\venv\Scripts\activate  # Windows

# Installer les dépendances
pip install -r requirements.txt
```

#### Configuration de la Base de Données
```bash
# Créer la base de données PostgreSQL
createdb fofal_erp

# Copier le fichier d'environnement
cp .env.example .env

# Éditer .env avec vos paramètres
DATABASE_URL=postgresql://user:password@localhost/fofal_erp
REDIS_URL=redis://localhost:6379
SECRET_KEY=your-secret-key
```

#### Migrations
```bash
# Initialiser Alembic
alembic init migrations

# Appliquer les migrations
alembic upgrade head

# Charger les données initiales
python scripts/seed_data.py
```

### 3. Frontend

#### Installation des Dépendances
```bash
# Installer les dépendances
cd frontend
npm install

# ou avec Yarn
yarn install
```

#### Configuration Frontend
```bash
# Copier la configuration
cp .env.example .env.local

# Éditer .env.local avec vos paramètres
VITE_API_URL=http://localhost:8000
VITE_WEATHER_API_KEY=your-weather-api-key
```

## Configuration des Modules

### 1. Module Production
```bash
# Configuration météo
WEATHER_API_KEY=your-key
WEATHER_API_URL=https://api.weather.com

# Configuration cartographie
MAP_PROVIDER_KEY=your-key
```

### 2. Module Gestion de Projets
```bash
# Configuration stockage documents
STORAGE_PROVIDER=s3
STORAGE_ACCESS_KEY=your-key
STORAGE_SECRET_KEY=your-secret
STORAGE_BUCKET=your-bucket
```

### 3. Module Finance
```bash
# Configuration devise
DEFAULT_CURRENCY=XAF
EXCHANGE_RATE_API_KEY=your-key
```

### 4. Module RH
```bash
# Configuration email
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USER=your-user
SMTP_PASSWORD=your-password
```

## Démarrage

### Backend
```bash
# Démarrer le serveur de développement
uvicorn main:app --reload

# Avec configuration personnalisée
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Frontend
```bash
# Mode développement
npm run dev

# Build production
npm run build
```

## Vérification de l'Installation

### 1. Services
- Backend API: http://localhost:8000
- Frontend: http://localhost:5173
- Documentation API: http://localhost:8000/docs
- Admin Interface: http://localhost:8000/admin

### 2. Tests
```bash
# Tests backend
pytest

# Tests avec couverture
pytest --cov=app

# Tests frontend
cd frontend
npm run test
```

### 3. Linting et Formatage
```bash
# Backend
flake8
black .
isort .

# Frontend
npm run lint
npm run format
```

## Docker (Optionnel)

```bash
# Build des images
docker-compose build

# Démarrage des services
docker-compose up -d

# Logs
docker-compose logs -f
```

## Troubleshooting

### Base de Données
```bash
# Réinitialiser la base
dropdb fofal_erp
createdb fofal_erp
alembic upgrade head

# Vérifier les migrations
alembic current
alembic history
```

### Cache
```bash
# Nettoyer le cache Redis
redis-cli flushall

# Vérifier le statut
redis-cli ping
```

### Logs
```bash
# Logs backend
tail -f logs/app.log

# Logs frontend
npm run dev -- --debug
```

## Support

Pour toute assistance :
- Documentation : /docs
- Issues : GitHub Issues
- Email : support@fofal.com

## Notes de Sécurité

1. Ne jamais commiter les fichiers .env
2. Utiliser des mots de passe forts
3. Configurer le pare-feu
4. Activer HTTPS en production
5. Mettre à jour régulièrement les dépendances
