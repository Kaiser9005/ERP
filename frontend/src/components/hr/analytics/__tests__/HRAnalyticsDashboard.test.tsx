import React from 'react';
import { render, screen } from '@testing-library/react';
import { useHRAnalytics } from '../../../../services/hr_analytics';
import HRAnalyticsDashboard from '../HRAnalyticsDashboard';

// Mock des hooks
jest.mock('../../../../services/hr_analytics');

const mockAnalytics = {
  employee_stats: {
    total_employees: 100,
    active_contracts: 85,
    formations_completed: 15,
    formation_completion_rate: 0.75
  },
  formation_analytics: {
    total_formations: 20,
    total_participations: 150,
    completion_rate: 0.85,
    formations_by_type: {
      technique: 10,
      management: 5,
      securite: 5
    },
    success_rate_by_formation: {
      technique: 0.9,
      management: 0.85,
      securite: 0.95
    }
  },
  contract_analytics: {
    total_contracts: 90,
    contracts_by_type: {
      cdi: 70,
      cdd: 15,
      stage: 5
    },
    contract_duration_stats: {
      average: 730,
      min: 90,
      max: 3650
    },
    contract_renewal_rate: 0.75
  },
  payroll_analytics: {
    total_payroll: 350000,
    average_salary: 3500,
    salary_distribution: {
      junior: 2500,
      intermediaire: 3500,
      senior: 4500
    },
    payroll_trends: {
      '2024-03': 5.2
    }
  }
};

describe('HRAnalyticsDashboard', () => {
  beforeEach(() => {
    (useHRAnalytics as jest.Mock).mockReturnValue({
      data: mockAnalytics,
      isLoading: false,
      error: null
    });
  });

  it('affiche le titre du tableau de bord', () => {
    render(<HRAnalyticsDashboard />);
    expect(screen.getByText('Tableau de Bord RH')).toBeInTheDocument();
  });

  it('affiche un loader pendant le chargement', () => {
    (useHRAnalytics as jest.Mock).mockReturnValue({
      data: null,
      isLoading: true,
      error: null
    });

    render(<HRAnalyticsDashboard />);
    expect(screen.getByRole('progressbar')).toBeInTheDocument();
  });

  it('affiche une erreur en cas d\'échec', () => {
    (useHRAnalytics as jest.Mock).mockReturnValue({
      data: null,
      isLoading: false,
      error: new Error('Erreur de chargement')
    });

    render(<HRAnalyticsDashboard />);
    expect(screen.getByText(/Une erreur est survenue/)).toBeInTheDocument();
  });

  it('affiche les statistiques des formations', () => {
    render(<HRAnalyticsDashboard />);
    expect(screen.getByText('Formations')).toBeInTheDocument();
    expect(screen.getByText('20')).toBeInTheDocument();
    expect(screen.getByText('85%')).toBeInTheDocument();
  });

  it('affiche les statistiques des contrats', () => {
    render(<HRAnalyticsDashboard />);
    expect(screen.getByText('Contrats')).toBeInTheDocument();
    expect(screen.getByText('90')).toBeInTheDocument();
    expect(screen.getByText('75%')).toBeInTheDocument();
  });

  it('affiche les statistiques de la masse salariale', () => {
    render(<HRAnalyticsDashboard />);
    expect(screen.getByText('Masse Salariale')).toBeInTheDocument();
    expect(screen.getByText('350 000,00 €')).toBeInTheDocument();
    expect(screen.getByText('5,2%')).toBeInTheDocument();
  });

  it('affiche un message si aucune donnée n\'est disponible', () => {
    (useHRAnalytics as jest.Mock).mockReturnValue({
      data: null,
      isLoading: false,
      error: null
    });

    render(<HRAnalyticsDashboard />);
    expect(screen.getByText('Aucune donnée disponible')).toBeInTheDocument();
  });
});
