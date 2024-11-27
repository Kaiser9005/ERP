import { render, screen, waitFor } from '@testing-library/react';
import { ThemeProvider } from '@mui/material';
import { theme } from '../../../theme';
import { CrossModuleAnalytics } from '../CrossModuleAnalytics';
import { useAnalyticsCrossModule } from '../../../services/analytics_cross_module';

// Mock le service
jest.mock('../../../services/analytics_cross_module');

const mockAnalytics = {
  timestamp: '2024-03-15T10:00:00',
  periode: {
    debut: '2024-02-15',
    fin: '2024-03-15'
  },
  modules: {
    hr: {
      analytics: {
        total_employees: 100,
        active_contracts: 95,
        completed_trainings: 45,
        training_completion_rate: 0.85,
        recent_activities: []
      },
      production_impact: {
        productivity: { current_rate: 0.92 },
        skills_coverage: { coverage_rate: 0.88 },
        training_impact: { productivity_gain: 0.15 }
      },
      finance_impact: {
        labor_costs: { total: 150000 },
        training_roi: { value: 2.5 },
        productivity_value: { total: 500000 }
      },
      weather_impact: { score: 0.75 }
    },
    production: {
      analytics: {
        daily_production: 1000,
        efficiency_rate: 0.88,
        active_sensors: 25,
        quality_metrics: { defect_rate: 0.02 }
      },
      hr_impact: {
        workload: { current_load: 0.85 },
        skills_required: { current: [] },
        schedule_impact: { delays: 2 }
      },
      finance_impact: {
        production_costs: { total: 200000 },
        revenue_impact: { total: 800000 },
        efficiency_savings: { total: 50000 }
      },
      weather_impact: { score: 0.65 }
    },
    finance: {
      analytics: {
        daily_revenue: 50000,
        monthly_expenses: 450000,
        cash_flow: 150000,
        budget_status: { current: 1000000 }
      },
      hr_impact: {
        budget_constraints: { current_usage: 0.75 },
        hiring_capacity: { budget_available: 100000 },
        training_budget: { allocated: 50000 }
      },
      production_impact: {
        investment_capacity: { available: 200000 },
        maintenance_budget: { allocated: 75000 },
        expansion_potential: { budget_available: 300000 }
      },
      weather_impact: { score: 0.55 }
    },
    inventory: {
      analytics: {
        total_items: 5000,
        low_stock_items: [],
        stock_value: 750000,
        recent_movements: []
      },
      production_impact: {
        stock_availability: { rate: 0.95 },
        production_constraints: { current: [] },
        quality_impact: { defect_rate: 0.01 }
      },
      finance_impact: {
        storage_costs: { total: 25000 },
        stock_value: { total: 750000 },
        turnover_rate: { global: 4.5 }
      },
      weather_impact: { score: 0.45 }
    },
    weather: {
      current: {
        temperature: 22,
        humidity: 65,
        precipitation: 0,
        wind_speed: 10
      },
      forecast: [],
      alerts: [],
      impact: {
        production: { score: 0.65, facteurs: [] },
        hr: { score: 0.75, facteurs: [] },
        finance: { score: 0.55, facteurs: [] },
        inventory: { score: 0.45, facteurs: [] }
      }
    }
  },
  correlations: {
    hr_production: 0.85,
    production_finance: 0.75,
    weather_global: 0.65,
    inventory_finance: 0.80
  },
  predictions: {
    hr: { predictions: [], confidence: 0.85, risk_level: 0.15 },
    production: { predictions: [], confidence: 0.82, risk_level: 0.18 },
    finance: { predictions: [], confidence: 0.88, risk_level: 0.12 },
    inventory: { predictions: [], confidence: 0.90, risk_level: 0.10 },
    cross_module: { predictions: [], confidence: 0.85, risk_level: 0.15 }
  },
  recommendations: [
    {
      type: 'CORRELATION',
      priority: 'HIGH',
      modules: ['hr', 'production'],
      description: 'Forte corrélation entre formation et productivité',
      actions: ['Augmenter le budget formation', 'Planifier des formations ciblées']
    }
  ]
};

describe('CrossModuleAnalytics', () => {
  beforeEach(() => {
    (useAnalyticsCrossModule as jest.Mock).mockReturnValue({
      getUnifiedAnalytics: jest.fn().mockResolvedValue(mockAnalytics)
    });
  });

  it('affiche le chargement initialement', () => {
    render(
      <ThemeProvider theme={theme}>
        <CrossModuleAnalytics />
      </ThemeProvider>
    );
    expect(screen.getByText('Chargement des analytics...')).toBeInTheDocument();
  });

  it('affiche les données une fois chargées', async () => {
    render(
      <ThemeProvider theme={theme}>
        <CrossModuleAnalytics />
      </ThemeProvider>
    );

    await waitFor(() => {
      expect(screen.getByText('Corrélations entre modules')).toBeInTheDocument();
      expect(screen.getByText('Prédictions ML')).toBeInTheDocument();
      expect(screen.getByText('Impact entre modules')).toBeInTheDocument();
      expect(screen.getByText('Recommandations')).toBeInTheDocument();
    });
  });

  it('affiche les statistiques clés', async () => {
    render(
      <ThemeProvider theme={theme}>
        <CrossModuleAnalytics />
      </ThemeProvider>
    );

    await waitFor(() => {
      expect(screen.getByText('Impact RH')).toBeInTheDocument();
      expect(screen.getByText('Impact Production')).toBeInTheDocument();
      expect(screen.getByText('Impact Finance')).toBeInTheDocument();
      expect(screen.getByText('Impact Inventaire')).toBeInTheDocument();
    });
  });

  it('gère les erreurs correctement', async () => {
    (useAnalyticsCrossModule as jest.Mock).mockReturnValue({
      getUnifiedAnalytics: jest.fn().mockRejectedValue(new Error('Erreur test'))
    });

    render(
      <ThemeProvider theme={theme}>
        <CrossModuleAnalytics />
      </ThemeProvider>
    );

    await waitFor(() => {
      expect(screen.getByText('Erreur lors de la récupération des données')).toBeInTheDocument();
    });
  });
});
