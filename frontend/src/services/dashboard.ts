import { api } from './api';

export interface DashboardStats {
  production: {
    total: number;
    variation: {
      value: number;
      type: 'increase' | 'decrease';
    };
  };
  inventory: {
    value: number;
    variation: {
      value: number;
      type: 'increase' | 'decrease';
    };
  };
  finance: {
    revenue: number;
    variation: {
      value: number;
      type: 'increase' | 'decrease';
    };
  };
  hr: {
    activeEmployees: number;
    variation: {
      value: number;
      type: 'increase' | 'decrease';
    };
  };
}

export const getDashboardStats = async (): Promise<DashboardStats> => {
  const response = await api.get('/dashboard/stats');
  return response.data;
};