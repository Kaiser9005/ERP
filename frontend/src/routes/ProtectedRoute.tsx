import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';

interface ProtectedRouteProps {
  children?: React.ReactNode;
  requiredRoles?: string[];
}

export const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ 
  children,
  requiredRoles = []
}) => {
  const { isAuthenticated, user } = useAuth();

  if (!isAuthenticated) {
    // Rediriger vers la page de connexion si non authentifié
    return <Navigate to="/login" replace />;
  }

  // Vérifier les rôles si spécifiés
  if (requiredRoles.length > 0 && user) {
    const hasRequiredRole = requiredRoles.some(role => 
      user.roles?.includes(role)
    );

    if (!hasRequiredRole) {
      // Rediriger vers la page d'accueil si l'utilisateur n'a pas les rôles requis
      return <Navigate to="/" replace />;
    }
  }

  return children ? <>{children}</> : <Outlet />;
};

export default ProtectedRoute;
