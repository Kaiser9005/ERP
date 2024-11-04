import React from 'react';
import { render, screen } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from 'react-query';
import BudgetOverview from '../BudgetOverview';
import { getBudgetOverview } from '../../../services/finance';

jest.mock('../../../services/finance');

const mockBudgets = [
  {
    category: 'Production',
    allocated: 1000000,
    spent: 750000
  },
  {
    category: 'Marketing',
    allocated: 500000,
    spent: 450000
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

describe('BudgetOverview', () => {
  beforeEach(() => {
    (getBudgetOverview as jest.Mock).mockResolvedValue(mockBudgets);
  });

  it('affiche le titre', async () => {
    renderWithProviders(<BudgetOverview />);
    
    expect(screen.getByText('Suivi Budgétaire')).toBeInTheDocument();
  });

  it('affiche les catégories de budget', async () => {
    renderWithProviders(<BudgetOverview />);
    
    expect(await screen.findByText('Production')).toBeInTheDocument();
    expect(await screen.findByText('Marketing')).toBeInTheDocument();
  });

  it('affiche les montants formatés', async () => {
    renderWithProviders(<BudgetOverview />);
    
    expect(await screen.findByText('750 000 FCFA')).toBeInTheDocument();
    expect(await screen.findByText('1 000 000 FCFA')).toBeInTheDocument();
  });

  it('affiche les pourcentages d\'utilisation', async () => {
    renderWithProviders(<BudgetOverview />);
    
    expect(await screen.findByText('75.0% utilisé')).toBeInTheDocument();
    expect(await screen.findByText('90.0% utilisé')).toBeInTheDocument();
  });

  it('utilise les bonnes couleurs selon le pourcentage', async () => {
    renderWithProviders(<BudgetOverview />);
    
    const progressBars = await screen.findAllByRole('progressbar');
    expect(progressBars[0]).toHaveClass('MuiLinearProgress-colorWarning');
    expect(progressBars[1]).toHaveClass('MuiLinearProgress-colorError');
  });

  it('gère les erreurs de chargement', async () => {
    (getBudgetOverview as jest.Mock).mockRejectedValue(new Error('Erreur de chargement'));
    
    renderWithProviders(<BudgetOverview />);
    
    expect(await screen.findByText('Erreur de chargement du budget')).toBeInTheDocument();
  });
});