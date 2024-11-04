import React from 'react';
import {
  Card,
  CardContent,
  Typography,
  List,
  ListItem,
  ListItemText,
  ListItemAvatar,
  Avatar,
  Chip,
  Box,
  IconButton
} from '@mui/material';
import { Assignment, Edit } from '@mui/icons-material';
import { useQuery } from 'react-query';
import { getRecentTasks } from '../../services/projects';
import { formatDistanceToNow } from 'date-fns';
import { fr } from 'date-fns/locale';

const TasksOverview: React.FC = () => {
  const { data: tasks } = useQuery('recent-tasks', getRecentTasks);

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

  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Tâches Récentes
        </Typography>

        <List>
          {tasks?.map((task) => (
            <ListItem
              key={task.id}
              secondaryAction={
                <IconButton edge="end" size="small">
                  <Edit />
                </IconButton>
              }
            >
              <ListItemAvatar>
                <Avatar>
                  <Assignment />
                </Avatar>
              </ListItemAvatar>
              <ListItemText
                primary={
                  <Box display="flex" alignItems="center" gap={1}>
                    {task.titre}
                    <Chip
                      size="small"
                      label={task.priorite}
                      color={getPriorityColor(task.priorite)}
                    />
                  </Box>
                }
                secondary={
                  <>
                    {task.projet.nom}
                    <br />
                    {formatDistanceToNow(new Date(task.date_fin_prevue), {
                      addSuffix: true,
                      locale: fr
                    })}
                  </>
                }
              />
            </ListItem>
          ))}
        </List>
      </CardContent>
    </Card>
  );
};

export default TasksOverview;