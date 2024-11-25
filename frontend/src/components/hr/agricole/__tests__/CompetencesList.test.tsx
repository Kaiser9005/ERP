import { render, screen, fireEvent } from '@testing-library/react';
import { format } from 'date-fns';
import { fr } from 'date-fns/locale';
import CompetencesList from '../CompetencesList';
import { CompetenceAgricole } from '../../../../types/hr_agricole';

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

describe('CompetencesList', () => {
  const mockOnEdit = jest.fn();

  beforeEach(() => {
    mockOnEdit.mockClear();
  });

  it('affiche la liste des compétences', () => {
    render(
      <CompetencesList
        competences={mockCompetences}
        onEdit={mockOnEdit}
      />
    );

    // Vérifie les en-têtes
    expect(screen.getByText('Spécialité')).toBeInTheDocument();
    expect(screen.getByText('Niveau')).toBeInTheDocument();
    expect(screen.getByText('Cultures')).toBeInTheDocument();
    expect(screen.getByText('Équipements')).toBeInTheDocument();
    expect(screen.getByText('Date acquisition')).toBeInTheDocument();
    expect(screen.getByText('Validité')).toBeInTheDocument();

    // Vérifie les données de la première compétence
    expect(screen.getByText('CULTURE')).toBeInTheDocument();
    expect(screen.getByText('AVANCE')).toBeInTheDocument();
    expect(screen.getByText('Blé')).toBeInTheDocument();
    expect(screen.getByText('Maïs')).toBeInTheDocument();
    expect(screen.getByText('Tracteur')).toBeInTheDocument();
    expect(screen.getByText('Moissonneuse')).toBeInTheDocument();
    expect(screen.getByText(format(new Date('2023-01-15'), 'dd MMMM yyyy', { locale: fr }))).toBeInTheDocument();

    // Vérifie les données de la deuxième compétence
    expect(screen.getByText('ELEVAGE')).toBeInTheDocument();
    expect(screen.getByText('EXPERT')).toBeInTheDocument();
    expect(screen.getByText('Fourrage')).toBeInTheDocument();
    expect(screen.getByText('Robot de traite')).toBeInTheDocument();
    expect(screen.getByText(format(new Date('2023-02-20'), 'dd MMMM yyyy', { locale: fr }))).toBeInTheDocument();
  });

  it('affiche un message quand il n\'y a pas de compétences', () => {
    render(
      <CompetencesList
        competences={[]}
        onEdit={mockOnEdit}
      />
    );

    expect(screen.getByText('Aucune compétence agricole enregistrée pour cet employé')).toBeInTheDocument();
  });

  it('appelle onEdit avec la compétence correcte lors du clic sur le bouton modifier', () => {
    render(
      <CompetencesList
        competences={mockCompetences}
        onEdit={mockOnEdit}
      />
    );

    const editButtons = screen.getAllByRole('button');
    fireEvent.click(editButtons[0]); // Clic sur le premier bouton modifier

    expect(mockOnEdit).toHaveBeenCalledTimes(1);
    expect(mockOnEdit).toHaveBeenCalledWith(mockCompetences[0]);
  });

  it('affiche un indicateur d\'expiration pour les compétences expirées', () => {
    const competencesAvecExpiration = [
      {
        ...mockCompetences[0],
        validite: '2023-01-01' // Date expirée
      }
    ];

    render(
      <CompetencesList
        competences={competencesAvecExpiration}
        onEdit={mockOnEdit}
      />
    );

    // Vérifie la présence de l'icône d'avertissement (le titre du tooltip)
    expect(screen.getByTitle('Compétence expirée')).toBeInTheDocument();
  });
});
