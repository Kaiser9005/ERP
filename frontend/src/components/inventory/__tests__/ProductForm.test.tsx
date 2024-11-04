import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from 'react-query';
import { MemoryRouter, Routes, Route } from 'react-router-dom';
import ProductForm from '../ProductForm';
import { createProduct, updateProduct, getProduct } from '../../../services/inventory';

jest.mock('../../../services/inventory');

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
          <Route path="/inventory" element={<div>Inventory Page</div>} />
        </Routes>
      </MemoryRouter>
    </QueryClientProvider>
  );
};

describe('ProductForm', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('affiche le formulaire de création', () => {
    renderWithProviders(<ProductForm />);
    
    expect(screen.getByText('Nouveau Produit')).toBeInTheDocument();
    expect(screen.getByLabelText('Code')).toBeInTheDocument();
    expect(screen.getByLabelText('Nom')).toBeInTheDocument();
    expect(screen.getByLabelText('Catégorie')).toBeInTheDocument();
  });

  it('valide les champs requis', async () => {
    renderWithProviders(<ProductForm />);
    
    fireEvent.click(screen.getByText('Créer'));
    
    expect(await screen.findByText('Le code est requis')).toBeInTheDocument();
    expect(await screen.findByText('Le nom est requis')).toBeInTheDocument();
    expect(await screen.findByText('La catégorie est requise')).toBeInTheDocument();
    expect(await screen.findByText('L\'unité de mesure est requise')).toBeInTheDocument();
  });

  it('soumet le formulaire avec des données valides', async () => {
    (createProduct as jest.Mock).mockResolvedValue({ id: '1' });
    
    renderWithProviders(<ProductForm />);
    
    fireEvent.change(screen.getByLabelText('Code'), { target: { value: 'PRD001' } });
    fireEvent.change(screen.getByLabelText('Nom'), { target: { value: 'Engrais NPK' } });
    fireEvent.change(screen.getByLabelText('Catégorie'), { target: { value: 'INTRANT' } });
    fireEvent.change(screen.getByLabelText('Unité de Mesure'), { target: { value: 'KG' } });
    fireEvent.change(screen.getByLabelText('Seuil d\'Alerte'), { target: { value: '100' } });
    fireEvent.change(screen.getByLabelText('Prix Unitaire'), { target: { value: '1500' } });
    
    fireEvent.click(screen.getByText('Créer'));
    
    await waitFor(() => {
      expect(createProduct).toHaveBeenCalledWith({
        code: 'PRD001',
        nom: 'Engrais NPK',
        categorie: 'INTRANT',
        unite_mesure: 'KG',
        seuil_alerte: '100',
        prix_unitaire: '1500'
      });
    });
  });

  it('charge les données pour la modification', async () => {
    const mockProduct = {
      id: '1',
      code: 'PRD001',
      nom: 'Engrais NPK',
      categorie: 'INTRANT',
      unite_mesure: 'KG',
      seuil_alerte: 100,
      prix_unitaire: 1500
    };

    (getProduct as jest.Mock).mockResolvedValue(mockProduct);
    
    renderWithProviders(<ProductForm />);
    
    expect(await screen.findByDisplayValue('PRD001')).toBeInTheDocument();
    expect(await screen.findByDisplayValue('Engrais NPK')).toBeInTheDocument();
  });

  it('gère les erreurs de soumission', async () => {
    (createProduct as jest.Mock).mockRejectedValue(new Error('Erreur de création'));
    
    renderWithProviders(<ProductForm />);
    
    fireEvent.change(screen.getByLabelText('Code'), { target: { value: 'PRD001' } });
    fireEvent.click(screen.getByText('Créer'));
    
    expect(await screen.findByText('Une erreur est survenue')).toBeInTheDocument();
  });
});