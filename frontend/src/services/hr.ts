import { api } from './api';
import type { ApiResponse, UUID } from '../types/common';
import type { 
  Employee,
  Leave,
  Training,
  Attendance,
  EmployeeStats,
  LeaveType,
  LeaveStatus
} from '../types/hr';
import { QueryFunctionContext } from '@tanstack/react-query';

const BASE_URL = '/api/v1/hr';

// Types de retour des requêtes
export interface EmployeeListResponse {
  items: Employee[];
  total: number;
  page: number;
  pageSize: number;
}

export interface EmployeeFilter {
  search?: string;
  departement?: string;
  statut?: string;
  page?: number;
  pageSize?: number;
}

// Types pour les congés
export interface LeaveFormData {
  type: LeaveType;
  dateDebut: string;
  dateFin: string;
  motif: string;
  statut: LeaveStatus;
}

// Gestion des employés
export const getEmployees = async ({ queryKey }: QueryFunctionContext<readonly ['hr', 'employees']>): Promise<Employee[]> => {
  try {
    const response = await api.get<ApiResponse<EmployeeListResponse>>(`${BASE_URL}/employes`);
    return response.data.data.items;
  } catch (error) {
    throw new Error('Erreur lors de la récupération des employés');
  }
};

export const getEmployeesWithPagination = async (params: EmployeeFilter): Promise<EmployeeListResponse> => {
  try {
    const response = await api.get<ApiResponse<EmployeeListResponse>>(`${BASE_URL}/employes`, { params });
    return response.data.data;
  } catch (error) {
    throw new Error('Erreur lors de la récupération des employés');
  }
};

export const getEmployee = async (id: UUID): Promise<Employee> => {
  try {
    const response = await api.get<ApiResponse<Employee>>(`${BASE_URL}/employes/${id}`);
    return response.data.data;
  } catch (error) {
    throw new Error('Erreur lors de la récupération des détails de l\'employé');
  }
};

export const createEmployee = async (data: Omit<Employee, 'id'>): Promise<Employee> => {
  try {
    const response = await api.post<ApiResponse<Employee>>(`${BASE_URL}/employes`, data);
    return response.data.data;
  } catch (error) {
    throw new Error('Erreur lors de la création de l\'employé');
  }
};

export const updateEmployee = async (id: UUID, data: Partial<Employee>): Promise<Employee> => {
  try {
    const response = await api.patch<ApiResponse<Employee>>(`${BASE_URL}/employes/${id}`, data);
    return response.data.data;
  } catch (error) {
    throw new Error('Erreur lors de la mise à jour de l\'employé');
  }
};

export const deleteEmployee = async (id: UUID): Promise<void> => {
  try {
    await api.delete(`${BASE_URL}/employes/${id}`);
  } catch (error) {
    throw new Error('Erreur lors de la suppression de l\'employé');
  }
};

// Gestion des congés
export const getLeaves = async ({ queryKey }: QueryFunctionContext<readonly ['hr', 'leaves']>): Promise<Leave[]> => {
  try {
    const response = await api.get<ApiResponse<Leave[]>>(`${BASE_URL}/conges`);
    return response.data.data;
  } catch (error) {
    throw new Error('Erreur lors de la récupération des congés');
  }
};

export const getLeavesWithFilters = async (params: {
  employeeId?: UUID;
  statut?: LeaveStatus;
  dateDebut?: string;
  dateFin?: string;
}): Promise<Leave[]> => {
  try {
    const response = await api.get<ApiResponse<Leave[]>>(`${BASE_URL}/conges`, { params });
    return response.data.data;
  } catch (error) {
    throw new Error('Erreur lors de la récupération des congés');
  }
};

export const createLeave = async (data: LeaveFormData): Promise<Leave> => {
  try {
    const response = await api.post<ApiResponse<Leave>>(`${BASE_URL}/conges`, data);
    return response.data.data;
  } catch (error) {
    throw new Error('Erreur lors de la création du congé');
  }
};

