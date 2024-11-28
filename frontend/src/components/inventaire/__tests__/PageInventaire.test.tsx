import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { MemoryRouter, useNavigate } from 'react-router-dom';
import { vi } from 'vitest';
import PageInventaire from '../PageInventaire';
import { fetchInventoryPermissions } from '../../../services/inventaire';

// Mock des services
vi.mock('../../../services/inventaire');
vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual('react-router-dom');
  return {
    ...(typeof actual === 'object' ? actual : {}),
    useNavigate: vi.fn()
  };
});

// Mock des composants enfants
vi.mock('../ListeStock', () => ({
  default: () => <div data-testid="liste-stock">ListeStock</div>
}));

vi.mock('../StatsInventaire', () => ({
  default: () => <div data-testid="stats-inventaire">StatsInventaire</div>
}));

vi.mock('../HistoriqueMouvements', () => ({
  default: () => <div data-testid="historique-mouvements">HistoriqueMouvements</div>
}));

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
  const mockNavigate = vi.fn();

  beforeEach(() => {
    vi.clearAllMocks();
    (useNavigate as jest.Mock).mockReturnValue(mockNavigate);
    // Mock des permissions par défaut
    (fetchInventoryPermissions as jest.Mock).mockResolvedValue({
      canCreate: true,
      canEdit: true,
      canDelete: true
    });
  });

  it('affiche le titre et le sous-titre', async () => {
    renderWithProviders(<PageInventaire />);
    
    await waitFor(() => {
      expect(screen.getByText('inventory.page.title')).toBeInTheDocument();
      expect(screen.getByText('inventory.page.subtitle')).toBeInTheDocument();
    });
  });

  it('affiche un loader pendant le chargement', () => {
    renderWithProviders(<PageInventaire />);
    
    expect(screen.getByRole('progressbar')).toBeInTheDocument();
    expect(screen.getByLabelText('common.loading')).toBeInTheDocument();
  });

  it('affiche une erreur en cas de problème', async () => {
    (fetchInventoryPermissions as jest.Mock).mockRejectedValue(
      new Error('Test error')
    );

    renderWithProviders(<PageInventaire />);
    
    await waitFor(() => {
      expect(screen.getByText('inventory.error.loading')).toBeInTheDocument();
    });
  });

  it('affiche le bouton nouveau produit si autorisé', async () => {
    renderWithProviders(<PageInventaire />);
    
    await waitFor(() => {
      expect(screen.getByLabelText('inventory.actions.newProduct')).toBeInTheDocument();
    });
  });

  it('masque le bouton nouveau produit si non autorisé', async () => {
    (fetchInventoryPermissions as jest.Mock).mockResolvedValue({
      canCreate: false,
      canEdit: true,
      canDelete: true
    });

    renderWithProviders(<PageInventaire />);
    
    await waitFor(() => {
      expect(screen.queryByLabelText('inventory.actions.newProduct')).not.toBeInTheDocument();
    });
  });

  it('navigue vers le formulaire de création', async () => {
    renderWithProviders(<PageInventaire />);
    
    await waitFor(() => {
      const button = screen.getByLabelText('inventory.actions.newProduct');
      button.click();
      expect(mockNavigate).toHaveBeenCalledWith('/inventaire/produits/nouveau');
    });
  });

  it('affiche les composants principaux après chargement', async () => {
    renderWithProviders(<PageInventaire />);
    
    await waitFor(() => {
      expect(screen.getByTestId('stats-inventaire')).toBeInTheDocument();
      expect(screen.getByTestId('liste-stock')).toBeInTheDocument();
      expect(screen.getByTestId('historique-mouvements')).toBeInTheDocument();
    });
  });

  describe('Accessibilité', () => {
    it('a une structure sémantique correcte', async () => {
      renderWithProviders(<PageInventaire />);
      
      await waitFor(() => {
        expect(screen.getByRole('main')).toBeInTheDocument();
        expect(screen.getAllByRole('region')).toHaveLength(2);
      });
    });

    it('a des labels ARIA appropriés', async () => {
      renderWithProviders(<PageInventaire />);
      
      await waitFor(() => {
        expect(screen.getByLabelText('inventory.page.title')).toBeInTheDocument();
        expect(screen.getByLabelText('inventory.sections.stockList')).toBeInTheDocument();
        expect(screen.getByLabelText('inventory.sections.movements')).toBeInTheDocument();
      });
    });
  });
});
