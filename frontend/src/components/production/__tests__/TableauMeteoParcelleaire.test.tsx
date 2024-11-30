import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import TableauMeteoParcelleaire from '../TableauMeteoParcelleaire';
import { weatherService } from '../../../services/weather';
import { Parcelle } from '../../../types/production';
import { QueryClient, QueryClientProvider } from 'react-query';
import { AgriculturalMetrics } from '../../../types/weather';

// Mock du service météo
jest.mock('../../../services/weather', () => ({
  weatherService: {
    getAgriculturalMetrics: jest.fn(),
    getWarningMessage: jest.fn(),
    getCacheAge: jest.fn()
  }
}));

const mockWeatherService = weatherService as jest.Mocked<typeof weatherService>;

describe('TableauMeteoParcelleaire', () => {
  const queryClient = new QueryClient();
  
  const mockParcelle: Parcelle = {
    id: '1',
    code: 'P001',
    culture_type: 'palmier',
    surface_hectares: 10,
    statut: 'active',
    date_plantation: '2024-01-01',
    coordonnees_gps: {
      latitude: 0,
      longitude: 0
    },
    responsable_id: '1'
  };

  const mockMetrics: AgriculturalMetrics = {
    current_conditions: {
      date: new Date().toISOString(),
      temperature: 25,
      humidity: 65,
      precipitation: 0,
      wind_speed: 10,
      conditions: 'Ensoleillé',
      uv_index: 5,
      cloud_cover: 20,
      cached_at: new Date().toISOString()
    },
    risks: {
      precipitation: {
        level: 'LOW',
        message: 'Conditions de précipitation normales'
      },
      temperature: {
        level: 'MEDIUM',
        message: 'Températures élevées - Surveillance recommandée'
      },
      level: 'MEDIUM'
    },
    recommendations: [
      'Maintenir une surveillance de l\'hydratation des plants',
      'Conditions favorables pour les activités agricoles'
    ]
  };

  beforeEach(() => {
    mockWeatherService.getAgriculturalMetrics.mockResolvedValue(mockMetrics);
    mockWeatherService.getWarningMessage.mockReturnValue('Attention : températures élevées');
    mockWeatherService.getCacheAge.mockReturnValue('Il y a 5 minutes');
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  const renderWithQuery = (component: React.ReactElement) => {
    return render(
      <QueryClientProvider client={queryClient}>
        {component}
      </QueryClientProvider>
    );
  };

  it('affiche un message si aucune parcelle n\'est sélectionnée', () => {
    renderWithQuery(<TableauMeteoParcelleaire />);
    expect(screen.getByText(/Sélectionnez une parcelle pour voir les données météo/)).toBeInTheDocument();
  });

  it('affiche les conditions météorologiques de la parcelle', async () => {
    renderWithQuery(<TableauMeteoParcelleaire parcelle={mockParcelle} />);

    // Vérifie le titre avec le code de la parcelle
    expect(await screen.findByText(/Conditions Météorologiques - P001/)).toBeInTheDocument();

    // Vérifie les données météo
    expect(screen.getByText(/25°C/)).toBeInTheDocument();
    expect(screen.getByText(/65%/)).toBeInTheDocument();
    expect(screen.getByText(/5/)).toBeInTheDocument(); // UV Index
    expect(screen.getByText(/10 km\/h/)).toBeInTheDocument();
  });

  it('affiche les risques et recommandations', async () => {
    renderWithQuery(<TableauMeteoParcelleaire parcelle={mockParcelle} />);

    expect(await screen.findByText(/Conditions de précipitation normales/)).toBeInTheDocument();
    expect(screen.getByText(/Températures élevées - Surveillance recommandée/)).toBeInTheDocument();
    expect(screen.getByText(/Maintenir une surveillance de l'hydratation des plants/)).toBeInTheDocument();
    expect(screen.getByText(/Conditions favorables pour les activités agricoles/)).toBeInTheDocument();
  });

  it('affiche un indicateur de chargement', () => {
    mockWeatherService.getAgriculturalMetrics.mockImplementation(
      () => new Promise(() => {}) // Promise qui ne se résout jamais
    );

    renderWithQuery(<TableauMeteoParcelleaire parcelle={mockParcelle} />);
    expect(screen.getByText(/Chargement des données météo/)).toBeInTheDocument();
  });

  it('affiche une erreur en cas de problème', async () => {
    mockWeatherService.getAgriculturalMetrics.mockRejectedValue(
      new Error('Erreur lors du chargement des données météo')
    );

    renderWithQuery(<TableauMeteoParcelleaire parcelle={mockParcelle} />);
    expect(await screen.findByText(/Erreur lors du chargement des données météo/)).toBeInTheDocument();
  });

  it('appelle getAgriculturalMetrics', () => {
    renderWithQuery(<TableauMeteoParcelleaire parcelle={mockParcelle} />);
    expect(mockWeatherService.getAgriculturalMetrics).toHaveBeenCalled();
  });
});
