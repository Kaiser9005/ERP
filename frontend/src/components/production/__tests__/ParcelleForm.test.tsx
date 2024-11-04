import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from 'react-query';
import { MemoryRouter, Routes, Route } from 'react-router-dom';
import ParcelleForm from '../ParcelleForm';
import { createParcelle, updateParcelle, getParcelle } from '../../../services/production';

jest.mock('../../../services/production');

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
          <Route path="/production" element={<div>Production Page</div>} />
        </Routes>
      </MemoryRouter>
    </QueryClientProvider>
  );
};

describe('ParcelleForm', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('affiche le formulaire de création', () => {
    renderWithProviders(<ParcelleForm />);
    
    expect(screen.getByText('Nouvelle Parcelle')).toBeInTheDocument();
    expect(screen.getByLabelText('Code')).toBeInTheDocument();
    expect(screen.getByLabelText('Type de Culture')).toBeInTheDocument();
    expect(screen.getByLabelText('Surface (hectares)')).toBeInTheDocument();
  });

  it('valide les champs requis', async () => {
    renderWithProviders(<ParcelleForm />);
    
    fireEvent.click(screen.getByText('Créer'));
    
    expect(await screen.findByText('Le code est requis')).toBeInTheDocument();
    expect(await screen.findByText('Le type de culture est requis')).toBeInTheDocument();
    expect(await screen.findByText('La surface est requise')).toBeInTheDocument();
  });

  it('soumet le formulaire avec des données valides', async () => {
    (createParcelle as jest.Mock).mockResolvedValue({ id: '1' });
    
    renderWithProviders(<ParcelleForm />);
    
    fireEvent.change(screen.getByLabelText('Code'), { target: { value: 'P003' } });
    fireEvent.change(screen.getByLabelText('Type de Culture'), { target: { value: 'PALMIER' } });
    fireEvent.change(screen.getByLabelText('Surface (hectares)'), { target: { value: '15' } });
    
    fireEvent.click(screen.getByText('Créer'));
    
    await waitFor(() => {
      expect(createParcelle).toHaveBeenCalledWith({
        code: 'P003',
        culture_type: 'PALMIER',
        surface_hectares: '15',
        statut: 'EN_PREPARATION'
      });
    });
  });

  it('gère les erreurs de soumission', async () => {
    (createParcelle as jest.Mock).mockRejectedValue(new Error('Erreur de création'));
    
    renderWithProviders(<ParcelleForm />);
    
    fireEvent.change(screen.getByLabelText('Code'), { target: { value: 'P003' } });
    fireEvent.click(screen.getByText('Créer'));
    
    expect(await screen.findByText('Une erreur est survenue')).toBeInTheDocument();
  });
});