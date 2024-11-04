import React from 'react';
import { render, screen } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from 'react-query';
import MovementHistory from '../MovementHistory';
import { getRecentMovements } from '../../../services/inventory';

jest.mock('../../../services/inventory');

const mockMovements = [
  {
    id: '1',
    type: 'ENTREE',
    product: 'Engrais NPK',
    quantity: 100,
    unit: 'kg',
    reference: 'BL-2024-001',
    date: '2024-01-20T10:00:00Z'
  },
  {
    id: '2',
    type: 'SORTIE',
    product: 'Pesticide',
    quantity: 20,
    unit: 'L',
    reference: 'BS-2024-001',
    date: '2024-01-20T11:00:00Z'
  }
];

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: false,
    },
  },
});

const renderWithProviders = (component: React.ReactElement) => {
  return render(
    <QueryClientProvider client={queryClient}>
      {component}
    </QueryClientProvider>
  );
};

describe('MovementHistory', () => {
  beforeEach(() => {
    (getRecentMovements as jest.Mock).mockResolvedValue(mockMovements);
  });

  it('affiche l\'historique des mouvements', async () => {
    renderWithProviders(<MovementHistory />);
    
    expect(await screen.findByText('Derniers Mouvements')).toBeInTheDocument();
    expect(await screen.findByText('Engrais NPK')).toBeInTheDocument();
    expect(await screen.findByText('Pesticide')).toBeInTheDocument();
  });

  it('affiche les types de mouvements avec les bonnes couleurs', async () => {
    renderWithProviders(<MovementHistory />);
    
    const entreeChip = await screen.findByText('ENTREE');
    const sortieChip = await screen.findByText('SORTIE');
    
    expect(entreeChip).toHaveClass('MuiChip-colorSuccess');
    expect(sortieChip).toHaveClass('MuiChip-colorError');
  });

  it('affiche les quantités et références', async () => {
    renderWithProviders(<MovementHistory />);
    
    expect(await screen.findByText(/100 kg/)).toBeInTheDocument();
    expect(await screen.findByText(/BL-2024-001/)).toBeInTheDocument();
  });

  it('affiche les dates relatives', async () => {
    renderWithProviders(<MovementHistory />);
    
    expect(await screen.findByText(/il y a/)).toBeInTheDocument();
  });

  it('gère les erreurs de chargement', async () => {
    (getRecentMovements as jest.Mock).mockRejectedValue(new Error('Erreur de chargement'));
    
    renderWithProviders(<MovementHistory />);
    
    expect(await screen.findByText('Erreur de chargement des mouvements')).toBeInTheDocument();
  });
});