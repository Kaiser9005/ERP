import { api } from './api';

export interface Stock {
  id: string;
  code: string;
  nom: string;
  quantite: number;
  unite: string;
  valeur: number;
  seuil_alerte: number;
}

export interface Mouvement {
  id: string;
  type: 'ENTREE' | 'SORTIE' | 'TRANSFERT';
  produit: string;
  quantite: number;
  unite: string;
  reference: string;
  date: string;
}

export interface StatsInventaire {
  valeur_totale: number;
  variation_valeur: {
    valeur: number;
    type: 'hausse' | 'baisse';
  };
  taux_rotation: number;
  variation_rotation: {
    valeur: number;
    type: 'hausse' | 'baisse';
  };
  alertes: number;
  variation_alertes: {
    valeur: number;
    type: 'hausse' | 'baisse';
  };
  mouvements: number;
  variation_mouvements: {
    valeur: number;
    type: 'hausse' | 'baisse';
  };
}

export const getStocks = async (): Promise<Stock[]> => {
  const response = await api.get('/inventaire/stocks');
  return response.data;
};

export const getMouvementsRecents = async (): Promise<Mouvement[]> => {
  const response = await api.get('/inventaire/mouvements/recents');
  return response.data;
};

export const getStatsInventaire = async (): Promise<StatsInventaire> => {
  const response = await api.get('/inventaire/stats');
  return response.data;
};

export const creerMouvement = async (data: {
  produitId: string;
  type: string;
  quantite: number;
  reference?: string;
}): Promise<Mouvement> => {
  const response = await api.post('/inventaire/mouvements', data);
  return response.data;
};
