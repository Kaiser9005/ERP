import axios from 'axios';
import { Parcelle, CycleCulture, Recolte, ProductionEvent, WeatherData } from '../types/production';

const API_URL = '/api/v1/production';

export const productionService = {
  // Parcelles
  // Parcelles
  getParcelles: async (): Promise<Parcelle[]> => {
    const response = await axios.get(`${API_URL}/parcelles`);
    return response.data;
  },

  getParcelle: async (id: string): Promise<Parcelle> => {
    const response = await axios.get(`${API_URL}/parcelles/${id}`);
    return response.data;
  },

  createParcelle: async (parcelleData: Partial<Parcelle>): Promise<Parcelle> => {
    const response = await axios.post(`${API_URL}/parcelles`, parcelleData);
    return response.data;
  },

  updateParcelle: async (id: string, parcelleData: Partial<Parcelle>): Promise<Parcelle> => {
    const response = await axios.put(`${API_URL}/parcelles/${id}`, parcelleData);
    return response.data;
  },

  // Cycles de culture

  // Récoltes
  getRecoltes: async (parcelleId: string): Promise<Recolte[]> => {
    const response = await axios.get(`${API_URL}/parcelles/${parcelleId}/recoltes`);
    return response.data;
  },

  createRecolte: async (data: Partial<Recolte>): Promise<Recolte> => {
    const response = await axios.post(`${API_URL}/recoltes`, data);
    return response.data;
  },

  updateRecolte: async (id: string, data: Partial<Recolte>): Promise<Recolte> => {
    const response = await axios.put(`${API_URL}/recoltes/${id}`, data);
    return response.data;
  },

  // Événements de production
  getProductionEvents: async (parcelleId: string): Promise<ProductionEvent[]> => {
    const response = await axios.get(`${API_URL}/parcelles/${parcelleId}/events`);
    return response.data;
  },

  createProductionEvent: async (data: Partial<ProductionEvent>): Promise<ProductionEvent> => {
    const response = await axios.post(`${API_URL}/events`, data);
    return response.data;
  },

  // Statistiques de production
  getProductionStats: async (parcelleId: string) => {
    const response = await axios.get(`${API_URL}/parcelles/${parcelleId}/stats`);
    return response.data;
  },

  // Météo
  getWeatherData: async (type: 'current' | 'forecast'): Promise<WeatherData> => {
    const response = await axios.get(`${API_URL}/weather/${type}`);
    return response.data;
  }
};

export default productionService;
