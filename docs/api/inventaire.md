# Module Inventaire - Documentation API

## Produits

### GET /api/v1/inventaire/produits
Récupère la liste des produits en stock.

**Paramètres de requête:**
- `skip` (int, optionnel): Pagination
- `limit` (int, optionnel): Limite de résultats

**Réponse:**
```json
[
  {
    "id": "uuid",
    "code": "PRD001",
    "nom": "Engrais NPK",
    "categorie": "INTRANT",
    "description": "Engrais composé NPK 20-10-10",
    "unite_mesure": "KG",
    "seuil_alerte": 100,
    "prix_unitaire": 1500
  }
]
```

## Mouvements de Stock

### POST /api/v1/inventaire/mouvements
Enregistre un nouveau mouvement de stock.

**Corps de la requête:**
```json
{
  "produit_id": "uuid",
  "type_mouvement": "ENTREE",
  "quantite": 100,
  "entrepot_destination_id": "uuid",
  "responsable_id": "uuid",
  "reference_document": "BL-2024-001"
}
```

## État des Stocks

### GET /api/v1/inventaire/stocks
Récupère l'état actuel des stocks.