export enum TypeCompteComptable {
  ACTIF = 'ACTIF',
  PASSIF = 'PASSIF',
  CHARGE = 'CHARGE',
  PRODUIT = 'PRODUIT'
}

export enum StatutEcriture {
  BROUILLON = 'BROUILLON',
  VALIDEE = 'VALIDEE',
  ANNULEE = 'ANNULEE'
}

export interface CompteComptable {
  id: string;
  numero: string;
  libelle: string;
  type_compte: TypeCompteComptable;
  solde: number;
  actif: boolean;
  description?: string;
  metadata?: Record<string, any>;
}

export interface EcritureComptable {
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
  piece_jointe_url?: string;
  metadata?: Record<string, any>;
}

export interface JournalComptable {
  id: string;
  code: string;
  libelle: string;
  type: string;
  actif: boolean;
  description?: string;
  metadata?: Record<string, any>;
  ecritures: EcritureComptable[];
}

export interface CompteBalance {
  compte: {
    numero: string;
    libelle: string;
    type: TypeCompteComptable;
  };
  debit: number;
  credit: number;
  solde: number;
}

export interface Balance {
  periode: {
    debut: string;
    fin: string;
  };
  comptes: Array<{
    id: string;
    numero: string;
    libelle: string;
    type_compte: TypeCompteComptable;
    solde_initial: number;
    total_debit: number;
    total_credit: number;
    solde_final: number;
  }>;
  totaux: {
    debit: number;
    credit: number;
    solde: number;
  };
  metadata?: Record<string, any>;
  actif: Record<string, { libelle: string, montant: number }>;
  passif: Record<string, { libelle: string, montant: number }>;
  total_actif: number;
  total_passif: number;
}

import { ReactNode } from 'react';

export interface GrandLivreResponseType {
  debit: number;
  credit: number;
  date(date: any): ReactNode;
  piece: ReactNode;
  libelle: ReactNode;
  solde(solde: any): ReactNode;
  compte: {
    id: string;
    numero: string;
    libelle: string;
    type_compte: TypeCompteComptable;
  };
  periode: {
    debut: string;
    fin: string;
  };
  solde_initial: number;
  ecritures: GrandLivreEcriture[];
  totaux: {
    debit: number;
    credit: number;
    solde: number;
  };
  metadata?: Record<string, any>;
}

export interface GetGrandLivreParams {
  date_debut?: Date;
  date_fin?: Date;
  compte_id?: string[];
}

export interface GrandLivreEcriture {
  credit: number;
  debit: number;
  id: string;
  date: string;
  piece: string;
  libelle: string;
  ecritures: Array<{
    date: Date;
    piece: string;
    libelle: string;
    debit: number;
    credit: number;
    solde_cumule: number;
  }>;
  solde?: number;
}

export interface BudgetAnalysis {
  periode: {
    debut: string;
    fin: string;
  };
  total_prevu: number;
  total_realise: number;
  categories: Array<{
    code: string;
    libelle: string;
    prevu: number;
    realise: number;
    ecart: number;
    ecart_percentage: number;
  }>;
  weather_impact: {
    score: number;
    factors: string[];
    projections: Record<string, number>;
  };
  recommendations: string[];
  metadata?: Record<string, any>;
}

export interface RapportComptable {
  periode: {
    debut: string;
    fin: string;
  };
  bilan: {
    actif: Record<string, number>;
    passif: Record<string, number>;
    total: number;
  };
  resultat: {
    produits: Record<string, number>;
    charges: Record<string, number>;
    net: number;
  };
  tresorerie: {
    entrees: Record<string, number>;
    sorties: Record<string, number>;
    solde: number;
  };
  ratios: {
    liquidite: number;
    solvabilite: number;
    rentabilite: number;
  };
  metadata?: Record<string, any>;
}

export interface CloturePeriode {
  periode: {
    debut: string;
    fin: string;
    type: 'MENSUELLE' | 'ANNUELLE';
  };
  statut: 'EN_COURS' | 'TERMINEE' | 'ERREUR';
  etapes: Array<{
    code: string;
    libelle: string;
    statut: 'A_FAIRE' | 'EN_COURS' | 'TERMINEE' | 'ERREUR';
    message?: string;
  }>;
  resultats: {
    ecritures_validees: number;
    comptes_soldes: number;
    anomalies: Array<{
      type: string;
      message: string;
      compte?: string;
      ecriture?: string;
    }>;
  };
  metadata?: Record<string, any>;
}

export interface CashFlowData {
  periode: {
    debut: string;
    fin: string;
  };
  entrees: Array<{
    date: string;
    montant: number;
    categorie: string;
    description: string;
  }>;
  sorties: Array<{
    date: string;
    montant: number;
    categorie: string;
    description: string;
  }>;
  solde_initial: number;
  solde_final: number;
  variation: number;
  metadata?: Record<string, any>;
}

// Types pour les formulaires
export interface CompteComptableFormData {
  numero: string;
  libelle: string;
  type_compte: TypeCompteComptable;
  description?: string;
}

export interface EcritureComptableFormData {
  date_ecriture: string;
  journal_id: string;
  lignes: Array<{
    compte_id: string;
    libelle: string;
    debit: number;
    credit: number;
  }>;
}

// Types pour les filtres
export interface ComptabiliteFilters {
  type_compte?: TypeCompteComptable;
  date_debut?: string;
  date_fin?: string;
  actif?: boolean;
}

// Types pour les statistiques
export interface ComptabiliteStats {
  revenue: number;
  revenueVariation: {
    value: number;
    type: 'increase' | 'decrease';
  };
  expenses: number;
  expensesVariation: {
    value: number;
    type: 'increase' | 'decrease';
  };
  profit: number;
  profitVariation: {
    value: number;
    type: 'increase' | 'decrease';
  };
  cashflow: number;
  cashflowVariation: {
    value: number;
    type: 'increase' | 'decrease';
  };
}

export interface GetGrandLivreParams {
  date_debut?: Date;
  date_fin?: Date;
  compte_id?: string[];
}

export interface CompteResultatType {
  produits: Record<string, { libelle: string; montant: number }>;
  total_produits: number;
  charges: Record<string, { libelle: string; montant: number }>;
  total_charges: number;
  resultat_net: number;
}
