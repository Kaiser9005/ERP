import React from 'react';
import { render, screen } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from 'react-query';
import FinanceStats from '../FinanceStats';
import { getFinanceStats } from '../../../services/finance';

jest.mock('../../../services/finance');

const mockStats = {
  recettes: 1500000,
  variation: {
    value: 15,
    type: 'increase'
  },
  solde: 500000
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
    
    expect(await screen.findByText('Finance')).toBeInTheDocument();
    expect(await screen.findByText('1 500 000 FCFA')).toBeInTheDocument();
    expect(await screen.findByText('500 000 FCFA')).toBeInTheDocument();
  });

  it('affiche la variation positive correctement', async () => {
    renderWithProviders(<FinanceStats />);
    
    const variation = await screen.findByText('+15% ce mois');
    expect(variation).toHaveStyle({ color: expect.stringContaining('success') });
  });

  it('affiche la variation négative correctement', async () => {
    (getFinanceStats as jest.Mock).mockResolvedValue({
      ...mockStats,
      variation: { value: 10, type: 'decrease' }
    });

    renderWithProviders(<FinanceStats />);
    
    const variation = await screen.findByText('-10% ce mois');
    expect(variation).toHaveStyle({ color: expect.stringContaining('error') });
  });

  it('affiche le solde avec la bonne couleur', async () => {
    renderWithProviders(<FinanceStats />);
    
    const soldePositif = await screen.findByText('500 000 FCFA');
    expect(soldePositif).toHaveStyle({ color: expect.stringContaining('success') });

    // Test avec un solde négatif
    (getFinanceStats as jest.Mock).mockResolvedValue({
      ...mockStats,
      solde: -100000
    });

    renderWithProviders(<FinanceStats />);
    
    const soldeNegatif = await screen.findByText('-100 000 FCFA');
    expect(soldeNegatif).toHaveStyle({ color: expect.stringContaining('error') });
  });

  it('gère les erreurs de chargement', async () => {
    (getFinanceStats as jest.Mock).mockRejectedValue(new Error('Erreur de chargement'));
    
    renderWithProviders(<FinanceStats />);
    
    expect(await screen.findByText('0 FCFA')).toBeInTheDocument();
  });
});