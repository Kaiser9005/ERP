import { api } from './api';
import type {
  Transaction,
  TransactionFormData,
  TransactionFilter,
  TransactionListResponse,
  CashFlowData,
  FinanceStats,
  Budget,
  BudgetFormData,
  BudgetFilter,
  BudgetListResponse,
  BudgetAnalysis,
  DonneesTresorerie,
  AnalyseBudgetaire,
  ProjectionsFinancieres,
  VueBudgetaire,
  Compte
} from '../types/finance';
import type { ApiResponse, UUID } from '../types/common';

export const getComptes = async (): Promise<Compte[]> => {
  const response = await api.get<ApiResponse<Compte[]>>('/api/v1/finance/comptes');
  return response.data.data;
};

// Transactions
export const getTransactions = async (filter?: TransactionFilter): Promise<TransactionListResponse> => {
  const params = new URLSearchParams();
  if (filter) {
    Object.entries(filter).forEach(([key, value]) => {
      if (value !== undefined) {
        params.append(key, value.toString());
      }
    });
  }
  const response = await api.get<TransactionListResponse>(`/api/v1/finance/transactions?${params}`);
  return response.data;
};

export const getTransaction = async (id: UUID): Promise<Transaction> => {
  const response = await api.get<ApiResponse<Transaction>>(`/api/v1/finance/transactions/${id}`);
  return response.data.data;
};

export const createTransaction = async (data: TransactionFormData): Promise<Transaction> => {
  const formData = new FormData();
  Object.entries(data).forEach(([key, value]) => {
    if (value !== undefined) {
      if (value instanceof File) {
        formData.append(key, value);
      } else {
        formData.append(key, value.toString());
      }
    }
  });
  const response = await api.post<ApiResponse<Transaction>>('/api/v1/finance/transactions', formData);
  return response.data.data;
};

export const updateTransaction = async (id: UUID, data: Partial<TransactionFormData>): Promise<Transaction> => {
  const formData = new FormData();
  Object.entries(data).forEach(([key, value]) => {
    if (value !== undefined) {
      if (value instanceof File) {
        formData.append(key, value);
      } else {
        formData.append(key, value.toString());
      }
    }
  });
  const response = await api.patch<ApiResponse<Transaction>>(`/api/v1/finance/transactions/${id}`, formData);
  return response.data.data;
};

export const deleteTransaction = async (id: UUID): Promise<void> => {
  await api.delete(`/api/v1/finance/transactions/${id}`);
};

// Budgets
export const getBudgets = async (filter?: BudgetFilter): Promise<BudgetListResponse> => {
  const params = new URLSearchParams();
  if (filter) {
    Object.entries(filter).forEach(([key, value]) => {
      if (value !== undefined) {
        params.append(key, value.toString());
      }
    });
  }
  const response = await api.get<BudgetListResponse>(`/api/v1/finance/budgets?${params}`);
  return response.data;
};

export const getBudget = async (id: UUID): Promise<Budget> => {
  const response = await api.get<ApiResponse<Budget>>(`/api/v1/finance/budgets/${id}`);
  return response.data.data;
};

export const createBudget = async (data: BudgetFormData): Promise<Budget> => {
  const response = await api.post<ApiResponse<Budget>>('/api/v1/finance/budgets', data);
  return response.data.data;
};

export const updateBudget = async (id: UUID, data: Partial<BudgetFormData>): Promise<Budget> => {
  const response = await api.patch<ApiResponse<Budget>>(`/api/v1/finance/budgets/${id}`, data);
  return response.data.data;
};

export const deleteBudget = async (id: UUID): Promise<void> => {
  await api.delete(`/api/v1/finance/budgets/${id}`);
};

// Analyses et statistiques
export const getBudgetAnalysis = async (periode: string): Promise<BudgetAnalysis> => {
  const response = await api.get<ApiResponse<BudgetAnalysis>>(`/api/v1/finance/budgets/analysis`, {
    params: { periode }
  });
  return response.data.data;
};

export const getAnalyseBudget = async (periode: string): Promise<AnalyseBudgetaire> => {
  const response = await api.get<ApiResponse<AnalyseBudgetaire>>(`/api/v1/finance/analyse-budget`, {
    params: { periode }
  });
  return response.data.data;
};

export const getDonneesTresorerie = async (periode?: string): Promise<DonneesTresorerie> => {
  const params = new URLSearchParams();
  if (periode) {
    params.append('periode', periode);
  }
  const response = await api.get<ApiResponse<DonneesTresorerie>>(`/api/v1/finance/tresorerie?${params}`);
  return response.data.data;
};

export const getProjectionsFinancieres = async (periode: string): Promise<ProjectionsFinancieres> => {
  const response = await api.get<ApiResponse<ProjectionsFinancieres>>(`/api/v1/finance/projections`, {
    params: { periode }
  });
  return response.data.data;
};

export const getCashFlowData = async (periode?: string): Promise<CashFlowData> => {
  const params = new URLSearchParams();
  if (periode) {
    params.append('periode', periode);
  }
  const response = await api.get<ApiResponse<CashFlowData>>(`/api/v1/finance/cashflow?${params}`);
  return response.data.data;
};

export const getStatsFinance = async (periode?: string): Promise<FinanceStats> => {
  const params = new URLSearchParams();
  if (periode) {
    params.append('periode', periode);
  }
  const response = await api.get<ApiResponse<FinanceStats>>(`/api/v1/finance/stats?${params}`);
  return response.data.data;
};

export const getVueBudget = async (periode: string): Promise<VueBudgetaire[]> => {
  const response = await api.get<ApiResponse<VueBudgetaire[]>>(`/api/v1/finance/vue-budget`, {
    params: { periode }
  });
  return response.data.data;
};

// Alias pour la compatibilité avec le code existant
export { getStatsFinance as getFinanceStats };

export default {
  getTransactions,
  getTransaction,
  createTransaction,
  updateTransaction,
  deleteTransaction,
  getBudgets,
  getBudget,
  createBudget,
  updateBudget,
  deleteBudget,
  getBudgetAnalysis,
  getAnalyseBudget,
  getDonneesTresorerie,
  getProjectionsFinancieres,
  getCashFlowData,
  getStatsFinance,
  getVueBudget
};
