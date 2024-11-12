import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Chip,
  IconButton,
  Button,
  CircularProgress,
  Alert,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Pagination,
  LinearProgress
} from '@mui/material';
import {
  Edit as EditIcon,
  Delete as DeleteIcon,
  Add as AddIcon,
  WbSunny as WeatherIcon
} from '@mui/icons-material';
import { useNavigate, useParams } from 'react-router-dom';
import { TaskStatus, TaskPriority, TaskCategory, Task } from '../../types/task';
import * as taskService from '../../services/tasks';

const TaskList: React.FC = () => {
  const { projectId } = useParams<{ projectId: string }>();
  const navigate = useNavigate();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [statusFilter, setStatusFilter] = useState<TaskStatus | 'ALL'>('ALL');
  const [categoryFilter, setCategoryFilter] = useState<TaskCategory | 'ALL'>('ALL');

  const fetchTasks = async () => {
    if (!projectId) return;
    
    try {
      setLoading(true);
      const data = await taskService.getTasks(
        parseInt(projectId),
        page,
        statusFilter === 'ALL' ? undefined : statusFilter,
        categoryFilter === 'ALL' ? undefined : categoryFilter
      );
      
      setTasks(data.tasks);
      setTotalPages(data.total_pages);
      setError(null);
    } catch (err) {
      setError("Impossible de charger les tâches");
      console.error('Error fetching tasks:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTasks();
  }, [projectId, page, statusFilter, categoryFilter]);

  const handleStatusChange = (event: any) => {
    setStatusFilter(event.target.value);
    setPage(1);
  };

  const handleCategoryChange = (event: any) => {
    setCategoryFilter(event.target.value);
    setPage(1);
  };

  const handlePageChange = (event: any, value: number) => {
    setPage(value);
  };

  const handleEdit = (taskId: number) => {
    navigate(`/projects/${projectId}/tasks/${taskId}/edit`);
  };

  const handleDelete = async (taskId: number) => {
    if (!window.confirm('Êtes-vous sûr de vouloir supprimer cette tâche ?')) return;

    try {
      await taskService.deleteTask(taskId);
      fetchTasks();
    } catch (err) {
      setError("Impossible de supprimer la tâche");
      console.error('Error deleting task:', err);
    }
  };

  const handleCreate = () => {
    navigate(`/projects/${projectId}/tasks/create`);
  };

  const handleViewWeather = (taskId: number) => {
    navigate(`/projects/${projectId}/tasks/${taskId}/weather`);
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return <Alert severity="error">{error}</Alert>;
  }

  const getStatusColor = (status: TaskStatus) => {
    switch (status) {
      case 'A_FAIRE': return 'default';
      case 'EN_COURS': return 'primary';
      case 'EN_ATTENTE': return 'warning';
      case 'TERMINEE': return 'success';
      case 'ANNULEE': return 'error';
      default: return 'default';
    }
  };

  const getPriorityColor = (priority: TaskPriority) => {
    switch (priority) {
      case 'BASSE': return '#4caf50';
      case 'MOYENNE': return '#ff9800';
      case 'HAUTE': return '#f44336';
      case 'CRITIQUE': return '#d32f2f';
      default: return '#000000';
    }
  };

  return (
    <Box>
      <Box mb={3} display="flex" justifyContent="space-between" alignItems="center">
        <Typography variant="h5">Tâches du Projet</Typography>
        <Button
          variant="contained"
          color="primary"
          startIcon={<AddIcon />}
          onClick={handleCreate}
        >
          Nouvelle Tâche
        </Button>
      </Box>

      <Box mb={3} display="flex" gap={2}>
        <FormControl variant="outlined" size="small" style={{ minWidth: 200 }}>
          <InputLabel>Statut</InputLabel>
          <Select
            value={statusFilter}
            onChange={handleStatusChange}
            label="Statut"
          >
            <MenuItem value="ALL">Tous</MenuItem>
            <MenuItem value="A_FAIRE">À faire</MenuItem>
            <MenuItem value="EN_COURS">En cours</MenuItem>
            <MenuItem value="EN_ATTENTE">En attente</MenuItem>
            <MenuItem value="TERMINEE">Terminée</MenuItem>
            <MenuItem value="ANNULEE">Annulée</MenuItem>
          </Select>
        </FormControl>

        <FormControl variant="outlined" size="small" style={{ minWidth: 200 }}>
          <InputLabel>Catégorie</InputLabel>
          <Select
            value={categoryFilter}
            onChange={handleCategoryChange}
            label="Catégorie"
          >
            <MenuItem value="ALL">Toutes</MenuItem>
            <MenuItem value="PRODUCTION">Production</MenuItem>
            <MenuItem value="MAINTENANCE">Maintenance</MenuItem>
            <MenuItem value="RECOLTE">Récolte</MenuItem>
            <MenuItem value="PLANTATION">Plantation</MenuItem>
            <MenuItem value="IRRIGATION">Irrigation</MenuItem>
            <MenuItem value="TRAITEMENT">Traitement</MenuItem>
            <MenuItem value="AUTRE">Autre</MenuItem>
          </Select>
        </FormControl>
      </Box>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Titre</TableCell>
              <TableCell>Statut</TableCell>
              <TableCell>Priorité</TableCell>
              <TableCell>Catégorie</TableCell>
              <TableCell>Date début</TableCell>
              <TableCell>Date fin</TableCell>
              <TableCell>Progression</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {tasks.map((task) => (
              <TableRow key={task.id}>
                <TableCell>{task.title}</TableCell>
                <TableCell>
                  <Chip
                    label={task.status}
                    color={getStatusColor(task.status)}
                    size="small"
                  />
                </TableCell>
                <TableCell>
                  <Typography style={{ color: getPriorityColor(task.priority) }}>
                    {task.priority}
                  </Typography>
                </TableCell>
                <TableCell>{task.category}</TableCell>
                <TableCell>
                  {task.start_date && new Date(task.start_date).toLocaleDateString()}
                </TableCell>
                <TableCell>
                  {task.due_date && new Date(task.due_date).toLocaleDateString()}
                </TableCell>
                <TableCell>
                  <Box display="flex" alignItems="center">
                    <Box width="100%" mr={1}>
                      <LinearProgress
                        variant="determinate"
                        value={task.completion_percentage}
                      />
                    </Box>
                    <Box minWidth={35}>
                      <Typography variant="body2" color="textSecondary">
                        {task.completion_percentage}%
                      </Typography>
                    </Box>
                  </Box>
                </TableCell>
                <TableCell>
                  <IconButton
                    size="small"
                    onClick={() => handleEdit(task.id)}
                    title="Modifier"
                  >
                    <EditIcon />
                  </IconButton>
                  <IconButton
                    size="small"
                    onClick={() => handleDelete(task.id)}
                    title="Supprimer"
                  >
                    <DeleteIcon />
                  </IconButton>
                  {task.weather_dependent && (
                    <IconButton
                      size="small"
                      onClick={() => handleViewWeather(task.id)}
                      title="Conditions météo"
                    >
                      <WeatherIcon />
                    </IconButton>
                  )}
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      <Box mt={2} display="flex" justifyContent="center">
        <Pagination
          count={totalPages}
          page={page}
          onChange={handlePageChange}
          color="primary"
        />
      </Box>
    </Box>
  );
};

export default TaskList;
