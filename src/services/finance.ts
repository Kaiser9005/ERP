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
  BudgetListResponse
} from '../types/finance';
import type { ApiResponse, UUID } from '../types/common';

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

// Statistiques et tableaux de bord
export const getCashFlowData = async (periode?: string): Promise<CashFlowData> => {
  const params = new URLSearchParams();
  if (periode) {
    params.append('periode', periode);
  }
  const response = await api.get<ApiResponse<CashFlowData>>(`/api/v1/finance/cashflow?${params}`);
  return response.data.data;
};

export const getFinanceStats = async (periode?: string): Promise<FinanceStats> => {
  const params = new URLSearchParams();
  if (periode) {
    params.append('periode', periode);
  }
  const response = await api.get<ApiResponse<FinanceStats>>(`/api/v1/finance/stats?${params}`);
  return response.data.data;
};
