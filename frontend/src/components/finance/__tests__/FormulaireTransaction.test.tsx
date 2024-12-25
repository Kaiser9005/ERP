import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from 'react-query';
import FormulaireTransaction from '../FormulaireTransaction';
import { createTransaction } from '../../../services/finance';
import { Transaction } from '../../../types/finance';

// Mock du service finance
jest.mock('../../../services/finance');

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

describe('FormulaireTransaction', () => {
  beforeEach(() => {
    (createTransaction as jest.Mock).mockClear();
  });

  it('renders transaction form', () => {
    renderWithProviders(<FormulaireTransaction />);
    
    expect(screen.getByText('Nouvelle Transaction')).toBeInTheDocument();
    expect(screen.getByLabelText('Montant')).toBeInTheDocument();
    expect(screen.getByLabelText('Type de Transaction')).toBeInTheDocument();
    expect(screen.getByLabelText('Description')).toBeInTheDocument();
  });

  it('submits transaction successfully', async () => {
    const mockTransaction: Transaction = {
      id: '1',
      date: '2023-11-30',
      montant: 1000,
      type: 'revenu',
      description: 'Test transaction',
      reference: 'REF001'
    };

    (createTransaction as jest.Mock).mockResolvedValue(mockTransaction);

    renderWithProviders(<FormulaireTransaction />);
    
    // Remplir le formulaire
    fireEvent.change(screen.getByLabelText('Montant'), { target: { value: '1000' } });
    fireEvent.change(screen.getByLabelText('Type de Transaction'), { target: { value: 'revenu' } });
    fireEvent.change(screen.getByLabelText('Description'), { target: { value: 'Test transaction' } });
    
    fireEvent.click(screen.getByText('Enregistrer'));

    await waitFor(() => {
      expect(createTransaction).toHaveBeenCalledWith({
        montant: 1000,
        type: 'revenu',
        description: 'Test transaction'
      });
    });
  });

  it('handles form validation', async () => {
    renderWithProviders(<FormulaireTransaction />);
    
    fireEvent.click(screen.getByText('Enregistrer'));

    await waitFor(() => {
      expect(screen.getByText('Le montant est requis')).toBeInTheDocument();
      expect(screen.getByText('Le type de transaction est requis')).toBeInTheDocument();
    });
  });
});
