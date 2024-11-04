# Module Météo - Documentation API

## Données Météorologiques Actuelles

### GET /api/v1/weather/current

Récupère les données météorologiques actuelles pour le site de FOFAL.

**Réponse:**
```json
{
  "temperature": 25.5,
  "humidity": 80,
  "windSpeed": 5.2,
  "uvIndex": 8,
  "forecast": [
    {
      "date": "2024-01-20T12:00:00Z",
      "temperature": 26.5,
      "precipitation": 30
    }
  ]
}
```

**Description des champs:**
- `temperature`: Température en degrés Celsius
- `humidity`: Humidité relative en pourcentage
- `windSpeed`: Vitesse du vent en km/h
- `uvIndex`: Indice UV (0-11)
- `forecast`: Prévisions pour les prochaines périodes
  - `date`: Date et heure de la prévision
  - `temperature`: Température prévue
  - `precipitation`: Probabilité de précipitation en pourcentage