import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import ProjectRoutes from './projects';
import DashboardPage from '../components/dashboard/DashboardPage';
import WeatherDashboard from '../components/production/WeatherDashboard';

const AppRoutes: React.FC = () => {
  return (
    <Routes>
      {/* Page d'accueil - Dashboard */}
      <Route path="/" element={<DashboardPage />} />

      {/* Routes de production */}
      <Route path="/production">
        <Route path="weather" element={<WeatherDashboard />} />
      </Route>

      {/* Routes des projets et tâches */}
      <Route path="/projects/*" element={<ProjectRoutes />} />

      {/* Redirection par défaut */}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
};

export default AppRoutes;
