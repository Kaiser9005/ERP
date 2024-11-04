import { api } from './api';
import { Parametre, ConfigurationModule } from '../types/parametrage';

export const getParametres = async (type?: string): Promise<Parametre[]> => {
  const params = type ? { type } : {};
  const response = await api.get('/parametrage/parametres', { params });
  return response.data;
};

export const updateParametre = async (data: { id: string; valeur: any }): Promise<Parametre> => {
  const response = await api.put(`/parametrage/parametres/${data.id}`, { valeur: data.valeur });
  return response.data;
};

export const getModulesConfiguration = async (): Promise<ConfigurationModule[]> => {
  const response = await api.get('/parametrage/modules/configuration');
  return response.data;
};

export const updateModuleConfiguration = async (data: {
  module: string;
  actif?: boolean;
  configuration?: any;
}): Promise<ConfigurationModule> => {
  const response = await api.put(`/parametrage/modules/${data.module}/configuration`, data);
  return response.data;
};