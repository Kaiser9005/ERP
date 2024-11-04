import React from 'react';
import { render, screen } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from 'react-query';
import { MemoryRouter } from 'react-router-dom';
import FinancePage from '../FinancePage';

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
      <MemoryRouter>
        {component}
      </MemoryRouter>
    </QueryClientProvider>
  );
};

describe('FinancePage', () => {
  it('affiche le titre et le sous-titre', () => {
    renderWithProviders(<FinancePage />);
    
    expect(screen.getByText('Finance')).toBeInTheDocument();
    expect(screen.getByText('Gestion financière et trésorerie')).toBeInTheDocument();
  });

  it('affiche le bouton pour créer une nouvelle transaction', () => {
    renderWithProviders(<FinancePage />);
    
    expect(screen.getByText('Nouvelle Transaction')).toBeInTheDocument();
  });

  it('contient les composants principaux', () => {
    renderWithProviders(<FinancePage />);
    
    expect(screen.getByTestId('finance-stats')).toBeInTheDocument();
    expect(screen.getByTestId('cashflow-chart')).toBeInTheDocument();
    expect(screen.getByTestId('budget-overview')).toBeInTheDocument();
    expect(screen.getByTestId('transactions-list')).toBeInTheDocument();
  });
});