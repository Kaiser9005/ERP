import { api } from './api';

export interface Produit {
  id: string;
  code: string;
  nom: string;
  description?: string;
  categorie: string;
  unite_mesure: string;
  prix_unitaire: number;
  quantite_stock: number;
  seuil_alerte: number;
  emplacement?: string;
  specifications?: Record<string, any>;
  date_derniere_maj?: string;
}

export interface MouvementStock {
  id: string;
  produit_id: string;
  type_mouvement: 'ENTREE' | 'SORTIE' | 'TRANSFERT';
  quantite: number;
  date_mouvement: string;
  entrepot_source_id?: string;
  entrepot_destination_id?: string;
  responsable_id: string;
  reference_document?: string;
  notes?: string;
  cout_unitaire?: number;
}

export interface StatsInventaire {
  total_produits: number;
  stock_faible: number;
  valeur_totale: number;
  mouvements: {
    entrees: number;
    sorties: number;
  };
  valeur_stock: {
    valeur: number;
    type: 'hausse' | 'baisse';
  };
  rotation_stock: {
    valeur: number;
    type: 'hausse' | 'baisse';
  };
}

export interface Stock {
  id: string;
  code: string;
  name: string;
  quantity: number;
  unit: string;
  value: number;
  threshold: number;
}

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
