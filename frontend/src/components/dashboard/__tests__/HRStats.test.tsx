import React from 'react';
import { render, screen } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from 'react-query';
import HRStats from '../HRStats';
import { getEmployeeStats } from '../../../services/hr';

jest.mock('../../../services/hr');

const mockStats = {
  effectif_total: 42,
  en_conge: 5,
  presents: 35
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

describe('HRStats', () => {
  beforeEach(() => {
    (getEmployeeStats as jest.Mock).mockResolvedValue(mockStats);
  });

  it('affiche les statistiques RH', async () => {
    renderWithProviders(<HRStats />);
    
    expect(await screen.findByText('Ressources Humaines')).toBeInTheDocument();
    expect(await screen.findByText('42')).toBeInTheDocument();
  });

  it('affiche les indicateurs de présence', async () => {
    renderWithProviders(<HRStats />);
    
    expect(await screen.findByText('5 En congé')).toBeInTheDocument();
    expect(await screen.findByText('35 Présents')).toBeInTheDocument();
  });

  it('utilise les bonnes couleurs pour les indicateurs', async () => {
    renderWithProviders(<HRStats />);
    
    const congeChip = await screen.findByText('5 En congé');
    const presentsChip = await screen.findByText('35 Présents');
    
    expect(congeChip).toHaveClass('MuiChip-colorWarning');
    expect(presentsChip).toHaveClass('MuiChip-colorSuccess');
  });

  it('gère les erreurs de chargement', async () => {
    (getEmployeeStats as jest.Mock).mockRejectedValue(new Error('Erreur de chargement'));
    
    renderWithProviders(<HRStats />);
    
    expect(await screen.findByText('0')).toBeInTheDocument();
    expect(await screen.findByText('0 En congé')).toBeInTheDocument();
  });
});