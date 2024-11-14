import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import { QueryClient, QueryClientProvider } from 'react-query';
import ProductionStats from '../ProductionStats';
import { getProductionStats } from '../../../services/production';

jest.mock('../../../services/production');

const mockStats = {
  total: 125.5,
  variation: {
    value: 15,
    type: 'increase'
  },
  parcelles_actives: 8
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

describe('ProductionStats', () => {
  beforeEach(() => {
    (getProductionStats as jest.Mock).mockResolvedValue(mockStats);
  });

  it('affiche les statistiques de production', async () => {
    renderWithProviders(<ProductionStats />);
    
    expect(await screen.findByText('Production')).toBeInTheDocument();
    expect(await screen.findByText('125.5 T')).toBeInTheDocument();
    expect(await screen.findByText('Parcelles Actives: 8')).toBeInTheDocument();
  });

  it('affiche la variation positive correctement', async () => {
    renderWithProviders(<ProductionStats />);
    
    const variation = await screen.findByText('+15% par rapport au mois dernier');
    expect(variation).toHaveStyle({ color: expect.stringContaining('success') });
  });

  it('affiche la variation négative correctement', async () => {
    (getProductionStats as jest.Mock).mockResolvedValue({
      ...mockStats,
      variation: { value: 10, type: 'decrease' }
    });

    renderWithProviders(<ProductionStats />);
    
    const variation = await screen.findByText('-10% par rapport au mois dernier');
    expect(variation).toHaveStyle({ color: expect.stringContaining('error') });
  });

  it('gère les erreurs de chargement', async () => {
    (getProductionStats as jest.Mock).mockRejectedValue(new Error('Erreur de chargement'));
    
    renderWithProviders(<ProductionStats />);
    
    expect(await screen.findByText('0 T')).toBeInTheDocument();
  });
});