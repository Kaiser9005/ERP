import React from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  TextField,
  MenuItem,
  Grid,
  Box,
} from '@mui/material';
import { useForm, Controller } from 'react-hook-form';
import { LoadingButton } from '@mui/lab';

import {
  IoTSensorFormData,
  SensorType,
  SENSOR_TYPE_LABELS,
  DEFAULT_THRESHOLDS,
  SENSOR_UNITS,
} from '../../types/iot';
import { useCreateSensor } from '../../services/iot';

interface AddSensorDialogProps {
  open: boolean;
  onClose: () => void;
  parcelleId: string;
}

export const AddSensorDialog: React.FC<AddSensorDialogProps> = ({
  open,
  onClose,
  parcelleId,
}) => {
  const { control, handleSubmit, watch, reset } = useForm<IoTSensorFormData>({
    defaultValues: {
      code: '',
      type: SensorType.TEMPERATURE_SOL,
      parcelle_id: parcelleId,
      intervalle_lecture: 300, // 5 minutes par défaut
      config: {},
      seuils_alerte: {},
    },
  });

  const createSensor = useCreateSensor();
  const selectedType = watch('type');

  const onSubmit = async (data: IoTSensorFormData) => {
    try {
      // Ajout des seuils par défaut pour le type de capteur
      data.seuils_alerte = DEFAULT_THRESHOLDS[data.type];
      
      await createSensor.mutateAsync(data);
      reset();
      onClose();
    } catch (error) {
      console.error('Erreur lors de la création du capteur:', error);
    }
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <DialogTitle>Ajouter un nouveau capteur</DialogTitle>
      
      <form onSubmit={handleSubmit(onSubmit)}>
        <DialogContent>
          <Grid container spacing={2}>
            <Grid item xs={12}>
              <Controller
                name="code"
                control={control}
                rules={{ required: 'Le code est requis' }}
                render={({ field, fieldState: { error } }) => (
                  <TextField
                    {...field}
                    label="Code du capteur"
                    fullWidth
                    error={!!error}
                    helperText={error?.message}
                  />
                )}
              />
            </Grid>

            <Grid item xs={12}>
              <Controller
                name="type"
                control={control}
                rules={{ required: 'Le type est requis' }}
                render={({ field, fieldState: { error } }) => (
                  <TextField
                    {...field}
                    select
                    label="Type de capteur"
                    fullWidth
                    error={!!error}
                    helperText={error?.message}
                  >
                    {Object.entries(SENSOR_TYPE_LABELS).map(([value, label]) => (
                      <MenuItem key={value} value={value}>
                        {label} ({SENSOR_UNITS[value as SensorType]})
                      </MenuItem>
                    ))}
                  </TextField>
                )}
              />
            </Grid>

            <Grid item xs={12}>
              <Controller
                name="intervalle_lecture"
                control={control}
                rules={{
                  required: "L'intervalle de lecture est requis",
                  min: {
                    value: 60,
                    message: 'Minimum 60 secondes',
                  },
                  max: {
                    value: 3600,
                    message: 'Maximum 3600 secondes (1 heure)',
                  },
                }}
                render={({ field, fieldState: { error } }) => (
                  <TextField
                    {...field}
                    type="number"
                    label="Intervalle de lecture (secondes)"
                    fullWidth
                    error={!!error}
                    helperText={error?.message}
                  />
                )}
              />
            </Grid>

            <Grid item xs={12} sm={6}>
              <Controller
                name="latitude"
                control={control}
                render={({ field, fieldState: { error } }) => (
                  <TextField
                    {...field}
                    type="number"
                    label="Latitude"
                    fullWidth
                    error={!!error}
                    helperText={error?.message}
                  />
                )}
              />
            </Grid>

            <Grid item xs={12} sm={6}>
              <Controller
                name="longitude"
                control={control}
                render={({ field, fieldState: { error } }) => (
                  <TextField
                    {...field}
                    type="number"
                    label="Longitude"
                    fullWidth
                    error={!!error}
                    helperText={error?.message}
                  />
                )}
              />
            </Grid>

            <Grid item xs={12} sm={6}>
              <Controller
                name="fabricant"
                control={control}
                render={({ field, fieldState: { error } }) => (
                  <TextField
                    {...field}
                    label="Fabricant"
                    fullWidth
                    error={!!error}
                    helperText={error?.message}
                  />
                )}
              />
            </Grid>

            <Grid item xs={12} sm={6}>
              <Controller
                name="modele"
                control={control}
                render={({ field, fieldState: { error } }) => (
                  <TextField
                    {...field}
                    label="Modèle"
                    fullWidth
                    error={!!error}
                    helperText={error?.message}
                  />
                )}
              />
            </Grid>
          </Grid>

          <Box mt={2}>
            <Grid container spacing={2}>
              {Object.entries(DEFAULT_THRESHOLDS[selectedType] || {}).map(([key, value]) => (
                <Grid item xs={12} sm={6} key={key}>
                  <TextField
                    label={`Seuil ${key}`}
                    type="number"
                    value={value}
                    disabled
                    fullWidth
                    helperText={`Seuil ${key} par défaut pour ce type de capteur`}
                  />
                </Grid>
              ))}
            </Grid>
          </Box>
        </DialogContent>

        <DialogActions>
          <Button onClick={onClose}>Annuler</Button>
          <LoadingButton
            type="submit"
            variant="contained"
            loading={createSensor.isPending}
          >
            Ajouter
          </LoadingButton>
        </DialogActions>
      </form>
    </Dialog>
  );
};
