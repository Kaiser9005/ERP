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
  MenuItem,
  FormControlLabel,
  Switch
} from '@mui/material';
import { DatePicker } from '@mui/x-date-pickers';
import { useNavigate, useParams } from 'react-router-dom';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { createTask, updateTask, getTask } from '../../services/tasks';
import PageHeader from '../layout/PageHeader';
import { LoadingButton } from '@mui/lab';
import { TaskStatus, TaskPriority, TaskCategory, Task, TaskFormData } from '../../types/task';

interface FormValues {
  title: string;
  description?: string;
  status: TaskStatus;
  priority: TaskPriority;
  category: TaskCategory;
  start_date?: Date;
  due_date: Date;  // Required
  project_id: number;
  assigned_to?: number;
  parcelle_id?: number;
  weather_dependent: boolean;
  min_temperature?: number;
  max_temperature?: number;
  max_wind_speed?: number;
  max_precipitation?: number;
  estimated_hours?: number;
  actual_hours?: number;
  completion_percentage: number;
  resources: Array<{
    resource_id: number;
    quantity_required: number;
    quantity_used: number;
  }>;
  dependencies: Array<{
    dependent_on_id: number;
    dependency_type: string;
  }>;
}

const schema = yup.object().shape({
  title: yup.string().required('Le titre est requis'),
  description: yup.string().optional(),
  status: yup.string().oneOf(Object.values(TaskStatus)).required('Le statut est requis'),
  priority: yup.string().oneOf(Object.values(TaskPriority)).required('La priorité est requise'),
  category: yup.string().oneOf(Object.values(TaskCategory)).required('La catégorie est requise'),
  start_date: yup.date().optional(),
  due_date: yup.date()
    .required('La date de fin est requise')
    .test('date-after-start', 'La date de fin doit être après la date de début', function(value) {
      const start = this.parent.start_date;
      if (!start || !value) return true;
      return value > start;
    }),
  project_id: yup.number().required(),
  assigned_to: yup.number().optional(),
  parcelle_id: yup.number().optional(),
  weather_dependent: yup.boolean().required(),
  min_temperature: yup.number().optional().when('weather_dependent', {
    is: true,
    then: (schema) => schema.required('La température minimale est requise')
  }),
  max_temperature: yup.number().optional().when('weather_dependent', {
    is: true,
    then: (schema) => schema.required('La température maximale est requise')
  }),
  max_wind_speed: yup.number().optional().when('weather_dependent', {
    is: true,
    then: (schema) => schema.required('La vitesse du vent maximale est requise')
  }),
  max_precipitation: yup.number().optional().when('weather_dependent', {
    is: true,
    then: (schema) => schema.required('Les précipitations maximales sont requises')
  }),
  estimated_hours: yup.number().optional(),
  actual_hours: yup.number().optional(),
  completion_percentage: yup.number().min(0).max(100).required(),
  resources: yup.array().of(
    yup.object({
      resource_id: yup.number().required(),
      quantity_required: yup.number().required(),
      quantity_used: yup.number().required()
    })
  ).default([]),
  dependencies: yup.array().of(
    yup.object({
      dependent_on_id: yup.number().required(),
      dependency_type: yup.string().required()
    })
  ).default([])
}) satisfies yup.ObjectSchema<FormValues>;

