import React from 'react';
import { render, screen } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from 'react-query';
import ProjectStats from '../ProjectStats';
import { getProjectStats } from '../../../services/projects';
import type { ProjectStats as ProjectStatsType } from '../../../types/project';

// Mock du service
jest.mock('../../../services/projects', () => ({
  getProjectStats: jest.fn()
}));

const mockStats: ProjectStatsType = {
  projets_actifs: 10,
  total_projets: 15,
  variation_projets_actifs: 20,
  taches_completees: 45,
  total_taches: 60,
  taches_retard: 5,
  variation_taches_retard: -10,
  heures_travaillees: 120,
  variation_heures: 15,
  repartition: {
    en_cours: 8,
    en_attente: 2,
    termines: 4,
    en_retard: 1
  },
  taux_completion: 75,
  projets_termines: 5
};

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: false,
    },
  },
});

const renderWithClient = (ui: React.ReactElement) => {
  return render(
    <QueryClientProvider client={queryClient}>
      {ui}
    </QueryClientProvider>
  );
};

describe('ProjectStats', () => {
  beforeEach(() => {
    (getProjectStats as jest.Mock).mockResolvedValue(mockStats);
  });

  afterEach(() => {
    jest.clearAllMocks();
    queryClient.clear();
  });

  it('affiche les statistiques des projets', async () => {
    renderWithClient(<ProjectStats />);

    // Vérifie le chargement initial
    expect(screen.getByText('Chargement...')).toBeInTheDocument();

    // Vérifie les données chargées
    expect(await screen.findByText('10')).toBeInTheDocument();
    expect(screen.getByText('Projets Actifs')).toBeInTheDocument();
    expect(screen.getByText('45')).toBeInTheDocument();
    expect(screen.getByText('Tâches Complétées')).toBeInTheDocument();
  });

  it('affiche le message d\'erreur quand les données sont indisponibles', async () => {
    (getProjectStats as jest.Mock).mockResolvedValue(null);
    
    renderWithClient(<ProjectStats />);
    
    expect(await screen.findByText('Aucune donnée disponible')).toBeInTheDocument();
  });

  it('affiche la répartition des projets', async () => {
    renderWithClient(<ProjectStats />);

    expect(await screen.findByText('En cours (8)')).toBeInTheDocument();
    expect(screen.getByText('En attente (2)')).toBeInTheDocument();
    expect(screen.getByText('Terminés (4)')).toBeInTheDocument();
    expect(screen.getByText('En retard (1)')).toBeInTheDocument();
  });

  it('affiche le taux de complétion', async () => {
    renderWithClient(<ProjectStats />);

    expect(await screen.findByText('75%')).toBeInTheDocument();
    expect(screen.getByText('5 projets terminés sur 15')).toBeInTheDocument();
  });
});
