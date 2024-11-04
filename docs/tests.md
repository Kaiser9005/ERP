# Guide des Tests FOFAL ERP

## Vue d'ensemble

Le système de tests de FOFAL ERP utilise pytest comme framework principal et est organisé en plusieurs catégories :

- Tests unitaires
- Tests d'intégration
- Tests de services
- Tests d'API

## Configuration

### Prérequis
```bash
pip install pytest pytest-asyncio pytest-cov
```

### Exécution des tests
```bash
# Tous les tests
pytest

# Avec couverture
pytest --cov=app

# Tests spécifiques
pytest tests/test_dashboard.py
```

## Structure des Tests

```
tests/
├── conftest.py          # Fixtures partagées
├── test_dashboard.py    # Tests du tableau de bord
├── test_weather.py      # Tests du service météo
└── test_activities.py   # Tests des activités
```

## Fixtures

Les fixtures principales sont définies dans `conftest.py` :
- `db`: Session de base de données de test
- `client`: Client de test FastAPI
- `test_user`: Utilisateur de test
- `test_data`: Données de test (parcelles, stocks, etc.)

## Bonnes Pratiques

1. Chaque test doit être indépendant
2. Utiliser les fixtures pour la configuration
3. Tester les cas normaux et les cas d'erreur
4. Maintenir une couverture de code > 80%
5. Documenter les cas de test complexes