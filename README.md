# FOFAL ERP 2024 - Système de Gestion Agricole Intégré

## Vue d'ensemble

FOFAL ERP est un système de gestion intégré spécialement conçu pour FOFAL (Family Land), une entreprise agricole spécialisée dans la culture du palmier à huile (70 ha) et des papayes (10 ha).

## État du Projet

Le projet est en développement actif avec plusieurs modules à différents stades d'avancement :
- Production (95%) : 
  - Gestion complète des parcelles et cycles de culture
  - Dashboard météo en temps réel
  - Système d'alertes intelligent
  - Rapports de production avancés
  - Tests End-to-End et unitaires
- Gestion des Projets (85%) : 
  - Système de tâches complet
  - Intégration des données météo
  - Gestion des ressources
  - Tests d'intégration
  - Documentation utilisateur
- Finance (60%) : 
  - Gestion budgétaire avancée
  - Analyse d'impact météo
  - Projections financières
  - Tests unitaires complets
  - Documentation API
  - Gestion des pièces jointes  

  - Comptabilité (75%) :
  - Gestion complète des comptes et écritures
  - Dashboard financier avancé
  - Analyse budgétaire avec impact météo
  - Suivi de trésorerie en temps réel
  - Rapports comptables intelligents
  - Tests unitaires backend
  - Documentation API complète
  - Cache Redis optimisé
  - Intégration météo pour prévisions
- RH (25%) : 
  - Gestion basique des employés
  - Structure des présences
- Inventaire (35%) : 
  - Modèles de stocks
  - Mouvements de base

Pour plus de détails sur l'état actuel et les prochaines étapes, consultez notre [Plan de Développement](docs/plan_developpement.md).

## Modules Principaux

### 1. Production Agricole
- Gestion des parcelles
- Suivi des cycles de culture
- Monitoring météorologique
- Contrôle qualité des récoltes
- Planification agricole

### 2. Gestion des Projets
- Planification des activités
- Suivi des tâches
- Gestion des ressources
- Rapports d'avancement
- Calendrier des projets

### 3. Comptabilité et Finance
- Comptabilité générale complète
- Dashboard financier interactif
- Analyse budgétaire intelligente
- Suivi de trésorerie en temps réel
- Intégration météo pour prévisions
- Rapports financiers avancés
- Recommandations contextuelles
- Cache optimisé pour performances
- Gestion de trésorerie
- Budgétisation avancée
- Rapports financiers
- Analyse des coûts
- Projections météo-dépendantes

### 4. Ressources Humaines
- Gestion du personnel
- Système de paie
- Gestion des présences
- Évaluation des performances
- Formation et développement

### 5. Gestion des Stocks
- Inventaire en temps réel
- Traçabilité des produits
- Gestion des mouvements
- Alertes de stock
- Optimisation des niveaux

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

La documentation complète est disponible dans le dossier [docs](docs/README.md) :
- [Guide d'Installation](docs/guides/installation.md)
- [Guide de Développement](docs/guides/developpement.md)
- [Documentation API](docs/api/)
  - [API Comptabilité](docs/api/comptabilite.md)
- [Diagrammes Techniques](docs/diagrammes/)
- [Plan de Développement](docs/plan_developpement.md)
- [Mises à jour Comptabilité](docs/modules/comptabilite_updates.md)

## Standards de Développement

### Code
- PEP 8 pour Python
- ESLint pour TypeScript
- Tests unitaires (coverage > 80%)
- Documentation des fonctions
- Revue de code

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
