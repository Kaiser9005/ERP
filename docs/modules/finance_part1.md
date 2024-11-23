# Module Finance (70%) - Partie 1 : Fondamentaux

## Vue d'ensemble

Le module Finance gère les opérations financières quotidiennes de FOFAL, notamment :
- Transactions (recettes, dépenses, virements)
- Gestion de trésorerie
- Budgets opérationnels
- Rapports financiers
- Projections et analyses

## Architecture

### Composants Principaux

#### 1. Transactions
- Gestion des recettes
- Gestion des dépenses
- Virements internes
- Pièces justificatives
- Validation et workflow

#### 2. Comptes Financiers
- Comptes bancaires
- Caisses
- Comptes d'épargne
- Crédits

#### 3. Budget
- Suivi budgétaire
- Alertes de dépassement
- Réaffectations
- Impact météorologique

#### 4. Rapports
- États de trésorerie
- Suivi budgétaire
- Projections financières
- Analyses d'impact météo

## Implémentation Technique

### Types de Données
```typescript
// Types principaux
type TypeTransaction = 'RECETTE' | 'DEPENSE' | 'VIREMENT';
type StatutTransaction = 'EN_ATTENTE' | 'VALIDEE' | 'REJETEE' | 'ANNULEE';
type TypeCompteFinancier = 'BANQUE' | 'CAISSE' | 'EPARGNE' | 'CREDIT';

interface Transaction {
  id: string;
  reference: string;
  type_transaction: TypeTransaction;
  montant: number;
  devise: string;
  compte_source_id?: string;
  compte_destination_id?: string;
  statut: StatutTransaction;
}

interface CompteFinancier {
  id: string;
  numero: string;
  type_compte: TypeCompteFinancier;
  solde: number;
  devise: string;
}
```

### Services
```typescript
// Service finance
const financeService = {
  // Transactions
  getTransactions(filters?: TransactionFilter): Promise<Transaction[]>;
  createTransaction(data: TransactionFormData): Promise<Transaction>;
  updateTransaction(id: string, data: Partial<TransactionFormData>): Promise<Transaction>;
  
  // Comptes
  getComptes(): Promise<CompteFinancier[]>;
  getCompte(id: string): Promise<CompteFinancier>;
}
```

### Composants React
- TransactionForm : Création/modification des transactions
- TransactionList : Liste des transactions avec filtres
- CompteDetails : Détails et mouvements d'un compte
- BudgetOverview : Vue d'ensemble budgétaire
- TresorerieChart : Graphique de trésorerie

[Suite dans finance_part2.md]
