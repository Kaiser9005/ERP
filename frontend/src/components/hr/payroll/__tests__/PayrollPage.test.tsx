import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { LocalizationProvider } from '@mui/x-date-pickers';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { fr } from 'date-fns/locale';
import { PayrollPage } from '../PayrollPage';
import { payrollService } from '../../../../services/payroll';

// Mock du service
jest.mock('../../../../services/payroll');

// Mock des données
const mockPayrolls = [
  {
    id: '1',
    contract_id: 'contract1',
    period_start: '2024-01-01',
    period_end: '2024-01-31',
    worked_hours: 151.67,
    overtime_hours: 10,
    base_salary: 2000,
    overtime_amount: 250,
    bonus: 100,
    deductions: 50,
    bonus_details: { prime_agricole: 100 },
    deduction_details: { absence: 50 },
    employer_contributions: 500,
    employee_contributions: 200,
    gross_total: 2300,
    net_total: 2100,
    is_paid: false,
    payment_date: null,
    created_at: '2024-01-01',
    updated_at: '2024-01-01'
  }
];

// Configuration du client React Query
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
      <LocalizationProvider dateAdapter={AdapterDateFns} adapterLocale={fr}>
        <PayrollPage />
      </LocalizationProvider>
    </QueryClientProvider>
  );
};

describe('PayrollPage', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    (payrollService.getByPeriod as jest.Mock).mockResolvedValue(mockPayrolls);
  });

  it('affiche le titre de la page', () => {
    renderComponent();
    expect(screen.getByText('Gestion des Fiches de Paie')).toBeInTheDocument();
  });

  it('ouvre le formulaire de création lors du clic sur le bouton Nouvelle Fiche', () => {
    renderComponent();
    fireEvent.click(screen.getByText('Nouvelle Fiche de Paie'));
    expect(screen.getByText('Nouvelle fiche de paie')).toBeInTheDocument();
  });

  it('ferme le formulaire lors du clic sur Annuler', () => {
    renderComponent();
    fireEvent.click(screen.getByText('Nouvelle Fiche de Paie'));
    fireEvent.click(screen.getByText('Annuler'));
    expect(screen.queryByText('Nouvelle fiche de paie')).not.toBeInTheDocument();
  });

  it('crée une nouvelle fiche de paie', async () => {
    (payrollService.create as jest.Mock).mockResolvedValueOnce(mockPayrolls[0]);
    renderComponent();

    // Ouvrir le formulaire
    fireEvent.click(screen.getByText('Nouvelle Fiche de Paie'));

    // Remplir et soumettre le formulaire
    fireEvent.change(screen.getByLabelText('Heures travaillées'), {
      target: { value: '160' }
    });
    fireEvent.click(screen.getByText('Créer'));

    // Vérifier le succès
    await waitFor(() => {
      expect(screen.getByText('Fiche de paie créée avec succès')).toBeInTheDocument();
    });
  });

  it('modifie une fiche de paie existante', async () => {
    (payrollService.update as jest.Mock).mockResolvedValueOnce(mockPayrolls[0]);
    renderComponent();

    // Attendre le chargement des données
    await screen.findByText('151.67h (+ 10h sup.)');

    // Cliquer sur le bouton modifier
    const editButtons = screen.getAllByTitle('Modifier');
    fireEvent.click(editButtons[0]);

    // Modifier et soumettre le formulaire
    fireEvent.change(screen.getByLabelText('Heures travaillées'), {
      target: { value: '160' }
    });
    fireEvent.click(screen.getByText('Modifier'));

    // Vérifier le succès
    await waitFor(() => {
      expect(screen.getByText('Fiche de paie mise à jour avec succès')).toBeInTheDocument();
    });
  });

  it('supprime une fiche de paie', async () => {
    (payrollService.delete as jest.Mock).mockResolvedValueOnce({ message: 'Supprimé' });
    window.confirm = jest.fn(() => true);
    
    renderComponent();

    // Attendre le chargement des données
    await screen.findByText('151.67h (+ 10h sup.)');

    // Cliquer sur le bouton supprimer
    const deleteButtons = screen.getAllByTitle('Supprimer');
    fireEvent.click(deleteButtons[0]);

    // Vérifier le succès
    await waitFor(() => {
      expect(screen.getByText('Fiche de paie supprimée avec succès')).toBeInTheDocument();
    });
  });

  it('valide une fiche de paie', async () => {
    (payrollService.validate as jest.Mock).mockResolvedValueOnce({ message: 'Validé' });
    window.confirm = jest.fn(() => true);
    
    renderComponent();

    // Attendre le chargement des données
    await screen.findByText('151.67h (+ 10h sup.)');

    // Cliquer sur le bouton valider
    const validateButton = screen.getByTitle('Valider le paiement');
    fireEvent.click(validateButton);

    // Vérifier le succès
    await waitFor(() => {
      expect(screen.getByText('Fiche de paie validée avec succès')).toBeInTheDocument();
    });
  });

  it('affiche une erreur lors de l\'échec de création', async () => {
    (payrollService.create as jest.Mock).mockRejectedValueOnce(new Error('Erreur'));
    renderComponent();

    // Ouvrir le formulaire
    fireEvent.click(screen.getByText('Nouvelle Fiche de Paie'));

    // Soumettre le formulaire
    fireEvent.click(screen.getByText('Créer'));

    // Vérifier l'erreur
    await waitFor(() => {
      expect(screen.getByText('Erreur lors de la création de la fiche de paie')).toBeInTheDocument();
    });
  });

  it('demande confirmation avant la suppression', async () => {
    window.confirm = jest.fn(() => false);
    renderComponent();

    // Attendre le chargement des données
    await screen.findByText('151.67h (+ 10h sup.)');

    // Cliquer sur le bouton supprimer
    const deleteButtons = screen.getAllByTitle('Supprimer');
    fireEvent.click(deleteButtons[0]);

    // Vérifier que la confirmation a été demandée
    expect(window.confirm).toHaveBeenCalledWith('Êtes-vous sûr de vouloir supprimer cette fiche de paie ?');
    expect(payrollService.delete).not.toHaveBeenCalled();
  });
});
