export interface ApiResponse<T> {
  success: boolean;
  data: T;
  message?: string;
  errors?: Record<string, string[]>;
}

export interface PaginatedResponse<T> {
  data: T[];
  total: number;
  page: number;
  limit: number;
  totalPages: number;
}

export interface ApiError {
  message: string;
  code?: string;
  details?: Record<string, string[]>;
}

export interface QueryFilters {
  page?: number;
  limit?: number;
  sortBy?: string;
  sortOrder?: 'asc' | 'desc';
  search?: string;
  [key: string]: any;
}

export interface DateRange {
  dateDebut: string;
  dateFin: string;
}

export interface SelectOption {
  value: string | number;
  label: string;
  disabled?: boolean;
  group?: string;
}

export type SortDirection = 'asc' | 'desc';

export interface SortConfig {
  field: string;
  direction: SortDirection;
}

export interface FileUploadResponse {
  url: string;
  filename: string;
  mimetype: string;
  size: number;
}

export interface MetadataField {
  key: string;
  value: any;
  type: 'string' | 'number' | 'boolean' | 'date' | 'object' | 'array';
  label?: string;
  description?: string;
}

export interface AuditInfo {
  created_at: string;
  created_by: string;
  updated_at?: string;
  updated_by?: string;
  version: number;
}

export interface BaseEntity extends AuditInfo {
  id: string;
  metadata?: Record<string, any>;
}

export interface ValidationError {
  field: string;
  message: string;
  code?: string;
}

export interface ApiValidationError {
  message: string;
  errors: ValidationError[];
}

export type LoadingState = 'idle' | 'loading' | 'success' | 'error';

export interface LoadingStatus {
  state: LoadingState;
  error?: string | null;
  timestamp?: number;
}

export interface CacheConfig {
  ttl?: number;
  staleTime?: number;
  cacheKey?: string[];
}
