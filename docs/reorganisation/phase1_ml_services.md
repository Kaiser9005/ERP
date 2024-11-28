# Plan de Réorganisation - Phase 1 : Services ML

## Situation Actuelle

### Services ML Réorganisés

1. Module Projets ML ✅
   - Services migrés vers services/ml/projets/
   - Tests migrés vers tests/ml/projets/
   - Structure validée et cohérente avec core/
   - Tests de non-régression passés

2. Module Inventaire ML ✅
   - Services migrés vers services/ml/inventaire/
   - Tests migrés vers tests/ml/inventaire/
   - Structure validée et cohérente avec core/
   - Tests de non-régression passés

3. Module Finance/Comptabilité ML ✅
   - Tests migrés vers tests/ml/finance_comptabilite/
   - Structure validée et cohérente avec core/
   - Tests de non-régression passés
   - Documentation mise à jour

### Services ML à Réorganiser

1. Module Production ML
   - Déplacer services/production_ml_service.py vers services/ml/production/
   - Créer la structure modulaire (base.py, analysis.py, etc.)
   - Migrer les tests vers tests/ml/production/
   - Valider l'intégration avec core/

2. Module Tableau de Bord ML
   - Réorganiser services/ml/tableau_bord/
   - Migrer les tests correspondants
   - Standardiser l'architecture

## Plan d'Action

### 1. Centralisation des Services ML
Créer une nouvelle structure dans services/ml/ :

```
services/ml/
├── core/
│   ├── __init__.py
│   ├── base.py (classes de base communes)
│   ├── config.py (configuration centralisée)
│   └── types.py (types communs)
├── inventory/ ✅
│   ├── __init__.py
│   ├── base.py
│   ├── optimization.py
│   ├── analysis.py
│   └── quality.py
├── projects/ ✅
│   ├── __init__.py
│   ├── base.py
│   ├── optimization.py
│   ├── analysis.py
│   └── weather.py
├── finance/ ✅
│   ├── __init__.py
│   ├── analysis.py
│   ├── costs.py
│   ├── iot.py
│   └── closure.py
├── production/
│   ├── __init__.py
│   ├── base.py
│   ├── analysis.py
│   ├── optimization.py
│   └── quality.py
└── dashboard/
    ├── __init__.py
    ├── alerts.py
    ├── predictions.py
    └── unification.py
```

### 2. Standardisation des Interfaces
1. Créer des interfaces communes dans core/base.py :
   - MLModel (classe de base)
   - MLOptimizer (interface d'optimisation)
   - MLAnalyzer (interface d'analyse)
   - MLPredictor (interface de prédiction)

2. Standardiser les configurations :
   - Centraliser la config ML dans core/config.py
   - Utiliser des paramètres cohérents

### 3. Migration des Services Restants

1. Production ML :
   - Créer la structure dans services/ml/production/
   - Migrer le code existant
   - Adapter les imports
   - Implémenter les interfaces communes

2. Dashboard ML :
   - Réorganiser services/ml/tableau_bord/
   - Standardiser l'architecture
   - Adapter les imports
   - Implémenter les interfaces communes

### 4. Mise à Jour des Tests
1. Structure des tests ML :
```
tests/ml/
├── core/ ✅
├── inventory/ ✅
├── projects/ ✅
├── finance_comptabilite/ ✅
├── production/
└── dashboard/
```

2. Adapter les imports dans les tests
3. Vérifier la couverture de tests
4. Ajouter des tests d'intégration entre modules ML

## Validation Finale

1. Vérifier que tous les services ML sont dans services/ml/
2. Confirmer que les interfaces sont cohérentes
3. Valider que tous les tests passent
4. Vérifier les intégrations entre modules
5. Documenter les changements effectués

## Impact sur les Autres Services

1. Mettre à jour les imports dans :
   - services/inventory_service.py
   - services/project_service.py
   - services/finance_service.py
   - services/dashboard_unified_service.py

2. Adapter les services qui utilisent directement les fonctionnalités ML

3. Vérifier les dépendances circulaires potentielles
