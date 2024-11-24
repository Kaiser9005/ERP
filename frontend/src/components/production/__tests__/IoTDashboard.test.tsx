import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { IoTDashboard } from '../IoTDashboard';
import { useParcelleSensors, useCheckAllSensorsHealth } from '../../../services/iot';
import { SensorStatus } from '../../../types/iot';

// Mock des services
jest.mock('../../../services/iot', () => ({
  useParcelleSensors: jest.fn(),
  useCheckAllSensorsHealth: jest.fn(),
}));

const mockSensors = [
  {
    id: '1',
    code: 'TEMP-001',
    type: 'temperature_sol',
    status: SensorStatus.ACTIF,
    parcelle_id: 'parcelle-1',
    intervalle_lecture: 300,
    config: {},
    seuils_alerte: {
      min: 10,
      max: 35,
    },
    date_installation: '2024-01-01T00:00:00Z',
  },
];

const mockHealthData = [
  {
    sensor_id: '1',
    code: 'TEMP-001',
    health: {
      status: SensorStatus.ACTIF,
      message: 'Capteur fonctionnel',
      battery_level: 85,
      signal_quality: 92,
      last_reading: {
        id: 'reading-1',
        capteur_id: '1',
        timestamp: '2024-01-15T10:00:00Z',
        valeur: 22.5,
        unite: '°C',
      },
    },
  },
];

describe('IoTDashboard', () => {
  let queryClient: QueryClient;

  beforeEach(() => {
    queryClient = new QueryClient({
      defaultOptions: {
        queries: {
          retry: false,
        },
      },
    });

    (useParcelleSensors as jest.Mock).mockReturnValue({
      data: mockSensors,
      isLoading: false,
      error: null,
    });

    (useCheckAllSensorsHealth as jest.Mock).mockReturnValue({
      data: mockHealthData,
      isLoading: false,
      error: null,
      refetch: jest.fn(),
    });
  });

  const renderWithQuery = (ui: React.ReactElement) => {
    return render(
      <QueryClientProvider client={queryClient}>
        {ui}
      </QueryClientProvider>
    );
  };

  it('affiche un loader pendant le chargement', () => {
    (useParcelleSensors as jest.Mock).mockReturnValue({
      isLoading: true,
    });

    renderWithQuery(<IoTDashboard parcelleId="parcelle-1" />);
    expect(screen.getByRole('progressbar')).toBeInTheDocument();
  });

  it('affiche une erreur en cas de problème', () => {
    (useParcelleSensors as jest.Mock).mockReturnValue({
      error: new Error('Erreur test'),
    });

    renderWithQuery(<IoTDashboard parcelleId="parcelle-1" />);
    expect(screen.getByRole('alert')).toHaveTextContent(
      'Une erreur est survenue lors du chargement des données des capteurs'
    );
  });

  it('affiche un message quand il n\'y a pas de capteurs', () => {
    (useParcelleSensors as jest.Mock).mockReturnValue({
      data: [],
      isLoading: false,
      error: null,
    });

    renderWithQuery(<IoTDashboard parcelleId="parcelle-1" />);
    expect(screen.getByText('Aucun capteur n\'est installé sur cette parcelle')).toBeInTheDocument();
  });

  it('affiche la liste des capteurs', () => {
    renderWithQuery(<IoTDashboard parcelleId="parcelle-1" />);
    expect(screen.getByText('TEMP-001')).toBeInTheDocument();
    expect(screen.getByText('Température du sol')).toBeInTheDocument();
  });

  it('affiche les données de santé du capteur', () => {
    renderWithQuery(<IoTDashboard parcelleId="parcelle-1" />);
    expect(screen.getByText('Batterie: 85%')).toBeInTheDocument();
    expect(screen.getByText('Signal: 92%')).toBeInTheDocument();
    expect(screen.getByText('22.5 °C')).toBeInTheDocument();
  });

  it('ouvre le dialogue d\'ajout de capteur', () => {
    renderWithQuery(<IoTDashboard parcelleId="parcelle-1" />);
    const addButton = screen.getByRole('button', { name: /ajouter un capteur/i });
    fireEvent.click(addButton);
    expect(screen.getByText('Ajouter un nouveau capteur')).toBeInTheDocument();
  });

  it('ouvre le dialogue des graphiques', () => {
    renderWithQuery(<IoTDashboard parcelleId="parcelle-1" />);
    const chartButton = screen.getByRole('button', { name: /voir les graphiques/i });
    fireEvent.click(chartButton);
    expect(screen.getByText('TEMP-001 - Température du sol')).toBeInTheDocument();
  });

  it('rafraîchit les données de santé', async () => {
    const mockRefetch = jest.fn();
    (useCheckAllSensorsHealth as jest.Mock).mockReturnValue({
      data: mockHealthData,
      isLoading: false,
      error: null,
      refetch: mockRefetch,
    });

    renderWithQuery(<IoTDashboard parcelleId="parcelle-1" />);
    const refreshButton = screen.getByRole('button', { name: /rafraîchir/i });
    fireEvent.click(refreshButton);
    
    await waitFor(() => {
      expect(mockRefetch).toHaveBeenCalled();
    });
  });
});
