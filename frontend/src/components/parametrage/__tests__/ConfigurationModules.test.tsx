import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from 'react-query';
import ConfigurationModules from '../ConfigurationModules';
import { getModulesConfiguration, updateModuleConfiguration } from '../../../services/parametrage';

jest.mock('../../../services/parametrage');

const mockModules = [
  {
    id: '1',
    module: 'PRODUCTION',
    actif: true,
    configuration: {},
    ordre_affichage: 1,
    icone: 'agriculture',
    couleur: '#4CAF50',
    roles_autorises: ['ADMIN', 'MANAGER']
  },
  {
    id: '2',
    module: 'INVENTAIRE',
    actif: false,
    configuration: {},
    ordre_affichage: 2,
    icone: 'inventory',
    couleur: '#2196F3',
    roles_autorises: ['ADMIN']
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

describe('ConfigurationModules', () => {
  beforeEach(() => {
    (getModulesConfiguration as jest.Mock).mockResolvedValue(mockModules);
  });

  it('affiche la liste des modules', async () => {
    renderWithProviders(<ConfigurationModules />);
    
    expect(await screen.findByText('PRODUCTION')).toBeInTheDocument();
    expect(await screen.findByText('INVENTAIRE')).toBeInTheDocument();
  });

  it('permet l\'activation/désactivation des modules', async () => {
    (updateModuleConfiguration as jest.Mock).mockResolvedValue({
      ...mockModules[0],
      actif: false
    });

    renderWithProviders(<ConfigurationModules />);
    
    const toggle = await screen.findByRole('switch', { name: /PRODUCTION/ });
    fireEvent.click(toggle);

    await waitFor(() => {
      expect(updateModuleConfiguration).toHaveBeenCalledWith({
        module: 'PRODUCTION',
        actif: false
      });
    });
  });

  it('affiche les rôles autorisés', async () => {
    renderWithProviders(<ConfigurationModules />);
    
    expect(await screen.findByText('ADMIN')).toBeInTheDocument();
    expect(await screen.findByText('MANAGER')).toBeInTheDocument();
  });

  it('affiche l\'état actif/inactif des modules', async () => {
    renderWithProviders(<ConfigurationModules />);
    
    const productionSwitch = await screen.findByRole('switch', { name: /PRODUCTION/ });
    const inventaireSwitch = await screen.findByRole('switch', { name: /INVENTAIRE/ });
    
    expect(productionSwitch).toBeChecked();
    expect(inventaireSwitch).not.toBeChecked();
  });

  it('affiche le bouton de configuration', async () => {
    renderWithProviders(<ConfigurationModules />);
    
    const configButtons = await screen.findAllByTestId('settings-button');
    expect(configButtons).toHaveLength(2);
  });

  it('gère les erreurs de mise à jour', async () => {
    (updateModuleConfiguration as jest.Mock).mockRejectedValue(new Error('Erreur de configuration'));

    renderWithProviders(<ConfigurationModules />);
    
    const toggle = await screen.findByRole('switch', { name: /PRODUCTION/ });
    fireEvent.click(toggle);

    expect(await screen.findByText('Une erreur est survenue')).toBeInTheDocument();
  });
});