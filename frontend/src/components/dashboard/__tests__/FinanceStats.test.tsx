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
  revenueVariation: { valeur: 15, type: 'hausse' },
  expenses: 1200000,
  expensesVariation: { valeur: 10, type: 'baisse' },
  profit: 300000,
  profitVariation: { valeur: 20, type: 'hausse' },
  cashflow: 500000,
  cashflowVariation: { valeur: 5, type: 'hausse' },
  tresorerie: 100000,
  variation_tresorerie: { valeur: 2, type: 'hausse' },
  factures_impayees: 5,
  paiements_prevus: 10
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

    expect(increaseChips).toHaveLength(4); // revenue, profit, cashflow, tresorerie
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
