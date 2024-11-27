import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import WeatherDashboard from '../WeatherDashboard';
import { weatherService } from '../../../../services/weather';
import type { WeatherHRMetrics } from '../../../../types/weather';

// Mock du service météo
jest.mock('../../../../services/weather', () => ({
  weatherService: {
    getHRWeatherMetrics: jest.fn()
  }
}));

const mockWeatherData: WeatherHRMetrics = {
  current_conditions: {
    date: '2024-03-15T10:00:00Z',
    temperature: 32,
    humidity: 65,
    precipitation: 0,
    wind_speed: 15,
    conditions: 'Ensoleillé',
    uv_index: 7,
    cloud_cover: 10
  },
  risks: {
    temperature: {
      level: 'HIGH',
      message: 'Risque de stress thermique - Protection nécessaire'
    },
    precipitation: {
      level: 'LOW',
      message: 'Conditions normales'
    },
    wind: {
      level: 'MEDIUM',
      message: 'Vents modérés - Surveillance recommandée'
    },
    level: 'HIGH'
  },
  schedule_adjustments: [
    {
      date: '2024-03-15T10:00:00Z',
      original_schedule: { start: '09:00', end: '17:00' },
      adjusted_schedule: { start: '06:00', end: '14:00' },
      reason: 'Températures excessives - Horaires matinaux',
      affected_employees: ['emp1', 'emp2'],
      status: 'PROPOSED'
    }
  ],
  safety_requirements: [
    {
      weather_condition: 'high_temperature',
      required_equipment: ['chapeau', 'protection_solaire', 'eau'],
      optional_equipment: [],
      instructions: 'Port obligatoire des équipements de protection contre la chaleur'
    }
  ],
  training_needs: [
    {
      weather_type: 'high_temperature',
      required_training: 'Prévention des risques liés à la chaleur',
      validity_period: 12,
      refresher_frequency: 12,
      priority: 'HIGH'
    }
  ],
  compliance: [],
  alerts: [
    {
      type: 'SAFETY',
      level: 'CRITICAL',
      message: 'Risque de stress thermique - Protection nécessaire',
      affected_roles: ['outdoor_workers', 'field_supervisors']
    }
  ]
};

describe('WeatherDashboard', () => {
  beforeEach(() => {
    (weatherService.getHRWeatherMetrics as jest.Mock).mockResolvedValue(mockWeatherData);
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  it('affiche le titre du tableau de bord', async () => {
    render(<WeatherDashboard />);
    expect(screen.getByText('Tableau de Bord Météo RH')).toBeInTheDocument();
  });

  it('affiche un message de chargement', () => {
    render(<WeatherDashboard />);
    expect(screen.getByText('Chargement des données météo...')).toBeInTheDocument();
  });

  it('affiche les données météo après chargement', async () => {
    render(<WeatherDashboard />);

    await waitFor(() => {
      expect(screen.getByText('32°C')).toBeInTheDocument();
      expect(screen.getByText('0 mm')).toBeInTheDocument();
      expect(screen.getByText('15 km/h')).toBeInTheDocument();
    });
  });

  it('affiche les alertes météo', async () => {
    render(<WeatherDashboard />);

    await waitFor(() => {
      expect(screen.getByText('Risque de stress thermique - Protection nécessaire')).toBeInTheDocument();
    });
  });

  it('affiche les ajustements de planning', async () => {
    render(<WeatherDashboard />);

    await waitFor(() => {
      expect(screen.getByText('Températures excessives - Horaires matinaux')).toBeInTheDocument();
      expect(screen.getByText('Horaires ajustés : 06:00 - 14:00')).toBeInTheDocument();
    });
  });

  it('affiche les équipements requis', async () => {
    render(<WeatherDashboard />);

    await waitFor(() => {
      expect(screen.getByText('Équipements Requis')).toBeInTheDocument();
      expect(screen.getByText('chapeau')).toBeInTheDocument();
      expect(screen.getByText('protection_solaire')).toBeInTheDocument();
      expect(screen.getByText('eau')).toBeInTheDocument();
    });
  });

  it('gère les erreurs de chargement', async () => {
    (weatherService.getHRWeatherMetrics as jest.Mock).mockRejectedValue(new Error('Erreur API'));
    render(<WeatherDashboard />);

    await waitFor(() => {
      expect(screen.getByText('Erreur lors de la récupération des données météo')).toBeInTheDocument();
    });
  });
});
