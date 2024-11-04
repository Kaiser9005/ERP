import React from 'react';
import { render, screen } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from 'react-query';
import ProductionStats from '../ProductionStats';
import { getProductionStats } from '../../../services/production';

jest.mock('../../../services/production');

const mockStats = {
  total: 1250,
  variation: {
    value: 15,
    type: 'increase'
  },
  rendement: 12.5,
  rendementVariation: {
    value: 5,
    type: 'increase'
  },
  parcellesActives: 8,
  parcellesVariation: {
    value: 0,
    type: 'increase'
  },
  cyclesEnCours: 3,
  cyclesVariation: {
    value: 50,
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

describe('ProductionStats', () => {
  beforeEach(() => {
    (getProductionStats as jest.Mock).mockResolvedValue(mockStats);
  });

  it('affiche les statistiques de production', async () => {
    renderWithProviders(<ProductionStats />);
    
    expect(await screen.findByText('Production Totale')).toBeInTheDocument();
    expect(await screen.findByText('1250')).toBeInTheDocument();
    expect(await screen.findByText('tonnes')).toBeInTheDocument();
  });

  it('affiche les variations', async () => {
    renderWithProviders(<ProductionStats />);
    
    expect(await screen.findByText('15%')).toBeInTheDocument();
    expect(await screen.findByText('5%')).toBeInTheDocument();
  });

  it('affiche tous les indicateurs', async () => {
    renderWithProviders(<ProductionStats />);
    
    expect(await screen.findByText('Rendement Moyen')).toBeInTheDocument();
    expect(await screen.findByText('Parcelles Actives')).toBeInTheDocument();
    expect(await screen.findByText('Cycles en Cours')).toBeInTheDocument();
  });

  it('gère les erreurs de chargement', async () => {
    (getProductionStats as jest.Mock).mockRejectedValue(new Error('Erreur de chargement'));
    
    renderWithProviders(<ProductionStats />);
    
    expect(await screen.findByText('0 tonnes')).toBeInTheDocument();
  });
});