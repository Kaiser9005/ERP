import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import StatsInventaire from '../../inventaire/StatsInventaire';
import { getStatsInventaire } from '../../../services/inventaire';

jest.mock('../../../services/inventaire');

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
  const mockStats = {
    totalProducts: 150,
    lowStockProducts: 15,
    stockValue: 150000,
    averageProductValue: 1000,
  };

  beforeEach(() => {
    (getStatsInventaire as jest.Mock).mockResolvedValue(mockStats);
  });

  it('affiche les statistiques d\'inventaire', async () => {
    renderWithProviders(<StatsInventaire />);

    expect(await screen.findByText('150')).toBeInTheDocument(); // Total produits
    expect(await screen.findByText('15')).toBeInTheDocument(); // Produits en stock faible
    expect(await screen.findByText('150 000,00 €')).toBeInTheDocument(); // Valeur du stock
    expect(await screen.findByText('1 000,00 €')).toBeInTheDocument(); // Valeur moyenne par produit
  });

  it('gère les erreurs de chargement', async () => {
    (getStatsInventaire as jest.Mock).mockRejectedValue(new Error('Erreur de chargement'));

    renderWithProviders(<StatsInventaire />);

    expect(await screen.findByText('Erreur de chargement des statistiques')).toBeInTheDocument();
  });

  it('affiche un indicateur de chargement', () => {
    (getStatsInventaire as jest.Mock).mockImplementation(() => new Promise(() => {}));

    renderWithProviders(<StatsInventaire />);

    expect(screen.getByRole('progressbar')).toBeInTheDocument();
  });
});
