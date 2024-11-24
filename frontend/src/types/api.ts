import { UseQueryOptions, UseMutationOptions } from '@tanstack/react-query';

// Types génériques pour les requêtes
export type QueryConfig<TData> = Omit<
  UseQueryOptions<TData, Error, TData>,
  'queryKey' | 'queryFn'
>;

export type MutationConfig<TData, TVariables> = Omit<
  UseMutationOptions<TData, Error, TVariables>,
  'mutationFn'
>;

// Types pour les réponses d'API
export interface ApiResponse<T> {
  data: T;
  message?: string;
  status: number;
}

// Types pour la pagination
export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  pageSize: number;
  totalPages: number;
}

// Types pour les filtres
export interface BaseFilter {
  page?: number;
  pageSize?: number;
  sortBy?: string;
  sortOrder?: 'asc' | 'desc';
}

// Types pour les erreurs
export interface ApiError {
  message: string;
  code: string;
  details?: Record<string, any>;
}
