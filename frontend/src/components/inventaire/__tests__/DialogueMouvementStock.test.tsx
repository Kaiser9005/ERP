import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import DialogueMouvementStock from '../DialogueMouvementStock';
import { createMouvement } from '../../../services/inventaire';
import { vi } from 'vitest';
import type { CreateMouvementStock } from '../../../types/inventaire';

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

const mockOnClose = vi.fn();

const renderWithProviders = (component: React.ReactElement) => {
  return render(
    <QueryClientProvider client={queryClient}>
      {component}
    </QueryClientProvider>
  );
};

describe('DialogueMouvementStock', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('affiche le dialogue quand il est ouvert', () => {
    renderWithProviders(
      <DialogueMouvementStock 
        open={true}
        onClose={mockOnClose}
        productId="1"
      />
    );
    
    expect(screen.getByText('Nouveau Mouvement de Stock')).toBeInTheDocument();
  });

  it('valide les champs requis', async () => {
    renderWithProviders(
      <DialogueMouvementStock 
        open={true}
        onClose={mockOnClose}
        productId="1"
      />
    );
    
    fireEvent.click(screen.getByText('Enregistrer'));
    
    expect(await screen.findByText('La quantité est requise')).toBeInTheDocument();
    expect(await screen.findByText('Le type de mouvement est requis')).toBeInTheDocument();
  });

  it('soumet le formulaire avec des données valides', async () => {
    const mockMouvement: CreateMouvementStock = {
      produit_id: '1',
      type_mouvement: 'ENTREE',
      quantite: 100,
      reference_document: 'BL-2024-001',
      cout_unitaire: 1500
    };

    (createMouvement as any).mockResolvedValue({ id: '1', ...mockMouvement });
    
    renderWithProviders(
      <DialogueMouvementStock 
        open={true}
        onClose={mockOnClose}
        productId="1"
      />
    );
    
    fireEvent.change(screen.getByLabelText('Quantité'), { target: { value: '100' } });
    fireEvent.change(screen.getByLabelText('Type de Mouvement'), { target: { value: 'ENTREE' } });
    fireEvent.change(screen.getByLabelText('Référence Document'), { target: { value: 'BL-2024-001' } });
    fireEvent.change(screen.getByLabelText('Coût Unitaire'), { target: { value: '1500' } });
    
    fireEvent.click(screen.getByText('Enregistrer'));
    
    await waitFor(() => {
      expect(createMouvement).toHaveBeenCalledWith(mockMouvement);
      expect(mockOnClose).toHaveBeenCalled();
    });
  });

  it('gère les erreurs de soumission', async () => {
    (createMouvement as any).mockRejectedValue(new Error('Erreur test'));
    
    renderWithProviders(
      <DialogueMouvementStock 
        open={true}
        onClose={mockOnClose}
        productId="1"
      />
    );
    
    fireEvent.change(screen.getByLabelText('Quantité'), { target: { value: '100' } });
    fireEvent.change(screen.getByLabelText('Type de Mouvement'), { target: { value: 'ENTREE' } });
    fireEvent.click(screen.getByText('Enregistrer'));
    
    expect(await screen.findByText('Une erreur est survenue')).toBeInTheDocument();
    expect(mockOnClose).not.toHaveBeenCalled();
  });

  it('permet de sélectionner un entrepôt pour les transferts', async () => {
    renderWithProviders(
      <DialogueMouvementStock 
        open={true}
        onClose={mockOnClose}
        productId="1"
      />
    );
    
    fireEvent.change(screen.getByLabelText('Type de Mouvement'), { target: { value: 'TRANSFERT' } });
    
    expect(screen.getByLabelText('Entrepôt Source')).toBeInTheDocument();
    expect(screen.getByLabelText('Entrepôt Destination')).toBeInTheDocument();
  });

  it('réinitialise le formulaire à la fermeture', () => {
    renderWithProviders(
      <DialogueMouvementStock 
        open={true}
        onClose={mockOnClose}
        productId="1"
      />
    );
    
    fireEvent.change(screen.getByLabelText('Quantité'), { target: { value: '100' } });
    fireEvent.click(screen.getByText('Annuler'));
    
    expect(mockOnClose).toHaveBeenCalled();
  });
});
