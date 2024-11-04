import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from 'react-query';
import { MemoryRouter, Routes, Route } from 'react-router-dom';
import ProjectForm from '../ProjectForm';
import { createProject, updateProject, getProject } from '../../../services/projects';

jest.mock('../../../services/projects');

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
          <Route path="/projects" element={<div>Projects Page</div>} />
        </Routes>
      </MemoryRouter>
    </QueryClientProvider>
  );
};

describe('ProjectForm', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('affiche le formulaire de création', () => {
    renderWithProviders(<ProjectForm />);
    
    expect(screen.getByText('Nouveau Projet')).toBeInTheDocument();
    expect(screen.getByLabelText('Code')).toBeInTheDocument();
    expect(screen.getByLabelText('Nom')).toBeInTheDocument();
    expect(screen.getByLabelText('Description')).toBeInTheDocument();
  });

  it('valide les champs requis', async () => {
    renderWithProviders(<ProjectForm />);
    
    fireEvent.click(screen.getByText('Créer'));
    
    expect(await screen.findByText('Le code est requis')).toBeInTheDocument();
    expect(await screen.findByText('Le nom est requis')).toBeInTheDocument();
    expect(await screen.findByText('La date de début est requise')).toBeInTheDocument();
  });

  it('soumet le formulaire avec des données valides', async () => {
    (createProject as jest.Mock).mockResolvedValue({ id: '1' });
    
    renderWithProviders(<ProjectForm />);
    
    fireEvent.change(screen.getByLabelText('Code'), { target: { value: 'PRJ001' } });
    fireEvent.change(screen.getByLabelText('Nom'), { target: { value: 'Nouveau Projet' } });
    fireEvent.change(screen.getByLabelText('Description'), { target: { value: 'Description du projet' } });
    
    fireEvent.click(screen.getByText('Créer'));
    
    await waitFor(() => {
      expect(createProject).toHaveBeenCalledWith({
        code: 'PRJ001',
        nom: 'Nouveau Projet',
        description: 'Description du projet'
      });
    });
  });

  it('gère les erreurs de soumission', async () => {
    (createProject as jest.Mock).mockRejectedValue(new Error('Erreur de création'));
    
    renderWithProviders(<ProjectForm />);
    
    fireEvent.change(screen.getByLabelText('Code'), { target: { value: 'PRJ001' } });
    fireEvent.click(screen.getByText('Créer'));
    
    expect(await screen.findByText('Une erreur est survenue')).toBeInTheDocument();
  });
});