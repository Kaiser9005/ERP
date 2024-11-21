import axios from 'axios';
import { Product, StockMovement, StockLevel, Stock, StatsInventaire, MouvementStock } from '../types/inventaire';

const API_URL = '/api/v1/inventaire';

// Produits
export const getProduct = async (id: string): Promise<Product> => {
  const response = await axios.get(`${API_URL}/produits/${id}`);
  return response.data;
};

export const getProducts = async (): Promise<Product[]> => {
  const response = await axios.get(`${API_URL}/produits`);
  return response.data;
};

export const createProduct = async (product: Omit<Product, 'id'>): Promise<Product> => {
  const response = await axios.post(`${API_URL}/produits`, product);
  return response.data;
};

export const updateProduct = async (id: string, product: Partial<Product>): Promise<Product> => {
  const response = await axios.put(`${API_URL}/produits/${id}`, product);
  return response.data;
};

export const deleteProduct = async (id: string): Promise<void> => {
  await axios.delete(`${API_URL}/produits/${id}`);
};

// Mouvements de stock
export const getProductMovements = async (productId: string): Promise<StockMovement[]> => {
  const response = await axios.get(`${API_URL}/produits/${productId}/mouvements`);
  return response.data;
};

export const getMouvements = async (params?: {
  debut?: string;
  fin?: string;
  type?: 'ENTREE' | 'SORTIE';
  produit_id?: string;
}): Promise<MouvementStock[]> => {
  const response = await axios.get(`${API_URL}/mouvements`, { params });
  return response.data;
};

export const createStockMovement = async (movement: Omit<StockMovement, 'id' | 'date_mouvement' | 'responsable'>): Promise<StockMovement> => {
  const response = await axios.post(`${API_URL}/mouvements`, movement);
  return response.data;
};

// Niveaux de stock
export const getStockLevel = async (productId: string): Promise<StockLevel> => {
  const response = await axios.get(`${API_URL}/produits/${productId}/stock`);
  return response.data;
};

export const getStockLevels = async (): Promise<Record<string, StockLevel>> => {
  const response = await axios.get(`${API_URL}/stock`);
  return response.data;
};

// Stock complet
export const getStocks = async (params?: {
  categorie?: string;
  seuil_alerte?: boolean;
}): Promise<Stock[]> => {
  const response = await axios.get(`${API_URL}/stocks`, { params });
  return response.data;
};

// Statistiques
export const getStatsInventaire = async (params?: {
  debut?: string;
  fin?: string;
  categorie?: string;
}): Promise<StatsInventaire> => {
  const response = await axios.get(`${API_URL}/stats`, { params });
  return response.data;
};
