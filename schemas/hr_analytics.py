from pydantic import BaseModel
from typing import Dict, List, Optional, Any
from datetime import datetime

class EmployeeStats(BaseModel):
    total_employees: int
    active_contracts: int
    formations_completed: int
    formation_completion_rate: float

class FormationAnalytics(BaseModel):
    total_formations: int
    total_participations: int
    completion_rate: float
    formations_by_type: Dict[str, int]
    success_rate_by_formation: Dict[str, float]

class ContractAnalytics(BaseModel):
    total_contracts: int
    contracts_by_type: Dict[str, int]
    contract_duration_stats: Dict[str, float]
    contract_renewal_rate: float

class PayrollAnalytics(BaseModel):
    total_payroll: float
    average_salary: float
    salary_distribution: Dict[str, int]
    payroll_trends: Dict[str, float]

class PerformancePrediction(BaseModel):
    predicted_performance: float
    confidence: float

class HRAnalytics(BaseModel):
    employee_stats: EmployeeStats
    formation_analytics: FormationAnalytics
    contract_analytics: ContractAnalytics
    payroll_analytics: PayrollAnalytics
