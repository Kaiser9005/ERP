# API Météo

## Vue d'ensemble

L'API météo fournit des données météorologiques en temps réel et des prévisions pour optimiser la planification agricole. Elle utilise l'API Visual Crossing Weather pour obtenir des données précises et fiables, avec un système de cache Redis pour optimiser les performances.

## Points d'accès

### Obtenir les conditions météorologiques actuelles

```http
GET /api/v1/weather/current
```

#### Réponse

```json
{
  "timestamp": "2024-01-20T14:30:00Z",
  "temperature": 28.5,
  "humidity": 65,
  "precipitation": 0,
  "wind_speed": 12,
  "conditions": "Partiellement nuageux",
  "uv_index": 6,
  "cloud_cover": 40,
  "cached_at": "2024-01-20T14:30:00Z",
  "risks": {
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
  "recommendations": [
    "Maintenir une surveillance de l'hydratation des plants",
    "Éviter les travaux aux heures les plus chaudes"
  ]
}
```

### Obtenir les prévisions météorologiques

```http
GET /api/v1/weather/forecast
```

#### Paramètres

| Paramètre | Type | Description |
|-----------|------|-------------|
| days | number | Nombre de jours de prévision (défaut: 7) |

#### Réponse

```json
{
  "location": "Ebondi, Cameroon",
  "days": [
    {
      "date": "2024-01-20",
      "temp_max": 32,
      "temp_min": 22,
      "precipitation": 0,
      "humidity": 65,
      "conditions": "Ensoleillé",
      "description": "Ciel dégagé toute la journée"
    }
  ]
}
```

### Obtenir les métriques agricoles

```http
GET /api/v1/weather/agricultural-metrics
```

#### Paramètres

| Paramètre | Type | Description |
|-----------|------|-------------|
| force_refresh | boolean | Force le rafraîchissement du cache (défaut: false) |

#### Réponse

```json
{
  "current_conditions": {
    "temperature": 28.5,
    "humidity": 65,
    "precipitation": 0,
    "wind_speed": 12,
    "conditions": "Partiellement nuageux",
    "uv_index": 6,
    "cloud_cover": 40,
    "cached_at": "2024-01-20T14:30:00Z"
  },
  "risks": {
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
  "recommendations": [
    "Maintenir une surveillance de l'hydratation des plants",
    "Éviter les travaux aux heures les plus chaudes"
  ]
}
```

## Niveaux de Risque

Les niveaux de risque sont catégorisés comme suit :

- `LOW`: Conditions normales, pas d'action particulière requise
- `MEDIUM`: Surveillance accrue recommandée
- `HIGH`: Actions préventives nécessaires

### Seuils de Risque

#### Précipitations
- `HIGH`: > 20mm/h
- `MEDIUM`: > 10mm/h
- `LOW`: ≤ 10mm/h

#### Température
- `HIGH`: > 35°C
- `MEDIUM`: > 30°C
- `LOW`: ≤ 30°C

## Configuration

La configuration du service météo se fait via les variables d'environnement :

```env
VITE_WEATHER_API_KEY=votre_clé_api
VITE_WEATHER_LOCATION=Ebondi,Cameroon
VITE_WEATHER_CACHE_DURATION=1800
```

## Cache et Performance

- Cache Redis pour les données fréquemment accédées
- Durée de cache : 30 minutes par défaut
- Invalidation automatique du cache si données trop anciennes
- Retry automatique en cas d'échec (3 tentatives)
- Compression gzip des réponses

## Sécurité

- Authentification JWT requise
- Rate limiting : 100 requêtes par minute par IP
- Validation des paramètres avec Pydantic
- Logs détaillés des accès
- Protection CSRF active

## Gestion des Erreurs

L'API retourne les codes d'erreur standard HTTP :

- `400` : Requête invalide
- `401` : Non authentifié
- `403` : Non autorisé
- `429` : Trop de requêtes
- `500` : Erreur serveur
- `503` : Service météo externe indisponible

## Mise à jour des Données

- Données météo actuelles : toutes les 30 minutes
- Prévisions : toutes les 6 heures
- Métriques agricoles : calculées en temps réel
- Indicateur de fraîcheur des données inclus dans les réponses

## Intégration Frontend

### Composants Disponibles

#### WeatherWidget
- Affichage des conditions actuelles
- Alertes visuelles pour les risques élevés
- Recommandations agricoles
- Mise à jour automatique
- Indicateur de fraîcheur des données

#### WeatherDashboard
- Vue détaillée des conditions météo
- Graphiques de tendances
- Prévisions sur 7 jours
- Métriques agricoles complètes

## Monitoring

- Logs détaillés des appels API
- Métriques de performance
- Alertes en cas d'erreurs fréquentes
- Dashboard de monitoring en temps réel
- Suivi des taux d'erreur et latences
