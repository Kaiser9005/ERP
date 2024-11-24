import { api } from './api';
import {
  Produit,
  MouvementStock,
  Stock,
  StatsInventaire
} from '../types/inventaire';

export const getProduits = async (): Promise<Produit[]> => {
  const { data } = await api.get<Produit[]>('/api/inventaire/produits');
  return data;
};

export const getProduit = async (id: string): Promise<Produit> => {
  const { data } = await api.get<Produit>(`/api/inventaire/produits/${id}`);
  return data;
};

export const creerProduit = async (produitData: Partial<Produit>): Promise<Produit> => {
  const { data } = await api.post<Produit>('/api/inventaire/produits', produitData);
  return data;
};

export const modifierProduit = async (id: string, produitData: Partial<Produit>): Promise<Produit> => {
  const { data } = await api.put<Produit>(`/api/inventaire/produits/${id}`, produitData);
  return data;
};

export const getMouvements = async (): Promise<MouvementStock[]> => {
  const { data } = await api.get<MouvementStock[]>('/api/inventaire/mouvements');
  return data;
};

export const getProductMovements = async (productId: string): Promise<MouvementStock[]> => {
  const { data } = await api.get<MouvementStock[]>(`/api/inventaire/produits/${productId}/mouvements`);
  return data;
};

export const creerMouvement = async (mouvementData: Partial<MouvementStock>): Promise<MouvementStock> => {
  const { data } = await api.post<MouvementStock>('/api/inventaire/mouvements', mouvementData);
  return data;
};

export const getStatsInventaire = async (): Promise<StatsInventaire> => {
  const { data } = await api.get<StatsInventaire>('/api/inventaire/stats');
  return data;
};

export const getStocks = async (): Promise<Stock[]> => {
  const { data } = await api.get<Stock[]>('/api/inventaire/stocks');
  return data;
};
