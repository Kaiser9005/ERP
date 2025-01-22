import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';

interface RouteProtegeProps {
  children: React.ReactElement;
  permissions?: string[];
}

const RouteProtege: React.FC<RouteProtegeProps> = ({ children, permissions = [] }) => {
  const { estAuthentifie, utilisateur } = useAuth();

  if (!estAuthentifie) {
    return <Navigate to="/connexion" replace />;
  }

  if (permissions.length > 0 && utilisateur) {
    const aPermissionsRequises = permissions.every(permission => 
      utilisateur.permissions?.includes(permission)
    );

    if (!aPermissionsRequises) {
      return <Navigate to="/non-autorise" replace />;
    }
  }

  return children;
};

export default RouteProtege;
