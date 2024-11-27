# Plan de Migration Architecture FOFAL ERP

## 1. Principes Directeurs

### Langue et Internationalisation
- Interface utilisateur : 100% en français
- Documentation utilisateur : 100% en français
- Code source : 
  * Structure technique : anglais (ex: src/, components/, services/)
  * Noms des modules métier : français (ex: comptabilite/, inventaire/)
  * Contenu et logique métier : français
  * Commentaires : français

## 2. Réorganisation des Services ML

### Structure Actuelle
```
services/
├── analytics_cross_module_service.py
├── dashboard_unified_service.py
├── finance_comptabilite/
│   ├── analyse.py
│   ├── couts.py
│   ├── meteo.py
│   └── iot.py
├── hr_analytics_service.py
├── inventory_ml_service.py
├── production_ml_service.py
└── projects_ml_service.py
```

### Nouvelle Structure
```
services/
└── ml/
    ├── tableau_bord/
    │   ├── __init__.py
    │   ├── unification.py
    │   ├── predictions.py
    │   └── alertes.py
    ├── analytique/
    │   ├── __init__.py
    │   ├── correlations.py
    │   ├── predictions.py
    │   └── recommandations.py
    ├── comptabilite/
    │   ├── __init__.py
    │   ├── prediction.py
    │   ├── analyse_couts.py
    │   ├── previsions.py
    │   └── optimisation.py
    ├── rh/
    │   ├── __init__.py
    │   ├── prediction.py
    │   ├── analyse_competences.py
    │   ├── formation.py
    │   └── planification.py
    ├── inventaire/
    │   ├── __init__.py
    │   ├── prediction.py
    │   ├── optimisation.py
    │   └── qualite.py
    ├── production/
    │   ├── __init__.py
    │   ├── prediction.py
    │   ├── meteo.py
    │   └── rendement.py
    └── projets/
        ├── __init__.py
        ├── prediction.py
        ├── ressources.py
        └── planification.py
```

## 3. Migration des Services ML

### Tableau de Bord Unifié
| Source | Destination |
|--------|-------------|
| dashboard_unified_service.py | ml/tableau_bord/unification.py |
| (nouveau) | ml/tableau_bord/predictions.py |
| (nouveau) | ml/tableau_bord/alertes.py |

### Analytics Cross-Module
| Source | Destination |
|--------|-------------|
| analytics_cross_module_service.py | ml/analytique/correlations.py |
| (nouveau) | ml/analytique/predictions.py |
| (nouveau) | ml/analytique/recommandations.py |

### Comptabilité
| Source | Destination |
|--------|-------------|
| finance_comptabilite/analyse.py | ml/comptabilite/analyse_couts.py |
| finance_comptabilite/couts.py | ml/comptabilite/prediction.py |
| finance_comptabilite/meteo.py | ml/comptabilite/previsions.py |
| finance_comptabilite/iot.py | ml/comptabilite/optimisation.py |

### Ressources Humaines
| Source | Destination |
|--------|-------------|
| hr_analytics_service.py | ml/rh/prediction.py |
| hr_formation_service.py | ml/rh/formation.py |
| (nouveau) | ml/rh/analyse_competences.py |
| (nouveau) | ml/rh/planification.py |

### Inventaire
| Source | Destination |
|--------|-------------|
| inventory_ml_service.py | ml/inventaire/prediction.py |
| inventory_ml/optimization.py | ml/inventaire/optimisation.py |
| inventory_ml/quality.py | ml/inventaire/qualite.py |

### Production
| Source | Destination |
|--------|-------------|
| production_ml_service.py | ml/production/prediction.py |
| production_ml/weather.py | ml/production/meteo.py |
| production_ml/optimization.py | ml/production/rendement.py |

### Projets
| Source | Destination |
|--------|-------------|
| projects_ml_service.py | ml/projets/prediction.py |
| projects_ml/optimization.py | ml/projets/ressources.py |
| projects_ml/analysis.py | ml/projets/planification.py |

## 4. Plan d'Exécution

### Phase 1 : Préparation
1. Sauvegarde complète du projet
2. Création de la nouvelle structure de dossiers
3. Documentation de l'existant

### Phase 2 : Migration
1. Migration module par module :
   - Tableau de Bord (prioritaire car dépendant des autres)
   - Analytics Cross-Module
   - Comptabilité
   - RH
   - Inventaire
   - Production
   - Projets

2. Pour chaque module :
   - Migration du code
   - Adaptation des imports
   - Tests unitaires
   - Tests d'intégration

### Phase 3 : Validation
1. Tests complets
2. Vérification des performances
3. Documentation mise à jour

## 5. Points d'Attention

### Dépendances
- Mise à jour des imports dans tous les services
- Gestion des dépendances circulaires
- Maintien des interfaces existantes

### Tests
- Migration des tests existants
- Ajout de nouveaux tests
- Validation des performances

### Documentation
- Mise à jour de la documentation technique
- Documentation des nouveaux composants ML
- Guide de maintenance

## 6. Timeline Estimée

### Semaine 1
- Migration Tableau de Bord et Analytics
- Migration Comptabilité et RH
- Tests initiaux

### Semaine 2
- Migration Production et Inventaire
- Tests d'intégration

### Semaine 3
- Migration Projets
- Tests complets
- Documentation

## 7. Validation Finale

### Critères de Succès
- Tous les tests passent
- Performance maintenue ou améliorée
- Documentation complète et à jour
- Interface utilisateur 100% en français
- Pas de régression fonctionnelle
