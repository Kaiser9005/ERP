import React from 'react';
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
    labels: ['Jan', 'Fév', 'Mar'],
    recettes: [1500000, 1800000, 1600000],
    depenses: [1200000, 1300000, 1400000]
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

  it('affiche les légendes du graphique', async () => {
    renderComponent();
    // Attendre que les données soient chargées
    await screen.findByText('Flux de Trésorerie');

    // Vérifier les légendes
    expect(screen.getByText('Recettes')).toBeInTheDocument();
    expect(screen.getByText('Dépenses')).toBeInTheDocument();
  });

  it('gère le cas où les données sont nulles', () => {
    mockGetDonneesTresorerie.mockResolvedValue(null as any);
    renderComponent();

    // Le composant devrait toujours s'afficher sans erreur
    expect(screen.getByText('Flux de Trésorerie')).toBeInTheDocument();
  });

  it('appelle getDonneesTresorerie au chargement', () => {
    renderComponent();
    expect(mockGetDonneesTresorerie).toHaveBeenCalled();
  });
});
