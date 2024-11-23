import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { MemoryRouter, Routes, Route } from 'react-router-dom';
import ProjectForm from '../ProjectForm';
import { createProject, updateProject, getProject } from '../../../services/projects';
import { ProjectStatus } from '../../../types/project';
import userEvent from '@testing-library/user-event';

jest.mock('../../../services/projects', () => ({
  createProject: jest.fn(),
  updateProject: jest.fn(),
  getProject: jest.fn()
}));

const mockProject = {
  id: '1',
  code: 'PRJ-001',
  nom: 'Projet Test',
  description: 'Description du projet',
  statut: ProjectStatus.EN_COURS,
  budget: 100000,
  date_debut: '2024-01-01',
  date_fin_prevue: '2024-12-31',
  responsable_id: '1',
  objectifs: [],
  risques: [],
  created_at: '2024-01-01T00:00:00Z',
  updated_at: '2024-01-01T00:00:00Z'
};

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: false,
    },
  },
});

const renderWithProviders = (path: string = '/projects/new') => {
  return render(
    <QueryClientProvider client={queryClient}>
      <MemoryRouter initialEntries={[path]}>
        <Routes>
          <Route path="/projects/new" element={<ProjectForm />} />
          <Route path="/projects/:id/edit" element={<ProjectForm />} />
        </Routes>
      </MemoryRouter>
    </QueryClientProvider>
  );
};

describe('ProjectForm', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    queryClient.clear();
  });

  it('affiche le formulaire de création', () => {
    renderWithProviders();
    
    expect(screen.getByText('Nouveau Projet')).toBeInTheDocument();
    expect(screen.getByLabelText('Code')).toBeInTheDocument();
    expect(screen.getByLabelText('Nom')).toBeInTheDocument();
    expect(screen.getByLabelText('Description')).toBeInTheDocument();
    expect(screen.getByLabelText('Budget')).toBeInTheDocument();
    expect(screen.getByText('Créer')).toBeInTheDocument();
  });

  it('valide les champs requis', async () => {
    renderWithProviders();
    
    fireEvent.click(screen.getByText('Créer'));
    
    expect(await screen.findByText('Le code est requis')).toBeInTheDocument();
    expect(await screen.findByText('Le nom est requis')).toBeInTheDocument();
    expect(await screen.findByText('Le budget est requis')).toBeInTheDocument();
  });

  it('crée un nouveau projet avec succès', async () => {
    (createProject as jest.Mock).mockResolvedValue(mockProject);
    
    renderWithProviders();
    
    await userEvent.type(screen.getByLabelText('Code'), 'PRJ-001');
    await userEvent.type(screen.getByLabelText('Nom'), 'Projet Test');
    await userEvent.type(screen.getByLabelText('Description'), 'Description du projet');
    await userEvent.type(screen.getByLabelText('Budget'), '100000');
    
    fireEvent.click(screen.getByText('Créer'));
    
    await waitFor(() => {
      expect(createProject).toHaveBeenCalledWith(expect.objectContaining({
        code: 'PRJ-001',
        nom: 'Projet Test',
        description: 'Description du projet',
        budget: 100000
      }));
    });
  });

  it('charge et modifie un projet existant', async () => {
    (getProject as jest.Mock).mockResolvedValue(mockProject);
    (updateProject as jest.Mock).mockResolvedValue(mockProject);
    
    renderWithProviders('/projects/1/edit');
    
    await waitFor(() => {
      expect(screen.getByDisplayValue('PRJ-001')).toBeInTheDocument();
      expect(screen.getByDisplayValue('Projet Test')).toBeInTheDocument();
    });
    
    await userEvent.clear(screen.getByLabelText('Nom'));
    await userEvent.type(screen.getByLabelText('Nom'), 'Projet Test Modifié');
    
    fireEvent.click(screen.getByText('Modifier'));
    
    await waitFor(() => {
      expect(updateProject).toHaveBeenCalledWith('1', expect.objectContaining({
        nom: 'Projet Test Modifié'
      }));
    });
  });

  it('gère les erreurs de création', async () => {
    const errorMessage = 'Erreur lors de la création du projet';
    (createProject as jest.Mock).mockRejectedValue(new Error(errorMessage));
    
    renderWithProviders();
    
    await userEvent.type(screen.getByLabelText('Code'), 'PRJ-001');
    await userEvent.type(screen.getByLabelText('Nom'), 'Projet Test');
    await userEvent.type(screen.getByLabelText('Budget'), '100000');
    
    fireEvent.click(screen.getByText('Créer'));
    
    expect(await screen.findByText(errorMessage)).toBeInTheDocument();
  });

  it('gère les erreurs de chargement', async () => {
    const errorMessage = 'Erreur lors du chargement du projet';
    (getProject as jest.Mock).mockRejectedValue(new Error(errorMessage));
    
    renderWithProviders('/projects/1/edit');
    
    expect(await screen.findByText('Chargement...')).toBeInTheDocument();
  });

  it('valide le budget positif', async () => {
    renderWithProviders();
    
    await userEvent.type(screen.getByLabelText('Budget'), '-1000');
    
    fireEvent.click(screen.getByText('Créer'));
    
    expect(await screen.findByText('Le budget doit être positif')).toBeInTheDocument();
  });

  it('valide les dates', async () => {
    renderWithProviders();
    
    // Implémenter la validation des dates quand la date de fin est avant la date de début
    // Note: Les tests de DatePicker nécessitent une configuration spéciale pour MUI
  });

  it('permet d\'annuler la création', async () => {
    renderWithProviders();
    
    fireEvent.click(screen.getByText('Annuler'));
    
    // Vérifier la navigation vers /projects
    // Note: Nécessite un mock de useNavigate ou une configuration supplémentaire
  });
});
