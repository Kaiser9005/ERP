import React from 'react';
import { useForm, Controller } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import * as yup from 'yup';
import {
  Card,
  CardContent,
  Grid,
  TextField,
  Button,
  Box,
  Alert,
  MenuItem
} from '@mui/material';
import { DatePicker } from '@mui/x-date-pickers';
import { useNavigate, useParams } from 'react-router-dom';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { createProject, updateProject, getProject } from '../../services/projects';
import PageHeader from '../layout/PageHeader';
import { LoadingButton } from '@mui/lab';
import { ProjectStatus } from '../../types/project';
import type { ProjectBase, Project } from '../../types/project';

interface Objectif {
  description: string;
  criteres_succes?: string;
  date_cible?: string;
  statut?: string;
}

interface Risque {
  description: string;
  impact: 'FAIBLE' | 'MOYEN' | 'ELEVE';
  probabilite: 'FAIBLE' | 'MOYENNE' | 'ELEVEE';
  mitigation?: string;
  statut?: string;
}

interface ProjectFormData {
  code: string;
  nom: string;
  description?: string;
  date_debut: Date;
  date_fin_prevue: Date;
  date_fin_reelle?: string;
  statut: ProjectStatus;
  budget: number;
  responsable_id: string;
  objectifs: Objectif[];
  risques: Risque[];
}

const defaultValues: ProjectFormData = {
  code: '',
  nom: '',
  description: '',
  date_debut: new Date(),
  date_fin_prevue: new Date(),
  budget: 0,
  responsable_id: '',
  statut: ProjectStatus.PLANIFIE,
  objectifs: [],
  risques: []
};

const objectifSchema = yup.object({
  description: yup.string().required(),
  criteres_succes: yup.string().optional(),
  date_cible: yup.string().optional(),
  statut: yup.string().optional()
});

const risqueSchema = yup.object({
  description: yup.string().required(),
  impact: yup.string().oneOf(['FAIBLE', 'MOYEN', 'ELEVE']).required(),
  probabilite: yup.string().oneOf(['FAIBLE', 'MOYENNE', 'ELEVEE']).required(),
  mitigation: yup.string().optional(),
  statut: yup.string().optional()
});

const schema = yup.object({
  code: yup.string().required('Le code est requis'),
  nom: yup.string().required('Le nom est requis'),
  description: yup.string().optional(),
  date_debut: yup.date().required('La date de début est requise'),
  date_fin_prevue: yup.date()
    .required('La date de fin est requise')
    .min(yup.ref('date_debut'), 'La date de fin doit être après la date de début'),
  date_fin_reelle: yup.string().optional(),
  budget: yup.number()
    .transform((value) => (isNaN(value) ? undefined : value))
    .positive('Le budget doit être positif')
    .required('Le budget est requis'),
  responsable_id: yup.string().required('Le responsable est requis'),
  statut: yup.string().oneOf(Object.values(ProjectStatus)).required('Le statut est requis'),
  objectifs: yup.array().of(objectifSchema).required().default([]),
  risques: yup.array().of(risqueSchema).required().default([])
}) as yup.ObjectSchema<ProjectFormData>;

const ProjectForm: React.FC = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const isEdit = Boolean(id);

  const { data: project, isLoading: isLoadingProject } = useQuery({
    queryKey: ['project', id],
    queryFn: () => getProject(id!),
    enabled: isEdit
  });

  const { control, handleSubmit, formState: { errors } } = useForm<ProjectFormData>({
    resolver: yupResolver(schema),
    defaultValues: project ? {
      ...project,
      date_debut: new Date(project.date_debut),
      date_fin_prevue: new Date(project.date_fin_prevue),
      budget: project.budget ?? 0,
      objectifs: project.objectifs ?? [],
      risques: project.risques ?? []
    } : defaultValues
  });

  const mutation = useMutation({
    mutationFn: (data: ProjectFormData) => {
      const projectData: ProjectBase = {
        ...data,
        date_debut: data.date_debut.toISOString().split('T')[0],
        date_fin_prevue: data.date_fin_prevue.toISOString().split('T')[0]
      };
      return isEdit ? updateProject(id!, projectData) : createProject(projectData);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['projects'] });
      navigate('/projects');
    }
  });

  const onSubmit = (data: ProjectFormData) => {
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
          {mutation.error instanceof Error && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {mutation.error.message || 'Une erreur est survenue'}
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
                      {Object.values(ProjectStatus).map((status) => (
                        <MenuItem key={status} value={status}>
                          {status}
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

export default ProjectForm;
