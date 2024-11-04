import { createBrowserRouter } from 'react-router-dom';
import LoginPage from '../components/auth/LoginPage';
import ProtectedRoute from '../components/auth/ProtectedRoute';
import DashboardLayout from '../components/layout/DashboardLayout';
import DashboardPage from '../components/dashboard/DashboardPage';
import { financeRoutes } from './finance';
import { inventoryRoutes } from './inventory';
import { productionRoutes } from './production';
import { hrRoutes } from './hr';
import { projectRoutes } from './projects';
import { parametrageRoutes } from './parametrage';

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
      {
        index: true,
        element: <DashboardPage />
      },
      {
        path: 'dashboard',
        element: <DashboardPage />
      },
      ...financeRoutes,
      ...inventoryRoutes,
      ...productionRoutes,
      ...hrRoutes,
      ...projectRoutes,
      ...parametrageRoutes
    ]
  }
]);