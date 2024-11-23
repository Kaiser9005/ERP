import React from 'react';
import {
  Card,
  CardContent,
  Typography,
  Box,
  TextField,
  Button,
  MenuItem,
  Grid,
  Alert
} from '@mui/material';
import { useForm, Controller } from 'react-hook-form';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { useNavigate } from 'react-router-dom';
import { createLeave } from '../../services/hr';
import { queryKeys } from '../../config/queryClient';
import { LeaveType } from '../../types/hr';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import fr from 'date-fns/locale/fr';
import { isBefore, isWeekend } from 'date-fns';
import { LeaveFormInputData } from './types/formTypes';

const TYPES_CONGE: { value: LeaveType; label: string }[] = [
  { value: 'conge_paye', label: 'Congé payé' },
  { value: 'maladie', label: 'Congé maladie' },
  { value: 'formation', label: 'Formation' },
  { value: 'autre', label: 'Autre' }
];

const LeaveRequestForm: React.FC = () => {
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const { control, handleSubmit, watch, formState: { errors } } = useForm<LeaveFormInputData>();
  const dateDebut = watch('dateDebut');

  const mutation = useMutation({
    mutationFn: (data: LeaveFormInputData) => createLeave({
      type: data.type,
      dateDebut: data.dateDebut.toISOString(),
      dateFin: data.dateFin.toISOString(),
      motif: data.motif,
      statut: 'en_attente'
    }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.hr.leaves() });
      navigate('/hr/leaves');
    }
  });

  const validateDateFin = (dateFin: Date) => {
    if (!dateDebut) return true;
    if (isBefore(dateFin, dateDebut)) {
      return "La date de fin doit être après la date de début";
    }
    return true;
  };

  const validateDateDebut = (date: Date) => {
    if (isWeekend(date)) {
      return "La date de début ne peut pas être un weekend";
    }
    if (isBefore(date, new Date())) {
      return "La date de début doit être dans le futur";
    }
    return true;
  };

  const onSubmit = (data: LeaveFormInputData) => {
    mutation.mutate(data);
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
            onClick={() => navigate('/hr/leaves')}
          >
            Retour à la liste
          </Button>
        </Box>

        {mutation.isError && (
          <Alert severity="error" sx={{ mb: 3 }}>
            Une erreur est survenue lors de la soumission de la demande
          </Alert>
        )}

        <Card>
          <CardContent>
            <form onSubmit={handleSubmit(onSubmit)}>
              <Grid container spacing={3}>
                <Grid item xs={12}>
                  <Controller
                    name="type"
                    control={control}
                    defaultValue={TYPES_CONGE[0].value}
                    rules={{ required: 'Ce champ est requis' }}
                    render={({ field }) => (
                      <TextField
                        {...field}
                        select
                        fullWidth
                        label="Type de congé"
                        error={!!errors.type}
                        helperText={errors.type?.message}
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
                    name="dateDebut"
                    control={control}
                    rules={{ 
                      required: 'Ce champ est requis',
                      validate: validateDateDebut
                    }}
                    render={({ field }) => (
                      <DatePicker
                        label="Date de début"
                        value={field.value}
                        onChange={field.onChange}
                        slotProps={{
                          textField: {
                            fullWidth: true,
                            error: !!errors.dateDebut,
                            helperText: errors.dateDebut?.message
                          }
                        }}
                      />
                    )}
                  />
                </Grid>

                <Grid item xs={12} md={6}>
                  <Controller
                    name="dateFin"
                    control={control}
                    rules={{ 
                      required: 'Ce champ est requis',
                      validate: validateDateFin
                    }}
                    render={({ field }) => (
                      <DatePicker
                        label="Date de fin"
                        value={field.value}
                        onChange={field.onChange}
                        minDate={dateDebut}
                        slotProps={{
                          textField: {
                            fullWidth: true,
                            error: !!errors.dateFin,
                            helperText: errors.dateFin?.message
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
                    rules={{ 
                      required: 'Ce champ est requis',
                      minLength: {
                        value: 10,
                        message: 'Le motif doit contenir au moins 10 caractères'
                      }
                    }}
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
                      onClick={() => navigate('/hr/leaves')}
                    >
                      Annuler
                    </Button>
                    <Button
                      type="submit"
                      variant="contained"
                      color="primary"
                      disabled={mutation.isPending}
                    >
                      {mutation.isPending ? 'Envoi...' : 'Soumettre'}
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
