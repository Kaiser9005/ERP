import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from 'react-query';
import StockMovementDialog from '../StockMovementDialog';
import { createMovement } from '../../../services/inventory';

jest.mock('../../../services/inventory');

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: false,
    },
  },
});

const mockOnClose = jest.fn();

const renderWithProviders = (component: React.ReactElement) => {
  return render(
    <QueryClientProvider client={queryClient}>
      {component}
    </QueryClientProvider>
  );
};

describe('StockMovementDialog', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('affiche le dialogue quand il est ouvert', () => {
    renderWithProviders(
      <StockMovementDialog 
        open={true}
        onClose={mockOnClose}
        productId="1"
      />
    );
    
    expect(screen.getByText('Nouveau Mouvement de Stock')).toBeInTheDocument();
  });

  it('valide les champs requis', async () => {
    renderWithProviders(
      <StockMovementDialog 
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
    (createMovement as jest.Mock).mockResolvedValue({ id: '1' });
    
    renderWithProviders(
      <StockMovementDialog 
        open={true}
        onClose={mockOnClose}
        productId="1"
      />
    );
    
    fireEvent.change(screen.getByLabelText('Quantité'), { target: { value: '100' } });
    fireEvent.change(screen.getByLabelText('Type'), { target: { value: 'ENTREE' } });
    
    fireEvent.click(screen.getByText('Enregistrer'));
    
    await waitFor(() => {
      expect(createMovement).toHaveBeenCalledWith({
        productId: '1',
        quantity: 100,
        type: 'ENTREE'
      });
      expect(mockOnClose).toHaveBeenCalled();
    });
  });

  it('gère les erreurs de soumission', async () => {
    (createMovement as jest.Mock).mockRejectedValue(new Error('Erreur de création'));
    
    renderWithProviders(
      <StockMovementDialog 
        open={true}
        onClose={mockOnClose}
        productId="1"
      />
    );
    
    fireEvent.change(screen.getByLabelText('Quantité'), { target: { value: '100' } });
    fireEvent.click(screen.getByText('Enregistrer'));
    
    expect(await screen.findByText('Une erreur est survenue')).toBeInTheDocument();
    expect(mockOnClose).not.toHaveBeenCalled();
  });
});