import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import { QueryClient, QueryClientProvider } from 'react-query';
import StatsRH from '../StatsRH';
import { getStatsRH } from '../../../services/rh';

// Mock du service RH
jest.mock('../../../services/rh');
const mockGetStatsRH = getStatsRH as jest.MockedFunction<typeof getStatsRH>;

describe('StatsRH', () => {
  const queryClient = new QueryClient();

  beforeEach(() => {
    mockGetStatsRH.mockResolvedValue({
      effectif_total: 150,
      variation_effectif: {
        valeur: 5,
        type: 'hausse'
      },
      absences_jour: 3,
      conges_en_cours: 8,
      evaluations_prevues: 12,
      formations_en_cours: 4
    });
  });

  it('affiche les statistiques RH correctement', async () => {
    render(
      <QueryClientProvider client={queryClient}>
        <StatsRH />
      </QueryClientProvider>
    );

    // Vérifie le titre
    expect(screen.getByText('Ressources Humaines')).toBeInTheDocument();

    // Vérifie l'effectif total
    expect(await screen.findByText('150')).toBeInTheDocument();

    // Vérifie la variation d'effectif
    expect(screen.getByText('+5% par rapport au mois dernier')).toBeInTheDocument();

    // Vérifie les indicateurs
    expect(screen.getByText('3 Absences')).toBeInTheDocument();
    expect(screen.getByText('8 En congé')).toBeInTheDocument();
    expect(screen.getByText('12 Évaluations')).toBeInTheDocument();
  });

  it('gère correctement une baisse d\'effectif', async () => {
    mockGetStatsRH.mockResolvedValue({
      effectif_total: 145,
      variation_effectif: {
        valeur: 3,
        type: 'baisse'
      },
      absences_jour: 2,
      conges_en_cours: 6,
      evaluations_prevues: 10,
      formations_en_cours: 3
    });

    render(
      <QueryClientProvider client={queryClient}>
        <StatsRH />
      </QueryClientProvider>
    );

    expect(await screen.findByText('-3% par rapport au mois dernier')).toBeInTheDocument();
  });
});
