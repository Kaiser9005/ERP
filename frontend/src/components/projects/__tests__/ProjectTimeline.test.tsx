import React from 'react';
import { render, screen } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from 'react-query';
import ProjectTimeline from '../ProjectTimeline';
import { getProjectTimeline } from '../../../services/projects';

jest.mock('../../../services/projects');

const mockEvents = [
  {
    id: '1',
    title: 'Début projet',
    start: new Date('2024-01-20'),
    end: new Date('2024-01-20'),
    type: 'PROJECT_START'
  },
  {
    id: '2',
    title: 'Fin projet',
    start: new Date('2024-03-20'),
    end: new Date('2024-03-20'),
    type: 'PROJECT_END'
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

describe('ProjectTimeline', () => {
  beforeEach(() => {
    (getProjectTimeline as jest.Mock).mockResolvedValue(mockEvents);
  });

  it('affiche le titre', () => {
    renderWithProviders(<ProjectTimeline />);
    
    expect(screen.getByText('Timeline des Projets')).toBeInTheDocument();
  });

  it('affiche le calendrier avec les traductions', () => {
    renderWithProviders(<ProjectTimeline />);
    
    expect(screen.getByText("Aujourd'hui")).toBeInTheDocument();
    expect(screen.getByText('Mois')).toBeInTheDocument();
    expect(screen.getByText('Semaine')).toBeInTheDocument();
  });

  it('affiche les événements', async () => {
    renderWithProviders(<ProjectTimeline />);
    
    expect(await screen.findByText('Début projet')).toBeInTheDocument();
    expect(await screen.findByText('Fin projet')).toBeInTheDocument();
  });

  it('gère les erreurs de chargement', async () => {
    (getProjectTimeline as jest.Mock).mockRejectedValue(new Error('Erreur de chargement'));
    
    renderWithProviders(<ProjectTimeline />);
    
    expect(await screen.findByText('Aucun événement dans cette période')).toBeInTheDocument();
  });
});