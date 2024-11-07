# API Production

## Vue d'ensemble
API pour la gestion complète de la production agricole, incluant la gestion des parcelles, cycles de culture, récoltes et événements de production.

## Endpoints

### Parcelles

#### GET /api/v1/production/parcelles
Liste toutes les parcelles avec pagination et filtres.

**Paramètres**
- `skip` (int, optionnel): Nombre d'éléments à sauter
- `limit` (int, optionnel): Nombre maximum d'éléments à retourner
- `culture_type` (string, optionnel): PALMIER ou PAPAYE
- `statut` (string, optionnel): ACTIVE, EN_REPOS, EN_PREPARATION

**Réponse**
```json
[
  {
    "id": "uuid",
    "code": "P001",
    "culture_type": "PALMIER",
    "surface_hectares": 10.5,
    "date_plantation": "2024-01-15",
    "statut": "ACTIVE",
    "coordonnees_gps": {
      "latitude": 4.0511,
      "longitude": 9.7679
    }
  }
]
```

### Cycles de Culture

#### GET /api/v1/production/cycles-culture
Liste les cycles de culture.

**Paramètres**
- `skip` (int, optionnel)
- `limit` (int, optionnel)
- `parcelle_id` (uuid, optionnel)

#### POST /api/v1/production/cycles-culture
Crée un nouveau cycle de culture.

**Corps de la requête**
```json
{
  "parcelle_id": "uuid",
  "date_debut": "2024-01-01",
  "date_fin": "2024-12-31",
  "rendement_prevu": 1500.0,
  "notes": "Cycle principal 2024"
}
```

### Récoltes

#### GET /api/v1/production/recoltes
Liste les récoltes avec filtres.

**Paramètres**
- `skip` (int, optionnel)
- `limit` (int, optionnel)
- `parcelle_id` (uuid, optionnel)
- `date_debut` (string, optionnel): Format YYYY-MM-DD
- `date_fin` (string, optionnel): Format YYYY-MM-DD

#### POST /api/v1/production/recoltes
Enregistre une nouvelle récolte.

**Corps de la requête**
```json
{
  "parcelle_id": "uuid",
  "date_recolte": "2024-02-01T08:00:00",
  "quantite_kg": 500.5,
  "qualite": "A",
  "conditions_meteo": {
    "temperature": 25.5,
    "humidite": 75.0,
    "precipitation": 0.0
  },
  "equipe_recolte": ["uuid1", "uuid2"]
}
```

### Événements de Production

#### GET /api/v1/production/events
Liste les événements de production.

**Paramètres**
- `skip` (int, optionnel)
- `limit` (int, optionnel)
- `parcelle_id` (uuid, optionnel)
- `date_debut` (string, optionnel)
- `date_fin` (string, optionnel)

#### POST /api/v1/production/events
Crée un nouvel événement de production.

**Corps de la requête**
```json
{
  "parcelle_id": "uuid",
  "type": "MAINTENANCE",
  "date_debut": "2024-02-01T08:00:00",
  "description": "Maintenance des équipements",
  "responsable_id": "uuid"
}
```

### Statistiques

#### GET /api/v1/production/stats
Obtient les statistiques de production.

**Réponse**
```json
{
  "total_surface": 100.5,
  "parcelles_actives": 5,
  "recolte_en_cours": 2,
  "production_mensuelle": 1500.0,
  "rendement_moyen": 14.92
}
```

## Notes d'Utilisation

- Toutes les requêtes nécessitent une authentification
- Les coordonnées GPS doivent être valides (latitude: -90 à 90, longitude: -180 à 180)
- Les dates doivent être au format ISO 8601
- Les quantités sont en kilogrammes
- Les surfaces sont en hectares
