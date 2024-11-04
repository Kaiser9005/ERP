import { api } from './api';

export interface Stock {
  id: string;
  code: string;
  name: string;
  quantity: number;
  unit: string;
  value: number;
  threshold: number;
}

export interface Movement {
  id: string;
  type: 'ENTREE' | 'SORTIE' | 'TRANSFERT';
  product: string;
  quantity: number;
  unit: string;
  reference: string;
  date: string;
}

export interface InventoryStats {
  totalValue: number;
  valueVariation: {
    value: number;
    type: 'increase' | 'decrease';
  };
  turnoverRate: number;
  turnoverVariation: {
    value: number;
    type: 'increase' | 'decrease';
  };
  alerts: number;
  alertsVariation: {
    value: number;
    type: 'increase' | 'decrease';
  };
  movements: number;
  movementsVariation: {
    value: number;
    type: 'increase' | 'decrease';
  };
}

export const getStocks = async (): Promise<Stock[]> => {
  const response = await api.get('/inventory/stocks');
  return response.data;
};

export const getRecentMovements = async (): Promise<Movement[]> => {
  const response = await api.get('/inventory/movements/recent');
  return response.data;
};

export const getInventoryStats = async (): Promise<InventoryStats> => {
  const response = await api.get('/inventory/stats');
  return response.data;
};

export const createMovement = async (data: {
  productId: string;
  type: string;
  quantity: number;
  reference?: string;
}): Promise<Movement> => {
  const response = await api.post('/inventory/movements', data);
  return response.data;
};