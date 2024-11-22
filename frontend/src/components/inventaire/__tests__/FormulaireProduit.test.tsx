import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { MemoryRouter, Routes, Route } from 'react-router-dom';
import FormulaireProduit from '../FormulaireProduit';
import { createProduit, updateProduit, getProduit } from '../../../services/inventaire';
import { vi } from 'vitest';
import type { Produit } from '../../../types/inventaire';

declare global {
  namespace Vi {
    interface JestMatchers<T> {
      toBeInTheDocument(): boolean;
    }
  }
}

vi.mock('../../../services/inventaire');

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: false,
    },
  },
});

const renderWithProviders = (initialPath: string = '/') => {
  return render(
    <QueryClientProvider client={queryClient}>
      <MemoryRouter initialEntries={[initialPath]}>
        <Routes>
          <Route path="/" element={<FormulaireProduit />} />
          <Route path="/produit/:id" element={<FormulaireProduit />} />
          <Route path="/inventaire" element={<div>Page Inventaire</div>} />
        </Routes>
      </MemoryRouter>
    </QueryClientProvider>
  );
};

describe('FormulaireProduit', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('affiche le formulaire de création', () => {
    renderWithProviders();
    
    expect(screen.getByText('Nouveau Produit')).toBeInTheDocument();
    expect(screen.getByLabelText('Code')).toBeInTheDocument();
    expect(screen.getByLabelText('Nom')).toBeInTheDocument();
    expect(screen.getByLabelText('Catégorie')).toBeInTheDocument();
  });

  it('valide les champs requis', async () => {
    renderWithProviders();
    
    fireEvent.click(screen.getByText('Créer'));
    
    expect(await screen.findByText('Le code est requis')).toBeInTheDocument();
    expect(await screen.findByText('Le nom est requis')).toBeInTheDocument();
    expect(await screen.findByText('La catégorie est requise')).toBeInTheDocument();
    expect(await screen.findByText('L\'unité de mesure est requise')).toBeInTheDocument();
  });

  it('soumet le formulaire avec des données valides', async () => {
    const mockProduit: Partial<Produit> = {
      code: 'PRD001',
      nom: 'Engrais NPK',
      categorie: 'INTRANT',
      unite_mesure: 'KG',
      seuil_alerte: 100,
      prix_unitaire: 1500,
      specifications: {}
    };

    (createProduit as any).mockResolvedValue({ id: '1', ...mockProduit });
    
    renderWithProviders();
    
    fireEvent.change(screen.getByLabelText('Code'), { target: { value: 'PRD001' } });
    fireEvent.change(screen.getByLabelText('Nom'), { target: { value: 'Engrais NPK' } });
    fireEvent.change(screen.getByLabelText('Catégorie'), { target: { value: 'INTRANT' } });
    fireEvent.change(screen.getByLabelText('Unité de Mesure'), { target: { value: 'KG' } });
    fireEvent.change(screen.getByLabelText('Seuil d\'Alerte'), { target: { value: '100' } });
    fireEvent.change(screen.getByLabelText('Prix Unitaire'), { target: { value: '1500' } });
    
    fireEvent.click(screen.getByText('Créer'));
    
    await waitFor(() => {
      expect(createProduit).toHaveBeenCalledWith(mockProduit);
    });
  });

  it('charge les données pour la modification', async () => {
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

    (getProduit as any).mockResolvedValue(mockProduit);
    
    renderWithProviders('/produit/1');
    
    expect(await screen.findByDisplayValue('PRD001')).toBeInTheDocument();
    expect(await screen.findByDisplayValue('Engrais NPK')).toBeInTheDocument();
  });

  it('gère les erreurs de soumission', async () => {
    (createProduit as any).mockRejectedValue(new Error('Erreur test'));
    
    renderWithProviders();
    
    fireEvent.change(screen.getByLabelText('Code'), { target: { value: 'PRD001' } });
    fireEvent.click(screen.getByText('Créer'));
    
    expect(await screen.findByText('Une erreur est survenue')).toBeInTheDocument();
  });

  it('permet la modification d\'un produit existant', async () => {
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

    (getProduit as any).mockResolvedValue(mockProduit);
    (updateProduit as any).mockResolvedValue({ ...mockProduit, nom: 'Engrais NPK Plus' });
    
    renderWithProviders('/produit/1');
    
    await waitFor(() => {
      expect(screen.getByDisplayValue('Engrais NPK')).toBeInTheDocument();
    });

    fireEvent.change(screen.getByLabelText('Nom'), { target: { value: 'Engrais NPK Plus' } });
    fireEvent.click(screen.getByText('Modifier'));
    
    await waitFor(() => {
      expect(updateProduit).toHaveBeenCalledWith('1', {
        ...mockProduit,
        nom: 'Engrais NPK Plus'
      });
    });
  });
});
