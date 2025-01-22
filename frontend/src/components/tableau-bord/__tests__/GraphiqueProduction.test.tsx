import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import { QueryClient, QueryClientProvider } from 'react-query';
import GraphiqueProduction from '../GraphiqueProduction';

// Mock de fetch
global.fetch = jest.fn();

// Mock de recharts pour éviter les erreurs de rendu du SVG dans les tests
jest.mock('recharts', () => ({
  ResponsiveContainer: ({ children }: { children: React.ReactNode }) => children,
  LineChart: ({ children }: { children: React.ReactNode }) => <div data-testid="line-chart">{children}</div>,
  Line: () => <div data-testid="line" />,
  XAxis: () => <div data-testid="x-axis" />,
  YAxis: () => <div data-testid="y-axis" />,
  CartesianGrid: () => <div data-testid="cartesian-grid" />,
  Tooltip: () => <div data-testid="tooltip" />,
  Legend: () => <div data-testid="legend" />
}));

describe('GraphiqueProduction', () => {
  const queryClient = new QueryClient();
  const mockDonnees = [
    {
      date: '2024-01-01',
      parcelle_a: 1200,
      parcelle_b: 1000,
      parcelle_c: 800,
      parcelle_d: 900
    },
    {
      date: '2024-01-02',
      parcelle_a: 1300,
      parcelle_b: 1100,
      parcelle_c: 850,
      parcelle_d: 950
    },
    {
      date: '2024-01-03',
      parcelle_a: 1250,
      parcelle_b: 1050,
      parcelle_c: 825,
      parcelle_d: 925
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

  it('affiche le titre et le graphique de production', async () => {
    render(
      <QueryClientProvider client={queryClient}>
        <GraphiqueProduction />
      </QueryClientProvider>
    );

    // Vérifie le titre
    expect(screen.getByText('Production par Parcelle')).toBeInTheDocument();

    // Vérifie les composants du graphique
    expect(await screen.findByTestId('line-chart')).toBeInTheDocument();
    expect(screen.getAllByTestId('line')).toHaveLength(4); // 4 parcelles
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
        <GraphiqueProduction />
      </QueryClientProvider>
    );

    expect(screen.getByText('Chargement des données de production...')).toBeInTheDocument();
  });

  it('gère les erreurs de chargement', async () => {
    (global.fetch as jest.Mock).mockImplementation(() =>
      Promise.reject(new Error('Erreur de chargement'))
    );

    render(
      <QueryClientProvider client={queryClient}>
        <GraphiqueProduction />
      </QueryClientProvider>
    );

    // Le composant devrait afficher le graphique vide avec les axes
    expect(await screen.findByTestId('line-chart')).toBeInTheDocument();
  });
});
