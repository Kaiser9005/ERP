import { api } from '../config/axios';
import { 
  Produit, 
  Stock, 
  MouvementStock,
  StatsInventaire,
  Entrepot,
  InventoryPermissions,
  FiltresInventaire,
  PrevisionStock
} from '../types/inventaire';

// Stats
export const getStatsInventaire = async (filtres?: FiltresInventaire): Promise<StatsInventaire> => {
  const { data } = await api.get<StatsInventaire>('/api/v1/inventory/stats', { params: filtres });
  return data;
};

// Produits
export const getProduits = async (filtres?: FiltresInventaire): Promise<Produit[]> => {
  const { data } = await api.get<Produit[]>('/api/v1/inventory/produits', { params: filtres });
  return data;
};

export const getProduit = async (id: string): Promise<Produit> => {
  const { data } = await api.get<Produit>(`/api/v1/inventory/produits/${id}`);
  return data;
};

export const creerProduit = async (produit: Omit<Produit, 'id'>): Promise<Produit> => {
  const { data } = await api.post<Produit>('/api/v1/inventory/produits', produit);
  return data;
};

export const modifierProduit = async (id: string, produit: Partial<Produit>): Promise<Produit> => {
  const { data } = await api.patch<Produit>(`/api/v1/inventory/produits/${id}`, produit);
  return data;
};

export const supprimerProduit = async (id: string): Promise<void> => {
  await api.delete(`/api/v1/inventory/produits/${id}`);
};

// Stocks
export const getStocks = async (filtres?: FiltresInventaire): Promise<Stock[]> => {
  const { data } = await api.get<Stock[]>('/api/v1/inventory/stocks', { params: filtres });
  return data;
};

export const getStock = async (id: string): Promise<Stock> => {
  const { data } = await api.get<Stock>(`/api/v1/inventory/stocks/${id}`);
  return data;
};

export const modifierStock = async (id: string, stock: Partial<Stock>): Promise<Stock> => {
  const { data } = await api.patch<Stock>(`/api/v1/inventory/stocks/${id}`, stock);
  return data;
};

// Mouvements
export const getMouvements = async (filtres?: FiltresInventaire): Promise<MouvementStock[]> => {
  const { data } = await api.get<MouvementStock[]>('/api/v1/inventory/mouvements', { params: filtres });
  return data;
};

export const getMouvementsProduit = async (produitId: string, filtres?: FiltresInventaire): Promise<MouvementStock[]> => {
  const { data } = await api.get<MouvementStock[]>(`/api/v1/inventory/produits/${produitId}/mouvements`, { params: filtres });
  return data;
};

export const creerMouvement = async (mouvement: Omit<MouvementStock, 'id' | 'date_mouvement'>): Promise<MouvementStock> => {
  const { data } = await api.post<MouvementStock>('/api/v1/inventory/mouvements', mouvement);
  return data;
};

// Entrepôts
export const getEntrepots = async (): Promise<Entrepot[]> => {
  const { data } = await api.get<Entrepot[]>('/api/v1/inventory/entrepots');
  return data;
};

export const creerEntrepot = async (entrepot: Omit<Entrepot, 'id'>): Promise<Entrepot> => {
  const { data } = await api.post<Entrepot>('/api/v1/inventory/entrepots', entrepot);
  return data;
};

// Fournisseurs
export const getFournisseurs = async (): Promise<string[]> => {
  const { data } = await api.get<string[]>('/api/v1/inventory/fournisseurs');
  return data;
};

// Prévisions
export const getPrevisions = async (filtres?: FiltresInventaire): Promise<PrevisionStock[]> => {
  const { data } = await api.get<PrevisionStock[]>('/api/v1/inventory/previsions', { params: filtres });
  return data;
};

// Permissions
export const getPermissions = async (): Promise<InventoryPermissions> => {
  const { data } = await api.get<InventoryPermissions>('/api/v1/inventory/permissions');
  return data;
};

// Alias pour la compatibilité avec le code existant
export const fetchInventoryPermissions = getPermissions;
