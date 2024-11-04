# Guide de Développement FOFAL ERP

## Structure du Projet

```
fofal_erp/
├── api/
│   └── v1/
│       ├── endpoints/
│       │   ├── production.py
│       │   ├── inventaire.py
│       │   └── employes.py
│       └── __init__.py
├── core/
│   └── config.py
├── db/
│   └── database.py
├── models/
│   ├── production.py
│   ├── inventory.py
│   └── hr.py
├── schemas/
│   ├── production.py
│   ├── inventaire.py
│   └── employe.py
└── docs/
    ├── api/
    └── guides/
```

## Standards de Code

### Python
- Suivre PEP 8
- Utiliser les type hints
- Documenter avec docstrings
- Tests unitaires obligatoires

### Base de Données
- Utiliser les migrations Alembic
- Nommer les tables en français
- UUID pour les clés primaires
- Timestamps sur toutes les tables

## Processus de Développement

1. Créer une branche feature
2. Implémenter les tests
3. Développer la fonctionnalité
4. Documenter l'API
5. Review de code
6. Merger vers develop

## Tests

```bash
# Exécuter les tests
pytest

# Avec couverture
pytest --cov=app
```

## Documentation

- Documenter toutes les APIs
- Maintenir les guides à jour
- Inclure des exemples de code
- Documenter les modèles de données