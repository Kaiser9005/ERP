import { useMutation, useQuery, useQueryClient, UseQueryOptions } from '@tanstack/react-query';
import axios from 'axios';
import { format } from 'date-fns';
import { fr } from 'date-fns/locale';

import {
  IoTSensor,
  SensorReading,
  SensorStats,
  SensorHealth,
  IoTSensorFormData,
  SensorReadingFormData,
  SensorQueryParams
} from '../types/iot';

const API_BASE = '/api/v1/iot';

// Clés de requête
export const iotKeys = {
  all: ['iot'] as const,
  sensors: () => [...iotKeys.all, 'sensors'] as const,
  sensor: (id: string) => [...iotKeys.sensors(), id] as const,
  parcelleSensors: (parcelleId: string) => [...iotKeys.sensors(), 'parcelle', parcelleId] as const,
  readings: (sensorId: string) => [...iotKeys.sensor(sensorId), 'readings'] as const,
  stats: (sensorId: string) => [...iotKeys.sensor(sensorId), 'stats'] as const,
  health: (sensorId: string) => [...iotKeys.sensor(sensorId), 'health'] as const,
};

// Hooks pour les capteurs
export const useCreateSensor = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (data: IoTSensorFormData) => {
      const response = await axios.post<IoTSensor>(`${API_BASE}/sensors`, data);
      return response.data;
    },
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: iotKeys.sensors() });
      if (data.parcelle_id) {
        queryClient.invalidateQueries({ queryKey: iotKeys.parcelleSensors(data.parcelle_id) });
      }
    },
  });
};

export const useSensor = (id: string) => {
  return useQuery({
    queryKey: iotKeys.sensor(id),
    queryFn: async () => {
      const response = await axios.get<IoTSensor>(`${API_BASE}/sensors/${id}`);
      return response.data;
    }
  });
};

export const useParcelleSensors = (parcelleId: string) => {
  return useQuery({
    queryKey: iotKeys.parcelleSensors(parcelleId),
    queryFn: async () => {
      const response = await axios.get<IoTSensor[]>(`${API_BASE}/parcelles/${parcelleId}/sensors`);
      return response.data;
    }
  });
};

export const useUpdateSensor = (id: string) => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (data: Partial<IoTSensorFormData>) => {
      const response = await axios.patch<IoTSensor>(`${API_BASE}/sensors/${id}`, data);
      return response.data;
    },
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: iotKeys.sensor(id) });
      if (data.parcelle_id) {
        queryClient.invalidateQueries({ queryKey: iotKeys.parcelleSensors(data.parcelle_id) });
      }
    },
  });
};

export const useDeleteSensor = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (id: string) => {
      await axios.delete(`${API_BASE}/sensors/${id}`);
    },
    onSuccess: (_, id) => {
      queryClient.invalidateQueries({ queryKey: iotKeys.sensors() });
      queryClient.removeQueries({ queryKey: iotKeys.sensor(id) });
    },
  });
};

// Hooks pour les lectures
export const useCreateReading = (sensorId: string) => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (data: SensorReadingFormData) => {
      const response = await axios.post<SensorReading>(
        `${API_BASE}/sensors/${sensorId}/readings`,
        data
      );
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: iotKeys.readings(sensorId) });
      queryClient.invalidateQueries({ queryKey: iotKeys.stats(sensorId) });
      queryClient.invalidateQueries({ queryKey: iotKeys.health(sensorId) });
    },
  });
};

export const useSensorReadings = (
  sensorId: string,
  params?: SensorQueryParams,
  options?: Omit<UseQueryOptions<SensorReading[], Error>, 'queryKey' | 'queryFn'>
) => {
  return useQuery({
    queryKey: [...iotKeys.readings(sensorId), params],
    queryFn: async () => {
      const response = await axios.get<SensorReading[]>(`${API_BASE}/sensors/${sensorId}/readings`, {
        params: {
          ...params,
          start_date: params?.start_date ? format(new Date(params.start_date), "yyyy-MM-dd'T'HH:mm:ss", { locale: fr }) : undefined,
          end_date: params?.end_date ? format(new Date(params.end_date), "yyyy-MM-dd'T'HH:mm:ss", { locale: fr }) : undefined,
        },
      });
      return response.data;
    },
    ...options
  });
};

export const useSensorStats = (
  sensorId: string,
  params?: Pick<SensorQueryParams, 'start_date' | 'end_date'>,
  options?: Omit<UseQueryOptions<SensorStats, Error>, 'queryKey' | 'queryFn'>
) => {
  return useQuery({
    queryKey: [...iotKeys.stats(sensorId), params],
    queryFn: async () => {
      const response = await axios.get<SensorStats>(`${API_BASE}/sensors/${sensorId}/stats`, {
        params: {
          start_date: params?.start_date ? format(new Date(params.start_date), "yyyy-MM-dd'T'HH:mm:ss", { locale: fr }) : undefined,
          end_date: params?.end_date ? format(new Date(params.end_date), "yyyy-MM-dd'T'HH:mm:ss", { locale: fr }) : undefined,
        },
      });
      return response.data;
    },
    ...options
  });
};

export const useSensorHealth = (sensorId: string) => {
  return useQuery({
    queryKey: iotKeys.health(sensorId),
    queryFn: async () => {
      const response = await axios.get<SensorHealth>(`${API_BASE}/sensors/${sensorId}/health`);
      return response.data;
    },
    refetchInterval: 60 * 1000, // Rafraîchir toutes les minutes
  });
};

// Hook pour les lectures en masse
export const useCreateBatchReadings = (sensorId: string) => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (data: SensorReadingFormData[]) => {
      const response = await axios.post<Array<{
        success: boolean;
        reading?: SensorReading;
        error?: string;
      }>>(`${API_BASE}/sensors/batch-readings`, data, {
        params: { sensor_id: sensorId },
      });
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: iotKeys.readings(sensorId) });
      queryClient.invalidateQueries({ queryKey: iotKeys.stats(sensorId) });
      queryClient.invalidateQueries({ queryKey: iotKeys.health(sensorId) });
    },
  });
};

// Hook pour la vérification de santé globale
export const useCheckAllSensorsHealth = (parcelleId?: string) => {
  return useQuery({
    queryKey: ['sensors', 'health-check', parcelleId],
    queryFn: async () => {
      const response = await axios.get<Array<{
        sensor_id: string;
        code: string;
        health?: SensorHealth;
        error?: string;
      }>>(`${API_BASE}/sensors/health-check`, {
        params: parcelleId ? { parcelle_id: parcelleId } : undefined,
      });
      return response.data;
    },
    refetchInterval: 5 * 60 * 1000, // Rafraîchir toutes les 5 minutes
  });
};
