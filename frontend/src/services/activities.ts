import { api } from './api';

export interface Activity {
  id: string;
  type: string;
  title: string;
  description: string;
  date: string;
  color: string;
  user: {
    id: string;
    name: string;
  };
}

export const getRecentActivities = async (): Promise<Activity[]> => {
  const response = await api.get('/activities/recent');
  return response.data;
};