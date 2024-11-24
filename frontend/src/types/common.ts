// Types communs utilisés dans toute l'application

// Type pour les identifiants uniques
export type UUID = string;

// Type pour les dates au format ISO
export type ISODate = string;

// Type pour les timestamps au format ISO
export type ISODateTime = string;

// Type pour les montants décimaux
export type Decimal = number;

// Type pour les métadonnées
export type Metadata = Record<string, any>;

// Type pour les réponses paginées
export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  pageSize: number;
  totalPages: number;
}

// Type pour les filtres de base
export interface BaseFilter {
  page?: number;
  pageSize?: number;
  sortBy?: string;
  sortOrder?: 'asc' | 'desc';
}

// Type pour les réponses d'API
export interface ApiResponse<T> {
  data: T;
  message?: string;
  status: number;
}

// Type pour les erreurs d'API
export interface ApiError {
  message: string;
  code: string;
  details?: Record<string, any>;
}

// Type pour les champs de traçabilité
export interface AuditFields {
  created_at?: ISODateTime;
  updated_at?: ISODateTime;
  created_by_id?: UUID;
  updated_by_id?: UUID;
}

// Type pour les entités de base
export interface BaseEntity extends AuditFields {
  id: UUID;
  metadata?: Metadata;
}
