import React from 'react';
import {
    Box,
    Button,
    IconButton,
    Paper,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    Typography,
    Chip,
    Tooltip
} from '@mui/material';
import { Add as AddIcon, Edit as EditIcon, Delete as DeleteIcon } from '@mui/icons-material';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Formation } from '../../../types/formation';
import { getFormations, deleteFormation } from '../../../services/formation';
import { format } from 'date-fns';
import { fr } from 'date-fns/locale';

interface FormationListProps {
    onAdd: () => void;
    onEdit: (formation: Formation) => void;
}

export const FormationList: React.FC<FormationListProps> = ({ onAdd, onEdit }) => {
    const queryClient = useQueryClient();

    const { data: formations, isLoading } = useQuery({
        queryKey: ['formations'],
        queryFn: () => getFormations()
    });

    const deleteMutation = useMutation({
        mutationFn: deleteFormation,
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['formations'] });
        }
    });

    const handleDelete = async (id: string) => {
        if (window.confirm('Êtes-vous sûr de vouloir supprimer cette formation ?')) {
            await deleteMutation.mutateAsync(id);
        }
    };

    const getTypeColor = (type: string) => {
        switch (type) {
            case 'technique':
                return 'primary';
            case 'securite':
                return 'error';
            case 'agricole':
                return 'success';
            default:
                return 'default';
        }
    };

    if (isLoading) {
        return <Typography>Chargement des formations...</Typography>;
    }

    return (
        <Box>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
                <Typography variant="h5" component="h2">
                    Formations
                </Typography>
                <Button
                    variant="contained"
                    color="primary"
                    startIcon={<AddIcon />}
                    onClick={onAdd}
                >
                    Nouvelle Formation
                </Button>
            </Box>

            <TableContainer component={Paper}>
                <Table>
                    <TableHead>
                        <TableRow>
                            <TableCell>Titre</TableCell>
                            <TableCell>Type</TableCell>
                            <TableCell>Durée (heures)</TableCell>
                            <TableCell>Date de création</TableCell>
                            <TableCell>Actions</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {formations?.map((formation) => (
                            <TableRow key={formation.id}>
                                <TableCell>
                                    <Typography variant="body1">
                                        {formation.titre}
                                    </Typography>
                                    {formation.description && (
                                        <Typography
                                            variant="body2"
                                            color="textSecondary"
                                            sx={{ mt: 0.5 }}
                                        >
                                            {formation.description}
                                        </Typography>
                                    )}
                                </TableCell>
                                <TableCell>
                                    <Chip
                                        label={formation.type}
                                        color={getTypeColor(formation.type)}
                                        size="small"
                                    />
                                </TableCell>
                                <TableCell>{formation.duree}</TableCell>
                                <TableCell>
                                    {format(new Date(formation.created_at), 'Pp', { locale: fr })}
                                </TableCell>
                                <TableCell>
                                    <Tooltip title="Modifier">
                                        <IconButton
                                            size="small"
                                            onClick={() => onEdit(formation)}
                                            color="primary"
                                        >
                                            <EditIcon />
                                        </IconButton>
                                    </Tooltip>
                                    <Tooltip title="Supprimer">
                                        <IconButton
                                            size="small"
                                            onClick={() => handleDelete(formation.id)}
                                            color="error"
                                        >
                                            <DeleteIcon />
                                        </IconButton>
                                    </Tooltip>
                                </TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>
        </Box>
    );
};
