import axios from 'axios';
import { ModuleStats, ModuleType } from '../types/dashboard';

const BASE_URL = '/api/v1/dashboard';

export const DashboardService = {
  /**
   * Récupère les données du dashboard unifié
   */
  async getUnifiedDashboard(): Promise<ModuleStats> {
    try {
      const response = await axios.get(`${BASE_URL}/unified`);
      return response.data;
    } catch (error) {
      console.error('Erreur lors de la récupération des données du dashboard:', error);
      throw error;
    }
  },

  /**
   * Récupère les détails d'un module spécifique
   * @param module - Le module dont on veut récupérer les détails
   */
  async getModuleDetails(module: ModuleType): Promise<any> {
    try {
      const response = await axios.get(`${BASE_URL}/module/${module}`);
      return response.data;
    } catch (error) {
      console.error(`Erreur lors de la récupération des détails du module ${module}:`, error);
      throw error;
    }
  },

  /**
   * Rafraîchit les données d'un module spécifique
   * @param module - Le module à rafraîchir
   */
  async refreshModule(module: ModuleType): Promise<any> {
    try {
      const response = await axios.post(`${BASE_URL}/module/${module}/refresh`);
      return response.data;
    } catch (error) {
      console.error(`Erreur lors du rafraîchissement du module ${module}:`, error);
      throw error;
    }
  },

  /**
   * Récupère les alertes critiques de tous les modules
   */
  async getCriticalAlerts(): Promise<any> {
    try {
      const response = await axios.get(`${BASE_URL}/alerts/critical`);
      return response.data;
    } catch (error) {
      console.error('Erreur lors de la récupération des alertes critiques:', error);
      throw error;
    }
  },

  /**
   * Récupère les prédictions ML pour tous les modules
   */
  async getMLPredictions(): Promise<any> {
    try {
      const response = await axios.get(`${BASE_URL}/predictions`);
      return response.data;
    } catch (error) {
      console.error('Erreur lors de la récupération des prédictions ML:', error);
      throw error;
    }
  },

  /**
   * Met à jour le statut d'une alerte
   * @param alertId - L'ID de l'alerte
   * @param status - Le nouveau statut
   */
  async updateAlertStatus(alertId: string, status: 'acknowledged' | 'resolved'): Promise<any> {
    try {
      const response = await axios.put(`${BASE_URL}/alerts/${alertId}`, { status });
      return response.data;
    } catch (error) {
      console.error(`Erreur lors de la mise à jour du statut de l'alerte ${alertId}:`, error);
      throw error;
    }
  },

  /**
   * Récupère l'historique des activités pour tous les modules
   * @param limit - Nombre d'activités à récupérer
   */
  async getRecentActivities(limit: number = 10): Promise<any> {
    try {
      const response = await axios.get(`${BASE_URL}/activities/recent`, {
        params: { limit }
      });
      return response.data;
    } catch (error) {
      console.error('Erreur lors de la récupération des activités récentes:', error);
      throw error;
    }
  },

  /**
   * Récupère les données de performance pour tous les modules
   */
  async getPerformanceMetrics(): Promise<any> {
    try {
      const response = await axios.get(`${BASE_URL}/performance`);
      return response.data;
    } catch (error) {
      console.error('Erreur lors de la récupération des métriques de performance:', error);
      throw error;
    }
  },

  /**
   * Récupère les recommandations d'optimisation pour tous les modules
   */
  async getOptimizationRecommendations(): Promise<any> {
    try {
      const response = await axios.get(`${BASE_URL}/recommendations`);
      return response.data;
    } catch (error) {
      console.error('Erreur lors de la récupération des recommandations:', error);
      throw error;
    }
  }
};

export default DashboardService;
