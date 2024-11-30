import axios, { AxiosError } from 'axios';
import type {
  WeatherCondition,
  WeatherForecast,
  WeatherRisk,
  AgriculturalMetrics,
  WeatherResponse,
  IoTData,
  WeatherImpact,
  IoTReading,
  WeatherHRMetrics,
  WeatherScheduleAdjustment,
  WeatherSafetyEquipment,
  WeatherTrainingRequirement,
  WeatherComplianceRecord,
  WeatherPolicyConfig,
  WeatherRiskAssessment
} from '../types/weather';
import { TaskWithWeather } from '../types/task';

const WEATHER_API_KEY = import.meta.env.VITE_WEATHER_API_KEY;
const WEATHER_LOCATION = import.meta.env.VITE_WEATHER_LOCATION;
const BASE_URL = import.meta.env.VITE_WEATHER_API_URL;
const API_BASE_URL = '/api/v1/weather';
const MAX_RETRIES = 3;
const RETRY_DELAY = 5000;

class WeatherService {
  private policyConfig: WeatherPolicyConfig = {
    temperature_thresholds: {
      max_work: 35,
      reduced_activity: 30,
      normal_activity: 25
    },
    wind_thresholds: {
      stop_work: 50,
      restricted_work: 30,
      normal_work: 20
    },
    precipitation_thresholds: {
      stop_work: 30,
      indoor_only: 20,
      normal_work: 10
    },
    break_schedule: {
      high_temp_frequency: 30,
      high_temp_duration: 15,
      normal_frequency: 120,
      normal_duration: 10
    },
    ppe_requirements: {
      'high_temperature': ['chapeau', 'protection_solaire', 'eau'],
      'rain': ['imperméable', 'bottes'],
      'wind': ['lunettes_protection', 'masque']
    }
  };

  private async fetchWithRetry<T>(
    url: string,
    retryCount = 0,
    params: Record<string, string> = {}
  ): Promise<T> {
    try {
      const response = await axios.get<T>(url, { params });
      return response.data;
    } catch (error) {
      if (retryCount < MAX_RETRIES && error instanceof AxiosError) {
        console.log(`Tentative de reconnexion ${retryCount + 1}/${MAX_RETRIES}...`);
        await new Promise(resolve => setTimeout(resolve, RETRY_DELAY));
        return this.fetchWithRetry<T>(url, retryCount + 1, params);
      }
      throw error;
    }
  }

  private async fetchWeatherData<T>(endpoint: string, params: Record<string, string> = {}): Promise<T> {
    try {
      return await this.fetchWithRetry<T>(`${BASE_URL}/${endpoint}`, 0, {
        key: WEATHER_API_KEY,
        unitGroup: 'metric',
        contentType: 'json',
        ...params
      });
    } catch (error) {
      console.error('Erreur lors de la récupération des données météo:', error);
      throw error;
    }
  }

  async getCurrentWeather(): Promise<WeatherCondition> {
    try {
      // Essayer d'abord l'API locale avec cache
      const data = await this.fetchWithRetry<WeatherCondition>(
        `${API_BASE_URL}/current`
      );
      return data;
    } catch (error) {
      // Fallback sur l'API externe en cas d'erreur
      const data = await this.fetchWeatherData<WeatherResponse>(
        `${WEATHER_LOCATION}/today`,
        { include: 'current' }
      );

      const current = data.currentConditions;
      return {
        date: new Date().toISOString(),
        temperature: current.temp,
        humidity: current.humidity,
        precipitation: current.precip,
        wind_speed: current.windspeed,
        conditions: current.conditions,
        uv_index: current.uvindex,
        cloud_cover: current.cloudcover
      };
    }
  }

