import { api } from './api';

export interface Employee {
  id: string;
  matricule: string;
  nom: string;
  prenom: string;
  date_naissance: string;
  lieu_naissance?: string;
  sexe: string;
  adresse?: string;
  telephone?: string;
  email?: string;
  departement: string;
  poste: string;
  date_embauche: string;
  type_contrat: string;
  statut: string;
  salaire_base: number;
}

export interface Leave {
  id: string;
  type_conge: string;
  date_debut: string;
  date_fin: string;
  nb_jours: number;
  motif?: string;
  statut: string;
  employe: {
    id: string;
    nom: string;
    prenom: string;
  };
}

export const getEmployees = async (): Promise<Employee[]> => {
  const response = await api.get('/employes');
  return response.data;
};

export const getEmployee = async (id: string): Promise<Employee> => {
  const response = await api.get(`/employes/${id}`);
  return response.data;
};

export const createEmployee = async (data: Partial<Employee>): Promise<Employee> => {
  const response = await api.post('/employes', data);
  return response.data;
};

export const updateEmployee = async (id: string, data: Partial<Employee>): Promise<Employee> => {
  const response = await api.put(`/employes/${id}`, data);
  return response.data;
};

export const getEmployeeLeaves = async (employeeId: string): Promise<Leave[]> => {
  const response = await api.get(`/employes/${employeeId}/conges`);
  return response.data;
};

export const createLeaveRequest = async (data: {
  employe_id: string;
  type_conge: string;
  date_debut: string;
  date_fin: string;
  motif?: string;
}): Promise<Leave> => {
  const response = await api.post('/employes/conges', data);
  return response.data;
};