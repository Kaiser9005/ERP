import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from 'react-query';
import ProjectStats from '../ProjectStats';
import { projectService } from '../../../services/projects';

// Mock du service
jest.mock('../../../services/projects');

const mockStats = {
  projets_actifs: 5,
  total_projets: 10,
  variation_projets_actifs: 20,
  taches_completees: 25,
  total_taches: 40,
  taches_retard: 3,
  variation_taches_retard: -10,
  heures_travaillees: 120,
  variation_heures: 15,
  repartition: {
    en_cours: 5,
    en_attente: 2,
    termines: 2,
    en_retard: 1
  },
  taux_completion: 60,
  projets_termines: 6
};

describe('ProjectStats', () => {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: {
        retry: false,
      },
    },
  });

  beforeEach(() => {
    (projectService.getProjectStats as jest.Mock).mockResolvedValue(mockStats);
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  it('affiche correctement les statistiques des projets', async () => {
    render(
      <QueryClientProvider client={queryClient}>
        <ProjectStats />
      </QueryClientProvider>
    );

    // Vérifie le chargement initial
    expect(screen.getByText('Chargement...')).toBeInTheDocument();

    // Attend que les données soient chargées
    await waitFor(() => {
      expect(screen.getByText("Vue d'ensemble des Projets")).toBeInTheDocument();
    });

    // Vérifie les cartes de statistiques principales
    expect(screen.getByText('Projets Actifs')).toBeInTheDocument();
    expect(screen.getByText('5')).toBeInTheDocument(); // projets_actifs
    expect(screen.getByText('/ 10')).toBeInTheDocument(); // total_projets

    expect(screen.getByText('Tâches Complétées')).toBeInTheDocument();
    expect(screen.getByText('25')).toBeInTheDocument(); // taches_completees
    expect(screen.getByText('/ 40')).toBeInTheDocument(); // total_taches

    expect(screen.getByText('Tâches En Retard')).toBeInTheDocument();
    expect(screen.getByText('3')).toBeInTheDocument(); // taches_retard

    expect(screen.getByText('Heures Travaillées')).toBeInTheDocument();
    expect(screen.getByText('120')).toBeInTheDocument(); // heures_travaillees

    // Vérifie la répartition par statut
    expect(screen.getByText('Répartition par Statut')).toBeInTheDocument();
    expect(screen.getByText('En cours (5)')).toBeInTheDocument();
    expect(screen.getByText('En attente (2)')).toBeInTheDocument();
    expect(screen.getByText('Terminés (2)')).toBeInTheDocument();
    expect(screen.getByText('En retard (1)')).toBeInTheDocument();

    // Vérifie le taux de complétion
    expect(screen.getByText('Taux de Complétion')).toBeInTheDocument();
    expect(screen.getByText('60%')).toBeInTheDocument();
    expect(screen.getByText('6 projets terminés sur 10')).toBeInTheDocument();
  });

  it('affiche un message d\'erreur quand les données ne sont pas disponibles', async () => {
    (projectService.getProjectStats as jest.Mock).mockResolvedValue(null);

    render(
      <QueryClientProvider client={queryClient}>
        <ProjectStats />
      </QueryClientProvider>
    );

    await waitFor(() => {
      expect(screen.getByText('Aucune donnée disponible')).toBeInTheDocument();
    });
  });

  it('gère correctement les erreurs de chargement', async () => {
    (projectService.getProjectStats as jest.Mock).mockRejectedValue(new Error('Erreur de chargement'));

    render(
      <QueryClientProvider client={queryClient}>
        <ProjectStats />
      </QueryClientProvider>
    );

    // Vérifie d'abord le chargement
    expect(screen.getByText('Chargement...')).toBeInTheDocument();

    // Attend que l'erreur soit affichée
    await waitFor(() => {
      expect(screen.getByText('Aucune donnée disponible')).toBeInTheDocument();
    });
  });
});
