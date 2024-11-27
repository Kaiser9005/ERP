import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import { QueryClient, QueryClientProvider } from 'react-query';
import StatsInventaire from '../StatsInventaire';
import { getStatsInventaire } from '../../../services/inventaire';
import { vi } from 'vitest';
import type { StatsInventaire as StatsInventaireType } from '../../../types/inventaire';

vi.mock('../../../services/inventaire');

const mockStats: StatsInventaireType = {
  total_produits: 150,
  stock_faible: 3,
  valeur_totale: 1500000,
  mouvements: {
    entrees: 25,
    sorties: 15
  },
  valeur_stock: {
    valeur: 15,
    type: 'hausse'
  },
  rotation_stock: {
    valeur: 5,
    type: 'hausse'
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

describe('StatsInventaire', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    (getStatsInventaire as any).mockResolvedValue(mockStats);
  });

  it('affiche les statistiques d\'inventaire', async () => {
    renderWithProviders(<StatsInventaire />);
    
    expect(await screen.findByText('Valeur Totale')).toBeInTheDocument();
    expect(await screen.findByText('Rotation de Stock')).toBeInTheDocument();
    expect(await screen.findByText('Alertes de Stock')).toBeInTheDocument();
    expect(await screen.findByText('Mouvements')).toBeInTheDocument();
  });

  it('affiche les valeurs correctes', async () => {
    renderWithProviders(<StatsInventaire />);
    
    // Valeur totale
    const valeurTotale = await screen.findByText(/1500000/);
    expect(valeurTotale).toBeInTheDocument();
    
    // Rotation de stock
    const rotation = await screen.findByText(/150/);
    expect(rotation).toBeInTheDocument();
    
    // Alertes
    const alertes = await screen.findByText(/3/);
    expect(alertes).toBeInTheDocument();
    
    // Mouvements
    const mouvements = await screen.findByText(/25/);
    expect(mouvements).toBeInTheDocument();
  });

  it('affiche les variations', async () => {
    renderWithProviders(<StatsInventaire />);
    
    // Variation valeur stock
    const variationValeur = await screen.findByText(/15/);
    expect(variationValeur).toBeInTheDocument();
    
    // Variation rotation
    const variationRotation = await screen.findByText(/5/);
    expect(variationRotation).toBeInTheDocument();
  });

  it('gère le cas où les données sont absentes', () => {
    (getStatsInventaire as any).mockResolvedValue(null);
    renderWithProviders(<StatsInventaire />);
    
    const cards = screen.getAllByRole('article');
    expect(cards).toHaveLength(4);
    
    cards.forEach(card => {
      expect(card).toHaveTextContent('0');
    });
  });
});
