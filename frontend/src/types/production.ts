// Types pour les données météorologiques
export interface WeatherConditions {
  timestamp: string;
  temperature: number;
  humidity: number;
  precipitation: number;
  wind_speed: number;
  conditions: string;
  uv_index: number;
  cloud_cover: number;
  cached_at?: string;
}

export type RiskLevel = 'LOW' | 'MEDIUM' | 'HIGH';

export interface WeatherRisk {
  level: RiskLevel;
  message: string;
}

export interface WeatherData extends WeatherConditions {
  risks?: {
    precipitation: WeatherRisk;
    temperature: WeatherRisk;
    level: RiskLevel;
  };
  recommendations?: string[];
}

// Types pour les parcelles
export interface Parcelle {
  id: string;
  code: string;
  surface_hectares: number;
  culture_type: 'palmier' | 'papaye';
  date_plantation: string;
  statut: 'en_preparation' | 'active' | 'en_recolte' | 'en_repos';
  coordonnees_gps: {
    latitude: number;
    longitude: number;
  };
  responsable_id: string;
  metadata?: Record<string, unknown>;
}

// Types pour les cycles de culture
export interface CycleCulture {
  id: string;
  parcelle_id: string;
  date_debut: string;
  date_fin: string;
  rendement_prevu: number;
  rendement_reel?: number;
  notes?: string;
  metadata?: Record<string, unknown>;
}

// Types pour les récoltes
export interface Recolte {
  id: string;
  parcelle_id: string;
  cycle_culture_id: string;
  date_recolte: string;
  quantite_kg: number;
  qualite: 'A' | 'B' | 'C';
  conditions_meteo: WeatherConditions;
  equipe_recolte: string[];
  notes?: string;
  metadata?: Record<string, unknown>;
}

// Types pour les événements de production
export interface ProductionEvent {
  id: string;
  parcelle_id: string;
  type: 'irrigation' | 'fertilisation' | 'traitement' | 'maintenance' | 'autre';
  date_debut: string;
  date_fin: string;
  description: string;
  statut: 'planifie' | 'en_cours' | 'termine' | 'annule';
  responsable_id: string;
  metadata?: Record<string, unknown>;
}

// Types pour les statistiques de production
export interface ProductionStats {
  periode: string;
  recolte_totale: number;
  rendement_moyen: number;
  qualite_distribution: {
    A: number;
    B: number;
    C: number;
  };
  comparaison_periode_precedente: {
    variation_pourcentage: number;
    tendance: 'hausse' | 'baisse' | 'stable';
  };
}
