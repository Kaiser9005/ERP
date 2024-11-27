export interface EmployeeStats {
  total_employees: number;
  active_contracts: number;
  formations_completed: number;
  formation_completion_rate: number;
}

export interface FormationAnalytics {
  total_formations: number;
  total_participations: number;
  completion_rate: number;
  formations_by_type: Record<string, number>;
  success_rate_by_formation: Record<string, number>;
}

export interface ContractAnalytics {
  total_contracts: number;
  contracts_by_type: Record<string, number>;
  contract_duration_stats: {
    average: number;
    min: number;
    max: number;
  };
  contract_renewal_rate: number;
}

export interface PayrollAnalytics {
  total_payroll: number;
  average_salary: number;
  salary_distribution: Record<string, number>;
  payroll_trends: Record<string, number>;
}

export interface PerformancePrediction {
  predicted_performance: number;
  confidence: number;
}

export interface HRAnalytics {
  employee_stats: EmployeeStats;
  formation_analytics: FormationAnalytics;
  contract_analytics: ContractAnalytics;
  payroll_analytics: PayrollAnalytics;
}
