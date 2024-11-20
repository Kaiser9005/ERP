import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import { QueryClient, QueryClientProvider } from 'react-query';
import { BrowserRouter } from 'react-router-dom';
import ListeTransactions from '../ListeTransactions';
import { getTransactions, Transaction, TypeTransaction, StatutTransaction } from '../../../services/finance';

// Mock du service finance
jest.mock('../../../services/finance', () => ({
  getTransactions: jest.fn(),
  TypeTransaction: {
    RECETTE: 'RECETTE',
    DEPENSE: 'DEPENSE'
  },
  StatutTransaction: {
    EN_ATTENTE: 'EN_ATTENTE',
    VALIDEE: 'VALIDEE',
    ANNULEE: 'ANNULEE'
  }
}));

const mockGetTransactions = getTransactions as jest.MockedFunction<typeof getTransactions>;

describe('ListeTransactions', () => {
  const queryClient = new QueryClient();
  const mockTransactions: Transaction[] = [
    {
      id: '1',
      date: '2024-01-15T10:00:00Z',
      montant: 150000,
      type_transaction: 'RECETTE' as TypeTransaction,
      statut: 'VALIDEE' as StatutTransaction,
      description: 'Vente de produits agricoles',
      reference: 'VNT-001'
    },
    {
      id: '2',
      date: '2024-01-15T11:00:00Z',
      montant: 50000,
      type_transaction: 'DEPENSE' as TypeTransaction,
      statut: 'EN_ATTENTE' as StatutTransaction,
      description: 'Achat de matériel',
      reference: 'ACH-001'
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

  it('affiche la liste des transactions', async () => {
    renderComponent();

    // Vérifie le titre
    expect(screen.getByText('Transactions')).toBeInTheDocument();

    // Vérifie les transactions
    expect(await screen.findByText('Vente de produits agricoles')).toBeInTheDocument();
    expect(screen.getByText('Achat de matériel')).toBeInTheDocument();

    // Vérifie les montants formatés
    expect(screen.getByText('150 000 XAF')).toBeInTheDocument();
    expect(screen.getByText('50 000 XAF')).toBeInTheDocument();

    // Vérifie les types et statuts
    expect(screen.getByText('RECETTE')).toBeInTheDocument();
    expect(screen.getByText('DEPENSE')).toBeInTheDocument();
    expect(screen.getByText('VALIDEE')).toBeInTheDocument();
    expect(screen.getByText('EN_ATTENTE')).toBeInTheDocument();
  });

  it('filtre les transactions par recherche', async () => {
    renderComponent();

    // Attend que les transactions soient chargées
    await screen.findByText('Vente de produits agricoles');

    // Effectue une recherche
    const searchInput = screen.getByPlaceholderText('Rechercher...');
    fireEvent.change(searchInput, { target: { value: 'vente' } });

    // Vérifie que seule la transaction correspondante est affichée
    expect(screen.getByText('Vente de produits agricoles')).toBeInTheDocument();
    expect(screen.queryByText('Achat de matériel')).not.toBeInTheDocument();
  });

  it('filtre les transactions par référence', async () => {
    renderComponent();

    // Attend que les transactions soient chargées
    await screen.findByText('Vente de produits agricoles');

    // Effectue une recherche par référence
    const searchInput = screen.getByPlaceholderText('Rechercher...');
    fireEvent.change(searchInput, { target: { value: 'ACH' } });

    // Vérifie que seule la transaction correspondante est affichée
    expect(screen.queryByText('Vente de produits agricoles')).not.toBeInTheDocument();
    expect(screen.getByText('Achat de matériel')).toBeInTheDocument();
  });
});
