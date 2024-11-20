export interface Variation {
  value: number;
  type: 'increase' | 'decrease';
}

export interface FinanceStats {
  revenue: number;
  revenueVariation: Variation;
  expenses: number;
  expensesVariation: Variation;
  profit: number;
  profitVariation: Variation;
  cashflow: number;
  cashflowVariation: Variation;
}

export type TypeTransaction = 'RECETTE' | 'DEPENSE';
export type StatutTransaction = 'EN_ATTENTE' | 'VALIDEE' | 'ANNULEE';

export interface Transaction {
  id: string;
  date: string;
  reference: string;
  description: string;
  montant: number;
  type_transaction: TypeTransaction;
  statut: StatutTransaction;
}
