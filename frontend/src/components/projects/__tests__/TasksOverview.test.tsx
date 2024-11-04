import React from 'react';
import { render, screen } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from 'react-query';
import TasksOverview from '../TasksOverview';
import { getRecentTasks } from '../../../services/projects';

jest.mock('../../../services/projects');

const mockTasks = [
  {
    id: '1',
    titre: 'Tâche test',
    priorite: 'HAUTE',
    projet: {
      nom: 'Projet test'
    },
    date_fin_prevue: '2024-01-25T10:00:00Z'
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

describe('TasksOverview', () => {
  beforeEach(() => {
    (getRecentTasks as jest.Mock).mockResolvedValue(mockTasks);
  });

  it('affiche le titre', async () => {
    renderWithProviders(<TasksOverview />);
    
    expect(screen.getByText('Tâches Récentes')).toBeInTheDocument();
  });

  it('affiche les tâches avec leurs détails', async () => {
    renderWithProviders(<TasksOverview />);
    
    expect(await screen.findByText('Tâche test')).toBeInTheDocument();
    expect(await screen.findByText('Projet test')).toBeInTheDocument();
    expect(await screen.findByText('HAUTE')).toBeInTheDocument();
  });

  it('utilise les bonnes couleurs pour les priorités', async () => {
    renderWithProviders(<TasksOverview />);
    
    const priorityChip = await screen.findByText('HAUTE');
    expect(priorityChip).toHaveClass('MuiChip-colorWarning');
  });

  it('gère les erreurs de chargement', async () => {
    (getRecentTasks as jest.Mock).mockRejectedValue(new Error('Erreur de chargement'));
    
    renderWithProviders(<TasksOverview />);
    
    expect(screen.queryByText('Tâche test')).not.toBeInTheDocument();
  });
});