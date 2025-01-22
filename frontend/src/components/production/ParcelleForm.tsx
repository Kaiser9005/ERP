import React from 'react';
import { useForm, Controller } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import * as yup from 'yup';
import {
  Card,
  CardContent,
  Grid,
  TextField,
  MenuItem,
  Button,
  Box,
  Alert
} from '@mui/material';
import { DatePicker } from '@mui/x-date-pickers';
import { useNavigate, useParams } from 'react-router-dom';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { productionService } from '../../services/production';
import { CultureType, ParcelleStatus, Parcelle } from '../../types/production';
import PageHeader from '../layout/PageHeader';
import { LoadingButton } from '@mui/lab';

type ParcelleFormData = Omit<Parcelle, 'id'>;

const schema = yup.object().shape({
  code: yup.string().required('Le code est requis'),
  culture_type: yup.string().oneOf(Object.values(CultureType)).required('Le type de culture est requis'),
  surface_hectares: yup.number()
    .required('La surface est requise')
    .positive('La surface doit être positive'),
  date_plantation: yup.string().required('La date de plantation est requise'),
  statut: yup.string().oneOf(Object.values(ParcelleStatus)).required('Le statut est requis'),
  responsable_id: yup.string().required('Le responsable est requis'),
  coordonnees_gps: yup.object({
    latitude: yup.number().required('La latitude est requise'),
    longitude: yup.number().required('La longitude est requise')
  }).required('Les coordonnées GPS sont requises'),
  metadata: yup.object().optional()
});

const ParcelleForm: React.FC = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const isEdit = Boolean(id);

  const { data: parcelle, isLoading: isLoadingParcelle } = useQuery({
    queryKey: ['parcelle', id],
    queryFn: () => productionService.getParcelle(id!),
    enabled: isEdit
  });

  const defaultValues: ParcelleFormData = {
    code: '',
    culture_type: CultureType.PALMIER,
    surface_hectares: 0,
    date_plantation: new Date().toISOString(),
    statut: ParcelleStatus.EN_PREPARATION,
    responsable_id: '',
    coordonnees_gps: {
      latitude: 0,
      longitude: 0
    },
    metadata: {}
  };

  const { control, handleSubmit, formState: { errors } } = useForm<ParcelleFormData>({
    resolver: yupResolver(schema),
    defaultValues: parcelle || defaultValues
  });

  const mutation = useMutation({
    mutationFn: (data: ParcelleFormData) => 
      isEdit ? productionService.updateParcelle(id!, data) : productionService.createParcelle(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['parcelles'] });
      navigate('/production');
    }
  });

  const onSubmit = (data: ParcelleFormData) => {
    mutation.mutate(data);
  };

  if (isEdit && isLoadingParcelle) {
    return <div>Chargement...</div>;
  }

  return (
    <>
      <PageHeader
        title={isEdit ? 'Modifier la Parcelle' : 'Nouvelle Parcelle'}
        subtitle={isEdit ? `Modification de ${parcelle?.code}` : 'Création d\'une nouvelle parcelle'}
      />

      <Card>
        <CardContent>
          {mutation.error && (
            <Alert severity="error" sx={{ mb: 2 }}>
              Une erreur est survenue
            </Alert>
          )}

          <form onSubmit={handleSubmit(onSubmit)}>
            <Grid container spacing={3}>
              <Grid item xs={12} md={6}>
                <Controller
                  name="code"
                  control={control}
                  render={({ field }) => (
                    <TextField
                      {...field}
                      label="Code"
                      fullWidth
                      error={!!errors.code}
                      helperText={errors.code?.message}
                    />
                  )}
                />
              </Grid>

              <Grid item xs={12} md={6}>
                <Controller
                  name="culture_type"
                  control={control}
                  render={({ field }) => (
                    <TextField
                      {...field}
                      select
                      label="Type de Culture"
                      fullWidth
                      error={!!errors.culture_type}
                      helperText={errors.culture_type?.message}
                    >
                      <MenuItem value={CultureType.PALMIER}>Palmier à huile</MenuItem>
                      <MenuItem value={CultureType.PAPAYE}>Papaye</MenuItem>
                    </TextField>
                  )}
                />
              </Grid>

              <Grid item xs={12} md={6}>
                <Controller
                  name="surface_hectares"
                  control={control}
                  render={({ field }) => (
                    <TextField
                      {...field}
                      label="Surface (hectares)"
                      type="number"
                      fullWidth
                      error={!!errors.surface_hectares}
                      helperText={errors.surface_hectares?.message}
                    />
                  )}
                />
              </Grid>

              <Grid item xs={12} md={6}>
                <Controller
                  name="date_plantation"
                  control={control}
                  render={({ field }) => (
                    <DatePicker
                      value={field.value ? new Date(field.value) : null}
                      onChange={(date) => field.onChange(date?.toISOString())}
                      label="Date de Plantation"
                      slotProps={{
                        textField: {
                          fullWidth: true,
                          error: !!errors.date_plantation,
                          helperText: errors.date_plantation?.message
                        }
                      }}
                    />
                  )}
                />
              </Grid>

              <Grid item xs={12} md={6}>
                <Controller
                  name="statut"
                  control={control}
                  render={({ field }) => (
                    <TextField
                      {...field}
                      select
                      label="Statut"
                      fullWidth
                      error={!!errors.statut}
                      helperText={errors.statut?.message}
                    >
                      <MenuItem value={ParcelleStatus.EN_PREPARATION}>En préparation</MenuItem>
                      <MenuItem value={ParcelleStatus.ACTIVE}>Active</MenuItem>
                      <MenuItem value={ParcelleStatus.EN_RECOLTE}>En récolte</MenuItem>
                      <MenuItem value={ParcelleStatus.EN_REPOS}>En repos</MenuItem>
                    </TextField>
                  )}
                />
              </Grid>

              <Grid item xs={12} md={6}>
                <Controller
                  name="responsable_id"
                  control={control}
                  render={({ field }) => (
                    <TextField
                      {...field}
                      label="Responsable"
                      fullWidth
                      error={!!errors.responsable_id}
                      helperText={errors.responsable_id?.message}
                    />
                  )}
                />
              </Grid>

              <Grid item xs={12} md={6}>
                <Controller
                  name="coordonnees_gps.latitude"
                  control={control}
                  render={({ field }) => (
                    <TextField
                      {...field}
                      label="Latitude"
                      type="number"
                      fullWidth
                      error={!!errors.coordonnees_gps?.latitude}
                      helperText={errors.coordonnees_gps?.latitude?.message}
                    />
                  )}
                />
              </Grid>

              <Grid item xs={12} md={6}>
                <Controller
                  name="coordonnees_gps.longitude"
                  control={control}
                  render={({ field }) => (
                    <TextField
                      {...field}
                      label="Longitude"
                      type="number"
                      fullWidth
                      error={!!errors.coordonnees_gps?.longitude}
                      helperText={errors.coordonnees_gps?.longitude?.message}
                    />
                  )}
                />
              </Grid>

              <Grid item xs={12}>
                <Box sx={{ display: 'flex', gap: 2, justifyContent: 'flex-end' }}>
                  <Button
                    variant="outlined"
                    onClick={() => navigate('/production')}
                  >
                    Annuler
                  </Button>
                  <LoadingButton
                    variant="contained"
                    type="submit"
                    loading={mutation.isPending}
                  >
                    {isEdit ? 'Modifier' : 'Créer'}
                  </LoadingButton>
                </Box>
              </Grid>
            </Grid>
          </form>
        </CardContent>
      </Card>
    </>
  );
};

export default ParcelleForm;
