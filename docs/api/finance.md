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

### GET /api/v1/finance/budgets/analysis/{periode}
Récupère l'analyse budgétaire détaillée pour une période.

**Paramètres:**
- periode: Format YYYY-MM

**Réponse:**
```json
{
  "total_prevu": 5000000,
  "total_realise": 4800000,
  "categories": {
    "ACHAT_INTRANT": {
      "prevu": 2000000,
      "realise": 1900000,
      "ecart": -100000,
      "ecart_percentage": -5
    }
  },
  "weather_impact": {
    "score": 30,
    "factors": ["Fortes précipitations"],
    "projections": {
      "TRANSPORT": "Augmentation probable des coûts"
    }
  },
  "recommendations": [
    "Ajustement recommandé du budget transport"
  ]
}
```

## Projections Financières

### GET /api/v1/finance/projections
Récupère les projections financières avec impact météo.

**Paramètres:**
- months_ahead (optionnel): Nombre de mois à projeter (défaut: 3)

**Réponse:**
```json
{
  "revenue": [
    {
      "period": "2024-02",
      "amount": 12000000,
      "weather_impact": 20
    }
  ],
  "expenses": [
    {
      "period": "2024-02",
      "amount": 8000000,
      "weather_impact": 15
    }
  ],
  "weather_factors": [
    "Températures élevées prévues"
  ]
}
```

## Modèles de Données

### Transaction
```typescript
{
  id: UUID
  reference: string
  date_transaction: DateTime
  type_transaction: "RECETTE" | "DEPENSE" | "VIREMENT"
  categorie: "VENTE" | "ACHAT_INTRANT" | "SALAIRE" | "MAINTENANCE" | "TRANSPORT" | "AUTRE"
  montant: number
  devise: string
  description?: string
  statut: "EN_ATTENTE" | "VALIDEE" | "REJETEE" | "ANNULEE"
  piece_jointe?: string
}
```

### Budget
```typescript
{
  id: UUID
  periode: string // YYYY-MM
  categorie: string
  montant_prevu: number
  montant_realise: number
  notes?: string
  metadata?: object
}
```

## Sécurité

Tous les endpoints nécessitent une authentification JWT valide.
Les rôles suivants sont requis :
- FINANCE_READ: Lecture des données financières
- FINANCE_WRITE: Création/modification des transactions et budgets
- FINANCE_ADMIN: Validation des transactions et accès aux analyses
