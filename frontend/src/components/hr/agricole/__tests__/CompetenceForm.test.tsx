import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { LocalizationProvider } from '@mui/x-date-pickers';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { fr } from 'date-fns/locale';
import CompetenceForm from '../CompetenceForm';
import { CompetenceAgricole } from '../../../../types/hr_agricole';

const mockCompetence: CompetenceAgricole = {
  id: '1',
  employe_id: 'emp-123',
  specialite: 'CULTURE',
  niveau: 'AVANCE',
  cultures: ['Blé', 'Maïs'],
  equipements: ['Tracteur', 'Moissonneuse'],
  date_acquisition: '2023-01-15',
  validite: '2024-01-15',
  commentaire: 'Très bon niveau',
  donnees_supplementaires: {}
};

const renderWithProviders = (ui: React.ReactElement) => {
  return render(
    <LocalizationProvider dateAdapter={AdapterDateFns} adapterLocale={fr}>
      {ui}
    </LocalizationProvider>
  );
};

describe('CompetenceForm', () => {
  const mockOnSubmit = jest.fn();
  const mockOnClose = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('affiche le formulaire en mode création', () => {
    renderWithProviders(
      <CompetenceForm
        open={true}
        onClose={mockOnClose}
        onSubmit={mockOnSubmit}
        employeId="emp-123"
      />
    );

    expect(screen.getByText('Nouvelle compétence')).toBeInTheDocument();
    expect(screen.getByLabelText('Spécialité')).toBeInTheDocument();
    expect(screen.getByLabelText('Niveau')).toBeInTheDocument();
    expect(screen.getByLabelText(/Cultures/)).toBeInTheDocument();
    expect(screen.getByLabelText(/Équipements/)).toBeInTheDocument();
    expect(screen.getByLabelText(/Date d'acquisition/)).toBeInTheDocument();
  });

  it('affiche le formulaire en mode édition avec les données pré-remplies', () => {
    renderWithProviders(
      <CompetenceForm
        open={true}
        onClose={mockOnClose}
        onSubmit={mockOnSubmit}
        employeId="emp-123"
        competence={mockCompetence}
      />
    );

    expect(screen.getByText('Modifier la compétence')).toBeInTheDocument();
    expect(screen.getByText('CULTURE')).toBeInTheDocument();
    expect(screen.getByText('AVANCE')).toBeInTheDocument();
    expect(screen.getByText('Blé')).toBeInTheDocument();
    expect(screen.getByText('Maïs')).toBeInTheDocument();
    expect(screen.getByText('Tracteur')).toBeInTheDocument();
    expect(screen.getByText('Moissonneuse')).toBeInTheDocument();
  });

  it('affiche les erreurs de validation', async () => {
    renderWithProviders(
      <CompetenceForm
        open={true}
        onClose={mockOnClose}
        onSubmit={mockOnSubmit}
        employeId="emp-123"
      />
    );

    const submitButton = screen.getByText('Créer');
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText(/Au moins une culture doit être sélectionnée/)).toBeInTheDocument();
    });
  });

  it('appelle onSubmit avec les données correctes', async () => {
    renderWithProviders(
      <CompetenceForm
        open={true}
        onClose={mockOnClose}
        onSubmit={mockOnSubmit}
        employeId="emp-123"
      />
    );

    // Remplir le formulaire
    fireEvent.mouseDown(screen.getByLabelText('Spécialité'));
    fireEvent.click(screen.getByText('CULTURE'));

    fireEvent.mouseDown(screen.getByLabelText('Niveau'));
    fireEvent.click(screen.getByText('AVANCE'));

    // Sélectionner une culture
    const culturesInput = screen.getByLabelText(/Cultures/);
    fireEvent.change(culturesInput, { target: { value: 'Blé' } });
    fireEvent.keyDown(culturesInput, { key: 'Enter' });

    // Sélectionner un équipement
    const equipementsInput = screen.getByLabelText(/Équipements/);
    fireEvent.change(equipementsInput, { target: { value: 'Tracteur' } });
    fireEvent.keyDown(equipementsInput, { key: 'Enter' });

    // Définir la date d'acquisition
    const dateAcquisitionInput = screen.getByLabelText(/Date d'acquisition/);
    fireEvent.change(dateAcquisitionInput, { target: { value: '2023-01-15' } });

    // Soumettre le formulaire
    fireEvent.click(screen.getByText('Créer'));

    await waitFor(() => {
      expect(mockOnSubmit).toHaveBeenCalledWith(expect.objectContaining({
        employe_id: 'emp-123',
        specialite: 'CULTURE',
        niveau: 'AVANCE',
        cultures: ['Blé'],
        equipements: ['Tracteur'],
        date_acquisition: expect.any(String)
      }));
    });
  });

  it('désactive les boutons pendant le chargement', () => {
    renderWithProviders(
      <CompetenceForm
        open={true}
        onClose={mockOnClose}
        onSubmit={mockOnSubmit}
        employeId="emp-123"
        isLoading={true}
      />
    );

    expect(screen.getByText('Créer')).toBeDisabled();
    expect(screen.getByText('Annuler')).toBeDisabled();
  });

  it('appelle onClose lors du clic sur Annuler', () => {
    renderWithProviders(
      <CompetenceForm
        open={true}
        onClose={mockOnClose}
        onSubmit={mockOnSubmit}
        employeId="emp-123"
      />
    );

    fireEvent.click(screen.getByText('Annuler'));
    expect(mockOnClose).toHaveBeenCalled();
  });

  it('réinitialise le formulaire lors de la fermeture', () => {
    const { rerender } = renderWithProviders(
      <CompetenceForm
        open={true}
        onClose={mockOnClose}
        onSubmit={mockOnSubmit}
        employeId="emp-123"
      />
    );

    // Remplir le formulaire
    fireEvent.mouseDown(screen.getByLabelText('Spécialité'));
    fireEvent.click(screen.getByText('CULTURE'));

    // Fermer et rouvrir le formulaire
    rerender(
      <CompetenceForm
        open={false}
        onClose={mockOnClose}
        onSubmit={mockOnSubmit}
        employeId="emp-123"
      />
    );

    rerender(
      <CompetenceForm
        open={true}
        onClose={mockOnClose}
        onSubmit={mockOnSubmit}
        employeId="emp-123"
      />
    );

    // Vérifier que le formulaire est vide
    expect(screen.queryByText('CULTURE')).not.toBeInTheDocument();
  });
});
