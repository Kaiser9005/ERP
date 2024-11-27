import React, { useState } from 'react';
import { Box, Typography, Paper } from '@mui/material';
import { Formation } from '../../../types/formation';
import { FormationList } from './FormationList';
import { FormationForm } from './FormationForm';

export const FormationPage: React.FC = () => {
    const [formOpen, setFormOpen] = useState(false);
    const [selectedFormation, setSelectedFormation] = useState<Formation | undefined>();

    const handleAdd = () => {
        setSelectedFormation(undefined);
        setFormOpen(true);
    };

    const handleEdit = (formation: Formation) => {
        setSelectedFormation(formation);
        setFormOpen(true);
    };

    const handleClose = () => {
        setFormOpen(false);
        setSelectedFormation(undefined);
    };

    return (
        <Box sx={{ p: 3 }}>
            <Typography variant="h4" component="h1" gutterBottom>
                Gestion des Formations
            </Typography>

            <Paper sx={{ p: 2, mb: 2 }}>
                <Typography variant="body1" paragraph>
                    Gérez les formations de l'entreprise, y compris les formations techniques,
                    de sécurité et agricoles. Chaque formation peut être associée à des compétences
                    requises et acquises, du matériel nécessaire et des conditions météorologiques
                    spécifiques.
                </Typography>
            </Paper>

            <FormationList
                onAdd={handleAdd}
                onEdit={handleEdit}
            />

            <FormationForm
                open={formOpen}
                onClose={handleClose}
                formation={selectedFormation}
            />
        </Box>
    );
};
