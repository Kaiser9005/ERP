import React from 'react';
import { render, screen } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from 'react-query';
import { MemoryRouter } from 'react-router-dom';
import ProductionPage from '../ProductionPage';

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

describe('ProductionPage', () => {
  it('affiche le titre et le sous-titre', () => {
    renderWithProviders(<ProductionPage />);
    
    expect(screen.getByText('Production')).toBeInTheDocument();
    expect(screen.getByText('Gestion des parcelles et des récoltes')).toBeInTheDocument();
  });

  it('affiche le bouton pour créer une nouvelle parcelle', () => {
    renderWithProviders(<ProductionPage />);
    
    expect(screen.getByText('Nouvelle Parcelle')).toBeInTheDocument();
  });

  it('contient les composants principaux', () => {
    renderWithProviders(<ProductionPage />);
    
    expect(screen.getByTestId('production-stats')).toBeInTheDocument();
    expect(screen.getByTestId('production-calendar')).toBeInTheDocument();
    expect(screen.getByTestId('parcelles-list')).toBeInTheDocument();
  });
});