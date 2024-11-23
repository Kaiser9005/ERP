import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { MemoryRouter, Routes, Route } from 'react-router-dom';
import { LocalizationProvider } from '@mui/x-date-pickers';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import fr from 'date-fns/locale/fr';
import TaskForm from '../TaskForm';
import { createTask, updateTask, getTask } from '../../../services/tasks';
import { TaskStatus, TaskPriority, TaskCategory } from '../../../types/task';

jest.mock('../../../services/tasks', () => ({
  createTask: jest.fn(),
  updateTask: jest.fn(),
  getTask: jest.fn()
}));

const mockTask = {
  id: '1',
  title: 'Tâche Test',
  description: 'Description de la tâche',
  status: TaskStatus.EN_COURS,
  priority: TaskPriority.MOYENNE,
  category: TaskCategory.PRODUCTION,
  start_date: '2024-01-01',
  due_date: '2024-12-31',
  project_id: 1,
  weather_dependent: false,
  completion_percentage: 0,
  resources: [],
  dependencies: []
};

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: false,
    },
  },
});

const renderWithProviders = (path: string = '/projects/1/tasks/new') => {
  return render(
    <QueryClientProvider client={queryClient}>
      <LocalizationProvider dateAdapter={AdapterDateFns} adapterLocale={fr}>
        <MemoryRouter initialEntries={[path]}>
          <Routes>
            <Route path="/projects/:projectId/tasks/new" element={<TaskForm />} />
            <Route path="/projects/:projectId/tasks/:taskId/edit" element={<TaskForm />} />
          </Routes>
        </MemoryRouter>
      </LocalizationProvider>
    </QueryClientProvider>
  );
};

describe('TaskForm', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    queryClient.clear();
  });

  it('affiche le formulaire de création', () => {
    renderWithProviders();
    
    expect(screen.getByText('Nouvelle Tâche')).toBeInTheDocument();
    expect(screen.getByLabelText('Titre')).toBeInTheDocument();
    expect(screen.getByLabelText('Description')).toBeInTheDocument();
    expect(screen.getByLabelText('Date de fin')).toBeInTheDocument();
  });

  it('valide les champs requis', async () => {
    renderWithProviders();
    
    fireEvent.click(screen.getByText('Créer'));
    
    expect(await screen.findByText('Le titre est requis')).toBeInTheDocument();
  });

  it('crée une nouvelle tâche avec succès', async () => {
    (createTask as jest.Mock).mockResolvedValue(mockTask);
    
    renderWithProviders();
    
    fireEvent.change(screen.getByLabelText('Titre'), {
      target: { value: 'Nouvelle Tâche' }
    });
    
    fireEvent.change(screen.getByLabelText('Description'), {
      target: { value: 'Description de la tâche' }
    });
    
    fireEvent.click(screen.getByText('Créer'));
    
    await waitFor(() => {
      expect(createTask).toHaveBeenCalledWith(expect.objectContaining({
        title: 'Nouvelle Tâche',
        description: 'Description de la tâche'
      }));
    });
  });

  it('charge et modifie une tâche existante', async () => {
    (getTask as jest.Mock).mockResolvedValue(mockTask);
    (updateTask as jest.Mock).mockResolvedValue(mockTask);
    
    renderWithProviders('/projects/1/tasks/1/edit');
    
    await waitFor(() => {
      expect(screen.getByDisplayValue('Tâche Test')).toBeInTheDocument();
    });
    
    fireEvent.change(screen.getByLabelText('Titre'), {
      target: { value: 'Tâche Modifiée' }
    });
    
    fireEvent.click(screen.getByText('Modifier'));
    
    await waitFor(() => {
      expect(updateTask).toHaveBeenCalledWith('1', expect.objectContaining({
        title: 'Tâche Modifiée'
      }));
    });
  });

  it('gère les erreurs de création', async () => {
    const errorMessage = 'Erreur lors de la création de la tâche';
    (createTask as jest.Mock).mockRejectedValue(new Error(errorMessage));
    
    renderWithProviders();
    
    fireEvent.change(screen.getByLabelText('Titre'), {
      target: { value: 'Nouvelle Tâche' }
    });
    
    fireEvent.click(screen.getByText('Créer'));
    
    expect(await screen.findByText(errorMessage)).toBeInTheDocument();
  });

  it('affiche les champs météo quand weather_dependent est activé', async () => {
    renderWithProviders();
    
    const weatherSwitch = screen.getByRole('checkbox');
    fireEvent.click(weatherSwitch);
    
    expect(screen.getByLabelText('Température minimale (°C)')).toBeInTheDocument();
    expect(screen.getByLabelText('Température maximale (°C)')).toBeInTheDocument();
    expect(screen.getByLabelText('Vitesse du vent maximale (km/h)')).toBeInTheDocument();
    expect(screen.getByLabelText('Précipitations maximales (mm)')).toBeInTheDocument();
  });

  it('valide les champs météo quand ils sont requis', async () => {
    renderWithProviders();
    
    const weatherSwitch = screen.getByRole('checkbox');
    fireEvent.click(weatherSwitch);
    
    fireEvent.click(screen.getByText('Créer'));
    
    expect(await screen.findByText('La température minimale est requise')).toBeInTheDocument();
    expect(await screen.findByText('La température maximale est requise')).toBeInTheDocument();
    expect(await screen.findByText('La vitesse du vent maximale est requise')).toBeInTheDocument();
    expect(await screen.findByText('Les précipitations maximales sont requises')).toBeInTheDocument();
  });

  it('permet d\'annuler la création', () => {
    renderWithProviders();
    
    fireEvent.click(screen.getByText('Annuler'));
    // La navigation sera testée via l'intégration
  });
});
