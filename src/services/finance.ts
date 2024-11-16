import { api } from './api';

export interface Variation {
  value: number;
  type: 'increase' | 'decrease';
}

export interface FinanceStats {
  revenue: number;
  revenueVariation: Variation;
  profit: number;
  profitVariation: Variation;
  cashflow: number;
  cashflowVariation: Variation;
  expenses: number;
  expensesVariation: Variation;
}

export interface Transaction {
  id: string;
  reference: string;
  date_transaction: string;
  type_transaction: string;
  categorie: string;
  montant: number;
  description?: string;
  statut: string;
  piece_jointe?: string;
  compte_source?: string;
  compte_destination?: string;
  validee_par?: string;
  date_validation?: string;
}

export interface CashFlowData {
  labels: string[];
  recettes: number[];
  depenses: number[];
  solde?: number[];
  previsions?: number[];
  impact_meteo?: number[];
}

export interface Budget {
  category: string;
  allocated: number;
  spent: number;
}

export interface Compte {
  id: string;
  numero: string;
  libelle: string;
  type: string;
  solde: number;
}

export const getFinanceStats = async (): Promise<FinanceStats> => {
  const response = await api.get<FinanceStats>('/finance/stats');
  return response.data;
};

export const getTransactions = async (): Promise<Transaction[]> => {
  const response = await api.get<Transaction[]>('/finance/transactions');
  return response.data;
};

export const getTransaction = async (id: string): Promise<Transaction> => {
  const response = await api.get<Transaction>(`/finance/transactions/${id}`);
  return response.data;
};

export const createTransaction = async (data: Partial<Transaction>): Promise<Transaction> => {
  const response = await api.post<Transaction>('/finance/transactions', data);
  return response.data;
};

export const updateTransaction = async (id: string, data: Partial<Transaction>): Promise<Transaction> => {
  const response = await api.put<Transaction>(`/finance/transactions/${id}`, data);
  return response.data;
};

export const getCashFlowData = async (): Promise<CashFlowData> => {
  const response = await api.get<CashFlowData>('/finance/cashflow');
  return response.data;
};

export const getBudgetOverview = async (): Promise<Budget[]> => {
  const response = await api.get<Budget[]>('/finance/budget');
  return response.data;
};

export const getComptes = async (): Promise<Compte[]> => {
  const response = await api.get<Compte[]>('/finance/comptes');
  return response.data;
};
