import React from 'react';
import { Routes, Route } from 'react-router-dom';
import PageInventaire from '../components/inventaire/PageInventaire';
import ProtectedRoute from '../components/auth/ProtectedRoute';

const InventaireRoutes: React.FC = () => {
  return (
    <Routes>
      <Route
        path="/"
        element={
          <ProtectedRoute permissions={['INVENTAIRE_READ']}>
            <PageInventaire />
          </ProtectedRoute>
        }
      />
    </Routes>
  );
};

export default InventaireRoutes;
