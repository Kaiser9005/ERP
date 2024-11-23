import { render, screen } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import WeatherWidget from '../WeatherWidget';
import { productionService } from '../../../services/production';

// Mock du service
jest.mock('../../../services/production', () => ({
  productionService: {
    getWeatherData: jest.fn()
  }
}));

const mockWeatherData = {
  temperature: 25,
  humidity: 65,
  precipitation: 2.5
};

describe('WeatherWidget', () => {
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

  it('affiche les données météorologiques', async () => {
    (productionService.getWeatherData as jest.Mock).mockResolvedValue(mockWeatherData);

    render(
      <QueryClientProvider client={queryClient}>
        <WeatherWidget />
      </QueryClientProvider>
    );

    // Vérifie l'état de chargement
    expect(screen.getByRole('progressbar')).toBeInTheDocument();

    // Vérifie le titre
    expect(await screen.findByText('Conditions Météorologiques')).toBeInTheDocument();

    // Vérifie les données météo
    expect(screen.getByText('25°C')).toBeInTheDocument();
    expect(screen.getByText('65%')).toBeInTheDocument();
    expect(screen.getByText('2.5mm')).toBeInTheDocument();

    // Vérifie les labels
    expect(screen.getByText('Température')).toBeInTheDocument();
    expect(screen.getByText('Humidité')).toBeInTheDocument();
    expect(screen.getByText('Précipitations')).toBeInTheDocument();
  });

  it('affiche un message quand il n\'y a pas de données', async () => {
    (productionService.getWeatherData as jest.Mock).mockResolvedValue(null);

    render(
      <QueryClientProvider client={queryClient}>
        <WeatherWidget />
      </QueryClientProvider>
    );

    // Vérifie le message d'absence de données
    expect(await screen.findByText('Données météo non disponibles')).toBeInTheDocument();
  });

  it('utilise la bonne configuration de react-query', () => {
    render(
      <QueryClientProvider client={queryClient}>
        <WeatherWidget />
      </QueryClientProvider>
    );

    // Vérifie que le service est appelé avec les bons paramètres
    expect(productionService.getWeatherData).toHaveBeenCalledWith('current');

    // Vérifie que la requête est configurée correctement
    const queries = queryClient.getQueryCache().findAll();
    const weatherQuery = queries.find(
      query => Array.isArray(query.queryKey) && 
      query.queryKey[0] === 'weather' && 
      query.queryKey[1] === 'current'
    );

    expect(weatherQuery).toBeDefined();
  });
});
