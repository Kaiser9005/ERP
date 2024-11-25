# Documentation des Tests FOFAL ERP

## Vue d'ensemble

Cette documentation détaille l'ensemble des tests du système FOFAL ERP. Elle est organisée en plusieurs sections pour faciliter la navigation et la maintenance.

## Structure de la Documentation

### Guides
- [Configuration et Prérequis](guides/configuration.md)
- [Structure des Tests](guides/structure.md)
- [Tests React et React Query](guides/react.md)
- [Tests End-to-End](guides/e2e.md)
- [Bonnes Pratiques](guides/best_practices.md)
- [Maintenance](guides/maintenance.md)

### Modules
- [Tests Machine Learning](modules/ml.md)
- [Tests Inventaire](modules/inventory.md)
- [Tests Finance](modules/finance.md)
- [Tests Production](modules/production.md)
- [Tests RH](modules/hr.md)

### Exemples
- [Exemples React Query](examples/react_query.md)
- [Exemples ML](examples/ml.md)
- [Exemples E2E](examples/e2e.md)

## Commandes Principales

```bash
# Installation des dépendances
pip install -r requirements.txt

# Exécution de tous les tests
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

## Liens Utiles

- [Guide React Query](../guides/typage.md)
- [Guide E2E](../guides/developpement.md)
- [Tests ML des projets](../modules/projets_ml_tests_mars2024.md)

## Support

Pour toute question sur les tests :
1. Consulter la documentation appropriée dans les sections ci-dessus
2. Voir les exemples dans le dossier `examples/`
3. Contacter l'équipe de développement

## Maintenance de la Documentation

Cette documentation est divisée en plusieurs fichiers pour faciliter sa maintenance :
- Chaque guide est dans un fichier séparé dans `guides/`
- La documentation spécifique aux modules est dans `modules/`
- Les exemples sont dans `examples/`

Pour mettre à jour la documentation :
1. Identifier la section appropriée
2. Modifier le fichier correspondant
3. Mettre à jour ce README si nécessaire
4. Vérifier les liens et références
