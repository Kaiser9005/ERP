import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from 'react-query';
import { MemoryRouter, Routes, Route } from 'react-router-dom';
import EmployeeDetails from '../EmployeeDetails';
import { getEmployee, getEmployeeLeaves } from '../../../services/hr';

jest.mock('../../../services/hr');

const mockEmployee = {
  id: '1',
  matricule: 'EMP001',
  nom: 'Dupont',
  prenom: 'Jean',
  date_naissance: '1990-01-01',
  email: 'jean.dupont@fofal.cm',
  telephone: '123456789',
  adresse: '123 Rue Test',
  departement: 'PRODUCTION',
  poste: 'Chef d\'équipe',
  date_embauche: '2023-01-01',
  type_contrat: 'CDI',
  statut: 'ACTIF'
};

const mockLeaves = [
  {
    id: '1',
    type_conge: 'ANNUEL',
    date_debut: '2024-02-01',
    date_fin: '2024-02-15',
    nb_jours: 15,
    statut: 'APPROUVE'
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
        </Routes>
      </MemoryRouter>
    </QueryClientProvider>
  );
};

describe('EmployeeDetails', () => {
  beforeEach(() => {
    (getEmployee as jest.Mock).mockResolvedValue(mockEmployee);
    (getEmployeeLeaves as jest.Mock).mockResolvedValue(mockLeaves);
  });

  it('affiche les informations personnelles de l\'employé', async () => {
    renderWithProviders(<EmployeeDetails />);
    
    expect(await screen.findByText('Jean Dupont')).toBeInTheDocument();
    expect(await screen.findByText('EMP001')).toBeInTheDocument();
    expect(await screen.findByText('jean.dupont@fofal.cm')).toBeInTheDocument();
    expect(await screen.findByText('123456789')).toBeInTheDocument();
  });

  it('affiche les informations professionnelles', async () => {
    renderWithProviders(<EmployeeDetails />);
    
    expect(await screen.findByText('PRODUCTION')).toBeInTheDocument();
    expect(await screen.findByText('Chef d\'équipe')).toBeInTheDocument();
    expect(await screen.findByText('CDI')).toBeInTheDocument();
  });

  it('affiche le statut avec la bonne couleur', async () => {
    renderWithProviders(<EmployeeDetails />);
    
    const statusChip = await screen.findByText('ACTIF');
    expect(statusChip).toHaveClass('MuiChip-colorSuccess');
  });

  it('affiche l\'historique des congés', async () => {
    renderWithProviders(<EmployeeDetails />);
    
    expect(await screen.findByText('ANNUEL')).toBeInTheDocument();
    expect(await screen.findByText('15')).toBeInTheDocument();
    
    const statusChip = await screen.findByText('APPROUVE');
    expect(statusChip).toHaveClass('MuiChip-colorSuccess');
  });

  it('ouvre le formulaire de demande de congé', async () => {
    renderWithProviders(<EmployeeDetails />);
    
    const button = await screen.findByText('Nouvelle Demande');
    fireEvent.click(button);
    
    expect(screen.getByText('Nouvelle Demande de Congé')).toBeInTheDocument();
  });

  it('gère les erreurs de chargement', async () => {
    (getEmployee as jest.Mock).mockRejectedValue(new Error('Erreur de chargement'));
    
    renderWithProviders(<EmployeeDetails />);
    
    expect(await screen.findByText('Une erreur est survenue')).toBeInTheDocument();
  });
});