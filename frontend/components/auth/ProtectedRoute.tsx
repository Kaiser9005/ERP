import React from 'react'
import { Navigate } from 'react-router-dom'

interface ProtectedRouteProps {
  children: React.ReactNode
}

// Pour le développement, on désactive temporairement la protection
const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children }) => {
  // Temporairement, on laisse passer tout le monde
  const isAuthenticated = true

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }

  return <>{children}</>
}

export default ProtectedRoute