import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import Balance from '../rapports/Balance';
import { getBalance } from '../../../services/comptabilite';
import { TypeCompteComptable } from '../../../types/comptabilite';

// Mock du service
jest.mock('../../../services/comptabilite', () => ({
  getBalance: jest.fn()
}));

const mockBalanceData = [
  {
    compte: {
      numero: '101',
      libelle: 'Capital',
      type: TypeCompteComptable.PASSIF
    },
    debit: 0,
    credit: 10000,
    solde: -10000
  },
  {
    compte: {
      numero: '512',
      libelle: 'Banque',
      type: TypeCompteComptable.ACTIF
    },
    debit: 15000,
    credit: 5000,
    solde: 10000
  }
];

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

describe('Balance', () => {
  beforeEach(() => {
    // Reset des mocks
    jest.resetAllMocks();
    // Configuration du mock pour getBalance
    (getBalance as jest.Mock).mockResolvedValue(mockBalanceData);
  });

  it('affiche le chargement initialement', () => {
    renderWithQuery(<Balance />);
    expect(screen.getByRole('progressbar')).toBeInTheDocument();
  });

  it('affiche les données de la balance après chargement', async () => {
    renderWithQuery(<Balance />);

    await waitFor(() => {
      expect(screen.getByText('Balance des comptes')).toBeInTheDocument();
    });

    // Vérification des comptes
    expect(screen.getByText('Capital')).toBeInTheDocument();
    expect(screen.getByText('Banque')).toBeInTheDocument();

    // Vérification des montants
    expect(screen.getByText('10 000,00 €')).toBeInTheDocument();
    expect(screen.getByText('15 000,00 €')).toBeInTheDocument();
  });

  it('affiche un message quand il n\'y a pas de données', async () => {
    (getBalance as jest.Mock).mockResolvedValue([]);
    
    renderWithQuery(<Balance />);

    await waitFor(() => {
      expect(screen.getByText('Aucune donnée disponible pour la période sélectionnée')).toBeInTheDocument();
    });
  });

  it('affiche une erreur en cas d\'échec du chargement', async () => {
    const error = new Error('Erreur de chargement');
    (getBalance as jest.Mock).mockRejectedValue(error);

    renderWithQuery(<Balance />);

    await waitFor(() => {
      expect(screen.getByText('Erreur lors du chargement de la balance')).toBeInTheDocument();
    });
  });

  it('met à jour les données périodiquement', async () => {
    jest.useFakeTimers();
    renderWithQuery(<Balance />);

    await waitFor(() => {
      expect(getBalance).toHaveBeenCalledTimes(1);
    });

    // Avance le temps de 5 minutes
    jest.advanceTimersByTime(5 * 60 * 1000);

    await waitFor(() => {
      expect(getBalance).toHaveBeenCalledTimes(2);
    });

    jest.useRealTimers();
  });
});
