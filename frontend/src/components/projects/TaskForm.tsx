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
import { DateTimePicker } from '@mui/x-date-pickers';
import { useMutation, useQueryClient } from 'react-query';
import { createTask } from '../../services/projects';
import { LoadingButton } from '@mui/lab';

const schema = yup.object({
  projet_id: yup.string().required('Le projet est requis'),
  titre: yup.string().required('Le titre est requis'),
  description: yup.string(),
  priorite: yup.string().required('La priorité est requise'),
  date_fin_prevue: yup.date().required('La date de fin est requise'),
  assignee_id: yup.string(),
  temps_estime: yup.number().positive('Le temps estimé doit être positif')
}).required();

interface TaskFormProps {
  open: boolean;
  onClose: () => void;
  projectId?: string;
}

const TaskForm: React.FC<TaskFormProps> = ({
  open,
  onClose,
  projectId
}) => {
  const queryClient = useQueryClient();

  const { control, handleSubmit, formState: { errors } } = useForm({
    resolver: yupResolver(schema),
    defaultValues: {
      projet_id: projectId || '',
      titre: '',
      description: '',
      priorite: 'MOYENNE',
      date_fin_prevue: null,
      assignee_id: '',
      temps_estime: ''
    }
  });

  const mutation = useMutation(createTask, {
    onSuccess: () => {
      queryClient.invalidateQueries(['project-tasks', projectId]);
      onClose();
    }
  });

  const onSubmit = (data: any) => {
    mutation.mutate(data);
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="md" fullWidth>
      <form onSubmit={handleSubmit(onSubmit)}>
        <DialogTitle>Nouvelle Tâche</DialogTitle>
        
        <DialogContent>
          <Grid container spacing={3} sx={{ mt: 1 }}>
            <Grid item xs={12}>
              <Controller
                name="titre"
                control={control}
                render={({ field }) => (
                  <TextField
                    {...field}
                    label="Titre"
                    fullWidth
                    error={!!errors.titre}
                    helperText={errors.titre?.message}
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
                name="priorite"
                control={control}
                render={({ field }) => (
                  <TextField
                    {...field}
                    select
                    label="Priorité"
                    fullWidth
                    error={!!errors.priorite}
                    helperText={errors.priorite?.message}
                  >
                    <MenuItem value="BASSE">Basse</MenuItem>
                    <MenuItem value="MOYENNE">Moyenne</MenuItem>
                    <MenuItem value="HAUTE">Haute</MenuItem>
                    <MenuItem value="CRITIQUE">Critique</MenuItem>
                  </TextField>
                )}
              />
            </Grid>

            <Grid item xs={12} md={6}>
              <Controller
                name="date_fin_prevue"
                control={control}
                render={({ field }) => (
                  <DateTimePicker
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
                name="temps_estime"
                control={control}
                render={({ field }) => (
                  <TextField
                    {...field}
                    label="Temps Estimé (heures)"
                    type="number"
                    fullWidth
                    error={!!errors.temps_estime}
                    helperText={errors.temps_estime?.message}
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
            Créer
          </LoadingButton>
        </DialogActions>
      </form>
    </Dialog>
  );
};

export default TaskForm;