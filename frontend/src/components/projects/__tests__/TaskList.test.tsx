import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from 'react-query';
import TaskList from '../TaskList';
import { getProjectTasks } from '../../../services/projects';

jest.mock('../../../services/projects');

const mockTasks = [
  {
    id: '1',
    titre: 'Tâche test',
    priorite: 'HAUTE',
    statut: 'EN_COURS',
    date_fin_prevue: '2024-01-25T10:00:00Z',
    assignee: {
      prenom: 'Jean',
      nom: 'Dupont'
    }
  },
  {
    id: '2',
    titre: 'Tâche terminée',
    priorite: 'MOYENNE',
    statut: 'TERMINE',
    date_fin_prevue: '2024-01-20T10:00:00Z',
    assignee: null
  }
];

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
      {component}
    </QueryClientProvider>
  );
};

describe('TaskList', () => {
  beforeEach(() => {
    (getProjectTasks as jest.Mock).mockResolvedValue(mockTasks);
  });

  it('affiche la liste des tâches', async () => {
    renderWithProviders(<TaskList projectId="1" />);
    
    expect(await screen.findByText('Tâche test')).toBeInTheDocument();
    expect(await screen.findByText('Tâche terminée')).toBeInTheDocument();
  });

  it('affiche les priorités avec les bonnes couleurs', async () => {
    renderWithProviders(<TaskList projectId="1" />);
    
    const prioriteHaute = await screen.findByText('HAUTE');
    const prioriteMoyenne = await screen.findByText('MOYENNE');
    
    expect(prioriteHaute).toHaveClass('MuiChip-colorWarning');
    expect(prioriteMoyenne).toHaveClass('MuiChip-colorInfo');
  });

  it('affiche les statuts avec les bonnes couleurs', async () => {
    renderWithProviders(<TaskList projectId="1" />);
    
    const statutEnCours = await screen.findByText('EN_COURS');
    const statutTermine = await screen.findByText('TERMINE');
    
    expect(statutEnCours).toHaveClass('MuiChip-colorInfo');
    expect(statutTermine).toHaveClass('MuiChip-colorSuccess');
  });

  it('affiche correctement les assignations', async () => {
    renderWithProviders(<TaskList projectId="1" />);
    
    expect(await screen.findByText('Jean Dupont')).toBeInTheDocument();
    expect(await screen.findByText('-')).toBeInTheDocument();
  });

  it('ouvre le formulaire de nouvelle tâche', async () => {
    renderWithProviders(<TaskList projectId="1" />);
    
    const button = screen.getByText('Nouvelle Tâche');
    fireEvent.click(button);
    
    expect(screen.getByText('Nouvelle Tâche')).toBeInTheDocument();
  });

  it('gère les erreurs de chargement', async () => {
    (getProjectTasks as jest.Mock).mockRejectedValue(new Error('Erreur de chargement'));
    
    renderWithProviders(<TaskList projectId="1" />);
    
    expect(await screen.findByText('Une erreur est survenue')).toBeInTheDocument();
  });
});