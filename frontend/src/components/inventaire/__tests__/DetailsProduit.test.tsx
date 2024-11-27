import React from 'react';
import { render, screen, fireEvent, within } from '@testing-library/react';
import '@testing-library/jest-dom';
import { QueryClient, QueryClientProvider } from 'react-query';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import DetailsProduit from '../DetailsProduit';
import { getProduit, getProductMovements } from '../../../services/inventaire';
import { vi } from 'vitest';
import { CategoryProduit, TypeMouvement } from '../../../types/inventaire';

vi.mock('../../../services/inventaire');

const mockProduct = {
  id: '1',
  code: 'PRD001',
  nom: 'Engrais NPK',
  categorie: CategoryProduit.INTRANT,
  unite_mesure: 'KG',
  prix_unitaire: 1500,
  seuil_alerte: 100,
  specifications: {}
};

const mockMovements = [
  {
    id: '1',
    produit_id: '1',
    type_mouvement: TypeMouvement.ENTREE,
    quantite: 500,
    date_mouvement: '2024-03-15T10:00:00Z',
    reference_document: 'BON001',
    responsable: {
      id: '1',
      nom: 'Dupont',
      prenom: 'Jean'
    }
  },
  {
    id: '2',
    produit_id: '1',
    type_mouvement: TypeMouvement.SORTIE,
    quantite: 100,
    date_mouvement: '2024-03-16T14:30:00Z',
    reference_document: 'BON002',
    responsable: {
      id: '2',
      nom: 'Martin',
      prenom: 'Sophie'
    }
  }
];

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: false,
    },
  },
});

const renderWithProviders = (productId: string = '1') => {
  return render(
    <QueryClientProvider client={queryClient}>
      <MemoryRouter initialEntries={[`/inventaire/produits/${productId}`]}>
        <Routes>
          <Route path="/inventaire/produits/:id" element={<DetailsProduit />} />
        </Routes>
      </MemoryRouter>
    </QueryClientProvider>
  );
};

describe('DetailsProduit', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    (getProduit as any).mockResolvedValue(mockProduct);
    (getProductMovements as any).mockResolvedValue(mockMovements);
  });

  describe('États de chargement et erreurs', () => {
    it('affiche un indicateur de chargement', () => {
      renderWithProviders();
      
      const loadingStatus = screen.getByRole('status');
      expect(loadingStatus).toBeInTheDocument();
      expect(loadingStatus).toHaveAttribute('aria-label', 'Chargement des données du produit');
      expect(screen.getByText(/chargement des données/i)).toBeInTheDocument();
    });

    it('affiche une erreur en cas d\'échec du chargement du produit', async () => {
      (getProduit as any).mockRejectedValue(new Error('Erreur test'));
      renderWithProviders();
      
      const alert = await screen.findByRole('alert');
      expect(alert).toBeInTheDocument();
      expect(alert).toHaveTextContent(/une erreur est survenue/i);
    });
  });

  describe('Affichage des informations', () => {
    it('affiche les informations du produit', async () => {
      renderWithProviders();
      
      expect(await screen.findByText('Engrais NPK')).toBeInTheDocument();
      expect(screen.getByText('INTRANT')).toBeInTheDocument();
      expect(screen.getByText('KG')).toBeInTheDocument();
      expect(screen.getByText('1 500,00 XAF')).toBeInTheDocument();
      expect(screen.getByText('100 KG')).toBeInTheDocument();
    });

    it('affiche l\'historique des mouvements', async () => {
      renderWithProviders();
      
      const table = await screen.findByRole('table', { name: /historique des mouvements/i });
      const rows = within(table).getAllByRole('row');
      
      expect(rows).toHaveLength(3); // En-tête + 2 mouvements
      expect(within(rows[1]).getByText('BON001')).toBeInTheDocument();
      expect(within(rows[2]).getByText('BON002')).toBeInTheDocument();
    });
  });

  describe('Tri et pagination', () => {
    it('permet de trier les mouvements par date', async () => {
      renderWithProviders();
      
      const dateHeader = await screen.findByText('Date');
      fireEvent.click(dateHeader);
      
      const rows = screen.getAllByRole('row');
      expect(within(rows[1]).getByText('BON001')).toBeInTheDocument();
      
      fireEvent.click(dateHeader);
      expect(within(rows[1]).getByText('BON002')).toBeInTheDocument();
    });

    it('permet de changer le nombre de lignes par page', async () => {
      renderWithProviders();
      
      await screen.findByRole('table');
      
      const rowsPerPageSelect = screen.getByLabelText(/lignes par page/i);
      fireEvent.mouseDown(rowsPerPageSelect);
      
      const listbox = within(screen.getByRole('listbox'));
      fireEvent.click(listbox.getByText('5'));
      
      expect(screen.getByText('1-2 sur 2')).toBeInTheDocument();
    });
  });

  describe('Recherche et filtrage', () => {
    it('permet de rechercher par référence', async () => {
      renderWithProviders();
      
      await screen.findByRole('table');
      
      const searchInput = screen.getByPlaceholderText(/rechercher/i);
      fireEvent.change(searchInput, { target: { value: 'BON001' } });
      
      const rows = screen.getAllByRole('row');
      expect(rows).toHaveLength(2); // En-tête + 1 mouvement
      expect(screen.getByText('BON001')).toBeInTheDocument();
      expect(screen.queryByText('BON002')).not.toBeInTheDocument();
    });

    it('permet de rechercher par nom du responsable', async () => {
      renderWithProviders();
      
      await screen.findByRole('table');
      
      const searchInput = screen.getByPlaceholderText(/rechercher/i);
      fireEvent.change(searchInput, { target: { value: 'Dupont' } });
      
      const rows = screen.getAllByRole('row');
      expect(rows).toHaveLength(2);
      expect(screen.getByText('Dupont')).toBeInTheDocument();
      expect(screen.queryByText('Martin')).not.toBeInTheDocument();
    });
  });

  describe('Export des données', () => {
    it('permet d\'exporter les données en CSV', async () => {
      const mockCreateElement = document.createElement.bind(document);
      const mockClick = vi.fn();
      document.createElement = vi.fn().mockImplementation((tagName) => {
        const element = mockCreateElement(tagName);
        if (tagName === 'a') {
          element.click = mockClick;
        }
        return element;
      });

      renderWithProviders();
      
      await screen.findByRole('table');
      
      const exportButton = screen.getByLabelText(/exporter.*csv/i);
      fireEvent.click(exportButton);
      
      expect(mockClick).toHaveBeenCalled();
      
      document.createElement = mockCreateElement;
    });
  });

  describe('Accessibilité', () => {
    it('utilise des rôles ARIA appropriés', async () => {
      renderWithProviders();
      
      await screen.findByRole('table', { name: /historique des mouvements/i });
      expect(screen.getByRole('button', { name: /nouveau mouvement/i })).toBeInTheDocument();
      expect(screen.getByRole('searchbox', { name: /rechercher/i })).toBeInTheDocument();
      expect(screen.getByRole('button', { name: /exporter.*csv/i })).toBeInTheDocument();
    });

    it('fournit des descriptions pour les éléments interactifs', async () => {
      renderWithProviders();
      
      await screen.findByRole('table');
      
      const exportButton = screen.getByRole('button', { name: /exporter.*csv/i });
      expect(exportButton).toHaveAccessibleName();
      
      const searchInput = screen.getByRole('searchbox');
      expect(searchInput).toHaveAccessibleName();
    });
  });
});
