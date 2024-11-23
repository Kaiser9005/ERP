export enum CultureType {
  PALMIER = "PALMIER",
  PAPAYE = "PAPAYE"
}

export enum ParcelleStatus {
  EN_PREPARATION = "EN_PREPARATION",
  ACTIVE = "ACTIVE",
  EN_REPOS = "EN_REPOS"
}

export enum QualiteRecolte {
  A = "A",
  B = "B",
  C = "C"
}

export interface Coordonnees {
  latitude: number;
  longitude: number;
}

export interface WeatherData {
  timestamp: string;
  temperature: number;
  humidity: number;
  precipitation: number;
  wind_speed: number;
  conditions: string;
  uv_index: number;
  cloud_cover: number;
}

export interface WeatherMetrics {
  current_conditions: WeatherData;
  risks: {
    precipitation: {
      level: "LOW" | "MEDIUM" | "HIGH";
      message: string;
    };
    temperature: {
      level: "LOW" | "MEDIUM" | "HIGH";
      message: string;
    };
    level: "LOW" | "MEDIUM" | "HIGH";
  };
  recommendations: string[];
}

export interface Parcelle {
  id: string;
  code: string;
  culture_type: CultureType;
  surface_hectares: number;
  date_plantation: string;
  statut: ParcelleStatus;
  coordonnees_gps: Coordonnees;
  responsable_id: string;
  metadata?: Record<string, any>;
}

export interface CycleCulture {
  id: string;
  parcelle_id: string;
  date_debut: string;
  date_fin?: string;
  rendement_prevu?: number;
  rendement_reel?: number;
  notes?: string;
  metadata?: Record<string, any>;
}

export interface Recolte {
  id: string;
  parcelle_id: string;
  cycle_culture_id?: string;
  date_recolte: string;
  quantite_kg: number;
  qualite: QualiteRecolte;
  conditions_meteo?: {
    temperature: number;
    humidite: number;
    precipitation: number;
  };
  equipe_recolte?: string[];
  notes?: string;
  metadata?: Record<string, any>;
}

export interface ProductionEvent {
  id: string;
  parcelle_id: string;
  type: string;
  date_debut: string;
  date_fin?: string;
  description?: string;
  statut?: string;
  responsable_id?: string;
  metadata?: Record<string, any>;
}
