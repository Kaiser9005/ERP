import React from 'react';
import { useForm, Controller } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import * as yup from 'yup';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Grid,
  TextField,
  MenuItem,
  Button
} from '@mui/material';
import { DatePicker } from '@mui/x-date-pickers';
import { useMutation, useQueryClient } from 'react-query';
import { createLeaveRequest } from '../../services/hr';
import { LoadingButton } from '@mui/lab';

const schema = yup.object({
  employe_id: yup.string().required('L\'employé est requis'),
  type_conge: yup.string().required('Le type de congé est requis'),
  date_debut: yup.date().required('La date de début est requise'),
  date_fin: yup.date()
    .required('La date de fin est requise')
    .min(yup.ref('date_debut'), 'La date de fin doit être après la date de début'),
  motif: yup.string()
}).required();

interface LeaveRequestFormProps {
  open: boolean;
  onClose: () => void;
  employeeId?: string;
}

const LeaveRequestForm: React.FC<LeaveRequestFormProps> = ({
  open,
  onClose,
  employeeId
}) => {
  const queryClient = useQueryClient();

  const { control, handleSubmit, formState: { errors } } = useForm({
    resolver: yupResolver(schema),
    defaultValues: {
      employe_id: employeeId || '',
      type_conge: '',
      date_debut: null,
      date_fin: null,
      motif: ''
    }
  });

  const mutation = useMutation(createLeaveRequest, {
    onSuccess: () => {
      queryClient.invalidateQueries('leave-requests');
      onClose();
    }
  });

  const onSubmit = (data: any) => {
    mutation.mutate(data);
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="md" fullWidth>
      <form onSubmit={handleSubmit(onSubmit)}>
        <DialogTitle>Nouvelle Demande de Congé</DialogTitle>
        
        <DialogContent>
          <Grid container spacing={3} sx={{ mt: 1 }}>
            <Grid item xs={12} md={6}>
              <Controller
                name="type_conge"
                control={control}
                render={({ field }) => (
                  <TextField
                    {...field}
                    select
                    label="Type de Congé"
                    fullWidth
                    error={!!errors.type_conge}
                    helperText={errors.type_conge?.message}
                  >
                    <MenuItem value="ANNUEL">Congé Annuel</MenuItem>
                    <MenuItem value="MALADIE">Congé Maladie</MenuItem>
                    <MenuItem value="MATERNITE">Congé Maternité</MenuItem>
                    <MenuItem value="SPECIAL">Congé Spécial</MenuItem>
                    <MenuItem value="SANS_SOLDE">Congé Sans Solde</MenuItem>
                  </TextField>
                )}
              />
            </Grid>

            <Grid item xs={12} md={6}>
              <Controller
                name="date_debut"
                control={control}
                render={({ field }) => (
                  <DatePicker
                    {...field}
                    label="Date de Début"
                    slotProps={{
                      textField: {
                        fullWidth: true,
                        error: !!errors.date_debut,
                        helperText: errors.date_debut?.message
                      }
                    }}
                  />
                )}
              />
            </Grid>

            <Grid item xs={12} md={6}>
              <Controller
                name="date_fin"
                control={control}
                render={({ field }) => (
                  <DatePicker
                    {...field}
                    label="Date de Fin"
                    slotProps={{
                      textField: {
                        fullWidth: true,
                        error: !!errors.date_fin,
                        helperText: errors.date_fin?.message
                      }
                    }}
                  />
                )}
              />
            </Grid>

            <Grid item xs={12}>
              <Controller
                name="motif"
                control={control}
                render={({ field }) => (
                  <TextField
                    {...field}
                    label="Motif"
                    multiline
                    rows={4}
                    fullWidth
                    error={!!errors.motif}
                    helperText={errors.motif?.message}
                  />
                )}
              />
            </Grid>
          </Grid>
        </DialogContent>

        <DialogActions>
          <Button onClick={onClose}>
            Annuler
          </Button>
          <LoadingButton
            variant="contained"
            type="submit"
            loading={mutation.isLoading}
          >
            Soumettre
          </LoadingButton>
        </DialogActions>
      </form>
    </Dialog>
  );
};

export default LeaveRequestForm;