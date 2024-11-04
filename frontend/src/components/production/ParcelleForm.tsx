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
  Typography,
  Alert
} from '@mui/material';
import { DatePicker } from '@mui/x-date-pickers';
import { useNavigate, useParams } from 'react-router-dom';
import { useMutation, useQuery, useQueryClient } from 'react-query';
import { createParcelle, updateParcelle, getParcelle } from '../../services/production';
import PageHeader from '../layout/PageHeader';
import { LoadingButton } from '@mui/lab';

const schema = yup.object({
  code: yup.string().required('Le code est requis'),
  culture_type: yup.string().required('Le type de culture est requis'),
  surface_hectares: yup.number()
    .required('La surface est requise')
    .positive('La surface doit être positive'),
  date_plantation: yup.date().required('La date de plantation est requise'),
  statut: yup.string().required('Le statut est requis'),
  responsable_id: yup.string().required('Le responsable est requis')
}).required();

const ParcelleForm: React.FC = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const isEdit = Boolean(id);

  const { data: parcelle, isLoading: isLoadingParcelle } = useQuery(
    ['parcelle', id],
    () => getParcelle(id!),
    { enabled: isEdit }
  );

  const { control, handleSubmit, formState: { errors } } = useForm({
    resolver: yupResolver(schema),
    defaultValues: parcelle || {
      code: '',
      culture_type: '',
      surface_hectares: '',
      date_plantation: null,
      statut: 'EN_PREPARATION',
      responsable_id: ''
    }
  });

  const mutation = useMutation(
    (data: any) => isEdit ? updateParcelle(id!, data) : createParcelle(data),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('parcelles');
        navigate('/production');
      }
    }
  );

  const onSubmit = (data: any) => {
    mutation.mutate(data);
  };

  if (isEdit && isLoadingParcelle) {
    return <div>Chargement...</div>;
  }

  return (
    <>
      <PageHeader
        title={isEdit ? 'Modifier la Parcelle' : 'Nouvelle Parcelle'}
        subtitle={isEdit ? `Modification de ${parcelle?.code}` : 'Création d'une nouvelle parcelle'}
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
                      <MenuItem value="PALMIER">Palmier à huile</MenuItem>
                      <MenuItem value="PAPAYE">Papaye</MenuItem>
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
                      {...field}
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
                      <MenuItem value="EN_PREPARATION">En préparation</MenuItem>
                      <MenuItem value="ACTIVE">Active</MenuItem>
                      <MenuItem value="EN_REPOS">En repos</MenuItem>
                    </TextField>
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
                    loading={mutation.isLoading}
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