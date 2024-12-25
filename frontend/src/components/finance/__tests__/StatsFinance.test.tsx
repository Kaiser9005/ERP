import { render, screen } from '@testing-library/react';
import StatsFinance from '../StatsFinance';
import { FinanceStats } from '../../../types/finance';

const mockStats: FinanceStats = {
  revenue: 1200000,
  revenueVariation: {
    valeur: 15,
    type: 'hausse'
  },
  profit: 250000,
  profitVariation: {
    valeur: 10,
    type: 'hausse'
  },
  cashflow: 300000,
  cashflowVariation: {
    valeur: 5,
    type: 'baisse'
  },
  expenses: 950000,
  expensesVariation: {
    valeur: 12,
    type: 'hausse'
  },
  tresorerie: 15000000,
  variation_tresorerie: {
    valeur: 10,
    type: 'hausse'
  },
  factures_impayees: 5,
  paiements_prevus: 8,
  budget_mensuel: 20000000,
  depenses_mois: 18000000
};

describe('StatsFinance', () => {
  it('renders financial statistics', () => {
    render(<StatsFinance stats={mockStats} />);
    
    expect(screen.getByText('Statistiques Financières')).toBeInTheDocument();
    
    // Revenus
    expect(screen.getByText('Revenus')).toBeInTheDocument();
    expect(screen.getByText('1 200 000 FCFA')).toBeInTheDocument();
    expect(screen.getByText('▲ 15%')).toBeInTheDocument();
    
    // Bénéfice
    expect(screen.getByText('Bénéfice')).toBeInTheDocument();
    expect(screen.getByText('250 000 FCFA')).toBeInTheDocument();
    expect(screen.getByText('▲ 10%')).toBeInTheDocument();
    
    // Flux de Trésorerie
    expect(screen.getByText('Flux de Trésorerie')).toBeInTheDocument();
    expect(screen.getByText('300 000 FCFA')).toBeInTheDocument();
    expect(screen.getByText('▼ 5%')).toBeInTheDocument();
    
    // Dépenses
    expect(screen.getByText('Dépenses')).toBeInTheDocument();
    expect(screen.getByText('950 000 FCFA')).toBeInTheDocument();
    expect(screen.getByText('▲ 12%')).toBeInTheDocument();
  });

  it('handles missing values', () => {
    const partialStats: FinanceStats = {
      revenue: 1200000,
      expenses: 950000
    };

    render(<StatsFinance stats={partialStats} />);
    
    expect(screen.getByText('Statistiques Financières')).toBeInTheDocument();
    expect(screen.getByText('Revenus')).toBeInTheDocument();
    expect(screen.getByText('1 200 000 FCFA')).toBeInTheDocument();
    expect(screen.getByText('Dépenses')).toBeInTheDocument();
    expect(screen.getByText('950 000 FCFA')).toBeInTheDocument();
  });
});
