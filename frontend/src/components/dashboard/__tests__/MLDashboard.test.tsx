import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { vi } from 'vitest'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import MLDashboard from '../MLDashboard'
import { dashboardService } from '../../../services/dashboard'

// Mock des services
vi.mock('../../../services/dashboard', () => ({
  dashboardService: {
    getMLPredictions: vi.fn(),
    getCriticalAlerts: vi.fn(),
    getRecommendations: vi.fn()
  }
}))

describe('MLDashboard', () => {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: {
        retry: false
      }
    }
  })

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

  const mockAlerts = [
    { type: 'production', message: 'Alerte Production', priority: 1 },
    { type: 'finance', message: 'Alerte Finance', priority: 2 }
  ]

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

  beforeEach(() => {
    // Configuration des mocks
    vi.mocked(dashboardService.getMLPredictions).mockResolvedValue(mockPredictions)
    vi.mocked(dashboardService.getCriticalAlerts).mockResolvedValue(mockAlerts)
    vi.mocked(dashboardService.getRecommendations).mockResolvedValue(mockRecommendations)
  })

  it('affiche les prédictions ML correctement', async () => {
    render(
      <QueryClientProvider client={queryClient}>
        <MLDashboard />
      </QueryClientProvider>
    )

    // Vérification des prédictions de production
    await waitFor(() => {
      expect(screen.getByText('1200')).toBeInTheDocument() // yield_prediction
      expect(screen.getByText('95%')).toBeInTheDocument() // quality_prediction
    })

    // Vérification des prédictions financières
    expect(screen.getByText('150 000 €')).toBeInTheDocument() // revenue_prediction
    expect(screen.getByText('120 000 €')).toBeInTheDocument() // expense_prediction
    expect(screen.getByText('30 000 €')).toBeInTheDocument() // cash_flow_prediction

    // Vérification des prédictions d'inventaire
    expect(screen.getByText('item_3')).toBeInTheDocument() // reorder_suggestion
    expect(screen.getByText('item_4')).toBeInTheDocument() // reorder_suggestion

    // Vérification des prédictions RH
    expect(screen.getByText('15%')).toBeInTheDocument() // turnover_prediction
    expect(screen.getByText('Developer')).toBeInTheDocument() // hiring_needs
    expect(screen.getByText('Manager')).toBeInTheDocument() // hiring_needs
  })

  it('affiche les alertes critiques correctement', async () => {
    render(
      <QueryClientProvider client={queryClient}>
        <MLDashboard />
      </QueryClientProvider>
    )

    // Vérification des alertes
    await waitFor(() => {
      expect(screen.getByText('Alerte Production')).toBeInTheDocument()
      expect(screen.getByText('Alerte Finance')).toBeInTheDocument()
    })

    // Vérification du tri des alertes par priorité
    const alerts = screen.getAllByTestId('alert-item')
    expect(alerts[0]).toHaveTextContent('Alerte Production') // Priorité 1
    expect(alerts[1]).toHaveTextContent('Alerte Finance') // Priorité 2
  })

  it('affiche les recommandations ML correctement', async () => {
    render(
      <QueryClientProvider client={queryClient}>
        <MLDashboard />
      </QueryClientProvider>
    )

    // Vérification des recommandations
    await waitFor(() => {
      expect(screen.getByText('Optimiser la maintenance')).toBeInTheDocument()
      expect(screen.getByText('Réapprovisionner item_3')).toBeInTheDocument()
    })

    // Vérification des niveaux de confiance
    expect(screen.getByText('85%')).toBeInTheDocument()
    expect(screen.getByText('92%')).toBeInTheDocument()
  })

  it('gère le rafraîchissement des données', async () => {
    render(
      <QueryClientProvider client={queryClient}>
        <MLDashboard />
      </QueryClientProvider>
    )

    // Clic sur le bouton de rafraîchissement
    const refreshButton = screen.getByRole('button', { name: /rafraîchir/i })
    fireEvent.click(refreshButton)

    // Vérification que les services ont été rappelés
    await waitFor(() => {
      expect(dashboardService.getMLPredictions).toHaveBeenCalledTimes(2)
      expect(dashboardService.getCriticalAlerts).toHaveBeenCalledTimes(2)
      expect(dashboardService.getRecommendations).toHaveBeenCalledTimes(2)
    })
  })

  it('gère les erreurs correctement', async () => {
    // Configuration du mock pour simuler une erreur
    vi.mocked(dashboardService.getMLPredictions).mockRejectedValueOnce(new Error('Erreur API'))

    render(
      <QueryClientProvider client={queryClient}>
        <MLDashboard />
      </QueryClientProvider>
    )

    // Vérification du message d'erreur
    await waitFor(() => {
      expect(screen.getByText(/erreur lors du chargement des prédictions/i)).toBeInTheDocument()
    })
  })

  it('permet de filtrer les prédictions par module', async () => {
    render(
      <QueryClientProvider client={queryClient}>
        <MLDashboard />
      </QueryClientProvider>
    )

    // Sélection du filtre Production
    const productionFilter = screen.getByRole('button', { name: /production/i })
    fireEvent.click(productionFilter)

    // Vérification que seules les prédictions de production sont affichées
    await waitFor(() => {
      expect(screen.getByText('1200')).toBeInTheDocument() // yield_prediction
      expect(screen.queryByText('150 000 €')).not.toBeInTheDocument() // revenue_prediction masqué
    })
  })

  it('permet de trier les recommandations par confiance', async () => {
    render(
      <QueryClientProvider client={queryClient}>
        <MLDashboard />
      </QueryClientProvider>
    )

    // Clic sur le bouton de tri
    const sortButton = screen.getByRole('button', { name: /trier par confiance/i })
    fireEvent.click(sortButton)

    // Vérification de l'ordre des recommandations
    const recommendations = screen.getAllByTestId('recommendation-item')
    expect(recommendations[0]).toHaveTextContent('92%') // Plus haute confiance en premier
    expect(recommendations[1]).toHaveTextContent('85%')
  })
})
