import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { FormationPage } from '../FormationPage';
import { getFormations } from '../../../../services/formation';

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

describe('FormationPage', () => {
    beforeEach(() => {
        (getFormations as jest.Mock).mockResolvedValue(mockFormations);
    });

    afterEach(() => {
        jest.clearAllMocks();
    });

    it('affiche le titre de la page', () => {
        render(
            <QueryClientProvider client={queryClient}>
                <FormationPage />
            </QueryClientProvider>
        );

        expect(screen.getByText('Gestion des Formations')).toBeInTheDocument();
    });

    it('affiche la description de la page', () => {
        render(
            <QueryClientProvider client={queryClient}>
                <FormationPage />
            </QueryClientProvider>
        );

        expect(screen.getByText(/Gérez les formations de l'entreprise/)).toBeInTheDocument();
    });

    it('affiche la liste des formations', async () => {
        render(
            <QueryClientProvider client={queryClient}>
                <FormationPage />
            </QueryClientProvider>
        );

        await waitFor(() => {
            expect(screen.getByText('Formation Test 1')).toBeInTheDocument();
            expect(screen.getByText('Formation Test 2')).toBeInTheDocument();
        });
    });

    it('ouvre le formulaire de création quand on clique sur Nouvelle Formation', async () => {
        render(
            <QueryClientProvider client={queryClient}>
                <FormationPage />
            </QueryClientProvider>
        );

        const addButton = screen.getByText('Nouvelle Formation');
        fireEvent.click(addButton);

        await waitFor(() => {
            expect(screen.getByText('Nouvelle formation')).toBeInTheDocument();
        });
    });

    it('ouvre le formulaire de modification quand on clique sur modifier', async () => {
        render(
            <QueryClientProvider client={queryClient}>
                <FormationPage />
            </QueryClientProvider>
        );

        await waitFor(() => {
            const editButtons = screen.getAllByRole('button', { name: /Modifier/i });
            fireEvent.click(editButtons[0]);
        });

        expect(screen.getByText('Modifier la formation')).toBeInTheDocument();
        expect(screen.getByDisplayValue('Formation Test 1')).toBeInTheDocument();
    });

    it('ferme le formulaire quand on clique sur Annuler', async () => {
        render(
            <QueryClientProvider client={queryClient}>
                <FormationPage />
            </QueryClientProvider>
        );

        // Ouvrir le formulaire
        const addButton = screen.getByText('Nouvelle Formation');
        fireEvent.click(addButton);

        // Vérifier que le formulaire est ouvert
        await waitFor(() => {
            expect(screen.getByText('Nouvelle formation')).toBeInTheDocument();
        });

        // Fermer le formulaire
        const cancelButton = screen.getByText('Annuler');
        fireEvent.click(cancelButton);

        // Vérifier que le formulaire est fermé
        await waitFor(() => {
            expect(screen.queryByText('Nouvelle formation')).not.toBeInTheDocument();
        });
    });

    it('gère correctement l\'état du formulaire entre création et modification', async () => {
        render(
            <QueryClientProvider client={queryClient}>
                <FormationPage />
            </QueryClientProvider>
        );

        // Ouvrir le formulaire de création
        const addButton = screen.getByText('Nouvelle Formation');
        fireEvent.click(addButton);

        await waitFor(() => {
            expect(screen.getByText('Nouvelle formation')).toBeInTheDocument();
        });

        // Fermer le formulaire
        const cancelButton = screen.getByText('Annuler');
        fireEvent.click(cancelButton);

        // Ouvrir le formulaire de modification
        await waitFor(() => {
            const editButtons = screen.getAllByRole('button', { name: /Modifier/i });
            fireEvent.click(editButtons[0]);
        });

        // Vérifier que c'est bien le formulaire de modification
        expect(screen.getByText('Modifier la formation')).toBeInTheDocument();
        expect(screen.getByDisplayValue('Formation Test 1')).toBeInTheDocument();
    });

    it('rafraîchit la liste après la fermeture du formulaire', async () => {
        const updatedFormations = [
            ...mockFormations,
            {
                id: '3',
                titre: 'Nouvelle Formation',
                description: 'Description nouvelle formation',
                type: 'technique',
                duree: 6,
                created_at: '2024-01-03T00:00:00Z',
                updated_at: '2024-01-03T00:00:00Z'
            }
        ];

        (getFormations as jest.Mock)
            .mockResolvedValueOnce(mockFormations)
            .mockResolvedValueOnce(updatedFormations);

        render(
            <QueryClientProvider client={queryClient}>
                <FormationPage />
            </QueryClientProvider>
        );

        // Vérifier la liste initiale
        await waitFor(() => {
            expect(screen.getByText('Formation Test 1')).toBeInTheDocument();
            expect(screen.getByText('Formation Test 2')).toBeInTheDocument();
        });

        // Simuler une mise à jour
        queryClient.setQueryData(['formations'], updatedFormations);

        // Vérifier la mise à jour de la liste
        await waitFor(() => {
            expect(screen.getByText('Nouvelle Formation')).toBeInTheDocument();
        });
    });
});
