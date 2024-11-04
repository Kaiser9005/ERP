# Module Tableau de Bord - Documentation API

## Statistiques Globales

### GET /api/v1/dashboard/stats
Récupère les statistiques globales pour le tableau de bord.

**Réponse:**
```json
{
  "production": {
    "total": 125.5,
    "variation": {
      "value": 15.2,
      "type": "increase"
    },
    "parcelles_actives": 8
  },
  "inventory": {
    "valeur_totale": 45600000,
    "alertes": 3,
    "mouvements_jour": 12
  },
  "finance": {
    "recettes": 75000000,
    "depenses": 45000000,
    "solde": 30000000
  },
  "hr": {
    "effectif_total": 42,
    "en_conge": 5
  }
}
```

## Activités Récentes

### GET /api/v1/dashboard/activities
Récupère les activités récentes tous types confondus.

**Paramètres de requête:**
- `limit` (optionnel): Nombre maximum d'activités à retourner (défaut: 10)

**Réponse:**
```json
[
  {
    "type": "PRODUCTION",
    "titre": "Récolte - P001",
    "description": "Récolte de 500 kg",
    "date": "2024-01-20T10:30:00Z"
  }
]
```

## Données Météorologiques

### GET /api/v1/dashboard/weather
Récupère les données météorologiques pour le site.

**Réponse:**
```json
{
  "temperature": 25.5,
  "humidite": 80,
  "vent": 5.2,
  "description": "Partiellement nuageux"
}
```