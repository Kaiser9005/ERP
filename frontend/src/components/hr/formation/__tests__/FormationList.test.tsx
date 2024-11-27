import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { FormationList } from '../FormationList';
import { getFormations, deleteFormation } from '../../../../services/formation';

// Mock des services
jest.mock('../../../../services/formation');

const mockFormations = [
    {
        id: '1',
        titre: 'Formation Test 1',
        description: 'Description test 1',
        type: 'technique',
        duree: 8,
        created_at: '2024-01-01T00:00:00Z',
        updated_at: '2024-01-01T00:00:00Z'
    },
    {
        id: '2',
        titre: 'Formation Test 2',
        description: 'Description test 2',
        type: 'securite',
        duree: 4,
        created_at: '2024-01-02T00:00:00Z',
        updated_at: '2024-01-02T00:00:00Z'
    }
];

const queryClient = new QueryClient({
    defaultOptions: {
        queries: {
            retry: false
        }
    }
});

const mockOnAdd = jest.fn();
const mockOnEdit = jest.fn();

describe('FormationList', () => {
    beforeEach(() => {
        (getFormations as jest.Mock).mockResolvedValue(mockFormations);
        (deleteFormation as jest.Mock).mockResolvedValue(undefined);
    });

    afterEach(() => {
        jest.clearAllMocks();
    });

    it('affiche la liste des formations', async () => {
        render(
            <QueryClientProvider client={queryClient}>
                <FormationList onAdd={mockOnAdd} onEdit={mockOnEdit} />
            </QueryClientProvider>
        );

        await waitFor(() => {
            expect(screen.getByText('Formation Test 1')).toBeInTheDocument();
            expect(screen.getByText('Formation Test 2')).toBeInTheDocument();
        });
    });

    it('appelle onAdd quand le bouton Nouvelle Formation est cliqué', async () => {
        render(
            <QueryClientProvider client={queryClient}>
                <FormationList onAdd={mockOnAdd} onEdit={mockOnEdit} />
            </QueryClientProvider>
        );

        const addButton = screen.getByText('Nouvelle Formation');
        fireEvent.click(addButton);

        expect(mockOnAdd).toHaveBeenCalled();
    });

    it('appelle onEdit quand le bouton modifier est cliqué', async () => {
        render(
            <QueryClientProvider client={queryClient}>
                <FormationList onAdd={mockOnAdd} onEdit={mockOnEdit} />
            </QueryClientProvider>
        );

        await waitFor(() => {
            const editButtons = screen.getAllByRole('button', { name: /Modifier/i });
            fireEvent.click(editButtons[0]);
        });

        expect(mockOnEdit).toHaveBeenCalledWith(mockFormations[0]);
    });

    it('supprime une formation quand le bouton supprimer est cliqué', async () => {
        window.confirm = jest.fn(() => true);

        render(
            <QueryClientProvider client={queryClient}>
                <FormationList onAdd={mockOnAdd} onEdit={mockOnEdit} />
            </QueryClientProvider>
        );

        await waitFor(() => {
            const deleteButtons = screen.getAllByRole('button', { name: /Supprimer/i });
            fireEvent.click(deleteButtons[0]);
        });

        expect(deleteFormation).toHaveBeenCalledWith(mockFormations[0].id);
    });

    it('affiche le bon type de formation avec la bonne couleur', async () => {
        render(
            <QueryClientProvider client={queryClient}>
                <FormationList onAdd={mockOnAdd} onEdit={mockOnEdit} />
            </QueryClientProvider>
        );

        await waitFor(() => {
            const typeChips = screen.getAllByRole('button');
            expect(typeChips[0]).toHaveClass('MuiChip-colorPrimary'); // technique
            expect(typeChips[1]).toHaveClass('MuiChip-colorError'); // securite
        });
    });

    it('affiche un message de chargement', () => {
        (getFormations as jest.Mock).mockImplementation(() => new Promise(() => {}));

        render(
            <QueryClientProvider client={queryClient}>
                <FormationList onAdd={mockOnAdd} onEdit={mockOnEdit} />
            </QueryClientProvider>
        );

        expect(screen.getByText('Chargement des formations...')).toBeInTheDocument();
    });
});