  async getForecast(days: number = 7): Promise<WeatherForecast> {
    try {
      // Essayer d'abord l'API locale avec cache
      const data = await this.fetchWithRetry<WeatherForecast>(
        `${API_BASE_URL}/forecast?days=${days}`
      );
      return data;
    } catch (error) {
      // Fallback sur l'API externe en cas d'erreur
      const data = await this.fetchWeatherData<WeatherResponse>(
        `${WEATHER_LOCATION}/next/${days}days`
      );

      return {
        location: data.resolvedAddress,
        days: data.days.map(day => ({
          date: day.datetime,
          temp_max: day.tempmax,
          temp_min: day.tempmin,
          precipitation: day.precip,
          humidity: day.humidity,
          conditions: day.conditions,
          description: day.description
        }))
      };
    }
  }

  async getAgriculturalMetrics(): Promise<AgriculturalMetrics> {
    try {
      // Essayer d'abord l'API locale avec cache
      return await this.fetchWithRetry<AgriculturalMetrics>(
        `${API_BASE_URL}/agricultural-metrics`
      );
    } catch (error) {
      // Fallback sur le calcul local en cas d'erreur
      const [current, forecast] = await Promise.all([
        this.getCurrentWeather(),
        this.getForecast(3)
      ]);

      const precipitationRisk = this.analyzePrecipitationRisk(
        current.precipitation,
        forecast.days.map(day => day.precipitation)
      );

      const temperatureRisk = this.analyzeTemperatureRisk(
        current.temperature,
        forecast.days.map(day => day.temp_max)
      );

      return {
        current_conditions: current,
        risks: {
          precipitation: precipitationRisk,
          temperature: temperatureRisk,
          level: this.getHighestRiskLevel([precipitationRisk, temperatureRisk])
        },
        recommendations: this.generateRecommendations(precipitationRisk, temperatureRisk)
      };
    }
  }

  async getTaskWeather(taskId: string): Promise<TaskWithWeather> {
    try {
      return await this.fetchWithRetry<TaskWithWeather>(
        `${API_BASE_URL}/tasks/${taskId}`
      );
    } catch (error) {
      // En cas d'erreur, on récupère les données météo actuelles
      const weather = await this.getCurrentWeather();
      const task = await this.fetchWithRetry<TaskWithWeather>(`/api/v1/tasks/${taskId}`);
      
      // On analyse si les conditions météo sont favorables pour la tâche
      const suitable = this.analyzeTaskWeatherSuitability(task, weather);
      
      // On génère les avertissements si nécessaire
      const warnings = this.generateTaskWeatherWarnings(task, weather);
      
      return {
        ...task,
        weather_suitable: suitable,
        weather_conditions: {
          temperature: weather.temperature,
          humidity: weather.humidity,
          precipitation: weather.precipitation,
          wind_speed: weather.wind_speed,
          conditions: weather.conditions,
          uv_index: weather.uv_index,
          cloud_cover: weather.cloud_cover
        },
        weather_warnings: warnings
      };
    }
  }

  private analyzeTaskWeatherSuitability(task: TaskWithWeather, weather: WeatherCondition): boolean {
    if (!task.weather_dependent) return true;

    const conditions = [
      task.min_temperature === undefined || weather.temperature >= task.min_temperature,
      task.max_temperature === undefined || weather.temperature <= task.max_temperature,
      task.max_wind_speed === undefined || weather.wind_speed <= task.max_wind_speed,
      task.max_precipitation === undefined || weather.precipitation <= task.max_precipitation
    ];

    return conditions.every(condition => condition);
  }

  private generateTaskWeatherWarnings(task: TaskWithWeather, weather: WeatherCondition): string[] {
    const warnings: string[] = [];

    if (!task.weather_dependent) return warnings;

    if (task.min_temperature !== undefined && weather.temperature < task.min_temperature) {
      warnings.push(`Température trop basse (${weather.temperature}°C < ${task.min_temperature}°C)`);
    }

    if (task.max_temperature !== undefined && weather.temperature > task.max_temperature) {
      warnings.push(`Température trop élevée (${weather.temperature}°C > ${task.max_temperature}°C)`);
    }

    if (task.max_wind_speed !== undefined && weather.wind_speed > task.max_wind_speed) {
      warnings.push(`Vent trop fort (${weather.wind_speed} km/h > ${task.max_wind_speed} km/h)`);
    }

    if (task.max_precipitation !== undefined && weather.precipitation > task.max_precipitation) {
      warnings.push(`Précipitations trop importantes (${weather.precipitation} mm > ${task.max_precipitation} mm)`);
    }

    return warnings;
  }

