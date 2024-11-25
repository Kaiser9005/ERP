# Documentation des Tests FOFAL ERP

## Vue d'ensemble

La documentation des tests de FOFAL ERP a été réorganisée pour une meilleure maintenabilité et lisibilité. Cette page sert de point d'entrée vers la documentation détaillée.

## Types de Tests

Le système de tests de FOFAL ERP utilise plusieurs niveaux de tests :

- Tests unitaires (Unit tests)
- Tests d'intégration (Integration tests)
- Tests end-to-end (E2E tests)
- Tests de services (Service tests)
- Tests ML (Machine Learning tests)

## Documentation Détaillée

La documentation complète est maintenant organisée dans le dossier `/docs/tests/` :

### Guides Principaux
- [Configuration et Prérequis](tests/guides/configuration.md)
- [Tests React et React Query](tests/guides/react.md)
- [Tests Machine Learning](tests/guides/ml.md)
- [Tests End-to-End](tests/guides/e2e.md)
- [Bonnes Pratiques](tests/guides/best_practices.md)
- [Maintenance](tests/guides/maintenance.md)

### Documentation Spécifique
- Tests ML des projets : [Projets ML Tests - Mars 2024](modules/projets_ml_tests_mars2024.md)
- Tests React Query : [Guide React Query](guides/typage.md)
- Tests E2E : [Guide E2E](guides/developpement.md)

## Structure des Tests

```
tests/
├── conftest.py                           # Fixtures partagées globales
├── test_*.py                            # Tests unitaires
├── e2e/                                 # Tests end-to-end
│   ├── conftest.py                     # Fixtures E2E
│   └── test_*.py                       # Tests E2E spécifiques
└── integration/                        # Tests d'intégration
    └── test_*_integration.py           # Tests d'intégration spécifiques
```

## Commandes Principales

```bash
# Installation des dépendances
pip install -r requirements.txt

# Tous les tests
pytest

# Tests avec couverture
pytest --cov=app

# Tests spécifiques
pytest tests/test_dashboard.py

# Tests E2E
pytest tests/e2e/

# Tests ML
pytest tests/test_projects_ml_service.py
pytest tests/integration/test_projects_ml_integration.py

# Tests Inventaire
pytest tests/integration/test_inventory_*.py
```

## Standards Globaux

1. Nommage des Tests
   - Tests unitaires : `test_*.py`
   - Tests d'intégration : `test_*_integration.py`
   - Tests E2E : `test_*_e2e.py`

2. Organisation
   - Un fichier de test par module/composant
   - Fixtures partagées dans `conftest.py`
   - Tests groupés par fonctionnalité

3. Documentation
   - Chaque test doit avoir une description claire
   - Les cas complexes doivent être documentés
   - Les fixtures doivent être documentées

## Support

Pour toute question sur les tests :
1. Consulter la documentation appropriée dans `/docs/tests/`
2. Voir les exemples dans le dossier `docs/tests/examples/`
3. Contacter l'équipe de développement

## Migration

Cette documentation est en cours de migration vers une structure plus modulaire. Les anciens guides sont progressivement déplacés vers la nouvelle structure dans `/docs/tests/`.

Pour plus de détails sur la nouvelle structure et les dernières mises à jour, consultez le [README de la documentation des tests](tests/README.md).
