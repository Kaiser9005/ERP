# API Finance

## Vue d'ensemble

L'API Finance fournit les endpoints nécessaires pour la gestion financière de FOFAL, incluant :
- Analyse budgétaire
- Projections financières
- Gestion des transactions
- Statistiques financières

## Endpoints

### Analyse Budgétaire

#### GET /api/finance/budget/analyse/{periode}
Récupère l'analyse budgétaire détaillée pour une période donnée.

**Paramètres**
- `periode`: Format YYYY-MM

**Réponse**
```json
{
  "total_prevu": 5000000,
  "total_realise": 4500000,
  "categories": {
    "Équipement": {
      "prevu": 2000000,
      "realise": 1800000,
      "ecart": -200000,
      "ecart_pourcentage": -10
    }
  },
  "impact_meteo": {
    "score": 15,
    "facteurs": ["Précipitations abondantes"],
    "projections": {
      "Équipement": "Usure accélérée due aux conditions météo"
    }
  },
  "recommandations": [
    "Prévoir un budget supplémentaire pour la maintenance"
  ]
}
```

### Projections Financières

#### GET /api/finance/projections
Récupère les projections financières avec impact météorologique.

**Paramètres**
- `mois_avenir`: Nombre de mois à projeter (défaut: 3)

**Réponse**
```json
{
  "recettes": [
    {
      "periode": "2024-01",
      "montant": 1500000,
      "impact_meteo": 15
    }
  ],
  "depenses": [
    {
      "periode": "2024-01",
      "montant": 1200000,
      "impact_meteo": 10
    }
  ],
  "facteurs_meteo": [
    "Précipitations abondantes",
    "Température élevée"
  ]
}
```

### Statistiques Financières

#### GET /api/finance/stats
Récupère les statistiques financières globales.

**Réponse**
```json
{
  "tresorerie_actuelle": 5000000,
  "recettes_mois": 1500000,
  "depenses_mois": 1200000,
  "variation_mensuelle": 10
}
```

### Transactions

#### GET /api/finance/transactions
Liste toutes les transactions.

**Paramètres de requête**
- `page`: Numéro de page (défaut: 1)
- `limite`: Nombre d'éléments par page (défaut: 20)
- `type`: Type de transaction (RECETTE/DEPENSE)
- `statut`: Statut de la transaction

**Réponse**
```json
{
  "total": 100,
  "page": 1,
  "limite": 20,
  "transactions": [
    {
      "id": "uuid",
      "date": "2024-01-15",
      "montant": 150000,
      "type": "RECETTE",
      "description": "Vente production",
      "statut": "VALIDEE"
    }
  ]
}
```

#### POST /api/finance/transactions
Crée une nouvelle transaction.

**Corps de la requête**
```json
{
  "date": "2024-01-15",
  "montant": 150000,
  "type": "RECETTE",
  "description": "Vente production"
}
```

#### PUT /api/finance/transactions/{id}
Met à jour une transaction existante.

**Paramètres**
- `id`: Identifiant de la transaction

**Corps de la requête**
```json
{
  "montant": 160000,
  "description": "Vente production modifiée"
}
```

## Modèles de Données

### Transaction
```typescript
interface Transaction {
  id: string;
  date: string;
  montant: number;
  type: 'RECETTE' | 'DEPENSE';
  description: string;
  statut: 'BROUILLON' | 'VALIDEE' | 'ANNULEE';
  pieces_jointes?: string[];
  metadata?: Record<string, any>;
}
```

### AnalyseBudgetaire
```typescript
interface AnalyseBudgetaire {
  total_prevu: number;
  total_realise: number;
  categories: {
    [key: string]: {
      prevu: number;
      realise: number;
      ecart: number;
      ecart_pourcentage: number;
    };
  };
  impact_meteo: {
    score: number;
    facteurs: string[];
    projections: Record<string, string>;
  };
  recommandations: string[];
}
```

### ProjectionsFinancieres
```typescript
interface ProjectionsFinancieres {
  recettes: Array<{
    periode: string;
    montant: number;
    impact_meteo: number;
  }>;
  depenses: Array<{
    periode: string;
    montant: number;
    impact_meteo: number;
  }>;
  facteurs_meteo: string[];
}
```

## Codes d'Erreur

- `400`: Requête invalide
- `401`: Non authentifié
- `403`: Non autorisé
- `404`: Ressource non trouvée
- `409`: Conflit (ex: transaction déjà validée)
- `500`: Erreur serveur

## Notes d'Implémentation

- Toutes les dates sont au format ISO 8601
- Les montants sont en XAF (Franc CFA)
- L'impact météo est exprimé en pourcentage
- Les projections sont calculées sur la base des données historiques et des prévisions météo
- Les transactions validées ne peuvent plus être modifiées
