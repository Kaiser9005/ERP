import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import CompetencesAgricoles from '../CompetencesAgricoles';
import { getCompetencesEmploye, createCompetence, updateCompetence } from '../../../../services/hr_agricole';
import { CompetenceAgricole } from '../../../../types/hr_agricole';

// Mock des services
jest.mock('../../../../services/hr_agricole');

const mockCompetences: CompetenceAgricole[] = [
  {
    id: '1',
    employe_id: 'emp1',
    specialite: 'CULTURE',
    niveau: 'AVANCE',
    cultures: ['Blé', 'Maïs'],
    equipements: ['Tracteur', 'Moissonneuse'],
    date_acquisition: '2023-01-15',
    validite: '2024-01-15',
    commentaire: 'Très bon niveau',
    donnees_supplementaires: {}
  },
  {
    id: '2',
    employe_id: 'emp1',
    specialite: 'ELEVAGE',
    niveau: 'EXPERT',
    cultures: ['Fourrage'],
    equipements: ['Robot de traite'],
    date_acquisition: '2023-02-20',
    validite: '2024-02-20',
    commentaire: 'Expert en élevage bovin',
    donnees_supplementaires: {}
  }
];

describe('CompetencesAgricoles', () => {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: {
        retry: false,
      },
    },
  });

  const renderComponent = () => {
    return render(
      <QueryClientProvider client={queryClient}>
        <CompetencesAgricoles employeId="emp1" />
      </QueryClientProvider>
    );
  };

  beforeEach(() => {
    jest.clearAllMocks();
    (getCompetencesEmploye as jest.Mock).mockResolvedValue(mockCompetences);
  });

  it('affiche un loader pendant le chargement des données', () => {
    renderComponent();
    expect(screen.getByRole('progressbar')).toBeInTheDocument();
  });

  it('affiche la liste des compétences après le chargement', async () => {
    renderComponent();

    await waitFor(() => {
      expect(screen.getByText('CULTURE')).toBeInTheDocument();
      expect(screen.getByText('ELEVAGE')).toBeInTheDocument();
    });

    expect(screen.getByText('Blé')).toBeInTheDocument();
    expect(screen.getByText('Maïs')).toBeInTheDocument();
    expect(screen.getByText('Tracteur')).toBeInTheDocument();
    expect(screen.getByText('Robot de traite')).toBeInTheDocument();
  });

  it('affiche un message d\'erreur en cas d\'échec du chargement', async () => {
    (getCompetencesEmploye as jest.Mock).mockRejectedValue(new Error('Erreur de chargement'));
    renderComponent();

    await waitFor(() => {
      expect(screen.getByText('Une erreur est survenue lors du chargement des compétences')).toBeInTheDocument();
    });
  });

  it('ouvre le formulaire lors du clic sur le bouton ajouter', async () => {
    renderComponent();

    await waitFor(() => {
      expect(screen.getByText('Ajouter une compétence')).toBeInTheDocument();
    });

    fireEvent.click(screen.getByText('Ajouter une compétence'));
    expect(screen.getByText('Nouvelle compétence')).toBeInTheDocument();
  });

  it('ouvre le formulaire en mode édition lors du clic sur modifier', async () => {
    renderComponent();

    await waitFor(() => {
      expect(screen.getByText('CULTURE')).toBeInTheDocument();
    });

    // Trouver et cliquer sur le bouton modifier
    const editButtons = screen.getAllByTitle('Modifier');
    fireEvent.click(editButtons[0]);

    expect(screen.getByText('Modifier la compétence')).toBeInTheDocument();
    expect(screen.getByDisplayValue('CULTURE')).toBeInTheDocument();
  });

  it('crée une nouvelle compétence avec succès', async () => {
    const newCompetence = {
      id: '3',
      employe_id: 'emp1',
      specialite: 'MARAICHAGE',
      niveau: 'INTERMEDIAIRE',
      cultures: ['Tomates', 'Salades'],
      equipements: ['Serre'],
      date_acquisition: '2023-03-15',
      validite: '2024-03-15',
      commentaire: 'Formation en cours',
      donnees_supplementaires: {}
    };

    (createCompetence as jest.Mock).mockResolvedValue(newCompetence);
    renderComponent();

    await waitFor(() => {
      expect(screen.getByText('Ajouter une compétence')).toBeInTheDocument();
    });

    fireEvent.click(screen.getByText('Ajouter une compétence'));

    // Remplir et soumettre le formulaire
    // Note: Les détails du remplissage du formulaire sont testés dans CompetenceForm.test.tsx
    const submitButton = screen.getByText('Créer');
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(createCompetence).toHaveBeenCalled();
    });
  });

  it('met à jour une compétence avec succès', async () => {
    const updatedCompetence = {
      ...mockCompetences[0],
      niveau: 'EXPERT'
    };

    (updateCompetence as jest.Mock).mockResolvedValue(updatedCompetence);
    renderComponent();

    await waitFor(() => {
      expect(screen.getByText('CULTURE')).toBeInTheDocument();
    });

    // Cliquer sur le bouton modifier
    const editButtons = screen.getAllByTitle('Modifier');
    fireEvent.click(editButtons[0]);

    // Soumettre le formulaire
    const submitButton = screen.getByText('Modifier');
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(updateCompetence).toHaveBeenCalled();
    });
  });

  it('ferme le formulaire après une création réussie', async () => {
    (createCompetence as jest.Mock).mockResolvedValue(mockCompetences[0]);
    renderComponent();

    await waitFor(() => {
      expect(screen.getByText('Ajouter une compétence')).toBeInTheDocument();
    });

    fireEvent.click(screen.getByText('Ajouter une compétence'));
    expect(screen.getByText('Nouvelle compétence')).toBeInTheDocument();

    const submitButton = screen.getByText('Créer');
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(screen.queryByText('Nouvelle compétence')).not.toBeInTheDocument();
    });
  });

  it('ferme le formulaire après une mise à jour réussie', async () => {
    (updateCompetence as jest.Mock).mockResolvedValue(mockCompetences[0]);
    renderComponent();

    await waitFor(() => {
      expect(screen.getByText('CULTURE')).toBeInTheDocument();
    });

    const editButtons = screen.getAllByTitle('Modifier');
    fireEvent.click(editButtons[0]);
    expect(screen.getByText('Modifier la compétence')).toBeInTheDocument();

    const submitButton = screen.getByText('Modifier');
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(screen.queryByText('Modifier la compétence')).not.toBeInTheDocument();
    });
  });
});
