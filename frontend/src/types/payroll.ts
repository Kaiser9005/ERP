export interface PayrollSlip {
  id: string;
  contract_id: string;
  period_start: string;
  period_end: string;
  worked_hours: number;
  overtime_hours: number;
  base_salary: number;
  overtime_amount: number;
  bonus: number;
  deductions: number;
  bonus_details: Record<string, number>;
  deduction_details: Record<string, number>;
  employer_contributions: number;
  employee_contributions: number;
  gross_total: number;
  net_total: number;
  is_paid: boolean;
  payment_date: string | null;
  created_at: string;
  updated_at: string;
}

export interface CreatePayrollRequest {
  contract_id: string;
  period_start: string;
  period_end: string;
  worked_hours: number;
  overtime_hours: number;
  overtime_amount: number;
  bonus: number;
  deductions: number;
  bonus_details: Record<string, number>;
  deduction_details: Record<string, number>;
  employer_contributions: number;
  employee_contributions: number;
}

export interface UpdatePayrollRequest {
  worked_hours?: number;
  overtime_hours?: number;
  overtime_amount?: number;
  bonus?: number;
  deductions?: number;
  bonus_details?: Record<string, number>;
  deduction_details?: Record<string, number>;
}

export interface PayrollStats {
  total_gross: number;
  total_net: number;
  total_employer_contributions: number;
  total_employee_contributions: number;
  total_bonus: number;
  total_deductions: number;
  average_gross: number;
  average_net: number;
  period_start: string;
  period_end: string;
}

export interface OvertimeCalculation {
  overtime_hours: number;
  overtime_amount: number;
}

export interface ContributionsCalculation {
  employer: number;
  employee: number;
}

export interface PayrollPeriodQuery {
  start_date: string;
  end_date: string;
}

export interface PayrollValidationResponse {
  message: string;
}

export interface PayrollDeleteResponse {
  message: string;
}
