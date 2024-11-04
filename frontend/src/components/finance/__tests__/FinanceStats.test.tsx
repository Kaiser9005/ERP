import React from 'react';
import { render, screen } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from 'react-query';
import FinanceStats from '../FinanceStats';
import { getFinanceStats } from '../../../services/finance';

jest.mock('../../../services/finance');

const mockStats = {
  revenue: 1500000,
  revenueVariation: {
    value: 15,
    type: 'increase'
  },
  profit: 300000,
  profitVariation: {
    value: 5,
    type: 'decrease'
  },
  cashflow: 500000,
  cashflowVariation: {
    value: 10,
    type: 'increase'
  },
  expenses: 1200000,
  expensesVariation: {
    value: 8,
    type: 'increase'
  }
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
    
    expect(await screen.findByText('Chiffre d\'Affaires')).toBeInTheDocument();
    expect(await screen.findByText('1 500 000')).toBeInTheDocument();
    expect(await screen.findByText('FCFA')).toBeInTheDocument();
  });

  it('affiche les variations', async () => {
    renderWithProviders(<FinanceStats />);
    
    expect(await screen.findByText('15%')).toBeInTheDocument();
    expect(await screen.findByText('5%')).toBeInTheDocument();
  });

  it('affiche tous les indicateurs', async () => {
    renderWithProviders(<FinanceStats />);
    
    expect(await screen.findByText('Bénéfice Net')).toBeInTheDocument();
    expect(await screen.findByText('Trésorerie')).toBeInTheDocument();
    expect(await screen.findByText('Dépenses')).toBeInTheDocument();
  });

  it('gère les erreurs de chargement', async () => {
    (getFinanceStats as jest.Mock).mockRejectedValue(new Error('Erreur de chargement'));
    
    renderWithProviders(<FinanceStats />);
    
    expect(await screen.findByText('0 FCFA')).toBeInTheDocument();
  });
});