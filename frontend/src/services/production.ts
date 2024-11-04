import { api } from './api';
import { Parcelle, ProductionStats, ProductionEvent } from '../types/production';

export const getParcelles = async (): Promise<Parcelle[]> => {
  const response = await api.get('/production/parcelles');
  return response.data;
};

export const getProductionStats = async (): Promise<ProductionStats> => {
  const response = await api.get('/production/stats');
  return response.data;
};

export const getProductionEvents = async (): Promise<ProductionEvent[]> => {
  const response = await api.get('/production/events');
  return response.data.map((event: any) => ({
    ...event,
    start: new Date(event.start),
    end: new Date(event.end)
  }));
};

export const createParcelle = async (data: Partial<Parcelle>): Promise<Parcelle> => {
  const response = await api.post('/production/parcelles', data);
  return response.data;
};

export const updateParcelle = async (id: string, data: Partial<Parcelle>): Promise<Parcelle> => {
  const response = await api.put(`/production/parcelles/${id}`, data);
  return response.data;
};