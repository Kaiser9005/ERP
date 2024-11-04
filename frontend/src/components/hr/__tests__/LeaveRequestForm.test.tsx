import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from 'react-query';
import LeaveRequestForm from '../LeaveRequestForm';
import { createLeaveRequest } from '../../../services/hr';

jest.mock('../../../services/hr');

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

describe('LeaveRequestForm', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('affiche le formulaire quand il est ouvert', () => {
    renderWithProviders(
      <LeaveRequestForm 
        open={true}
        onClose={mockOnClose}
        employeeId="1"
      />
    );
    
    expect(screen.getByText('Nouvelle Demande de Congé')).toBeInTheDocument();
    expect(screen.getByLabelText('Type de Congé')).toBeInTheDocument();
    expect(screen.getByLabelText('Date de Début')).toBeInTheDocument();
    expect(screen.getByLabelText('Date de Fin')).toBeInTheDocument();
  });

  it('valide les champs requis', async () => {
    renderWithProviders(
      <LeaveRequestForm 
        open={true}
        onClose={mockOnClose}
        employeeId="1"
      />
    );
    
    fireEvent.click(screen.getByText('Soumettre'));
    
    expect(await screen.findByText('Le type de congé est requis')).toBeInTheDocument();
    expect(await screen.findByText('La date de début est requise')).toBeInTheDocument();
    expect(await screen.findByText('La date de fin est requise')).toBeInTheDocument();
  });

  it('vérifie que la date de fin est après la date de début', async () => {
    renderWithProviders(
      <LeaveRequestForm 
        open={true}
        onClose={mockOnClose}
        employeeId="1"
      />
    );
    
    // Simuler la sélection des dates
    const dateDebut = screen.getByLabelText('Date de Début');
    const dateFin = screen.getByLabelText('Date de Fin');
    
    fireEvent.change(dateDebut, { target: { value: '2024-02-15' } });
    fireEvent.change(dateFin, { target: { value: '2024-02-01' } });
    
    fireEvent.click(screen.getByText('Soumettre'));
    
    expect(await screen.findByText('La date de fin doit être après la date de début')).toBeInTheDocument();
  });

  it('soumet le formulaire avec des données valides', async () => {
    (createLeaveRequest as jest.Mock).mockResolvedValue({ id: '1' });
    
    renderWithProviders(
      <LeaveRequestForm 
        open={true}
        onClose={mockOnClose}
        employeeId="1"
      />
    );
    
    // Remplir le formulaire
    fireEvent.change(screen.getByLabelText('Type de Congé'), { target: { value: 'ANNUEL' } });
    fireEvent.change(screen.getByLabelText('Date de Début'), { target: { value: '2024-02-01' } });
    fireEvent.change(screen.getByLabelText('Date de Fin'), { target: { value: '2024-02-15' } });
    fireEvent.change(screen.getByLabelText('Motif'), { target: { value: 'Congés annuels' } });
    
    fireEvent.click(screen.getByText('Soumettre'));
    
    await waitFor(() => {
      expect(createLeaveRequest).toHaveBeenCalledWith({
        employe_id: '1',
        type_conge: 'ANNUEL',
        date_debut: '2024-02-01',
        date_fin: '2024-02-15',
        motif: 'Congés annuels'
      });
      expect(mockOnClose).toHaveBeenCalled();
    });
  });

  it('gère les erreurs de soumission', async () => {
    (createLeaveRequest as jest.Mock).mockRejectedValue(new Error('Erreur de création'));
    
    renderWithProviders(
      <LeaveRequestForm 
        open={true}
        onClose={mockOnClose}
        employeeId="1"
      />
    );
    
    fireEvent.change(screen.getByLabelText('Type de Congé'), { target: { value: 'ANNUEL' } });
    fireEvent.click(screen.getByText('Soumettre'));
    
    expect(await screen.findByText('Une erreur est survenue')).toBeInTheDocument();
    expect(mockOnClose).not.toHaveBeenCalled();
  });
});