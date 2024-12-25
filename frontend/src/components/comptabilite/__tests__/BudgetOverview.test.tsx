import React from 'react';
import { render, screen } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from 'react-query';
import BudgetOverview from '../../comptabilite/BudgetOverview';
import { getBudgetAnalysis } from '../../../services/comptabilite';

jest.mock('../../../services/finance');

const mockBudgetAnalysis = {
  total_prevu: 1500000,
  total_realise: 1200000,
  categories: [
    {
      code: 'PROD',
      libelle: 'Production',
      prevu: 1000000,
      realise: 750000,
      ecart_percentage: -25
    },
    {
      code: 'MKT',
      libelle: 'Marketing',
      prevu: 500000,
      realise: 450000,
      ecart_percentage: -10
    }
  ],
  weather_impact: {
    score: 15,
    factors: ['Précipitations élevées', 'Température']
  },
  recommendations: [
    'Ajuster le budget production',
    'Surveiller les dépenses marketing'
  ]
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
      {component}
    </QueryClientProvider>
  );
};

describe('BudgetOverview', () => {
  beforeEach(() => {
    (getBudgetAnalysis as jest.Mock).mockResolvedValue(mockBudgetAnalysis);
  });

  it('affiche le titre et le score météo', async () => {
    renderWithProviders(<BudgetOverview />);
    
    expect(await screen.findByText('Aperçu Budgétaire')).toBeInTheDocument();
    expect(await screen.findByText('Impact météo: 15%')).toBeInTheDocument();
  });

  it('affiche les catégories budgétaires', async () => {
    renderWithProviders(<BudgetOverview />);
    
    expect(await screen.findByText('Production')).toBeInTheDocument();
    expect(await screen.findByText('Marketing')).toBeInTheDocument();
  });

  it('affiche les montants formatés', async () => {
    renderWithProviders(<BudgetOverview />);
    
    expect(await screen.findByText('750 000 FCFA / 1 000 000 FCFA')).toBeInTheDocument();
    expect(await screen.findByText('450 000 FCFA / 500 000 FCFA')).toBeInTheDocument();
  });

  it('affiche les facteurs météorologiques', async () => {
    renderWithProviders(<BudgetOverview />);
    
    expect(await screen.findByText('Précipitations élevées')).toBeInTheDocument();
    expect(await screen.findByText('Température')).toBeInTheDocument();
  });

  it('affiche les recommandations', async () => {
    renderWithProviders(<BudgetOverview />);
    
    expect(await screen.findByText('• Ajuster le budget production')).toBeInTheDocument();
    expect(await screen.findByText('• Surveiller les dépenses marketing')).toBeInTheDocument();
  });

  it('gère les erreurs de chargement', async () => {
    (getBudgetAnalysis as jest.Mock).mockRejectedValue(new Error('Erreur de chargement'));
    
    renderWithProviders(<BudgetOverview />);
    
    expect(await screen.findByText('Aucune donnée budgétaire disponible')).toBeInTheDocument();
  });
});