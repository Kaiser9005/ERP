import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import FinanceStats from '@components/comptabilite/FinanceStats';
import { getComptabiliteStats } from '@services/comptabilite';

// Mock du service
jest.mock('@services/comptabilite', () => ({
  getComptabiliteStats: jest.fn()
}));

const mockStatsData = {
  revenue: 150000,
  revenueVariation: {
    value: 5.2,
    type: 'increase'
  },
  expenses: 120000,
  expensesVariation: {
    value: 3.1,
    type: 'decrease'
  },
  profit: 30000,
  profitVariation: {
    value: 8.5,
    type: 'increase'
  },
  cashflow: 45000,
  cashflowVariation: {
    value: 4.2,
    type: 'increase'
  }
};

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: false,
    },
  },
});

const renderWithQuery = (component: React.ReactElement) => {
  return render(
    <QueryClientProvider client={queryClient}>
      {component}
    </QueryClientProvider>
  );
};

describe('FinanceStats', () => {
  beforeEach(() => {
    // Reset des mocks
    jest.resetAllMocks();
    // Configuration du mock pour getStats
    (getComptabiliteStats as jest.Mock).mockResolvedValue(mockStatsData);
  });

  it('affiche le chargement initialement', () => {
    renderWithQuery(<FinanceStats />);
    expect(screen.getAllByTestId('skeleton')).toHaveLength(4);
  });

  it('affiche les statistiques financières après chargement', async () => {
    renderWithQuery(<FinanceStats />);

    // Vérification du chiffre d'affaires
    await waitFor(() => {
      expect(screen.getByText('Chiffre d\'affaires')).toBeInTheDocument();
      expect(screen.getByText('150 000,00 €')).toBeInTheDocument();
      expect(screen.getByText('5.2%')).toBeInTheDocument();
    });

    // Vérification des charges
    expect(screen.getByText('Charges')).toBeInTheDocument();
    expect(screen.getByText('120 000,00 €')).toBeInTheDocument();
    expect(screen.getByText('3.1%')).toBeInTheDocument();

    // Vérification du bénéfice
    expect(screen.getByText('Bénéfice')).toBeInTheDocument();
    expect(screen.getByText('30 000,00 €')).toBeInTheDocument();
    expect(screen.getByText('8.5%')).toBeInTheDocument();

    // Vérification de la trésorerie
    expect(screen.getByText('Trésorerie')).toBeInTheDocument();
    expect(screen.getByText('45 000,00 €')).toBeInTheDocument();
    expect(screen.getByText('4.2%')).toBeInTheDocument();
  });

  it('affiche les variations avec les bonnes couleurs', async () => {
    renderWithQuery(<FinanceStats />);

    await waitFor(() => {
      // Vérification des variations positives (vert)
      const increaseChips = screen.getAllByTestId('increase-chip');
      expect(increaseChips).toHaveLength(3);
      increaseChips.forEach(chip => {
        expect(chip).toHaveClass('MuiChip-colorSuccess');
      });

      // Vérification des variations négatives (rouge)
      const decreaseChips = screen.getAllByTestId('decrease-chip');
      expect(decreaseChips).toHaveLength(1);
      decreaseChips.forEach(chip => {
        expect(chip).toHaveClass('MuiChip-colorError');
      });
    });
  });

  it('affiche les infobulles au survol', async () => {
    renderWithQuery(<FinanceStats />);

    await waitFor(() => {
      const infoButtons = screen.getAllByRole('button', { name: /info/i });
      expect(infoButtons).toHaveLength(4);

      // Vérification des titres des infobulles
      expect(screen.getByTitle('Chiffre d\'affaires total du mois en cours')).toBeInTheDocument();
      expect(screen.getByTitle('Total des charges du mois en cours')).toBeInTheDocument();
      expect(screen.getByTitle('Bénéfice net après déduction des charges')).toBeInTheDocument();
      expect(screen.getByTitle('Solde de trésorerie disponible')).toBeInTheDocument();
    });
  });

  it('affiche un message d\'erreur en cas d\'échec du chargement', async () => {
    const error = new Error('Erreur de chargement');
    (getComptabiliteStats as jest.Mock).mockRejectedValue(error);

    renderWithQuery(<FinanceStats />);

    await waitFor(() => {
      expect(screen.getByText('Aucune donnée statistique disponible')).toBeInTheDocument();
    });
  });

  it('met à jour les données périodiquement', async () => {
    jest.useFakeTimers();
    renderWithQuery(<FinanceStats />);

    await waitFor(() => {
      expect(getComptabiliteStats).toHaveBeenCalledTimes(1);
    });

    // Avance le temps de 5 minutes
    jest.advanceTimersByTime(5 * 60 * 1000);

    await waitFor(() => {
      expect(getComptabiliteStats).toHaveBeenCalledTimes(2);
    });

    jest.useRealTimers();
  });
});