export const updateLeave = async (id: UUID, data: Partial<LeaveFormData>): Promise<Leave> => {
  try {
    const response = await api.patch<ApiResponse<Leave>>(`${BASE_URL}/conges/${id}`, data);
    return response.data.data;
  } catch (error) {
    throw new Error('Erreur lors de la mise à jour du congé');
  }
};

export const approveLeave = async (id: UUID): Promise<Leave> => {
  try {
    const response = await api.post<ApiResponse<Leave>>(`${BASE_URL}/conges/${id}/approve`);
    return response.data.data;
  } catch (error) {
    throw new Error('Erreur lors de l\'approbation du congé');
  }
};

export const rejectLeave = async (id: UUID, motif: string): Promise<Leave> => {
  try {
    const response = await api.post<ApiResponse<Leave>>(`${BASE_URL}/conges/${id}/reject`, { motif });
    return response.data.data;
  } catch (error) {
    throw new Error('Erreur lors du refus du congé');
  }
};

// Gestion des formations
export const getTrainings = async ({ queryKey }: QueryFunctionContext<readonly ['hr', 'trainings']>): Promise<Training[]> => {
  try {
    const response = await api.get<ApiResponse<Training[]>>(`${BASE_URL}/formations`);
    return response.data.data;
  } catch (error) {
    throw new Error('Erreur lors de la récupération des formations');
  }
};

export const createTraining = async (data: Omit<Training, 'id'>): Promise<Training> => {
  try {
    const response = await api.post<ApiResponse<Training>>(`${BASE_URL}/formations`, data);
    return response.data.data;
  } catch (error) {
    throw new Error('Erreur lors de la création de la formation');
  }
};

export const updateTraining = async (id: UUID, data: Partial<Training>): Promise<Training> => {
  try {
    const response = await api.patch<ApiResponse<Training>>(`${BASE_URL}/formations/${id}`, data);
    return response.data.data;
  } catch (error) {
    throw new Error('Erreur lors de la mise à jour de la formation');
  }
};

// Gestion des présences
export const getAttendances = async ({ queryKey }: QueryFunctionContext<readonly ['hr', 'attendances']>): Promise<Attendance[]> => {
  try {
    const response = await api.get<ApiResponse<Attendance[]>>(`${BASE_URL}/presences`);
    return response.data.data;
  } catch (error) {
    throw new Error('Erreur lors de la récupération des présences');
  }
};

export const createAttendance = async (data: Omit<Attendance, 'id'>): Promise<Attendance> => {
  try {
    const response = await api.post<ApiResponse<Attendance>>(`${BASE_URL}/presences`, data);
    return response.data.data;
  } catch (error) {
    throw new Error('Erreur lors de l\'enregistrement de la présence');
  }
};

// Statistiques
export const getEmployeeStats = async (): Promise<EmployeeStats> => {
  try {
    const response = await api.get<ApiResponse<EmployeeStats>>(`${BASE_URL}/stats`);
    return response.data.data;
  } catch (error) {
    throw new Error('Erreur lors de la récupération des statistiques RH');
  }
};

// Export/Import
export const exportEmployees = async (format: 'csv' | 'xlsx' = 'xlsx'): Promise<Blob> => {
  try {
    const response = await api.get(`${BASE_URL}/employes/export`, {
      params: { format },
      responseType: 'blob'
    });
    return response.data;
  } catch (error) {
    throw new Error('Erreur lors de l\'export des données');
  }
};

export const importEmployees = async (file: File): Promise<{ imported: number; errors: string[] }> => {
  try {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await api.post<ApiResponse<{ imported: number; errors: string[] }>>(
      `${BASE_URL}/employes/import`,
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      }
    );
    return response.data.data;
  } catch (error) {
    throw new Error('Erreur lors de l\'import des données');
  }
};