  async getWeatherImpact(
    projectId?: string,
    startDate?: Date,
    endDate?: Date
  ): Promise<WeatherImpact> {
    const params = new URLSearchParams();
    if (projectId) {
      params.append('project_id', projectId);
    }
    if (startDate) {
      params.append('start_date', startDate.toISOString().split('T')[0]);
    }
    if (endDate) {
      params.append('end_date', endDate.toISOString().split('T')[0]);
    }

    return this.fetchWithRetry<WeatherImpact>(
      `${API_BASE_URL}/impact?${params.toString()}`
    );
  }

  async getIoTData(projectId?: string): Promise<IoTData> {
    const params = new URLSearchParams();
    if (projectId) {
      params.append('project_id', projectId);
    }

    return this.fetchWithRetry<IoTData>(
      `${API_BASE_URL}/iot-data?${params.toString()}`
    );
  }

  async getHistoricalData(
    startDate: Date,
    endDate: Date,
    metrics: string[] = ['temperature', 'humidity', 'precipitation']
  ): Promise<IoTReading[]> {
    const params = new URLSearchParams({
      start_date: startDate.toISOString().split('T')[0],
      end_date: endDate.toISOString().split('T')[0],
      metrics: metrics.join(',')
    });

    return this.fetchWithRetry<IoTReading[]>(
      `${API_BASE_URL}/historical?${params.toString()}`
    );
  }

  async refreshWeatherData(): Promise<AgriculturalMetrics> {
    return this.fetchWithRetry<AgriculturalMetrics>(
      `${API_BASE_URL}/agricultural-metrics?force_refresh=true`
    );
  }

  // Nouvelles méthodes pour l'intégration RH-météo

  async getHRWeatherMetrics(): Promise<WeatherHRMetrics> {
    try {
      const response = await axios.get(`${API_BASE_URL}/hr/metrics`);
      return response.data;
    } catch (error) {
      // Fallback sur le calcul local
      const weather = await this.getCurrentWeather();
      const forecast = await this.getForecast(3);
      
      const forecastCondition: WeatherCondition = {
        date: forecast.days[0].date,
        temperature: forecast.days[0].temp_max,
        humidity: forecast.days[0].humidity,
        precipitation: forecast.days[0].precipitation,
        wind_speed: 0, // Assuming wind_speed is not available in WeatherForecastDay
        conditions: forecast.days[0].conditions,
        uv_index: 0, // Assuming uv_index is not available in WeatherForecastDay
        cloud_cover: 0 // Assuming cloud_cover is not available in WeatherForecastDay
      };
      return this.calculateHRMetrics(weather, forecastCondition);
    }
  }

  async getScheduleAdjustments(date: string): Promise<WeatherScheduleAdjustment[]> {
    try {
      const response = await axios.get(`${API_BASE_URL}/hr/schedule-adjustments`, {
        params: { date }
      });
      return response.data;
    } catch (error) {
      console.error("Erreur lors de la récupération des ajustements d'horaires:", error);
      throw error;
    }
  }

  async proposeScheduleAdjustment(
    adjustment: Omit<WeatherScheduleAdjustment, 'status'>
  ): Promise<WeatherScheduleAdjustment> {
    const response = await axios.post(`${API_BASE_URL}/hr/schedule-adjustments`, adjustment);
    return response.data;
  }

  async getSafetyEquipment(conditions: string[]): Promise<WeatherSafetyEquipment[]> {
    try {
      const response = await axios.get(`${API_BASE_URL}/hr/safety-equipment`, {
        params: { conditions: conditions.join(',') }
      });
      return response.data;
    } catch (error) {
      // Fallback sur les règles locales
      return conditions.map(condition => ({
        weather_condition: condition,
        required_equipment: this.policyConfig.ppe_requirements[condition] || [],
        optional_equipment: [],
        instructions: `Équipement requis pour conditions: ${condition}`
      }));
    }
  }

