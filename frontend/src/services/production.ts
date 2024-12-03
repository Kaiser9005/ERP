import axios from 'axios';
import { Parcelle, CycleCulture, Recolte, ProductionEvent } from '../types/production';

const API_URL = '/api/v1/production';

// Parcelles
export const getParcelles = async (): Promise<Parcelle[]> => {
  const response = await axios.get(`${API_URL}/parcelles`);
  return response.data;
};

export const getParcelle = async (id: string): Promise<Parcelle> => {
  const response = await axios.get(`${API_URL}/parcelles/${id}`);
  return response.data;
};

export const createParcelle = async (data: Omit<Parcelle, 'id'>): Promise<Parcelle> => {
  const response = await axios.post(`${API_URL}/parcelles`, data);
  return response.data;
};

export const updateParcelle = async (id: string, data: Partial<Parcelle>): Promise<Parcelle> => {
  const response = await axios.put(`${API_URL}/parcelles/${id}`, data);
  return response.data;
};

// Cycles de culture
export const getCyclesCulture = async (parcelleId: string): Promise<CycleCulture[]> => {
  const response = await axios.get(`${API_URL}/parcelles/${parcelleId}/cycles`);
  return response.data;
};

export const createCycleCulture = async (data: Partial<CycleCulture>): Promise<CycleCulture> => {
  const response = await axios.post(`${API_URL}/cycles`, data);
  return response.data;
};

// Récoltes
export const getRecoltes = async (parcelleId: string): Promise<Recolte[]> => {
  const response = await axios.get(`${API_URL}/parcelles/${parcelleId}/recoltes`);
  return response.data;
};

export const createRecolte = async (data: Partial<Recolte>): Promise<Recolte> => {
  const response = await axios.post(`${API_URL}/recoltes`, data);
  return response.data;
};

export const updateRecolte = async (id: string, data: Partial<Recolte>): Promise<Recolte> => {
  const response = await axios.put(`${API_URL}/recoltes/${id}`, data);
  return response.data;
};

// Événements de production
export const getProductionEvents = async (parcelleId: string): Promise<ProductionEvent[]> => {
  const response = await axios.get(`${API_URL}/parcelles/${parcelleId}/events`);
  return response.data;
};

export const createProductionEvent = async (data: Partial<ProductionEvent>): Promise<ProductionEvent> => {
  const response = await axios.post(`${API_URL}/events`, data);
  return response.data;
};

// Statistiques de production
export const getProductionStats = async (parcelleId: string) => {
  const response = await axios.get(`${API_URL}/parcelles/${parcelleId}/stats`);
  return response.data;
};

export const productionService = {
  getParcelles,
  getParcelle,
  createParcelle,
  updateParcelle,
  getCyclesCulture,
  createCycleCulture,
  getRecoltes,
  createRecolte,
  updateRecolte,
  getProductionEvents,
  createProductionEvent,
  getProductionStats
};

export default productionService;
