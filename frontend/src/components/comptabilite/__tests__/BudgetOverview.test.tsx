import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import BudgetOverview from '../BudgetOverview';
import { comptabiliteService } from '../../../services/comptabilite';

// Mock du service
jest.mock('../../../services/comptabilite');

const mockBudgetData = {
  total_prevu: 250000,
  total_realise: 245000,
  categories: {
    '601': {
      libelle: 'Achats matières premières',
      prevu: 100000,
      realise: 98000
    }
  },
  weather_impact: {
    score: 25,
    factors: ['Fortes précipitations', 'Températures élevées'],
    projections: {
      'TRANSPORT': 'Augmentation probable des coûts'
    }
  },
  recommendations: [
    'Optimisation des coûts de transport recommandée'
  ]
};

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: false,
    },
  },
});

const renderWithQuery = (component: React.ReactElement) => {
  return render(
    <QueryClientProvider client={queryClient}>
      {component}
    </QueryClientProvider>
  );
};

describe('BudgetOverview', () => {
  beforeEach(() => {
    // Reset des mocks
    jest.resetAllMocks();
    // Configuration du mock pour getBudgetAnalysis
    (comptabiliteService.getBudgetAnalysis as jest.Mock).mockResolvedValue(mockBudgetData);
  });

  it('affiche le chargement initialement', () => {
    renderWithQuery(<BudgetOverview />);
    expect(screen.getByRole('progressbar')).toBeInTheDocument();
  });

  it('affiche les données budgétaires après chargement', async () => {
    renderWithQuery(<BudgetOverview />);

    await waitFor(() => {
      expect(screen.getByText('Aperçu Budgétaire')).toBeInTheDocument();
    });

    // Vérification des données principales
    expect(screen.getByText('Progression globale')).toBeInTheDocument();
    expect(screen.getByText('98.0%')).toBeInTheDocument();

    // Vérification des montants
    expect(screen.getByText('250 000,00 €')).toBeInTheDocument();
    expect(screen.getByText('245 000,00 €')).toBeInTheDocument();

    // Vérification des catégories
    expect(screen.getByText('Achats matières premières')).toBeInTheDocument();

    // Vérification de l'impact météo
    expect(screen.getByText('Impact météo: 25%')).toBeInTheDocument();
    expect(screen.getByText('Fortes précipitations')).toBeInTheDocument();
    expect(screen.getByText('Températures élevées')).toBeInTheDocument();

    // Vérification des recommandations
    expect(screen.getByText('Optimisation des coûts de transport recommandée')).toBeInTheDocument();
  });

  it('affiche un message d\'erreur en cas d\'échec du chargement', async () => {
    const error = new Error('Erreur de chargement');
    (comptabiliteService.getBudgetAnalysis as jest.Mock).mockRejectedValue(error);

    renderWithQuery(<BudgetOverview />);

    await waitFor(() => {
      expect(screen.getByText('Aucune donnée budgétaire disponible')).toBeInTheDocument();
    });
  });

  it('met à jour les données périodiquement', async () => {
    jest.useFakeTimers();
    renderWithQuery(<BudgetOverview />);

    await waitFor(() => {
      expect(comptabiliteService.getBudgetAnalysis).toHaveBeenCalledTimes(1);
    });

    // Avance le temps de 5 minutes
    jest.advanceTimersByTime(5 * 60 * 1000);

    await waitFor(() => {
      expect(comptabiliteService.getBudgetAnalysis).toHaveBeenCalledTimes(2);
    });

    jest.useRealTimers();
  });
});
