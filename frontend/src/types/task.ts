export enum TaskStatus {
  A_FAIRE = "A_FAIRE",
  EN_COURS = "EN_COURS",
  EN_ATTENTE = "EN_ATTENTE",
  TERMINEE = "TERMINEE",
  ANNULEE = "ANNULEE"
}

export enum TaskPriority {
  BASSE = "BASSE",
  MOYENNE = "MOYENNE",
  HAUTE = "HAUTE",
  CRITIQUE = "CRITIQUE"
}

export enum TaskCategory {
  PRODUCTION = "PRODUCTION",
  MAINTENANCE = "MAINTENANCE",
  RECOLTE = "RECOLTE",
  PLANTATION = "PLANTATION",
  IRRIGATION = "IRRIGATION",
  TRAITEMENT = "TRAITEMENT",
  AUTRE = "AUTRE"
}

export interface TaskResourceBase {
  resource_id: number;
  quantity_required: number;
  quantity_used: number;
}

export interface TaskResource extends TaskResourceBase {
  id: number;
  created_at: string;
  updated_at: string;
}

export interface TaskCommentBase {
  content: string;
  user_id: number;
}

export interface TaskComment extends TaskCommentBase {
  id: number;
  task_id: number;
  created_at: string;
  updated_at: string;
}

export interface TaskDependencyBase {
  dependent_on_id: number;
  dependency_type: string;
}

export interface TaskDependency extends TaskDependencyBase {
  id: number;
  task_id: number;
  created_at: string;
  updated_at: string;
}

export interface TaskBase {
  title: string;
  description?: string;
  status: TaskStatus;
  priority: TaskPriority;
  category: TaskCategory;
  start_date?: string;
  due_date?: string;
  project_id: number;
  assigned_to?: number;
  parcelle_id?: number;
  weather_dependent: boolean;
  min_temperature?: number;
  max_temperature?: number;
  max_wind_speed?: number;
  max_precipitation?: number;
  estimated_hours?: number;
  actual_hours?: number;
  completion_percentage: number;
}

export interface TaskFormData extends TaskBase {
  resources: TaskResourceBase[];
  dependencies: TaskDependencyBase[];
}

export interface Task extends TaskBase {
  id: number;
  completed_date?: string;
  created_at: string;
  updated_at: string;
  resources: TaskResource[];
  comments: TaskComment[];
  dependencies: TaskDependency[];
}

export interface TaskWithWeather extends Task {
  weather_suitable: boolean;
  weather_conditions: {
    temperature: number;
    humidity: number;
    precipitation: number;
    wind_speed: number;
    conditions: string;
    uv_index: number;
    cloud_cover: number;
  };
  weather_warnings: string[];
}

export interface TaskList {
  tasks: Task[];
  total: number;
  page: number;
  size: number;
  total_pages: number;
}
