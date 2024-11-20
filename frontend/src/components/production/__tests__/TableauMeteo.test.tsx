import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import { QueryClient, QueryClientProvider } from 'react-query';
import TableauMeteo from '../TableauMeteo';
import { weatherService } from '../../../services/weather';

// Mock du service météo
jest.mock('../../../services/weather', () => ({
  weatherService: {
    getAgriculturalMetrics: jest.fn(),
    getWarningMessage: jest.fn(),
    getCacheAge: jest.fn()
  }
}));

const mockWeatherService = weatherService as jest.Mocked<typeof weatherService>;

describe('TableauMeteo', () => {
  const queryClient = new QueryClient();

  beforeEach(() => {
    mockWeatherService.getAgriculturalMetrics.mockResolvedValue({
      current_conditions: {
        timestamp: new Date().toISOString(),
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
    });

    mockWeatherService.getWarningMessage.mockReturnValue(null);
    mockWeatherService.getCacheAge.mockReturnValue('il y a 5 minutes');
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  it('affiche le titre et les conditions météorologiques actuelles', async () => {
    render(
      <QueryClientProvider client={queryClient}>
        <TableauMeteo />
      </QueryClientProvider>
    );

    // Vérifie le titre
    expect(screen.getByText('Tableau de Bord Météorologique')).toBeInTheDocument();

    // Vérifie les conditions actuelles
    expect(await screen.findByText(/Température : 25°C/)).toBeInTheDocument();
    expect(screen.getByText(/Humidité : 65%/)).toBeInTheDocument();
    expect(screen.getByText(/Précipitations : 0 mm/)).toBeInTheDocument();
    expect(screen.getByText(/Vitesse du vent : 10 km\/h/)).toBeInTheDocument();

    // Vérifie la dernière mise à jour
    expect(screen.getByText('Dernière mise à jour : il y a 5 minutes')).toBeInTheDocument();
  });

  it('affiche les risques et recommandations', async () => {
    render(
      <QueryClientProvider client={queryClient}>
        <TableauMeteo />
      </QueryClientProvider>
    );

    // Vérifie les risques
    expect(await screen.findByText(/Conditions de précipitation normales/)).toBeInTheDocument();
    expect(screen.getByText(/Températures élevées - Surveillance recommandée/)).toBeInTheDocument();

    // Vérifie les recommandations
    expect(screen.getByText(/Maintenir une surveillance de l'hydratation des plants/)).toBeInTheDocument();
    expect(screen.getByText(/Conditions favorables pour les activités agricoles/)).toBeInTheDocument();
  });

  it('affiche une alerte météo si nécessaire', async () => {
    mockWeatherService.getWarningMessage.mockReturnValue(
      'ALERTE MÉTÉO: Risque de fortes précipitations'
    );

    render(
      <QueryClientProvider client={queryClient}>
        <TableauMeteo />
      </QueryClientProvider>
    );

    expect(await screen.findByText(/ALERTE MÉTÉO/)).toBeInTheDocument();
  });

  it('affiche un indicateur de chargement', () => {
    mockWeatherService.getAgriculturalMetrics.mockImplementation(
      () => new Promise(() => {}) // Promise qui ne se résout jamais
    );

    render(
      <QueryClientProvider client={queryClient}>
        <TableauMeteo />
      </QueryClientProvider>
    );

    expect(screen.getByRole('progressbar')).toBeInTheDocument();
  });

  it('affiche une erreur en cas de problème', async () => {
    mockWeatherService.getAgriculturalMetrics.mockRejectedValue(
      new Error('Erreur de connexion')
    );

    render(
      <QueryClientProvider client={queryClient}>
        <TableauMeteo />
      </QueryClientProvider>
    );

    expect(await screen.findByText(/Erreur lors du chargement des données météorologiques/)).toBeInTheDocument();
  });
});
