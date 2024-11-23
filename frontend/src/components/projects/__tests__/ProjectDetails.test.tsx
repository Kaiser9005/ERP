import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { MemoryRouter, Routes, Route } from 'react-router-dom';
import ProjectDetails from '../ProjectDetails';
import { getProject } from '../../../services/projects';
import { ProjectStatus } from '../../../types/project';

jest.mock('../../../services/projects', () => ({
  getProject: jest.fn()
}));

// Mock TaskList component pour simplifier les tests
jest.mock('../TaskList', () => {
  return function MockTaskList() {
    return <div data-testid="task-list">Liste des tâches</div>;
  };
});

const mockProject = {
  id: '1',
  code: 'PRJ-001',
  nom: 'Projet Test',
  description: 'Description du projet',
  statut: ProjectStatus.EN_COURS,
  budget: 100000,
  date_debut: '2024-01-01T00:00:00Z',
  date_fin_prevue: '2024-12-31T00:00:00Z',
  taches: [
    { id: '1', statut: 'TERMINEE' },
    { id: '2', statut: 'EN_COURS' }
  ],
  created_at: '2024-01-01T00:00:00Z',
  updated_at: '2024-01-01T00:00:00Z',
  responsable_id: '1'
};

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: false,
    },
  },
});

const renderWithProviders = (projectId: string = '1') => {
  return render(
    <QueryClientProvider client={queryClient}>
      <MemoryRouter initialEntries={[`/projects/${projectId}`]}>
        <Routes>
          <Route path="/projects/:id" element={<ProjectDetails />} />
        </Routes>
      </MemoryRouter>
    </QueryClientProvider>
  );
};

describe('ProjectDetails', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    queryClient.clear();
  });

  it('affiche un indicateur de chargement', () => {
    (getProject as jest.Mock).mockImplementation(() => new Promise(() => {}));
    renderWithProviders();
    expect(screen.getByRole('progressbar')).toBeInTheDocument();
  });

  it('affiche les détails du projet', async () => {
    (getProject as jest.Mock).mockResolvedValue(mockProject);
    renderWithProviders();

    await waitFor(() => {
      expect(screen.getByText('Projet PRJ-001')).toBeInTheDocument();
    });

    expect(screen.getByText('Projet Test')).toBeInTheDocument();
    expect(screen.getByText('Description du projet')).toBeInTheDocument();
    expect(screen.getByText('EN_COURS')).toBeInTheDocument();
    expect(screen.getByText('100 000,00 XAF')).toBeInTheDocument();
  });

  it('affiche la progression des tâches', async () => {
    (getProject as jest.Mock).mockResolvedValue(mockProject);
    renderWithProviders();

    await waitFor(() => {
      expect(screen.getByText('50%')).toBeInTheDocument();
    });
  });

  it('gère les erreurs de chargement', async () => {
    const errorMessage = 'Erreur de chargement';
    (getProject as jest.Mock).mockRejectedValue(new Error(errorMessage));
    renderWithProviders();

    expect(await screen.findByText(errorMessage)).toBeInTheDocument();
  });

  it('gère les projets non trouvés', async () => {
    (getProject as jest.Mock).mockResolvedValue(null);
    renderWithProviders();

    expect(await screen.findByText('Projet non trouvé')).toBeInTheDocument();
  });

  it('affiche la liste des tâches', async () => {
    (getProject as jest.Mock).mockResolvedValue(mockProject);
    renderWithProviders();

    await waitFor(() => {
      expect(screen.getByTestId('task-list')).toBeInTheDocument();
    });
  });

  it('formate correctement les dates', async () => {
    (getProject as jest.Mock).mockResolvedValue(mockProject);
    renderWithProviders();

    await waitFor(() => {
      expect(screen.getByText(/1 janvier 2024/)).toBeInTheDocument();
      expect(screen.getByText(/31 décembre 2024/)).toBeInTheDocument();
    });
  });

  it('gère un projet sans budget', async () => {
    const projectWithoutBudget = { ...mockProject, budget: undefined };
    (getProject as jest.Mock).mockResolvedValue(projectWithoutBudget);
    renderWithProviders();

    await waitFor(() => {
      expect(screen.getByText('0,00 XAF')).toBeInTheDocument();
    });
  });

  it('gère un projet sans tâches', async () => {
    const projectWithoutTasks = { ...mockProject, taches: [] };
    (getProject as jest.Mock).mockResolvedValue(projectWithoutTasks);
    renderWithProviders();

    await waitFor(() => {
      expect(screen.getByText('0%')).toBeInTheDocument();
    });
  });
});
