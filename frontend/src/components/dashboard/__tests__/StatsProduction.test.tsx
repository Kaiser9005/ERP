import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import { QueryClient, QueryClientProvider } from 'react-query';
import StatsProduction from '../StatsProduction';
import { getStatsProduction } from '../../../services/production';

// Mock du service de production
jest.mock('../../../services/production');
const mockGetStatsProduction = getStatsProduction as jest.MockedFunction<typeof getStatsProduction>;

describe('StatsProduction', () => {
  const queryClient = new QueryClient();

  beforeEach(() => {
    mockGetStatsProduction.mockResolvedValue({
      total: 1500,
      variation: {
        valeur: 10,
        type: 'hausse'
      },
      parcelles_actives: 50
    });
  });

  it('affiche les statistiques de production correctement', async () => {
    render(
      <QueryClientProvider client={queryClient}>
        <StatsProduction />
      </QueryClientProvider>
    );

    // Vérifie le titre
    expect(screen.getByText('Production')).toBeInTheDocument();

    // Vérifie la production totale
    expect(await screen.findByText('1500 T')).toBeInTheDocument();

    // Vérifie la variation
    expect(screen.getByText('+10% par rapport au mois dernier')).toBeInTheDocument();

    // Vérifie les parcelles actives
    expect(screen.getByText('Parcelles Actives: 50')).toBeInTheDocument();
  });

  it('gère correctement une baisse de production', async () => {
    mockGetStatsProduction.mockResolvedValue({
      total: 1200,
      variation: {
        valeur: 5,
        type: 'baisse'
      },
      parcelles_actives: 45
    });

    render(
      <QueryClientProvider client={queryClient}>
        <StatsProduction />
      </QueryClientProvider>
    );

    expect(await screen.findByText('-5% par rapport au mois dernier')).toBeInTheDocument();
  });
});
