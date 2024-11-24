import { render, screen } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import ProductionChart from '../ProductionChart';
import { productionService } from '../../../services/production';

// Mock du service
jest.mock('../../../services/production', () => ({
  productionService: {
    getProductionStats: jest.fn()
  }
}));

const mockProductionStats = [
  { mois: 'Janvier', quantite: 120 },
  { mois: 'Février', quantite: 150 },
  { mois: 'Mars', quantite: 180 }
];

describe('ProductionChart', () => {
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

  it('affiche le graphique avec les données', async () => {
    (productionService.getProductionStats as jest.Mock).mockResolvedValue(mockProductionStats);

    render(
      <QueryClientProvider client={queryClient}>
        <ProductionChart />
      </QueryClientProvider>
    );

    // Vérifie l'état de chargement
    expect(screen.getByRole('progressbar')).toBeInTheDocument();

    // Vérifie le titre
    expect(await screen.findByText('Production Mensuelle')).toBeInTheDocument();

    // Vérifie que les données sont affichées
    expect(screen.getByText('Janvier')).toBeInTheDocument();
    expect(screen.getByText('Février')).toBeInTheDocument();
    expect(screen.getByText('Mars')).toBeInTheDocument();
  });

  it('affiche un message quand il n\'y a pas de données', async () => {
    (productionService.getProductionStats as jest.Mock).mockResolvedValue(null);

    render(
      <QueryClientProvider client={queryClient}>
        <ProductionChart />
      </QueryClientProvider>
    );

    // Vérifie le message d'absence de données
    expect(await screen.findByText('Aucune donnée disponible')).toBeInTheDocument();
  });

  it('utilise la bonne configuration de react-query', () => {
    render(
      <QueryClientProvider client={queryClient}>
        <ProductionChart />
      </QueryClientProvider>
    );

    // Vérifie que le service est appelé avec les bons paramètres
    expect(productionService.getProductionStats).toHaveBeenCalledWith('global');

    // Vérifie que la requête est configurée correctement
    const queries = queryClient.getQueryCache().findAll();
    const productionQuery = queries.find(
      query => Array.isArray(query.queryKey) && 
      query.queryKey[0] === 'production' && 
      query.queryKey[1] === 'stats'
    );

    expect(productionQuery).toBeDefined();
  });
});