  async getTrainingRequirements(weatherTypes: string[]): Promise<WeatherTrainingRequirement[]> {
    const response = await axios.get(`${API_BASE_URL}/hr/training-requirements`, {
      params: { weather_types: weatherTypes.join(',') }
    });
    return response.data;
  }

  async submitComplianceRecord(record: WeatherComplianceRecord): Promise<void> {
    await axios.post(`${API_BASE_URL}/hr/compliance-records`, record);
  }

  async getRiskAssessment(location: string): Promise<WeatherRiskAssessment> {
    try {
      const response = await axios.get(`${API_BASE_URL}/hr/risk-assessment`, {
        params: { location }
      });
      return response.data;
    } catch (error) {
      const weather = await this.getCurrentWeather();
      return this.generateRiskAssessment(weather, location);
    }
  }

  private analyzePrecipitationRisk(current: number, forecast: number[]): WeatherRisk {
    const avgForecast = forecast.reduce((a, b) => a + b, 0) / forecast.length;

    if (current > 20 || avgForecast > 20) {
      return {
        level: 'HIGH',
        message: "Risque d'inondation - Vérifier le drainage"
      };
    } else if (current > 10 || avgForecast > 10) {
      return {
        level: 'MEDIUM',
        message: "Précipitations modérées - Surveillance recommandée"
      };
    }
    return {
      level: 'LOW',
      message: "Conditions de précipitation normales"
    };
  }

  private analyzeTemperatureRisk(current: number, forecast: number[]): WeatherRisk {
    const maxTemp = Math.max(current, ...forecast);

    if (maxTemp > 35) {
      return {
        level: 'HIGH',
        message: "Risque de stress thermique - Protection nécessaire"
      };
    } else if (maxTemp > 30) {
      return {
        level: 'MEDIUM',
        message: "Températures élevées - Surveillance recommandée"
      };
    }
    return {
      level: 'LOW',
      message: "Températures dans la normale"
    };
  }

  private analyzeWindRisk(windSpeed: number): WeatherRisk {
    const { wind_thresholds } = this.policyConfig;
    
    if (windSpeed >= wind_thresholds.stop_work) {
      return {
        level: 'HIGH',
        message: 'Vents violents - Arrêt des activités extérieures'
      };
    } else if (windSpeed >= wind_thresholds.restricted_work) {
      return {
        level: 'MEDIUM',
        message: 'Vents forts - Activités extérieures restreintes'
      };
    }
    return {
      level: 'LOW',
      message: 'Conditions de vent acceptables'
    };
  }

  private getHighestRiskLevel(risks: WeatherRisk[]): 'LOW' | 'MEDIUM' | 'HIGH' {
    const levels = {
      'HIGH': 2,
      'MEDIUM': 1,
      'LOW': 0
    };
    
    const maxLevel = Math.max(...risks.map(risk => levels[risk.level]));
    return Object.keys(levels).find(
      key => levels[key as keyof typeof levels] === maxLevel
    ) as 'LOW' | 'MEDIUM' | 'HIGH';
  }

  private generateRecommendations(
    precipRisk: WeatherRisk,
    tempRisk: WeatherRisk
  ): string[] {
    const recommendations: string[] = [];

    if (precipRisk.level === 'HIGH') {
      recommendations.push(
        "Vérifier les systèmes de drainage",
        "Reporter les activités de plantation",
        "Protéger les jeunes plants"
      );
    } else if (precipRisk.level === 'MEDIUM') {
      recommendations.push(
        "Surveiller l'accumulation d'eau dans les parcelles"
      );
    }

    if (tempRisk.level === 'HIGH') {
      recommendations.push(
        "Augmenter l'irrigation",
        "Protéger les plants sensibles",
        "Éviter les travaux aux heures les plus chaudes"
      );
    } else if (tempRisk.level === 'MEDIUM') {
      recommendations.push(
        "Maintenir une surveillance de l'hydratation des plants"
      );
    }

    return recommendations.length > 0
      ? recommendations
      : ["Conditions favorables pour les activités agricoles normales"];
  }

