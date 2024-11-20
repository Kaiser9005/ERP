import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import { QueryClient, QueryClientProvider } from 'react-query';
import ProjectionsFinancieres from '../ProjectionsFinancieres';
import { getProjectionsFinancieres } from '../../../services/finance';

// Mock du service finance
jest.mock('../../../services/finance', () => ({
  getProjectionsFinancieres: jest.fn()
}));

const mockGetProjectionsFinancieres = getProjectionsFinancieres as jest.MockedFunction<typeof getProjectionsFinancieres>;

describe('ProjectionsFinancieres', () => {
  const queryClient = new QueryClient();

  const mockProjections = {
    recettes: [
      { periode: '2024-01', montant: 1500000, impact_meteo: 15 },
      { periode: '2024-02', montant: 1800000, impact_meteo: 20 },
      { periode: '2024-03', montant: 1600000, impact_meteo: 25 }
    ],
    depenses: [
      { periode: '2024-01', montant: 1200000, impact_meteo: 10 },
      { periode: '2024-02', montant: 1300000, impact_meteo: 15 },
      { periode: '2024-03', montant: 1400000, impact_meteo: 20 }
    ],
    facteurs_meteo: [
      'Précipitations abondantes',
      'Température élevée',
      'Humidité importante'
    ]
  };

  beforeEach(() => {
    mockGetProjectionsFinancieres.mockResolvedValue(mockProjections);
  });

  const renderComponent = () => {
    render(
      <QueryClientProvider client={queryClient}>
        <ProjectionsFinancieres />
      </QueryClientProvider>
    );
  };

  it('affiche le titre et les en-têtes', async () => {
    renderComponent();

    await waitFor(() => {
      expect(screen.getByText('Projections Financières (3 mois)')).toBeInTheDocument();
      expect(screen.getByText('Facteurs Météorologiques')).toBeInTheDocument();
      expect(screen.getByText('Projections des Recettes')).toBeInTheDocument();
      expect(screen.getByText('Projections des Dépenses')).toBeInTheDocument();
    });
  });

  it('affiche les facteurs météorologiques', async () => {
    renderComponent();

    await waitFor(() => {
      expect(screen.getByText('Précipitations abondantes')).toBeInTheDocument();
      expect(screen.getByText('Température élevée')).toBeInTheDocument();
      expect(screen.getByText('Humidité importante')).toBeInTheDocument();
    });
  });

  it('affiche les projections de recettes', async () => {
    renderComponent();

    await waitFor(() => {
      // Vérifier les montants
      expect(screen.getByText('1 500 000 XAF')).toBeInTheDocument();
      expect(screen.getByText('1 800 000 XAF')).toBeInTheDocument();
      expect(screen.getByText('1 600 000 XAF')).toBeInTheDocument();

      // Vérifier les impacts météo
      expect(screen.getByText('15%')).toBeInTheDocument();
      expect(screen.getByText('20%')).toBeInTheDocument();
      expect(screen.getByText('25%')).toBeInTheDocument();
    });
  });

  it('affiche les projections de dépenses', async () => {
    renderComponent();

    await waitFor(() => {
      // Vérifier les montants
      expect(screen.getByText('1 200 000 XAF')).toBeInTheDocument();
      expect(screen.getByText('1 300 000 XAF')).toBeInTheDocument();
      expect(screen.getByText('1 400 000 XAF')).toBeInTheDocument();

      // Vérifier les impacts météo
      expect(screen.getByText('10%')).toBeInTheDocument();
      expect(screen.getByText('15%')).toBeInTheDocument();
      expect(screen.getByText('20%')).toBeInTheDocument();
    });
  });

  it('affiche les tendances avec les bonnes couleurs', async () => {
    renderComponent();

    await waitFor(() => {
      // Pour les recettes (hausse = vert)
      const successChips = screen.getAllByTestId('success-chip');
      expect(successChips.length).toBeGreaterThan(0);

      // Pour les dépenses (hausse = rouge)
      const errorChips = screen.getAllByTestId('error-chip');
      expect(errorChips.length).toBeGreaterThan(0);
    });
  });

  it('affiche un indicateur de chargement', () => {
    renderComponent();
    expect(screen.getByRole('progressbar')).toBeInTheDocument();
  });

  it('gère les erreurs de chargement', async () => {
    mockGetProjectionsFinancieres.mockRejectedValueOnce(new Error('Erreur de chargement'));
    renderComponent();

    await waitFor(() => {
      expect(screen.getByText(/Une erreur est survenue/)).toBeInTheDocument();
    });
  });

  it('gère le cas où les données sont vides', async () => {
    mockGetProjectionsFinancieres.mockResolvedValueOnce({
      recettes: [],
      depenses: [],
      facteurs_meteo: []
    });
    renderComponent();

    await waitFor(() => {
      expect(screen.getByText('Projections Financières (3 mois)')).toBeInTheDocument();
      expect(screen.queryByText('1 500 000 XAF')).not.toBeInTheDocument();
    });
  });
});
