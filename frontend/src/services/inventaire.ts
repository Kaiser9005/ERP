import { api } from './api';
import { 
  Produit, 
  MouvementStock,
  CreateMouvementStock,
  Stock, 
  StatsInventaire
} from '../types/inventaire';

// Produits
export const getProduits = async (): Promise<Produit[]> => {
  const response = await api.get('/api/v1/inventory/produits');
  return response.data;
};

export const getProduit = async (id: string): Promise<Produit> => {
  const response = await api.get(`/api/v1/inventory/produits/${id}`);
  return response.data;
};

export const createProduit = async (produit: Omit<Produit, 'id'>): Promise<Produit> => {
  const response = await api.post('/api/v1/inventory/produits', produit);
  return response.data;
};

export const updateProduit = async (id: string, produit: Partial<Produit>): Promise<Produit> => {
  const response = await api.put(`/api/v1/inventory/produits/${id}`, produit);
  return response.data;
};

export const deleteProduit = async (id: string): Promise<void> => {
  await api.delete(`/api/v1/inventory/produits/${id}`);
};

// Mouvements de stock
export const getMouvements = async (params?: {
  debut?: string;
  fin?: string;
  type?: 'ENTREE' | 'SORTIE' | 'TRANSFERT';
  produit_id?: string;
}): Promise<MouvementStock[]> => {
  const response = await api.get('/api/v1/inventory/mouvements', { params });
  return response.data;
};

export const getMouvementsProduit = async (produitId: string): Promise<MouvementStock[]> => {
  const response = await api.get(`/api/v1/inventory/mouvements/produit/${produitId}`);
  return response.data;
};

export const createMouvement = async (mouvement: CreateMouvementStock): Promise<MouvementStock> => {
  const response = await api.post('/api/v1/inventory/mouvements', mouvement);
  return response.data;
};

// Stock
export const getStocks = async (params?: {
  entrepot_id?: string;
  produit_id?: string;
  seuil_alerte?: boolean;
}): Promise<Stock[]> => {
  const response = await api.get('/api/v1/inventory/stocks', { params });
  return response.data;
};

export const getStockProduit = async (produitId: string): Promise<Stock[]> => {
  const response = await api.get(`/api/v1/inventory/stocks/produit/${produitId}`);
  return response.data;
};

// Statistiques
export const getStatsInventaire = async (params?: {
  debut?: string;
  fin?: string;
  categorie?: string;
}): Promise<StatsInventaire> => {
  const response = await api.get('/api/v1/inventory/stats', { params });
  return response.data;
};

// Alertes
export const getAlertesSeuil = async (): Promise<Produit[]> => {
  const response = await api.get('/api/v1/inventory/alertes/seuil');
  return response.data;
};

// Utilitaires
export const getValeurStock = async (produitId: string): Promise<number> => {
  const response = await api.get(`/api/v1/inventory/stocks/valeur/${produitId}`);
  return response.data.valeur;
};

export const validerMouvement = async (mouvement: CreateMouvementStock): Promise<boolean> => {
  const response = await api.post('/api/v1/inventory/mouvements/valider', mouvement);
  return response.data.valide;
};
