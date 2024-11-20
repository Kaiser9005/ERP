import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import { QueryClient, QueryClientProvider } from 'react-query';
import AnalyseBudget from '../AnalyseBudget';
import { getAnalyseBudget } from '../../../services/finance';

// Mock du service finance
jest.mock('../../../services/finance', () => ({
  getAnalyseBudget: jest.fn()
}));

const mockGetAnalyseBudget = getAnalyseBudget as jest.MockedFunction<typeof getAnalyseBudget>;

describe('AnalyseBudget', () => {
  const queryClient = new QueryClient();

  const mockAnalyse = {
    total_prevu: 5000000,
    total_realise: 4500000,
    categories: {
      'Équipement': {
        prevu: 2000000,
        realise: 1800000,
        ecart: -200000,
        ecart_pourcentage: -10
      },
      'Personnel': {
        prevu: 3000000,
        realise: 2700000,
        ecart: -300000,
        ecart_pourcentage: -10
      }
    },
    impact_meteo: {
      score: 15,
      facteurs: ['Précipitations abondantes', 'Température élevée'],
      projections: {
        'Équipement': 'Usure accélérée due aux conditions météo',
        'Personnel': 'Productivité réduite pendant les heures chaudes'
      }
    },
    recommandations: [
      'Prévoir un budget supplémentaire pour la maintenance',
      'Ajuster les horaires de travail'
    ]
  };

  const emptyAnalyse = {
    total_prevu: 0,
    total_realise: 0,
    categories: {},
    impact_meteo: {
      score: 0,
      facteurs: [],
      projections: {}
    },
    recommandations: []
  };

  beforeEach(() => {
    mockGetAnalyseBudget.mockResolvedValue(mockAnalyse);
  });

  const renderComponent = () => {
    render(
      <QueryClientProvider client={queryClient}>
        <AnalyseBudget />
      </QueryClientProvider>
    );
  };

  it('affiche les données globales', async () => {
    renderComponent();

    await waitFor(() => {
      expect(screen.getByText('5 000 000 XAF')).toBeInTheDocument(); // Budget Total
      expect(screen.getByText('4 500 000 XAF')).toBeInTheDocument(); // Réalisé
      expect(screen.getByText('15%')).toBeInTheDocument(); // Impact Météo
    });
  });

  it('affiche le tableau détaillé des catégories', async () => {
    renderComponent();

    await waitFor(() => {
      // En-têtes
      expect(screen.getByText('Catégorie')).toBeInTheDocument();
      expect(screen.getByText('Budget')).toBeInTheDocument();
      expect(screen.getByText('Réalisé')).toBeInTheDocument();
      expect(screen.getByText('Écart')).toBeInTheDocument();

      // Données
      expect(screen.getByText('Équipement')).toBeInTheDocument();
      expect(screen.getByText('Personnel')).toBeInTheDocument();
      expect(screen.getByText('-10%')).toBeInTheDocument();
    });
  });

  it('affiche les impacts météorologiques', async () => {
    renderComponent();

    await waitFor(() => {
      expect(screen.getByText('Impact Météorologique')).toBeInTheDocument();
      expect(screen.getByText('Précipitations abondantes')).toBeInTheDocument();
      expect(screen.getByText('Température élevée')).toBeInTheDocument();
      expect(screen.getByText(/Usure accélérée/)).toBeInTheDocument();
      expect(screen.getByText(/Productivité réduite/)).toBeInTheDocument();
    });
  });

  it('affiche les recommandations', async () => {
    renderComponent();

    await waitFor(() => {
      expect(screen.getByText('Recommandations')).toBeInTheDocument();
      expect(screen.getByText(/budget supplémentaire/)).toBeInTheDocument();
      expect(screen.getByText(/Ajuster les horaires/)).toBeInTheDocument();
    });
  });

  it('affiche un indicateur de chargement', () => {
    renderComponent();
    expect(screen.getByRole('progressbar')).toBeInTheDocument();
  });

  it('gère les erreurs de chargement', async () => {
    mockGetAnalyseBudget.mockRejectedValueOnce(new Error('Erreur de chargement'));
    renderComponent();

    await waitFor(() => {
      expect(screen.getByText(/Une erreur est survenue/)).toBeInTheDocument();
    });
  });

  it('gère le cas où les données sont vides', async () => {
    mockGetAnalyseBudget.mockResolvedValueOnce(emptyAnalyse);
    renderComponent();

    await waitFor(() => {
      expect(screen.getByText('0 XAF')).toBeInTheDocument();
      expect(screen.getByText('0%')).toBeInTheDocument();
    });
  });
});
