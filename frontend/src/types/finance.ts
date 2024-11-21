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

export type TypeTransaction = 'ENTREE' | 'SORTIE';
export type StatutTransaction = 'EN_ATTENTE' | 'VALIDEE' | 'ANNULEE';

export interface Transaction {
  id: string;
  date: string;
  reference?: string;
  description: string;
  montant: number;
  type: TypeTransaction;
  statut: StatutTransaction;
  categorie?: string;
}

export interface VueBudgetaire {
  categorie: string;
  depense: number;
  alloue: number;
}

export interface Projection {
  periode: string;
  montant: number;
  impact_meteo: number;
}

export interface ProjectionsFinancieres {
  recettes: Projection[];
  depenses: Projection[];
  facteurs_meteo: string[];
}
