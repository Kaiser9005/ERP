import React, { useState, useEffect } from 'react';
import {
  Box,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  FormControlLabel,
  Switch,
  Button,
  Grid,
  Typography,
  Paper,
  IconButton,
  List,
  ListItem,
  Alert,
  CircularProgress
} from '@mui/material';
import { DateTimePicker } from '@mui/x-date-pickers/DateTimePicker';
import { Delete as DeleteIcon, Add as AddIcon } from '@mui/icons-material';
import { useNavigate, useParams } from 'react-router-dom';
import {
  TaskFormData,
  TaskStatus,
  TaskPriority,
  TaskCategory,
  TaskResourceBase,
  TaskDependencyBase,
  Task
} from '../../types/task';
import * as taskService from '../../services/tasks';

interface Resource {
  id: number;
  name: string;
  quantity_available: number;
  unit: string;
}

const initialFormData: TaskFormData = {
  title: '',
  description: '',
  status: TaskStatus.A_FAIRE,
  priority: TaskPriority.MOYENNE,
  category: TaskCategory.AUTRE,
  project_id: 0,
  weather_dependent: false,
  completion_percentage: 0,
  resources: [],
  dependencies: []
};

const TaskForm: React.FC = () => {
  const { projectId, taskId } = useParams<{ projectId: string; taskId?: string }>();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [resources, setResources] = useState<Resource[]>([]);
  const [tasks, setTasks] = useState<Task[]>([]);
  const [formData, setFormData] = useState<TaskFormData>({
    ...initialFormData,
    project_id: projectId ? parseInt(projectId) : 0
  });

  useEffect(() => {
    const fetchData = async () => {
      if (!projectId) return;
      
      try {
        setLoading(true);
        
        // Chargement des ressources disponibles
        const resourcesResponse = await fetch('/api/v1/resources');
        if (!resourcesResponse.ok) throw new Error('Erreur chargement ressources');
        const resourcesData = await resourcesResponse.json();
        setResources(resourcesData);

        // Chargement des tâches du projet pour les dépendances
        const tasksResponse = await fetch(`/api/v1/projects/${projectId}/tasks`);
        if (!tasksResponse.ok) throw new Error('Erreur chargement tâches');
        const tasksData = await tasksResponse.json();
        setTasks(tasksData.tasks);

        // Si mode édition, charger la tâche
        if (taskId) {
          const taskResponse = await fetch(`/api/v1/tasks/${taskId}`);
          if (!taskResponse.ok) throw new Error('Erreur chargement tâche');
          const taskData: Task = await taskResponse.json();
          
          // Conversion de Task vers TaskFormData
          const formTaskData: TaskFormData = {
            title: taskData.title,
            description: taskData.description,
            status: taskData.status,
            priority: taskData.priority,
            category: taskData.category,
            start_date: taskData.start_date,
            due_date: taskData.due_date,
            project_id: taskData.project_id,
            assigned_to: taskData.assigned_to,
            parcelle_id: taskData.parcelle_id,
            weather_dependent: taskData.weather_dependent,
            min_temperature: taskData.min_temperature,
            max_temperature: taskData.max_temperature,
            max_wind_speed: taskData.max_wind_speed,
            max_precipitation: taskData.max_precipitation,
            estimated_hours: taskData.estimated_hours,
            actual_hours: taskData.actual_hours,
            completion_percentage: taskData.completion_percentage,
            resources: taskData.resources.map(r => ({
              resource_id: r.resource_id,
              quantity_required: r.quantity_required,
              quantity_used: r.quantity_used
            })),
            dependencies: taskData.dependencies.map(d => ({
              dependent_on_id: d.dependent_on_id,
              dependency_type: d.dependency_type
            }))
          };
          
          setFormData(formTaskData);
        }

        setError(null);
      } catch (err) {
        setError("Erreur lors du chargement des données");
        console.error('Error fetching data:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [projectId, taskId]);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSelectChange = (e: any) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleDateChange = (name: string) => (date: Date | null) => {
    setFormData(prev => ({ ...prev, [name]: date?.toISOString() }));
  };

  const handleWeatherDependentChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { checked } = e.target;
    setFormData(prev => ({
      ...prev,
      weather_dependent: checked,
      min_temperature: checked ? prev.min_temperature : undefined,
      max_temperature: checked ? prev.max_temperature : undefined,
      max_wind_speed: checked ? prev.max_wind_speed : undefined,
      max_precipitation: checked ? prev.max_precipitation : undefined
    }));
  };

  const handleAddResource = () => {
    const newResource: TaskResourceBase = {
      resource_id: 0,
      quantity_required: 0,
      quantity_used: 0
    };
    
    setFormData(prev => ({
      ...prev,
      resources: [...prev.resources, newResource]
    }));
  };

  const handleResourceChange = (index: number, field: keyof TaskResourceBase, value: number) => {
    setFormData(prev => {
      const resources = [...prev.resources];
      resources[index] = { ...resources[index], [field]: value };
      return { ...prev, resources };
    });
  };

  const handleRemoveResource = (index: number) => {
    setFormData(prev => ({
      ...prev,
      resources: prev.resources.filter((_, i) => i !== index)
    }));
  };

  const handleAddDependency = () => {
    const newDependency: TaskDependencyBase = {
      dependent_on_id: 0,
      dependency_type: 'finish_to_start'
    };
    
    setFormData(prev => ({
      ...prev,
      dependencies: [...prev.dependencies, newDependency]
    }));
  };

  const handleDependencyChange = (index: number, field: keyof TaskDependencyBase, value: string | number) => {
    setFormData(prev => {
      const dependencies = [...prev.dependencies];
      dependencies[index] = { ...dependencies[index], [field]: value };
      return { ...prev, dependencies };
    });
  };

  const handleRemoveDependency = (index: number) => {
    setFormData(prev => ({
      ...prev,
      dependencies: prev.dependencies.filter((_, i) => i !== index)
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!projectId) return;

    try {
      setLoading(true);
      if (taskId) {
        await taskService.updateTask(parseInt(taskId), formData);
      } else {
        await taskService.createTask(formData);
      }
      navigate(`/projects/${projectId}/tasks`);
    } catch (err) {
      setError("Impossible de sauvegarder la tâche");
      console.error('Error saving task:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box component="form" onSubmit={handleSubmit} noValidate>
      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      <Paper sx={{ p: 3, mb: 3 }}>
        <Typography variant="h6" gutterBottom>
          {taskId ? 'Modifier la Tâche' : 'Nouvelle Tâche'}
        </Typography>
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <TextField
              required
              fullWidth
              name="title"
              label="Titre"
              value={formData.title}
              onChange={handleInputChange}
            />
          </Grid>
          <Grid item xs={12}>
            <TextField
              fullWidth
              multiline
              rows={4}
              name="description"
              label="Description"
              value={formData.description}
              onChange={handleInputChange}
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <FormControl fullWidth>
              <InputLabel>Statut</InputLabel>
              <Select
                name="status"
                value={formData.status}
                onChange={handleSelectChange}
                label="Statut"
              >
                {Object.values(TaskStatus).map(status => (
                  <MenuItem key={status} value={status}>
                    {status}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>
          <Grid item xs={12} sm={6}>
            <FormControl fullWidth>
              <InputLabel>Priorité</InputLabel>
              <Select
                name="priority"
                value={formData.priority}
                onChange={handleSelectChange}
                label="Priorité"
              >
                {Object.values(TaskPriority).map(priority => (
                  <MenuItem key={priority} value={priority}>
                    {priority}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>
          <Grid item xs={12} sm={6}>
            <FormControl fullWidth>
              <InputLabel>Catégorie</InputLabel>
              <Select
                name="category"
                value={formData.category}
                onChange={handleSelectChange}
                label="Catégorie"
              >
                {Object.values(TaskCategory).map(category => (
                  <MenuItem key={category} value={category}>
                    {category}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              type="number"
              name="completion_percentage"
              label="Progression (%)"
              value={formData.completion_percentage}
              onChange={handleInputChange}
              inputProps={{ min: 0, max: 100 }}
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <DateTimePicker
              label="Date de début"
              value={formData.start_date ? new Date(formData.start_date) : null}
              onChange={handleDateChange('start_date')}
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <DateTimePicker
              label="Date d'échéance"
              value={formData.due_date ? new Date(formData.due_date) : null}
              onChange={handleDateChange('due_date')}
            />
          </Grid>
        </Grid>
      </Paper>

      <Paper sx={{ p: 3, mb: 3 }}>
        <Typography variant="h6" gutterBottom>
          Conditions Météorologiques
        </Typography>
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <FormControlLabel
              control={
                <Switch
                  checked={formData.weather_dependent}
                  onChange={handleWeatherDependentChange}
                  name="weather_dependent"
                />
              }
              label="Tâche dépendante de la météo"
            />
          </Grid>
          {formData.weather_dependent && (
            <>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  type="number"
                  name="min_temperature"
                  label="Température minimale (°C)"
                  value={formData.min_temperature}
                  onChange={handleInputChange}
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  type="number"
                  name="max_temperature"
                  label="Température maximale (°C)"
                  value={formData.max_temperature}
                  onChange={handleInputChange}
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  type="number"
                  name="max_wind_speed"
                  label="Vitesse du vent maximale (km/h)"
                  value={formData.max_wind_speed}
                  onChange={handleInputChange}
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  type="number"
                  name="max_precipitation"
                  label="Précipitations maximales (mm)"
                  value={formData.max_precipitation}
                  onChange={handleInputChange}
                />
              </Grid>
            </>
          )}
        </Grid>
      </Paper>

      <Paper sx={{ p: 3, mb: 3 }}>
        <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
          <Typography variant="h6">Ressources</Typography>
          <Button
            startIcon={<AddIcon />}
            onClick={handleAddResource}
            variant="outlined"
          >
            Ajouter une ressource
          </Button>
        </Box>
        <List>
          {formData.resources.map((resource, index) => (
            <ListItem key={index} divider>
              <Grid container spacing={2} alignItems="center">
                <Grid item xs={5}>
                  <FormControl fullWidth>
                    <InputLabel>Ressource</InputLabel>
                    <Select
                      value={resource.resource_id}
                      onChange={(e) => handleResourceChange(index, 'resource_id', Number(e.target.value))}
                      label="Ressource"
                    >
                      {resources.map(r => (
                        <MenuItem key={r.id} value={r.id}>
                          {r.name} ({r.quantity_available} {r.unit} disponibles)
                        </MenuItem>
                      ))}
                    </Select>
                  </FormControl>
                </Grid>
                <Grid item xs={5}>
                  <TextField
                    fullWidth
                    type="number"
                    label="Quantité requise"
                    value={resource.quantity_required}
                    onChange={(e) => handleResourceChange(index, 'quantity_required', Number(e.target.value))}
                    inputProps={{ min: 0 }}
                  />
                </Grid>
                <Grid item xs={2}>
                  <IconButton
                    onClick={() => handleRemoveResource(index)}
                    color="error"
                  >
                    <DeleteIcon />
                  </IconButton>
                </Grid>
              </Grid>
            </ListItem>
          ))}
        </List>
      </Paper>

      <Paper sx={{ p: 3, mb: 3 }}>
        <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
          <Typography variant="h6">Dépendances</Typography>
          <Button
            startIcon={<AddIcon />}
            onClick={handleAddDependency}
            variant="outlined"
          >
            Ajouter une dépendance
          </Button>
        </Box>
        <List>
          {formData.dependencies.map((dependency, index) => (
            <ListItem key={index} divider>
              <Grid container spacing={2} alignItems="center">
                <Grid item xs={5}>
                  <FormControl fullWidth>
                    <InputLabel>Tâche requise</InputLabel>
                    <Select
                      value={dependency.dependent_on_id}
                      onChange={(e) => handleDependencyChange(index, 'dependent_on_id', Number(e.target.value))}
                      label="Tâche requise"
                    >
                      {tasks
                        .filter(t => t.id !== parseInt(taskId || '0'))
                        .map(task => (
                          <MenuItem key={task.id} value={task.id}>
                            {task.title}
                          </MenuItem>
                        ))
                      }
                    </Select>
                  </FormControl>
                </Grid>
                <Grid item xs={5}>
                  <FormControl fullWidth>
                    <InputLabel>Type de dépendance</InputLabel>
                    <Select
                      value={dependency.dependency_type}
                      onChange={(e) => handleDependencyChange(index, 'dependency_type', e.target.value)}
                      label="Type de dépendance"
                    >
                      <MenuItem value="finish_to_start">Fin pour début</MenuItem>
                      <MenuItem value="start_to_start">Début pour début</MenuItem>
                      <MenuItem value="finish_to_finish">Fin pour fin</MenuItem>
                    </Select>
                  </FormControl>
                </Grid>
                <Grid item xs={2}>
                  <IconButton
                    onClick={() => handleRemoveDependency(index)}
                    color="error"
                  >
                    <DeleteIcon />
                  </IconButton>
                </Grid>
              </Grid>
            </ListItem>
          ))}
        </List>
      </Paper>

      <Box display="flex" gap={2} justifyContent="flex-end">
        <Button
          variant="outlined"
          onClick={() => navigate(`/projects/${projectId}/tasks`)}
        >
          Annuler
        </Button>
        <Button
          type="submit"
          variant="contained"
          color="primary"
          disabled={loading}
        >
          {loading ? <CircularProgress size={24} /> : 'Enregistrer'}
        </Button>
      </Box>
    </Box>
  );
};

export default TaskForm;
