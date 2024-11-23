import { render, screen } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import RecentActivities from '../RecentActivities';
import { productionService } from '../../../services/production';

// Mock du service
jest.mock('../../../services/production', () => ({
  productionService: {
    getProductionEvents: jest.fn()
  }
}));

const mockActivities = [
  {
    id: '1',
    type: 'Récolte',
    date_debut: '2024-01-15T10:00:00Z',
    description: 'Récolte du maïs - Parcelle A'
  },
  {
    id: '2',
    type: 'Irrigation',
    date_debut: '2024-01-14T08:30:00Z',
    description: 'Irrigation des cultures - Zone B'
  },
  {
    id: '3',
    type: 'Fertilisation',
    date_debut: '2024-01-13T09:15:00Z',
    description: 'Application d\'engrais - Parcelle C'
  }
];

describe('RecentActivities', () => {
  let queryClient: QueryClient;

  beforeEach(() => {
    queryClient = new QueryClient({
      defaultOptions: {
        queries: {
          retry: false
        }
      }
    });
    jest.clearAllMocks();
  });

  it('affiche la liste des activités récentes', async () => {
    (productionService.getProductionEvents as jest.Mock).mockResolvedValue(mockActivities);

    render(
      <QueryClientProvider client={queryClient}>
        <RecentActivities />
      </QueryClientProvider>
    );

    // Vérifie l'état de chargement
    expect(screen.getByRole('progressbar')).toBeInTheDocument();

    // Vérifie le titre
    expect(await screen.findByText('Activités Récentes')).toBeInTheDocument();

    // Vérifie que les activités sont affichées
    expect(screen.getByText('Récolte')).toBeInTheDocument();
    expect(screen.getByText('Irrigation')).toBeInTheDocument();
    expect(screen.getByText('Fertilisation')).toBeInTheDocument();

    // Vérifie les descriptions
    expect(screen.getByText(/Récolte du maïs - Parcelle A/)).toBeInTheDocument();
    expect(screen.getByText(/Irrigation des cultures - Zone B/)).toBeInTheDocument();
    expect(screen.getByText(/Application d'engrais - Parcelle C/)).toBeInTheDocument();
  });

  it('affiche un message quand il n\'y a pas d\'activités', async () => {
    (productionService.getProductionEvents as jest.Mock).mockResolvedValue([]);

    render(
      <QueryClientProvider client={queryClient}>
        <RecentActivities />
      </QueryClientProvider>
    );

    // Vérifie le message d'absence d'activités
    expect(await screen.findByText('Aucune activité récente')).toBeInTheDocument();
  });

  it('utilise la bonne configuration de react-query', () => {
    render(
      <QueryClientProvider client={queryClient}>
        <RecentActivities />
      </QueryClientProvider>
    );

    // Vérifie que le service est appelé avec les bons paramètres
    expect(productionService.getProductionEvents).toHaveBeenCalledWith('all');

    // Vérifie que la requête est configurée correctement
    const queries = queryClient.getQueryCache().findAll();
    const eventsQuery = queries.find(
      query => Array.isArray(query.queryKey) && 
      query.queryKey[0] === 'production' && 
      query.queryKey[1] === 'events'
    );

    expect(eventsQuery).toBeDefined();
  });
});
