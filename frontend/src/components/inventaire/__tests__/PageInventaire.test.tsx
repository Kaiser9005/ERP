import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { MemoryRouter } from 'react-router-dom';
import PageInventaire from '../PageInventaire';
import { vi } from 'vitest';

declare global {
  namespace Vi {
    interface JestMatchers<T> {
      toBeInTheDocument(): boolean;
    }
  }
}

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

describe('PageInventaire', () => {
  it('affiche le titre et le sous-titre', () => {
    renderWithProviders(<PageInventaire />);
    
    expect(screen.getByText('Inventaire')).toBeInTheDocument();
    expect(screen.getByText('Gestion des stocks et mouvements')).toBeInTheDocument();
  });

  it('affiche le bouton pour créer un nouveau produit', () => {
    renderWithProviders(<PageInventaire />);
    
    expect(screen.getByText('Nouveau Produit')).toBeInTheDocument();
  });

  it('contient les composants principaux', () => {
    renderWithProviders(<PageInventaire />);
    
    expect(screen.getByTestId('stats-inventaire')).toBeInTheDocument();
    expect(screen.getByTestId('liste-stock')).toBeInTheDocument();
    expect(screen.getByTestId('historique-mouvements')).toBeInTheDocument();
  });

  it('affiche le bouton de filtrage', () => {
    renderWithProviders(<PageInventaire />);
    
    expect(screen.getByTestId('bouton-filtres')).toBeInTheDocument();
  });

  it('affiche le champ de recherche', () => {
    renderWithProviders(<PageInventaire />);
    
    expect(screen.getByPlaceholderText('Rechercher un produit...')).toBeInTheDocument();
  });

  it('affiche les statistiques globales', () => {
    renderWithProviders(<PageInventaire />);
    
    expect(screen.getByTestId('stats-inventaire')).toBeInTheDocument();
  });
});
