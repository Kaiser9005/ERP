import React from 'react';
import { render, screen } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from 'react-query';
import { MemoryRouter } from 'react-router-dom';
import PageFinance from '../PageFinance';

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

describe('PageFinance', () => {
  it('affiche le titre et le sous-titre', () => {
    renderWithProviders(<PageFinance />);
    
    expect(screen.getByText('Finance')).toBeInTheDocument();
    expect(screen.getByText('Gestion financière et trésorerie')).toBeInTheDocument();
  });

  it('affiche le bouton pour créer une nouvelle transaction', () => {
    renderWithProviders(<PageFinance />);
    
    expect(screen.getByText('Nouvelle Transaction')).toBeInTheDocument();
  });

  it('contient les composants principaux', () => {
    renderWithProviders(<PageFinance />);
    
    expect(screen.getByTestId('finance-stats')).toBeInTheDocument();
    expect(screen.getByTestId('cashflow-chart')).toBeInTheDocument();
    expect(screen.getByTestId('budget-overview')).toBeInTheDocument();
    expect(screen.getByTestId('transactions-list')).toBeInTheDocument();
  });
});