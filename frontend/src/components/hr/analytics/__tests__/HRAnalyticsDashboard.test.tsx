import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from 'react-query';
import { HRAnalyticsDashboard } from '../HRAnalyticsDashboard';
import { getHRAnalytics } from '../../../../services/hr_analytics';

// Mock du service
jest.mock('../../../../services/hr_analytics');

// Données de test
const mockAnalytics = {
  employee_stats: {
    total_employees: 100,
    active_contracts: 80,
    formations_completed: 150,
    formation_completion_rate: 0.75
  },
  formation_analytics: {
    total_formations: 20,
    total_participations: 150,
    completion_rate: 0.8,
    formations_by_type: {
      technique: 10,
      securite: 5,
      management: 5
    },
    success_rate_by_formation: {
      '1': 0.9,
      '2': 0.85
    }
  },
  contract_analytics: {
    total_contracts: 100,
    contracts_by_type: {
      CDI: 60,
      CDD: 30,
      Stage: 10
    },
    contract_duration_stats: {
      average: 365,
      min: 90,
      max: 730
    },
    contract_renewal_rate: 0.7
  },
  payroll_analytics: {
    total_payroll: 500000,
    average_salary: 3500,
    salary_distribution: {
      Q1: 25,
      Q2: 25,
      Q3: 25,
      Q4: 25
    },
    payroll_trends: {
      '2024-01': 480000,
      '2024-02': 485000,
      '2024-03': 500000
    }
  }
};

// Configuration du client React Query
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: false
    }
  }
});

const renderWithQueryClient = (component: React.ReactElement) => {
  return render(
    <QueryClientProvider client={queryClient}>
      {component}
    </QueryClientProvider>
  );
};

describe('HRAnalyticsDashboard', () => {
  beforeEach(() => {
    (getHRAnalytics as jest.Mock).mockResolvedValue(mockAnalytics);
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  it('affiche un loader pendant le chargement', () => {
    renderWithQueryClient(<HRAnalyticsDashboard />);
    expect(screen.getByRole('progressbar')).toBeInTheDocument();
  });

  it('affiche les statistiques générales', async () => {
    renderWithQueryClient(<HRAnalyticsDashboard />);

    await waitFor(() => {
      expect(screen.getByText('Employés Total')).toBeInTheDocument();
      expect(screen.getByText('100')).toBeInTheDocument();
      expect(screen.getByText('Contrats Actifs')).toBeInTheDocument();
      expect(screen.getByText('80')).toBeInTheDocument();
      expect(screen.getByText('Formations Complétées')).toBeInTheDocument();
      expect(screen.getByText('150')).toBeInTheDocument();
      expect(screen.getByText('Taux de Complétion')).toBeInTheDocument();
      expect(screen.getByText('75')).toBeInTheDocument();
    });
  });

  it('affiche les statistiques des formations', async () => {
    renderWithQueryClient(<HRAnalyticsDashboard />);

    await waitFor(() => {
      expect(screen.getByText('Types de Formation')).toBeInTheDocument();
      expect(screen.getByText('Total Formations')).toBeInTheDocument();
      expect(screen.getByText('20')).toBeInTheDocument();
      expect(screen.getByText('Total Participations')).toBeInTheDocument();
      expect(screen.getByText('150')).toBeInTheDocument();
    });
  });

  it('affiche les statistiques des contrats', async () => {
    renderWithQueryClient(<HRAnalyticsDashboard />);

    await waitFor(() => {
      expect(screen.getByText('Types de Contrat')).toBeInTheDocument();
      expect(screen.getByText('Total Contrats')).toBeInTheDocument();
      expect(screen.getByText('100')).toBeInTheDocument();
      expect(screen.getByText('Taux de Renouvellement')).toBeInTheDocument();
      expect(screen.getByText('70')).toBeInTheDocument();
    });
  });

  it('affiche les statistiques des salaires', async () => {
    renderWithQueryClient(<HRAnalyticsDashboard />);

    await waitFor(() => {
      expect(screen.getByText('Évolution des Salaires')).toBeInTheDocument();
      expect(screen.getByText('Total Masse Salariale')).toBeInTheDocument();
      expect(screen.getByText('500 000,00 €')).toBeInTheDocument();
      expect(screen.getByText('Salaire Moyen')).toBeInTheDocument();
      expect(screen.getByText('3 500,00 €')).toBeInTheDocument();
    });
  });

  it('affiche une erreur en cas d\'échec de chargement', async () => {
    (getHRAnalytics as jest.Mock).mockRejectedValue(new Error('Erreur de chargement'));
    renderWithQueryClient(<HRAnalyticsDashboard />);

    await waitFor(() => {
      expect(screen.getByText('Une erreur est survenue lors du chargement des analytics')).toBeInTheDocument();
    });
  });
});
