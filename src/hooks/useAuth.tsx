import React, { createContext, useContext, useState, useCallback } from 'react';
import { api } from '../services/api';

interface AuthContextType {
  isAuthenticated: boolean;
  user: any | null;
  login: (username: string, password: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<any | null>(null);

  const login = useCallback(async (username: string, password: string) => {
    try {
      const response = await api.post('/auth/token', {
        username,
        password
      });

      const { access_token } = response.data;
      localStorage.setItem('token', access_token);

      // Récupérer les informations de l'utilisateur
      const userResponse = await api.get('/auth/users/me');
      setUser(userResponse.data);
    } catch (error) {
      throw new Error('Identifiants invalides');
    }
  }, []);

  const logout = useCallback(() => {
    localStorage.removeItem('token');
    setUser(null);
  }, []);

  return (
    <AuthContext.Provider value={{
      isAuthenticated: !!user,
      user,
      login,
      logout
    }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};