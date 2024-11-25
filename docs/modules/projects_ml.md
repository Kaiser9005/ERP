# Module ML Projets

## Vue d'Ensemble

Le module ML des projets ajoute des capacités prédictives et d'optimisation au module projets existant. Il utilise:

1. Données historiques des projets
2. Données météorologiques
3. Données IoT
4. Métriques de performance

## Fonctionnalités

### 1. Prédiction de Succès

```python
prediction = await ml_service.predict_project_success(
    project_id="P001",
    current_date=date(2024, 1, 1)
)
```

Retourne:
```json
{
    "success_probability": 0.85,
    "risk_factors": [
        {
            "factor": "Ressources",
            "impact": 0.3,
            "description": "Allocation sous-optimale"
        }
    ],
    "recommendations": [
        {
            "type": "RESOURCE",
            "priority": "HIGH",
            "description": "Optimiser l'allocation",
            "actions": [
                "Revoir la planification",
                "Identifier goulots"
            ]
        }
    ]
}
```

### 2. Optimisation Ressources

```python
allocation = await ml_service.optimize_resource_allocation(
    project_id="P001",
    start_date=date(2024, 1, 1),
    end_date=date(2024, 12, 31)
)
```

Retourne:
```json
{
    "optimal_allocation": [
        {
            "task_id": "T1",
            "resources": ["R1", "R2"],
            "start_date": "2024-01-01",
            "end_date": "2024-01-07"
        }
    ],
    "efficiency_score": 0.85,
    "bottlenecks": [
        {
            "resource": "R1",
            "period": "2024-02",
            "utilization": 0.95
        }
    ],
    "recommendations": [
        "Répartir la charge de R1",
        "Ajouter des ressources en février"
    ]
}
```

### 3. Analyse Performance

```python
performance = await ml_service.analyze_project_performance(
    project_id="P001",
    start_date=date(2024, 1, 1),
    end_date=date(2024, 12, 31)
)
```

Retourne:
```json
{
    "kpis": {
        "schedule_performance": 0.85,
        "cost_performance": 0.92,
        "resource_efficiency": 0.78,
        "quality_score": 0.88,
        "risk_score": 0.25
    },
    "trends": {
        "velocity": {
            "current": 8.5,
            "trend": "increasing",
            "forecast": 9.2
        },
        "completion_rate": {
            "current": 0.82,
            "trend": "stable",
            "forecast": 0.85
        }
    },
    "predictions": {
        "completion_date": "2024-03-15",
        "final_cost": 150000,
        "quality_forecast": 0.90
    }
}
```

### 4. Impact Météo

```python
impact = await ml_service.predict_weather_impact(
    project_id="P001",
    start_date=date(2024, 1, 1),
    end_date=date(2024, 12, 31)
)
```

Retourne:
```json
{
    "impact_score": 0.7,
    "affected_tasks": [
        {
            "task_id": "T1",
            "impact": "HIGH",
            "conditions": ["RAIN", "WIND"]
        }
    ],
    "risk_periods": [
        {
            "period": "2024-02",
            "risk": "HIGH",
            "conditions": ["FROST"]
        }
    ],
    "alternatives": [
        {
            "task_id": "T1",
            "original_date": "2024-02-01",
            "alternative_date": "2024-02-15",
            "reason": "Éviter période gel"
        }
    ]
}
```

## Tests

Le module ML est couvert par plusieurs niveaux de tests:

### 1. Tests Unitaires
```bash
# Exécution des tests unitaires
pytest tests/test_projects_ml_service.py
```

Les tests unitaires couvrent:
- Prédiction de succès
- Optimisation des ressources
- Analyse de performance
- Impact météo
- Calcul des features
- Génération des recommandations

### 2. Tests d'Intégration
```bash
# Exécution des tests d'intégration
pytest tests/integration/test_projects_ml_integration.py
```

Les tests d'intégration vérifient:
- Intégration avec le service météo
- Intégration avec le service IoT
- Intégration avec le cache Redis
- Gestion des erreurs
- Timeouts et résilience
- Performance et charge
- Accès concurrents
- Cohérence des données

### 3. Gestion des Erreurs

Le service gère plusieurs types d'erreurs:
- Erreurs de service (météo, IoT)
- Erreurs de cache
- Timeouts
- Données invalides
- Erreurs de validation ML

Exemple de gestion d'erreur:
```python
try:
    impact = await ml_service.predict_weather_impact(
        project_id="P001",
        start_date=date.today(),
        end_date=date.today() + timedelta(days=7)
    )
except Exception as e:
    # Valeurs par défaut en cas d'erreur
    impact = {
        "impact_score": 0.5,
        "affected_tasks": [],
        "risk_periods": [],
        "alternatives": [],
        "error_handled": str(e)
    }
```

### 4. Performance

Le service est optimisé pour:
- Temps de réponse < 1s
- Support de charge élevée
- Utilisation efficace du cache
- Gestion de la mémoire
- Accès concurrents

## Intégration

Le service ML est intégré au service projets principal via plusieurs points:

1. Détails Projet
```python
details = await project_service.get_project_details(
    project_id="P001",
    include_analytics=True  # Active les analytics ML
)
```

2. Création Projet
```python
project = await project_service.create_project(
    project_data=data,
    optimize_resources=True  # Active l'optimisation ML
)
```

3. Mise à Jour Projet
```python
updated = await project_service.update_project(
    project_id="P001",
    project_data=data,
    reoptimize=True  # Active la ré-optimisation ML
)
```

4. Analytics Projet
```python
analytics = await project_service.get_project_analytics(
    project_id="P001",
    start_date=date(2024, 1, 1),
    end_date=date(2024, 12, 31)
)
```

## Architecture

Le module ML utilise une architecture en couches:

1. Collecte Données
- Historique projets
- Données météo
- Données IoT
- Métriques performance

2. Préparation Features
- Calcul métriques
- Normalisation
- Agrégation temporelle
- Extraction caractéristiques

3. Modèles Prédictifs
- Prédiction succès
- Optimisation ressources
- Impact météo
- Prévisions performance

4. Génération Recommandations
- Analyse impacts
- Identification risques
- Actions correctives
- Optimisations suggérées

## Bonnes Pratiques

1. Cache
- Utiliser le cache pour les calculs fréquents
- Invalider le cache lors des mises à jour
- Cache paramétrable par type de donnée

2. Performance
- Calculs asynchrones
- Optimisation requêtes
- Agrégation données
- Mise en cache résultats

3. Maintenance
- Logs détaillés
- Métriques performance
- Alertes erreurs
- Documentation à jour

4. Évolution
- Tests complets
- Versioning modèles
- Métriques qualité
- Feedback utilisateurs

## Prochaines Étapes

1. Modèles ML
- Implémentation modèles prédictifs
- Entraînement sur données historiques
- Validation performances
- Optimisation hyperparamètres

2. Intégrations
- Dashboard ML dédié
- Alertes intelligentes
- Rapports prédictifs
- Export données

3. Optimisations
- Performance calculs
- Précision prédictions
- Utilisation cache
- Scalabilité système

4. Documentation
- Guide utilisateur
- Documentation technique
- Exemples d'utilisation
- Bonnes pratiques
