import React from 'react';
import {
  Card,
  CardContent,
  Typography,
  Box,
  TextField,
  Button,
  MenuItem,
  Grid
} from '@mui/material';
import { useForm, Controller } from 'react-hook-form';
import { useMutation, useQueryClient } from 'react-query';
import { useNavigate } from 'react-router-dom';
import { createLeaveRequest, LeaveRequest } from '../../services/hr';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import fr from 'date-fns/locale/fr';

type FormData = {
  type_conge: string;
  date_debut: Date;
  date_fin: Date;
  motif: string;
};

const TYPES_CONGE = [
  { value: 'CONGE_ANNUEL', label: 'Congé annuel' },
  { value: 'CONGE_MALADIE', label: 'Congé maladie' },
  { value: 'CONGE_MATERNITE', label: 'Congé maternité' },
  { value: 'CONGE_PATERNITE', label: 'Congé paternité' },
  { value: 'CONGE_SANS_SOLDE', label: 'Congé sans solde' },
  { value: 'AUTRE', label: 'Autre' }
];

const LeaveRequestForm: React.FC = () => {
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const { control, handleSubmit, formState: { errors } } = useForm<FormData>();

  const mutation = useMutation(
    (data: Partial<LeaveRequest>) => createLeaveRequest(data),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('leave-requests');
        navigate('/hr/leave-requests');
      }
    }
  );

  const onSubmit = (data: FormData) => {
    mutation.mutate({
      ...data,
      date_debut: data.date_debut.toISOString(),
      date_fin: data.date_fin.toISOString(),
      statut: 'EN_ATTENTE'
    });
  };

  return (
    <LocalizationProvider dateAdapter={AdapterDateFns} adapterLocale={fr}>
      <Box>
        <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
          <Typography variant="h5">
            Nouvelle Demande de Congé
          </Typography>
          <Button
            variant="outlined"
            onClick={() => navigate('/hr/leave-requests')}
          >
            Retour à la liste
          </Button>
        </Box>

        <Card>
          <CardContent>
            <form onSubmit={handleSubmit(onSubmit)}>
              <Grid container spacing={3}>
                <Grid item xs={12}>
                  <Controller
                    name="type_conge"
                    control={control}
                    defaultValue=""
                    rules={{ required: 'Ce champ est requis' }}
                    render={({ field }) => (
                      <TextField
                        {...field}
                        select
                        fullWidth
                        label="Type de congé"
                        error={!!errors.type_conge}
                        helperText={errors.type_conge?.message}
                      >
                        {TYPES_CONGE.map((option) => (
                          <MenuItem key={option.value} value={option.value}>
                            {option.label}
                          </MenuItem>
                        ))}
                      </TextField>
                    )}
                  />
                </Grid>

                <Grid item xs={12} md={6}>
                  <Controller
                    name="date_debut"
                    control={control}
                    rules={{ required: 'Ce champ est requis' }}
                    render={({ field }) => (
                      <DatePicker
                        label="Date de début"
                        value={field.value}
                        onChange={field.onChange}
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
                    rules={{ required: 'Ce champ est requis' }}
                    render={({ field }) => (
                      <DatePicker
                        label="Date de fin"
                        value={field.value}
                        onChange={field.onChange}
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
                    defaultValue=""
                    rules={{ required: 'Ce champ est requis' }}
                    render={({ field }) => (
                      <TextField
                        {...field}
                        fullWidth
                        multiline
                        rows={4}
                        label="Motif"
                        error={!!errors.motif}
                        helperText={errors.motif?.message}
                      />
                    )}
                  />
                </Grid>

                <Grid item xs={12}>
                  <Box display="flex" justifyContent="flex-end" gap={2}>
                    <Button
                      variant="outlined"
                      onClick={() => navigate('/hr/leave-requests')}
                    >
                      Annuler
                    </Button>
                    <Button
                      type="submit"
                      variant="contained"
                      color="primary"
                      disabled={mutation.isLoading}
                    >
                      {mutation.isLoading ? 'Envoi...' : 'Soumettre'}
                    </Button>
                  </Box>
                </Grid>
              </Grid>
            </form>
          </CardContent>
        </Card>
      </Box>
    </LocalizationProvider>
  );
};

export default LeaveRequestForm;