  private calculateHRMetrics(
    current: WeatherCondition,
    forecast: WeatherCondition
  ): WeatherHRMetrics {
    const temperatureRisk = this.analyzeTemperatureRisk(current.temperature, [forecast.temperature]);
    const precipitationRisk = this.analyzePrecipitationRisk(current.precipitation, [forecast.precipitation]);
    const windRisk = this.analyzeWindRisk(current.wind_speed);

    return {
      current_conditions: current,
      risks: {
        temperature: temperatureRisk,
        precipitation: precipitationRisk,
        wind: windRisk,
        level: this.getHighestRiskLevel([temperatureRisk, precipitationRisk, windRisk])
      },
      schedule_adjustments: this.generateScheduleAdjustments(current),
      safety_requirements: this.generateSafetyRequirements(current),
      training_needs: this.generateTrainingNeeds(current),
      compliance: [],
      alerts: this.generateAlerts(temperatureRisk, precipitationRisk, windRisk)
    };
  }

  private generateScheduleAdjustments(
    weather: WeatherCondition
  ): WeatherScheduleAdjustment[] {
    const adjustments: WeatherScheduleAdjustment[] = [];
    const { temperature_thresholds } = this.policyConfig;

    if (weather.temperature >= temperature_thresholds.max_work) {
      adjustments.push({
        date: weather.date,
        original_schedule: { start: '09:00', end: '17:00' },
        adjusted_schedule: { start: '06:00', end: '14:00' },
        reason: 'Températures excessives - Horaires matinaux',
        affected_employees: [],
        status: 'PROPOSED'
      });
    } else if (weather.temperature >= temperature_thresholds.reduced_activity) {
      adjustments.push({
        date: weather.date,
        original_schedule: { start: '09:00', end: '17:00' },
        adjusted_schedule: { start: '07:00', end: '15:00' },
        reason: 'Températures élevées - Horaires adaptés',
        affected_employees: [],
        status: 'PROPOSED'
      });
    }

    return adjustments;
  }

  private generateSafetyRequirements(
    weather: WeatherCondition
  ): WeatherSafetyEquipment[] {
    const requirements: WeatherSafetyEquipment[] = [];
    const { temperature_thresholds } = this.policyConfig;

    if (weather.temperature >= temperature_thresholds.reduced_activity) {
      requirements.push({
        weather_condition: 'high_temperature',
        required_equipment: this.policyConfig.ppe_requirements.high_temperature,
        optional_equipment: [],
        instructions: 'Port obligatoire des équipements de protection contre la chaleur'
      });
    }

    return requirements;
  }

  private generateTrainingNeeds(
    weather: WeatherCondition
  ): WeatherTrainingRequirement[] {
    const needs: WeatherTrainingRequirement[] = [];
    const { temperature_thresholds } = this.policyConfig;

    if (weather.temperature >= temperature_thresholds.reduced_activity) {
      needs.push({
        weather_type: 'high_temperature',
        required_training: 'Prévention des risques liés à la chaleur',
        validity_period: 12,
        refresher_frequency: 12,
        priority: 'HIGH'
      });
    }

    return needs;
  }

