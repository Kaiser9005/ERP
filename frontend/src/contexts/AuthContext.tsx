import React, { createContext, useState, useCallback, ReactNode } from 'react';
import axios from 'axios';
import { Utilisateur, ContexteAuthType } from '../types/auth';

export const AuthContext = createContext<ContexteAuthType | null>(null);

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider = ({ children }: AuthProviderProps) => {
  const [utilisateur, setUtilisateur] = useState<Utilisateur | null>(() => {
    const utilisateurSauvegarde = localStorage.getItem('utilisateur');
    return utilisateurSauvegarde ? JSON.parse(utilisateurSauvegarde) : null;
  });

  const connexion = useCallback(async (nomUtilisateur: string, motDePasse: string) => {
    try {
      console.log('Tentative de connexion avec:', nomUtilisateur, motDePasse);
      const params = new URLSearchParams();
      params.append('username', nomUtilisateur);
      params.append('password', motDePasse);

      const reponse = await axios.post<{ access_token: string; token_type: string }>('/api/v1/auth/token', params, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      });
      console.log('Réponse de connexion:', reponse.data);

      const { access_token } = reponse.data;
      localStorage.setItem('token', access_token);

      // Configurer axios pour inclure le token dans les futures requêtes
      axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;

      // Récupérer les informations de l'utilisateur
      const reponseUtilisateur = await axios.get<Utilisateur>('/api/v1/auth/users/me');
      const donneesUtilisateur = reponseUtilisateur.data;
      
      // Sauvegarder l'utilisateur dans le localStorage
      localStorage.setItem('utilisateur', JSON.stringify(donneesUtilisateur));
      setUtilisateur(donneesUtilisateur);

    } catch (erreur) {
      console.error('Erreur de connexion:', erreur);
      throw erreur;
    }
  }, []);

  const deconnexion = useCallback(() => {
    localStorage.removeItem('utilisateur');
    localStorage.removeItem('token');
    setUtilisateur(null);
    delete axios.defaults.headers.common['Authorization'];
  }, []);

  // Configurer le token d'authentification au démarrage
  React.useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    }
  }, []);

  // Intercepteur pour gérer l'expiration du token
  React.useEffect(() => {
    const intercepteur = axios.interceptors.response.use(
      reponse => reponse,
      erreur => {
        if (erreur.response?.status === 401) {
          deconnexion();
        }
        return Promise.reject(erreur);
      }
    );

    return () => {
      axios.interceptors.response.eject(intercepteur);
    };
  }, [deconnexion]);

  const valeur = {
    utilisateur,
    estAuthentifie: !!utilisateur,
    connexion,
    deconnexion
  };

  return <AuthContext.Provider value={valeur}>{children}</AuthContext.Provider>;
};