import { render, screen } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import CashFlowChart from '../CashFlowChart';
import { getCashFlowData } from '../../../services/finance';

// Mock du service
jest.mock('../../../services/finance', () => ({
  getCashFlowData: jest.fn()
}));

const mockCashFlowData = {
  labels: ['Jan', 'Fév', 'Mar'],
  recettes: [100000, 150000, 200000],
  depenses: [80000, 90000, 100000],
  solde: [20000, 60000, 100000],
  previsions: [120000, 180000, 220000],
  impact_meteo: [0, -10000, -20000]
};

describe('CashFlowChart', () => {
  let queryClient: QueryClient;

  beforeEach(() => {
    queryClient = new QueryClient({
      defaultOptions: {
        queries: {
          retry: false
        }
      }
    });
    jest.clearAllMocks();
  });

  it('affiche le graphique avec les données', async () => {
    (getCashFlowData as jest.Mock).mockResolvedValue(mockCashFlowData);

    render(
      <QueryClientProvider client={queryClient}>
        <CashFlowChart />
      </QueryClientProvider>
    );

    // Vérifie l'état de chargement
    expect(screen.getByRole('progressbar')).toBeInTheDocument();

    // Vérifie le titre
    expect(await screen.findByText('Flux de Trésorerie')).toBeInTheDocument();

    // Vérifie les légendes
    expect(screen.getByText('Recettes')).toBeInTheDocument();
    expect(screen.getByText('Dépenses')).toBeInTheDocument();
    expect(screen.getByText('Solde')).toBeInTheDocument();
    expect(screen.getByText('Prévisions')).toBeInTheDocument();
    expect(screen.getByText('Impact Météo')).toBeInTheDocument();

    // Vérifie les labels des mois
    expect(screen.getByText('Jan')).toBeInTheDocument();
    expect(screen.getByText('Fév')).toBeInTheDocument();
    expect(screen.getByText('Mar')).toBeInTheDocument();
  });

  it('affiche un message d\'erreur quand la requête échoue', async () => {
    (getCashFlowData as jest.Mock).mockRejectedValue(new Error('Erreur test'));

    render(
      <QueryClientProvider client={queryClient}>
        <CashFlowChart />
      </QueryClientProvider>
    );

    expect(await screen.findByText('Erreur lors du chargement des données de trésorerie')).toBeInTheDocument();
  });

  it('utilise la bonne configuration de react-query', () => {
    render(
      <QueryClientProvider client={queryClient}>
        <CashFlowChart />
      </QueryClientProvider>
    );

    // Vérifie que le service est appelé
    expect(getCashFlowData).toHaveBeenCalled();

    // Vérifie que la requête est configurée correctement
    const queries = queryClient.getQueryCache().findAll();
    const cashflowQuery = queries.find(
      query => Array.isArray(query.queryKey) && 
      query.queryKey[0] === 'finance' && 
      query.queryKey[1] === 'cashflow'
    );

    expect(cashflowQuery).toBeDefined();
  });

  it('affiche un état de chargement', () => {
    (getCashFlowData as jest.Mock).mockImplementation(() => new Promise(() => {}));

    render(
      <QueryClientProvider client={queryClient}>
        <CashFlowChart />
      </QueryClientProvider>
    );

    expect(screen.getByRole('progressbar')).toBeInTheDocument();
  });
});
