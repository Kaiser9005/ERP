# API Monitoring IoT

## Vue d'ensemble

L'API de monitoring IoT permet de surveiller et gérer les capteurs IoT déployés sur les parcelles. Elle fournit des fonctionnalités pour :

- Récupérer les données de monitoring en temps réel
- Consulter le dashboard de monitoring
- Gérer les alertes et la maintenance
- Configurer le système de monitoring

## Endpoints

### Monitoring Parcelle

```http
GET /api/v1/iot-monitoring/parcelles/{parcelle_id}
```

Récupère les données de monitoring pour une parcelle spécifique.

#### Paramètres

| Nom | Type | Description |
|-----|------|-------------|
| parcelle_id | UUID | ID de la parcelle |
| start_date | DateTime | Date de début (optionnel) |
| end_date | DateTime | Date de fin (optionnel) |

#### Réponse

```json
{
  "parcelle_id": "uuid",
  "periode": {
    "debut": "2024-03-15T00:00:00Z",
    "fin": "2024-03-15T23:59:59Z"
  },
  "capteurs": [
    {
      "id": "uuid",
      "code": "TEMP001",
      "type": "temperature_sol",
      "status": "actif",
      "message": "Capteur fonctionnel",
      "batterie": 85,
      "signal": 90
    }
  ],
  "mesures": {
    "temperature_sol": [
      {
        "capteur_id": "uuid",
        "lectures": [...],
        "statistiques": {
          "moyenne": 22.5,
          "minimum": 18.0,
          "maximum": 27.0,
          "nombre_lectures": 288
        }
      }
    ]
  },
  "alertes": [...],
  "predictions": {...},
  "sante_systeme": {...}
}
```

### Dashboard Monitoring

```http
GET /api/v1/iot-monitoring/parcelles/{parcelle_id}/dashboard
```

Récupère les données du dashboard de monitoring.

#### Paramètres

| Nom | Type | Description |
|-----|------|-------------|
| parcelle_id | UUID | ID de la parcelle |

#### Réponse

```json
{
  "temps_reel": {...},
  "historique": {
    "24h": {...},
    "7j": {...},
    "30j": {...}
  },
  "predictions": {...},
  "maintenance": [...]
}
```

### Recommandations Maintenance

```http
GET /api/v1/iot-monitoring/parcelles/{parcelle_id}/maintenance
```

Récupère les recommandations de maintenance pour une parcelle.

#### Paramètres

| Nom | Type | Description |
|-----|------|-------------|
| parcelle_id | UUID | ID de la parcelle |
| priorite_minimum | string | Filtre par priorité minimum (optionnel) |
| types_capteur | array | Filtre par types de capteur (optionnel) |

#### Réponse

```json
[
  {
    "capteur_id": "uuid",
    "code": "TEMP001",
    "type": "temperature_sol",
    "priorite": "haute",
    "raison": "Batterie faible (15%)",
    "action_recommandee": "Remplacement batterie",
    "deadline": "2024-03-16T12:00:00Z"
  }
]
```

### Webhooks Alertes

```http
POST /api/v1/iot-monitoring/webhooks/alerts
```

Enregistre un webhook pour les alertes.

#### Corps de la requête

```json
{
  "type_alerte": "seuil_depassé",
  "capteur_id": "uuid",
  "message": "Température trop élevée",
  "timestamp": "2024-03-15T10:30:00Z",
  "niveau": "critique",
  "donnees": {
    "valeur": 35.5,
    "seuil": 30.0
  }
}
```

### Configuration

```http
GET /api/v1/iot-monitoring/config
PUT /api/v1/iot-monitoring/config
```

Gère la configuration du système de monitoring.

#### Configuration

```json
{
  "intervalle_actualisation": 300,
  "seuil_alerte_batterie": 20.0,
  "seuil_alerte_signal": 30.0,
  "periode_retention_donnees": 90,
  "webhook_urls": {
    "alertes": "https://example.com/webhooks/alerts"
  },
  "notifications_email": [
    "admin@example.com"
  ]
}
```

### État Santé

```http
GET /api/v1/iot-monitoring/health
```

Vérifie l'état de santé du système de monitoring.

#### Réponse

```json
{
  "status": "healthy",
  "timestamp": "2024-03-15T10:30:00Z",
  "components": {
    "database": "ok",
    "cache": "ok",
    "services": {
      "iot": "ok",
      "weather": "ok",
      "ml": "ok"
    }
  }
}
```

## Codes d'Erreur

| Code | Description |
|------|-------------|
| 404 | Ressource non trouvée |
| 400 | Requête invalide |
| 500 | Erreur serveur |

## Modèles de Données

### SensorStatus

```typescript
enum SensorStatus {
  ACTIF = "actif",
  INACTIF = "inactif",
  MAINTENANCE = "maintenance",
  ERREUR = "erreur"
}
```

### SensorType

```typescript
enum SensorType {
  TEMPERATURE_SOL = "temperature_sol",
  TEMPERATURE_AIR = "temperature_air",
  HUMIDITE_SOL = "humidite_sol",
  HUMIDITE_AIR = "humidite_air",
  LUMINOSITE = "luminosite",
  PLUVIOMETRIE = "pluviometrie",
  PH_SOL = "ph_sol",
  CONDUCTIVITE = "conductivite"
}
```

## Exemples d'Utilisation

### Récupération des données de monitoring

```python
import requests
from datetime import datetime, timedelta

# Configuration
base_url = "http://api.example.com/api/v1/iot-monitoring"
parcelle_id = "123e4567-e89b-12d3-a456-426614174000"

# Paramètres
params = {
    "start_date": (datetime.utcnow() - timedelta(days=1)).isoformat(),
    "end_date": datetime.utcnow().isoformat()
}

# Requête
response = requests.get(
    f"{base_url}/parcelles/{parcelle_id}",
    params=params
)

# Traitement de la réponse
if response.status_code == 200:
    data = response.json()
    print(f"Nombre de capteurs: {len(data['capteurs'])}")
    print(f"Période: {data['periode']}")
else:
    print(f"Erreur: {response.status_code}")
```

### Configuration des alertes

```python
import requests

# Configuration
config = {
    "seuil_alerte_batterie": 15.0,
    "seuil_alerte_signal": 25.0,
    "webhook_urls": {
        "alertes": "https://example.com/webhooks/alerts"
    }
}

# Mise à jour de la configuration
response = requests.put(
    f"{base_url}/config",
    json=config
)

if response.status_code == 200:
    print("Configuration mise à jour avec succès")
else:
    print(f"Erreur: {response.status_code}")
