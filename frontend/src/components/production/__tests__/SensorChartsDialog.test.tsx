import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { SensorChartsDialog } from '../SensorChartsDialog';
import { useSensor, useSensorReadings, useSensorStats } from '../../../services/iot';
import { SensorType } from '../../../types/iot';

// Mock des services
jest.mock('../../../services/iot', () => ({
  useSensor: jest.fn(),
  useSensorReadings: jest.fn(),
  useSensorStats: jest.fn(),
}));

// Mock de recharts car il ne fonctionne pas bien avec jest
jest.mock('recharts', () => ({
  ResponsiveContainer: ({ children }: any) => <div>{children}</div>,
  LineChart: ({ children }: any) => <div>{children}</div>,
  Line: () => null,
  XAxis: () => null,
  YAxis: () => null,
  CartesianGrid: () => null,
  Tooltip: () => null,
}));

const mockSensor = {
  id: '1',
  code: 'TEMP-001',
  type: SensorType.TEMPERATURE_SOL,
  parcelle_id: 'parcelle-1',
  intervalle_lecture: 300,
  config: {},
  seuils_alerte: {
    min: 10,
    max: 35,
    critique_min: 5,
    critique_max: 40,
  },
  date_installation: '2024-01-01T00:00:00Z',
};

const mockReadings = [
  {
    id: 'reading-1',
    capteur_id: '1',
    timestamp: '2024-01-15T10:00:00Z',
    valeur: 22.5,
    unite: '°C',
    metadata: {},
  },
  {
    id: 'reading-2',
    capteur_id: '1',
    timestamp: '2024-01-15T10:05:00Z',
    valeur: 23.0,
    unite: '°C',
    metadata: {},
  },
];

const mockStats = {
  moyenne: 22.75,
  minimum: 22.5,
  maximum: 23.0,
  nombre_lectures: 2,
};

describe('SensorChartsDialog', () => {
  let queryClient: QueryClient;

  beforeEach(() => {
    queryClient = new QueryClient({
      defaultOptions: {
        queries: {
          retry: false,
        },
      },
    });

    (useSensor as jest.Mock).mockReturnValue({
      data: mockSensor,
      isLoading: false,
      error: null,
    });

    (useSensorReadings as jest.Mock).mockReturnValue({
      data: mockReadings,
      isLoading: false,
      error: null,
    });

    (useSensorStats as jest.Mock).mockReturnValue({
      data: mockStats,
      isLoading: false,
      error: null,
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
    (useSensor as jest.Mock).mockReturnValue({
      isLoading: true,
    });

    renderWithQuery(
      <SensorChartsDialog
        open={true}
        onClose={() => {}}
        sensorId="1"
      />
    );

    expect(screen.getByRole('progressbar')).toBeInTheDocument();
  });

  it('affiche une erreur en cas de problème', () => {
    (useSensor as jest.Mock).mockReturnValue({
      error: new Error('Erreur test'),
    });

    renderWithQuery(
      <SensorChartsDialog
        open={true}
        onClose={() => {}}
        sensorId="1"
      />
    );

    expect(screen.getByRole('alert')).toHaveTextContent(
      'Une erreur est survenue lors du chargement des données'
    );
  });

  it('affiche les informations du capteur', async () => {
    renderWithQuery(
      <SensorChartsDialog
        open={true}
        onClose={() => {}}
        sensorId="1"
      />
    );

    await waitFor(() => {
      expect(screen.getByText('TEMP-001 - Température du sol')).toBeInTheDocument();
    });
  });

  it('affiche les statistiques', async () => {
    renderWithQuery(
      <SensorChartsDialog
        open={true}
        onClose={() => {}}
        sensorId="1"
      />
    );

    await waitFor(() => {
      expect(screen.getByText('22.75 °C')).toBeInTheDocument(); // moyenne
      expect(screen.getByText('22.50 °C')).toBeInTheDocument(); // minimum
      expect(screen.getByText('23.00 °C')).toBeInTheDocument(); // maximum
    });
  });

  it('affiche les seuils configurés', async () => {
    renderWithQuery(
      <SensorChartsDialog
        open={true}
        onClose={() => {}}
        sensorId="1"
      />
    );

    await waitFor(() => {
      expect(screen.getByText('Seuil min')).toBeInTheDocument();
      expect(screen.getByText('10 °C')).toBeInTheDocument();
      expect(screen.getByText('Seuil max')).toBeInTheDocument();
      expect(screen.getByText('35 °C')).toBeInTheDocument();
      expect(screen.getByText('Seuil critique_min')).toBeInTheDocument();
      expect(screen.getByText('5 °C')).toBeInTheDocument();
      expect(screen.getByText('Seuil critique_max')).toBeInTheDocument();
      expect(screen.getByText('40 °C')).toBeInTheDocument();
    });
  });

  it('n\'affiche pas le dialogue quand open est false', () => {
    renderWithQuery(
      <SensorChartsDialog
        open={false}
        onClose={() => {}}
        sensorId="1"
      />
    );

    expect(screen.queryByText('TEMP-001')).not.toBeInTheDocument();
  });

  it('appelle onClose quand on clique sur le bouton fermer', async () => {
    const mockOnClose = jest.fn();

    renderWithQuery(
      <SensorChartsDialog
        open={true}
        onClose={mockOnClose}
        sensorId="1"
      />
    );

    const closeButton = screen.getByRole('button', { name: /close/i });
    closeButton.click();

    expect(mockOnClose).toHaveBeenCalled();
  });

  it('utilise les bonnes dates pour les requêtes', () => {
    renderWithQuery(
      <SensorChartsDialog
        open={true}
        onClose={() => {}}
        sensorId="1"
      />
    );

    expect(useSensorReadings).toHaveBeenCalledWith('1', expect.objectContaining({
      start_date: expect.any(String),
      end_date: expect.any(String),
    }));

    expect(useSensorStats).toHaveBeenCalledWith('1', expect.objectContaining({
      start_date: expect.any(String),
      end_date: expect.any(String),
    }));
  });
});
