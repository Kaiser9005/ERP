import { vi } from 'vitest'
import axios from 'axios'
import { DashboardService } from '../dashboard'

// Mock axios
vi.mock('axios')
const mockedAxios = axios as jest.Mocked<typeof axios>

describe('DashboardService', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  describe('getMLPredictions', () => {
    const mockPredictions = {
      production: {
        yield_prediction: 1200,
        quality_prediction: 0.95,
        maintenance_prediction: ['Machine A', 'Machine C']
      },
      finance: {
        revenue_prediction: 150000,
        expense_prediction: 120000,
        cash_flow_prediction: 30000
      },
      inventory: {
        stock_level_predictions: { item_1: 100, item_2: 50 },
        reorder_suggestions: ['item_3', 'item_4'],
        optimal_quantities: { item_1: 150, item_2: 75 }
      },
      hr: {
        turnover_prediction: 0.15,
        hiring_needs: ['Developer', 'Manager'],
        training_recommendations: ['Python', 'Leadership']
      }
    }

    it('récupère les prédictions ML avec succès', async () => {
      mockedAxios.get.mockResolvedValueOnce({ data: mockPredictions })
      
      const result = await DashboardService.getMLPredictions()
      
      expect(result).toEqual(mockPredictions)
      expect(mockedAxios.get).toHaveBeenCalledWith('/api/v1/dashboard/predictions')
    })

    it('gère les erreurs lors de la récupération des prédictions', async () => {
      const error = new Error('Erreur API')
      mockedAxios.get.mockRejectedValueOnce(error)
      
      await expect(DashboardService.getMLPredictions()).rejects.toThrow('Erreur API')
    })
  })

  describe('getCriticalAlerts', () => {
    const mockAlerts = [
      { type: 'production', message: 'Alerte Production', priority: 1 },
      { type: 'finance', message: 'Alerte Finance', priority: 2 }
    ]

    it('récupère les alertes critiques avec succès', async () => {
      mockedAxios.get.mockResolvedValueOnce({ data: mockAlerts })
      
      const result = await DashboardService.getCriticalAlerts()
      
      expect(result).toEqual(mockAlerts)
      expect(mockedAxios.get).toHaveBeenCalledWith('/api/v1/dashboard/alerts/critical')
    })

    it('gère les erreurs lors de la récupération des alertes', async () => {
      const error = new Error('Erreur API')
      mockedAxios.get.mockRejectedValueOnce(error)
      
      await expect(DashboardService.getCriticalAlerts()).rejects.toThrow('Erreur API')
    })
  })

  describe('getOptimizationRecommendations', () => {
    const mockRecommendations = [
      {
        module: 'production',
        action: 'Optimiser la maintenance',
        confidence: 0.85
      },
      {
        module: 'inventory',
        action: 'Réapprovisionner item_3',
        confidence: 0.92
      }
    ]

    it('récupère les recommandations avec succès', async () => {
      mockedAxios.get.mockResolvedValueOnce({ data: mockRecommendations })
      
      const result = await DashboardService.getOptimizationRecommendations()
      
      expect(result).toEqual(mockRecommendations)
      expect(mockedAxios.get).toHaveBeenCalledWith('/api/v1/dashboard/recommendations')
    })

    it('gère les erreurs lors de la récupération des recommandations', async () => {
      const error = new Error('Erreur API')
      mockedAxios.get.mockRejectedValueOnce(error)
      
      await expect(DashboardService.getOptimizationRecommendations()).rejects.toThrow('Erreur API')
    })
  })

  describe('updateAlertStatus', () => {
    const alertId = 'alert123'
    const status = 'acknowledged' as const

    it('met à jour le statut d\'une alerte avec succès', async () => {
      const mockResponse = { success: true }
      mockedAxios.put.mockResolvedValueOnce({ data: mockResponse })
      
      const result = await DashboardService.updateAlertStatus(alertId, status)
      
      expect(result).toEqual(mockResponse)
      expect(mockedAxios.put).toHaveBeenCalledWith(
        `/api/v1/dashboard/alerts/${alertId}`,
        { status }
      )
    })

    it('gère les erreurs lors de la mise à jour du statut', async () => {
      const error = new Error('Erreur API')
      mockedAxios.put.mockRejectedValueOnce(error)
      
      await expect(DashboardService.updateAlertStatus(alertId, status))
        .rejects.toThrow('Erreur API')
    })
  })

  describe('getUnifiedDashboard', () => {
    const mockUnifiedData = {
      modules: {
        production: { /* ... */ },
        finance: { /* ... */ },
        inventory: { /* ... */ },
        hr: { /* ... */ }
      },
      alerts: [],
      predictions: {},
      timestamp: '2024-01-01T00:00:00Z'
    }

    it('récupère les données unifiées avec succès', async () => {
      mockedAxios.get.mockResolvedValueOnce({ data: mockUnifiedData })
      
      const result = await DashboardService.getUnifiedDashboard()
      
      expect(result).toEqual(mockUnifiedData)
      expect(mockedAxios.get).toHaveBeenCalledWith('/api/v1/dashboard/unified')
    })

    it('gère les erreurs lors de la récupération des données unifiées', async () => {
      const error = new Error('Erreur API')
      mockedAxios.get.mockRejectedValueOnce(error)
      
      await expect(DashboardService.getUnifiedDashboard()).rejects.toThrow('Erreur API')
    })
  })

  describe('getModuleDetails', () => {
    const mockModuleDetails = {
      stats: { /* ... */ },
      alerts: [],
      predictions: {},
      recommendations: []
    }

    it('récupère les détails d\'un module avec succès', async () => {
      mockedAxios.get.mockResolvedValueOnce({ data: mockModuleDetails })
      
      const result = await DashboardService.getModuleDetails('production')
      
      expect(result).toEqual(mockModuleDetails)
      expect(mockedAxios.get).toHaveBeenCalledWith('/api/v1/dashboard/module/production')
    })

    it('gère les erreurs lors de la récupération des détails', async () => {
      const error = new Error('Erreur API')
      mockedAxios.get.mockRejectedValueOnce(error)
      
      await expect(DashboardService.getModuleDetails('production'))
        .rejects.toThrow('Erreur API')
    })
  })
})
