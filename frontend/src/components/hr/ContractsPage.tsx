import React, { useState, useCallback } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {
    Box,
    Button,
    Dialog,
    DialogContent,
    DialogTitle,
    IconButton,
    Typography,
    Alert,
    Snackbar
} from '@mui/material';
import { Add as AddIcon, Close as CloseIcon } from '@mui/icons-material';
import { ContractForm } from './ContractForm';
import { ContractList } from './ContractList';
import { Contract, ContractCreate, ContractUpdate } from '../../types/contract';
import { contractService } from '../../services/contract';

export const ContractsPage: React.FC = () => {
    const queryClient = useQueryClient();
    const [isFormOpen, setIsFormOpen] = useState(false);
    const [selectedContract, setSelectedContract] = useState<Contract | null>(null);
    const [snackbar, setSnackbar] = useState<{
        open: boolean;
        message: string;
        severity: 'success' | 'error';
    }>({
        open: false,
        message: '',
        severity: 'success'
    });

    // Récupération des contrats
    const { data: contracts = [], isLoading } = useQuery({
        queryKey: ['contracts'],
        queryFn: contractService.getActiveContracts
    });

    // Création d'un contrat
    const createMutation = useMutation({
        mutationFn: contractService.createContract,
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['contracts'] });
            setIsFormOpen(false);
            setSnackbar({
                open: true,
                message: 'Contrat créé avec succès',
                severity: 'success'
            });
        },
        onError: (error) => {
            setSnackbar({
                open: true,
                message: `Erreur lors de la création: ${error.message}`,
                severity: 'error'
            });
        }
    });

    // Mise à jour d'un contrat
    const updateMutation = useMutation({
        mutationFn: (params: { id: string; contract: ContractUpdate }) =>
            contractService.updateContract(params.id, params.contract),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['contracts'] });
            setIsFormOpen(false);
            setSelectedContract(null);
            setSnackbar({
                open: true,
                message: 'Contrat mis à jour avec succès',
                severity: 'success'
            });
        },
        onError: (error) => {
            setSnackbar({
                open: true,
                message: `Erreur lors de la mise à jour: ${error.message}`,
                severity: 'error'
            });
        }
    });

    // Suppression d'un contrat
    const terminateMutation = useMutation({
        mutationFn: (params: { id: string; endDate: string }) =>
            contractService.terminateContract(params.id, params.endDate),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['contracts'] });
            setSnackbar({
                open: true,
                message: 'Contrat terminé avec succès',
                severity: 'success'
            });
        },
        onError: (error) => {
            setSnackbar({
                open: true,
                message: `Erreur lors de la terminaison: ${error.message}`,
                severity: 'error'
            });
        }
    });

    const handleCreate = useCallback((data: ContractCreate) => {
        createMutation.mutate(data);
    }, [createMutation]);

    const handleUpdate = useCallback((data: ContractUpdate) => {
        if (selectedContract) {
            updateMutation.mutate({ id: selectedContract.id, contract: data });
        }
    }, [selectedContract, updateMutation]);

    const handleEdit = useCallback((contract: Contract) => {
        setSelectedContract(contract);
        setIsFormOpen(true);
    }, []);

    const handleDelete = useCallback((contractId: string) => {
        const today = new Date().toISOString().split('T')[0];
        terminateMutation.mutate({ id: contractId, endDate: today });
    }, [terminateMutation]);

    const handleCloseForm = useCallback(() => {
        setIsFormOpen(false);
        setSelectedContract(null);
    }, []);

    const handleCloseSnackbar = useCallback(() => {
        setSnackbar(prev => ({ ...prev, open: false }));
    }, []);

    if (isLoading) {
        return <Box sx={{ p: 3 }}>Chargement...</Box>;
    }

    return (
        <Box sx={{ p: 3 }}>
            <Box sx={{ mb: 3, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <Typography variant="h5">Gestion des Contrats</Typography>
                <Button
                    variant="contained"
                    startIcon={<AddIcon />}
                    onClick={() => setIsFormOpen(true)}
                >
                    Nouveau Contrat
                </Button>
            </Box>

            <ContractList
                contracts={contracts}
                onEdit={handleEdit}
                onDelete={handleDelete}
            />

            <Dialog
                open={isFormOpen}
                onClose={handleCloseForm}
                maxWidth="md"
                fullWidth
            >
                <DialogTitle sx={{ m: 0, p: 2 }}>
                    {selectedContract ? 'Modifier le Contrat' : 'Nouveau Contrat'}
                    <IconButton
                        onClick={handleCloseForm}
                        sx={{ position: 'absolute', right: 8, top: 8 }}
                    >
                        <CloseIcon />
                    </IconButton>
                </DialogTitle>
                <DialogContent>
                    {selectedContract ? (
                        <ContractForm
                            initialData={selectedContract}
                            onSubmit={handleUpdate}
                            onCancel={handleCloseForm}
                            isLoading={updateMutation.isPending}
                        />
                    ) : (
                        <ContractForm
                            onSubmit={data => handleCreate(data as ContractCreate)}
                            onCancel={handleCloseForm}
                            isLoading={createMutation.isPending}
                        />
                    )}
                </DialogContent>
            </Dialog>

            <Snackbar
                open={snackbar.open}
                autoHideDuration={6000}
                onClose={handleCloseSnackbar}
                anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
            >
                <Alert
                    onClose={handleCloseSnackbar}
                    severity={snackbar.severity}
                    variant="filled"
                    sx={{ width: '100%' }}
                >
                    {snackbar.message}
                </Alert>
            </Snackbar>
        </Box>
    );
};
