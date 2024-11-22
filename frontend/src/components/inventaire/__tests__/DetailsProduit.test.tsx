import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { MemoryRouter, Routes, Route } from 'react-router-dom';
import DetailsProduit from '../DetailsProduit';
import { getProduit, getMouvementsProduit } from '../../../services/inventaire';
import { vi } from 'vitest';
import type { Produit, MouvementStock } from '../../../types/inventaire';

declare global {
  namespace Vi {
    interface JestMatchers<T> {
      toBeInTheDocument(): boolean;
    }
  }
}

vi.mock('../../../services/inventaire');

const mockProduit: Produit = {
  id: '1',
  code: 'PRD001',
  nom: 'Engrais NPK',
  categorie: 'INTRANT',
  unite_mesure: 'KG',
  seuil_alerte: 100,
  prix_unitaire: 1500,
  specifications: {}
};

const mockMouvements: MouvementStock[] = [
  {
    id: '1',
    type_mouvement: 'ENTREE',
    quantite: 100,
    date_mouvement: '2024-01-20T10:00:00Z',
    reference_document: 'BL-2024-001',
    responsable: {
      id: '1',
      nom: 'Doe',
      prenom: 'John'
    },
    produit_id: '1',
    produit: mockProduit,
    cout_unitaire: 1500
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

describe('DetailsProduit', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    (getProduit as any).mockResolvedValue(mockProduit);
    (getMouvementsProduit as any).mockResolvedValue(mockMouvements);
  });

  it('affiche les informations du produit', async () => {
    renderWithProviders(<DetailsProduit />);
    
    expect(await screen.findByText('Engrais NPK')).toBeInTheDocument();
    expect(await screen.findByText('INTRANT')).toBeInTheDocument();
    expect(await screen.findByText('1 500,00 XAF')).toBeInTheDocument();
  });

  it('affiche l\'historique des mouvements', async () => {
    renderWithProviders(<DetailsProduit />);
    
    expect(await screen.findByText('Historique des Mouvements')).toBeInTheDocument();
    expect(await screen.findByText('ENTREE')).toBeInTheDocument();
    expect(await screen.findByText('100 KG')).toBeInTheDocument();
    expect(await screen.findByText('BL-2024-001')).toBeInTheDocument();
  });

  it('affiche le responsable du mouvement', async () => {
    renderWithProviders(<DetailsProduit />);
    
    expect(await screen.findByText('John Doe')).toBeInTheDocument();
  });

  it('ouvre le dialogue de mouvement', async () => {
    renderWithProviders(<DetailsProduit />);
    
    const bouton = await screen.findByText('Nouveau Mouvement');
    fireEvent.click(bouton);
    
    expect(screen.getByText('Nouveau Mouvement de Stock')).toBeInTheDocument();
  });

  it('affiche un message de chargement', () => {
    (getProduit as any).mockReturnValue(new Promise(() => {}));
    renderWithProviders(<DetailsProduit />);
    
    expect(screen.getByText('Chargement...')).toBeInTheDocument();
  });

  it('gère les erreurs de chargement', async () => {
    (getProduit as any).mockRejectedValue(new Error('Erreur test'));
    renderWithProviders(<DetailsProduit />);
    
    expect(await screen.findByText('Erreur lors du chargement du produit')).toBeInTheDocument();
  });

  it('affiche le seuil d\'alerte', async () => {
    renderWithProviders(<DetailsProduit />);
    
    expect(await screen.findByText('Seuil d\'Alerte')).toBeInTheDocument();
    expect(await screen.findByText('100 KG')).toBeInTheDocument();
  });
});
