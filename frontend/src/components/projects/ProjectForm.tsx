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
import { createProject, updateProject, getProject } from '../../services/projects';
import PageHeader from '../layout/PageHeader';
import { LoadingButton } from '@mui/lab';

const schema = yup.object({
  code: yup.string().required('Le code est requis'),
  nom: yup.string().required('Le nom est requis'),
  description: yup.string(),
  date_debut: yup.date().required('La date de début est requise'),
  date_fin_prevue: yup.date()
    .required('La date de fin est requise')
    .min(yup.ref('date_debut'), 'La date de fin doit être après la date de début'),
  budget: yup.number()
    .required('Le budget est requis')
    .positive('Le budget doit être positif'),
  responsable_id: yup.string().required('Le responsable est requis')
}).required();

const ProjectForm: React.FC = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const isEdit = Boolean(id);

  const { data: project, isLoading: isLoadingProject } = useQuery(
    ['project', id],
    () => getProject(id!),
    { enabled: isEdit }
  );

  const { control, handleSubmit, formState: { errors } } = useForm({
    resolver: yupResolver(schema),
    defaultValues: project || {
      code: '',
      nom: '',
      description: '',
      date_debut: null,
      date_fin_prevue: null,
      budget: '',
      responsable_id: '',
      objectifs: [],
      risques: []
    }
  });

  const mutation = useMutation(
    (data: any) => isEdit ? updateProject(id!, data) : createProject(data),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('projects');
        navigate('/projects');
      }
    }
  );

  const onSubmit = (data: any) => {
    mutation.mutate(data);
  };

  if (isEdit && isLoadingProject) {
    return <div>Chargement...</div>;
  }

  return (
    <>
      <PageHeader
        title={isEdit ? 'Modifier le Projet' : 'Nouveau Projet'}
        subtitle={isEdit ? `Modification de ${project?.nom}` : 'Création d\'un nouveau projet'}
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
                  name="nom"
                  control={control}
                  render={({ field }) => (
                    <TextField
                      {...field}
                      label="Nom"
                      fullWidth
                      error={!!errors.nom}
                      helperText={errors.nom?.message}
                    />
                  )}
                />
              </Grid>

              <Grid item xs={12}>
                <Controller
                  name="description"
                  control={control}
                  render={({ field }) => (
                    <TextField
                      {...field}
                      label="Description"
                      multiline
                      rows={4}
                      fullWidth
                      error={!!errors.description}
                      helperText={errors.description?.message}
                    />
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
                  name="date_fin_prevue"
                  control={control}
                  render={({ field }) => (
                    <DatePicker
                      {...field}
                      label="Date de Fin Prévue"
                      slotProps={{
                        textField: {
                          fullWidth: true,
                          error: !!errors.date_fin_prevue,
                          helperText: errors.date_fin_prevue?.message
                        }
                      }}
                    />
                  )}
                />
              </Grid>

              <Grid item xs={12} md={6}>
                <Controller
                  name="budget"
                  control={control}
                  render={({ field }) => (
                    <TextField
                      {...field}
                      label="Budget"
                      type="number"
                      fullWidth
                      error={!!errors.budget}
                      helperText={errors.budget?.message}
                    />
                  )}
                />
              </Grid>

              <Grid item xs={12}>
                <Box sx={{ display: 'flex', gap: 2, justifyContent: 'flex-end' }}>
                  <Button
                    variant="outlined"
                    onClick={() => navigate('/projects')}
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

export default ProjectForm;