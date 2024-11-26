import React, { useState } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import {
  Box,
  Typography,
  Button,
  Dialog,
  DialogContent,
  Snackbar,
  Alert,
} from '@mui/material';
import { Add as AddIcon } from '@mui/icons-material';
import { PayrollList } from './PayrollList';
import { PayrollForm } from './PayrollForm';
import { payrollService } from '../../../services/payroll';
import { PayrollSlip, CreatePayrollRequest } from '../../../types/payroll';

export const PayrollPage: React.FC = () => {
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [selectedPayroll, setSelectedPayroll] = useState<PayrollSlip | undefined>();
  const [snackbar, setSnackbar] = useState<{
    open: boolean;
    message: string;
    severity: 'success' | 'error';
  }>({
    open: false,
    message: '',
    severity: 'success',
  });

  const queryClient = useQueryClient();

  const createMutation = useMutation({
    mutationFn: payrollService.create,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['payrolls'] });
      setSnackbar({
        open: true,
        message: 'Fiche de paie créée avec succès',
        severity: 'success',
      });
      handleCloseForm();
    },
    onError: () => {
      setSnackbar({
        open: true,
        message: 'Erreur lors de la création de la fiche de paie',
        severity: 'error',
      });
    },
  });

  const updateMutation = useMutation({
    mutationFn: (data: { id: string; payload: CreatePayrollRequest }) =>
      payrollService.update(data.id, data.payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['payrolls'] });
      setSnackbar({
        open: true,
        message: 'Fiche de paie mise à jour avec succès',
        severity: 'success',
      });
      handleCloseForm();
    },
    onError: () => {
      setSnackbar({
        open: true,
        message: 'Erreur lors de la mise à jour de la fiche de paie',
        severity: 'error',
      });
    },
  });

  const deleteMutation = useMutation({
    mutationFn: payrollService.delete,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['payrolls'] });
      setSnackbar({
        open: true,
        message: 'Fiche de paie supprimée avec succès',
        severity: 'success',
      });
    },
    onError: () => {
      setSnackbar({
        open: true,
        message: 'Erreur lors de la suppression de la fiche de paie',
        severity: 'error',
      });
    },
  });

  const validateMutation = useMutation({
    mutationFn: payrollService.validate,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['payrolls'] });
      setSnackbar({
        open: true,
        message: 'Fiche de paie validée avec succès',
        severity: 'success',
      });
    },
    onError: () => {
      setSnackbar({
        open: true,
        message: 'Erreur lors de la validation de la fiche de paie',
        severity: 'error',
      });
    },
  });

  const handleOpenForm = (payroll?: PayrollSlip) => {
    setSelectedPayroll(payroll);
    setIsFormOpen(true);
  };

  const handleCloseForm = () => {
    setSelectedPayroll(undefined);
    setIsFormOpen(false);
  };

  const handleSubmit = (data: CreatePayrollRequest) => {
    if (selectedPayroll) {
      updateMutation.mutate({ id: selectedPayroll.id, payload: data });
    } else {
      createMutation.mutate(data);
    }
  };

  const handleDelete = (id: string) => {
    if (window.confirm('Êtes-vous sûr de vouloir supprimer cette fiche de paie ?')) {
      deleteMutation.mutate(id);
    }
  };

  const handleValidate = (id: string) => {
    if (window.confirm('Êtes-vous sûr de vouloir valider cette fiche de paie ?')) {
      validateMutation.mutate(id);
    }
  };

  return (
    <Box sx={{ p: 3 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h5">Gestion des Fiches de Paie</Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => handleOpenForm()}
        >
          Nouvelle Fiche de Paie
        </Button>
      </Box>

      <PayrollList
        onEdit={(id: string) => {
          const payroll = queryClient.getQueryData<PayrollSlip[]>(['payrolls'])?.find(p => p.id === id);
          handleOpenForm(payroll);
        }}
        onDelete={handleDelete}
        onValidate={handleValidate}
      />

      <Dialog
        open={isFormOpen}
        onClose={handleCloseForm}
        maxWidth="md"
        fullWidth
      >
        <DialogContent>
          <PayrollForm
            initialData={selectedPayroll}
            onSubmit={handleSubmit}
            onCancel={handleCloseForm}
          />
        </DialogContent>
      </Dialog>

      <Snackbar
        open={snackbar.open}
        autoHideDuration={6000}
        onClose={() => setSnackbar({ ...snackbar, open: false })}
      >
        <Alert
          onClose={() => setSnackbar({ ...snackbar, open: false })}
          severity={snackbar.severity}
          sx={{ width: '100%' }}
        >
          {snackbar.message}
        </Alert>
      </Snackbar>
    </Box>
  );
};
