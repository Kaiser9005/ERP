/**
 * Service pour les analytics cross-module
 */

import axios from 'axios';
import { format } from 'date-fns';
import type {
  CrossModuleAnalytics,
  ModuleCorrelations,
  ModulePredictions,
  CrossModuleRecommendation,
  HRAnalytics,
  ProductionAnalytics,
  FinanceAnalytics,
  InventoryAnalytics,
  AnalyseMétéo,
  ProjectsAnalytics
} from '../types/analytics_cross_module';

const BASE_URL = '/api/v1/analytics/cross-module';

interface AnalyticsParams {
  date_debut?: Date;
  date_fin?: Date;
}

/**
 * Formate les paramètres de date pour l'API
 */
const formatDateParams = (params?: AnalyticsParams) => {
  if (!params) return {};
  
  const formatted: Record<string, string> = {};
  if (params.date_debut) {
    formatted.date_debut = format(params.date_debut, 'yyyy-MM-dd');
  }
  if (params.date_fin) {
    formatted.date_fin = format(params.date_fin, 'yyyy-MM-dd');
  }
  return formatted;
};

/**
 * Service pour les analytics cross-module
 */
export const analyticsCrossModuleService = {
  /**
   * Récupère les analytics unifiés
   */
  async getUnifiedAnalytics(params?: AnalyticsParams): Promise<CrossModuleAnalytics> {
    const { data } = await axios.get<CrossModuleAnalytics>(
      `${BASE_URL}/unified`,
      { params: formatDateParams(params) }
    );
    return data;
  },

  /**
   * Récupère les corrélations entre modules
   */
  async getCorrelations(params?: AnalyticsParams): Promise<ModuleCorrelations> {
    const { data } = await axios.get<ModuleCorrelations>(
      `${BASE_URL}/correlations`,
      { params: formatDateParams(params) }
    );
    return data;
  },

  /**
   * Récupère les prédictions ML
   */
  async getPredictions(params?: AnalyticsParams): Promise<ModulePredictions> {
    const { data } = await axios.get<ModulePredictions>(
      `${BASE_URL}/predictions`,
      { params: formatDateParams(params) }
    );
    return data;
  },

  /**
   * Récupère les recommandations
   */
  async getRecommendations(params?: AnalyticsParams): Promise<CrossModuleRecommendation[]> {
    const { data } = await axios.get<CrossModuleRecommendation[]>(
      `${BASE_URL}/recommendations`,
      { params: formatDateParams(params) }
    );
    return data;
  },

  /**
   * Récupère l'impact RH
   */
  async getHRImpact(params?: AnalyticsParams): Promise<HRAnalytics> {
    const { data } = await axios.get<HRAnalytics>(
      `${BASE_URL}/hr-impact`,
      { params: formatDateParams(params) }
    );
    return data;
  },

  /**
   * Récupère l'impact production
   */
  async getProductionImpact(params?: AnalyticsParams): Promise<ProductionAnalytics> {
    const { data } = await axios.get<ProductionAnalytics>(
      `${BASE_URL}/production-impact`,
      { params: formatDateParams(params) }
    );
    return data;
  },

  /**
   * Récupère l'impact finance
   */
  async getFinanceImpact(params?: AnalyticsParams): Promise<FinanceAnalytics> {
    const { data } = await axios.get<FinanceAnalytics>(
      `${BASE_URL}/finance-impact`,
      { params: formatDateParams(params) }
    );
    return data;
  },

  /**
   * Récupère l'impact inventaire
   */
  async getInventoryImpact(params?: AnalyticsParams): Promise<InventoryAnalytics> {
    const { data } = await axios.get<InventoryAnalytics>(
      `${BASE_URL}/inventory-impact`,
      { params: formatDateParams(params) }
    );
    return data;
  },

  /**
   * Récupère l'impact météo
   */
  async getWeatherImpact(params?: AnalyticsParams): Promise<AnalyseMétéo> {
    const { data } = await axios.get<AnalyseMétéo>(
      `${BASE_URL}/weather-impact`,
      { params: formatDateParams(params) }
    );
    return data;
  },

  /**
   * Récupère l'impact des projets
   */
  async getProjectsImpact(params?: AnalyticsParams): Promise<ProjectsAnalytics> {
    const { data } = await axios.get<ProjectsAnalytics>(
      `${BASE_URL}/projects-impact`,
      { params: formatDateParams(params) }
    );
    return data;
  }
};

/**
 * Hook React Query pour les analytics cross-module
 */
export const useAnalyticsCrossModule = () => {
  return {
    getUnifiedAnalytics: (params?: AnalyticsParams) => 
      analyticsCrossModuleService.getUnifiedAnalytics(params),
    getCorrelations: (params?: AnalyticsParams) =>
      analyticsCrossModuleService.getCorrelations(params),
    getPredictions: (params?: AnalyticsParams) =>
      analyticsCrossModuleService.getPredictions(params),
    getRecommendations: (params?: AnalyticsParams) =>
      analyticsCrossModuleService.getRecommendations(params),
    getHRImpact: (params?: AnalyticsParams) =>
      analyticsCrossModuleService.getHRImpact(params),
    getProductionImpact: (params?: AnalyticsParams) =>
      analyticsCrossModuleService.getProductionImpact(params),
    getFinanceImpact: (params?: AnalyticsParams) =>
      analyticsCrossModuleService.getFinanceImpact(params),
    getInventoryImpact: (params?: AnalyticsParams) =>
      analyticsCrossModuleService.getInventoryImpact(params),
    getWeatherImpact: (params?: AnalyticsParams) =>
      analyticsCrossModuleService.getWeatherImpact(params),
    getProjectsImpact: (params?: AnalyticsParams) =>
      analyticsCrossModuleService.getProjectsImpact(params)
  };
};

export default analyticsCrossModuleService;
