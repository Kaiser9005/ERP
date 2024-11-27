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
