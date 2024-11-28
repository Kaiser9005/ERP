/**
 * Types pour les analytics cross-module
 */

export interface CrossModuleAnalytics {
  timestamp: string;
  periode: {
    debut: string;
    fin: string;
  };
  modules: {
    hr: HRAnalytics;
    production: ProductionAnalytics;
    finance: FinanceAnalytics;
    inventory: InventoryAnalytics;
    weather: AnalyseMétéo;
    projects: ProjectsAnalytics;
  };
  correlations: ModuleCorrelations;
  predictions: ModulePredictions;
  recommendations: CrossModuleRecommendation[];
}

export interface HRAnalytics {
  analytics: {
    total_employees: number;
    active_contracts: number;
    completed_trainings: number;
    training_completion_rate: number;
    recent_activities: Activity[];
  };
  production_impact: {
    productivity: ProductivityMetrics;
    skills_coverage: SkillsCoverage;
    training_impact: TrainingImpact;
  };
  finance_impact: {
    labor_costs: LaborCosts;
    training_roi: TrainingROI;
    productivity_value: ProductivityValue;
  };
  weather_impact: WeatherImpact;
}

export interface ProductionAnalytics {
  analytics: {
    daily_production: number;
    efficiency_rate: number;
    active_sensors: number;
    quality_metrics: QualityMetrics;
    recent_activities: Activity[];
  };
  hr_impact: {
    workload: WorkloadMetrics;
    skills_required: SkillsRequired;
    schedule_impact: ScheduleImpact;
  };
  finance_impact: {
    production_costs: ProductionCosts;
    revenue_impact: RevenueImpact;
    efficiency_savings: EfficiencySavings;
  };
  weather_impact: WeatherImpact;
}

export interface FinanceAnalytics {
  analytics: {
    daily_revenue: number;
    monthly_expenses: number;
    cash_flow: number;
    budget_status: BudgetStatus;
    recent_transactions: Transaction[];
  };
  hr_impact: {
    budget_constraints: BudgetConstraints;
    hiring_capacity: HiringCapacity;
    training_budget: TrainingBudget;
  };
  production_impact: {
    investment_capacity: InvestmentCapacity;
    maintenance_budget: MaintenanceBudget;
    expansion_potential: ExpansionPotential;
  };
  weather_impact: WeatherImpact;
}

export interface InventoryAnalytics {
  analytics: {
    total_items: number;
    low_stock_items: StockItem[];
    stock_value: number;
    recent_movements: StockMovement[];
  };
  production_impact: {
    stock_availability: StockAvailability;
    production_constraints: ProductionConstraints;
    quality_impact: QualityImpact;
  };
  finance_impact: {
    storage_costs: StorageCosts;
    stock_value: StockValue;
    turnover_rate: TurnoverRate;
  };
  weather_impact: WeatherImpact;
}

export interface AnalyseMétéo {
  current: WeatherConditions;
  forecast: WeatherForecast[];
  alerts: WeatherAlert[];
  impact: {
    production: WeatherImpact;
    hr: WeatherImpact;
    finance: WeatherImpact;
    inventory: WeatherImpact;
  };
}

export interface ProjectsAnalytics {
  active_projects: number;
  completion_predictions: CompletionPredictions;
  resource_optimization: ResourceOptimization;
  impact: {
    hr: ProjectImpact;
    production: ProjectImpact;
    finance: ProjectImpact;
  };
}

export interface ModuleCorrelations {
  hr_production: number;
  production_finance: number;
  weather_global: number;
  inventory_finance: number;
}

export interface ModulePredictions {
  hr: MLPrediction;
  production: MLPrediction;
  finance: MLPrediction;
  inventory: MLPrediction;
  cross_module: CrossModulePrediction;
}

export interface CrossModuleRecommendation {
  type: 'CORRELATION' | 'ML_PREDICTION' | 'OPTIMIZATION' | 'ALERT';
  priority: 'HIGH' | 'MEDIUM' | 'LOW';
  modules: string[];
  description: string;
  actions: string[];
  expected_impact?: {
    savings?: number;
    timeline?: string;
  };
}

// Interfaces communes
export interface Activity {
  id: string;
  type: string;
  description: string;
  timestamp: string;
  module: string;
  impact_level: number;
}

