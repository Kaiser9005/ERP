import { api } from './api';
import {
  Produit,
  MouvementStock,
  Stock,
  StatsInventaire,
  FiltresInventaire,
  PrevisionStock
} from '../types/inventaire';
import { formatQueryParams } from '../utils/format';

export const getProduits = async (): Promise<Produit[]> => {
  const { data } = await api.get<Produit[]>('/api/inventaire/produits');
  return data;
};

export const getProduit = async (id: string): Promise<Produit> => {
  const { data } = await api.get<Produit>(`/api/inventaire/produits/${id}`);
  return data;
};

export const verifierCodeUnique = async (code: string): Promise<boolean> => {
  try {
    const { data } = await api.get<{ exists: boolean }>(`/api/inventaire/produits/verifier-code/${code}`);
    return !data.exists;
  } catch (error) {
    return false;
  }
};

export const creerProduit = async (produitData: Partial<Produit>): Promise<Produit> => {
  const { data } = await api.post<Produit>('/api/inventaire/produits', produitData);
  return data;
};

export const modifierProduit = async (id: string, produitData: Partial<Produit>): Promise<Produit> => {
  const { data } = await api.put<Produit>(`/api/inventaire/produits/${id}`, produitData);
  return data;
};

export const getMouvements = async (filtres?: FiltresInventaire): Promise<MouvementStock[]> => {
  const params = filtres ? formatQueryParams(filtres) : '';
  const { data } = await api.get<MouvementStock[]>(`/api/inventaire/mouvements${params}`);
  return data;
};

export const getProductMovements = async (productId: string, filtres?: FiltresInventaire): Promise<MouvementStock[]> => {
  const params = filtres ? formatQueryParams(filtres) : '';
  const { data } = await api.get<MouvementStock[]>(`/api/inventaire/produits/${productId}/mouvements${params}`);
  return data;
};

export const creerMouvement = async (mouvementData: Partial<MouvementStock>): Promise<MouvementStock> => {
  const { data } = await api.post<MouvementStock>('/api/inventaire/mouvements', mouvementData);
  return data;
};

export const getStatsInventaire = async (filtres?: FiltresInventaire): Promise<StatsInventaire> => {
  const params = filtres ? formatQueryParams(filtres) : '';
  const { data } = await api.get<StatsInventaire>(`/api/inventaire/stats${params}`);
  return data;
};

export const getStocks = async (filtres?: FiltresInventaire): Promise<(Stock & { produit: Produit })[]> => {
  const params = filtres ? formatQueryParams(filtres) : '';
  const { data } = await api.get<(Stock & { produit: Produit })[]>(`/api/inventaire/stocks${params}`);
  return data;
};

export const getFournisseurs = async (): Promise<string[]> => {
  const { data } = await api.get<string[]>('/api/inventaire/fournisseurs');
  return data;
};

export const getPrevisions = async (filtres?: FiltresInventaire): Promise<PrevisionStock[]> => {
  const params = filtres ? formatQueryParams(filtres) : '';
  const { data } = await api.get<PrevisionStock[]>(`/api/inventaire/previsions${params}`);
  return data;
};

export const getTendances = async (filtres?: FiltresInventaire): Promise<{
  date: string;
  entrees: number;
  sorties: number;
}[]> => {
  const params = filtres ? formatQueryParams(filtres) : '';
  const { data } = await api.get<{
    date: string;
    entrees: number;
    sorties: number;
  }[]>(`/api/inventaire/tendances${params}`);
  return data;
};
