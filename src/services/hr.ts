import { api } from './api';

export interface Employee {
  id: string;
  matricule: string;
  nom: string;
  prenom: string;
  date_naissance: string;
  sexe: 'M' | 'F';
  email: string;
  telephone: string;
  poste: string;
  departement: string;
  date_embauche: string;
  type_contrat: 'CDI' | 'CDD' | 'STAGE' | 'TEMPORAIRE';
  salaire_base: number;
  statut: 'ACTIF' | 'CONGE' | 'FORMATION' | 'INACTIF';
}

export interface EmployeeStats {
  totalEmployees: number;
  activeEmployees: number;
  onLeave: number;
  inTraining: number;
  employeeGrowth: {
    value: number;
    type: 'increase' | 'decrease';
  };
  leaveRate: {
    value: number;
    type: 'increase' | 'decrease';
  };
  trainingRate: {
    value: number;
    type: 'increase' | 'decrease';
  };
}

export interface LeaveRequest {
  id: string;
  employee_id: string;
  type_conge: string;
  date_debut: string;
  date_fin: string;
  motif: string;
  statut: 'EN_ATTENTE' | 'APPROUVE' | 'REFUSE';
  commentaire?: string;
  validee_par?: string;
  date_validation?: string;
}

export const getEmployees = async (): Promise<Employee[]> => {
  const { data } = await api.get<Employee[]>('/api/hr/employees');
  return data;
};

export const getEmployee = async (id: string): Promise<Employee> => {
  const { data } = await api.get<Employee>(`/api/hr/employees/${id}`);
  return data;
};

export const createEmployee = async (employeeData: Partial<Employee>): Promise<Employee> => {
  const { data } = await api.post<Employee>('/api/hr/employees', employeeData);
  return data;
};

export const updateEmployee = async (id: string, employeeData: Partial<Employee>): Promise<Employee> => {
  const { data } = await api.put<Employee>(`/api/hr/employees/${id}`, employeeData);
  return data;
};

export const getEmployeeStats = async (): Promise<EmployeeStats> => {
  const { data } = await api.get<EmployeeStats>('/api/hr/stats');
  return data;
};

export const getLeaveRequests = async (): Promise<LeaveRequest[]> => {
  const { data } = await api.get<LeaveRequest[]>('/api/hr/leave-requests');
  return data;
};

export const createLeaveRequest = async (requestData: Partial<LeaveRequest>): Promise<LeaveRequest> => {
  const { data } = await api.post<LeaveRequest>('/api/hr/leave-requests', requestData);
  return data;
};

export const updateLeaveRequest = async (id: string, requestData: Partial<LeaveRequest>): Promise<LeaveRequest> => {
  const { data } = await api.put<LeaveRequest>(`/api/hr/leave-requests/${id}`, requestData);
  return data;
};
