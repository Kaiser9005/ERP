import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import { QueryClient, QueryClientProvider } from 'react-query';
import { BrowserRouter } from 'react-router-dom';
import PageFinance from '../PageFinance';

// Mock des composants enfants
jest.mock('../StatsFinance', () => {
  return function MockStatsFinance() {
    return <div data-testid="stats-finance">Stats Finance</div>;
  };
});

jest.mock('../GraphiqueTresorerie', () => {
  return function MockGraphiqueTresorerie() {
    return <div data-testid="graphique-tresorerie">Graphique Trésorerie</div>;
  };
});

jest.mock('../VueBudget', () => {
  return function MockVueBudget() {
    return <div data-testid="vue-budget">Vue Budget</div>;
  };
});

jest.mock('../AnalyseBudget', () => {
  return function MockAnalyseBudget() {
    return <div data-testid="analyse-budget">Analyse Budget</div>;
  };
});

jest.mock('../ProjectionsFinancieres', () => {
  return function MockProjectionsFinancieres() {
    return <div data-testid="projections-financieres">Projections Financières</div>;
  };
});

jest.mock('../ListeTransactions', () => {
  return function MockListeTransactions() {
    return <div data-testid="liste-transactions">Liste Transactions</div>;
  };
});

describe('PageFinance', () => {
  const queryClient = new QueryClient();

  const renderComponent = () => {
    render(
      <BrowserRouter>
        <QueryClientProvider client={queryClient}>
          <PageFinance />
        </QueryClientProvider>
      </BrowserRouter>
    );
  };

  it('affiche le titre et le sous-titre', () => {
    renderComponent();
    expect(screen.getByText('Finance')).toBeInTheDocument();
    expect(screen.getByText('Gestion financière et trésorerie')).toBeInTheDocument();
  });

  it('affiche le bouton Nouvelle Transaction', () => {
    renderComponent();
    expect(screen.getByText('Nouvelle Transaction')).toBeInTheDocument();
  });

  it('affiche les statistiques financières', () => {
    renderComponent();
    expect(screen.getByTestId('stats-finance')).toBeInTheDocument();
  });

  it('affiche tous les onglets', () => {
    renderComponent();
    expect(screen.getByText('Tableau de Bord')).toBeInTheDocument();
    expect(screen.getByText('Analyse Budgétaire')).toBeInTheDocument();
    expect(screen.getByText('Projections')).toBeInTheDocument();
    expect(screen.getByText('Transactions')).toBeInTheDocument();
  });

  it('affiche le tableau de bord par défaut', () => {
    renderComponent();
    expect(screen.getByTestId('graphique-tresorerie')).toBeInTheDocument();
    expect(screen.getByTestId('vue-budget')).toBeInTheDocument();
  });

  it('navigue vers l\'analyse budgétaire', async () => {
    renderComponent();
    fireEvent.click(screen.getByText('Analyse Budgétaire'));
    
    await waitFor(() => {
      expect(screen.getByTestId('analyse-budget')).toBeInTheDocument();
      expect(screen.queryByTestId('graphique-tresorerie')).not.toBeInTheDocument();
    });
  });

  it('navigue vers les projections', async () => {
    renderComponent();
    fireEvent.click(screen.getByText('Projections'));
    
    await waitFor(() => {
      expect(screen.getByTestId('projections-financieres')).toBeInTheDocument();
      expect(screen.queryByTestId('graphique-tresorerie')).not.toBeInTheDocument();
    });
  });

  it('navigue vers les transactions', async () => {
    renderComponent();
    fireEvent.click(screen.getByText('Transactions'));
    
    await waitFor(() => {
      expect(screen.getByTestId('liste-transactions')).toBeInTheDocument();
      expect(screen.queryByTestId('graphique-tresorerie')).not.toBeInTheDocument();
    });
  });

  it('maintient les stats visibles lors du changement d\'onglet', async () => {
    renderComponent();
    
    // Vérifier que les stats sont visibles initialement
    expect(screen.getByTestId('stats-finance')).toBeInTheDocument();
    
    // Changer d'onglet
    fireEvent.click(screen.getByText('Analyse Budgétaire'));
    
    // Vérifier que les stats sont toujours visibles
    await waitFor(() => {
      expect(screen.getByTestId('stats-finance')).toBeInTheDocument();
    });
  });
});
