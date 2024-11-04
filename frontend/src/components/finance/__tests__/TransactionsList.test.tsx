import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from 'react-query';
import TransactionsList from '../TransactionsList';
import { getTransactions } from '../../../services/finance';

jest.mock('../../../services/finance');

const mockTransactions = [
  {
    id: '1',
    date: '2024-01-20T10:00:00Z',
    reference: 'TR001',
    description: 'Vente de produits',
    amount: 500000,
    type: 'RECETTE',
    status: 'VALIDEE'
  },
  {
    id: '2',
    date: '2024-01-20T11:00:00Z',
    reference: 'TR002',
    description: 'Achat fournitures',
    amount: 150000,
    type: 'DEPENSE',
    status: 'EN_ATTENTE'
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

describe('TransactionsList', () => {
  beforeEach(() => {
    (getTransactions as jest.Mock).mockResolvedValue(mockTransactions);
  });

  it('affiche la liste des transactions', async () => {
    renderWithProviders(<TransactionsList />);
    
    expect(await screen.findByText('TR001')).toBeInTheDocument();
    expect(await screen.findByText('Vente de produits')).toBeInTheDocument();
  });

  it('permet la recherche de transactions', async () => {
    renderWithProviders(<TransactionsList />);
    
    const searchInput = screen.getByPlaceholderText('Rechercher...');
    fireEvent.change(searchInput, { target: { value: 'Vente' } });
    
    expect(screen.getByText('Vente de produits')).toBeInTheDocument();
    expect(screen.queryByText('Achat fournitures')).not.toBeInTheDocument();
  });

  it('affiche les montants formatés', async () => {
    renderWithProviders(<TransactionsList />);
    
    expect(await screen.findByText('500 000 FCFA')).toBeInTheDocument();
    expect(await screen.findByText('150 000 FCFA')).toBeInTheDocument();
  });

  it('affiche les statuts avec les bonnes couleurs', async () => {
    renderWithProviders(<TransactionsList />);
    
    const recetteChip = await screen.findByText('RECETTE');
    const depenseChip = await screen.findByText('DEPENSE');
    
    expect(recetteChip).toHaveClass('MuiChip-colorSuccess');
    expect(depenseChip).toHaveClass('MuiChip-colorError');
  });
});