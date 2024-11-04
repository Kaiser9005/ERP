import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from 'react-query';
import RecolteForm from '../RecolteForm';
import { createRecolte } from '../../../services/production';

jest.mock('../../../services/production');

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

describe('RecolteForm', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('affiche le formulaire quand il est ouvert', () => {
    renderWithProviders(
      <RecolteForm 
        open={true}
        onClose={mockOnClose}
        parcelleId="1"
      />
    );
    
    expect(screen.getByText('Nouvelle Récolte')).toBeInTheDocument();
    expect(screen.getByLabelText('Quantité (kg)')).toBeInTheDocument();
    expect(screen.getByLabelText('Qualité')).toBeInTheDocument();
  });

  it('valide les champs requis', async () => {
    renderWithProviders(
      <RecolteForm 
        open={true}
        onClose={mockOnClose}
        parcelleId="1"
      />
    );
    
    fireEvent.click(screen.getByText('Enregistrer'));
    
    expect(await screen.findByText('La quantité est requise')).toBeInTheDocument();
    expect(await screen.findByText('La qualité est requise')).toBeInTheDocument();
  });

  it('soumet le formulaire avec des données valides', async () => {
    (createRecolte as jest.Mock).mockResolvedValue({ id: '1' });
    
    renderWithProviders(
      <RecolteForm 
        open={true}
        onClose={mockOnClose}
        parcelleId="1"
      />
    );
    
    fireEvent.change(screen.getByLabelText('Quantité (kg)'), { target: { value: '500' } });
    fireEvent.change(screen.getByLabelText('Qualité'), { target: { value: 'A' } });
    
    fireEvent.click(screen.getByText('Enregistrer'));
    
    await waitFor(() => {
      expect(createRecolte).toHaveBeenCalledWith({
        parcelle_id: '1',
        quantite_kg: '500',
        qualite: 'A'
      });
      expect(mockOnClose).toHaveBeenCalled();
    });
  });

  it('gère les erreurs de soumission', async () => {
    (createRecolte as jest.Mock).mockRejectedValue(new Error('Erreur de création'));
    
    renderWithProviders(
      <RecolteForm 
        open={true}
        onClose={mockOnClose}
        parcelleId="1"
      />
    );
    
    fireEvent.change(screen.getByLabelText('Quantité (kg)'), { target: { value: '500' } });
    fireEvent.click(screen.getByText('Enregistrer'));
    
    expect(await screen.findByText('Une erreur est survenue')).toBeInTheDocument();
    expect(mockOnClose).not.toHaveBeenCalled();
  });
});