export interface WeatherImpact {
  score: number;
  facteurs: string[];
  couts_additionnels: Record<string, number>;
  risques: string[];
  opportunites: string[];
}

export interface MLPrediction {
  predictions: any[];
  confidence: number;
  risk_level: number;
  recommended_actions: string[];
}

export interface CrossModulePrediction extends MLPrediction {
  correlations: Record<string, number>;
  impacts: Record<string, any>;
}

// Interfaces spécifiques
export interface ProductivityMetrics {
  current_rate: number;
  trend: number;
  factors: string[];
}

export interface SkillsCoverage {
  coverage_rate: number;
  gaps: string[];
  critical_skills: string[];
}

export interface TrainingImpact {
  productivity_gain: number;
  cost_savings: number;
  skill_improvements: Record<string, number>;
}

export interface LaborCosts {
  total: number;
  by_department: Record<string, number>;
  trends: number[];
}

export interface TrainingROI {
  value: number;
  by_program: Record<string, number>;
  projected_benefits: number;
}

export interface ProductivityValue {
  total: number;
  by_employee: Record<string, number>;
  potential_gains: number;
}

export interface QualityMetrics {
  defect_rate: number;
  customer_satisfaction: number;
  compliance_rate: number;
}

export interface WorkloadMetrics {
  current_load: number;
  capacity: number;
  bottlenecks: string[];
}

export interface SkillsRequired {
  current: string[];
  future: string[];
  gaps: string[];
}

export interface ScheduleImpact {
  delays: number;
  overtime_needed: number;
  resource_conflicts: string[];
}

export interface ProductionCosts {
  total: number;
  by_category: Record<string, number>;
  optimization_potential: number;
}

export interface RevenueImpact {
  total: number;
  by_product: Record<string, number>;
  growth_potential: number;
}

export interface EfficiencySavings {
  total: number;
  by_initiative: Record<string, number>;
  projected: number;
}

export interface BudgetStatus {
  current: number;
  projected: number;
  variance: number;
}

export interface Transaction {
  id: string;
  type: string;
  amount: number;
  date: string;
  category: string;
}

export interface BudgetConstraints {
  limit: number;
  current_usage: number;
  projected_needs: number;
}

export interface HiringCapacity {
  budget_available: number;
  positions_open: number;
  timeline: string;
}

export interface TrainingBudget {
  allocated: number;
  used: number;
  remaining: number;
}

export interface InvestmentCapacity {
  available: number;
  committed: number;
  projected: number;
}

export interface MaintenanceBudget {
  allocated: number;
  used: number;
  projected_needs: number;
}

export interface ExpansionPotential {
  budget_available: number;
  roi_projected: number;
  timeline: string;
}

export interface StockItem {
  id: string;
  name: string;
  quantity: number;
  threshold: number;
}

export interface StockMovement {
  id: string;
  type: string;
  quantity: number;
  date: string;
  item_id: string;
}

export interface StockAvailability {
  rate: number;
  critical_items: string[];
  impact_level: number;
}

export interface ProductionConstraints {
  current: string[];
  projected: string[];
  mitigation_actions: string[];
}

export interface QualityImpact {
  defect_rate: number;
  cost_impact: number;
  improvement_actions: string[];
}

export interface StorageCosts {
  total: number;
  by_category: Record<string, number>;
  optimization_potential: number;
}

export interface StockValue {
  total: number;
  by_category: Record<string, number>;
  trend: number;
}

export interface TurnoverRate {
  global: number;
  by_category: Record<string, number>;
  optimization_target: number;
}

export interface WeatherConditions {
  temperature: number;
  humidity: number;
  precipitation: number;
  wind_speed: number;
}

export interface WeatherForecast extends WeatherConditions {
  date: string;
  probability: number;
}

export interface WeatherAlert {
  type: string;
  severity: string;
  description: string;
  start_date: string;
  end_date: string;
}

export interface CompletionPredictions {
  on_time: number;
  delayed: number;
  at_risk: string[];
}

export interface ResourceOptimization {
  savings_potential: number;
  recommendations: string[];
  implementation_plan: string[];
}

export interface ProjectImpact {
  resource_usage: number;
  budget_impact: number;
  timeline_impact: string;
}
