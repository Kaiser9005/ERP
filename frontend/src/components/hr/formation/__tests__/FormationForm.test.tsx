import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { FormationForm } from '../FormationForm';
import { createFormation, updateFormation } from '../../../../services/formation';
import { Formation } from '../../../../types/formation';

// Mock des services
jest.mock('../../../../services/formation');

const queryClient = new QueryClient({
    defaultOptions: {
        queries: {
            retry: false
        }
    }
});

const mockFormation: Formation = {
    id: '1',
    titre: 'Formation Test',
    description: 'Description test',
    type: 'technique',
    duree: 8,
    competences_requises: { niveau: 'debutant' },
    competences_acquises: { technique: 'base' },
    materiel_requis: { ordinateur: true },
    conditions_meteo: { exterieur: false },
    created_at: '2024-01-01T00:00:00Z',
    updated_at: '2024-01-01T00:00:00Z'
};

describe('FormationForm', () => {
    const mockOnClose = jest.fn();

    beforeEach(() => {
        (createFormation as jest.Mock).mockResolvedValue(mockFormation);
        (updateFormation as jest.Mock).mockResolvedValue(mockFormation);
    });

    afterEach(() => {
        jest.clearAllMocks();
    });

    it('affiche le formulaire de création', () => {
        render(
            <QueryClientProvider client={queryClient}>
                <FormationForm open={true} onClose={mockOnClose} />
            </QueryClientProvider>
        );

        expect(screen.getByText('Nouvelle formation')).toBeInTheDocument();
        expect(screen.getByLabelText('Titre')).toBeInTheDocument();
        expect(screen.getByLabelText('Description')).toBeInTheDocument();
        expect(screen.getByLabelText('Type')).toBeInTheDocument();
        expect(screen.getByLabelText('Durée (heures)')).toBeInTheDocument();
    });

    it('affiche le formulaire de modification avec les données existantes', () => {
        render(
            <QueryClientProvider client={queryClient}>
                <FormationForm 
                    open={true} 
                    onClose={mockOnClose}
                    formation={mockFormation}
                />
            </QueryClientProvider>
        );

        expect(screen.getByText('Modifier la formation')).toBeInTheDocument();
        expect(screen.getByLabelText('Titre')).toHaveValue(mockFormation.titre);
        expect(screen.getByLabelText('Description')).toHaveValue(mockFormation.description);
        expect(screen.getByLabelText('Type')).toHaveValue(mockFormation.type);
        expect(screen.getByLabelText('Durée (heures)')).toHaveValue(mockFormation.duree);
    });

    it('valide les champs requis', async () => {
        render(
            <QueryClientProvider client={queryClient}>
                <FormationForm open={true} onClose={mockOnClose} />
            </QueryClientProvider>
        );

        // Cliquer sur le bouton de soumission sans remplir les champs
        fireEvent.click(screen.getByText('Créer'));

        // Vérifier les messages d'erreur
        await waitFor(() => {
            expect(screen.getByText('Le titre est requis')).toBeInTheDocument();
            expect(screen.getByText('Le type est requis')).toBeInTheDocument();
            expect(screen.getByText('La durée est requise')).toBeInTheDocument();
        });
    });

    it('crée une nouvelle formation', async () => {
        render(
            <QueryClientProvider client={queryClient}>
                <FormationForm open={true} onClose={mockOnClose} />
            </QueryClientProvider>
        );

        // Remplir le formulaire
        fireEvent.change(screen.getByLabelText('Titre'), {
            target: { value: 'Nouvelle Formation' }
        });
        fireEvent.change(screen.getByLabelText('Description'), {
            target: { value: 'Description de la formation' }
        });
        fireEvent.change(screen.getByLabelText('Type'), {
            target: { value: 'technique' }
        });
        fireEvent.change(screen.getByLabelText('Durée (heures)'), {
            target: { value: '8' }
        });

        // Soumettre le formulaire
        fireEvent.click(screen.getByText('Créer'));

        await waitFor(() => {
            expect(createFormation).toHaveBeenCalledWith({
                titre: 'Nouvelle Formation',
                description: 'Description de la formation',
                type: 'technique',
                duree: 8,
                competences_requises: {},
                competences_acquises: {},
                materiel_requis: {},
                conditions_meteo: {}
            });
            expect(mockOnClose).toHaveBeenCalled();
        });
    });

    it('met à jour une formation existante', async () => {
        render(
            <QueryClientProvider client={queryClient}>
                <FormationForm 
                    open={true} 
                    onClose={mockOnClose}
                    formation={mockFormation}
                />
            </QueryClientProvider>
        );

        // Modifier les champs
        fireEvent.change(screen.getByLabelText('Titre'), {
            target: { value: 'Formation Modifiée' }
        });

        // Soumettre le formulaire
        fireEvent.click(screen.getByText('Modifier'));

        await waitFor(() => {
            expect(updateFormation).toHaveBeenCalledWith(mockFormation.id, {
                ...mockFormation,
                titre: 'Formation Modifiée'
            });
            expect(mockOnClose).toHaveBeenCalled();
        });
    });

    it('gère correctement les champs JSON', async () => {
        render(
            <QueryClientProvider client={queryClient}>
                <FormationForm open={true} onClose={mockOnClose} />
            </QueryClientProvider>
        );

        // Tester la saisie de JSON valide
        fireEvent.change(screen.getByLabelText('Compétences requises'), {
            target: { value: '{"niveau": "avance", "experience": "2ans"}' }
        });

        // Tester la saisie de JSON invalide
        fireEvent.change(screen.getByLabelText('Compétences acquises'), {
            target: { value: 'json invalide' }
        });

        // Soumettre le formulaire
        fireEvent.click(screen.getByText('Créer'));

        await waitFor(() => {
            expect(screen.getByLabelText('Compétences requises')).toHaveValue(
                '{\n  "niveau": "avance",\n  "experience": "2ans"\n}'
            );
        });
    });

    it('ferme le formulaire quand on clique sur Annuler', () => {
        render(
            <QueryClientProvider client={queryClient}>
                <FormationForm open={true} onClose={mockOnClose} />
            </QueryClientProvider>
        );

        fireEvent.click(screen.getByText('Annuler'));
        expect(mockOnClose).toHaveBeenCalled();
    });
});
