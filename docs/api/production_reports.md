# API Rapports de Production

## Vue d'ensemble

Cette API fournit des endpoints pour générer et accéder aux rapports de production intégrés avec les données météorologiques.

## Endpoints

### GET /api/v1/production-reports/weekly

Génère un rapport hebdomadaire de production intégrant les données météo.

#### Paramètres de requête

- `date` (optionnel): Date de début au format YYYY-MM-DD. Par défaut: date actuelle

#### Réponse

```json
{
    "periode": {
        "debut": "2024-01-15T00:00:00",
        "fin": "2024-01-22T00:00:00"
    },
    "meteo": {
        "conditions": {
            "temperature": 28.5,
            "humidity": 75,
            "precipitation": 0.5,
            "wind_speed": 12,
            "conditions": "Partiellement nuageux",
            "uv_index": 6,
            "cloud_cover": 40
        },
        "risques": {
            "precipitation": {
                "level": "LOW",
                "message": "Conditions de précipitation normales"
            },
            "temperature": {
                "level": "MEDIUM",
                "message": "Températures élevées - Surveillance recommandée"
            },
            "level": "MEDIUM"
        },
        "impact": {
            "niveau": "MOYEN",
            "facteurs": [
                {
                    "facteur": "Températures modérées",
                    "impact": "Possible stress des cultures sensibles",
                    "recommandation": "Surveiller l'hydratation"
                }
            ]
        }
    },
    "production": {
        "recoltes": [
            {
                "id": 1,
                "parcelle_id": 1,
                "date": "2024-01-16T10:30:00",
                "quantite": 100,
                "qualite": 8
            }
        ],
        "totaux_parcelles": {
            "1": {
                "quantite": 100,
                "qualite_moyenne": 8,
                "nombre_recoltes": 1
            }
        },
        "total_global": 100
    },
    "recommandations": [
        {
            "type": "METEO",
            "priorite": "MOYENNE",
            "description": "Surveiller l'hydratation des plants",
            "details": "En raison de : Températures modérées - Possible stress des cultures sensibles"
        },
        {
            "type": "PRODUCTION",
            "priorite": "NORMALE",
            "description": "Conditions favorables pour les activités agricoles",
            "details": "Maintenir les pratiques actuelles"
        }
    ]
}
```

### GET /api/v1/production-reports/impact-meteo

Analyse l'impact des conditions météo sur la production pour une période donnée.

#### Paramètres de requête

- `start_date` (requis): Date de début au format YYYY-MM-DD
- `end_date` (requis): Date de fin au format YYYY-MM-DD

#### Réponse

```json
{
    "periode": {
        "debut": "2024-01-01",
        "fin": "2024-01-15"
    },
    "analyse_impact": {
        "niveau": "ÉLEVÉ",
        "facteurs": [
            {
                "facteur": "Précipitations excessives",
                "impact": "Risque d'inondation et de perte de récoltes",
                "recommandation": "Renforcer le drainage des parcelles"
            }
        ]
    },
    "recommandations": [
        {
            "type": "METEO",
            "priorite": "HAUTE",
            "description": "Renforcer le drainage des parcelles",
            "details": "En raison de : Précipitations excessives - Risque d'inondation"
        }
    ],
    "statistiques_production": {
        "total_recoltes": 10,
        "total_quantite": 1500,
        "parcelles_impactees": 3
    }
}
```

## Codes d'erreur

- `400 Bad Request`: Format de date invalide ou dates incohérentes
- `500 Internal Server Error`: Erreur lors de la génération du rapport

## Notes d'utilisation

- Les rapports intègrent automatiquement les données météo actuelles et les prévisions
- Les recommandations sont priorisées (HAUTE, MOYENNE, NORMALE) selon l'impact des conditions météo
- Les statistiques de production sont calculées sur la période spécifiée
- L'analyse d'impact prend en compte les précipitations et les températures

## Exemples d'utilisation

### Rapport hebdomadaire à partir d'une date spécifique

```bash
curl -X GET "http://api.example.com/api/v1/production-reports/weekly?date=2024-01-15"
```

### Analyse d'impact sur une période

```bash
curl -X GET "http://api.example.com/api/v1/production-reports/impact-meteo?start_date=2024-01-01&end_date=2024-01-15"
