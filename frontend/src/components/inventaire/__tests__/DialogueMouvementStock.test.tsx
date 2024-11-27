import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import { QueryClient, QueryClientProvider } from 'react-query';
import DialogueMouvementStock from '../DialogueMouvementStock';
import { creerMouvement, getProduit } from '../../../services/inventaire';
import { vi } from 'vitest';
import { TypeMouvement } from '../../../types/inventaire';

vi.mock('../../../services/inventaire');

const mockProduct = {
  id: '1',
  code: 'PRD001',
  nom: 'Engrais NPK',
  categorie: 'INTRANT',
  unite_mesure: 'KG',
  prix_unitaire: 1500,
  quantite_stock: 1000,
  seuil_alerte: 100
};

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: false,
    },
  },
});

const renderWithProviders = (props: {
  open: boolean;
  onClose: () => void;
  productId: string | null;
}) => {
  return render(
    <QueryClientProvider client={queryClient}>
      <DialogueMouvementStock {...props} />
    </QueryClientProvider>
  );
};

describe('DialogueMouvementStock', () => {
  const mockOnClose = vi.fn();
  
  beforeEach(() => {
    vi.clearAllMocks();
    (getProduit as any).mockResolvedValue(mockProduct);
    (creerMouvement as any).mockResolvedValue({ success: true });
  });

  describe('Affichage', () => {
    it('affiche les informations du produit', async () => {
      renderWithProviders({
        open: true,
        onClose: mockOnClose,
        productId: '1'
      });

      expect(await screen.findByText(/PRD001/)).toBeInTheDocument();
      expect(screen.getByText(/Engrais NPK/)).toBeInTheDocument();
      expect(screen.getByText(/Stock actuel: 1000 KG/)).toBeInTheDocument();
    });

    it('affiche tous les champs du formulaire', async () => {
      renderWithProviders({
        open: true,
        onClose: mockOnClose,
        productId: '1'
      });

      expect(screen.getByLabelText(/Type de mouvement/i)).toBeInTheDocument();
      expect(screen.getByLabelText(/Quantité/i)).toBeInTheDocument();
      expect(screen.getByLabelText(/Coût unitaire/i)).toBeInTheDocument();
      expect(screen.getByLabelText(/Référence/i)).toBeInTheDocument();
      expect(screen.getByLabelText(/Notes/i)).toBeInTheDocument();
    });
  });

  describe('Validation', () => {
    it('affiche une erreur si la quantité est négative', async () => {
      renderWithProviders({
        open: true,
        onClose: mockOnClose,
        productId: '1'
      });

      const quantiteInput = screen.getByLabelText(/Quantité/i);
      fireEvent.change(quantiteInput, { target: { value: '-10' } });
      fireEvent.blur(quantiteInput);

      expect(await screen.findByText(/quantité doit être positive/i)).toBeInTheDocument();
    });

    it('affiche une erreur si la référence est vide', async () => {
      renderWithProviders({
        open: true,
        onClose: mockOnClose,
        productId: '1'
      });

      const referenceInput = screen.getByLabelText(/Référence/i);
      fireEvent.change(referenceInput, { target: { value: '' } });
      fireEvent.blur(referenceInput);

      expect(await screen.findByText(/référence est requise/i)).toBeInTheDocument();
    });

    it('vérifie le stock disponible pour les sorties', async () => {
      renderWithProviders({
        open: true,
        onClose: mockOnClose,
        productId: '1'
      });

      const typeSelect = screen.getByLabelText(/Type de mouvement/i);
      fireEvent.mouseDown(typeSelect);
      const sortieOption = screen.getByText('Sortie');
      fireEvent.click(sortieOption);

      const quantiteInput = screen.getByLabelText(/Quantité/i);
      fireEvent.change(quantiteInput, { target: { value: '1500' } });
      fireEvent.blur(quantiteInput);

      expect(await screen.findByText(/Stock insuffisant/i)).toBeInTheDocument();
    });
  });

  describe('Soumission', () => {
    it('soumet le formulaire avec les données correctes', async () => {
      renderWithProviders({
        open: true,
        onClose: mockOnClose,
        productId: '1'
      });

      // Remplir le formulaire
      fireEvent.change(screen.getByLabelText(/Quantité/i), { target: { value: '100' } });
      fireEvent.change(screen.getByLabelText(/Référence/i), { target: { value: 'BON001' } });
      fireEvent.change(screen.getByLabelText(/Coût unitaire/i), { target: { value: '1500' } });
      fireEvent.change(screen.getByLabelText(/Notes/i), { target: { value: 'Test notes' } });

      // Soumettre
      fireEvent.click(screen.getByRole('button', { name: /Enregistrer/i }));

      await waitFor(() => {
        expect(creerMouvement).toHaveBeenCalledWith({
          produit_id: '1',
          type_mouvement: TypeMouvement.ENTREE,
          quantite: 100,
          reference_document: 'BON001',
          cout_unitaire: 1500,
          notes: 'Test notes'
        });
      });

      expect(mockOnClose).toHaveBeenCalled();
    });

    it('affiche une confirmation pour les sorties', async () => {
      renderWithProviders({
        open: true,
        onClose: mockOnClose,
        productId: '1'
      });

      // Sélectionner "Sortie"
      const typeSelect = screen.getByLabelText(/Type de mouvement/i);
      fireEvent.mouseDown(typeSelect);
      const sortieOption = screen.getByText('Sortie');
      fireEvent.click(sortieOption);

      // Remplir les champs requis
      fireEvent.change(screen.getByLabelText(/Quantité/i), { target: { value: '100' } });
      fireEvent.change(screen.getByLabelText(/Référence/i), { target: { value: 'BON001' } });

      // Soumettre
      fireEvent.click(screen.getByRole('button', { name: /Enregistrer/i }));

      // Vérifier la boîte de dialogue de confirmation
      expect(await screen.findByText(/Confirmer la sortie de stock/i)).toBeInTheDocument();
      expect(screen.getByText(/Stock après opération: 900 KG/i)).toBeInTheDocument();

      // Confirmer
      fireEvent.click(screen.getByRole('button', { name: /Confirmer/i }));

      await waitFor(() => {
        expect(creerMouvement).toHaveBeenCalled();
      });
    });

    it('gère les erreurs de soumission', async () => {
      (creerMouvement as any).mockRejectedValue(new Error('Erreur test'));

      renderWithProviders({
        open: true,
        onClose: mockOnClose,
        productId: '1'
      });

      fireEvent.change(screen.getByLabelText(/Quantité/i), { target: { value: '100' } });
      fireEvent.change(screen.getByLabelText(/Référence/i), { target: { value: 'BON001' } });

      fireEvent.click(screen.getByRole('button', { name: /Enregistrer/i }));

      expect(await screen.findByText('Erreur test')).toBeInTheDocument();
      expect(mockOnClose).not.toHaveBeenCalled();
    });
  });

  describe('Accessibilité', () => {
    it('gère la navigation au clavier', async () => {
      renderWithProviders({
        open: true,
        onClose: mockOnClose,
        productId: '1'
      });

      const typeSelect = screen.getByLabelText(/Type de mouvement/i);
      const quantiteInput = screen.getByLabelText(/Quantité/i);
      const referenceInput = screen.getByLabelText(/Référence/i);

      typeSelect.focus();
      expect(document.activeElement).toBe(typeSelect);

      fireEvent.keyDown(typeSelect, { key: 'Tab' });
      expect(document.activeElement).toBe(quantiteInput);

      fireEvent.keyDown(quantiteInput, { key: 'Tab' });
      expect(document.activeElement).toBe(referenceInput);
    });

    it('fournit des messages d\'erreur accessibles', async () => {
      renderWithProviders({
        open: true,
        onClose: mockOnClose,
        productId: '1'
      });

      const quantiteInput = screen.getByLabelText(/Quantité/i);
      fireEvent.change(quantiteInput, { target: { value: '-10' } });
      fireEvent.blur(quantiteInput);

      const errorMessage = await screen.findByText(/quantité doit être positive/i);
      expect(errorMessage).toHaveAttribute('id');
      expect(quantiteInput).toHaveAttribute('aria-describedby', errorMessage.id);
    });

    it('a des tooltips informatifs', async () => {
      renderWithProviders({
        open: true,
        onClose: mockOnClose,
        productId: '1'
      });

      const referenceTooltip = screen.getByTitle(/Numéro du document justificatif/i);
      expect(referenceTooltip).toBeInTheDocument();

      const typeTooltip = screen.getByTitle(/Choisissez le type d'opération/i);
      expect(typeTooltip).toBeInTheDocument();
    });
  });
});
