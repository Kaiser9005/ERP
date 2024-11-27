import { render, screen } from '@testing-library/react';
import { ThemeProvider } from '@mui/material';
import { theme } from '../../../theme';
import { ModuleImpactGrid } from '../ModuleImpactGrid';
import type { Activity } from '../../../types/analytics_cross_module';

const mockActivities: Activity[] = [
  {
    id: 'ACT-001',
    type: 'PRODUCTION',
    timestamp: '2024-03-15T10:00:00',
    description: 'Mise à jour production',
    impact: 'HIGH',
    metrics: { efficiency: 0.95 }
  }
];

const mockModules = {
  hr: {
    analytics: {
      total_employees: 100,
      active_contracts: 95,
      completed_trainings: 45,
      training_completion_rate: 0.85,
      recent_activities: mockActivities
    },
    production_impact: {
      productivity: {
        current_rate: 0.92,
        trend: 0.05,
        factors: ['Formation', 'Motivation']
      },
      skills_coverage: {
        coverage_rate: 0.88,
        gaps: ['Technique', 'Management'],
        critical_skills: ['Leadership']
      },
      training_impact: {
        productivity_gain: 0.15,
        cost_savings: 25000,
        skill_improvements: { 'Technique': 0.2 }
      }
    },
    finance_impact: {
      labor_costs: {
        total: 150000,
        by_department: { 'Production': 80000 },
        trends: [0.1, 0.2]
      },
      training_roi: {
        value: 2.5,
        by_program: { 'Technique': 3.0 },
        projected_benefits: 50000
      },
      productivity_value: {
        total: 500000,
        by_employee: { 'EMP001': 5000 },
        potential_gains: 50000
      }
    },
    weather_impact: {
      score: 0.75,
      facteurs: ['Température', 'Humidité'],
      couts_additionnels: { 'Climatisation': 5000 },
      risques: ['Fatigue'],
      opportunites: ['Télétravail']
    }
  },
  production: {
    analytics: {
      daily_production: 1000,
      efficiency_rate: 0.88,
      active_sensors: 25,
      quality_metrics: {
        defect_rate: 0.02,
        customer_satisfaction: 0.95,
        compliance_rate: 0.98
      },
      recent_activities: mockActivities
    },
    hr_impact: {
      workload: {
        current_load: 0.85,
        capacity: 1.0,
        bottlenecks: ['Équipe A']
      },
      skills_required: {
        current: ['Technique'],
        future: ['IA'],
        gaps: ['Data Science']
      },
      schedule_impact: {
        delays: 2,
        overtime_needed: 10,
        resource_conflicts: ['Équipe B']
      }
    },
    finance_impact: {
      production_costs: {
        total: 200000,
        by_category: { 'Matériel': 150000 },
        optimization_potential: 20000
      },
      revenue_impact: {
        total: 800000,
        by_product: { 'PROD-A': 500000 },
        growth_potential: 100000
      },
      efficiency_savings: {
        total: 50000,
        by_initiative: { 'Automatisation': 30000 },
        projected: 75000
      }
    },
    weather_impact: {
      score: 0.65,
      facteurs: ['Température'],
      couts_additionnels: { 'Énergie': 10000 },
      risques: ['Surchauffe'],
      opportunites: ['Optimisation']
    }
  },
  finance: {
    analytics: {
      daily_revenue: 50000,
      monthly_expenses: 450000,
      cash_flow: 150000,
      budget_status: {
        current: 1000000,
        projected: 1200000,
        variance: 200000
      },
      recent_activities: mockActivities,
      recent_transactions: []
    },
    hr_impact: {
      budget_constraints: {
        limit: 500000,
        current_usage: 0.75,
        projected_needs: 600000
      },
      hiring_capacity: {
        budget_available: 100000,
        positions_open: 5,
        timeline: 'Q2 2024'
      },
      training_budget: {
        allocated: 50000,
        used: 30000,
        remaining: 20000
      }
    },
    production_impact: {
      investment_capacity: {
        available: 200000,
        committed: 150000,
        projected: 300000
      },
      maintenance_budget: {
        allocated: 75000,
        used: 50000,
        projected_needs: 100000
      },
      expansion_potential: {
        budget_available: 300000,
        roi_projected: 0.25,
        timeline: 'Q3 2024'
      }
    },
    weather_impact: {
      score: 0.55,
      facteurs: ['Précipitations'],
      couts_additionnels: { 'Maintenance': 15000 },
      risques: ['Retards'],
      opportunites: ['Économies']
    }
  },
  inventory: {
    analytics: {
      total_items: 5000,
      low_stock_items: [],
      stock_value: 750000,
      recent_movements: [],
      recent_activities: mockActivities
    },
    production_impact: {
      stock_availability: {
        rate: 0.95,
        critical_items: ['ITEM-001'],
        impact_level: 0.8
      },
      production_constraints: {
        current: ['Stock faible'],
        projected: ['Rupture possible'],
        mitigation_actions: ['Commander']
      },
      quality_impact: {
        defect_rate: 0.01,
        cost_impact: 5000,
        improvement_actions: ['Contrôle']
      }
    },
    finance_impact: {
      storage_costs: {
        total: 25000,
        by_category: { 'Stockage': 15000 },
        optimization_potential: 5000
      },
      stock_value: {
        total: 750000,
        by_category: { 'Matières premières': 500000 },
        trend: 0.1
      },
      turnover_rate: {
        global: 4.5,
        by_category: { 'Produits finis': 5.0 },
        optimization_target: 5.0
      }
    },
    weather_impact: {
      score: 0.45,
      facteurs: ['Humidité'],
      couts_additionnels: { 'Stockage': 5000 },
      risques: ['Détérioration'],
      opportunites: ['Réorganisation']
    }
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
      production: {
        score: 0.65,
        facteurs: ['Température'],
        couts_additionnels: { 'Énergie': 10000 },
        risques: ['Surchauffe'],
        opportunites: ['Optimisation']
      },
      hr: {
        score: 0.75,
        facteurs: ['Température'],
        couts_additionnels: { 'Climatisation': 5000 },
        risques: ['Fatigue'],
        opportunites: ['Télétravail']
      },
      finance: {
        score: 0.55,
        facteurs: ['Précipitations'],
        couts_additionnels: { 'Maintenance': 15000 },
        risques: ['Retards'],
        opportunites: ['Économies']
      },
      inventory: {
        score: 0.45,
        facteurs: ['Humidité'],
        couts_additionnels: { 'Stockage': 5000 },
        risques: ['Détérioration'],
        opportunites: ['Réorganisation']
      }
    }
  },
  projects: {
    active_projects: 15,
    completion_predictions: {
      on_time: 10,
      delayed: 3,
      at_risk: ['PROJ-001', 'PROJ-002']
    },
    resource_optimization: {
      savings_potential: 50000,
      recommendations: ['Optimiser allocation ressources', 'Réduire délais'],
      implementation_plan: ['Phase 1', 'Phase 2']
    },
    impact: {
      hr: {
        resource_usage: 0.85,
        budget_impact: 75000,
        timeline_impact: 'Moyen'
      },
      production: {
        resource_usage: 0.75,
        budget_impact: 100000,
        timeline_impact: 'Élevé'
      },
      finance: {
        resource_usage: 0.65,
        budget_impact: 150000,
        timeline_impact: 'Faible'
      }
    }
  }
};

