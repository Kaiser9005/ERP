# API Météo

## Vue d'ensemble

L'API météo fournit des données météorologiques en temps réel et des prévisions pour optimiser la planification agricole. Elle utilise l'API Visual Crossing Weather pour obtenir des données précises et fiables.

## Points d'accès

### Obtenir les conditions météorologiques actuelles

```http
GET /api/weather/current
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
  "cloud_cover": 40
}
```

### Obtenir les prévisions météorologiques

```http
GET /api/weather/forecast
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
GET /api/weather/agricultural-metrics
```

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
    "cloud_cover": 40
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

## Configuration

La configuration du service météo se fait via les variables d'environnement :

```env
VITE_WEATHER_API_KEY=votre_clé_api
VITE_WEATHER_LOCATION=Ebondi,Cameroon
```

## Sécurité

- L'accès à l'API nécessite une authentification JWT
- La clé API est stockée de manière sécurisée dans les variables d'environnement
- Les requêtes sont limitées en fréquence pour éviter l'abus

## Gestion des Erreurs

L'API retourne les codes d'erreur standard HTTP :

- `400` : Requête invalide
- `401` : Non authentifié
- `403` : Non autorisé
- `429` : Trop de requêtes
- `500` : Erreur serveur

## Mise à jour des Données

- Les données météorologiques actuelles sont mises à jour toutes les 30 minutes
- Les prévisions sont actualisées toutes les 6 heures
- Les métriques agricoles sont calculées en temps réel à chaque requête

## Intégration Frontend

Le composant `WeatherDashboard` affiche les données météorologiques dans une interface utilisateur intuitive avec :

- Affichage des conditions actuelles
- Visualisation des risques
- Liste des recommandations
- Mise à jour automatique
- Indicateurs visuels pour les niveaux de risque
