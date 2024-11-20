import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import { QueryClient, QueryClientProvider } from 'react-query';
import StatsFinance from '../StatsFinance';
import { getStatsFinance } from '../../../services/finance';

// Mock du service finance
jest.mock('../../../services/finance', () => ({
  getStatsFinance: jest.fn()
}));

const mockGetStatsFinance = getStatsFinance as jest.MockedFunction<typeof getStatsFinance>;

describe('StatsFinance', () => {
  const queryClient = new QueryClient();

  const mockStats = {
    revenue: 1500000,
    revenueVariation: { value: 5.2, type: 'increase' as const },
    profit: 450000,
    profitVariation: { value: 3.8, type: 'increase' as const },
    cashflow: 750000,
    cashflowVariation: { value: -2.1, type: 'decrease' as const },
    expenses: 1050000,
    expensesVariation: { value: 1.5, type: 'increase' as const }
  };

  beforeEach(() => {
    mockGetStatsFinance.mockResolvedValue(mockStats);
  });

  const renderComponent = () => {
    render(
      <QueryClientProvider client={queryClient}>
        <StatsFinance />
      </QueryClientProvider>
    );
  };

  it('affiche les statistiques financières', async () => {
    renderComponent();

    // Vérifie les titres
    expect(await screen.findByText("Chiffre d'Affaires")).toBeInTheDocument();
    expect(screen.getByText('Bénéfice Net')).toBeInTheDocument();
    expect(screen.getByText('Trésorerie')).toBeInTheDocument();
    expect(screen.getByText('Dépenses')).toBeInTheDocument();

    // Vérifie les valeurs formatées
    expect(screen.getByText('1 500 000 FCFA')).toBeInTheDocument();
    expect(screen.getByText('450 000 FCFA')).toBeInTheDocument();
    expect(screen.getByText('750 000 FCFA')).toBeInTheDocument();
    expect(screen.getByText('1 050 000 FCFA')).toBeInTheDocument();

    // Vérifie les variations
    expect(screen.getByText('5.2%')).toBeInTheDocument();
    expect(screen.getByText('3.8%')).toBeInTheDocument();
    expect(screen.getByText('-2.1%')).toBeInTheDocument();
    expect(screen.getByText('1.5%')).toBeInTheDocument();
  });

  it('gère le cas où les données sont nulles', () => {
    mockGetStatsFinance.mockResolvedValue(null as any);
    renderComponent();

    // Vérifie que les valeurs par défaut sont affichées
    const defaultValues = screen.getAllByText('0 FCFA');
    expect(defaultValues.length).toBeGreaterThan(0);
  });

  it('affiche les variations avec les bonnes couleurs', async () => {
    renderComponent();

    // Attend que les données soient chargées
    await screen.findByText("Chiffre d'Affaires");

    // Vérifie les puces de variation
    const increaseChips = screen.getAllByTestId('increase-chip');
    const decreaseChips = screen.getAllByTestId('decrease-chip');

    expect(increaseChips.length).toBe(3); // Pour revenue, profit et expenses
    expect(decreaseChips.length).toBe(1); // Pour cashflow
  });
});
