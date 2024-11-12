import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import FinancePage from '../components/finance/FinancePage';
import TransactionForm from '../components/finance/TransactionForm';
import { ProtectedRoute } from '../routes/ProtectedRoute';

const FinanceRoutes: React.FC = () => {
  return (
    <Routes>
      <Route
        path="/"
        element={
          <ProtectedRoute>
            <FinancePage />
          </ProtectedRoute>
        }
      />
      <Route
        path="/transactions/new"
        element={
          <ProtectedRoute>
            <TransactionForm />
          </ProtectedRoute>
        }
      />
      <Route
        path="/transactions/:id"
        element={
          <ProtectedRoute>
            <TransactionForm />
          </ProtectedRoute>
        }
      />
      {/* Redirection par défaut */}
      <Route path="*" element={<Navigate to="/finance" replace />} />
    </Routes>
  );
};

export default FinanceRoutes;
