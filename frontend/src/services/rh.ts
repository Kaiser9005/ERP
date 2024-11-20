import { api } from './api';

export interface StatsRH {
  effectif_total: number;
  variation_effectif: {
    valeur: number;
    type: 'hausse' | 'baisse';
  };
  absences_jour: number;
  conges_en_cours: number;
  evaluations_prevues: number;
  formations_en_cours: number;
}

export interface Employe {
  id: string;
  matricule: string;
  nom: string;
  prenom: string;
  poste: string;
  departement: string;
  date_embauche: string;
  statut: 'ACTIF' | 'INACTIF' | 'CONGE';
}

export interface Conge {
  id: string;
  employe_id: string;
  type: string;
  date_debut: string;
  date_fin: string;
  statut: 'EN_ATTENTE' | 'APPROUVE' | 'REFUSE';
  commentaire?: string;
}

export const getStatsRH = async (): Promise<StatsRH> => {
  const response = await api.get('/rh/stats');
  return response.data;
};

export const getEmployes = async (): Promise<Employe[]> => {
  const response = await api.get('/rh/employes');
  return response.data;
};

export const getConges = async (): Promise<Conge[]> => {
  const response = await api.get('/rh/conges');
  return response.data;
};

export const creerEmploye = async (data: Omit<Employe, 'id'>): Promise<Employe> => {
  const response = await api.post('/rh/employes', data);
  return response.data;
};

export const modifierEmploye = async (id: string, data: Partial<Employe>): Promise<Employe> => {
  const response = await api.put(`/rh/employes/${id}`, data);
  return response.data;
};

export const creerConge = async (data: Omit<Conge, 'id'>): Promise<Conge> => {
  const response = await api.post('/rh/conges', data);
  return response.data;
};

export const modifierConge = async (id: string, data: Partial<Conge>): Promise<Conge> => {
  const response = await api.put(`/rh/conges/${id}`, data);
  return response.data;
};