const TaskForm: React.FC = () => {
  const { projectId, taskId } = useParams<{ projectId: string; taskId: string }>();
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const isEdit = Boolean(taskId);

  const { data: task } = useQuery({
    queryKey: ['task', taskId],
    queryFn: () => getTask(parseInt(taskId!)),
    enabled: isEdit
  });

  const defaultValues: FormValues = {
    title: '',
    description: '',
    status: TaskStatus.A_FAIRE,
    priority: TaskPriority.MOYENNE,
    category: TaskCategory.PRODUCTION,
    project_id: parseInt(projectId!),
    due_date: new Date(),  // Default to today
    weather_dependent: false,
    completion_percentage: 0,
    resources: [],
    dependencies: []
  };

  const { control, handleSubmit, watch, formState: { errors } } = useForm<FormValues>({
    resolver: yupResolver(schema),
    defaultValues: task ? {
      ...task,
      start_date: task.start_date ? new Date(task.start_date) : undefined,
      due_date: task.due_date ? new Date(task.due_date) : new Date(),
      resources: task.resources || [],
      dependencies: task.dependencies || []
    } : defaultValues
  });

  const weatherDependent = watch('weather_dependent');

  const mutation = useMutation({
    mutationFn: (data: FormValues) => {
      const formattedData: TaskFormData = {
        ...data,
        start_date: data.start_date?.toISOString().split('T')[0],
        due_date: data.due_date.toISOString().split('T')[0]
      };
      return isEdit ? updateTask(parseInt(taskId!), formattedData) : createTask(formattedData);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks', projectId] });
      navigate(`/projects/${projectId}/tasks`);
    }
  });

  const onSubmit = (data: FormValues) => {
    mutation.mutate(data);
  };

  return (
    <>
      <PageHeader
        title={isEdit ? 'Modifier la Tâche' : 'Nouvelle Tâche'}
        subtitle={isEdit ? `Modification de ${task?.title}` : 'Création d\'une nouvelle tâche'}
        data-testid="page-title"
      />

      <Card>
        <CardContent>
          {mutation.error instanceof Error && (
            <Alert severity="error" sx={{ mb: 2 }} data-testid="error-message">
              {mutation.error.message || 'Une erreur est survenue'}
            </Alert>
          )}

          <form onSubmit={handleSubmit(onSubmit)} data-testid="task-form">
            <Grid container spacing={3}>
              <Grid item xs={12}>
                <Controller
                  name="title"
                  control={control}
                  render={({ field }) => (
                    <TextField
                      {...field}
                      label="Titre"
                      fullWidth
                      error={!!errors.title}
                      helperText={errors.title?.message}
                      data-testid="task-title-input"
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
                      data-testid="task-description-input"
                    />
                  )}
                />
              </Grid>

              <Grid item xs={12} md={4}>
                <Controller
                  name="status"
                  control={control}
                  render={({ field }) => (
                    <TextField
                      {...field}
                      select
                      label="Statut"
                      fullWidth
                      error={!!errors.status}
                      helperText={errors.status?.message}
                      data-testid="task-status-select"
                    >
                      {Object.values(TaskStatus).map((status) => (
                        <MenuItem key={status} value={status} data-testid={`status-option-${status}`}>
                          {status}
                        </MenuItem>
                      ))}
                    </TextField>
                  )}
                />
              </Grid>

              <Grid item xs={12} md={4}>
                <Controller
                  name="priority"
                  control={control}
                  render={({ field }) => (
                    <TextField
                      {...field}
                      select
                      label="Priorité"
                      fullWidth
                      error={!!errors.priority}
                      helperText={errors.priority?.message}
                      data-testid="task-priority-select"
                    >
                      {Object.values(TaskPriority).map((priority) => (
                        <MenuItem key={priority} value={priority} data-testid={`priority-option-${priority}`}>
                          {priority}
                        </MenuItem>
                      ))}
                    </TextField>
                  )}
                />
              </Grid>

```typescriptreact
              <Grid item xs={12} md={4}>
                <Controller
                  name="category"
                  control={control}
                  render={({ field }) => (
                    <TextField
                      {...field}
                      select
                      label="Catégorie"
                      fullWidth
                      error={!!errors.category}
                      helperText={errors.category?.message}
                      data-testid="task-category-select"
                    >
                      {Object.values(TaskCategory).map((category) => (
                        <MenuItem key={category} value={category} data-testid={`category-option-${category}`}>
                          {category}
                        </MenuItem>
                      ))}
                    </TextField>
                  )}
                />
              </Grid>

              <Grid item xs={12} md={6}>
                <Controller
                  name="start_date"
                  control={control}
                  render={({ field }) => (
                    <DatePicker
                      {...field}
                      label="Date de début"
                      render={(params) => (
                        <TextField
                          {...params}
                          fullWidth
                          error={!!errors.start_date}
                          helperText={errors.start_date?.message}
                          data-testid="start-date-input"
                        />
                      )}
                    />
                  )}
                />
              </Grid>

              <Grid item xs={12} md={6}>
                <Controller
                  name="due_date"
                  control={control}
                  render={({ field }) => (
                    <DatePicker
                      {...field}
                      label="Date de fin"
                      renderInput={(params) => (
                        <TextField
                          {...params}
                          fullWidth
                          error={!!errors.due_date}
                          helperText={errors.due_date?.message}
                          data-testid="due-date-input"
                        />
                      )}
                    />
                  )}
                />
              </Grid>
```

              <Grid item xs={12}>
                <Controller
                  name="weather_dependent"
                  control={control}
                  render={({ field }) => (
                    <FormControlLabel
                      control={
                        <Switch
                          {...field}
                          checked={field.value}
                          data-testid="weather-dependent-checkbox"
                        />
                      }
                      label="Tâche dépendante de la météo"
                    />
                  )}
                />
              </Grid>

              {weatherDependent && (
                <>
                  <Grid item xs={12} md={3}>
                    <Controller
                      name="min_temperature"
                      control={control}
                      render={({ field }) => (
                        <TextField
                          {...field}
                          type="number"
                          label="Température minimale (°C)"
                          fullWidth
                          error={!!errors.min_temperature}
                          helperText={errors.min_temperature?.message}
                          data-testid="min-temperature-input"
                        />
                      )}
                    />
                  </Grid>

                  <Grid item xs={12} md={3}>
                    <Controller
                      name="max_temperature"
                      control={control}
                      render={({ field }) => (
                        <TextField
                          {...field}
                          type="number"
                          label="Température maximale (°C)"
                          fullWidth
                          error={!!errors.max_temperature}
                          helperText={errors.max_temperature?.message}
                          data-testid="max-temperature-input"
                        />
                      )}
                    />
                  </Grid>

                  <Grid item xs={12} md={3}>
                    <Controller
                      name="max_wind_speed"
                      control={control}
                      render={({ field }) => (
                        <TextField
                          {...field}
                          type="number"
                          label="Vitesse du vent maximale (km/h)"
                          fullWidth
                          error={!!errors.max_wind_speed}
                          helperText={errors.max_wind_speed?.message}
                          data-testid="max-wind-speed-input"
                        />
                      )}
                    />
                  </Grid>

                  <Grid item xs={12} md={3}>
                    <Controller
                      name="max_precipitation"
                      control={control}
                      render={({ field }) => (
                        <TextField
                          {...field}
                          type="number"
                          label="Précipitations maximales (mm)"
                          fullWidth
                          error={!!errors.max_precipitation}
                          helperText={errors.max_precipitation?.message}
                          data-testid="max-precipitation-input"
                        />
                      )}
                    />
                  </Grid>
                </>
              )}

              <Grid item xs={12} md={6}>
                <Controller
                  name="estimated_hours"
                  control={control}
                  render={({ field }) => (
                    <TextField
                      {...field}
                      type="number"
                      label="Heures estimées"
                      fullWidth
                      error={!!errors.estimated_hours}
                      helperText={errors.estimated_hours?.message}
                      data-testid="estimated-hours-input"
                    />
                  )}
                />
              </Grid>

              <Grid item xs={12} md={6}>
                <Controller
                  name="completion_percentage"
                  control={control}
                  render={({ field }) => (
                    <TextField
                      {...field}
                      type="number"
                      label="Progression (%)"
                      fullWidth
                      inputProps={{ min: 0, max: 100 }}
                      error={!!errors.completion_percentage}
                      helperText={errors.completion_percentage?.message}
                      data-testid="completion-percentage-input"
                    />
                  )}
                />
              </Grid>

              <Grid item xs={12}>
                <Box sx={{ display: 'flex', gap: 2, justifyContent: 'flex-end' }}>
                  <Button
                    variant="outlined"
                    onClick={() => navigate(`/projects/${projectId}/tasks`)}
                    data-testid="cancel-button"
                  >
                    Annuler
                  </Button>
                  <LoadingButton
                    variant="contained"
                    type="submit"
                    loading={mutation.isPending}
                    data-testid="submit-button"
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

export default TaskForm;
