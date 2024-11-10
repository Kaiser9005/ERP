import axios from 'axios';

const WEATHER_API_KEY = import.meta.env.VITE_WEATHER_API_KEY;
const WEATHER_LOCATION = import.meta.env.VITE_WEATHER_LOCATION;
const BASE_URL = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline';

interface WeatherConditions {
  timestamp: string;
  temperature: number;
  humidity: number;
  precipitation: number;
  wind_speed: number;
  conditions: string;
  uv_index: number;
  cloud_cover: number;
}

interface WeatherForecastDay {
  date: string;
  temp_max: number;
  temp_min: number;
  precipitation: number;
  humidity: number;
  conditions: string;
  description: string;
}

interface WeatherForecast {
  location: string;
  days: WeatherForecastDay[];
}

interface WeatherRisk {
  level: 'LOW' | 'MEDIUM' | 'HIGH';
  message: string;
}

interface AgriculturalMetrics {
  current_conditions: WeatherConditions;
  risks: {
    precipitation: WeatherRisk;
    temperature: WeatherRisk;
    level: 'LOW' | 'MEDIUM' | 'HIGH';
  };
  recommendations: string[];
}

interface WeatherResponse {
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

class WeatherService {
  private async fetchWeatherData<T>(endpoint: string, params: Record<string, string> = {}): Promise<T> {
    try {
      const response = await axios.get<T>(`${BASE_URL}/${endpoint}`, {
        params: {
          key: WEATHER_API_KEY,
          unitGroup: 'metric',
          contentType: 'json',
          ...params
        }
      });
      return response.data;
    } catch (error) {
      console.error('Erreur lors de la récupération des données météo:', error);
      throw error;
    }
  }

  async getCurrentWeather(): Promise<WeatherConditions> {
    const data = await this.fetchWeatherData<WeatherResponse>(`${WEATHER_LOCATION}/today`, {
      include: 'current'
    });

    const current = data.currentConditions;
    return {
      timestamp: new Date().toISOString(),
      temperature: current.temp,
      humidity: current.humidity,
      precipitation: current.precip,
      wind_speed: current.windspeed,
      conditions: current.conditions,
      uv_index: current.uvindex,
      cloud_cover: current.cloudcover
    };
  }

  async getForecast(days: number = 7): Promise<WeatherForecast> {
    const data = await this.fetchWeatherData<WeatherResponse>(`${WEATHER_LOCATION}/next/${days}days`);

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

  async getAgriculturalMetrics(): Promise<AgriculturalMetrics> {
    try {
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
          level: this.getHighestRiskLevel(precipitationRisk, temperatureRisk)
        },
        recommendations: this.generateRecommendations(precipitationRisk, temperatureRisk)
      };
    } catch (error) {
      console.error('Erreur lors du calcul des métriques agricoles:', error);
      throw error;
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
        message: "Risque de stress thermique pour les cultures"
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

  private getHighestRiskLevel(
    risk1: WeatherRisk,
    risk2: WeatherRisk
  ): 'LOW' | 'MEDIUM' | 'HIGH' {
    const levels: Record<'LOW' | 'MEDIUM' | 'HIGH', number> = {
      LOW: 0,
      MEDIUM: 1,
      HIGH: 2
    };
    return levels[risk1.level] > levels[risk2.level] ? risk1.level : risk2.level;
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
}

export const weatherService = new WeatherService();
