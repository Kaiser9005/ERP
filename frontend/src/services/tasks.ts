import { Task, TaskFormData, TaskWithWeather, TaskList } from '../types/task';

const BASE_URL = '/api/v1';

export const getTasks = async (
  projectId: number,
  page: number = 1,
  status?: string,
  category?: string
): Promise<TaskList> => {
  const params = new URLSearchParams({
    page: page.toString()
  });

  if (status) params.append('status', status);
  if (category) params.append('category', category);

  const response = await fetch(
    `${BASE_URL}/projects/${projectId}/tasks?${params.toString()}`
  );

  if (!response.ok) {
    throw new Error('Erreur lors de la récupération des tâches');
  }

  return response.json();
};

export const getTask = async (taskId: number): Promise<Task> => {
  const response = await fetch(`${BASE_URL}/tasks/${taskId}`);

  if (!response.ok) {
    throw new Error('Erreur lors de la récupération de la tâche');
  }

  return response.json();
};

export const getTaskWeather = async (taskId: number): Promise<TaskWithWeather> => {
  const response = await fetch(`${BASE_URL}/tasks/${taskId}/weather`);

  if (!response.ok) {
    throw new Error('Erreur lors de la récupération des données météo');
  }

  return response.json();
};

export const createTask = async (taskData: TaskFormData): Promise<Task> => {
  const response = await fetch(`${BASE_URL}/tasks`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(taskData)
  });

  if (!response.ok) {
    throw new Error('Erreur lors de la création de la tâche');
  }

  return response.json();
};

export const updateTask = async (taskId: number, taskData: TaskFormData): Promise<Task> => {
  const response = await fetch(`${BASE_URL}/tasks/${taskId}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(taskData)
  });

  if (!response.ok) {
    throw new Error('Erreur lors de la mise à jour de la tâche');
  }

  return response.json();
};

export const deleteTask = async (taskId: number): Promise<void> => {
  const response = await fetch(`${BASE_URL}/tasks/${taskId}`, {
    method: 'DELETE'
  });

  if (!response.ok) {
    throw new Error('Erreur lors de la suppression de la tâche');
  }
};

export const getWeatherDependentTasks = async (): Promise<TaskWithWeather[]> => {
  const response = await fetch(`${BASE_URL}/tasks/weather-dependent`);

  if (!response.ok) {
    throw new Error('Erreur lors de la récupération des tâches météo-dépendantes');
  }

  return response.json();
};

export const updateTaskResource = async (
  taskId: number,
  resourceId: number,
  quantityUsed: number
): Promise<void> => {
  const response = await fetch(
    `${BASE_URL}/tasks/${taskId}/resources/${resourceId}?quantity_used=${quantityUsed}`,
    {
      method: 'PUT'
    }
  );

  if (!response.ok) {
    throw new Error("Erreur lors de la mise à jour de l'utilisation des ressources");
  }
};
