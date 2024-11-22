import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import ListeStock from '../ListeStock';
import { getStocks, getProduits } from '../../../services/inventaire';
import { vi } from 'vitest';
import type { Stock, Produit } from '../../../types/inventaire';

declare global {
  namespace Vi {
    interface JestMatchers<T> {
      toBeInTheDocument(): boolean;
      toHaveClass(className: string): boolean;
    }
  }
}

vi.mock('../../../services/inventaire');

const mockStocks: Stock[] = [
  {
    id: '1',
    produit_id: '1',
    produit: {
      id: '1',
      code: 'PRD001',
      nom: 'Engrais NPK',
      categorie: 'INTRANT',
      unite_mesure: 'KG',
      prix_unitaire: 1500,
      seuil_alerte: 100,
      specifications: {}
    },
    quantite: 500,
    valeur_unitaire: 1500,
    emplacement: 'Stock Principal',
    date_derniere_maj: new Date().toISOString()
  },
  {
    id: '2',
    produit_id: '2',
    produit: {
      id: '2',
      code: 'PRD002',
      nom: 'Pesticide',
      categorie: 'INTRANT',
      unite_mesure: 'LITRE',
      prix_unitaire: 5000,
      seuil_alerte: 20,
      specifications: {}
    },
    quantite: 15,
    valeur_unitaire: 5000,
    emplacement: 'Stock Secondaire',
    date_derniere_maj: new Date().toISOString()
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
    (getProduits as any).mockResolvedValue([]);
  });

  it('affiche la liste des stocks', async () => {
    renderWithProviders(<ListeStock />);
    
    const tableStocks = await screen.findByTestId('table-stocks');
    expect(tableStocks).toBeInTheDocument();
    
    const stock1 = await screen.findByTestId('stock-1');
    const stock2 = await screen.findByTestId('stock-2');
    expect(stock1).toBeInTheDocument();
    expect(stock2).toBeInTheDocument();
  });

  it('filtre par catégorie', async () => {
    renderWithProviders(<ListeStock />);
    
    const filtreCategorie = await screen.findByTestId('filtre-categorie');
    fireEvent.change(filtreCategorie, { target: { value: 'INTRANT' } });
    
    const stock1 = await screen.findByTestId('stock-1');
    const stock2 = await screen.findByTestId('stock-2');
    expect(stock1).toBeInTheDocument();
    expect(stock2).toBeInTheDocument();
  });

  it('filtre par niveau de stock', async () => {
    renderWithProviders(<ListeStock />);
    
    const filtreNiveau = await screen.findByTestId('filtre-niveau');
    fireEvent.change(filtreNiveau, { target: { value: 'SOUS_SEUIL' } });
    
    expect(getStocks).toHaveBeenCalledWith({ seuil_alerte: true });
  });

  it('affiche les statuts de stock corrects', async () => {
    renderWithProviders(<ListeStock />);
    
    const statut1 = await screen.findByTestId('statut-1');
    const statut2 = await screen.findByTestId('statut-2');
    
    expect(statut1).toHaveClass('MuiChip-colorSuccess');
    expect(statut2).toHaveClass('MuiChip-colorError');
  });

  it('affiche les valeurs des stocks', async () => {
    renderWithProviders(<ListeStock />);
    
    const stock1 = await screen.findByTestId('stock-1');
    const stock2 = await screen.findByTestId('stock-2');
    
    expect(stock1).toHaveTextContent('1 500,00 XAF');
    expect(stock2).toHaveTextContent('5 000,00 XAF');
  });

  it('affiche un message de chargement', () => {
    (getStocks as any).mockReturnValue(new Promise(() => {}));
    renderWithProviders(<ListeStock />);
    
    expect(screen.getByTestId('chargement-stocks')).toBeInTheDocument();
  });

  it('gère les erreurs de chargement', async () => {
    (getStocks as any).mockRejectedValue(new Error('Erreur test'));
    renderWithProviders(<ListeStock />);
    
    expect(await screen.findByTestId('erreur-stocks')).toBeInTheDocument();
  });

  it('affiche les unités de mesure', async () => {
    renderWithProviders(<ListeStock />);
    
    const stock1 = await screen.findByTestId('stock-1');
    const stock2 = await screen.findByTestId('stock-2');
    
    expect(stock1).toHaveTextContent('500 KG');
    expect(stock2).toHaveTextContent('15 LITRE');
  });

  it('affiche les seuils d\'alerte', async () => {
    renderWithProviders(<ListeStock />);
    
    const stock1 = await screen.findByTestId('stock-1');
    const stock2 = await screen.findByTestId('stock-2');
    
    expect(stock1).toHaveTextContent('100 KG');
    expect(stock2).toHaveTextContent('20 LITRE');
  });
});
