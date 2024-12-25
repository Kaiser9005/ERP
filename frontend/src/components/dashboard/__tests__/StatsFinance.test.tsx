import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import { QueryClient, QueryClientProvider } from 'react-query';
import StatsFinance from '../StatsFinance';
import { getStatsFinance } from '../../../services/finance';

// Mock du service finance
jest.mock('../../../services/finance');
const mockGetStatsFinance = getStatsFinance as jest.MockedFunction<typeof getStatsFinance>;

describe('StatsFinance', () => {
  const queryClient = new QueryClient();

  beforeEach(() => {
    mockGetStatsFinance.mockResolvedValue({
      tresorerie: 15000000,
      variation_tresorerie: {
        valeur: 10,
        type: 'hausse'
      },
      factures_impayees: 5,
      paiements_prevus: 8,
      budget_mensuel: 20000000,
      depenses_mois: 18000000
    });
  });

  it('affiche les statistiques financières correctement', async () => {
    render(
      <QueryClientProvider client={queryClient}>
        <StatsFinance />
      </QueryClientProvider>
    );

    // Vérifie le titre
    expect(screen.getByText('Finance')).toBeInTheDocument();

    // Vérifie la trésorerie
    expect(await screen.findByText('15 000 000 XAF')).toBeInTheDocument();

    // Vérifie la variation
    expect(screen.getByText('+10% par rapport au mois dernier')).toBeInTheDocument();

    // Vérifie les factures et paiements
    expect(screen.getByText('5 Factures impayées')).toBeInTheDocument();
    expect(screen.getByText('8 Paiements prévus')).toBeInTheDocument();
  });

  it('gère correctement une baisse de trésorerie', async () => {
    mockGetStatsFinance.mockResolvedValue({
      tresorerie: 12000000,
      variation_tresorerie: {
        valeur: 5,
        type: 'baisse'
      },
      factures_impayees: 3,
      paiements_prevus: 6,
      budget_mensuel: 20000000,
      depenses_mois: 19000000
    });

    render(
      <QueryClientProvider client={queryClient}>
        <StatsFinance />
      </QueryClientProvider>
    );

    expect(await screen.findByText('-5% par rapport au mois dernier')).toBeInTheDocument();
  });

  it('gère correctement les données manquantes', async () => {
    mockGetStatsFinance.mockResolvedValue({});

    render(
      <QueryClientProvider client={queryClient}>
        <StatsFinance />
      </QueryClientProvider>
    );

    // Vérifie que le composant affiche des valeurs par défaut
    expect(screen.getByText('Finance')).toBeInTheDocument();
    expect(await screen.findByText('N/A')).toBeInTheDocument();
    expect(screen.queryByText(/par rapport au mois dernier/)).not.toBeInTheDocument();
    expect(screen.queryByText(/Factures impayées/)).not.toBeInTheDocument();
    expect(screen.queryByText(/Paiements prévus/)).not.toBeInTheDocument();
  });
});
