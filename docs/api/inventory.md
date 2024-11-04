# Module Inventaire - Documentation API

## Statistiques

### GET /api/v1/inventory/stats
Récupère les statistiques d'inventaire.

**Réponse:**
```json
{
  "totalValue": 1500000,
  "valueVariation": {
    "value": 15,
    "type": "increase"
  },
  "turnoverRate": 12,
  "turnoverVariation": {
    "value": 5,
    "type": "decrease"
  },
  "alerts": 3,
  "alertsVariation": {
    "value": 50,
    "type": "increase"
  },
  "movements": 25,
  "movementsVariation": {
    "value": 10,
    "type": "increase"
  }
}
```

## Produits

### GET /api/v1/inventory/produits
Récupère la liste des produits.

**Paramètres de requête:**
- `categorie` (optionnel): Filtre par catégorie
- `skip` (optionnel): Pagination
- `limit` (optionnel): Limite de résultats

### POST /api/v1/inventory/produits
Crée un nouveau produit.

## Stocks

### GET /api/v1/inventory/stocks
Récupère l'état des stocks.

**Paramètres de requête:**
- `entrepot_id` (optionnel): Filtre par entrepôt
- `produit_id` (optionnel): Filtre par produit

## Mouvements

### POST /api/v1/inventory/mouvements
Enregistre un mouvement de stock.

**Corps de la requête:**
```json
{
  "produit_id": "uuid",
  "type_mouvement": "ENTREE",
  "quantite": 100,
  "entrepot_destination_id": "uuid",
  "cout_unitaire": 1500,
  "reference_document": "BL-2024-001"
}
```

## Entrepôts

### GET /api/v1/inventory/entrepots
Récupère la liste des entrepôts.

### POST /api/v1/inventory/entrepots
Crée un nouvel entrepôt.