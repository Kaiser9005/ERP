import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { MemoryRouter, Routes, Route } from 'react-router-dom';
import TaskWeatherDetails from '../TaskWeatherDetails';
import { TaskWithWeather, TaskStatus, TaskPriority, TaskCategory } from '../../../types/task';

// Mock des paramètres de route
jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  useParams: () => ({
    taskId: '123'
  })
}));

const mockTaskData: TaskWithWeather = {
  id: 123,
  title: 'Tâche test',
  weather_dependent: true,
  weather_suitable: true,
  min_temperature: 15,
  max_temperature: 30,
  max_wind_speed: 20,
  max_precipitation: 5,
  weather_conditions: {
    temperature: 25,
    humidity: 60,
    precipitation: 0,
    wind_speed: 15,
    conditions: 'Ensoleillé',
    uv_index: 5,
    cloud_cover: 10
  },
  weather_warnings: ['Risque de vent fort dans l\'après-midi'],
  status: TaskStatus.EN_COURS,
  priority: TaskPriority.MOYENNE,
  category: TaskCategory.PRODUCTION,
  completion_percentage: 50,
  start_date: '2024-01-01T00:00:00Z',
  due_date: '2024-01-31T00:00:00Z',
  created_at: '',
  updated_at: '',
  resources: [],
  comments: [],
  dependencies: [],
  project_id: 0
};

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: false,
    },
  },
});

const renderWithProviders = (ui: React.ReactElement) => {
  return render(
    <QueryClientProvider client={queryClient}>
      <MemoryRouter initialEntries={['/tasks/123/weather']}>
        <Routes>
          <Route path="/tasks/:taskId/weather" element={ui} />
        </Routes>
      </MemoryRouter>
    </QueryClientProvider>
  );
};

describe('TaskWeatherDetails', () => {
  beforeEach(() => {
    // Mock de la requête fetch
    global.fetch = jest.fn(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve(mockTaskData),
      })
    ) as jest.Mock;
  });

  afterEach(() => {
    jest.clearAllMocks();
    queryClient.clear();
  });

  it('affiche un indicateur de chargement', () => {
    renderWithProviders(<TaskWeatherDetails />);
    expect(screen.getByRole('progressbar')).toBeInTheDocument();
  });

  it('affiche les détails météo de la tâche', async () => {
    renderWithProviders(<TaskWeatherDetails />);

    // Vérifie le titre
    expect(await screen.findByText('Tâche test')).toBeInTheDocument();

    // Vérifie le statut météo
    expect(screen.getByText('Conditions météo favorables')).toBeInTheDocument();

    // Vérifie les conditions actuelles
    expect(screen.getByText('25°C')).toBeInTheDocument();
    expect(screen.getByText('60%')).toBeInTheDocument();
    expect(screen.getByText('15 km/h')).toBeInTheDocument();
    expect(screen.getByText('0 mm')).toBeInTheDocument();
  });

  it('affiche les contraintes météorologiques', async () => {
    renderWithProviders(<TaskWeatherDetails />);

    // Vérifie les contraintes
    expect(await screen.findByText('15°C')).toBeInTheDocument();
    expect(screen.getByText('30°C')).toBeInTheDocument();
    expect(screen.getByText('20 km/h')).toBeInTheDocument();
    expect(screen.getByText('5 mm')).toBeInTheDocument();
  });

  it('affiche les alertes météo', async () => {
    renderWithProviders(<TaskWeatherDetails />);

    // Vérifie les alertes
    expect(await screen.findByText('Risque de vent fort dans l\'après-midi')).toBeInTheDocument();
  });

  it('affiche une erreur en cas d\'échec de la requête', async () => {
    const errorMessage = 'Erreur lors de la récupération des données';
    global.fetch = jest.fn(() =>
      Promise.resolve({
        ok: false,
        status: 500,
        statusText: errorMessage,
      })
    ) as jest.Mock;

    renderWithProviders(<TaskWeatherDetails />);
    
    expect(await screen.findByText(errorMessage)).toBeInTheDocument();
  });

  it('affiche un message pour les tâches indépendantes de la météo', async () => {
    const independentTask = {
      ...mockTaskData,
      weather_dependent: false
    };

    global.fetch = jest.fn(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve(independentTask),
      })
    ) as jest.Mock;

    renderWithProviders(<TaskWeatherDetails />);
    
    expect(await screen.findByText('Tâche indépendante de la météo')).toBeInTheDocument();
  });
});
