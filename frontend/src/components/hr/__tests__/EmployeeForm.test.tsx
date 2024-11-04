import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from 'react-query';
import { MemoryRouter, Routes, Route } from 'react-router-dom';
import EmployeeForm from '../EmployeeForm';
import { createEmployee, updateEmployee, getEmployee } from '../../../services/hr';

jest.mock('../../../services/hr');

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
          <Route path="/hr" element={<div>HR Page</div>} />
        </Routes>
      </MemoryRouter>
    </QueryClientProvider>
  );
};

describe('EmployeeForm', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('affiche le formulaire de création', () => {
    renderWithProviders(<EmployeeForm />);
    
    expect(screen.getByText('Nouvel Employé')).toBeInTheDocument();
    expect(screen.getByLabelText('Matricule')).toBeInTheDocument();
    expect(screen.getByLabelText('Nom')).toBeInTheDocument();
    expect(screen.getByLabelText('Prénom')).toBeInTheDocument();
  });

  it('valide les champs requis', async () => {
    renderWithProviders(<EmployeeForm />);
    
    fireEvent.click(screen.getByText('Créer'));
    
    expect(await screen.findByText('Le matricule est requis')).toBeInTheDocument();
    expect(await screen.findByText('Le nom est requis')).toBeInTheDocument();
    expect(await screen.findByText('Le prénom est requis')).toBeInTheDocument();
  });

  it('soumet le formulaire avec des données valides', async () => {
    (createEmployee as jest.Mock).mockResolvedValue({ id: '1' });
    
    renderWithProviders(<EmployeeForm />);
    
    fireEvent.change(screen.getByLabelText('Matricule'), { target: { value: 'EMP001' } });
    fireEvent.change(screen.getByLabelText('Nom'), { target: { value: 'Doe' } });
    fireEvent.change(screen.getByLabelText('Prénom'), { target: { value: 'John' } });
    fireEvent.change(screen.getByLabelText('Poste'), { target: { value: 'Technicien' } });
    
    fireEvent.click(screen.getByText('Créer'));
    
    await waitFor(() => {
      expect(createEmployee).toHaveBeenCalledWith({
        matricule: 'EMP001',
        nom: 'Doe',
        prenom: 'John',
        poste: 'Technicien'
      });
    });
  });

  it('gère les erreurs de soumission', async () => {
    (createEmployee as jest.Mock).mockRejectedValue(new Error('Erreur de création'));
    
    renderWithProviders(<EmployeeForm />);
    
    fireEvent.change(screen.getByLabelText('Matricule'), { target: { value: 'EMP001' } });
    fireEvent.click(screen.getByText('Créer'));
    
    expect(await screen.findByText('Une erreur est survenue')).toBeInTheDocument();
  });
});