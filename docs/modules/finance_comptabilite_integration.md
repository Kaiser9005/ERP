# Intégration Finance-Comptabilité

## Vue d'Ensemble

L'intégration entre les modules Finance (70%) et Comptabilité (75%) est structurée selon les principes suivants :

### Séparation des Responsabilités

#### Module Finance
- Gestion des transactions opérationnelles
- Interface utilisateur pour les opérations financières
- Suivi des comptes bancaires et de la trésorerie
- Gestion des budgets et prévisions

#### Module Comptabilité
- Traitement comptable des transactions
- Génération des écritures comptables
- Production des états financiers
- Respect des normes comptables

## Structure Technique

### Organisation des Fichiers

```plaintext
frontend/src/
├── components/
│   ├── finance/
│   │   ├── TransactionForm.tsx
│   │   ├── TransactionList.tsx
│   │   └── FinanceStats.tsx
│   └── comptabilite/
│       ├── GrandLivre.tsx
│       ├── Balance.tsx
│       └── ComptabilitePage.tsx
├── types/
│   ├── finance.ts
│   └── comptabilite.ts
└── services/
    ├── finance.ts
    └── comptabilite.ts
```

### Types et Interfaces

#### Finance (finance.ts)
```typescript
enum TypeTransaction {
  RECETTE = 'RECETTE',
  DEPENSE = 'DEPENSE',
  VIREMENT = 'VIREMENT'
}

enum StatutTransaction {
  EN_ATTENTE = 'EN_ATTENTE',
  VALIDEE = 'VALIDEE',
  REJETEE = 'REJETEE',
  ANNULEE = 'ANNULEE'
}

interface Transaction {
  id: string;
  reference: string;
  type: TypeTransaction;
  montant: number;
  devise: string;
  date_transaction: string;
  statut: StatutTransaction;
  compte_source_id?: string;
  compte_destination_id?: string;
}
```

#### Comptabilité (comptabilite.ts)
```typescript
enum TypeCompte {
  ACTIF = 'ACTIF',
  PASSIF = 'PASSIF',
  CHARGE = 'CHARGE',
  PRODUIT = 'PRODUIT'
}

enum StatutEcriture {
  BROUILLON = 'BROUILLON',
  VALIDEE = 'VALIDEE',
  ANNULEE = 'ANNULEE'
}

interface EcritureComptable {
  id: string;
  date_ecriture: string;
  journal_id: string;
  lignes: Array<{
    compte_id: string;
    libelle: string;
    debit: number;
    credit: number;
  }>;
  statut: StatutEcriture;
}
```

## Workflow d'Intégration

### 1. Création d'une Transaction
```typescript
// 1. Saisie dans TransactionForm
const transaction = await financeService.createTransaction({
  type: 'RECETTE',
  montant: 1000,
  devise: 'EUR',
  compte_destination_id: 'COMPTE1'
});

// 2. Génération automatique des écritures
const ecritures = await comptabiliteService.genererEcritures(transaction);

// 3. Validation comptable
await comptabiliteService.validerEcritures(ecritures);
```

### 2. Rapprochement Bancaire
```typescript
interface Rapprochement {
  transaction_id: string;
  ecriture_id: string;
  date_rapprochement: string;
  statut: 'RAPPROCHE' | 'ECART';
  commentaire?: string;
}

// Processus de rapprochement
const rapprochement = await financeService.rapprochement({
  releve_bancaire: releveBancaire,
  periode: { debut: '2024-01-01', fin: '2024-01-31' }
});
```

### 3. Reporting Intégré
```typescript
interface ReportingFinancier {
  tresorerie: {
    solde_actuel: number;
    previsions: Array<{
      date: string;
      montant: number;
    }>;
  };
  comptable: {
    balance: Array<CompteBalance>;
    grand_livre: Array<LigneGrandLivre>;
  };
}
```

## QueryKeys Structure

### Finance
```typescript
export const financeKeys = {
  transactions: {
    all: ['transactions'] as const,
    lists: () => [...financeKeys.transactions.all, 'list'] as const,
    detail: (id: string) => [...financeKeys.transactions.all, id] as const,
  },
  comptes: {
    all: ['comptes'] as const,
    lists: () => [...financeKeys.comptes.all, 'list'] as const,
    detail: (id: string) => [...financeKeys.comptes.all, id] as const,
  }
};
```

### Comptabilité
```typescript
export const comptabiliteKeys = {
  ecritures: {
    all: ['ecritures'] as const,
    lists: () => [...comptabiliteKeys.ecritures.all, 'list'] as const,
    detail: (id: string) => [...comptabiliteKeys.ecritures.all, id] as const,
  },
  comptes: {
    all: ['comptes_comptables'] as const,
    lists: () => [...comptabiliteKeys.comptes.all, 'list'] as const,
    detail: (id: string) => [...comptabiliteKeys.comptes.all, id] as const,
  }
};
```

## Validation et Contrôles

### Règles de Validation
1. Toute transaction doit générer des écritures équilibrées
2. Les écritures doivent respecter le plan comptable
3. Les rapprochements doivent être validés par un comptable
4. Les clôtures nécessitent une double validation

### Contrôles Automatiques
```typescript
interface ControleIntegration {
  transaction: {
    montant_min: number;
    devise_autorisees: string[];
    validation_requise: boolean;
  };
  ecriture: {
    equilibre: boolean;
    comptes_autorises: string[];
    double_validation: boolean;
  };
}
```

## Maintenance et Évolution

### Points d'Attention
1. Maintenir la cohérence des données entre les modules
2. Assurer la traçabilité des opérations
3. Gérer les cas particuliers (annulations, corrections)
4. Optimiser les performances des requêtes

### Évolutions Prévues
1. Automatisation complète des écritures
2. Rapprochement bancaire intelligent
3. Reporting en temps réel
4. Intégration IA pour la catégorisation
