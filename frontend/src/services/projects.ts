import { api } from './api';
import { Project, ProjectStats, ProjectBase, ProjectList } from '../types/project';

export const getProjectStats = async (): Promise<ProjectStats> => {
  const { data } = await api.get<ProjectStats>('/api/v1/projects/stats');
  return data;
};

export const getProjects = async (
  page: number = 1,
  size: number = 10,
  filters?: {
    status?: string;
    search?: string;
  }
): Promise<ProjectList> => {
  const params = new URLSearchParams({
    page: page.toString(),
    size: size.toString()
  });

  if (filters?.status) params.append('status', filters.status);
  if (filters?.search) params.append('search', filters.search);

  const { data } = await api.get<ProjectList>(`/api/v1/projects?${params.toString()}`);
  return data;
};

export const getProject = async (id: string): Promise<Project> => {
  const { data } = await api.get<Project>(`/api/v1/projects/${id}`);
  return data;
};

export const createProject = async (projectData: ProjectBase): Promise<Project> => {
  const { data } = await api.post<Project>('/api/v1/projects', projectData);
  return data;
};

export const updateProject = async (id: string, projectData: Partial<ProjectBase>): Promise<Project> => {
  const { data } = await api.put<Project>(`/api/v1/projects/${id}`, projectData);
  return data;
};

export const deleteProject = async (id: string): Promise<void> => {
  await api.delete(`/api/v1/projects/${id}`);
};

export const uploadDocument = async (projectId: string, file: File, type: string): Promise<void> => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('type', type);

  await api.post(`/api/v1/projects/${projectId}/documents`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  });
};

export const deleteDocument = async (projectId: string, documentId: string): Promise<void> => {
  await api.delete(`/api/v1/projects/${projectId}/documents/${documentId}`);
};

export const getProjectProgress = async (projectId: string): Promise<{
  completion_percentage: number;
  tasks_completed: number;
  total_tasks: number;
  hours_spent: number;
  estimated_hours: number;
}> => {
  const { data } = await api.get(`/api/v1/projects/${projectId}/progress`);
  return data;
};

export const getProjectTimeline = async (projectId: string): Promise<{
  planned_start: string;
  planned_end: string;
  actual_start?: string;
  actual_end?: string;
  milestones: Array<{
    date: string;
    description: string;
    completed: boolean;
  }>;
}> => {
  const { data } = await api.get(`/api/v1/projects/${projectId}/timeline`);
  return data;
};

export const getProjectRisks = async (projectId: string): Promise<{
  total_risks: number;
  high_priority: number;
  medium_priority: number;
  low_priority: number;
  mitigated: number;
  active: number;
}> => {
  const { data } = await api.get(`/api/v1/projects/${projectId}/risks`);
  return data;
};
