import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import StatsInventaire from '../StatsInventaire';
import { getStatsInventaire } from '../../../services/inventaire';
import { vi } from 'vitest';
import type { StatsInventaire as StatsInventaireType } from '../../../types/inventaire';

declare global {
  namespace Vi {
    interface JestMatchers<T> {
      toBeInTheDocument(): boolean;
    }
  }
}

vi.mock('../../../services/inventaire');

const mockStats: StatsInventaireType = {
  total_produits: 150,
  valeur_totale: 1500000,
  produits_sous_seuil: 3,
  mouvements_recents: 25,
  repartition_categories: {
    'INTRANT': 50,
    'EQUIPEMENT': 30,
    'RECOLTE': 40,
    'EMBALLAGE': 20,
    'PIECE_RECHANGE': 10
  },
  evolution_stock: [
    { date: '2024-01-01', valeur: 1400000 },
    { date: '2024-01-02', valeur: 1500000 }
  ],
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

describe('StatsInventaire', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    (getStatsInventaire as any).mockResolvedValue(mockStats);
  });

  it('affiche les statistiques d\'inventaire', async () => {
    renderWithProviders(<StatsInventaire />);
    
    expect(await screen.findByText('Valeur Totale')).toBeInTheDocument();
    expect(await screen.findByText('1 500 000,00 XAF')).toBeInTheDocument();
    expect(await screen.findByText('150 produits')).toBeInTheDocument();
  });

  it('affiche les variations', async () => {
    renderWithProviders(<StatsInventaire />);
    
    expect(await screen.findByText('+15%')).toBeInTheDocument();
    expect(await screen.findByText('-5%')).toBeInTheDocument();
  });

  it('affiche tous les indicateurs', async () => {
    renderWithProviders(<StatsInventaire />);
    
    expect(await screen.findByText('Taux de Rotation')).toBeInTheDocument();
    expect(await screen.findByText('Alertes')).toBeInTheDocument();
    expect(await screen.findByText('Mouvements')).toBeInTheDocument();
  });

  it('affiche la répartition par catégorie', async () => {
    renderWithProviders(<StatsInventaire />);
    
    expect(await screen.findByText('Intrants')).toBeInTheDocument();
    expect(await screen.findByText('Équipements')).toBeInTheDocument();
    expect(await screen.findByText('Récoltes')).toBeInTheDocument();
  });

  it('affiche l\'évolution du stock', async () => {
    renderWithProviders(<StatsInventaire />);
    
    expect(await screen.findByText('Évolution du Stock')).toBeInTheDocument();
  });

  it('affiche un message de chargement', () => {
    (getStatsInventaire as any).mockReturnValue(new Promise(() => {}));
    renderWithProviders(<StatsInventaire />);
    
    expect(screen.getByText('Chargement...')).toBeInTheDocument();
  });

  it('gère les erreurs de chargement', async () => {
    (getStatsInventaire as any).mockRejectedValue(new Error('Erreur test'));
    renderWithProviders(<StatsInventaire />);
    
    expect(await screen.findByText('Erreur lors du chargement des statistiques')).toBeInTheDocument();
  });
});
