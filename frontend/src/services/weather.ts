import { api } from './api';

export interface WeatherData {
  temperature: number;
  humidity: number;
  windSpeed: number;
  uvIndex: number;
  forecast: {
    date: string;
    temperature: number;
    precipitation: number;
  }[];
}

export const getWeatherData = async (): Promise<WeatherData> => {
  const response = await api.get('/weather/current');
  return response.data;
};