import React from 'react';
import { render, screen } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from 'react-query';
import InventoryStats from '../InventoryStats';
import { getInventoryStats } from '../../../services/inventory';

jest.mock('../../../services/inventory');

const mockStats = {
  totalValue: 1500000,
  valueVariation: {
    value: 15,
    type: 'increase'
  },
  turnoverRate: 12,
  turnoverVariation: {
    value: 5,
    type: 'decrease'
  },
  alerts: 3,
  alertsVariation: {
    value: 50,
    type: 'increase'
  },
  movements: 25,
  movementsVariation: {
    value: 10,
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

describe('InventoryStats', () => {
  beforeEach(() => {
    (getInventoryStats as jest.Mock).mockResolvedValue(mockStats);
  });

  it('affiche les statistiques d\'inventaire', async () => {
    renderWithProviders(<InventoryStats />);
    
    expect(await screen.findByText('Valeur Totale')).toBeInTheDocument();
    expect(await screen.findByText('1 500 000')).toBeInTheDocument();
    expect(await screen.findByText('FCFA')).toBeInTheDocument();
  });

  it('affiche les variations', async () => {
    renderWithProviders(<InventoryStats />);
    
    expect(await screen.findByText('15%')).toBeInTheDocument();
    expect(await screen.findByText('5%')).toBeInTheDocument();
  });

  it('affiche tous les indicateurs', async () => {
    renderWithProviders(<InventoryStats />);
    
    expect(await screen.findByText('Rotation Stock')).toBeInTheDocument();
    expect(await screen.findByText('Alertes Stock')).toBeInTheDocument();
    expect(await screen.findByText('Mouvements')).toBeInTheDocument();
  });

  it('gère les erreurs de chargement', async () => {
    (getInventoryStats as jest.Mock).mockRejectedValue(new Error('Erreur de chargement'));
    
    renderWithProviders(<InventoryStats />);
    
    expect(await screen.findByText('Erreur de chargement des statistiques')).toBeInTheDocument();
  });
});