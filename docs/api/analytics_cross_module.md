# API Analytics Cross-Module

Cette API fournit des endpoints pour accéder aux analytics cross-module, permettant d'analyser les corrélations et impacts entre les différents modules de l'ERP.

## Endpoints

### GET /analytics/cross-module/unified

Récupère une vue unifiée des analytics de tous les modules.

**Paramètres**
- `date_debut` (optionnel): Date de début de l'analyse (format: YYYY-MM-DD)
- `date_fin` (optionnel): Date de fin de l'analyse (format: YYYY-MM-DD)

**Réponse**
```json
{
  "timestamp": "2024-03-15T10:00:00",
  "periode": {
    "debut": "2024-02-15",
    "fin": "2024-03-15"
  },
  "modules": {
    "hr": {
      "analytics": {},
      "production_impact": {},
      "finance_impact": {},
      "weather_impact": {}
    },
    "production": {},
    "finance": {},
    "inventory": {},
    "weather": {},
    "projects": {}
  },
  "correlations": {},
  "predictions": {},
  "recommendations": []
}
```

### GET /analytics/cross-module/correlations

Récupère les corrélations entre les différents modules.

**Paramètres**
- `date_debut` (optionnel): Date de début de l'analyse (format: YYYY-MM-DD)
- `date_fin` (optionnel): Date de fin de l'analyse (format: YYYY-MM-DD)

**Réponse**
```json
{
  "hr_production": 0.85,
  "production_finance": 0.75,
  "weather_global": 0.65,
  "inventory_finance": 0.80
}
```

### GET /analytics/cross-module/predictions

Récupère les prédictions ML cross-module.

**Paramètres**
- `date_debut` (optionnel): Date de début de l'analyse (format: YYYY-MM-DD)
- `date_fin` (optionnel): Date de fin de l'analyse (format: YYYY-MM-DD)

**Réponse**
```json
{
  "hr": {
    "predictions": [],
    "confidence": 0.85
  },
  "production": {},
  "finance": {},
  "inventory": {},
  "cross_module": {
    "predictions": [],
    "correlations": {},
    "impacts": {}
  }
}
```

### GET /analytics/cross-module/recommendations

Récupère les recommandations cross-module basées sur ML.

**Paramètres**
- `date_debut` (optionnel): Date de début de l'analyse (format: YYYY-MM-DD)
- `date_fin` (optionnel): Date de fin de l'analyse (format: YYYY-MM-DD)

**Réponse**
```json
[
  {
    "type": "CORRELATION",
    "priority": "HIGH",
    "modules": ["hr", "production"],
    "description": "Forte corrélation hr_production",
    "actions": []
  }
]
```

### GET /analytics/cross-module/hr-impact

Analyse l'impact RH sur les autres modules.

**Paramètres**
- `date_debut` (optionnel): Date de début de l'analyse (format: YYYY-MM-DD)
- `date_fin` (optionnel): Date de fin de l'analyse (format: YYYY-MM-DD)

**Réponse**
```json
{
  "analytics": {},
  "production_impact": {
    "productivity": {},
    "skills_coverage": {},
    "training_impact": {}
  },
  "finance_impact": {
    "labor_costs": {},
    "training_roi": {},
    "productivity_value": {}
  },
  "weather_impact": {}
}
```

### GET /analytics/cross-module/production-impact

Analyse l'impact production sur les autres modules.

**Paramètres**
- `date_debut` (optionnel): Date de début de l'analyse (format: YYYY-MM-DD)
- `date_fin` (optionnel): Date de fin de l'analyse (format: YYYY-MM-DD)

**Réponse**
```json
{
  "analytics": {},
  "hr_impact": {
    "workload": {},
    "skills_required": {},
    "schedule_impact": {}
  },
  "finance_impact": {
    "production_costs": {},
    "revenue_impact": {},
    "efficiency_savings": {}
  },
  "weather_impact": {}
}
```

### GET /analytics/cross-module/finance-impact

Analyse l'impact finance sur les autres modules.

**Paramètres**
- `date_debut` (optionnel): Date de début de l'analyse (format: YYYY-MM-DD)
- `date_fin` (optionnel): Date de fin de l'analyse (format: YYYY-MM-DD)

**Réponse**
```json
{
  "analytics": {},
  "hr_impact": {
    "budget_constraints": {},
    "hiring_capacity": {},
    "training_budget": {}
  },
  "production_impact": {
    "investment_capacity": {},
    "maintenance_budget": {},
    "expansion_potential": {}
  },
  "weather_impact": {}
}
```

### GET /analytics/cross-module/inventory-impact

Analyse l'impact inventaire sur les autres modules.

**Paramètres**
- `date_debut` (optionnel): Date de début de l'analyse (format: YYYY-MM-DD)
- `date_fin` (optionnel): Date de fin de l'analyse (format: YYYY-MM-DD)

**Réponse**
```json
{
  "analytics": {},
  "production_impact": {
    "stock_availability": {},
    "production_constraints": {},
    "quality_impact": {}
  },
  "finance_impact": {
    "storage_costs": {},
    "stock_value": {},
    "turnover_rate": {}
  },
  "weather_impact": {}
}
```

### GET /analytics/cross-module/weather-impact

Analyse l'impact météo sur tous les modules.

**Paramètres**
- `date_debut` (optionnel): Date de début de l'analyse (format: YYYY-MM-DD)
- `date_fin` (optionnel): Date de fin de l'analyse (format: YYYY-MM-DD)

**Réponse**
```json
{
  "current": {},
  "forecast": {},
  "alerts": [],
  "impact": {
    "production": {},
    "hr": {},
    "finance": {},
    "inventory": {}
  }
}
```

### GET /analytics/cross-module/projects-impact

Analyse l'impact des projets sur tous les modules.

**Paramètres**
- `date_debut` (optionnel): Date de début de l'analyse (format: YYYY-MM-DD)
- `date_fin` (optionnel): Date de fin de l'analyse (format: YYYY-MM-DD)

**Réponse**
```json
{
  "active_projects": 10,
  "completion_predictions": {},
  "resource_optimization": {},
  "impact": {
    "hr": {},
    "production": {},
    "finance": {}
  }
}
```

## Codes d'erreur

- `400 Bad Request`: Paramètres invalides
- `401 Unauthorized`: Authentification requise
- `403 Forbidden`: Permissions insuffisantes
- `404 Not Found`: Ressource non trouvée
- `500 Internal Server Error`: Erreur serveur

## Notes

- Les dates sont optionnelles. Par défaut, l'analyse porte sur les 30 derniers jours
- Les données sont mises en cache pendant 15 minutes pour optimiser les performances
- Les prédictions ML sont basées sur les données historiques et les corrélations observées
- Les recommandations sont générées automatiquement en fonction des analyses ML
