import { api } from './api';
import { format } from 'date-fns';
import type { ApiResponse } from '../types/common';
import {
  CompteComptable,
  EcritureComptable,
  JournalComptable,
  GrandLivre,
  CompteBalance,
  ComptabiliteStats,
  CompteComptableFormData,
  EcritureComptableFormData,
  TypeCompteComptable,
  StatutEcriture,
  BudgetAnalysis,
  Balance,
  RapportComptable
} from '../types/comptabilite';

const API_BASE = '/api/v1/comptabilite';

// Statistiques et analyses
export const getComptabiliteStats = async (): Promise<ComptabiliteStats> => {
  const response = await api.get<ApiResponse<ComptabiliteStats>>(`${API_BASE}/stats`);
  return response.data.data;
};

export const getBudgetAnalysis = async (periode: string): Promise<BudgetAnalysis> => {
  const response = await api.get<ApiResponse<BudgetAnalysis>>(`${API_BASE}/budget/analysis`, {
    params: { periode }
  });
  return response.data.data;
};

export const getCashFlow = async (days: number = 30) => {
  const response = await api.get<ApiResponse<any>>(`${API_BASE}/cashflow`, {
    params: { days }
  });
  return response.data.data;
};

// Comptes comptables
export const getComptes = async (params?: {
  type_compte?: TypeCompteComptable;
  actif?: boolean;
}): Promise<CompteComptable[]> => {
  const response = await api.get<ApiResponse<CompteComptable[]>>(`${API_BASE}/comptes`, { params });
  return response.data.data;
};

export const getCompte = async (id: string): Promise<CompteComptable> => {
  const response = await api.get<ApiResponse<CompteComptable>>(`${API_BASE}/comptes/${id}`);
  return response.data.data;
};

export const createCompte = async (data: CompteComptableFormData): Promise<CompteComptable> => {
  const response = await api.post<ApiResponse<CompteComptable>>(`${API_BASE}/comptes`, data);
  return response.data.data;
};

export const updateCompte = async (id: string, data: Partial<CompteComptableFormData>): Promise<CompteComptable> => {
  const response = await api.patch<ApiResponse<CompteComptable>>(`${API_BASE}/comptes/${id}`, data);
  return response.data.data;
};

// Écritures comptables
export const getEcritures = async (params?: {
  compte_id?: string;
  journal_id?: string;
  date_debut?: Date;
  date_fin?: Date;
  statut?: StatutEcriture;
}): Promise<EcritureComptable[]> => {
  const formattedParams = {
    ...params,
    date_debut: params?.date_debut ? format(params.date_debut, 'yyyy-MM-dd') : undefined,
    date_fin: params?.date_fin ? format(params.date_fin, 'yyyy-MM-dd') : undefined,
  };
  const response = await api.get<ApiResponse<EcritureComptable[]>>(`${API_BASE}/ecritures`, { params: formattedParams });
  return response.data.data;
};

export const createEcriture = async (data: EcritureComptableFormData): Promise<EcritureComptable> => {
  const response = await api.post<ApiResponse<EcritureComptable>>(`${API_BASE}/ecritures`, data);
  return response.data.data;
};

export const validerEcriture = async (id: string, validee_par_id: string): Promise<EcritureComptable> => {
  const response = await api.post<ApiResponse<EcritureComptable>>(`${API_BASE}/ecritures/${id}/valider`, {
    validee_par_id
  });
  return response.data.data;
};

// Journaux comptables
export const getJournaux = async (params?: {
  type?: string;
  actif?: boolean;
}): Promise<JournalComptable[]> => {
  const response = await api.get<ApiResponse<JournalComptable[]>>(`${API_BASE}/journaux`, { params });
  return response.data.data;
};

export const getJournal = async (id: string): Promise<JournalComptable> => {
  const response = await api.get<ApiResponse<JournalComptable>>(`${API_BASE}/journaux/${id}`);
  return response.data.data;
};

export const createJournal = async (data: Partial<JournalComptable>): Promise<JournalComptable> => {
  const response = await api.post<ApiResponse<JournalComptable>>(`${API_BASE}/journaux`, data);
  return response.data.data;
};

// Rapports
export const getGrandLivre = async (params?: {
  compte_id?: string;
  date_debut?: Date;
  date_fin?: Date;
}): Promise<GrandLivre[]> => {
  const formattedParams = {
    ...params,
    date_debut: params?.date_debut ? format(params.date_debut, 'yyyy-MM-dd') : undefined,
    date_fin: params?.date_fin ? format(params.date_fin, 'yyyy-MM-dd') : undefined,
  };
  const response = await api.get<ApiResponse<GrandLivre[]>>(`${API_BASE}/grand-livre`, { params: formattedParams });
  return response.data.data;
};

export const getBalance = async (params?: {
  date_debut?: Date;
  date_fin?: Date;
  type_compte?: TypeCompteComptable;
}): Promise<CompteBalance[]> => {
  const formattedParams = {
    ...params,
    date_debut: params?.date_debut ? format(params.date_debut, 'yyyy-MM-dd') : undefined,
    date_fin: params?.date_fin ? format(params.date_fin, 'yyyy-MM-dd') : undefined,
  };
  const response = await api.get<ApiResponse<CompteBalance[]>>(`${API_BASE}/balance`, { params: formattedParams });
  return response.data.data;
};

export const getBilan = async (date_fin: Date): Promise<Balance> => {
  const response = await api.get<ApiResponse<Balance>>(`${API_BASE}/bilan`, {
    params: { date_fin: format(date_fin, 'yyyy-MM-dd') }
  });
  return response.data.data;
};

export const getCompteResultat = async (date_debut: Date, date_fin: Date): Promise<RapportComptable> => {
  const response = await api.get<ApiResponse<RapportComptable>>(`${API_BASE}/compte-resultat`, {
    params: {
      date_debut: format(date_debut, 'yyyy-MM-dd'),
      date_fin: format(date_fin, 'yyyy-MM-dd')
    }
  });
  return response.data.data;
};

// Export
export const exporterDonnees = async (params: { type: string; dateDebut: string; dateFin: string; format: string }) => {
  const queryParams = new URLSearchParams({
    type: params.type,
    date_debut: params.dateDebut,
    date_fin: params.dateFin,
    format: params.format
  });
  const response = await api.get<Blob>(`${API_BASE}/export?${queryParams}`, {
    responseType: 'blob'
  });
  return response.data;
};
