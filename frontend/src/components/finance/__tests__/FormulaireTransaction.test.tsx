import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { BrowserRouter } from 'react-router-dom';
import { LocalizationProvider } from '@mui/x-date-pickers';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { fr } from 'date-fns/locale';
import FormulaireTransaction from '../FormulaireTransaction';
import { creerTransaction, modifierTransaction, getTransaction, getComptes } from '../../../services/finance';
import type { Transaction, Compte } from '../../../types/finance';

// Mock des services
jest.mock('../../../services/finance', () => ({
  creerTransaction: jest.fn(),
  modifierTransaction: jest.fn(),
  getTransaction: jest.fn(),
  getComptes: jest.fn()
}));

const mockNavigate = jest.fn();
jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  useNavigate: () => mockNavigate,
  useParams: () => ({})
}));

describe('FormulaireTransaction', () => {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: {
        retry: false
      }
    }
  });

  const mockComptes: Compte[] = [
    { id: '1', numero: 'CPTE-001', libelle: 'Compte Principal', type_compte: 'BANQUE', devise: 'XAF', solde: 1000000, actif: true },
    { id: '2', numero: 'CPTE-002', libelle: 'Caisse', type_compte: 'CAISSE', devise: 'XAF', solde: 500000, actif: true }
  ];

  beforeEach(() => {
    (getComptes as jest.Mock).mockResolvedValue(mockComptes);
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  const renderComponent = () => {
    render(
      <BrowserRouter>
        <QueryClientProvider client={queryClient}>
          <LocalizationProvider dateAdapter={AdapterDateFns} adapterLocale={fr}>
            <FormulaireTransaction />
          </LocalizationProvider>
        </QueryClientProvider>
      </BrowserRouter>
    );
  };

  it('affiche le formulaire avec les champs requis', async () => {
    renderComponent();

    expect(screen.getByText('Nouvelle Transaction')).toBeInTheDocument();
    expect(screen.getByLabelText(/Référence/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Date de Transaction/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Type de Transaction/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Catégorie/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Montant/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Description/i)).toBeInTheDocument();
  });

  it('affiche les messages de validation pour les champs requis', async () => {
    renderComponent();

    const submitButton = screen.getByRole('button', { name: /Créer/i });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText('La référence est requise')).toBeInTheDocument();
      expect(screen.getByText('Le type est requis')).toBeInTheDocument();
      expect(screen.getByText('La catégorie est requise')).toBeInTheDocument();
    });
  });

  it('affiche les comptes source/destination selon le type de transaction', async () => {
    renderComponent();

    const typeSelect = screen.getByLabelText(/Type de Transaction/i);
    
    // Test pour une entrée
    fireEvent.mouseDown(typeSelect);
    fireEvent.click(screen.getByText('RECETTE'));
    
    await waitFor(() => {
      expect(screen.getByLabelText(/Compte Destination/i)).toBeInTheDocument();
      expect(screen.queryByLabelText(/Compte Source/i)).not.toBeInTheDocument();
    });

    // Test pour une sortie
    fireEvent.mouseDown(typeSelect);
    fireEvent.click(screen.getByText('DEPENSE'));

    await waitFor(() => {
      expect(screen.queryByLabelText(/Compte Destination/i)).not.toBeInTheDocument();
      expect(screen.getByLabelText(/Compte Source/i)).toBeInTheDocument();
    });
  });

  it('soumet le formulaire avec les données correctes', async () => {
    const mockTransaction: Transaction = {
      id: '1',
      reference: 'TEST-001',
      date_transaction: '2024-01-20T10:00:00Z',
      type_transaction: 'RECETTE',
      categorie: 'VENTE',
      montant: 150000,
      devise: 'XAF',
      description: 'Test transaction',
      compte_destination_id: '1',
      statut: 'EN_ATTENTE'
    };

    (creerTransaction as jest.Mock).mockResolvedValueOnce(mockTransaction);

    renderComponent();

    // Remplir le formulaire
    fireEvent.change(screen.getByLabelText(/Référence/i), {
      target: { value: 'TEST-001' }
    });

    fireEvent.mouseDown(screen.getByLabelText(/Type de Transaction/i));
    fireEvent.click(screen.getByText('RECETTE'));

    fireEvent.mouseDown(screen.getByLabelText(/Catégorie/i));
    fireEvent.click(screen.getByText('VENTE'));

    fireEvent.change(screen.getByLabelText(/Montant/i), {
      target: { value: '150000' }
    });

    fireEvent.change(screen.getByLabelText(/Description/i), {
      target: { value: 'Test transaction' }
    });

    // Sélectionner le compte destination
    await waitFor(() => {
      fireEvent.mouseDown(screen.getByLabelText(/Compte Destination/i));
    });
    fireEvent.click(screen.getByText('Compte Principal'));

    // Soumettre le formulaire
    fireEvent.click(screen.getByRole('button', { name: /Créer/i }));

    await waitFor(() => {
      expect(creerTransaction).toHaveBeenCalledWith({
        reference: 'TEST-001',
        type_transaction: 'RECETTE',
        categorie: 'VENTE',
        montant: 150000,
        description: 'Test transaction',
        compte_destination_id: '1'
      });
      expect(mockNavigate).toHaveBeenCalledWith('/finance');
    });
  });

  it('gère les erreurs de soumission', async () => {
    const errorMessage = 'Erreur lors de la création de la transaction';
    (creerTransaction as jest.Mock).mockRejectedValueOnce(new Error(errorMessage));

    renderComponent();

    // Remplir et soumettre le formulaire
    fireEvent.change(screen.getByLabelText(/Référence/i), {
      target: { value: 'TEST-001' }
    });

    fireEvent.mouseDown(screen.getByLabelText(/Type de Transaction/i));
    fireEvent.click(screen.getByText('RECETTE'));

    fireEvent.mouseDown(screen.getByLabelText(/Catégorie/i));
    fireEvent.click(screen.getByText('VENTE'));

    fireEvent.change(screen.getByLabelText(/Montant/i), {
      target: { value: '150000' }
    });

    fireEvent.click(screen.getByRole('button', { name: /Créer/i }));

    await waitFor(() => {
      expect(screen.getByText(errorMessage)).toBeInTheDocument();
    });
  });
});
