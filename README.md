# FOFAL ERP 2024 - Système de Gestion Agricole Intégré

## Vue d'ensemble

FOFAL ERP est un système de gestion intégré spécialement conçu pour FOFAL (Family Land), une entreprise agricole spécialisée dans la culture du palmier à huile (70 ha) et des papayes (10 ha). Introduction prochaine de 10 hectares de BitterKola (garniciaKola).

## État du Projet

Le projet est en développement actif avec plusieurs modules à différents stades d'avancement :
- Production (100%) : 
  - Gestion complète des parcelles et cycles de culture
  - Dashboard météo en temps réel
  - Système d'alertes intelligent
  - Rapports de production avancés
  - Tests End-to-End et unitaires
  - Monitoring IoT optimisé
  - ML prédictif validé
- Gestion des Projets (100%) : 
  - Système de tâches complet
  - Intégration des données météo
  - Gestion des ressources
  - Tests d'intégration
  - Documentation utilisateur
  - ML prédictif
  - Architecture tests modulaire
  - Tests ML spécialisés
- Finance (95%) : 
  - Gestion budgétaire avancée
  - Analyse d'impact météo
  - Projections financières ML
  - Tests unitaires complets
  - Documentation API
  - Cache Redis optimisé
  - Recommandations ML
- Comptabilité (95%) :
  - Gestion complète des comptes et écritures
  - Dashboard financier avancé
  - Analyse budgétaire avec impact météo
  - Suivi de trésorerie en temps réel
  - Rapports comptables intelligents
  - Tests unitaires backend
  - Documentation API complète
  - Cache Redis optimisé
  - Intégration météo pour prévisions
  - ML prédictif
- RH (100%) : 
  - Gestion basique des employés
  - Structure des présences
  - Gestion des compétences agricoles
  - Gestion des contrats
  - Système de paie (backend)
    - Modèle de données ✓
    - Service métier ✓
    - API REST ✓
    - Tests unitaires et intégration ✓
    - Documentation API ✓
- Inventaire (100%) : 
  - Modèles de stocks
  - Mouvements de base
  - Traçabilité avancée
  - Intégration IoT
  - ML prédictif
  - Tests ML
  - Documentation ML

Pour plus de détails sur l'état actuel et les prochaines étapes, consultez notre [Plan de Développement](docs/plan_developpement.md).

## Architecture Tests ML

L'architecture modulaire des tests ML établit un nouveau standard pour le projet :

```python
tests/module_ml/
    test_base.py         # Tests ML de base
    test_optimization.py # Tests optimisation
    test_analysis.py     # Tests analyse
    test_weather.py      # Tests météo
    test_integration.py  # Tests intégration
    README.md           # Documentation
```

Cette architecture assure :
- Tests spécialisés par domaine
- Validation complète des modèles
- Monitoring des performances
- Documentation détaillée
- Maintenance facilitée
- Évolution contrôlée

## Modules Principaux

### 1. Production Agricole
- Gestion des parcelles
- Suivi des cycles de culture
- Monitoring météorologique
- Contrôle qualité des récoltes
- Planification agricole
- ML prédictif
- IoT monitoring

### 2. Gestion des Projets
- Planification des activités
- Suivi des tâches
- Gestion des ressources
- Rapports d'avancement
- Calendrier des projets
- ML prédictif
- Tests modulaires

### 3. Comptabilité et Finance
- Comptabilité générale complète
- Dashboard financier interactif
- Analyse budgétaire intelligente
- Suivi de trésorerie en temps réel
- Intégration météo pour prévisions
- Rapports financiers avancés
- Recommandations ML
- Cache optimisé
- Gestion de trésorerie
- Budgétisation avancée
- Rapports financiers
- Analyse des coûts
- Projections météo-dépendantes

### 4. Ressources Humaines
- Gestion du personnel
- Système de paie
  - Calcul automatisé des salaires
  - Gestion des cotisations
  - Intégration contrats
  - Validation multi-niveaux
  - Documentation complète
- Gestion des présences
- Gestion des compétences agricoles
- Gestion des contrats
- Évaluation des performances
- Formation et développement

### 5. Gestion des Stocks
- Inventaire en temps réel
- Traçabilité des produits
- Gestion des mouvements
- Alertes de stock
- Optimisation des niveaux
- ML prédictif
- Intégration IoT
- Tests ML

### 6. Paramétrage
- Configuration système
- Gestion des utilisateurs
- Droits d'accès
- Personnalisation
- Maintenance

## Architecture Technique

### Backend
- FastAPI (API REST)
- PostgreSQL (Base de données)
- SQLAlchemy (ORM)
- Alembic (Migrations)
- JWT (Authentification)
- Redis (Cache)
- ML Services
- IoT Integration

### Frontend
- React 18+
- TypeScript
- Material-UI
- Redux
- React Router
- React Query

## Installation

1. Prérequis
```bash
# Python 3.9+
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows

# Node.js 16+
npm install
```

2. Configuration
```bash
# Backend
pip install -r requirements.txt
alembic upgrade head

# Frontend
npm install
npm run dev
```

## Documentation

La documentation complète est organisée comme suit :

