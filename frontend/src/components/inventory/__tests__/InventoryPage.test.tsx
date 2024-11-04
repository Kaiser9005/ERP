import React from 'react';
import { render, screen } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from 'react-query';
import { MemoryRouter } from 'react-router-dom';
import InventoryPage from '../InventoryPage';

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

describe('InventoryPage', () => {
  it('affiche le titre et le sous-titre', () => {
    renderWithProviders(<InventoryPage />);
    
    expect(screen.getByText('Inventaire')).toBeInTheDocument();
    expect(screen.getByText('Gestion des stocks et mouvements')).toBeInTheDocument();
  });

  it('affiche le bouton pour créer un nouveau produit', () => {
    renderWithProviders(<InventoryPage />);
    
    expect(screen.getByText('Nouveau Produit')).toBeInTheDocument();
  });

  it('contient les composants principaux', () => {
    renderWithProviders(<InventoryPage />);
    
    expect(screen.getByTestId('inventory-stats')).toBeInTheDocument();
    expect(screen.getByTestId('stock-list')).toBeInTheDocument();
    expect(screen.getByTestId('movement-history')).toBeInTheDocument();
  });
});