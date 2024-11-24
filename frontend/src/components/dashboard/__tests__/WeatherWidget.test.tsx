import { render, screen } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import WeatherWidget from '../WeatherWidget';
import { weatherService } from '../../../services/weather';
import type { WeatherData } from '../../../types/production';

// Mock du service
jest.mock('../../../services/weather', () => ({
  weatherService: {
    getCurrentWeather: jest.fn()
  }
}));

const mockWeatherData: WeatherData = {
  timestamp: '2024-01-01T12:00:00Z',
  temperature: 25,
  humidity: 65,
  precipitation: 2.5,
  wind_speed: 10,
  conditions: 'sunny',
  uv_index: 5,
  cloud_cover: 20,
  cached_at: '2024-01-01T12:00:00Z'
};

const mockWeatherDataWithRisks: WeatherData = {
  ...mockWeatherData,
  risks: {
    precipitation: {
      level: 'HIGH',
      message: "Risque d'inondation - Vérifier le drainage"
    },
    temperature: {
      level: 'MEDIUM',
      message: "Températures élevées - Surveillance recommandée"
    },
    level: 'HIGH'
  },
  recommendations: [
    "Vérifier les systèmes de drainage",
    "Reporter les activités de plantation"
  ]
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

  it('affiche les données météorologiques de base', async () => {
    (weatherService.getCurrentWeather as jest.Mock).mockResolvedValue(mockWeatherData);

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

    // Vérifie l'heure de mise à jour
    expect(screen.getByText(/Mis à jour/)).toBeInTheDocument();
  });

  it('affiche les alertes et recommandations quand le risque est élevé', async () => {
    (weatherService.getCurrentWeather as jest.Mock).mockResolvedValue(mockWeatherDataWithRisks);

    render(
      <QueryClientProvider client={queryClient}>
        <WeatherWidget />
      </QueryClientProvider>
    );

    // Vérifie l'alerte
    expect(await screen.findByText(/Risque d'inondation/)).toBeInTheDocument();

    // Vérifie les recommandations
    expect(screen.getByText('Recommandations :')).toBeInTheDocument();
    expect(screen.getByText('Vérifier les systèmes de drainage')).toBeInTheDocument();
  });

  it('affiche un message quand il n\'y a pas de données', async () => {
    (weatherService.getCurrentWeather as jest.Mock).mockResolvedValue(null);

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

    // Vérifie que le service est appelé
    expect(weatherService.getCurrentWeather).toHaveBeenCalled();

    // Vérifie que la requête est configurée correctement
    const queries = queryClient.getQueryCache().findAll();
    const weatherQuery = queries.find(
      query => Array.isArray(query.queryKey) && 
      query.queryKey[0] === 'weather' && 
      query.queryKey[1] === 'current'
    );

    expect(weatherQuery).toBeDefined();
    expect(weatherQuery?.meta?.staleTime).toBe(1000 * 60 * 30); // 30 minutes
    expect(weatherQuery?.meta?.refetchInterval).toBe(1000 * 60 * 30); // 30 minutes
  });
});
