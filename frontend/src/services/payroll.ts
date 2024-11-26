import axios from 'axios';
import {
  PayrollSlip,
  CreatePayrollRequest,
  UpdatePayrollRequest,
  PayrollStats,
  OvertimeCalculation,
  ContributionsCalculation,
  PayrollPeriodQuery,
  PayrollValidationResponse,
  PayrollDeleteResponse,
} from '../types/payroll';

const BASE_URL = '/api/v1/payroll';

export const payrollService = {
  // Créer une fiche de paie
  create: async (data: CreatePayrollRequest): Promise<PayrollSlip> => {
    const response = await axios.post(BASE_URL, data);
    return response.data;
  },

  // Récupérer une fiche de paie
  getById: async (id: string): Promise<PayrollSlip> => {
    const response = await axios.get(`${BASE_URL}/${id}`);
    return response.data;
  },

  // Lister les fiches de paie d'un contrat
  getByContract: async (contractId: string): Promise<PayrollSlip[]> => {
    const response = await axios.get(`${BASE_URL}/contract/${contractId}`);
    return response.data;
  },

  // Lister les fiches de paie par période
  getByPeriod: async (query: PayrollPeriodQuery): Promise<PayrollSlip[]> => {
    const response = await axios.get(`${BASE_URL}/period`, { params: query });
    return response.data;
  },

  // Mettre à jour une fiche de paie
  update: async (id: string, data: UpdatePayrollRequest): Promise<PayrollSlip> => {
    const response = await axios.patch(`${BASE_URL}/${id}`, data);
    return response.data;
  },

  // Valider une fiche de paie
  validate: async (id: string): Promise<PayrollValidationResponse> => {
    const response = await axios.post(`${BASE_URL}/${id}/validate`);
    return response.data;
  },

  // Supprimer une fiche de paie
  delete: async (id: string): Promise<PayrollDeleteResponse> => {
    const response = await axios.delete(`${BASE_URL}/${id}`);
    return response.data;
  },

  // Obtenir les statistiques
  getStats: async (query: PayrollPeriodQuery): Promise<PayrollStats> => {
    const response = await axios.get(`${BASE_URL}/stats`, { params: query });
    return response.data;
  },

  // Calculer les heures supplémentaires
  calculateOvertime: async (id: string, hours: number): Promise<OvertimeCalculation> => {
    const response = await axios.post(`${BASE_URL}/${id}/calculate-overtime`, { hours });
    return response.data;
  },

  // Calculer les cotisations
  calculateContributions: async (id: string): Promise<ContributionsCalculation> => {
    const response = await axios.post(`${BASE_URL}/${id}/calculate-contributions`);
    return response.data;
  },
};

// Hook personnalisé pour la gestion des erreurs
export const usePayrollError = (error: any): string => {
  if (axios.isAxiosError(error)) {
    switch (error.response?.status) {
      case 400:
        return 'Données de paie invalides';
      case 404:
        return 'Fiche de paie non trouvée';
      case 500:
        return 'Erreur serveur lors du traitement de la paie';
      default:
        return 'Erreur lors de la gestion de la paie';
    }
  }
  return 'Erreur inattendue';
};
