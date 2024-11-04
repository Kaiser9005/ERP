# Module Activités - Documentation API

## Activités Récentes

### GET /api/v1/activities/recent

Récupère la liste des activités récentes dans le système.

**Paramètres de requête:**
- `limit` (optionnel): Nombre maximum d'activités à retourner (défaut: 10)

**Réponse:**
```json
[
  {
    "id": "uuid",
    "type": "PRODUCTION",
    "title": "Récolte - P001",
    "description": "Récolte de 500 kg",
    "date": "2024-01-20T10:30:00Z",
    "color": "success",
    "user": {
      "id": "uuid",
      "name": "John Doe"
    }
  }
]
```

**Types d'activités:**
- `PRODUCTION`: Activités liées à la production agricole
- `INVENTORY`: Mouvements de stock
- `FINANCE`: Transactions financières
- `HR`: Activités RH