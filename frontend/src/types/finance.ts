import { UUID } from './common';

export interface Compte {
  id: UUID;
  libelle: string;
  type: string;
  solde: number;
}

export enum TypeTransaction {
  RECETTE = 'RECETTE',
  DEPENSE = 'DEPENSE',
  VIREMENT = 'VIREMENT',
  ENTREE = "ENTREE",
  SORTIE = "SORTIE"
}

export enum StatutTransaction {
  BROUILLON = 'BROUILLON',
  VALIDE = 'VALIDE',
  ANNULE = 'ANNULE'
}

export interface TransactionFilter {
  [key: string]: string | number | boolean | undefined;
}

export interface Transaction {
  id: UUID;
  date: string;
  montant: number;
  type: string;
  description?: string;
  categorie?: string;
  reference?: string;
}

export interface TransactionListResponse {
  transactions: Transaction[];
  total: number;
  page: number;
  limit: number;
}

export interface TransactionFormData {
  date_transaction: string;
  montant: number;
  type_transaction: TypeTransaction;
  description?: string;
  categorie: string;
  fichierJustificatif?: File;
  compte_source?: string;
  compte_destination?: string;
  reference: string;
  statut: StatutTransaction;
}

export interface ApiResponse<T> {
  data: T;
  message?: string;
  status: number;
}

export interface Budget {
  id: UUID;
  categorie: string;
  montantAlloue: number;
  montantDepense: number;
  periode: string;
}

export interface BudgetFilter {
  [key: string]: string | number | boolean | undefined;
}

export interface BudgetListResponse {
  budgets: Budget[];
  total: number;
  page: number;
  limit: number;
}

export interface BudgetFormData {
  categorie: string;
  montantAlloue: number;
  periode: string;
}

export interface BudgetAnalysis {
  totalBudget: number;
  totalDepense: number;
  pourcentageUtilisation: number;
  categoriesAnalyse: {
    categorie: string;
    montantAlloue: number;
    montantDepense: number;
    pourcentageUtilisation: number;
  }[];
}

export interface AnalyseBudgetaire {
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
    projections: {
      [key: string]: string;
    };
  };
  recommandations: string[];
  periode?: string;
  total?: number;
  alertes?: string[];
}

export interface DonneesTresorerie {
  soldeActuel: number;
  entrees: number;
  sorties: number;
  previsionsTresorerie: number;
}

export interface ProjectionsFinancieres {
  revenus: number;
  depenses: number;
  beneficeProjetePeriode: number;
  tendances: {
    periode: string;
    revenus: number;
    depenses: number;
  }[];
}

export interface CashFlowData {
  periodes: string[];
  entrees: number[];
  sorties: number[];
  soldeNet: number[];
}

export interface FinanceStats {
  totalRevenus?: number;
  totalDepenses?: number;
  beneficeNet?: number;
  ratioDepensesRevenus?: number;
  revenue?: number;
  revenueVariation?: {
    valeur: number;
    type: 'hausse' | 'baisse';
  };
  profit?: number;
  profitVariation?: {
    valeur: number;
    type: 'hausse' | 'baisse';
  };
  cashflow?: number;
  cashflowVariation?: {
    valeur: number;
    type: 'hausse' | 'baisse';
  };
  expenses?: number;
  expensesVariation?: {
    valeur: number;
    type: 'hausse' | 'baisse';
  };
  tresorerie?: number;
  variation_tresorerie?: {
    valeur: number;
    type: 'hausse' | 'baisse';
  };
  factures_impayees?: number;
  paiements_prevus?: number;
  budget_mensuel?: number;
  depenses_mois?: number;
}

export interface VueBudgetaire {
  categorie: string;
  montantAlloue: number;
  montantDepense: number;
  pourcentageUtilisation: number;
}
