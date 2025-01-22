import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import { QueryClient, QueryClientProvider } from 'react-query';
import WidgetMeteo from '../WidgetMeteo';
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

describe('WidgetMeteo', () => {
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

  it('affiche les conditions météorologiques actuelles', async () => {
    render(
      <QueryClientProvider client={queryClient}>
        <WidgetMeteo />
      </QueryClientProvider>
    );

    // Vérifie le titre
    expect(screen.getByText('Conditions Météo')).toBeInTheDocument();

    // Vérifie la température
    expect(await screen.findByText('25°C')).toBeInTheDocument();

    // Vérifie l'humidité et les précipitations
    expect(screen.getByText('65% Humidité')).toBeInTheDocument();
    expect(screen.getByText('0mm Précip.')).toBeInTheDocument();

    // Vérifie les recommandations
    expect(screen.getByText(/Maintenir une surveillance/)).toBeInTheDocument();
    expect(screen.getByText(/Conditions favorables/)).toBeInTheDocument();

    // Vérifie l'âge du cache
    expect(screen.getByText('Mis à jour il y a 5 minutes')).toBeInTheDocument();
  });

  it('affiche une alerte météo si nécessaire', async () => {
    mockWeatherService.getWarningMessage.mockReturnValue(
      'ALERTE MÉTÉO: Risque de stress thermique pour les cultures'
    );

    render(
      <QueryClientProvider client={queryClient}>
        <WidgetMeteo />
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
        <WidgetMeteo />
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
        <WidgetMeteo />
      </QueryClientProvider>
    );

    expect(await screen.findByText(/Erreur lors du chargement des données météo/)).toBeInTheDocument();
  });
});
