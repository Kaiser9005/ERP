import { render, screen, fireEvent } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { PayrollList } from '../PayrollList';
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
  },
  {
    id: '2',
    contract_id: 'contract2',
    period_start: '2024-02-01',
    period_end: '2024-02-29',
    worked_hours: 151.67,
    overtime_hours: 0,
    base_salary: 2000,
    overtime_amount: 0,
    bonus: 0,
    deductions: 0,
    bonus_details: {},
    deduction_details: {},
    employer_contributions: 500,
    employee_contributions: 200,
    gross_total: 2000,
    net_total: 1800,
    is_paid: true,
    payment_date: '2024-03-01',
    created_at: '2024-02-01',
    updated_at: '2024-03-01'
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

// Mock des fonctions de callback
const mockOnEdit = jest.fn();
const mockOnDelete = jest.fn();
const mockOnValidate = jest.fn();

describe('PayrollList', () => {
  beforeEach(() => {
    // Reset des mocks
    jest.clearAllMocks();
    
    // Configuration du mock du service
    (payrollService.getByPeriod as jest.Mock).mockResolvedValue(mockPayrolls);
  });

  const renderComponent = () => {
    return render(
      <QueryClientProvider client={queryClient}>
        <PayrollList
          onEdit={mockOnEdit}
          onDelete={mockOnDelete}
          onValidate={mockOnValidate}
        />
      </QueryClientProvider>
    );
  };

  it('affiche la liste des fiches de paie', async () => {
    renderComponent();

    // Vérifie que les fiches de paie sont affichées
    expect(await screen.findByText('151.67h (+ 10h sup.)')).toBeInTheDocument();
    expect(screen.getByText('151.67h')).toBeInTheDocument();
  });

  it('affiche le statut correct pour les fiches payées et non payées', async () => {
    renderComponent();

    // Vérifie les statuts
    expect(await screen.findByText('En attente')).toBeInTheDocument();
    expect(screen.getByText('Payée le 1 mars 2024')).toBeInTheDocument();
  });

  it('appelle onEdit avec l\'id correct lors du clic sur modifier', async () => {
    renderComponent();

    // Attendre que le composant soit chargé
    await screen.findByText('151.67h (+ 10h sup.)');

    // Cliquer sur le bouton modifier de la première fiche
    const editButtons = screen.getAllByTitle('Modifier');
    fireEvent.click(editButtons[0]);

    expect(mockOnEdit).toHaveBeenCalledWith('1');
  });

  it('appelle onDelete avec l\'id correct lors du clic sur supprimer', async () => {
    renderComponent();

    // Attendre que le composant soit chargé
    await screen.findByText('151.67h (+ 10h sup.)');

    // Cliquer sur le bouton supprimer de la première fiche
    const deleteButtons = screen.getAllByTitle('Supprimer');
    fireEvent.click(deleteButtons[0]);

    expect(mockOnDelete).toHaveBeenCalledWith('1');
  });

  it('appelle onValidate avec l\'id correct lors du clic sur valider', async () => {
    renderComponent();

    // Attendre que le composant soit chargé
    await screen.findByText('151.67h (+ 10h sup.)');

    // Cliquer sur le bouton valider de la première fiche
    const validateButton = screen.getByTitle('Valider le paiement');
    fireEvent.click(validateButton);

    expect(mockOnValidate).toHaveBeenCalledWith('1');
  });

  it('désactive les boutons d\'action pour les fiches payées', async () => {
    renderComponent();

    // Attendre que le composant soit chargé
    await screen.findByText('151.67h (+ 10h sup.)');

    // Récupérer tous les boutons d'action
    const editButtons = screen.getAllByTitle('Modifier');
    const deleteButtons = screen.getAllByTitle('Supprimer');

    // Vérifier que les boutons sont désactivés pour la fiche payée
    expect(editButtons[1]).toBeDisabled();
    expect(deleteButtons[1]).toBeDisabled();
  });

  it('affiche un message de chargement', () => {
    (payrollService.getByPeriod as jest.Mock).mockImplementationOnce(() => new Promise(() => {}));
    renderComponent();
    expect(screen.getByText('Chargement des fiches de paie...')).toBeInTheDocument();
  });

  it('affiche un message d\'erreur en cas d\'échec du chargement', async () => {
    (payrollService.getByPeriod as jest.Mock).mockRejectedValueOnce(new Error('Erreur de chargement'));
    renderComponent();
    expect(await screen.findByText('Erreur lors du chargement des fiches de paie')).toBeInTheDocument();
  });
});
