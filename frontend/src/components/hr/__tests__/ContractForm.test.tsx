import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { ContractForm } from '../ContractForm';
import { LocalizationProvider } from '@mui/x-date-pickers';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { fr } from 'date-fns/locale';

const mockContract = {
    id: '1',
    employee_id: 'emp1',
    employee_name: 'John Doe',
    type: 'CDI',
    start_date: '2024-01-01',
    wage: 2500,
    position: 'Agriculteur',
    department: 'Production',
    is_active: true,
    created_at: '2024-01-01',
    updated_at: '2024-01-01'
};

describe('ContractForm', () => {
    const mockOnSubmit = jest.fn();
    const mockOnCancel = jest.fn();

    const renderForm = (props = {}) => {
        return render(
            <LocalizationProvider dateAdapter={AdapterDateFns} adapterLocale={fr}>
                <ContractForm
                    onSubmit={mockOnSubmit}
                    onCancel={mockOnCancel}
                    {...props}
                />
            </LocalizationProvider>
        );
    };

    beforeEach(() => {
        jest.clearAllMocks();
    });

    it('renders correctly with empty form', () => {
        renderForm();
        expect(screen.getByLabelText(/Type de Contrat/i)).toBeInTheDocument();
        expect(screen.getByLabelText(/Salaire/i)).toBeInTheDocument();
        expect(screen.getByLabelText(/Date de Début/i)).toBeInTheDocument();
        expect(screen.getByLabelText(/Poste/i)).toBeInTheDocument();
        expect(screen.getByLabelText(/Département/i)).toBeInTheDocument();
    });

    it('renders with initial data', () => {
        renderForm({ initialData: mockContract });
        expect(screen.getByLabelText(/Type de Contrat/i)).toHaveValue(mockContract.type);
        expect(screen.getByLabelText(/Salaire/i)).toHaveValue(mockContract.wage);
        expect(screen.getByLabelText(/Poste/i)).toHaveValue(mockContract.position);
        expect(screen.getByLabelText(/Département/i)).toHaveValue(mockContract.department);
    });

    it('shows validation errors for required fields', async () => {
        renderForm();
        
        const submitButton = screen.getByRole('button', { name: /Enregistrer/i });
        fireEvent.click(submitButton);

        await waitFor(() => {
            expect(screen.getByText(/Type de contrat requis/i)).toBeInTheDocument();
            expect(screen.getByText(/Salaire requis/i)).toBeInTheDocument();
            expect(screen.getByText(/Date de début requise/i)).toBeInTheDocument();
            expect(screen.getByText(/Poste requis/i)).toBeInTheDocument();
            expect(screen.getByText(/Département requis/i)).toBeInTheDocument();
        });
    });

    it('calls onSubmit with form data when valid', async () => {
        renderForm();

        // Remplir le formulaire
        await userEvent.click(screen.getByLabelText(/Type de Contrat/i));
        await userEvent.click(screen.getByText('CDI'));
        
        await userEvent.type(screen.getByLabelText(/Salaire/i), '2500');
        await userEvent.type(screen.getByLabelText(/Poste/i), 'Agriculteur');
        await userEvent.type(screen.getByLabelText(/Département/i), 'Production');

        // Sélectionner la date
        const dateInput = screen.getByLabelText(/Date de Début/i);
        fireEvent.change(dateInput, { target: { value: '2024-01-01' } });

        // Soumettre le formulaire
        const submitButton = screen.getByRole('button', { name: /Enregistrer/i });
        fireEvent.click(submitButton);

        await waitFor(() => {
            expect(mockOnSubmit).toHaveBeenCalledWith(expect.objectContaining({
                type: 'CDI',
                wage: 2500,
                position: 'Agriculteur',
                department: 'Production',
                start_date: expect.any(Date)
            }));
        });
    });

    it('calls onCancel when cancel button is clicked', () => {
        renderForm();
        const cancelButton = screen.getByRole('button', { name: /Annuler/i });
        fireEvent.click(cancelButton);
        expect(mockOnCancel).toHaveBeenCalled();
    });

    it('disables form submission when isLoading is true', () => {
        renderForm({ isLoading: true });
        const submitButton = screen.getByRole('button', { name: /Enregistrement/i });
        const cancelButton = screen.getByRole('button', { name: /Annuler/i });
        
        expect(submitButton).toBeDisabled();
        expect(cancelButton).toBeDisabled();
    });
});
