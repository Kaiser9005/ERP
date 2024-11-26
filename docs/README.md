# Documentation FOFAL ERP

## Vue d'ensemble

FOFAL ERP est un système de gestion intégré pour l'exploitation agricole FOFAL, spécialisée dans la culture du palmier à huile et des papayes.

## Documentation Technique

### Plans et Évolutions
- [Plan de Développement](plan_developpement.md)
- [Plan de Développement Technique](plan_developpement_technique.md)
- [Développement Futur](developpement_futur.md)

### Diagrammes Techniques
- [Vue d'ensemble des Composants](diagrammes/composants.md)
- [Flux du Module Production](diagrammes/flux_production.md)
- [Flux des Projets](diagrammes/flux_projets.md)
- [Schéma de Base de Données](diagrammes/db_schema.md)
- [Architecture d'Infrastructure](diagrammes/infrastructure.md)

### Documentation API
- [Module Production](api/production.md)
- [Rapports de Production](api/production_reports.md)
- [Module Inventaire](api/inventaire.md)
- [Module Finance](api/finance.md)
- [Module Comptabilité](api/comptabilite.md)
- [Module RH](api/hr.md)
- [RH Agricole](api/hr_agricole.md)
- [Module Contrats](api/contracts.md)
- [Module Paie](api/payroll.md)
- [Module Projets](api/projects.md)
- [Gestion des Tâches](api/tasks.md)
- [IoT Monitoring](api/iot_monitoring.md)
- [Paramétrage](api/parametrage.md)
- [Documents](api/documents.md)
- [Dashboard](api/dashboard.md)
- [Météo](api/weather.md)
- [Authentification](api/auth.md)
- [Activités](api/activities.md)

### Documentation des Modules
#### Finance et Comptabilité
- [Finance - Vue d'ensemble](modules/finance_index.md)
- [Finance - Partie 1](modules/finance_part1.md)
- [Finance - Partie 2](modules/finance_part2.md)
- [Finance - API Endpoints](modules/finance_part3_api_endpoints.md)
- [Finance - Modèles](modules/finance_part3_models.md)
- [Finance - Support](modules/finance_part3_support.md)
- [Finance - Évolutions](modules/finance_part3_evolutions.md)
- [Comptabilité - Vue d'ensemble](modules/comptabilite_index.md)
- [Comptabilité - Partie 1](modules/comptabilite_part1.md)
- [Comptabilité - Partie 2](modules/comptabilite_part2.md)
- [Comptabilité - API](modules/comptabilite_part3_api.md)
- [Comptabilité - Mises à jour](modules/comptabilite_updates.md)
- [Intégration Finance-Comptabilité](modules/finance_comptabilite_integration.md)

#### Production et Inventaire
- [Production](modules/production.md)
- [Production ML](modules/production_ml.md)
- [Production Module](modules/production_module.md)
- [Inventaire](modules/inventaire/index.md)
- [Inventaire ML](modules/inventaire/ml/index.md)
  - [Modèles ML](modules/inventaire/ml/models.md)
  - [Intégrations](modules/inventaire/ml/integrations.md)
  - [Optimisation](modules/inventaire/ml/optimization.md)
  - [Monitoring](modules/inventaire/ml/monitoring.md)
  - [Tests](modules/inventaire/ml/tests.md)

#### RH et Projets
- [RH Agricole](modules/hr_agricole/index.md)
  - [Composants](modules/hr_agricole/composants.md)
  - [Types](modules/hr_agricole/types.md)
  - [Méthodes](modules/hr_agricole/methodes.md)
  - [Exemples](modules/hr_agricole/exemples.md)
- [Contrats RH](modules/hr_contract.md)
- [Projets ML](modules/projects_ml.md)
- [Tests Projets ML](modules/projets_ml_tests_mars2024.md)

### Guides
- [Guide d'Installation](guides/installation.md)
- [Guide de Développement](guides/developpement.md)
- [Guide de Typage](guides/typage.md)
- [Gestion des Tâches](guides/task_management.md)

### Tests
- [Documentation des Tests](tests.md)
- [Vue d'ensemble](tests/README.md)
#### Guides de Tests
- [Configuration](tests/guides/configuration.md)
- [React](tests/guides/react.md)
- [Machine Learning](tests/guides/ml.md)
- [ML Inventaire](tests/guides/ml_inventory.md)
- [Tests E2E](tests/guides/e2e.md)
- [Bonnes Pratiques](tests/guides/best_practices.md)
- [Maintenance](tests/guides/maintenance.md)

## Architecture Technique

### Backend
- FastAPI (API REST)
- PostgreSQL (Base de données)
- SQLAlchemy (ORM)
- Alembic (Migrations)
- Pydantic (Validation des données)
- Redis (Cache)
- ML Services
- IoT Integration

### Frontend
- React avec TypeScript
- Material-UI
- Redux pour la gestion d'état
- React Router pour la navigation
- React Query

## Modules Principaux

### 1. Production (100%)
- Gestion des parcelles
- Cycles de culture
- Suivi des récoltes
- Monitoring météorologique
  - Dashboard météo en temps réel
  - Affichage des conditions actuelles
  - Prévisions météorologiques
  - Système d'alertes intelligent
  - Recommandations agricoles
  - Métriques personnalisées
  - Analyse des risques
- Contrôle qualité
- ML prédictif
- IoT monitoring

### 2. Inventaire (100%)
- Gestion des stocks
- Mouvements de stock
- Traçabilité
- Alertes de stock
- Rapports d'inventaire
- ML prédictif
- Intégration IoT
- Tests ML

### 3. Finance (95%)
- Comptabilité générale
- Gestion de trésorerie
- Budgétisation
- Rapports financiers
- Analyses des coûts
- Analytics ML
- Cache Redis optimisé

### 4. Ressources Humaines (45%)
- Gestion des employés
- Gestion des contrats
  - Création et suivi des contrats
  - Gestion des modifications
  - Alertes d'expiration
  - Statistiques
- Système de paie (Backend complété)
  - Modèle de données ✓
  - Service métier avec calculs ✓
  - API REST complète ✓
  - Tests unitaires et intégration ✓
  - Documentation API ✓
  - Interface utilisateur (En cours)
- Présences et congés
- Évaluations
- Formation

### 5. Paramétrage
- Configuration système
- Gestion des modules
- Droits d'accès
- Personnalisation
- Configuration des services externes
  - API météo
  - Paramètres de localisation
  - Seuils d'alerte

## Sécurité
- Authentification JWT
- Contrôle d'accès RBAC
- Validation des données
- Audit trail
- Chiffrement des données sensibles
- Sécurisation des clés API

## Déploiement
- Configuration des environnements
- Gestion des dépendances
- Scripts de déploiement
- Monitoring et logs
- Variables d'environnement sécurisées
- Intégration continue (CI/CD)

## Contribution

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/nouvelle-fonctionnalite`)
3. Commiter les changements (`git commit -m 'Ajout nouvelle fonctionnalité'`)
4. Pousser vers la branche (`git push origin feature/nouvelle-fonctionnalite`)
5. Créer une Pull Request

## Standards de Développement
- Code style: PEP 8 pour Python, ESLint pour TypeScript
- Tests unitaires obligatoires
- Documentation des fonctions et API
- Revue de code systématique
- Gestion sécurisée des secrets
- Tests d'intégration pour les services externes

## Licence

Propriétaire - FOFAL © 2024
