import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import { QueryClient, QueryClientProvider } from 'react-query';
import { MemoryRouter, Routes, Route } from 'react-router-dom';
import FormulaireProduit from '../FormulaireProduit';
import { creerProduit, modifierProduit, getProduit, verifierCodeUnique } from '../../../services/inventaire';
import { CategoryProduit, UniteMesure } from '../../../types/inventaire';
import { vi } from 'vitest';

vi.mock('../../../services/inventaire');

const mockProduct = {
  id: '1',
  code: 'PRD001',
  nom: 'Engrais NPK',
  categorie: CategoryProduit.INTRANT,
  unite_mesure: UniteMesure.KG,
  seuil_alerte: 100,
  prix_unitaire: 1500,
  quantite_stock: 1000,
  description: 'Description test'
};

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: false,
    },
  },
});

const renderWithProviders = (id?: string) => {
  return render(
    <QueryClientProvider client={queryClient}>
      <MemoryRouter initialEntries={[id ? `/inventaire/produits/${id}` : '/inventaire/produits/nouveau']}>
        <Routes>
          <Route path="/inventaire/produits/:id" element={<FormulaireProduit />} />
          <Route path="/inventaire/produits/nouveau" element={<FormulaireProduit />} />
        </Routes>
      </MemoryRouter>
    </QueryClientProvider>
  );
};

describe('FormulaireProduit', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    (getProduit as any).mockResolvedValue(mockProduct);
    (verifierCodeUnique as any).mockResolvedValue(true);
    (creerProduit as any).mockResolvedValue({ ...mockProduct, id: '2' });
    (modifierProduit as any).mockResolvedValue(mockProduct);
  });

  describe('Affichage', () => {
    it('affiche le formulaire de création', () => {
      renderWithProviders();

      expect(screen.getByText('Nouveau Produit')).toBeInTheDocument();
      expect(screen.getByLabelText(/Code/)).toBeInTheDocument();
      expect(screen.getByLabelText(/Nom/)).toBeInTheDocument();
      expect(screen.getByLabelText(/Catégorie/)).toBeInTheDocument();
      expect(screen.getByLabelText(/Unité de mesure/)).toBeInTheDocument();
      expect(screen.getByLabelText(/Seuil d'alerte/)).toBeInTheDocument();
      expect(screen.getByLabelText(/Prix unitaire/)).toBeInTheDocument();
      expect(screen.getByLabelText(/Description/)).toBeInTheDocument();
    });

    it('charge et affiche les données du produit en mode édition', async () => {
      renderWithProviders('1');

      await waitFor(() => {
        expect(screen.getByDisplayValue(mockProduct.code)).toBeInTheDocument();
        expect(screen.getByDisplayValue(mockProduct.nom)).toBeInTheDocument();
        expect(screen.getByDisplayValue(mockProduct.description!)).toBeInTheDocument();
      });
    });
  });

  describe('Validation', () => {
    it('affiche une erreur si le code est invalide', async () => {
      renderWithProviders();

      const codeInput = screen.getByLabelText(/Code/);
      fireEvent.change(codeInput, { target: { value: 'ab' } });
      fireEvent.blur(codeInput);

      expect(await screen.findByText(/Le code doit contenir au moins 3 caractères/)).toBeInTheDocument();
    });

    it('vérifie l\'unicité du code', async () => {
      (verifierCodeUnique as any).mockResolvedValue(false);
      renderWithProviders();

      const codeInput = screen.getByLabelText(/Code/);
      fireEvent.change(codeInput, { target: { value: 'PRD001' } });
      fireEvent.blur(codeInput);

      expect(await screen.findByText(/Ce code existe déjà/)).toBeInTheDocument();
    });

    it('valide les champs requis', async () => {
      renderWithProviders();

      const submitButton = screen.getByRole('button', { name: /Créer/ });
      fireEvent.click(submitButton);

      expect(await screen.findByText(/Le code est requis/)).toBeInTheDocument();
      expect(await screen.findByText(/Le nom est requis/)).toBeInTheDocument();
    });
  });

  describe('Soumission', () => {
    it('crée un nouveau produit avec succès', async () => {
      renderWithProviders();

      fireEvent.change(screen.getByLabelText(/Code/), { target: { value: 'PRD002' } });
      fireEvent.change(screen.getByLabelText(/Nom/), { target: { value: 'Test Produit' } });
      fireEvent.change(screen.getByLabelText(/Seuil d'alerte/), { target: { value: '50' } });
      fireEvent.change(screen.getByLabelText(/Prix unitaire/), { target: { value: '1000' } });

      const submitButton = screen.getByRole('button', { name: /Créer/ });
      fireEvent.click(submitButton);

      await waitFor(() => {
        expect(creerProduit).toHaveBeenCalledWith(expect.objectContaining({
          code: 'PRD002',
          nom: 'Test Produit',
          seuil_alerte: 50,
          prix_unitaire: 1000
        }));
      });
    });

    it('modifie un produit existant avec succès', async () => {
      renderWithProviders('1');

      await waitFor(() => {
        expect(screen.getByDisplayValue(mockProduct.nom)).toBeInTheDocument();
      });

      fireEvent.change(screen.getByLabelText(/Nom/), { target: { value: 'Nouveau Nom' } });
      
      const submitButton = screen.getByRole('button', { name: /Modifier/ });
      fireEvent.click(submitButton);

      await waitFor(() => {
        expect(modifierProduit).toHaveBeenCalledWith('1', expect.objectContaining({
          nom: 'Nouveau Nom'
        }));
      });
    });

    it('affiche une confirmation avant de quitter avec des modifications', async () => {
      renderWithProviders();

      fireEvent.change(screen.getByLabelText(/Nom/), { target: { value: 'Test' } });
      
      const cancelButton = screen.getByRole('button', { name: /Annuler/ });
      fireEvent.click(cancelButton);

      expect(await screen.findByText(/Confirmer les modifications/)).toBeInTheDocument();
    });
  });

  describe('Accessibilité', () => {
    it('a des labels ARIA appropriés', () => {
      renderWithProviders();

      expect(screen.getByLabelText(/Code du produit/)).toBeInTheDocument();
      expect(screen.getByLabelText(/Nom du produit/)).toBeInTheDocument();
      expect(screen.getByLabelText(/Catégorie du produit/)).toBeInTheDocument();
    });

    it('a des messages d\'erreur accessibles', async () => {
      renderWithProviders();

      const codeInput = screen.getByLabelText(/Code/);
      fireEvent.change(codeInput, { target: { value: 'ab' } });
      fireEvent.blur(codeInput);

      const errorMessage = await screen.findByText(/Le code doit contenir au moins 3 caractères/);
      expect(errorMessage).toHaveAttribute('id');
      expect(codeInput).toHaveAttribute('aria-describedby', expect.stringContaining(errorMessage.id));
    });

    it('gère la navigation au clavier', () => {
      renderWithProviders();

      const codeInput = screen.getByLabelText(/Code/);
      const nomInput = screen.getByLabelText(/Nom/);

      codeInput.focus();
      expect(document.activeElement).toBe(codeInput);

      fireEvent.keyDown(codeInput, { key: 'Tab' });
      expect(document.activeElement).toBe(nomInput);
    });

    it('a des tooltips informatifs', () => {
      renderWithProviders();

      expect(screen.getByTitle(/Code unique du produit/)).toBeInTheDocument();
      expect(screen.getByTitle(/Type de produit/)).toBeInTheDocument();
      expect(screen.getByTitle(/Niveau de stock minimum/)).toBeInTheDocument();
    });
  });
});
