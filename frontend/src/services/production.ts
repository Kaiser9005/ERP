import { api } from './api';

export interface Parcelle {
  id: string;
  code: string;
  surface: number;
  culture: string;
  statut: string;
  date_plantation: string;
  responsable: string;
}

export interface StatsProduction {
  total: number;
  variation: {
    valeur: number;
    type: 'hausse' | 'baisse';
  };
  parcelles_actives: number;
}

export interface EvenementProduction {
  id: string;
  type: string;
  debut: Date;
  fin: Date;
  description: string;
  parcelle_id: string;
}

export const getParcelles = async (): Promise<Parcelle[]> => {
  const response = await api.get('/production/parcelles');
  return response.data;
};

export const getStatsProduction = async (): Promise<StatsProduction> => {
  const response = await api.get('/production/stats');
  return response.data;
};

export const getEvenementsProduction = async (): Promise<EvenementProduction[]> => {
  const response = await api.get('/production/evenements');
  return response.data.map((event: any) => ({
    ...event,
    debut: new Date(event.debut),
    fin: new Date(event.fin)
  }));
};

export const creerParcelle = async (data: Partial<Parcelle>): Promise<Parcelle> => {
  const response = await api.post('/production/parcelles', data);
  return response.data;
};

export const modifierParcelle = async (id: string, data: Partial<Parcelle>): Promise<Parcelle> => {
  const response = await api.put(`/production/parcelles/${id}`, data);
  return response.data;
};
