# Documentation FOFAL ERP

## Vue d'ensemble

FOFAL ERP est un système de gestion intégré pour l'exploitation agricole FOFAL, spécialisée dans la culture du palmier à huile et des papayes.

## Documentation Technique

### Diagrammes Techniques
- [Vue d'ensemble des Composants](diagrammes/composants.md)
- [Flux du Module Production](diagrammes/flux_production.md)
- [Schéma de Base de Données](diagrammes/db_schema.md)
- [Architecture d'Infrastructure](diagrammes/infrastructure.md)

### Guides
- [Guide d'Installation](guides/installation.md)
- [Guide de Développement](guides/developpement.md)

### Documentation API
- [Module Production](api/production.md)
- [Module Inventaire](api/inventaire.md)
- [Module Finance](api/finance.md)
- [Module RH](api/hr.md)
- [Paramétrage](api/parametrage.md)
- [Documents](api/documents.md)
- [Dashboard](api/dashboard.md)
- [Météo](api/weather.md)

## Architecture Technique

### Backend
- FastAPI (API REST)
- PostgreSQL (Base de données)
- SQLAlchemy (ORM)
- Alembic (Migrations)
- Pydantic (Validation des données)

### Frontend
- React avec TypeScript
- Material-UI
- Redux pour la gestion d'état
- React Router pour la navigation

## Modules Principaux

### 1. Production
- Gestion des parcelles
- Cycles de culture
- Suivi des récoltes
- Monitoring météorologique
  - Dashboard météo en temps réel
  - Affichage des conditions actuelles (température, humidité, précipitations)
  - Prévisions météorologiques sur 3 jours
  - Système d'alertes météo intelligent
  - Recommandations agricoles basées sur les conditions
  - Mise à jour automatique toutes les 30 minutes
  - Métriques agricoles personnalisées
  - Analyse des risques (précipitations, température)
- Contrôle qualité

### 2. Inventaire
- Gestion des stocks
- Mouvements de stock
- Traçabilité
- Alertes de stock
- Rapports d'inventaire

### 3. Finance
- Comptabilité générale
- Gestion de trésorerie
- Budgétisation
- Rapports financiers
- Analyses des coûts

### 4. Ressources Humaines
- Gestion des employés
- Système de paie
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
  - Seuils d'alerte personnalisables

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

---

Pour plus d'informations sur l'architecture technique et les diagrammes détaillés, consultez le [dossier diagrammes](diagrammes/README.md).
