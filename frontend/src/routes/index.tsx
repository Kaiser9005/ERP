import React from 'react';
import { Routes, Route } from 'react-router-dom';
import ProtectedRoute from './ProtectedRoute';
import DashboardPage from '../components/dashboard/DashboardPage';
import PageFinance from '../components/finance/PageFinance';
import PageInventaire from '../components/inventaire/PageInventaire';
import ProjectRoutes from './projects';
import HRRoutes from './hr';
import ProductionRoutes from './production';
import ComptabilitePage from '../components/comptabilite/ComptabilitePage';
import ParametrageLayout from '../components/parametrage/ParametrageLayout';

const AppRoutes: React.FC = () => {
  return (
    <Routes>
      <Route path="/" element={<ProtectedRoute />}>
        <Route index element={<DashboardPage />} />
        <Route path="finance/*" element={<PageFinance />} />
        <Route path="inventaire/*" element={<PageInventaire />} />
        <Route path="projects/*" element={<ProjectRoutes />} />
        <Route path="rh/*" element={<HRRoutes />} />
        <Route path="comptabilite/*" element={<ComptabilitePage />} />
        <Route path="parametrage/*" element={<ParametrageLayout />} />
        <Route path="production/*" element={<ProductionRoutes />} />
      </Route>
    </Routes>
  );
};

export default AppRoutes;
