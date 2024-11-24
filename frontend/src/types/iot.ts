/**
 * Types pour le module IoT
 */

export enum SensorType {
  TEMPERATURE_SOL = "temperature_sol",
  TEMPERATURE_AIR = "temperature_air",
  HUMIDITE_SOL = "humidite_sol",
  HUMIDITE_AIR = "humidite_air",
  LUMINOSITE = "luminosite",
  PLUVIOMETRIE = "pluviometrie",
  PH_SOL = "ph_sol",
  CONDUCTIVITE = "conductivite"
}

export enum SensorStatus {
  ACTIF = "actif",
  INACTIF = "inactif",
  MAINTENANCE = "maintenance",
  ERREUR = "erreur"
}

export interface IoTSensor {
  id: string;
  code: string;
  type: SensorType;
  status: SensorStatus;
  parcelle_id: string;
  latitude?: number;
  longitude?: number;
  altitude?: number;
  config: Record<string, any>;
  seuils_alerte: {
    min?: number;
    max?: number;
    critique_min?: number;
    critique_max?: number;
  };
  intervalle_lecture: number;
  fabricant?: string;
  modele?: string;
  firmware?: string;
  date_installation: string;
  derniere_maintenance?: string;
  prochaine_maintenance?: string;
}

export interface SensorReading {
  id: string;
  capteur_id: string;
  timestamp: string;
  valeur: number;
  unite: string;
  qualite_signal?: number;
  niveau_batterie?: number;
  metadata: Record<string, any>;
}

export interface SensorStats {
  moyenne: number;
  minimum: number;
  maximum: number;
  nombre_lectures: number;
}

export interface SensorHealth {
  status: SensorStatus;
  message: string;
  last_reading?: SensorReading;
  battery_level?: number;
  signal_quality?: number;
}

// Types pour les formulaires
export interface IoTSensorFormData {
  code: string;
  type: SensorType;
  parcelle_id: string;
  latitude?: number;
  longitude?: number;
  altitude?: number;
  config: Record<string, any>;
  seuils_alerte: {
    min?: number;
    max?: number;
    critique_min?: number;
    critique_max?: number;
  };
  intervalle_lecture: number;
  fabricant?: string;
  modele?: string;
  firmware?: string;
}

export interface SensorReadingFormData {
  valeur: number;
  unite: string;
  qualite_signal?: number;
  niveau_batterie?: number;
  metadata?: Record<string, any>;
}

// Types pour les filtres
export interface SensorFilters {
  type?: SensorType;
  status?: SensorStatus;
  parcelle_id?: string;
  date_debut?: string;
  date_fin?: string;
}

// Types pour les requêtes API
export interface SensorQueryParams {
  start_date?: string;
  end_date?: string;
  limit?: number;
}

// Types pour les réponses d'erreur
export interface SensorError {
  status: number;
  message: string;
  details?: Record<string, any>;
}

// Types pour les unités de mesure
export const SENSOR_UNITS: Record<SensorType, string> = {
  [SensorType.TEMPERATURE_SOL]: "°C",
  [SensorType.TEMPERATURE_AIR]: "°C",
  [SensorType.HUMIDITE_SOL]: "%",
  [SensorType.HUMIDITE_AIR]: "%",
  [SensorType.LUMINOSITE]: "lux",
  [SensorType.PLUVIOMETRIE]: "mm",
  [SensorType.PH_SOL]: "pH",
  [SensorType.CONDUCTIVITE]: "µS/cm"
};

// Types pour les seuils par défaut
export const DEFAULT_THRESHOLDS: Record<SensorType, {
  min?: number;
  max?: number;
  critique_min?: number;
  critique_max?: number;
}> = {
  [SensorType.TEMPERATURE_SOL]: {
    min: 10,
    max: 35,
    critique_min: 5,
    critique_max: 40
  },
  [SensorType.TEMPERATURE_AIR]: {
    min: 15,
    max: 35,
    critique_min: 10,
    critique_max: 40
  },
  [SensorType.HUMIDITE_SOL]: {
    min: 20,
    max: 80,
    critique_min: 10,
    critique_max: 90
  },
  [SensorType.HUMIDITE_AIR]: {
    min: 30,
    max: 80,
    critique_min: 20,
    critique_max: 90
  },
  [SensorType.LUMINOSITE]: {
    min: 1000,
    max: 100000
  },
  [SensorType.PLUVIOMETRIE]: {
    max: 50,
    critique_max: 100
  },
  [SensorType.PH_SOL]: {
    min: 5.5,
    max: 7.5,
    critique_min: 5,
    critique_max: 8
  },
  [SensorType.CONDUCTIVITE]: {
    min: 200,
    max: 2000,
    critique_min: 100,
    critique_max: 3000
  }
};

// Labels pour l'interface utilisateur
export const SENSOR_TYPE_LABELS: Record<SensorType, string> = {
  [SensorType.TEMPERATURE_SOL]: "Température du sol",
  [SensorType.TEMPERATURE_AIR]: "Température de l'air",
  [SensorType.HUMIDITE_SOL]: "Humidité du sol",
  [SensorType.HUMIDITE_AIR]: "Humidité de l'air",
  [SensorType.LUMINOSITE]: "Luminosité",
  [SensorType.PLUVIOMETRIE]: "Pluviométrie",
  [SensorType.PH_SOL]: "pH du sol",
  [SensorType.CONDUCTIVITE]: "Conductivité"
};

export const SENSOR_STATUS_LABELS: Record<SensorStatus, string> = {
  [SensorStatus.ACTIF]: "Actif",
  [SensorStatus.INACTIF]: "Inactif",
  [SensorStatus.MAINTENANCE]: "En maintenance",
  [SensorStatus.ERREUR]: "Erreur"
};
