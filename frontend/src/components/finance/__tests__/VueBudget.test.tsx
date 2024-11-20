import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import { QueryClient, QueryClientProvider } from 'react-query';
import VueBudget from '../VueBudget';
import { getVueBudget } from '../../../services/finance';

// Mock du service finance
jest.mock('../../../services/finance', () => ({
  getVueBudget: jest.fn()
}));

const mockGetVueBudget = getVueBudget as jest.MockedFunction<typeof getVueBudget>;

describe('VueBudget', () => {
  const queryClient = new QueryClient();

  const mockBudgets = [
    {
      categorie: 'Équipement',
      depense: 750000,
      alloue: 1000000
    },
    {
      categorie: 'Personnel',
      depense: 1800000,
      alloue: 2000000
    },
    {
      categorie: 'Maintenance',
      depense: 450000,
      alloue: 500000
    }
  ];

  beforeEach(() => {
    mockGetVueBudget.mockResolvedValue(mockBudgets);
  });

  const renderComponent = () => {
    render(
      <QueryClientProvider client={queryClient}>
        <VueBudget />
      </QueryClientProvider>
    );
  };

  it('affiche le titre du composant', async () => {
    renderComponent();
    expect(await screen.findByText('Suivi Budgétaire')).toBeInTheDocument();
  });

  it('affiche les catégories de budget', async () => {
    renderComponent();
    
    // Attendre que les données soient chargées
    await screen.findByText('Suivi Budgétaire');

    // Vérifier les catégories
    expect(screen.getByText('Équipement')).toBeInTheDocument();
    expect(screen.getByText('Personnel')).toBeInTheDocument();
    expect(screen.getByText('Maintenance')).toBeInTheDocument();
  });

  it('affiche les montants formatés', async () => {
    renderComponent();
    
    await screen.findByText('Suivi Budgétaire');

    // Vérifier les montants
    expect(screen.getByText('750 000 XAF')).toBeInTheDocument();
    expect(screen.getByText('1 000 000 XAF')).toBeInTheDocument();
    expect(screen.getByText('1 800 000 XAF')).toBeInTheDocument();
    expect(screen.getByText('2 000 000 XAF')).toBeInTheDocument();
  });

  it('affiche les pourcentages d\'utilisation', async () => {
    renderComponent();
    
    await screen.findByText('Suivi Budgétaire');

    // Vérifier les pourcentages (75%, 90%, 90%)
    expect(screen.getByText('75.0% utilisé')).toBeInTheDocument();
    expect(screen.getByText('90.0% utilisé')).toBeInTheDocument();
    expect(screen.getByText('90.0% utilisé')).toBeInTheDocument();
  });

  it('gère le cas où les données sont nulles', () => {
    mockGetVueBudget.mockResolvedValue(null as any);
    renderComponent();

    // Le composant devrait s'afficher sans erreur
    expect(screen.getByText('Suivi Budgétaire')).toBeInTheDocument();
  });
});
