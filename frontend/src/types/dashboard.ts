export interface ModuleStats {
  timestamp: string;
  modules: {
    hr: HRSummary;
    production: ProductionSummary;
    finance: FinanceSummary;
    inventory: InventorySummary;
    weather: WeatherSummary;
    projects: ProjectsSummary;
  };
  alerts: Alert[];
  predictions: MLPredictions;
}

export interface HRSummary {
  total_employees: number;
  active_contracts: number;
  completed_trainings: number;
  training_completion_rate: number;
  recent_activities: Activity[];
}

export interface ProductionSummary {
  daily_production: number;
  efficiency_rate: number;
  active_sensors: number;
  quality_metrics: QualityMetrics;
  recent_activities: Activity[];
}

export interface FinanceSummary {
  daily_revenue: number;
  monthly_expenses: number;
  cash_flow: number;
  budget_status: BudgetStatus;
  recent_transactions: Transaction[];
}

export interface InventorySummary {
  total_items: number;
  low_stock_items: StockItem[];
  stock_value: number;
  recent_movements: StockMovement[];
}

export interface WeatherSummary {
  current_conditions: WeatherConditions;
  daily_forecast: WeatherForecast[];
  alerts: WeatherAlert[];
  production_impact: ProductionImpact;
}

export interface ProjectsSummary {
  active_projects: number;
  completion_predictions: CompletionPrediction[];
  resource_optimization: ResourceOptimization;
  recent_activities: Activity[];
}

export interface Activity {
  id: string;
  type: string;
  description: string;
  timestamp: string;
  user: string;
  module: string;
  status: string;
}

export interface QualityMetrics {
  overall_score: number;
  defect_rate: number;
  compliance_rate: number;
  efficiency_score: number;
}

export interface BudgetStatus {
  current: number;
  planned: number;
  variance: number;
  status: 'under' | 'over' | 'on_track';
}

export interface Transaction {
  id: string;
  amount: number;
  type: string;
  category: string;
  timestamp: string;
  description: string;
}

export interface StockItem {
  id: string;
  name: string;
  current_quantity: number;
  minimum_quantity: number;
  unit: string;
  last_updated: string;
}

export interface StockMovement {
  id: string;
  item_id: string;
  type: 'in' | 'out';
  quantity: number;
  timestamp: string;
  reason: string;
}

export interface WeatherConditions {
  temperature: number;
  humidity: number;
  wind_speed: number;
  precipitation: number;
  condition: string;
}

export interface WeatherForecast {
  date: string;
  temperature_high: number;
  temperature_low: number;
  precipitation_chance: number;
  condition: string;
}

export interface WeatherAlert {
  id: string;
  type: string;
  severity: 'low' | 'medium' | 'high';
  description: string;
  start_time: string;
  end_time: string;
}

export interface ProductionImpact {
  risk_level: 'low' | 'medium' | 'high';
  affected_areas: string[];
  recommendations: string[];
}

export interface CompletionPrediction {
  project_id: string;
  project_name: string;
  predicted_completion: string;
  confidence: number;
  risk_factors: string[];
}

export interface ResourceOptimization {
  recommendations: string[];
  potential_savings: number;
  efficiency_gain: number;
}

export interface Alert {
  id: string;
  module: string;
  type: string;
  severity: 'low' | 'medium' | 'high';
  message: string;
  timestamp: string;
  status: 'active' | 'acknowledged' | 'resolved';
  priority: number;
}

export interface MLPredictions {
  production: {
    output_forecast: number;
    quality_prediction: number;
    maintenance_predictions: string[];
  };
  finance: {
    revenue_forecast: number;
    expense_forecast: number;
    cash_flow_prediction: number;
  };
  inventory: {
    stock_predictions: StockPrediction[];
    reorder_recommendations: string[];
  };
  hr: {
    attendance_forecast: number;
    training_needs: string[];
    performance_predictions: string[];
  };
}

export interface StockPrediction {
  item_id: string;
  item_name: string;
  predicted_quantity: number;
  confidence: number;
  reorder_point: number;
}

export type ModuleType = 'hr' | 'production' | 'finance' | 'inventory' | 'weather' | 'projects';

export interface ModuleDetails {
  module: ModuleType;
  expanded: boolean;
}
