import React from 'react';
import { Routes, Route } from 'react-router-dom';
import ProtectedRoute from './ProtectedRoute';
import DashboardPage from '../components/dashboard/DashboardPage';
import TableauMeteo from '../components/production/TableauMeteo';
import PageFinance from '../components/finance/PageFinance';
import PageInventaire from '../components/inventaire/PageInventaire';
import ProjectRoutes from './projects';

const AppRoutes: React.FC = () => {
  return (
    <Routes>
      <Route path="/" element={<ProtectedRoute />}>
        <Route index element={<DashboardPage />} />
        <Route path="meteo" element={<TableauMeteo />} />
        <Route path="finance/*" element={<PageFinance />} />
        <Route path="inventaire/*" element={<PageInventaire />} />
        <Route path="projects/*" element={<ProjectRoutes />} />
      </Route>
    </Routes>
  );
};

export default AppRoutes;
