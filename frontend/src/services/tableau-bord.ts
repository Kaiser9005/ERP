import axios from 'axios';
import { StatsModule, TypeModule } from '../types/tableau-bord';

const BASE_URL = '/api/v1/dashboard';

export const ServiceTableauBord = {
  /**
   * Récupère les données du tableau de bord unifié
   */
  async getTableauBordUnifie(): Promise<StatsModule> {
    try {
      const response = await axios.get(`${BASE_URL}/unified`);
      return response.data;
    } catch (error) {
      console.error('Erreur lors de la récupération des données du tableau de bord:', error);
      throw error;
    }
  },

  /**
   * Récupère les détails d'un module spécifique
   * @param module - Le module dont on veut récupérer les détails
   */
  async getDetailsModule(module: TypeModule): Promise<any> {
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
  async rafraichirModule(module: TypeModule): Promise<any> {
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
  async getAlertesCritiques(): Promise<any> {
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
  async getPredictionsML(): Promise<any> {
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
   * @param alerteId - L'ID de l'alerte
   * @param statut - Le nouveau statut
   */
  async mettreAJourStatutAlerte(alerteId: string, statut: 'reconnue' | 'resolue'): Promise<any> {
    try {
      const response = await axios.put(`${BASE_URL}/alerts/${alerteId}`, { status: statut });
      return response.data;
    } catch (error) {
      console.error(`Erreur lors de la mise à jour du statut de l'alerte ${alerteId}:`, error);
      throw error;
    }
  },

  /**
   * Récupère l'historique des activités pour tous les modules
   * @param limite - Nombre d'activités à récupérer
   */
  async getActivitesRecentes(limite: number = 10): Promise<any> {
    try {
      const response = await axios.get(`${BASE_URL}/activities/recent`, {
        params: { limit: limite }
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
  async getMetriquesPerformance(): Promise<any> {
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
  async getRecommandationsOptimisation(): Promise<any> {
    try {
      const response = await axios.get(`${BASE_URL}/recommendations`);
      return response.data;
    } catch (error) {
      console.error('Erreur lors de la récupération des recommandations:', error);
      throw error;
    }
  }
};

export default ServiceTableauBord;