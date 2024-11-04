import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from 'react-query';
import { MemoryRouter, Routes, Route } from 'react-router-dom';
import ProductDetails from '../ProductDetails';
import { getProduct, getProductMovements } from '../../../services/inventory';

jest.mock('../../../services/inventory');

const mockProduct = {
  id: '1',
  code: 'PRD001',
  nom: 'Engrais NPK',
  categorie: 'INTRANT',
  unite_mesure: 'KG',
  seuil_alerte: 100,
  prix_unitaire: 1500
};

const mockMovements = [
  {
    id: '1',
    type_mouvement: 'ENTREE',
    quantite: 100,
    date_mouvement: '2024-01-20T10:00:00Z',
    reference_document: 'BL-2024-001',
    responsable: {
      nom: 'Doe',
      prenom: 'John'
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
      <MemoryRouter>
        <Routes>
          <Route path="/" element={component} />
        </Routes>
      </MemoryRouter>
    </QueryClientProvider>
  );
};

describe('ProductDetails', () => {
  beforeEach(() => {
    (getProduct as jest.Mock).mockResolvedValue(mockProduct);
    (getProductMovements as jest.Mock).mockResolvedValue(mockMovements);
  });

  it('affiche les informations du produit', async () => {
    renderWithProviders(<ProductDetails />);
    
    expect(await screen.findByText('Engrais NPK')).toBeInTheDocument();
    expect(await screen.findByText('INTRANT')).toBeInTheDocument();
    expect(await screen.findByText('1 500 FCFA')).toBeInTheDocument();
  });

  it('affiche l\'historique des mouvements', async () => {
    renderWithProviders(<ProductDetails />);
    
    expect(await screen.findByText('Historique des Mouvements')).toBeInTheDocument();
    expect(await screen.findByText('ENTREE')).toBeInTheDocument();
    expect(await screen.findByText('100 KG')).toBeInTheDocument();
    expect(await screen.findByText('BL-2024-001')).toBeInTheDocument();
  });

  it('ouvre le dialogue de mouvement', async () => {
    renderWithProviders(<ProductDetails />);
    
    const button = await screen.findByText('Nouveau Mouvement');
    fireEvent.click(button);
    
    expect(screen.getByText('Nouveau Mouvement de Stock')).toBeInTheDocument();
  });

  it('gère les erreurs de chargement', async () => {
    (getProduct as jest.Mock).mockRejectedValue(new Error('Erreur de chargement'));
    
    renderWithProviders(<ProductDetails />);
    
    expect(await screen.findByText('Erreur de chargement')).toBeInTheDocument();
  });
});