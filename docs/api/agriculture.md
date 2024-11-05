# API Agriculture

## Vue d'ensemble
API pour la gestion des parcelles agricoles, cycles de culture et récoltes de FOFAL.

## Endpoints

### Parcelles

#### GET /api/v1/agriculture/parcelles
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

#### POST /api/v1/agriculture/parcelles
Crée une nouvelle parcelle.

**Corps de la requête**
```json
{
  "code": "P001",
  "culture_type": "PALMIER",
  "surface_hectares": 10.5,
  "date_plantation": "2024-01-15",
  "coordonnees_gps": {
    "latitude": 4.0511,
    "longitude": 9.7679
  },
  "responsable_id": "uuid"
}
```

### Cycles de Culture

#### GET /api/v1/agriculture/cycles-culture
Liste les cycles de culture.

**Paramètres**
- `skip` (int, optionnel)
- `limit` (int, optionnel)
- `parcelle_id` (uuid, optionnel)

#### POST /api/v1/agriculture/cycles-culture
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

#### GET /api/v1/agriculture/recoltes
Liste les récoltes avec filtres.

**Paramètres**
- `skip` (int, optionnel)
- `limit` (int, optionnel)
- `parcelle_id` (uuid, optionnel)
- `date_debut` (string, optionnel): Format YYYY-MM-DD
- `date_fin` (string, optionnel): Format YYYY-MM-DD

#### POST /api/v1/agriculture/recoltes
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

## Codes d'Erreur

- 400: Données invalides
- 401: Non authentifié
- 403: Non autorisé
- 404: Ressource non trouvée
- 422: Erreur de validation
- 500: Erreur serveur

## Notes d'Utilisation

- Toutes les requêtes nécessitent une authentification
- Les coordonnées GPS doivent être valides (latitude: -90 à 90, longitude: -180 à 180)
- Les dates doivent être au format ISO 8601
- Les quantités sont en kilogrammes
- Les surfaces sont en hectares
