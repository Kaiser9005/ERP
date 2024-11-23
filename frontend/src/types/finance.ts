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

// Types spécifiques aux opérations financières
export type TypeTransaction = 'RECETTE' | 'DEPENSE' | 'VIREMENT';
export type StatutTransaction = 'EN_ATTENTE' | 'VALIDEE' | 'REJETEE' | 'ANNULEE';
export type TypeCompteFinancier = 'BANQUE' | 'CAISSE' | 'EPARGNE' | 'CREDIT';

export interface CompteFinancier {
  id: string;
  numero: string;
  libelle: string;
  type_compte: TypeCompteFinancier;
  devise: string;
  solde: number;
  actif: boolean;
  compte_comptable_id?: string; // Lien vers le compte comptable associé
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
  validee_par?: {
    id: string;
    nom: string;
    prenom: string;
  };
  date_validation?: string;
  ecriture_comptable_id?: string; // Lien vers l'écriture comptable générée
  metadata?: Record<string, any>;
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

// Types pour les rapports financiers
export interface RapportTresorerie {
  date: string;
  solde_initial: number;
  entrees: number;
  sorties: number;
  solde_final: number;
  previsions: {
    entrees: number;
    sorties: number;
    impact_meteo: number;
  };
}

export interface RapportBudgetaire {
  periode: string;
  categories: Record<string, {
    prevu: number;
    realise: number;
    ecart: number;
    ecart_pourcentage: number;
  }>;
  total_prevu: number;
  total_realise: number;
  impact_meteo: {
    score: number;
    facteurs: string[];
  };
}

// Types pour les tableaux de bord
export interface DashboardFinance {
  tresorerie: {
    solde_actuel: number;
    variation_periode: Variation;
    prevision_fin_mois: number;
  };
  budget: {
    realisation: number;
    variation: Variation;
    alertes: string[];
  };
  transactions: {
    en_attente: number;
    a_valider: number;
    recentes: Transaction[];
  };
}
