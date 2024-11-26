import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ContractsPage } from '../ContractsPage';
import { contractService } from '../../../services/contract';
import { LocalizationProvider } from '@mui/x-date-pickers';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { fr } from 'date-fns/locale';

// Mock du service
jest.mock('../../../services/contract', () => ({
    contractService: {
        getActiveContracts: jest.fn(),
        createContract: jest.fn(),
        updateContract: jest.fn(),
        terminateContract: jest.fn()
    }
}));

const mockContracts = [
    {
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
    }
];

describe('ContractsPage', () => {
    const queryClient = new QueryClient({
        defaultOptions: {
            queries: {
                retry: false
            }
        }
    });

    const renderPage = () => {
        return render(
            <QueryClientProvider client={queryClient}>
                <LocalizationProvider dateAdapter={AdapterDateFns} adapterLocale={fr}>
                    <ContractsPage />
                </LocalizationProvider>
            </QueryClientProvider>
        );
    };

    beforeEach(() => {
        jest.clearAllMocks();
        (contractService.getActiveContracts as jest.Mock).mockResolvedValue(mockContracts);
    });

    it('renders the page title and new contract button', async () => {
        renderPage();
        
        expect(screen.getByText('Gestion des Contrats')).toBeInTheDocument();
        expect(screen.getByRole('button', { name: /Nouveau Contrat/i })).toBeInTheDocument();
        
        await waitFor(() => {
            expect(contractService.getActiveContracts).toHaveBeenCalled();
        });
    });

    it('opens the contract form dialog when clicking new contract button', async () => {
        renderPage();
        
        const newButton = screen.getByRole('button', { name: /Nouveau Contrat/i });
        fireEvent.click(newButton);
        
        expect(screen.getByText('Nouveau Contrat')).toBeInTheDocument();
        expect(screen.getByRole('dialog')).toBeInTheDocument();
    });

    it('creates a new contract successfully', async () => {
        (contractService.createContract as jest.Mock).mockResolvedValue(mockContracts[0]);
        renderPage();
        
        // Ouvrir le formulaire
        const newButton = screen.getByRole('button', { name: /Nouveau Contrat/i });
        fireEvent.click(newButton);
        
        // Remplir le formulaire
        await userEvent.click(screen.getByLabelText(/Type de Contrat/i));
        await userEvent.click(screen.getByText('CDI'));
        
        await userEvent.type(screen.getByLabelText(/Salaire/i), '2500');
        await userEvent.type(screen.getByLabelText(/Poste/i), 'Agriculteur');
        await userEvent.type(screen.getByLabelText(/Département/i), 'Production');

        const dateInput = screen.getByLabelText(/Date de Début/i);
        fireEvent.change(dateInput, { target: { value: '2024-01-01' } });

        // Soumettre le formulaire
        const submitButton = screen.getByRole('button', { name: /Enregistrer/i });
        fireEvent.click(submitButton);

        await waitFor(() => {
            expect(contractService.createContract).toHaveBeenCalled();
            expect(screen.getByText('Contrat créé avec succès')).toBeInTheDocument();
        });
    });

    it('handles contract creation error', async () => {
        const error = new Error('Erreur de création');
        (contractService.createContract as jest.Mock).mockRejectedValue(error);
        
        renderPage();
        
        const newButton = screen.getByRole('button', { name: /Nouveau Contrat/i });
        fireEvent.click(newButton);
        
        // Remplir et soumettre le formulaire
        await userEvent.click(screen.getByLabelText(/Type de Contrat/i));
        await userEvent.click(screen.getByText('CDI'));
        
        await userEvent.type(screen.getByLabelText(/Salaire/i), '2500');
        await userEvent.type(screen.getByLabelText(/Poste/i), 'Agriculteur');
        await userEvent.type(screen.getByLabelText(/Département/i), 'Production');

        const dateInput = screen.getByLabelText(/Date de Début/i);
        fireEvent.change(dateInput, { target: { value: '2024-01-01' } });

        const submitButton = screen.getByRole('button', { name: /Enregistrer/i });
        fireEvent.click(submitButton);

        await waitFor(() => {
            expect(screen.getByText(/Erreur lors de la création/)).toBeInTheDocument();
        });
    });

    it('terminates a contract successfully', async () => {
        (contractService.terminateContract as jest.Mock).mockResolvedValue({
            ...mockContracts[0],
            is_active: false
        });
        
        renderPage();
        
        await waitFor(() => {
            expect(screen.getByText('John Doe')).toBeInTheDocument();
        });

        const deleteButton = screen.getByRole('button', { name: /Supprimer/i });
        fireEvent.click(deleteButton);

        await waitFor(() => {
            expect(contractService.terminateContract).toHaveBeenCalled();
            expect(screen.getByText('Contrat terminé avec succès')).toBeInTheDocument();
        });
    });

    it('closes the dialog when clicking cancel', async () => {
        renderPage();
        
        const newButton = screen.getByRole('button', { name: /Nouveau Contrat/i });
        fireEvent.click(newButton);
        
        const cancelButton = screen.getByRole('button', { name: /Annuler/i });
        fireEvent.click(cancelButton);

        await waitFor(() => {
            expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
        });
    });

    it('shows loading state initially', () => {
        (contractService.getActiveContracts as jest.Mock).mockImplementation(
            () => new Promise(() => {})
        );
        
        renderPage();
        expect(screen.getByText('Chargement...')).toBeInTheDocument();
    });

    it('closes snackbar after timeout', async () => {
        (contractService.createContract as jest.Mock).mockResolvedValue(mockContracts[0]);
        
        renderPage();
        
        const newButton = screen.getByRole('button', { name: /Nouveau Contrat/i });
        fireEvent.click(newButton);
        
        // Remplir et soumettre le formulaire
        await userEvent.click(screen.getByLabelText(/Type de Contrat/i));
        await userEvent.click(screen.getByText('CDI'));
        
        await userEvent.type(screen.getByLabelText(/Salaire/i), '2500');
        await userEvent.type(screen.getByLabelText(/Poste/i), 'Agriculteur');
        await userEvent.type(screen.getByLabelText(/Département/i), 'Production');

        const dateInput = screen.getByLabelText(/Date de Début/i);
        fireEvent.change(dateInput, { target: { value: '2024-01-01' } });

        const submitButton = screen.getByRole('button', { name: /Enregistrer/i });
        fireEvent.click(submitButton);

        await waitFor(() => {
            expect(screen.getByText('Contrat créé avec succès')).toBeInTheDocument();
        });

        // Attendre que le snackbar se ferme
        await waitFor(() => {
            expect(screen.queryByText('Contrat créé avec succès')).not.toBeInTheDocument();
        }, { timeout: 7000 });
    });
});
