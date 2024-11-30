import axios from 'axios';

export const api = axios.create({
  baseURL: '/api/v1', // Base URL pour toutes les requêtes
  timeout: 30000, // Timeout de 30 secondes
  headers: {
    'Content-Type': 'application/json',
  },
});

// Intercepteur pour ajouter le token d'authentification
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Intercepteur pour gérer les erreurs globalement
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      // Erreur avec réponse du serveur
      switch (error.response.status) {
        case 401:
          // Non authentifié - rediriger vers la page de connexion
          localStorage.removeItem('token');
          window.location.href = '/login';
          break;
        case 403:
          // Non autorisé
          console.error('Accès non autorisé');
          break;
        case 404:
          // Ressource non trouvée
          console.error('Ressource non trouvée');
          break;
        case 422:
          // Erreur de validation
          console.error('Erreur de validation:', error.response.data);
          break;
        case 500:
          // Erreur serveur
          console.error('Erreur serveur:', error.response.data);
          break;
        default:
          console.error('Erreur:', error.response.data);
      }
    } else if (error.request) {
      // Pas de réponse du serveur
      console.error('Pas de réponse du serveur');
    } else {
      // Erreur lors de la configuration de la requête
      console.error('Erreur:', error.message);
    }
    return Promise.reject(error);
  }
);

// Fonction utilitaire pour formater les paramètres de requête
export const formatQueryParams = (params: Record<string, any>): string => {
  const searchParams = new URLSearchParams();
  
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== null) {
      if (Array.isArray(value)) {
        value.forEach((item) => searchParams.append(`${key}[]`, item.toString()));
      } else if (typeof value === 'object') {
        searchParams.append(key, JSON.stringify(value));
      } else {
        searchParams.append(key, value.toString());
      }
    }
  });
  
  return searchParams.toString();
};

// Types pour les réponses API
export interface ApiResponse<T> {
  data: T;
  message?: string;
  status: number;
}

export interface ApiError {
  message: string;
  errors?: Record<string, string[]>;
  status: number;
}

export interface PaginatedResponse<T> {
  data: T[];
  pagination: {
    page: number;
    limit: number;
    total: number;
    totalPages: number;
  };
}
