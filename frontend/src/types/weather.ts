export interface WeatherCondition {
  date: string;
  temperature: number;
  temperature_min?: number;
  temperature_max?: number;
  humidity: number;
  precipitation: number;
  wind_speed: number;
  conditions: string;
  uv_index: number;
  cloud_cover: number;
  cached_at?: string;
}

export interface WeatherForecastDay {
  date: string;
  temp_max: number;
  temp_min: number;
  precipitation: number;
  humidity: number;
  conditions: string;
  description: string;
}

export interface WeatherForecast {
  location: string;
  days: WeatherForecastDay[];
}

export interface WeatherRisk {
  level: 'LOW' | 'MEDIUM' | 'HIGH';
  message: string;
}

export interface AgriculturalMetrics {
  current_conditions: WeatherCondition;
  risks: {
    precipitation: WeatherRisk;
    temperature: WeatherRisk;
    level: 'LOW' | 'MEDIUM' | 'HIGH';
  };
  recommendations: string[];
}

export interface WeatherResponse {
  currentConditions: {
    temp: number;
    humidity: number;
    precip: number;
    windspeed: number;
    conditions: string;
    uvindex: number;
    cloudcover: number;
  };
  days: Array<{
    datetime: string;
    tempmax: number;
    tempmin: number;
    precip: number;
    humidity: number;
    conditions: string;
    description: string;
  }>;
  resolvedAddress: string;
}

export interface IoTSensorStats {
  moyenne: number;
  minimum: number;
  maximum: number;
}

export interface IoTReading {
  timestamp: string;
  temperature: number;
  humidity: number;
  soil_moisture?: number;
  wind_speed?: number;
}

export interface IoTData {
  readings: IoTReading[];
  stats: {
    temperature: IoTSensorStats;
    humidity: IoTSensorStats;
    soil_moisture?: IoTSensorStats;
  };
  health: {
    status: 'OK' | 'WARNING' | 'ERROR';
    last_update: string;
  };
}

export interface WeatherRiskPeriod {
  period: string;
  risk: 'LOW' | 'MEDIUM' | 'HIGH';
  conditions: string[];
}

export interface AffectedTask {
  task_id: string;
  impact: 'LOW' | 'MEDIUM' | 'HIGH';
  conditions: string[];
}

export interface TaskAlternative {
  task_id: string;
  original_date: string;
  alternative_date: string;
  reason: string;
}

export interface WeatherImpact {
  impact_score: number;
  affected_tasks: AffectedTask[];
  risk_periods: WeatherRiskPeriod[];
  alternatives: TaskAlternative[];
}

export interface WeatherScheduleAdjustment {
  date: string;
  original_schedule: {
    start: string;
    end: string;
  };
  adjusted_schedule: {
    start: string;
    end: string;
  };
  reason: string;
  affected_employees: string[];
  status: 'PROPOSED' | 'APPROVED' | 'ACTIVE' | 'COMPLETED';
}

export interface WeatherSafetyEquipment {
  weather_condition: string;
  required_equipment: string[];
  optional_equipment: string[];
  instructions: string;
  distribution_point?: string;
}

export interface WeatherTrainingRequirement {
  weather_type: string;
  required_training: string;
  validity_period: number;
  refresher_frequency: number;
  priority: 'LOW' | 'MEDIUM' | 'HIGH';
}

export interface WeatherComplianceRecord {
  date: string;
  weather_condition: string;
  measures_taken: string[];
  equipment_provided: string[];
  training_completed: string[];
  incidents: string[];
  supervisor: string;
}

export interface WeatherPolicyConfig {
  temperature_thresholds: {
    max_work: number;
    reduced_activity: number;
    normal_activity: number;
  };
  wind_thresholds: {
    stop_work: number;
    restricted_work: number;
    normal_work: number;
  };
  precipitation_thresholds: {
    stop_work: number;
    indoor_only: number;
    normal_work: number;
  };
  break_schedule: {
    high_temp_frequency: number;
    high_temp_duration: number;
    normal_frequency: number;
    normal_duration: number;
  };
  ppe_requirements: Record<string, string[]>;
}

export interface WeatherRiskAssessment {
  date: string;
  location: string;
  assessor: string;
  conditions: WeatherCondition;
  identified_risks: WeatherRisk[];
  control_measures: string[];
  residual_risk_level: 'LOW' | 'MEDIUM' | 'HIGH';
  review_date: string;
  approval_status: 'PENDING' | 'APPROVED' | 'REJECTED';
}

export type WeatherAlertType = 'SCHEDULE' | 'SAFETY' | 'EQUIPMENT' | 'TRAINING';
export type WeatherAlertLevel = 'INFO' | 'WARNING' | 'CRITICAL';

export interface WeatherAlert {
  type: WeatherAlertType;
  level: WeatherAlertLevel;
  message: string;
  affected_roles: string[];
}

export interface WeatherHRMetrics {
  current_conditions: WeatherCondition;
  risks: {
    temperature: WeatherRisk;
    precipitation: WeatherRisk;
    wind: WeatherRisk;
    level: 'LOW' | 'MEDIUM' | 'HIGH';
  };
  schedule_adjustments: WeatherScheduleAdjustment[];
  safety_requirements: WeatherSafetyEquipment[];
  training_needs: WeatherTrainingRequirement[];
  compliance: WeatherComplianceRecord[];
  alerts: WeatherAlert[];
}
