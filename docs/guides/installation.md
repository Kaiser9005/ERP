# Guide d'Installation FOFAL ERP

## Prérequis

- Python 3.10+
- PostgreSQL 14+
- Poetry (gestionnaire de dépendances)

## Installation

1. Cloner le repository
```bash
git clone https://github.com/Kaiser9005/fofal_erp_2024.git
cd fofal_erp_2024
```

2. Créer l'environnement virtuel
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
.\venv\Scripts\activate  # Windows
```

3. Installer les dépendances
```bash
pip install -r requirements.txt
```

4. Configuration
```bash
cp .env.example .env
# Éditer .env avec vos paramètres
```

5. Initialiser la base de données
```bash
alembic upgrade head
```

## Démarrage

```bash
uvicorn main:app --reload
```

L'API sera disponible sur http://localhost:8000

## Tests

```bash
pytest
```

## Documentation API

La documentation Swagger est disponible sur http://localhost:8000/docs