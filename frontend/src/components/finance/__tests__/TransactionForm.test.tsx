import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from 'react-query';
import { MemoryRouter, Routes, Route } from 'react-router-dom';
import TransactionForm from '../TransactionForm';
import { createTransaction, updateTransaction, getTransaction, getComptes } from '../../../services/finance';

jest.mock('../../../services/finance');

const mockComptes = [
  {
    id: '1',
    libelle: 'Compte Principal',
    type_compte: 'BANQUE',
    numero: 'CPT001'
  },
  {
    id: '2',
    libelle: 'Caisse',
    type_compte: 'CAISSE',
    numero: 'CSE001'
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
      <MemoryRouter>
        <Routes>
          <Route path="/" element={component} />
          <Route path="/finance" element={<div>Finance Page</div>} />
        </Routes>
      </MemoryRouter>
    </QueryClientProvider>
  );
};

describe('TransactionForm', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    (getComptes as jest.Mock).mockResolvedValue(mockComptes);
  });

  it('affiche le formulaire de création', () => {
    renderWithProviders(<TransactionForm />);
    
    expect(screen.getByText('Nouvelle Transaction')).toBeInTheDocument();
    expect(screen.getByLabelText('Référence')).toBeInTheDocument();
    expect(screen.getByLabelText('Type de Transaction')).toBeInTheDocument();
    expect(screen.getByLabelText('Montant')).toBeInTheDocument();
  });

  it('valide les champs requis', async () => {
    renderWithProviders(<TransactionForm />);
    
    fireEvent.click(screen.getByText('Créer'));
    
    expect(await screen.findByText('La référence est requise')).toBeInTheDocument();
    expect(await screen.findByText('Le type est requis')).toBeInTheDocument();
    expect(await screen.findByText('La catégorie est requise')).toBeInTheDocument();
    expect(await screen.findByText('Le montant est requis')).toBeInTheDocument();
  });

  it('affiche les champs appropriés selon le type de transaction', async () => {
    renderWithProviders(<TransactionForm />);
    
    const typeSelect = screen.getByLabelText('Type de Transaction');
    
    // Test pour une recette
    fireEvent.change(typeSelect, { target: { value: 'RECETTE' } });
    expect(await screen.findByLabelText('Compte Destination')).toBeInTheDocument();
    expect(screen.queryByLabelText('Compte Source')).not.toBeInTheDocument();

    // Test pour une dépense
    fireEvent.change(typeSelect, { target: { value: 'DEPENSE' } });
    expect(await screen.findByLabelText('Compte Source')).toBeInTheDocument();
    expect(screen.queryByLabelText('Compte Destination')).not.toBeInTheDocument();

    // Test pour un virement
    fireEvent.change(typeSelect, { target: { value: 'VIREMENT' } });
    expect(screen.getByLabelText('Compte Source')).toBeInTheDocument();
    expect(screen.getByLabelText('Compte Destination')).toBeInTheDocument();
  });

  it('soumet le formulaire avec des données valides', async () => {
    (createTransaction as jest.Mock).mockResolvedValue({ id: '1' });
    
    renderWithProviders(<TransactionForm />);
    
    fireEvent.change(screen.getByLabelText('Référence'), { target: { value: 'TR001' } });
    fireEvent.change(screen.getByLabelText('Type de Transaction'), { target: { value: 'RECETTE' } });
    fireEvent.change(screen.getByLabelText('Catégorie'), { target: { value: 'VENTE' } });
    fireEvent.change(screen.getByLabelText('Montant'), { target: { value: '1500' } });
    
    fireEvent.click(screen.getByText('Créer'));
    
    await waitFor(() => {
      expect(createTransaction).toHaveBeenCalledWith({
        reference: 'TR001',
        type_transaction: 'RECETTE',
        categorie: 'VENTE',
        montant: '1500',
        date_transaction: expect.any(Date)
      });
    });
  });

  it('gère les erreurs de soumission', async () => {
    (createTransaction as jest.Mock).mockRejectedValue(new Error('Erreur de création'));
    
    renderWithProviders(<TransactionForm />);
    
    fireEvent.change(screen.getByLabelText('Référence'), { target: { value: 'TR001' } });
    fireEvent.click(screen.getByText('Créer'));
    
    expect(await screen.findByText('Une erreur est survenue')).toBeInTheDocument();
  });
});