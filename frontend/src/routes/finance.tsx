import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import PageFinance from '../components/finance/PageFinance';
import FormulaireTransaction from '../components/finance/FormulaireTransaction';
import { ProtectedRoute } from '../routes/ProtectedRoute';

const FinanceRoutes: React.FC = () => {
  return (
    <Routes>
      <Route
        path="/"
        element={
          <ProtectedRoute>
            <PageFinance />
          </ProtectedRoute>
        }
      />
      <Route
        path="/transactions/new"
        element={
          <ProtectedRoute>
            <FormulaireTransaction />
          </ProtectedRoute>
        }
      />
      <Route
        path="/transactions/:id"
        element={
          <ProtectedRoute>
            <FormulaireTransaction />
          </ProtectedRoute>
        }
      />
      {/* Redirection par défaut */}
      <Route path="*" element={<Navigate to="/finance" replace />} />
    </Routes>
  );
};

export default FinanceRoutes;
