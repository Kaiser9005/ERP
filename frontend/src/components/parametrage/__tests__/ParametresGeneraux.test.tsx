import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from 'react-query';
import ParametresGeneraux from '../ParametresGeneraux';
import { getParametres, updateParametre } from '../../../services/parametrage';

jest.mock('../../../services/parametrage');

const mockParametres = [
  {
    id: '1',
    code: 'DEVISE_DEFAUT',
    libelle: 'Devise par défaut',
    description: 'Devise utilisée dans le système',
    type_parametre: 'GENERAL',
    valeur: { value: 'XAF' },
    modifiable: true,
    visible: true,
    ordre: 1
  },
  {
    id: '2',
    code: 'LANGUE_DEFAUT',
    libelle: 'Langue par défaut',
    description: 'Langue du système',
    type_parametre: 'GENERAL',
    valeur: { value: 'fr' },
    modifiable: true,
    visible: true,
    ordre: 2
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

describe('ParametresGeneraux', () => {
  beforeEach(() => {
    (getParametres as jest.Mock).mockResolvedValue(mockParametres);
  });

  it('affiche la liste des paramètres', async () => {
    renderWithProviders(<ParametresGeneraux />);
    
    expect(await screen.findByText('Devise par défaut')).toBeInTheDocument();
    expect(await screen.findByText('Langue par défaut')).toBeInTheDocument();
  });

  it('permet la modification des paramètres modifiables', async () => {
    (updateParametre as jest.Mock).mockResolvedValue({
      ...mockParametres[0],
      valeur: { value: 'EUR' }
    });

    renderWithProviders(<ParametresGeneraux />);
    
    const input = await screen.findByDisplayValue('XAF');
    fireEvent.change(input, { target: { value: 'EUR' } });

    await waitFor(() => {
      expect(updateParametre).toHaveBeenCalledWith({
        id: '1',
        valeur: { value: 'EUR' }
      });
    });
  });

  it('désactive les champs non modifiables', async () => {
    const nonModifiableParams = mockParametres.map(param => ({
      ...param,
      modifiable: false
    }));
    (getParametres as jest.Mock).mockResolvedValue(nonModifiableParams);

    renderWithProviders(<ParametresGeneraux />);
    
    const inputs = await screen.findAllByRole('textbox');
    inputs.forEach(input => {
      expect(input).toBeDisabled();
    });
  });

  it('affiche les descriptions des paramètres', async () => {
    renderWithProviders(<ParametresGeneraux />);
    
    expect(await screen.findByText('Devise utilisée dans le système')).toBeInTheDocument();
    expect(await screen.findByText('Langue du système')).toBeInTheDocument();
  });

  it('gère les erreurs de mise à jour', async () => {
    (updateParametre as jest.Mock).mockRejectedValue(new Error('Erreur de mise à jour'));

    renderWithProviders(<ParametresGeneraux />);
    
    const input = await screen.findByDisplayValue('XAF');
    fireEvent.change(input, { target: { value: 'EUR' } });

    expect(await screen.findByText('Une erreur est survenue')).toBeInTheDocument();
  });
});