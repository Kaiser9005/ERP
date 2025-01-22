import React from 'react';
import { Routes, Route } from 'react-router-dom';
import RouteProtege from '../components/auth/RouteProtege';
import PageTableauBord from '../components/tableau-bord/PageTableauBord';
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
      <Route path="/" element={<RouteProtege><PageTableauBord /></RouteProtege>} />
      <Route path="/finance/*" element={<RouteProtege><PageFinance /></RouteProtege>} />
      <Route path="/inventaire/*" element={<RouteProtege><PageInventaire /></RouteProtege>} />
      <Route path="/projects/*" element={<RouteProtege><ProjectRoutes /></RouteProtege>} />
      <Route path="/rh/*" element={<RouteProtege><HRRoutes /></RouteProtege>} />
      <Route path="/comptabilite/*" element={<RouteProtege><ComptabilitePage /></RouteProtege>} />
      <Route path="/parametrage/*" element={<RouteProtege><ParametrageLayout /></RouteProtege>} />
      <Route path="/production/*" element={<RouteProtege><ProductionRoutes /></RouteProtege>} />
    </Routes>
  );
};

export default AppRoutes;
