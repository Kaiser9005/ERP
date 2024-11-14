# API Rapports de Production

## Vue d'ensemble

Cette API fournit des endpoints pour générer et accéder aux rapports de production intégrés avec les données météorologiques. Les rapports sont mis en cache avec Redis pour optimiser les performances, et le système envoie des notifications automatiques pour les événements importants.

## Endpoints

### GET /api/v1/production-reports/weekly

Génère un rapport hebdomadaire de production intégrant les données météo.

#### Paramètres de requête

- `date` (optionnel): Date de début au format YYYY-MM-DD. Par défaut: date actuelle
- `force_refresh` (optionnel): Force le rafraîchissement du cache. Par défaut: false

#### Cache

Les rapports sont mis en cache pendant 1 heure pour optimiser les performances. Utilisez `force_refresh=true` pour forcer une mise à jour des données.

#### Notifications

Des notifications sont automatiquement envoyées dans les cas suivants :
- Risque météo élevé détecté
- Problèmes de qualité des récoltes
- Événements de production importants

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
            "cloud_cover": 40,
            "cached_at": "2024-01-15T10:30:00Z"
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
                "parcelle_code": "P001",
                "culture_type": "PALMIER",
                "date": "2024-01-16T10:30:00Z",
                "quantite": 100,
                "qualite": "A"
            }
        ],
        "totaux_parcelles": {
            "1": {
                "code": "P001",
                "culture_type": "PALMIER",
                "quantite": 100,
                "qualite_moyenne": 10,
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
    ],
    "generated_at": "2024-01-15T10:30:00Z"
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

### POST /api/v1/production-reports/events

Crée un nouvel événement de production.

#### Corps de la requête

```json
{
    "parcelle_id": "123e4567-e89b-12d3-a456-426614174000",
    "event_type": "RECOLTE",
    "description": "Récolte des palmiers - Zone Nord",
    "metadata": {
        "quantite_kg": 500,
        "qualite": "A",
        "equipe": ["emp001", "emp002"]
    }
}
```

#### Types d'événements disponibles

- `RECOLTE`: Enregistrement d'une récolte
- `PLANTATION`: Nouvelle plantation
- `MAINTENANCE`: Opération de maintenance
- `TRAITEMENT`: Application de traitements
- `IRRIGATION`: Opération d'irrigation

#### Réponse

```json
{
    "status": "success",
    "message": "Événement de production enregistré avec succès",
    "event": {
        "type": "RECOLTE",
        "parcelle_id": "123e4567-e89b-12d3-a456-426614174000",
        "timestamp": "2024-01-15T10:30:00Z"
    }
}
```

## Codes d'erreur

- `400 Bad Request`: Format de date invalide, dates incohérentes ou données d'événement invalides
- `500 Internal Server Error`: Erreur lors de la génération du rapport ou de l'enregistrement de l'événement

## Notes d'utilisation

- Les rapports intègrent automatiquement les données météo actuelles et les prévisions
- Les recommandations sont priorisées (HAUTE, MOYENNE, NORMALE) selon l'impact des conditions météo
- Les statistiques de production sont calculées sur la période spécifiée
- L'analyse d'impact prend en compte les précipitations et les températures
- Les données sont mises en cache pour optimiser les performances
- Des notifications sont envoyées automatiquement pour les événements importants

## Exemples d'utilisation

### Rapport hebdomadaire avec rafraîchissement forcé

```bash
curl -X GET "http://api.example.com/api/v1/production-reports/weekly?date=2024-01-15&force_refresh=true"
```

### Analyse d'impact sur une période

```bash
curl -X GET "http://api.example.com/api/v1/production-reports/impact-meteo?start_date=2024-01-01&end_date=2024-01-15"
```

### Création d'un événement de production

```bash
curl -X POST "http://api.example.com/api/v1/production-reports/events" \
  -H "Content-Type: application/json" \
  -d '{
    "parcelle_id": "123e4567-e89b-12d3-a456-426614174000",
    "event_type": "RECOLTE",
    "description": "Récolte des palmiers - Zone Nord",
    "metadata": {
        "quantite_kg": 500,
        "qualite": "A",
        "equipe": ["emp001", "emp002"]
    }
}'
