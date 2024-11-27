import React from 'react';
import { render, screen, fireEvent, within } from '@testing-library/react';
import '@testing-library/jest-dom';
import { QueryClient, QueryClientProvider } from 'react-query';
import ListeStock from '../ListeStock';
import { getStocks } from '../../../services/inventaire';
import { vi } from 'vitest';
import type { Stock, Produit } from '../../../types/inventaire';
import { CategoryProduit, UniteMesure } from '../../../types/inventaire';

vi.mock('../../../services/inventaire');

const mockStocks: (Stock & { produit: Produit })[] = [
  {
    id: '1',
    produit_id: '1',
    quantite: 500,
    valeur_unitaire: 1500,
    emplacement: 'Stock Principal',
    date_derniere_maj: new Date().toISOString(),
    produit: {
      id: '1',
      code: 'PRD001',
      nom: 'Engrais NPK',
      categorie: CategoryProduit.INTRANT,
      unite_mesure: UniteMesure.KG,
      prix_unitaire: 1500,
      seuil_alerte: 100,
      specifications: {}
    }
  },
  {
    id: '2',
    produit_id: '2',
    quantite: 15,
    valeur_unitaire: 5000,
    emplacement: 'Stock Secondaire',
    date_derniere_maj: new Date().toISOString(),
    produit: {
      id: '2',
      code: 'PRD002',
      nom: 'Pesticide',
      categorie: CategoryProduit.INTRANT,
      unite_mesure: UniteMesure.L,
      prix_unitaire: 5000,
      seuil_alerte: 20,
      specifications: {}
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

const renderWithProviders = (component: React.ReactElement) => {
  return render(
    <QueryClientProvider client={queryClient}>
      {component}
    </QueryClientProvider>
  );
};

describe('ListeStock', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    (getStocks as any).mockResolvedValue(mockStocks);
  });

  it('affiche la liste des stocks', async () => {
    renderWithProviders(<ListeStock />);
    
    expect(await screen.findByRole('table', { name: /liste des stocks/i })).toBeInTheDocument();
    expect(await screen.findByTestId('stock-1')).toBeInTheDocument();
    expect(await screen.findByTestId('stock-2')).toBeInTheDocument();
  });

  it('affiche les informations des produits', async () => {
    renderWithProviders(<ListeStock />);
    
    const stock1 = await screen.findByTestId('stock-1');
    const stock2 = await screen.findByTestId('stock-2');
    
    expect(stock1).toHaveTextContent('PRD001');
    expect(stock1).toHaveTextContent('Engrais NPK');
    expect(stock1).toHaveTextContent('500 KG');
    
    expect(stock2).toHaveTextContent('PRD002');
    expect(stock2).toHaveTextContent('Pesticide');
    expect(stock2).toHaveTextContent('15 L');
  });

  it('affiche les valeurs des stocks', async () => {
    renderWithProviders(<ListeStock />);
    
    const stock1 = await screen.findByTestId('stock-1');
    const stock2 = await screen.findByTestId('stock-2');
    
    expect(stock1).toHaveTextContent('750 000,00');
    expect(stock2).toHaveTextContent('75 000,00');
  });

  it('affiche les niveaux de stock avec les bons indicateurs visuels', async () => {
    renderWithProviders(<ListeStock />);
    
    const statut1 = await screen.findByTestId('statut-1');
    const statut2 = await screen.findByTestId('statut-2');
    
    expect(statut1).toHaveClass('MuiLinearProgress-colorSuccess');
    expect(statut2).toHaveClass('MuiLinearProgress-colorError');
    
    expect(statut1).toHaveAccessibleName(/niveau de stock: 500%/i);
    expect(statut2).toHaveAccessibleName(/niveau de stock: 75%/i);
  });

  it('filtre les produits par recherche', async () => {
    renderWithProviders(<ListeStock />);
    
    const searchInput = screen.getByRole('textbox', { name: /rechercher un produit/i });
    fireEvent.change(searchInput, { target: { value: 'Engrais' } });
    
    expect(await screen.findByTestId('stock-1')).toBeInTheDocument();
    expect(screen.queryByTestId('stock-2')).not.toBeInTheDocument();
  });

  it('filtre les produits par catégorie', async () => {
    renderWithProviders(<ListeStock />);
    
    const categorieSelect = screen.getByLabelText(/catégorie/i);
    fireEvent.mouseDown(categorieSelect);
    
    const listbox = within(screen.getByRole('listbox'));
    fireEvent.click(listbox.getByText(/intrant/i));
    
    expect(await screen.findByTestId('stock-1')).toBeInTheDocument();
    expect(await screen.findByTestId('stock-2')).toBeInTheDocument();
  });

  it('trie les produits par code', async () => {
    renderWithProviders(<ListeStock />);
    
    const codeHeader = screen.getByRole('columnheader', { name: /code/i });
    fireEvent.click(codeHeader);
    
    const rows = await screen.findAllByRole('row');
    expect(within(rows[1]).getByText('PRD001')).toBeInTheDocument();
    
    fireEvent.click(codeHeader);
    expect(within(rows[1]).getByText('PRD002')).toBeInTheDocument();
  });

  it('change le nombre de lignes par page', async () => {
    renderWithProviders(<ListeStock />);
    
    const rowsPerPageSelect = screen.getByLabelText(/lignes par page/i);
    fireEvent.mouseDown(rowsPerPageSelect);
    
    const listbox = within(screen.getByRole('listbox'));
    fireEvent.click(listbox.getByText('25'));
    
    expect(screen.getByText('1-2 sur 2')).toBeInTheDocument();
  });

  it('affiche un message de chargement', () => {
    (getStocks as any).mockReturnValue(new Promise(() => {}));
    renderWithProviders(<ListeStock />);
    
    expect(screen.getByRole('progressbar', { name: /chargement des stocks/i })).toBeInTheDocument();
    expect(screen.getByText(/chargement des stocks en cours/i)).toBeInTheDocument();
  });

  it('gère les erreurs de chargement', async () => {
    (getStocks as any).mockRejectedValue(new Error('Erreur test'));
    renderWithProviders(<ListeStock />);
    
    expect(await screen.findByText(/une erreur est survenue/i)).toBeInTheDocument();
  });

  it('affiche des tooltips pour les actions', async () => {
    renderWithProviders(<ListeStock />);
    
    const stock = await screen.findByTestId('stock-1');
    const addButton = within(stock).getByRole('button', { name: /ajouter un mouvement pour engrais npk/i });
    const editButton = within(stock).getByRole('button', { name: /modifier engrais npk/i });
    
    expect(addButton).toBeInTheDocument();
    expect(editButton).toBeInTheDocument();
  });

  it('affiche des tooltips pour les niveaux de stock', async () => {
    renderWithProviders(<ListeStock />);
    
    const stock1 = await screen.findByTestId('stock-1');
    const progressBar1 = within(stock1).getByRole('progressbar');
    expect(progressBar1).toHaveAttribute('aria-label', expect.stringMatching(/niveau de stock/i));
  });
});
