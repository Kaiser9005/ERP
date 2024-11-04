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
  // Pour le développement, on retourne des données statiques
  return {
    production: {
      total: 1250,
      variation: {
        value: 15,
        type: 'increase'
      }
    },
    inventory: {
      value: 45600000,
      variation: {
        value: 5,
        type: 'decrease'
      }
    },
    finance: {
      revenue: 75000000,
      variation: {
        value: 10,
        type: 'increase'
      }
    },
    hr: {
      activeEmployees: 42,
      variation: {
        value: 2,
        type: 'increase'
      }
    }
  };
};