import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from 'react-query';
import TaskForm from '../TaskForm';
import { createTask } from '../../../services/projects';

jest.mock('../../../services/projects');

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

describe('TaskForm', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('affiche le formulaire quand il est ouvert', () => {
    renderWithProviders(
      <TaskForm 
        open={true}
        onClose={mockOnClose}
        projectId="1"
      />
    );
    
    expect(screen.getByText('Nouvelle Tâche')).toBeInTheDocument();
  });

  it('valide les champs requis', async () => {
    renderWithProviders(
      <TaskForm 
        open={true}
        onClose={mockOnClose}
        projectId="1"
      />
    );
    
    fireEvent.click(screen.getByText('Créer'));
    
    expect(await screen.findByText('Le titre est requis')).toBeInTheDocument();
    expect(await screen.findByText('La priorité est requise')).toBeInTheDocument();
    expect(await screen.findByText('La date de fin est requise')).toBeInTheDocument();
  });

  it('soumet le formulaire avec des données valides', async () => {
    (createTask as jest.Mock).mockResolvedValue({ id: '1' });
    
    renderWithProviders(
      <TaskForm 
        open={true}
        onClose={mockOnClose}
        projectId="1"
      />
    );
    
    fireEvent.change(screen.getByLabelText('Titre'), { target: { value: 'Nouvelle tâche' } });
    fireEvent.change(screen.getByLabelText('Priorité'), { target: { value: 'MOYENNE' } });
    
    fireEvent.click(screen.getByText('Créer'));
    
    await waitFor(() => {
      expect(createTask).toHaveBeenCalled();
      expect(mockOnClose).toHaveBeenCalled();
    });
  });

  it('gère les erreurs de soumission', async () => {
    (createTask as jest.Mock).mockRejectedValue(new Error('Erreur de création'));
    
    renderWithProviders(
      <TaskForm 
        open={true}
        onClose={mockOnClose}
        projectId="1"
      />
    );
    
    fireEvent.change(screen.getByLabelText('Titre'), { target: { value: 'Nouvelle tâche' } });
    fireEvent.click(screen.getByText('Créer'));
    
    expect(await screen.findByText('Une erreur est survenue')).toBeInTheDocument();
    expect(mockOnClose).not.toHaveBeenCalled();
  });
});