import { api } from './api';

export interface FinanceStats {
  revenue: number;
  revenueVariation: {
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
  expenses: number;
  expensesVariation: {
    value: number;
    type: 'increase' | 'decrease';
  };
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
}

export interface CashFlowData {
  labels: string[];
  recettes: number[];
  depenses: number[];
}

export interface Budget {
  category: string;
  allocated: number;
  spent: number;
}

export const getFinanceStats = async (): Promise<FinanceStats> => {
  const response = await api.get('/finance/stats');
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

export const createTransaction = async (data: any): Promise<Transaction> => {
  const response = await api.post('/finance/transactions', data);
  return response.data;
};

export const updateTransaction = async (id: string, data: any): Promise<Transaction> => {
  const response = await api.put(`/finance/transactions/${id}`, data);
  return response.data;
};

export const getCashFlowData = async (): Promise<CashFlowData> => {
  const response = await api.get('/finance/cashflow');
  return response.data;
};

export const getBudgetOverview = async (): Promise<Budget[]> => {
  const response = await api.get('/finance/budget');
  return response.data;
};

export const getComptes = async () => {
  const response = await api.get('/finance/comptes');
  return response.data;
};