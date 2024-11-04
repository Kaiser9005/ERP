import React from 'react';
import { render, screen } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from 'react-query';
import { MemoryRouter, Routes, Route } from 'react-router-dom';
import ProjectDetails from '../ProjectDetails';
import { getProject } from '../../../services/projects';

jest.mock('../../../services/projects');

const mockProject = {
  id: '1',
  code: 'PRJ001',
  nom: 'Projet test',
  statut: 'EN_COURS',
  budget: 1500000,
  date_debut: '2024-01-01',
  date_fin_prevue: '2024-06-30',
  taches: [
    {
      id: '1',
      statut: 'TERMINE'
    },
    {
      id: '2',
      statut: 'EN_COURS'
    }
  ]
};

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
        </Routes>
      </MemoryRouter>
    </QueryClientProvider>
  );
};

describe('ProjectDetails', () => {
  beforeEach(() => {
    (getProject as jest.Mock).mockResolvedValue(mockProject);
  });

  it('affiche les informations du projet', async () => {
    renderWithProviders(<ProjectDetails />);
    
    expect(await screen.findByText('Projet PRJ001')).toBeInTheDocument();
    expect(await screen.findByText('Projet test')).toBeInTheDocument();
    expect(await screen.findByText('1 500 000 FCFA')).toBeInTheDocument();
  });

  it('affiche le statut avec la bonne couleur', async () => {
    renderWithProviders(<ProjectDetails />);
    
    const statusChip = await screen.findByText('EN_COURS');
    expect(statusChip).toHaveClass('MuiChip-colorSuccess');
  });

  it('affiche les dates correctement', async () => {
    renderWithProviders(<ProjectDetails />);
    
    expect(await screen.findByText('1 janvier 2024')).toBeInTheDocument();
    expect(await screen.findByText('30 juin 2024')).toBeInTheDocument();
  });

  it('calcule et affiche la progression', async () => {
    renderWithProviders(<ProjectDetails />);
    
    expect(await screen.findByText('50%')).toBeInTheDocument();
    
    const progressBar = screen.getByRole('progressbar');
    expect(progressBar).toHaveAttribute('aria-valuenow', '50');
  });

  it('affiche la liste des tâches', async () => {
    renderWithProviders(<ProjectDetails />);
    
    expect(await screen.findByText('Tâches')).toBeInTheDocument();
  });

  it('gère les erreurs de chargement', async () => {
    (getProject as jest.Mock).mockRejectedValue(new Error('Erreur de chargement'));
    
    renderWithProviders(<ProjectDetails />);
    
    expect(await screen.findByText('Une erreur est survenue')).toBeInTheDocument();
  });

  it('affiche le bouton de modification', async () => {
    renderWithProviders(<ProjectDetails />);
    
    expect(await screen.findByText('Modifier')).toBeInTheDocument();
  });
});