import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { AddSensorDialog } from '../AddSensorDialog';
import { useCreateSensor } from '../../../services/iot';
import { SensorType } from '../../../types/iot';

// Mock des services
jest.mock('../../../services/iot', () => ({
  useCreateSensor: jest.fn(),
}));

describe('AddSensorDialog', () => {
  let queryClient: QueryClient;
  const mockOnClose = jest.fn();
  const mockMutateAsync = jest.fn();

  beforeEach(() => {
    queryClient = new QueryClient({
      defaultOptions: {
        queries: {
          retry: false,
        },
      },
    });

    (useCreateSensor as jest.Mock).mockReturnValue({
      mutateAsync: mockMutateAsync,
      isPending: false,
    });
  });

  const renderWithQuery = (ui: React.ReactElement) => {
    return render(
      <QueryClientProvider client={queryClient}>
        {ui}
      </QueryClientProvider>
    );
  };

  it('affiche le dialogue quand open est true', () => {
    renderWithQuery(
      <AddSensorDialog
        open={true}
        onClose={mockOnClose}
        parcelleId="parcelle-1"
      />
    );

    expect(screen.getByText('Ajouter un nouveau capteur')).toBeInTheDocument();
  });

  it('n\'affiche pas le dialogue quand open est false', () => {
    renderWithQuery(
      <AddSensorDialog
        open={false}
        onClose={mockOnClose}
        parcelleId="parcelle-1"
      />
    );

    expect(screen.queryByText('Ajouter un nouveau capteur')).not.toBeInTheDocument();
  });

  it('appelle onClose quand on clique sur Annuler', () => {
    renderWithQuery(
      <AddSensorDialog
        open={true}
        onClose={mockOnClose}
        parcelleId="parcelle-1"
      />
    );

    fireEvent.click(screen.getByText('Annuler'));
    expect(mockOnClose).toHaveBeenCalled();
  });

  it('affiche une erreur quand le code est vide', async () => {
    renderWithQuery(
      <AddSensorDialog
        open={true}
        onClose={mockOnClose}
        parcelleId="parcelle-1"
      />
    );

    fireEvent.click(screen.getByText('Ajouter'));

    await waitFor(() => {
      expect(screen.getByText('Le code est requis')).toBeInTheDocument();
    });
  });

  it('soumet le formulaire avec les données correctes', async () => {
    mockMutateAsync.mockResolvedValueOnce({});

    renderWithQuery(
      <AddSensorDialog
        open={true}
        onClose={mockOnClose}
        parcelleId="parcelle-1"
      />
    );

    // Remplir le formulaire
    fireEvent.change(screen.getByLabelText('Code du capteur'), {
      target: { value: 'TEMP-001' },
    });

    fireEvent.change(screen.getByLabelText('Type de capteur'), {
      target: { value: SensorType.TEMPERATURE_SOL },
    });

    fireEvent.change(screen.getByLabelText('Intervalle de lecture (secondes)'), {
      target: { value: '300' },
    });

    // Soumettre le formulaire
    fireEvent.click(screen.getByText('Ajouter'));

    await waitFor(() => {
      expect(mockMutateAsync).toHaveBeenCalledWith(expect.objectContaining({
        code: 'TEMP-001',
        type: SensorType.TEMPERATURE_SOL,
        parcelle_id: 'parcelle-1',
        intervalle_lecture: 300,
      }));
      expect(mockOnClose).toHaveBeenCalled();
    });
  });

  it('affiche une erreur si l\'intervalle est trop court', async () => {
    renderWithQuery(
      <AddSensorDialog
        open={true}
        onClose={mockOnClose}
        parcelleId="parcelle-1"
      />
    );

    fireEvent.change(screen.getByLabelText('Intervalle de lecture (secondes)'), {
      target: { value: '30' },
    });

    fireEvent.click(screen.getByText('Ajouter'));

    await waitFor(() => {
      expect(screen.getByText('Minimum 60 secondes')).toBeInTheDocument();
    });
  });

  it('affiche une erreur si l\'intervalle est trop long', async () => {
    renderWithQuery(
      <AddSensorDialog
        open={true}
        onClose={mockOnClose}
        parcelleId="parcelle-1"
      />
    );

    fireEvent.change(screen.getByLabelText('Intervalle de lecture (secondes)'), {
      target: { value: '4000' },
    });

    fireEvent.click(screen.getByText('Ajouter'));

    await waitFor(() => {
      expect(screen.getByText('Maximum 3600 secondes (1 heure)')).toBeInTheDocument();
    });
  });

  it('affiche les seuils par défaut pour le type sélectionné', async () => {
    renderWithQuery(
      <AddSensorDialog
        open={true}
        onClose={mockOnClose}
        parcelleId="parcelle-1"
      />
    );

    // Sélectionner le type de capteur
    fireEvent.change(screen.getByLabelText('Type de capteur'), {
      target: { value: SensorType.TEMPERATURE_SOL },
    });

    await waitFor(() => {
      expect(screen.getByText('Seuil min')).toBeInTheDocument();
      expect(screen.getByText('Seuil max')).toBeInTheDocument();
      expect(screen.getByText('Seuil critique_min')).toBeInTheDocument();
      expect(screen.getByText('Seuil critique_max')).toBeInTheDocument();
    });
  });

  it('désactive le bouton pendant la soumission', async () => {
    (useCreateSensor as jest.Mock).mockReturnValue({
      mutateAsync: mockMutateAsync,
      isPending: true,
    });

    renderWithQuery(
      <AddSensorDialog
        open={true}
        onClose={mockOnClose}
        parcelleId="parcelle-1"
      />
    );

    const submitButton = screen.getByRole('button', { name: 'Ajouter' });
    expect(submitButton).toBeDisabled();
  });
});
