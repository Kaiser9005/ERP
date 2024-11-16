import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import FinanceStats from '../../finance/FinanceStats';
import { getFinanceStats } from '../../../services/finance';
import { FinanceStats as FinanceStatsType } from '../../../types/finance';

jest.mock('../../../services/finance');

const mockStats: FinanceStatsType = {
  revenue: 1500000,
  revenueVariation: { value: 15, type: 'increase' },
  expenses: 1200000,
  expensesVariation: { value: 10, type: 'decrease' },
  profit: 300000,
  profitVariation: { value: 20, type: 'increase' },
  cashflow: 500000,
  cashflowVariation: { value: 5, type: 'increase' }
};

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: false,
    },
  },
});

const renderWithProviders = (component: React.ReactElement) => {
  return render(
    <QueryClientProvider client={queryClient}>
      {component}
    </QueryClientProvider>
  );
};

describe('FinanceStats', () => {
  beforeEach(() => {
    (getFinanceStats as jest.Mock).mockResolvedValue(mockStats);
  });

  it('affiche les statistiques financières', async () => {
    renderWithProviders(<FinanceStats />);
    
    // Vérification des valeurs principales
    expect(await screen.findByText('1 500 000 FCFA')).toBeInTheDocument(); // Chiffre d'affaires
    expect(await screen.findByText('300 000 FCFA')).toBeInTheDocument(); // Bénéfice
    expect(await screen.findByText('500 000 FCFA')).toBeInTheDocument(); // Trésorerie
    expect(await screen.findByText('1 200 000 FCFA')).toBeInTheDocument(); // Dépenses
  });

  it('affiche les variations correctement', async () => {
    renderWithProviders(<FinanceStats />);
    
    // Vérification des variations
    const increaseChips = await screen.findAllByTestId('increase-chip');
    const decreaseChips = await screen.findAllByTestId('decrease-chip');

    expect(increaseChips).toHaveLength(3); // revenue, profit, cashflow
    expect(decreaseChips).toHaveLength(1); // expenses
  });

  it('gère les variations positives et négatives', async () => {
    renderWithProviders(<FinanceStats />);
    
    // Vérification des variations spécifiques
    const revenueVariation = await screen.findByText('15.0%');
    const expensesVariation = await screen.findByText('10.0%');
    
    expect(revenueVariation).toBeInTheDocument();
    expect(expensesVariation).toBeInTheDocument();
  });

  it('gère les erreurs de chargement', async () => {
    (getFinanceStats as jest.Mock).mockRejectedValue(new Error('Erreur de chargement'));
    
    renderWithProviders(<FinanceStats />);
    
    // Vérification du message d'erreur
    const errorMessage = await screen.findByText('Impossible de charger les statistiques financières');
    expect(errorMessage).toBeInTheDocument();
  });

  it('affiche un état de chargement initial', () => {
    // Mock d'une requête en attente
    (getFinanceStats as jest.Mock).mockReturnValue(new Promise(() => {}));

    renderWithProviders(<FinanceStats />);
    
    // Vérification des indicateurs de chargement
    const loadingIndicators = screen.getAllByRole('progressbar');
    expect(loadingIndicators).toHaveLength(4);
  });
});
