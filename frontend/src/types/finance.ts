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

export type TypeTransaction = 'RECETTE' | 'DEPENSE' | 'VIREMENT';
export type StatutTransaction = 'EN_ATTENTE' | 'VALIDEE' | 'REJETEE' | 'ANNULEE';
export type TypeCompte = 'BANQUE' | 'CAISSE' | 'EPARGNE' | 'CREDIT';

export interface Compte {
  id: string;
  numero: string;
  libelle: string;
  type_compte: TypeCompte;
  devise: string;
  solde: number;
  actif: boolean;
  metadata?: Record<string, any>;
}

export interface Transaction {
  id: string;
  reference: string;
  date_transaction: string;
  type_transaction: TypeTransaction;
  categorie: string;
  montant: number;
  devise: string;
  description?: string;
  compte_source_id?: string;
  compte_destination_id?: string;
  piece_jointe?: string;
  statut: StatutTransaction;
  validee_par_id?: {
    id: string;
    nom: string;
    prenom: string;
  };
  date_validation?: string;
  metadata?: Record<string, any>;
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

export interface TransactionFormData {
  reference: string;
  type_transaction: TypeTransaction;
  categorie: string;
  montant: number;
  description?: string;
  compte_source_id?: string;
  compte_destination_id?: string;
  piece_jointe?: File;
}

export interface TransactionFilter {
  dateDebut?: string;
  dateFin?: string;
  type?: TypeTransaction;
  categorie?: string;
  statut?: StatutTransaction;
  compte_id?: string;
  page?: number;
  limit?: number;
}
