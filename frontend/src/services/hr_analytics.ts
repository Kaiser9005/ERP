import axios from 'axios';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { HRAnalytics, EmployeeStats, FormationAnalytics, ContractAnalytics, PayrollAnalytics, PerformancePrediction } from '../types/hr_analytics';

const API_BASE_URL = '/api/v1/hr/analytics';

// Clés de cache
export const HR_ANALYTICS_KEYS = {
  all: ['hr-analytics'] as const,
  stats: () => [...HR_ANALYTICS_KEYS.all, 'stats'] as const,
  formation: () => [...HR_ANALYTICS_KEYS.all, 'formation'] as const,
  contract: () => [...HR_ANALYTICS_KEYS.all, 'contract'] as const,
  payroll: () => [...HR_ANALYTICS_KEYS.all, 'payroll'] as const,
  performance: (id: number) => [...HR_ANALYTICS_KEYS.all, 'performance', id] as const,
};

// Services API
const api = {
  getHRAnalytics: async (): Promise<HRAnalytics> => {
    const response = await axios.get(API_BASE_URL);
    return response.data;
  },

  getEmployeeStats: async (): Promise<EmployeeStats> => {
    const response = await axios.get(`${API_BASE_URL}/employee-stats`);
    return response.data;
  },

  getFormationAnalytics: async (): Promise<FormationAnalytics> => {
    const response = await axios.get(`${API_BASE_URL}/formation-analytics`);
    return response.data;
  },

  getContractAnalytics: async (): Promise<ContractAnalytics> => {
    const response = await axios.get(`${API_BASE_URL}/contract-analytics`);
    return response.data;
  },

  getPayrollAnalytics: async (): Promise<PayrollAnalytics> => {
    const response = await axios.get(`${API_BASE_URL}/payroll-analytics`);
    return response.data;
  },

  predictEmployeePerformance: async (employeeId: number): Promise<PerformancePrediction> => {
    const response = await axios.get(`${API_BASE_URL}/predict-performance/${employeeId}`);
    return response.data;
  },

  invalidateCache: async (employeeId?: number) => {
    const response = await axios.post(`${API_BASE_URL}/cache/invalidate`, { employee_id: employeeId });
    return response.data;
  },
};

// Hooks React Query
export const useHRAnalytics = () => {
  return useQuery({
    queryKey: HR_ANALYTICS_KEYS.all,
    queryFn: api.getHRAnalytics,
    staleTime: 15 * 60 * 1000, // 15 minutes
    gcTime: 30 * 60 * 1000, // 30 minutes
  });
};

export const useEmployeeStats = () => {
  return useQuery({
    queryKey: HR_ANALYTICS_KEYS.stats(),
    queryFn: api.getEmployeeStats,
    staleTime: 15 * 60 * 1000, // 15 minutes
    gcTime: 30 * 60 * 1000, // 30 minutes
  });
};

export const useFormationAnalytics = () => {
  return useQuery({
    queryKey: HR_ANALYTICS_KEYS.formation(),
    queryFn: api.getFormationAnalytics,
    staleTime: 30 * 60 * 1000, // 30 minutes
    gcTime: 60 * 60 * 1000, // 1 heure
  });
};

export const useContractAnalytics = () => {
  return useQuery({
    queryKey: HR_ANALYTICS_KEYS.contract(),
    queryFn: api.getContractAnalytics,
    staleTime: 30 * 60 * 1000, // 30 minutes
    gcTime: 60 * 60 * 1000, // 1 heure
  });
};

export const usePayrollAnalytics = () => {
  return useQuery({
    queryKey: HR_ANALYTICS_KEYS.payroll(),
    queryFn: api.getPayrollAnalytics,
    staleTime: 30 * 60 * 1000, // 30 minutes
    gcTime: 60 * 60 * 1000, // 1 heure
  });
};

export const useEmployeePerformancePrediction = (employeeId: number) => {
  return useQuery({
    queryKey: HR_ANALYTICS_KEYS.performance(employeeId),
    queryFn: () => api.predictEmployeePerformance(employeeId),
    staleTime: 60 * 60 * 1000, // 1 heure
    gcTime: 2 * 60 * 60 * 1000, // 2 heures
  });
};

// Mutation pour invalider le cache
export const useInvalidateCache = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: api.invalidateCache,
    onSuccess: (_, employeeId) => {
      if (employeeId) {
        // Invalide uniquement les données de l'employé spécifique
        queryClient.invalidateQueries({
          queryKey: HR_ANALYTICS_KEYS.performance(employeeId),
        });
      } else {
        // Invalide toutes les données RH
        queryClient.invalidateQueries({
          queryKey: HR_ANALYTICS_KEYS.all,
        });
      }
    },
  });
};

// Fonction utilitaire pour précharger les données
export const prefetchHRAnalytics = async (queryClient: ReturnType<typeof useQueryClient>) => {
  await queryClient.prefetchQuery({
    queryKey: HR_ANALYTICS_KEYS.all,
    queryFn: api.getHRAnalytics,
  });
};

// Export des fonctions API pour les tests
export const hrAnalyticsApi = api;