### Guides Développeurs
- [Guide d'Installation](docs/guides/installation.md)
- [Guide de Développement](docs/guides/developpement.md)
- [Guide de Typage](docs/guides/typage.md)
- [Gestion des Tâches](docs/guides/task_management.md)

### Documentation API
#### Core
- [Authentification](docs/api/auth.md)
- [Paramétrage](docs/api/parametrage.md)
- [Documents](docs/api/documents.md)
- [Dashboard](docs/api/dashboard.md)
- [Activités](docs/api/activities.md)

#### Production & Inventaire
- [Production](docs/api/production.md)
- [Rapports de Production](docs/api/production_reports.md)
- [Inventaire](docs/api/inventaire.md)
- [IoT Monitoring](docs/api/iot_monitoring.md)
- [Météo](docs/api/weather.md)

#### Finance & Comptabilité
- [Finance](docs/api/finance.md)
- [Comptabilité](docs/api/comptabilite.md)

#### RH & Projets
- [RH](docs/api/hr.md)
- [RH Agricole](docs/api/hr_agricole.md)
- [Contrats](docs/api/contracts.md)
- [Paie](docs/api/payroll.md)
- [Projets](docs/api/projects.md)
- [Tâches](docs/api/tasks.md)

### Documentation Modules
#### Finance & Comptabilité
- [Finance - Vue d'ensemble](docs/modules/finance_index.md)
- [Finance - Partie 1](docs/modules/finance_part1.md)
- [Finance - Partie 2](docs/modules/finance_part2.md)
- [Finance - API](docs/modules/finance_part3_api_endpoints.md)
- [Finance - Modèles](docs/modules/finance_part3_models.md)
- [Finance - Support](docs/modules/finance_part3_support.md)
- [Finance - Évolutions](docs/modules/finance_part3_evolutions.md)
- [Comptabilité - Vue d'ensemble](docs/modules/comptabilite_index.md)
- [Comptabilité - Partie 1](docs/modules/comptabilite_part1.md)
- [Comptabilité - Partie 2](docs/modules/comptabilite_part2.md)
- [Comptabilité - API](docs/modules/comptabilite_part3_api.md)
- [Comptabilité - Mises à jour](docs/modules/comptabilite_updates.md)
- [Intégration Finance-Comptabilité](docs/modules/finance_comptabilite_integration.md)

#### Production & Inventaire
- [Production](docs/modules/production_module.md)
- [Production ML](docs/modules/production_ml.md)
- [Inventaire](docs/modules/inventaire/index.md)
- [Inventaire ML](docs/modules/inventaire/ml/index.md)
  - [Modèles](docs/modules/inventaire/ml/models.md)
  - [Intégrations](docs/modules/inventaire/ml/integrations.md)
  - [Optimisation](docs/modules/inventaire/ml/optimization.md)
  - [Monitoring](docs/modules/inventaire/ml/monitoring.md)
  - [Tests](docs/modules/inventaire/ml/tests.md)

#### RH & Projets
- [RH Agricole](docs/modules/hr_agricole/index.md)
  - [Composants](docs/modules/hr_agricole/composants.md)
  - [Types](docs/modules/hr_agricole/types.md)
  - [Méthodes](docs/modules/hr_agricole/methodes.md)
  - [Exemples](docs/modules/hr_agricole/exemples.md)
- [Contrats RH](docs/modules/hr_contract.md)
- [Projets ML](docs/modules/projects_ml.md)
- [Tests Projets ML](docs/modules/projets_ml_tests_mars2024.md)

### Documentation Technique
- [Plan de Développement](docs/plan_developpement.md)
- [Plan Technique](docs/plan_developpement_technique.md)
- [Développement Futur](docs/developpement_futur.md)

### Diagrammes
- [Vue d'ensemble](docs/diagrammes/README.md)
- [Composants](docs/diagrammes/composants.md)
- [Infrastructure](docs/diagrammes/infrastructure.md)
- [Flux Production](docs/diagrammes/flux_production.md)
- [Flux Projets](docs/diagrammes/flux_projets.md)
- [Schéma Base de Données](docs/diagrammes/db_schema.md)

### Tests
- [Documentation des Tests](docs/tests.md)
- [Vue d'ensemble](docs/tests/README.md)
- [Configuration](docs/tests/guides/configuration.md)
- [React](docs/tests/guides/react.md)
- [Machine Learning](docs/tests/guides/ml.md)
- [ML Inventaire](docs/tests/guides/ml_inventory.md)
- [Tests E2E](docs/tests/guides/e2e.md)
- [Bonnes Pratiques](docs/tests/guides/best_practices.md)
- [Maintenance](docs/tests/guides/maintenance.md)

## Standards de Développement

### Code
- PEP 8 pour Python
- ESLint pour TypeScript
- Tests unitaires (coverage > 80%)
- Documentation des fonctions
- Revue de code
- Architecture modulaire

### Tests
- Architecture modulaire
- Tests spécialisés
- Tests ML dédiés
- Tests intégration
- Tests performance
- Documentation

### Base de Données
- Modèles avec BaseModel
- Timestamps UTC automatiques
- UUIDs pour les IDs
- Migrations versionnées
- Cache Redis optimisé

### Contribution
1. Fork le projet
2. Créer une branche (`git checkout -b feature/nouvelle-fonctionnalite`)
3. Commit (`git commit -m 'Ajout nouvelle fonctionnalité'`)
4. Push (`git push origin feature/nouvelle-fonctionnalite`)
5. Pull Request

## Sécurité
- Authentification JWT
- RBAC (Contrôle d'accès basé sur les rôles)
- Validation des données
- Audit trail
- SSL/TLS
- Chiffrement des données sensibles
- Protection CSRF
- Gestion sécurisée des clés API

## Support

Pour toute question ou assistance :
- Documentation : [docs/](docs/)
- Issues : Utiliser le système d'issues GitHub
- Contact : ivanfodjo@hotmail.com

## Licence

Propriétaire - FOFAL © 2024
