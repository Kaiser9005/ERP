import React from 'react';
import { render, screen } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from 'react-query';
import { MemoryRouter } from 'react-router-dom';
import TransactionDetails from '../TransactionDetails';
import { getTransaction } from '../../../services/finance';

jest.mock('../../../services/finance');

const mockTransaction = {
  id: '1',
  reference: 'TR001',
  date_transaction: '2024-01-20T10:00:00Z',
  type_transaction: 'RECETTE',
  categorie: 'VENTE',
  montant: 150000,
  description: 'Vente de produits',
  statut: 'VALIDEE',
  compte_destination: {
    id: '1',
    libelle: 'Compte Principal'
  },
  validee_par: {
    nom: 'Doe',
    prenom: 'John'
  },
  date_validation: '2024-01-20T11:00:00Z'
};

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
      <MemoryRouter>
        {component}
      </MemoryRouter>
    </QueryClientProvider>
  );
};

describe('TransactionDetails', () => {
  beforeEach(() => {
    (getTransaction as jest.Mock).mockResolvedValue(mockTransaction);
  });

  it('affiche les détails de la transaction', async () => {
    renderWithProviders(<TransactionDetails />);
    
    expect(await screen.findByText('TR001')).toBeInTheDocument();
    expect(await screen.findByText('150 000 FCFA')).toBeInTheDocument();
    expect(await screen.findByText('RECETTE')).toBeInTheDocument();
    expect(await screen.findByText('VALIDEE')).toBeInTheDocument();
  });

  it('affiche les informations du compte', async () => {
    renderWithProviders(<TransactionDetails />);
    
    expect(await screen.findByText('Compte Principal')).toBeInTheDocument();
  });

  it('affiche les informations de validation', async () => {
    renderWithProviders(<TransactionDetails />);
    
    expect(await screen.findByText('John Doe')).toBeInTheDocument();
  });

  it('gère les erreurs de chargement', async () => {
    (getTransaction as jest.Mock).mockRejectedValue(new Error('Erreur de chargement'));
    
    renderWithProviders(<TransactionDetails />);
    
    expect(await screen.findByText('Une erreur est survenue')).toBeInTheDocument();
  });
});