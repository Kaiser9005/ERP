import axios from 'axios';
import { HRAnalytics, EmployeeStats, FormationAnalytics, ContractAnalytics, PayrollAnalytics, PerformancePrediction } from '../types/hr_analytics';

const API_BASE_URL = '/api/v1/hr/analytics';

export const getHRAnalytics = async (): Promise<HRAnalytics> => {
  const response = await axios.get(API_BASE_URL);
  return response.data;
};

export const getEmployeeStats = async (): Promise<EmployeeStats> => {
  const response = await axios.get(`${API_BASE_URL}/employee-stats`);
  return response.data;
};

export const getFormationAnalytics = async (): Promise<FormationAnalytics> => {
  const response = await axios.get(`${API_BASE_URL}/formation-analytics`);
  return response.data;
};

export const getContractAnalytics = async (): Promise<ContractAnalytics> => {
  const response = await axios.get(`${API_BASE_URL}/contract-analytics`);
  return response.data;
};

export const getPayrollAnalytics = async (): Promise<PayrollAnalytics> => {
  const response = await axios.get(`${API_BASE_URL}/payroll-analytics`);
  return response.data;
};

export const predictEmployeePerformance = async (employeeId: number): Promise<PerformancePrediction> => {
  const response = await axios.get(`${API_BASE_URL}/predict-performance/${employeeId}`);
  return response.data;
};
