import React from 'react';
import { render, screen } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from 'react-query';
import InventoryStats from '../InventoryStats';
import { getInventoryStats } from '../../../services/inventory';

jest.mock('../../../services/inventory');

const mockStats = {
  valeur_totale: 1500000,
  alertes: 3,
  mouvements_jour: 12
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
    
    expect(await screen.findByText('Inventaire')).toBeInTheDocument();
    expect(await screen.findByText('1 500 000 FCFA')).toBeInTheDocument();
  });

  it('affiche les alertes et mouvements', async () => {
    renderWithProviders(<InventoryStats />);
    
    expect(await screen.findByText('3 Alertes')).toBeInTheDocument();
    expect(await screen.findByText('12 Mouvements')).toBeInTheDocument();
  });

  it('utilise les bonnes couleurs pour les indicateurs', async () => {
    renderWithProviders(<InventoryStats />);
    
    const alerteChip = await screen.findByText('3 Alertes');
    const mouvementChip = await screen.findByText('12 Mouvements');
    
    expect(alerteChip).toHaveClass('MuiChip-colorError');
    expect(mouvementChip).toHaveClass('MuiChip-colorInfo');
  });

  it('gère les erreurs de chargement', async () => {
    (getInventoryStats as jest.Mock).mockRejectedValue(new Error('Erreur de chargement'));
    
    renderWithProviders(<InventoryStats />);
    
    expect(await screen.findByText('0 FCFA')).toBeInTheDocument();
    expect(await screen.findByText('0 Alertes')).toBeInTheDocument();
  });
});