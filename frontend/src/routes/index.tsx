import { createBrowserRouter } from 'react-router-dom';
import LoginPage from '../components/auth/LoginPage';
import ProtectedRoute from '../components/auth/ProtectedRoute';
import { parametrageRoutes } from './parametrage';
import DashboardLayout from '../components/layout/DashboardLayout';

export const router = createBrowserRouter([
  {
    path: '/login',
    element: <LoginPage />
  },
  {
    path: '/',
    element: (
      <ProtectedRoute>
        <DashboardLayout />
      </ProtectedRoute>
    ),
    children: [
      ...parametrageRoutes
      // Autres routes à ajouter ici
    ]
  }
]);