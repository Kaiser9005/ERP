import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import { QueryClient, QueryClientProvider } from 'react-query';
import { BrowserRouter } from 'react-router-dom';
import ListeTransactions from '../ListeTransactions';
import { getTransactions, TypeTransaction, StatutTransaction } from '../../../services/finance';

// Mock du service finance
jest.mock('../../../services/finance', () => ({
  getTransactions: jest.fn()
}));

const mockGetTransactions = getTransactions as jest.MockedFunction<typeof getTransactions>;

describe('ListeTransactions', () => {
  const queryClient = new QueryClient();

  const mockTransactions = [
    {
      id: '1',
      date: '2024-01-15T10:00:00Z',
      reference: 'TR-001',
      description: 'Vente production',
      montant: 150000,
      type: 'ENTREE' as TypeTransaction,
      statut: 'VALIDEE' as StatutTransaction,
      categorie: 'Ventes'
    },
    {
      id: '2',
      date: '2024-01-16T14:30:00Z',
      reference: 'TR-002',
      description: 'Achat fournitures',
      montant: 50000,
      type: 'SORTIE' as TypeTransaction,
      statut: 'VALIDEE' as StatutTransaction,
      categorie: 'Fournitures'
    }
  ];

  beforeEach(() => {
    mockGetTransactions.mockResolvedValue(mockTransactions);
  });

  const renderComponent = () => {
    render(
      <BrowserRouter>
        <QueryClientProvider client={queryClient}>
          <ListeTransactions />
        </QueryClientProvider>
      </BrowserRouter>
    );
  };

  it('affiche le titre', () => {
    renderComponent();
    expect(screen.getByText('Transactions')).toBeInTheDocument();
  });

  it('affiche la liste des transactions', async () => {
    renderComponent();

    // Vérifier les en-têtes
    expect(await screen.findByText('Date')).toBeInTheDocument();
    expect(screen.getByText('Référence')).toBeInTheDocument();
    expect(screen.getByText('Description')).toBeInTheDocument();
    expect(screen.getByText('Montant')).toBeInTheDocument();
    expect(screen.getByText('Type')).toBeInTheDocument();

    // Vérifier les données
    expect(await screen.findByText('TR-001')).toBeInTheDocument();
    expect(screen.getByText('Vente production')).toBeInTheDocument();
    expect(screen.getByText('150 000 XAF')).toBeInTheDocument();
    expect(screen.getByText('Entrée')).toBeInTheDocument();

    expect(screen.getByText('TR-002')).toBeInTheDocument();
    expect(screen.getByText('Achat fournitures')).toBeInTheDocument();
    expect(screen.getByText('50 000 XAF')).toBeInTheDocument();
    expect(screen.getByText('Sortie')).toBeInTheDocument();
  });

  it('affiche un champ de recherche', () => {
    renderComponent();
    expect(screen.getByPlaceholderText('Rechercher...')).toBeInTheDocument();
  });

  it('gère le cas où il n\'y a pas de transactions', async () => {
    mockGetTransactions.mockResolvedValueOnce([]);
    renderComponent();

    // Vérifier que les en-têtes sont toujours affichés
    expect(await screen.findByText('Date')).toBeInTheDocument();
    expect(screen.getByText('Référence')).toBeInTheDocument();
    expect(screen.getByText('Description')).toBeInTheDocument();
    expect(screen.getByText('Montant')).toBeInTheDocument();
    expect(screen.getByText('Type')).toBeInTheDocument();

    // Vérifier qu'aucune donnée n'est affichée
    expect(screen.queryByText('TR-001')).not.toBeInTheDocument();
    expect(screen.queryByText('TR-002')).not.toBeInTheDocument();
  });
});
