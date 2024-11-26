import React from 'react';
import { render, screen, fireEvent, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { ContractList } from '../ContractList';
import { format } from 'date-fns';
import { fr } from 'date-fns/locale';

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
    },
    {
        id: '2',
        employee_id: 'emp2',
        employee_name: 'Jane Smith',
        type: 'CDD',
        start_date: '2024-01-01',
        end_date: '2024-12-31',
        wage: 2300,
        position: 'Technicien',
        department: 'Maintenance',
        is_active: true,
        created_at: '2024-01-01',
        updated_at: '2024-01-01'
    },
    {
        id: '3',
        employee_id: 'emp3',
        employee_name: 'Bob Wilson',
        type: 'Saisonnier',
        start_date: '2024-01-01',
        end_date: '2024-03-31',
        wage: 2000,
        position: 'Ouvrier agricole',
        department: 'Production',
        is_active: false,
        created_at: '2024-01-01',
        updated_at: '2024-01-01'
    }
];

describe('ContractList', () => {
    const mockOnEdit = jest.fn();
    const mockOnDelete = jest.fn();

    const renderList = () => {
        return render(
            <ContractList
                contracts={mockContracts}
                onEdit={mockOnEdit}
                onDelete={mockOnDelete}
            />
        );
    };

    beforeEach(() => {
        jest.clearAllMocks();
    });

    it('renders all contracts correctly', () => {
        renderList();
        
        mockContracts.forEach(contract => {
            expect(screen.getByText(contract.employee_name)).toBeInTheDocument();
            expect(screen.getByText(contract.type)).toBeInTheDocument();
            expect(screen.getByText(contract.position)).toBeInTheDocument();
            expect(screen.getByText(contract.department)).toBeInTheDocument();
            expect(screen.getByText(format(new Date(contract.start_date), 'dd MMM yyyy', { locale: fr }))).toBeInTheDocument();
        });
    });

    it('filters contracts by type', async () => {
        renderList();
        
        const typeSelect = screen.getByLabelText(/Type/i);
        await userEvent.click(typeSelect);
        await userEvent.click(screen.getByText('CDI'));

        expect(screen.getByText('John Doe')).toBeInTheDocument();
        expect(screen.queryByText('Jane Smith')).not.toBeInTheDocument();
        expect(screen.queryByText('Bob Wilson')).not.toBeInTheDocument();
    });

    it('filters contracts by department', async () => {
        renderList();
        
        const departmentInput = screen.getByLabelText(/Département/i);
        await userEvent.type(departmentInput, 'Production');

        expect(screen.getByText('John Doe')).toBeInTheDocument();
        expect(screen.getByText('Bob Wilson')).toBeInTheDocument();
        expect(screen.queryByText('Jane Smith')).not.toBeInTheDocument();
    });

    it('filters contracts by status', async () => {
        renderList();
        
        const statusSelect = screen.getByLabelText(/Statut/i);
        await userEvent.click(statusSelect);
        await userEvent.click(screen.getByText('Actif'));

        expect(screen.getByText('John Doe')).toBeInTheDocument();
        expect(screen.getByText('Jane Smith')).toBeInTheDocument();
        expect(screen.queryByText('Bob Wilson')).not.toBeInTheDocument();
    });

    it('calls onEdit when edit button is clicked', () => {
        renderList();
        
        const rows = screen.getAllByRole('row');
        const firstRow = rows[1]; // Skip header row
        const editButton = within(firstRow).getByRole('button', { name: /Modifier/i });
        
        fireEvent.click(editButton);
        expect(mockOnEdit).toHaveBeenCalledWith(mockContracts[0]);
    });

    it('calls onDelete when delete button is clicked', () => {
        renderList();
        
        const rows = screen.getAllByRole('row');
        const firstRow = rows[1]; // Skip header row
        const deleteButton = within(firstRow).getByRole('button', { name: /Supprimer/i });
        
        fireEvent.click(deleteButton);
        expect(mockOnDelete).toHaveBeenCalledWith(mockContracts[0].id);
    });

    it('disables edit button for inactive contracts', () => {
        renderList();
        
        const rows = screen.getAllByRole('row');
        const inactiveRow = rows[3]; // Row with inactive contract
        const editButton = within(inactiveRow).getByRole('button', { name: /Modifier/i });
        
        expect(editButton).toBeDisabled();
    });

    it('shows expiring status for contracts ending within 30 days', () => {
        const expiringContract = {
            ...mockContracts[0],
            id: '4',
            end_date: format(new Date(Date.now() + 15 * 24 * 60 * 60 * 1000), 'yyyy-MM-dd') // 15 days from now
        };

        render(
            <ContractList
                contracts={[expiringContract]}
                onEdit={mockOnEdit}
                onDelete={mockOnDelete}
            />
        );

        expect(screen.getByText(/Expire dans \d+ jours/)).toBeInTheDocument();
    });

    it('shows "Aucun contrat trouvé" when filtered results are empty', async () => {
        renderList();
        
        const departmentInput = screen.getByLabelText(/Département/i);
        await userEvent.type(departmentInput, 'Département inexistant');

        expect(screen.getByText('Aucun contrat trouvé')).toBeInTheDocument();
    });
});
