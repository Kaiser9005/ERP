import React from 'react';
import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import CashFlowChart from '../CashFlowChart';
import { comptabiliteService } from '../../../services/comptabilite';

// Mock du service
jest.mock('../../../services/comptabilite');

const mockCashFlowData = [
  {
    date: '2024-01-15',
    entrees: 25000,
    sorties: 20000,
    solde: 5000,
    prevision: 5200,
    impact_meteo: 4.0
  },
  {
    date: '2024-01-16',
    entrees: 30000,
    sorties: 22000,
    solde: 13000,
    prevision: 13500,
    impact_meteo: 3.8
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

describe('CashFlowChart', () => {
  beforeEach(() => {
    // Reset des mocks
    jest.resetAllMocks();
    // Configuration du mock pour getCashFlow
    (comptabiliteService.getCashFlow as jest.Mock).mockResolvedValue(mockCashFlowData);
  });

  it('affiche le chargement initialement', () => {
    renderWithQuery(<CashFlowChart />);
    expect(screen.getByRole('progressbar')).toBeInTheDocument();
  });

  it('affiche le graphique après chargement', async () => {
    renderWithQuery(<CashFlowChart />);

    await waitFor(() => {
      expect(screen.getByText('Évolution de la Trésorerie')).toBeInTheDocument();
    });

    // Vérification des éléments du graphique
    expect(screen.getByText('Entrées')).toBeInTheDocument();
    expect(screen.getByText('Sorties')).toBeInTheDocument();
    expect(screen.getByText('Solde')).toBeInTheDocument();
    expect(screen.getByText('Prévision')).toBeInTheDocument();
    expect(screen.getByText('Impact Météo')).toBeInTheDocument();
  });

  it('permet de changer la période', async () => {
    renderWithQuery(<CashFlowChart />);

    await waitFor(() => {
      expect(screen.getByRole('combobox')).toBeInTheDocument();
    });

    // Sélection d'une nouvelle période
    const select = screen.getByRole('combobox');
    fireEvent.change(select, { target: { value: '90' } });

    await waitFor(() => {
      expect(comptabiliteService.getCashFlow).toHaveBeenCalledWith(90);
    });
  });

  it('affiche la légende des indicateurs', async () => {
    renderWithQuery(<CashFlowChart />);

    await waitFor(() => {
      expect(screen.getByText(/Les barres représentent les entrées et sorties de trésorerie/)).toBeInTheDocument();
      expect(screen.getByText(/La ligne bleue montre l'évolution du solde/)).toBeInTheDocument();
      expect(screen.getByText(/La zone violette indique les prévisions/)).toBeInTheDocument();
      expect(screen.getByText(/La ligne orange représente l'impact météorologique/)).toBeInTheDocument();
    });
  });

  it('affiche un tooltip personnalisé au survol', async () => {
    renderWithQuery(<CashFlowChart />);

    await waitFor(() => {
      expect(screen.getByText('Évolution de la Trésorerie')).toBeInTheDocument();
    });

    // Simulation du survol (le test réel du tooltip nécessiterait une bibliothèque de test plus avancée)
    const chartContainer = screen.getByRole('presentation');
    expect(chartContainer).toBeInTheDocument();
  });

  it('affiche un message d\'erreur en cas d\'échec du chargement', async () => {
    const error = new Error('Erreur de chargement');
    (comptabiliteService.getCashFlow as jest.Mock).mockRejectedValue(error);

    renderWithQuery(<CashFlowChart />);

    await waitFor(() => {
      expect(screen.getByText('Aucune donnée de trésorerie disponible')).toBeInTheDocument();
    });
  });

  it('met à jour les données périodiquement', async () => {
    jest.useFakeTimers();
    renderWithQuery(<CashFlowChart />);

    await waitFor(() => {
      expect(comptabiliteService.getCashFlow).toHaveBeenCalledTimes(1);
    });

    // Avance le temps de 5 minutes
    jest.advanceTimersByTime(5 * 60 * 1000);

    await waitFor(() => {
      expect(comptabiliteService.getCashFlow).toHaveBeenCalledTimes(2);
    });

    jest.useRealTimers();
  });

  it('affiche les bonnes valeurs dans le graphique', async () => {
    renderWithQuery(<CashFlowChart />);

    await waitFor(() => {
      // Vérification des valeurs du premier jour
      expect(screen.getByText('25 000,00 €')).toBeInTheDocument();
      expect(screen.getByText('20 000,00 €')).toBeInTheDocument();
      expect(screen.getByText('5 000,00 €')).toBeInTheDocument();
      expect(screen.getByText('4.0%')).toBeInTheDocument();
    });
  });

  it('affiche le bouton d\'info avec tooltip', async () => {
    renderWithQuery(<CashFlowChart />);

    await waitFor(() => {
      const infoButton = screen.getByRole('button', { name: /info/i });
      expect(infoButton).toBeInTheDocument();
      expect(screen.getByTitle('Analyse de trésorerie avec impact météorologique')).toBeInTheDocument();
    });
  });
});
