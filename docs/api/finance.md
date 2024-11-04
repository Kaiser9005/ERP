# Module Finance - Documentation API

## Statistiques

### GET /api/v1/finance/stats
Récupère les statistiques financières.

**Réponse:**
```json
{
  "revenue": 1500000,
  "revenueVariation": {
    "value": 15,
    "type": "increase"
  },
  "profit": 300000,
  "profitVariation": {
    "value": 5,
    "type": "decrease"
  },
  "cashflow": 500000,
  "cashflowVariation": {
    "value": 10,
    "type": "increase"
  },
  "expenses": 1200000,
  "expensesVariation": {
    "value": 8,
    "type": "increase"
  }
}
```

## Transactions

### GET /api/v1/finance/transactions
Récupère la liste des transactions.

**Paramètres de requête:**
- `type` (optionnel): Type de transaction (RECETTE, DEPENSE, VIREMENT)
- `statut` (optionnel): Statut de la transaction
- `date_debut` (optionnel): Date de début de la période
- `date_fin` (optionnel): Date de fin de la période
- `skip` (optionnel): Pagination
- `limit` (optionnel): Limite de résultats

### POST /api/v1/finance/transactions
Crée une nouvelle transaction.

**Corps de la requête:**
- Multipart form data avec:
  - Transaction (JSON)
  - Pièce jointe (fichier)

## Comptes

### GET /api/v1/finance/comptes
Récupère la liste des comptes.

**Paramètres de requête:**
- `type` (optionnel): Type de compte (BANQUE, CAISSE, EPARGNE)
- `actif` (optionnel): État du compte

### POST /api/v1/finance/comptes
Crée un nouveau compte.

## Budgets

### GET /api/v1/finance/budgets
Récupère la liste des budgets.

**Paramètres de requête:**
- `periode` (optionnel): Période (format: YYYY-MM)
- `categorie` (optionnel): Catégorie de budget

### POST /api/v1/finance/budgets
Crée un nouveau budget.