describe('ModuleImpactGrid', () => {
  it('affiche tous les modules', () => {
    render(
      <ThemeProvider theme={theme}>
        <ModuleImpactGrid modules={mockModules} />
      </ThemeProvider>
    );

    expect(screen.getByText('Impact RH')).toBeInTheDocument();
    expect(screen.getByText('Impact Production')).toBeInTheDocument();
    expect(screen.getByText('Impact Finance')).toBeInTheDocument();
    expect(screen.getByText('Impact Inventaire')).toBeInTheDocument();
    expect(screen.getByText('Impact Météo Global')).toBeInTheDocument();
    expect(screen.getByText('Impact Projets')).toBeInTheDocument();
  });

  it('affiche les métriques RH', () => {
    render(
      <ThemeProvider theme={theme}>
        <ModuleImpactGrid modules={mockModules} />
      </ThemeProvider>
    );

    expect(screen.getByText('Formation')).toBeInTheDocument();
    expect(screen.getByText('85%')).toBeInTheDocument();
    expect(screen.getByText('Productivité')).toBeInTheDocument();
    expect(screen.getByText('92%')).toBeInTheDocument();
  });

  it('affiche les métriques de production', () => {
    render(
      <ThemeProvider theme={theme}>
        <ModuleImpactGrid modules={mockModules} />
      </ThemeProvider>
    );

    expect(screen.getByText('Efficacité')).toBeInTheDocument();
    expect(screen.getByText('88%')).toBeInTheDocument();
    expect(screen.getByText('Charge RH')).toBeInTheDocument();
    expect(screen.getByText('85%')).toBeInTheDocument();
  });

  it('affiche les métriques financières', () => {
    render(
      <ThemeProvider theme={theme}>
        <ModuleImpactGrid modules={mockModules} />
      </ThemeProvider>
    );

    expect(screen.getByText('Budget RH')).toBeInTheDocument();
    expect(screen.getByText('75%')).toBeInTheDocument();
    expect(screen.getByText('Cash Flow')).toBeInTheDocument();
    expect(screen.getByText('150000')).toBeInTheDocument();
  });

  it('affiche les métriques d\'inventaire', () => {
    render(
      <ThemeProvider theme={theme}>
        <ModuleImpactGrid modules={mockModules} />
      </ThemeProvider>
    );

    expect(screen.getByText('Stock')).toBeInTheDocument();
    expect(screen.getByText('5000')).toBeInTheDocument();
    expect(screen.getByText('Production')).toBeInTheDocument();
    expect(screen.getByText('95%')).toBeInTheDocument();
  });

  it('affiche les impacts météo', () => {
    render(
      <ThemeProvider theme={theme}>
        <ModuleImpactGrid modules={mockModules} />
      </ThemeProvider>
    );

    expect(screen.getByText('Score d\'impact')).toBeInTheDocument();
    expect(screen.getByText('Facteurs')).toBeInTheDocument();
  });

  it('affiche les métriques de projets', () => {
    render(
      <ThemeProvider theme={theme}>
        <ModuleImpactGrid modules={mockModules} />
      </ThemeProvider>
    );

    expect(screen.getByText('Projets actifs')).toBeInTheDocument();
    expect(screen.getByText('15')).toBeInTheDocument();
    expect(screen.getByText('Projets à risque')).toBeInTheDocument();
    expect(screen.getByText('PROJ-001, PROJ-002')).toBeInTheDocument();
  });

  it('utilise le bon style de grille', () => {
    const { container } = render(
      <ThemeProvider theme={theme}>
        <ModuleImpactGrid modules={mockModules} />
      </ThemeProvider>
    );

    const grid = container.querySelector('.MuiGrid-container');
    expect(grid).toHaveStyle({ gap: '16px' });
  });

  it('applique les styles de thème appropriés', () => {
    const { container } = render(
      <ThemeProvider theme={theme}>
        <ModuleImpactGrid modules={mockModules} />
      </ThemeProvider>
    );

    const papers = container.querySelectorAll('.MuiPaper-root');
    papers.forEach(paper => {
      expect(paper).toHaveStyle({ padding: '16px' });
    });
  });
});
