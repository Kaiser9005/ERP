import React, { useState } from 'react';
import {
  Card,
  CardContent,
  Typography,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  Chip,
  Box,
  IconButton,
  Button
} from '@mui/material';
import { Edit, Add } from '@mui/icons-material';
import { useQuery } from 'react-query';
import { getProjectTasks } from '../../services/projects';
import { format } from 'date-fns';
import { fr } from 'date-fns/locale';
import TaskForm from './TaskForm';

interface TaskListProps {
  projectId: string;
}

const TaskList: React.FC<TaskListProps> = ({ projectId }) => {
  const [taskFormOpen, setTaskFormOpen] = useState(false);
  const { data: tasks } = useQuery(['project-tasks', projectId], () => getProjectTasks(projectId));

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'CRITIQUE':
        return 'error';
      case 'HAUTE':
        return 'warning';
      case 'MOYENNE':
        return 'info';
      default:
        return 'default';
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'TERMINE':
        return 'success';
      case 'EN_COURS':
        return 'info';
      case 'BLOQUE':
        return 'error';
      default:
        return 'default';
    }
  };

  return (
    <Card>
      <CardContent>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
          <Typography variant="h6">
            Tâches
          </Typography>
          <Button
            variant="contained"
            startIcon={<Add />}
            onClick={() => setTaskFormOpen(true)}
          >
            Nouvelle Tâche
          </Button>
        </Box>

        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Titre</TableCell>
              <TableCell>Priorité</TableCell>
              <TableCell>Assigné à</TableCell>
              <TableCell>Échéance</TableCell>
              <TableCell>Statut</TableCell>
              <TableCell align="right">Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {tasks?.map((task) => (
              <TableRow key={task.id}>
                <TableCell>{task.titre}</TableCell>
                <TableCell>
                  <Chip
                    size="small"
                    label={task.priorite}
                    color={getPriorityColor(task.priorite)}
                  />
                </TableCell>
                <TableCell>
                  {task.assignee ? `${task.assignee.prenom} ${task.assignee.nom}` : '-'}
                </TableCell>
                <TableCell>
                  {format(new Date(task.date_fin_prevue), 'Pp', { locale: fr })}
                </TableCell>
                <TableCell>
                  <Chip
                    size="small"
                    label={task.statut}
                    color={getStatusColor(task.statut)}
                  />
                </TableCell>
                <TableCell align="right">
                  <IconButton size="small">
                    <Edit />
                  </IconButton>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>

        <TaskForm
          open={taskFormOpen}
          onClose={() => setTaskFormOpen(false)}
          projectId={projectId}
        />
      </CardContent>
    </Card>
  );
};

export default TaskList;