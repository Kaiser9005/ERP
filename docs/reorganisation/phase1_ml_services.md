# Plan de Réorganisation - Phase 1 : Services ML

## Situation Actuelle

### Services ML Dispersés
1. Dans services/ml/tableau_bord/ :
- alertes.py
- predictions.py
- unification.py

2. Dans services/inventory_ml/ :
- base.py
- optimization.py
- analysis.py
- quality.py
- config.py

3. Dans services/projects_ml/ :
- base.py
- optimization.py
- analysis.py
- weather.py

4. Dans services/finance_comptabilite/ (composants ML) :
- analyse.py (contient _analyze_with_ml, _prepare_ml_features, etc.)
- couts.py (contient analyse ML)
- iot.py (contient analyse ML)
- cloture.py (contient analyse ML)

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
├── inventory/
│   ├── __init__.py
│   ├── base.py
│   ├── optimization.py
│   ├── analysis.py
│   └── quality.py
├── projects/
│   ├── __init__.py
│   ├── base.py
│   ├── optimization.py
│   ├── analysis.py
│   └── weather.py
├── finance/
│   ├── __init__.py
│   ├── analysis.py
│   ├── costs.py
│   ├── iot.py
│   └── closure.py
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

### 3. Migration des Services
1. Inventory ML :
   - Déplacer les fichiers vers services/ml/inventory/
   - Adapter les imports
   - Implémenter les interfaces communes

2. Projects ML :
   - Déplacer les fichiers vers services/ml/projects/
   - Adapter les imports
   - Implémenter les interfaces communes

3. Finance ML :
   - Extraire la logique ML de finance_comptabilite/
   - Créer des services dédiés dans services/ml/finance/
   - Adapter les imports

4. Dashboard ML :
   - Déplacer les fichiers de tableau_bord/ vers services/ml/dashboard/
   - Adapter les imports
   - Implémenter les interfaces communes

### 4. Mise à Jour des Tests
1. Réorganiser les tests ML :
```
tests/ml/
├── core/
├── inventory/
├── projects/
├── finance/
└── dashboard/
```

2. Adapter les imports dans les tests
3. Vérifier la couverture de tests
4. Ajouter des tests d'intégration entre modules ML

## Étapes d'Implémentation

1. Préparation :
   - Créer la nouvelle structure de dossiers
   - Définir les interfaces communes
   - Préparer la configuration centralisée

2. Migration par Module :
   - Commencer par inventory_ml (le plus autonome)
   - Suivre avec projects_ml
   - Extraire et migrer finance_ml
   - Terminer par dashboard_ml

3. Tests et Validation :
   - Migrer les tests correspondants
   - Vérifier que tous les tests passent
   - Tester les intégrations entre modules

4. Documentation :
   - Mettre à jour la documentation API
   - Documenter les interfaces communes
   - Documenter les patterns d'utilisation

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
