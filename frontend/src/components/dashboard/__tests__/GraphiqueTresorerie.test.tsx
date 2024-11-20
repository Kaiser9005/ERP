import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import { QueryClient, QueryClientProvider } from 'react-query';
import GraphiqueTresorerie from '../GraphiqueTresorerie';

// Mock de fetch
global.fetch = jest.fn();

// Mock de recharts
jest.mock('recharts', () => ({
  ResponsiveContainer: ({ children }: { children: React.ReactNode }) => children,
  AreaChart: ({ children }: { children: React.ReactNode }) => <div data-testid="area-chart">{children}</div>,
  Area: () => <div data-testid="area" />,
  XAxis: () => <div data-testid="x-axis" />,
  YAxis: () => <div data-testid="y-axis" />,
  CartesianGrid: () => <div data-testid="cartesian-grid" />,
  Tooltip: () => <div data-testid="tooltip" />,
  Legend: () => <div data-testid="legend" />
}));

describe('GraphiqueTresorerie', () => {
  const queryClient = new QueryClient();
  const mockDonnees = [
    {
      date: '2024-01-01',
      solde: 5000000,
      entrees: 1000000,
      sorties: 500000
    },
    {
      date: '2024-01-02',
      solde: 5500000,
      entrees: 800000,
      sorties: 300000
    },
    {
      date: '2024-01-03',
      solde: 6000000,
      entrees: 1200000,
      sorties: 700000
    }
  ];

  beforeEach(() => {
    (global.fetch as jest.Mock).mockImplementation(() =>
      Promise.resolve({
        json: () => Promise.resolve(mockDonnees)
      })
    );
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  it('affiche le titre et le graphique de trésorerie', async () => {
    render(
      <QueryClientProvider client={queryClient}>
        <GraphiqueTresorerie />
      </QueryClientProvider>
    );

    // Vérifie le titre
    expect(screen.getByText('Évolution de la Trésorerie')).toBeInTheDocument();

    // Vérifie les composants du graphique
    expect(await screen.findByTestId('area-chart')).toBeInTheDocument();
    expect(screen.getAllByTestId('area')).toHaveLength(3); // solde, entrées, sorties
    expect(screen.getByTestId('x-axis')).toBeInTheDocument();
    expect(screen.getByTestId('y-axis')).toBeInTheDocument();
    expect(screen.getByTestId('cartesian-grid')).toBeInTheDocument();
    expect(screen.getByTestId('tooltip')).toBeInTheDocument();
    expect(screen.getByTestId('legend')).toBeInTheDocument();
  });

  it('affiche un message de chargement', () => {
    (global.fetch as jest.Mock).mockImplementation(() =>
      new Promise(() => {}) // Promise qui ne se résout jamais
    );

    render(
      <QueryClientProvider client={queryClient}>
        <GraphiqueTresorerie />
      </QueryClientProvider>
    );

    expect(screen.getByText('Chargement des données de trésorerie...')).toBeInTheDocument();
  });

  it('gère les erreurs de chargement', async () => {
    (global.fetch as jest.Mock).mockImplementation(() =>
      Promise.reject(new Error('Erreur de chargement'))
    );

    render(
      <QueryClientProvider client={queryClient}>
        <GraphiqueTresorerie />
      </QueryClientProvider>
    );

    // Le composant devrait afficher le graphique vide avec les axes
    expect(await screen.findByTestId('area-chart')).toBeInTheDocument();
  });

  it('formate correctement les montants', () => {
    const montantFormate = new Intl.NumberFormat('fr-FR', {
      style: 'currency',
      currency: 'XAF',
      maximumFractionDigits: 0
    }).format(5000000);

    expect(montantFormate).toBe('5 000 000 XAF');
  });
});
