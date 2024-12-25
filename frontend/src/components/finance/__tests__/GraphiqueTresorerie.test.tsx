import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import { QueryClient, QueryClientProvider } from 'react-query';
import GraphiqueTresorerie from '../GraphiqueTresorerie';
import { getDonneesTresorerie } from '../../../services/finance';

// Mock du service finance
jest.mock('../../../services/finance', () => ({
  getDonneesTresorerie: jest.fn()
}));

const mockGetDonneesTresorerie = getDonneesTresorerie as jest.MockedFunction<typeof getDonneesTresorerie>;

describe('GraphiqueTresorerie', () => {
  const queryClient = new QueryClient();

  const mockData = {
    soldeActuel: 2500000,
    entrees: 1800000,
    sorties: 1400000,
    previsionsTresorerie: 2900000
  };

  beforeEach(() => {
    mockGetDonneesTresorerie.mockResolvedValue(mockData);
  });

  const renderComponent = () => {
    render(
      <QueryClientProvider client={queryClient}>
        <GraphiqueTresorerie />
      </QueryClientProvider>
    );
  };

  it('affiche le titre du graphique', async () => {
    renderComponent();
    expect(await screen.findByText('Flux de Trésorerie')).toBeInTheDocument();
  });

  it('affiche les données de trésorerie', async () => {
    renderComponent();
    
    // Attendre que les données soient chargées
    await screen.findByText('Flux de Trésorerie');

    // Vérifier les légendes
    expect(screen.getByText('Recettes')).toBeInTheDocument();
    expect(screen.getByText('Dépenses')).toBeInTheDocument();
  });

  it('gère le cas où les données sont nulles', async () => {
    mockGetDonneesTresorerie.mockResolvedValue(null as any);
    renderComponent();

    // Le composant devrait toujours s'afficher sans erreur
    expect(await screen.findByText('Flux de Trésorerie')).toBeInTheDocument();
  });

  it('appelle getDonneesTresorerie au chargement', async () => {
    renderComponent();
    await screen.findByText('Flux de Trésorerie');
    expect(mockGetDonneesTresorerie).toHaveBeenCalled();
  });
});
