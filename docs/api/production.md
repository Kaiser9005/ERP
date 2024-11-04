# Module Production - Documentation API

## Parcelles

### GET /api/v1/production/parcelles
Récupère la liste des parcelles.

**Paramètres de requête:**
- `skip` (int, optionnel): Nombre d'éléments à sauter (pagination)
- `limit` (int, optionnel): Nombre maximum d'éléments à retourner

**Réponse:**
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
    },
    "responsable_id": "uuid"
  }
]
```

### POST /api/v1/production/parcelles
Crée une nouvelle parcelle.

**Corps de la requête:**
```json
{
  "code": "P001",
  "culture_type": "PALMIER",
  "surface_hectares": 10.5,
  "date_plantation": "2024-01-15",
  "statut": "ACTIVE",
  "coordonnees_gps": {
    "latitude": 4.0511,
    "longitude": 9.7679
  },
  "responsable_id": "uuid"
}
```

## Cycles de Culture

### GET /api/v1/production/cycles
Récupère la liste des cycles de culture.

**Paramètres de requête:**
- `parcelle_id` (UUID, optionnel): Filtre par parcelle
- `skip` (int, optionnel): Pagination
- `limit` (int, optionnel): Limite de résultats

## Récoltes

### GET /api/v1/production/recoltes
Récupère la liste des récoltes.

### POST /api/v1/production/recoltes
Enregistre une nouvelle récolte.