  private generateAlerts(
    tempRisk: WeatherRisk,
    precipRisk: WeatherRisk,
    windRisk: WeatherRisk
  ): { type: 'SCHEDULE' | 'SAFETY' | 'EQUIPMENT' | 'TRAINING'; level: 'CRITICAL' | 'WARNING' | 'INFO'; message: string; affected_roles: string[]; }[] {
    const alerts: { type: 'SCHEDULE' | 'SAFETY' | 'EQUIPMENT' | 'TRAINING'; level: 'CRITICAL' | 'WARNING' | 'INFO'; message: string; affected_roles: string[]; }[] = [];

    if (tempRisk.level === 'HIGH') {
      alerts.push({
        type: 'SCHEDULE',
        level: 'CRITICAL',
        message: tempRisk.message,
        affected_roles: ['outdoor_workers', 'field_supervisors']
      });
    }

    if (precipRisk.level === 'HIGH') {
      alerts.push({
        type: 'SAFETY',
        level: 'WARNING',
        message: precipRisk.message,
        affected_roles: ['all_outdoor_staff']
      });
    }

    if (windRisk.level === 'HIGH') {
      alerts.push({
        type: 'SAFETY',
        level: 'CRITICAL',
        message: windRisk.message,
        affected_roles: ['all_staff']
      });
    }

    return alerts;
  }

  private generateRiskAssessment(
    weather: WeatherCondition,
    location: string
  ): WeatherRiskAssessment {
    const tempRisk = this.analyzeTemperatureRisk(weather.temperature, []);
    const precipRisk = this.analyzePrecipitationRisk(weather.precipitation, []);
    const windRisk = this.analyzeWindRisk(weather.wind_speed);

    const risks = [tempRisk, precipRisk, windRisk].filter(risk => risk.level !== 'LOW');
    
    return {
      date: weather.date,
      location,
      assessor: 'SYSTEM',
      conditions: weather,
      identified_risks: risks,
      control_measures: this.generateControlMeasures(risks),
      residual_risk_level: this.getHighestRiskLevel(risks),
      review_date: new Date(new Date(weather.date).getTime() + 24 * 60 * 60 * 1000).toISOString(),
      approval_status: 'PENDING'
    };
  }

  private generateControlMeasures(risks: WeatherRisk[]): string[] {
    const measures = new Set<string>();

    risks.forEach(risk => {
      if (risk.level === 'HIGH') {
        measures.add('Suspension des activités extérieures');
        measures.add('Mise en place d\'activités alternatives en intérieur');
      }
      if (risk.level === 'MEDIUM') {
        measures.add('Rotation accrue des équipes');
        measures.add('Pauses plus fréquentes');
        measures.add('Surveillance renforcée');
      }
    });

    return Array.from(measures);
  }

  isCacheValid(cachedAt?: string): boolean {
    if (!cachedAt) return false;
    
    const cacheTime = new Date(cachedAt).getTime();
    const currentTime = new Date().getTime();
    const cacheAge = currentTime - cacheTime;
    
    // Considérer le cache valide pendant 30 minutes
    return cacheAge < 30 * 60 * 1000;
  }

  getCacheAge(cachedAt?: string): string | null {
    if (!cachedAt) return null;
    
    const cacheTime = new Date(cachedAt);
    const currentTime = new Date();
    const diffMinutes = Math.floor((currentTime.getTime() - cacheTime.getTime()) / (1000 * 60));
    
    if (diffMinutes < 1) return "à l'instant";
    if (diffMinutes === 1) return "il y a 1 minute";
    return `il y a ${diffMinutes} minutes`;
  }

  shouldShowWarning(risk: WeatherRisk): boolean {
    return risk.level === 'HIGH';
  }

  getWarningMessage(metrics: AgriculturalMetrics | WeatherHRMetrics): string | null {
    const warnings: string[] = [];
    
    if ('precipitation' in metrics.risks && this.shouldShowWarning(metrics.risks.precipitation)) {
      warnings.push(metrics.risks.precipitation.message);
    }
    if (this.shouldShowWarning(metrics.risks.temperature)) {
      warnings.push(metrics.risks.temperature.message);
    }
    if ('wind' in metrics.risks && this.shouldShowWarning(metrics.risks.wind)) {
      warnings.push(metrics.risks.wind.message);
    }
    
    return warnings.length > 0 
      ? `ALERTE MÉTÉO: ${warnings.join(' - ')}`
      : null;
  }
}

export const weatherService = new WeatherService();
