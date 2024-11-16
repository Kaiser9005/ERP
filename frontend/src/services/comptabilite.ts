import axios from 'axios';
import { format } from 'date-fns';

const API_BASE = '/api/v1/comptabilite';

export interface FinanceStats {
  revenue: number;
  revenueVariation: {
    value: number;
    type: 'increase' | 'decrease';
  };
  expenses: number;
  expensesVariation: {
    value: number;
    type: 'increase' | 'decrease';
  };
  profit: number;
  profitVariation: {
    value: number;
    type: 'increase' | 'decrease';
  };
  cashflow: number;
  cashflowVariation: {
    value: number;
    type: 'increase' | 'decrease';
  };
}

export interface BudgetAnalysis {
  total_prevu: number;
  total_realise: number;
  categories: Record<string, {
    libelle: string;
    prevu: number;
    realise: number;
  }>;
  weather_impact: {
    score: number;
    factors: string[];
    projections: Record<string, string>;
  };
  recommendations: string[];
}

export interface CashFlowData {
  date: string;
  entrees: number;
  sorties: number;
  solde: number;
  prevision: number;
  impact_meteo: number;
}

export interface CompteComptable {
  id: string;
  numero: string;
  libelle: string;
  type_compte: string;
  solde_debit: number;
  solde_credit: number;
  actif: boolean;
  description?: string;
}

export interface EcritureComptable {
  id: string;
  date_ecriture: string;
  numero_piece: string;
  compte_id: string;
  libelle: string;
  debit: number;
  credit: number;
  statut: string;
  journal_id: string;
  periode: string;
}

export interface JournalComptable {
  id: string;
  code: string;
  libelle: string;
  type_journal: string;
  actif: boolean;
  description?: string;
}

class ComptabiliteService {
  // Statistiques et analyses
  async getStats(): Promise<FinanceStats> {
    const response = await axios.get(`${API_BASE}/stats`);
    return response.data;
  }

  async getBudgetAnalysis(periode: string): Promise<BudgetAnalysis> {
    const response = await axios.get(`${API_BASE}/budget/analysis`, {
      params: { periode }
    });
    return response.data;
  }

  async getCashFlow(days: number = 30): Promise<CashFlowData[]> {
    const response = await axios.get(`${API_BASE}/cashflow`, {
      params: { days }
    });
    return response.data;
  }

  // Comptes comptables
  async getComptes(params?: {
    type_compte?: string;
    actif?: boolean;
  }): Promise<CompteComptable[]> {
    const response = await axios.get(`${API_BASE}/comptes`, { params });
    return response.data;
  }

  async getCompte(id: string): Promise<CompteComptable> {
    const response = await axios.get(`${API_BASE}/comptes/${id}`);
    return response.data;
  }

  async createCompte(data: Partial<CompteComptable>): Promise<CompteComptable> {
    const response = await axios.post(`${API_BASE}/comptes`, data);
    return response.data;
  }

  async updateCompte(id: string, data: Partial<CompteComptable>): Promise<CompteComptable> {
    const response = await axios.patch(`${API_BASE}/comptes/${id}`, data);
    return response.data;
  }

  // Écritures comptables
  async getEcritures(params?: {
    compte_id?: string;
    journal_id?: string;
    date_debut?: Date;
    date_fin?: Date;
    statut?: string;
  }): Promise<EcritureComptable[]> {
    const formattedParams = {
      ...params,
      date_debut: params?.date_debut ? format(params.date_debut, 'yyyy-MM-dd') : undefined,
      date_fin: params?.date_fin ? format(params.date_fin, 'yyyy-MM-dd') : undefined,
    };
    const response = await axios.get(`${API_BASE}/ecritures`, { params: formattedParams });
    return response.data;
  }

  async createEcriture(data: Partial<EcritureComptable>): Promise<EcritureComptable> {
    const response = await axios.post(`${API_BASE}/ecritures`, data);
    return response.data;
  }

  async validerEcriture(id: string, validee_par_id: string): Promise<EcritureComptable> {
    const response = await axios.post(`${API_BASE}/ecritures/${id}/valider`, {
      validee_par_id
    });
    return response.data;
  }

  // Journaux comptables
  async getJournaux(params?: {
    type_journal?: string;
    actif?: boolean;
  }): Promise<JournalComptable[]> {
    const response = await axios.get(`${API_BASE}/journaux`, { params });
    return response.data;
  }

  async createJournal(data: Partial<JournalComptable>): Promise<JournalComptable> {
    const response = await axios.post(`${API_BASE}/journaux`, data);
    return response.data;
  }

  // Rapports
  async getGrandLivre(params?: {
    compte_id?: string;
    date_debut?: Date;
    date_fin?: Date;
  }) {
    const formattedParams = {
      ...params,
      date_debut: params?.date_debut ? format(params.date_debut, 'yyyy-MM-dd') : undefined,
      date_fin: params?.date_fin ? format(params.date_fin, 'yyyy-MM-dd') : undefined,
    };
    const response = await axios.get(`${API_BASE}/grand-livre`, { params: formattedParams });
    return response.data;
  }

  async getBalance(params?: {
    date_debut?: Date;
    date_fin?: Date;
  }) {
    const formattedParams = {
      ...params,
      date_debut: params?.date_debut ? format(params.date_debut, 'yyyy-MM-dd') : undefined,
      date_fin: params?.date_fin ? format(params.date_fin, 'yyyy-MM-dd') : undefined,
    };
    const response = await axios.get(`${API_BASE}/balance`, { params: formattedParams });
    return response.data;
  }

  async getBilan(date_fin: Date) {
    const response = await axios.get(`${API_BASE}/bilan`, {
      params: { date_fin: format(date_fin, 'yyyy-MM-dd') }
    });
    return response.data;
  }

  async getCompteResultat(date_debut: Date, date_fin: Date) {
    const response = await axios.get(`${API_BASE}/compte-resultat`, {
      params: {
        date_debut: format(date_debut, 'yyyy-MM-dd'),
        date_fin: format(date_fin, 'yyyy-MM-dd')
      }
    });
    return response.data;
  }
}

export const comptabiliteService = new ComptabiliteService();
