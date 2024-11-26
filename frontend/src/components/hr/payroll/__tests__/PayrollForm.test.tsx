import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { LocalizationProvider } from '@mui/x-date-pickers';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { fr } from 'date-fns/locale';
import { PayrollForm } from '../PayrollForm';
import { PayrollSlip } from '../../../../types/payroll';

const mockPayroll: PayrollSlip = {
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
};

const mockOnSubmit = jest.fn();
const mockOnCancel = jest.fn();

const renderComponent = (initialData?: PayrollSlip) => {
  return render(
    <LocalizationProvider dateAdapter={AdapterDateFns} adapterLocale={fr}>
      <PayrollForm
        initialData={initialData}
        onSubmit={mockOnSubmit}
        onCancel={mockOnCancel}
      />
    </LocalizationProvider>
  );
};

describe('PayrollForm', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('affiche le titre correct pour un nouveau formulaire', () => {
    renderComponent();
    expect(screen.getByText('Nouvelle fiche de paie')).toBeInTheDocument();
  });

  it('affiche le titre correct pour la modification', () => {
    renderComponent(mockPayroll);
    expect(screen.getByText('Modifier la fiche de paie')).toBeInTheDocument();
  });

  it('initialise les champs avec les valeurs par défaut', () => {
    renderComponent();
    expect(screen.getByLabelText('Heures travaillées')).toHaveValue(151.67);
    expect(screen.getByLabelText('Heures supplémentaires')).toHaveValue(0);
    expect(screen.getByLabelText('Montant heures sup.')).toHaveValue(0);
    expect(screen.getByLabelText('Primes')).toHaveValue(0);
    expect(screen.getByLabelText('Retenues')).toHaveValue(0);
    expect(screen.getByLabelText('Charges patronales')).toHaveValue(0);
    expect(screen.getByLabelText('Charges salariales')).toHaveValue(0);
  });

  it('initialise les champs avec les données existantes', () => {
    renderComponent(mockPayroll);
    expect(screen.getByLabelText('Heures travaillées')).toHaveValue(151.67);
    expect(screen.getByLabelText('Heures supplémentaires')).toHaveValue(10);
    expect(screen.getByLabelText('Montant heures sup.')).toHaveValue(250);
    expect(screen.getByLabelText('Primes')).toHaveValue(100);
    expect(screen.getByLabelText('Retenues')).toHaveValue(50);
    expect(screen.getByLabelText('Charges patronales')).toHaveValue(500);
    expect(screen.getByLabelText('Charges salariales')).toHaveValue(200);
  });

  it('appelle onSubmit avec les données correctes', async () => {
    renderComponent();
    
    // Remplir le formulaire
    fireEvent.change(screen.getByLabelText('Heures travaillées'), {
      target: { value: '160' }
    });
    fireEvent.change(screen.getByLabelText('Heures supplémentaires'), {
      target: { value: '10' }
    });
    fireEvent.change(screen.getByLabelText('Montant heures sup.'), {
      target: { value: '250' }
    });
    fireEvent.change(screen.getByLabelText('Primes'), {
      target: { value: '100' }
    });

    // Soumettre le formulaire
    fireEvent.click(screen.getByText('Créer'));

    await waitFor(() => {
      expect(mockOnSubmit).toHaveBeenCalledWith(expect.objectContaining({
        worked_hours: 160,
        overtime_hours: 10,
        overtime_amount: 250,
        bonus: 100,
      }));
    });
  });

  it('appelle onCancel lors du clic sur Annuler', () => {
    renderComponent();
    fireEvent.click(screen.getByText('Annuler'));
    expect(mockOnCancel).toHaveBeenCalled();
  });

  it('affiche le bouton correct selon le mode', () => {
    // Nouveau formulaire
    const { rerender } = renderComponent();
    expect(screen.getByText('Créer')).toBeInTheDocument();

    // Formulaire de modification
    rerender(
      <LocalizationProvider dateAdapter={AdapterDateFns} adapterLocale={fr}>
        <PayrollForm
          initialData={mockPayroll}
          onSubmit={mockOnSubmit}
          onCancel={mockOnCancel}
        />
      </LocalizationProvider>
    );
    expect(screen.getByText('Modifier')).toBeInTheDocument();
  });

  it('permet la saisie de valeurs décimales pour les heures', () => {
    renderComponent();
    const input = screen.getByLabelText('Heures travaillées');
    
    fireEvent.change(input, { target: { value: '151.5' } });
    expect(input).toHaveValue(151.5);
  });

  it('permet la saisie de valeurs négatives pour les retenues', () => {
    renderComponent();
    const input = screen.getByLabelText('Retenues');
    
    fireEvent.change(input, { target: { value: '-50' } });
    expect(input).toHaveValue(-50);
  });
});
