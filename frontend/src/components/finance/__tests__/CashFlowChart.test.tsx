import React from 'react';
import { render, screen } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from 'react-query';
import CashFlowChart from '../CashFlowChart';
import { getCashFlowData } from '../../../services/finance';

jest.mock('../../../services/finance');

const mockData = {
  labels: ['Jan', 'Fév', 'Mar'],
  recettes: [500000, 600000, 550000],
  depenses: [400000, 450000, 425000]
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

describe('CashFlowChart', () => {
  beforeEach(() => {
    (getCashFlowData as jest.Mock).mockResolvedValue(mockData);
  });

  it('affiche le titre du graphique', async () => {
    renderWithProviders(<CashFlowChart />);
    
    expect(await screen.findByText('Flux de Trésorerie')).toBeInTheDocument();
  });

  it('affiche la légende', async () => {
    renderWithProviders(<CashFlowChart />);
    
    expect(await screen.findByText('Recettes')).toBeInTheDocument();
    expect(await screen.findByText('Dépenses')).toBeInTheDocument();
  });

  it('gère les erreurs de chargement', async () => {
    (getCashFlowData as jest.Mock).mockRejectedValue(new Error('Erreur de chargement'));
    
    renderWithProviders(<CashFlowChart />);
    
    expect(screen.queryByRole('graphics-document')).not.toBeInTheDocument();
  });

  it('utilise les bonnes couleurs pour les séries', () => {
    renderWithProviders(<CashFlowChart />);
    
    const canvas = screen.getByRole('img');
    expect(canvas).toBeInTheDocument();
    
    // Vérification des couleurs via les datasets du graphique
    const chart = (canvas as any)._chart;
    expect(chart.data.datasets[0].borderColor).toBe('rgb(46, 125, 50)'); // Recettes
    expect(chart.data.datasets[1].borderColor).toBe('rgb(211, 47, 47)'); // Dépenses
  });
});