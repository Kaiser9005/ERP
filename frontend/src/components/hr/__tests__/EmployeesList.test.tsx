import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from 'react-query';
import { MemoryRouter } from 'react-router-dom';
import EmployeesList from '../EmployeesList';
import { getEmployees } from '../../../services/hr';

jest.mock('../../../services/hr');

const mockEmployees = [
  {
    id: '1',
    matricule: 'EMP001',
    nom: 'Dupont',
    prenom: 'Jean',
    email: 'jean.dupont@fofal.cm',
    departement: 'PRODUCTION',
    poste: 'Chef d\'équipe',
    statut: 'ACTIF'
  },
  {
    id: '2',
    matricule: 'EMP002',
    nom: 'Martin',
    prenom: 'Marie',
    email: 'marie.martin@fofal.cm',
    departement: 'ADMINISTRATION',
    poste: 'Comptable',
    statut: 'CONGE'
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

describe('EmployeesList', () => {
  beforeEach(() => {
    (getEmployees as jest.Mock).mockResolvedValue(mockEmployees);
  });

  it('affiche la liste des employés', async () => {
    renderWithProviders(<EmployeesList />);
    
    expect(await screen.findByText('Jean Dupont')).toBeInTheDocument();
    expect(await screen.findByText('Marie Martin')).toBeInTheDocument();
  });

  it('permet la recherche d\'employés', async () => {
    renderWithProviders(<EmployeesList />);
    
    const searchInput = screen.getByPlaceholderText('Rechercher...');
    fireEvent.change(searchInput, { target: { value: 'Jean' } });
    
    expect(screen.getByText('Jean Dupont')).toBeInTheDocument();
    expect(screen.queryByText('Marie Martin')).not.toBeInTheDocument();
  });

  it('affiche les statuts avec les bonnes couleurs', async () => {
    renderWithProviders(<EmployeesList />);
    
    const actifChip = await screen.findByText('ACTIF');
    const congeChip = await screen.findByText('CONGE');
    
    expect(actifChip).toHaveClass('MuiChip-colorSuccess');
    expect(congeChip).toHaveClass('MuiChip-colorWarning');
  });

  it('affiche les boutons d\'action', async () => {
    renderWithProviders(<EmployeesList />);
    
    const viewButtons = await screen.findAllByTestId('view-button');
    const editButtons = await screen.findAllByTestId('edit-button');
    
    expect(viewButtons).toHaveLength(2);
    expect(editButtons).toHaveLength(2);
  });

  it('gère les erreurs de chargement', async () => {
    (getEmployees as jest.Mock).mockRejectedValue(new Error('Erreur de chargement'));
    
    renderWithProviders(<EmployeesList />);
    
    expect(await screen.findByText('Une erreur est survenue')).toBeInTheDocument();
  });
});