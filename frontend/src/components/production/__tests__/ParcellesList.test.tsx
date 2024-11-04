import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from 'react-query';
import { MemoryRouter } from 'react-router-dom';
import ParcellesList from '../ParcellesList';
import { getParcelles } from '../../../services/production';

jest.mock('../../../services/production');

const mockParcelles = [
  {
    id: '1',
    code: 'P001',
    culture_type: 'PALMIER',
    surface_hectares: 10,
    statut: 'ACTIVE',
    date_plantation: '2024-01-01'
  },
  {
    id: '2',
    code: 'P002',
    culture_type: 'PAPAYE',
    surface_hectares: 5,
    statut: 'EN_PREPARATION',
    date_plantation: '2024-01-15'
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
        {component}
      </MemoryRouter>
    </QueryClientProvider>
  );
};

describe('ParcellesList', () => {
  beforeEach(() => {
    (getParcelles as jest.Mock).mockResolvedValue(mockParcelles);
  });

  it('affiche la liste des parcelles', async () => {
    renderWithProviders(<ParcellesList />);
    
    expect(await screen.findByText('P001')).toBeInTheDocument();
    expect(await screen.findByText('P002')).toBeInTheDocument();
  });

  it('affiche les détails de chaque parcelle', async () => {
    renderWithProviders(<ParcellesList />);
    
    expect(await screen.findByText('PALMIER')).toBeInTheDocument();
    expect(await screen.findByText('10 ha')).toBeInTheDocument();
    expect(await screen.findByText('ACTIVE')).toBeInTheDocument();
  });

  it('affiche les boutons d\'action pour chaque parcelle', async () => {
    renderWithProviders(<ParcellesList />);
    
    const viewButtons = await screen.findAllByTestId('view-button');
    const editButtons = await screen.findAllByTestId('edit-button');
    
    expect(viewButtons).toHaveLength(2);
    expect(editButtons).toHaveLength(2);
  });

  it('gère les erreurs de chargement', async () => {
    (getParcelles as jest.Mock).mockRejectedValue(new Error('Erreur de chargement'));
    
    renderWithProviders(<ParcellesList />);
    
    expect(await screen.findByText('Erreur de chargement des parcelles')).toBeInTheDocument();
  });
});