import { api } from './api';

export interface Notification {
  id: string;
  title: string;
  message: string;
  type: 'success' | 'warning' | 'info' | 'error';
  date: string;
  read: boolean;
}

export const getNotifications = async (): Promise<Notification[]> => {
  const response = await api.get('/notifications');
  return response.data;
};

export const markNotificationAsRead = async (id: string): Promise<void> => {
  await api.put(`/notifications/${id}/read`);
};