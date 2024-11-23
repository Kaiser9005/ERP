import React from 'react';
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
  LinearProgress,
  SelectChangeEvent
} from '@mui/material';
import {
  Edit as EditIcon,
  Delete as DeleteIcon,
  Add as AddIcon,
  WbSunny as WeatherIcon
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { TaskStatus, TaskPriority, TaskCategory, Task } from '../../types/task';
import * as taskService from '../../services/tasks';

interface TaskListProps {
  projectId: string;
}

const TaskList: React.FC<TaskListProps> = ({ projectId }) => {
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const [page, setPage] = React.useState(1);
  const [statusFilter, setStatusFilter] = React.useState<TaskStatus | 'ALL'>('ALL');
  const [categoryFilter, setCategoryFilter] = React.useState<TaskCategory | 'ALL'>('ALL');

  const { data, isLoading, error } = useQuery({
    queryKey: ['tasks', projectId, page, statusFilter, categoryFilter],
    queryFn: () => taskService.getTasks(
      parseInt(projectId),
      page,
      statusFilter === 'ALL' ? undefined : statusFilter,
      categoryFilter === 'ALL' ? undefined : categoryFilter
    )
  });

  const deleteMutation = useMutation({
    mutationFn: taskService.deleteTask,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks', projectId] });
    }
  });

  const handleStatusChange = (event: SelectChangeEvent<TaskStatus | 'ALL'>) => {
    setStatusFilter(event.target.value as TaskStatus | 'ALL');
    setPage(1);
  };

  const handleCategoryChange = (event: SelectChangeEvent<TaskCategory | 'ALL'>) => {
    setCategoryFilter(event.target.value as TaskCategory | 'ALL');
    setPage(1);
  };

  const handlePageChange = (event: React.ChangeEvent<unknown>, value: number) => {
    setPage(value);
  };

  const handleEdit = (taskId: number) => {
    navigate(`/projects/${projectId}/tasks/${taskId}/edit`);
  };

  const handleDelete = async (taskId: number) => {
    if (!window.confirm('Êtes-vous sûr de vouloir supprimer cette tâche ?')) return;
    deleteMutation.mutate(taskId);
  };

  const handleCreate = () => {
    navigate(`/projects/${projectId}/tasks/create`);
  };

  const handleViewWeather = (taskId: number) => {
    navigate(`/projects/${projectId}/tasks/${taskId}/weather`);
  };

  if (isLoading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Alert severity="error">
        {error instanceof Error ? error.message : "Impossible de charger les tâches"}
      </Alert>
    );
  }

  const getStatusColor = (status: TaskStatus): "default" | "primary" | "warning" | "success" | "error" => {
    switch (status) {
      case TaskStatus.A_FAIRE: return 'default';
      case TaskStatus.EN_COURS: return 'primary';
      case TaskStatus.EN_ATTENTE: return 'warning';
      case TaskStatus.TERMINEE: return 'success';
      case TaskStatus.ANNULEE: return 'error';
      default: return 'default';
    }
  };

  const getPriorityColor = (priority: TaskPriority): string => {
    switch (priority) {
      case TaskPriority.BASSE: return '#4caf50';
      case TaskPriority.MOYENNE: return '#ff9800';
      case TaskPriority.HAUTE: return '#f44336';
      case TaskPriority.CRITIQUE: return '#d32f2f';
      default: return '#000000';
    }
  };

  if (deleteMutation.error) {
    return (
      <Alert severity="error">
        {deleteMutation.error instanceof Error 
          ? deleteMutation.error.message 
          : "Erreur lors de la suppression"}
      </Alert>
    );
  }

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
            {Object.values(TaskStatus).map(status => (
              <MenuItem key={status} value={status}>{status}</MenuItem>
            ))}
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
            {Object.values(TaskCategory).map(category => (
              <MenuItem key={category} value={category}>{category}</MenuItem>
            ))}
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
            {data?.tasks.map((task) => (
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
                    disabled={deleteMutation.isPending}
                  >
                    <EditIcon />
                  </IconButton>
                  <IconButton
                    size="small"
                    onClick={() => handleDelete(task.id)}
                    title="Supprimer"
                    disabled={deleteMutation.isPending}
                  >
                    <DeleteIcon />
                  </IconButton>
                  {task.weather_dependent && (
                    <IconButton
                      size="small"
                      onClick={() => handleViewWeather(task.id)}
                      title="Conditions météo"
                      disabled={deleteMutation.isPending}
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
          count={data?.total_pages || 1}
          page={page}
          onChange={handlePageChange}
          color="primary"
        />
      </Box>
    </Box>
  );
};

export default TaskList;
