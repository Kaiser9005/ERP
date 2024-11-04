import { api } from './api';

export interface ProjectStats {
  activeProjects: number;
  projectsVariation: {
    value: number;
    type: 'increase' | 'decrease';
  };
  completionRate: number;
  completionVariation: {
    value: number;
    type: 'increase' | 'decrease';
  };
  delayedTasks: number;
  delayedVariation: {
    value: number;
    type: 'increase' | 'decrease';
  };
  completedTasks: number;
  tasksVariation: {
    value: number;
    type: 'increase' | 'decrease';
  };
}

export interface Project {
  id: string;
  code: string;
  nom: string;
  description?: string;
  date_debut: string;
  date_fin_prevue: string;
  date_fin_reelle?: string;
  statut: string;
  budget?: number;
  responsable: {
    id: string;
    nom: string;
    prenom: string;
  };
  taches?: Task[];
}

export interface Task {
  id: string;
  titre: string;
  description?: string;
  priorite: string;
  statut: string;
  date_debut?: string;
  date_fin_prevue: string;
  date_fin_reelle?: string;
  assignee?: {
    id: string;
    nom: string;
    prenom: string;
  };
  projet: {
    id: string;
    nom: string;
  };
}

export const getProjectStats = async (): Promise<ProjectStats> => {
  const response = await api.get('/projects/stats');
  return response.data;
};

export const getProjects = async (): Promise<Project[]> => {
  const response = await api.get('/projects');
  return response.data;
};

export const getProject = async (id: string): Promise<Project> => {
  const response = await api.get(`/projects/${id}`);
  return response.data;
};

export const createProject = async (data: Partial<Project>): Promise<Project> => {
  const response = await api.post('/projects', data);
  return response.data;
};

export const updateProject = async (id: string, data: Partial<Project>): Promise<Project> => {
  const response = await api.put(`/projects/${id}`, data);
  return response.data;
};

export const getRecentTasks = async (): Promise<Task[]> => {
  const response = await api.get('/projects/tasks/recent');
  return response.data;
};

export const getProjectTimeline = async () => {
  const response = await api.get('/projects/timeline');
  return response.data.map((event: any) => ({
    ...event,
    start: new Date(event.start),
    end: new Date(event.end)
  }));
};