import { api } from './api';
import { Variation, FinanceStats, Transaction, TypeTransaction, StatutTransaction } from '../types/finance';

export interface Compte {
  id: string;
  libelle: string;
  type: string;
  solde: number;
  devise: string;
}

export interface Budget {
  id: string;
  periode: string;
  montant_prevu: number;
  montant_reel: number;
  categorie: string;
  statut: 'EN_COURS' | 'TERMINE';
}

export interface DonneesTresorerie {
  labels: string[];
  recettes: number[];
  depenses: number[];
}

export interface VueBudgetaire {
  categorie: string;
  depense: number;
  alloue: number;
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

export const getStatsFinance = async (): Promise<FinanceStats> => {
  const response = await api.get('/finance/stats');
  return response.data;
};

export const getDonneesTresorerie = async (): Promise<DonneesTresorerie> => {
  const response = await api.get('/finance/tresorerie');
  return response.data;
};

export const getVueBudget = async (): Promise<VueBudgetaire[]> => {
  const response = await api.get('/finance/budget/vue');
  return response.data;
};

export const getAnalyseBudget = async (periode: string): Promise<AnalyseBudgetaire> => {
  const response = await api.get(`/finance/budget/analyse/${periode}`);
  return response.data;
};

export const getProjectionsFinancieres = async (moisAvenir: number = 3): Promise<ProjectionsFinancieres> => {
  const response = await api.get(`/finance/projections?mois_avenir=${moisAvenir}`);
  return response.data;
};

export const getTransactions = async (): Promise<Transaction[]> => {
  const response = await api.get('/finance/transactions');
  return response.data;
};

export const getTransaction = async (id: string): Promise<Transaction> => {
  const response = await api.get(`/finance/transactions/${id}`);
  return response.data;
};

export const creerTransaction = async (data: Omit<Transaction, 'id'>): Promise<Transaction> => {
  const response = await api.post('/finance/transactions', data);
  return response.data;
};

export const modifierTransaction = async (id: string, data: Partial<Transaction>): Promise<Transaction> => {
  const response = await api.put(`/finance/transactions/${id}`, data);
  return response.data;
};

export const getBudgets = async (): Promise<Budget[]> => {
  const response = await api.get('/finance/budgets');
  return response.data;
};

export const getComptes = async (): Promise<Compte[]> => {
  const response = await api.get('/finance/comptes');
  return response.data;
};

export const creerBudget = async (data: Omit<Budget, 'id'>): Promise<Budget> => {
  const response = await api.post('/finance/budgets', data);
  return response.data;
};

export const modifierBudget = async (id: string, data: Partial<Budget>): Promise<Budget> => {
  const response = await api.put(`/finance/budgets/${id}`, data);
  return response.data;
};

// Re-export des types pour faciliter l'utilisation
export type { Variation, FinanceStats, Transaction, TypeTransaction, StatutTransaction };
