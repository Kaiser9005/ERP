# Module Finance (70%) - Documentation API - Endpoints

## Endpoints REST

### Transactions

#### CRUD de Base
```typescript
// Liste des transactions avec filtres
GET /api/v1/finance/transactions
Params: {
  dateDebut?: string;
  dateFin?: string;
  type?: TypeTransaction;
  statut?: StatutTransaction;
  compte_id?: string;
  page?: number;
  limit?: number;
}

// Création d'une transaction
POST /api/v1/finance/transactions
Body: {
  reference: string;
  type_transaction: TypeTransaction;
  montant: number;
  devise: string;
  description?: string;
  compte_source_id?: string;
  compte_destination_id?: string;
  piece_jointe?: File;
}

// Détails d'une transaction
GET /api/v1/finance/transactions/:id

// Mise à jour d'une transaction
PUT /api/v1/finance/transactions/:id
Body: Partial<TransactionFormData>

// Suppression d'une transaction
DELETE /api/v1/finance/transactions/:id
```

#### Actions Spécifiques
```typescript
// Validation d'une transaction
POST /api/v1/finance/transactions/:id/validate
Body: {
  validateur_id: string;
  commentaire?: string;
}

// Annulation d'une transaction
POST /api/v1/finance/transactions/:id/cancel
Body: {
  motif: string;
  commentaire?: string;
}

// Historique d'une transaction
GET /api/v1/finance/transactions/:id/history
```

### Comptes

#### CRUD de Base
```typescript
// Liste des comptes avec filtres
GET /api/v1/finance/comptes
Params: {
  type?: TypeCompteFinancier;
  actif?: boolean;
  devise?: string;
}

// Création d'un compte
POST /api/v1/finance/comptes
Body: {
  numero: string;
  libelle: string;
  type_compte: TypeCompteFinancier;
  devise: string;
  solde_initial: number;
}

// Détails d'un compte
GET /api/v1/finance/comptes/:id

// Mise à jour d'un compte
PUT /api/v1/finance/comptes/:id
Body: Partial<CompteFormData>
```

#### Actions Spécifiques
```typescript
// Mouvements d'un compte
GET /api/v1/finance/comptes/:id/mouvements
Params: {
  dateDebut?: string;
  dateFin?: string;
  type?: TypeMouvement;
}

// Solde d'un compte
GET /api/v1/finance/comptes/:id/solde
Params: {
  date?: string;
}

// Réconciliation bancaire
POST /api/v1/finance/comptes/:id/reconciliation
Body: {
  date_reconciliation: string;
  solde_releve: number;
  pieces_jointes?: File[];
}
```

### Rapports

#### Rapports Standards
```typescript
// Rapport de trésorerie
GET /api/v1/finance/rapports/tresorerie
Params: {
  dateDebut: string;
  dateFin: string;
  comptes?: string[];
  format?: 'json' | 'pdf' | 'xlsx';
}

// Rapport budgétaire
GET /api/v1/finance/rapports/budget
Params: {
  periode: string;
  categories?: string[];
  format?: 'json' | 'pdf' | 'xlsx';
}

// Statistiques globales
GET /api/v1/finance/stats
Params: {
  periode?: string;
}
```

#### Rapports Spécialisés
```typescript
// Projections financières
GET /api/v1/finance/rapports/projections
Params: {
  horizon: number;
  categories?: string[];
  inclure_meteo?: boolean;
}

// Impact météorologique
GET /api/v1/finance/rapports/impact-meteo
Params: {
  dateDebut: string;
  dateFin: string;
  categories?: string[];
}

// Rapport d'audit
GET /api/v1/finance/rapports/audit
Params: {
  dateDebut: string;
  dateFin: string;
  type?: 'transaction' | 'compte' | 'all';
  format?: 'json' | 'pdf';
}
