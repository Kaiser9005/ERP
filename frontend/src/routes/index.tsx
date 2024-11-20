import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import RoutesProjet from './projects';
import TableauBord from '../components/dashboard/DashboardPage';
import TableauMeteo from '../components/production/WeatherDashboard';

const RoutesApp: React.FC = () => {
  return (
    <Routes>
      {/* Page d'accueil - Tableau de bord */}
      <Route path="/" element={<TableauBord />} />

      {/* Routes de production */}
      <Route path="/production">
        <Route path="meteo" element={<TableauMeteo />} />
      </Route>

      {/* Routes des projets et tâches */}
      <Route path="/projets/*" element={<RoutesProjet />} />

      {/* Redirection par défaut */}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
};

export default RoutesApp;
