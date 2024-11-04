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
import { createRecolte } from '../../services/production';
import { LoadingButton } from '@mui/lab';

const schema = yup.object({
  parcelle_id: yup.string().required('La parcelle est requise'),
  date_recolte: yup.date().required('La date est requise'),
  quantite_kg: yup.number()
    .required('La quantité est requise')
    .positive('La quantité doit être positive'),
  qualite: yup.string().required('La qualité est requise'),
  equipe_recolte: yup.array().of(yup.string()).min(1, 'Au moins un membre d\'équipe est requis'),
  conditions_meteo: yup.object({
    temperature: yup.number(),
    humidite: yup.number(),
    precipitation: yup.boolean()
  })
}).required();

interface RecolteFormProps {
  open: boolean;
  onClose: () => void;
  parcelleId?: string;
}

const RecolteForm: React.FC<RecolteFormProps> = ({
  open,
  onClose,
  parcelleId
}) => {
  const queryClient = useQueryClient();

  const { control, handleSubmit, formState: { errors } } = useForm({
    resolver: yupResolver(schema),
    defaultValues: {
      parcelle_id: parcelleId || '',
      date_recolte: null,
      quantite_kg: '',
      qualite: '',
      equipe_recolte: [],
      conditions_meteo: {
        temperature: '',
        humidite: '',
        precipitation: false
      }
    }
  });

  const mutation = useMutation(createRecolte, {
    onSuccess: () => {
      queryClient.invalidateQueries(['recoltes', parcelleId]);
      onClose();
    }
  });

  const onSubmit = (data: any) => {
    mutation.mutate(data);
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="md" fullWidth>
      <form onSubmit={handleSubmit(onSubmit)}>
        <DialogTitle>Nouvelle Récolte</DialogTitle>
        
        <DialogContent>
          <Grid container spacing={3} sx={{ mt: 1 }}>
            <Grid item xs={12} md={6}>
              <Controller
                name="date_recolte"
                control={control}
                render={({ field }) => (
                  <DatePicker
                    {...field}
                    label="Date de Récolte"
                    slotProps={{
                      textField: {
                        fullWidth: true,
                        error: !!errors.date_recolte,
                        helperText: errors.date_recolte?.message
                      }
                    }}
                  />
                )}
              />
            </Grid>

            <Grid item xs={12} md={6}>
              <Controller
                name="quantite_kg"
                control={control}
                render={({ field }) => (
                  <TextField
                    {...field}
                    label="Quantité (kg)"
                    type="number"
                    fullWidth
                    error={!!errors.quantite_kg}
                    helperText={errors.quantite_kg?.message}
                  />
                )}
              />
            </Grid>

            <Grid item xs={12} md={6}>
              <Controller
                name="qualite"
                control={control}
                render={({ field }) => (
                  <TextField
                    {...field}
                    select
                    label="Qualité"
                    fullWidth
                    error={!!errors.qualite}
                    helperText={errors.qualite?.message}
                  >
                    <MenuItem value="A">A - Premium</MenuItem>
                    <MenuItem value="B">B - Standard</MenuItem>
                    <MenuItem value="C">C - Basse qualité</MenuItem>
                  </TextField>
                )}
              />
            </Grid>

            <Grid item xs={12} md={6}>
              <Controller
                name="conditions_meteo.temperature"
                control={control}
                render={({ field }) => (
                  <TextField
                    {...field}
                    label="Température (°C)"
                    type="number"
                    fullWidth
                  />
                )}
              />
            </Grid>

            <Grid item xs={12} md={6}>
              <Controller
                name="conditions_meteo.humidite"
                control={control}
                render={({ field }) => (
                  <TextField
                    {...field}
                    label="Humidité (%)"
                    type="number"
                    fullWidth
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
            Enregistrer
          </LoadingButton>
        </DialogActions>
      </form>
    </Dialog>
  );
};

export default RecolteForm;