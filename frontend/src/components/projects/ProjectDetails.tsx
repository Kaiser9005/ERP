import React from 'react';
import {
  Card,
  CardContent,
  Grid,
  Typography,
  Chip,
  Box,
  LinearProgress
} from '@mui/material';
import { useParams, useNavigate } from 'react-router-dom';
import { useQuery } from 'react-query';
import { getProject } from '../../services/projects';
import PageHeader from '../layout/PageHeader';
import { Edit } from '@mui/icons-material';
import { format } from 'date-fns';
import { fr } from 'date-fns/locale';
import TaskList from './TaskList';

const ProjectDetails: React.FC = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { data: project } = useQuery(['project', id], () => getProject(id!));

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'EN_COURS':
        return 'success';
      case 'EN_PAUSE':
        return 'warning';
      case 'TERMINE':
        return 'info';
      case 'ANNULE':
        return 'error';
      default:
        return 'default';
    }
  };

  const calculateProgress = () => {
    if (!project?.taches?.length) return 0;
    const completedTasks = project.taches.filter(t => t.statut === 'TERMINE').length;
    return (completedTasks / project.taches.length) * 100;
  };

  return (
    <>
      <PageHeader
        title={`Projet ${project?.code}`}
        subtitle={project?.nom}
        action={{
          label: "Modifier",
          onClick: () => navigate(`/projects/${id}/edit`),
          icon: <Edit />
        }}
      />

      <Grid container spacing={3}>
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Informations Générales
              </Typography>

              <Box sx={{ '& > *': { mb: 2 } }}>
                <Box>
                  <Typography color="text.secondary" gutterBottom>
                    Statut
                  </Typography>
                  <Chip
                    label={project?.statut}
                    color={getStatusColor(project?.statut || '')}
                  />
                </Box>

                <Box>
                  <Typography color="text.secondary" gutterBottom>
                    Budget
                  </Typography>
                  <Typography variant="h6">
                    {new Intl.NumberFormat('fr-FR', {
                      style: 'currency',
                      currency: 'XAF'
                    }).format(project?.budget || 0)}
                  </Typography>
                </Box>

                <Box>
                  <Typography color="text.secondary" gutterBottom>
                    Dates
                  </Typography>
                  <Typography variant="body2">
                    Début: {project?.date_debut &&
                      format(new Date(project.date_debut), 'PP', { locale: fr })}
                  </Typography>
                  <Typography variant="body2">
                    Fin prévue: {project?.date_fin_prevue &&
                      format(new Date(project.date_fin_prevue), 'PP', { locale: fr })}
                  </Typography>
                </Box>

                <Box>
                  <Typography color="text.secondary" gutterBottom>
                    Progression
                  </Typography>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <LinearProgress
                      variant="determinate"
                      value={calculateProgress()}
                      sx={{ flexGrow: 1 }}
                    />
                    <Typography variant="body2">
                      {Math.round(calculateProgress())}%
                    </Typography>
                  </Box>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={8}>
          <TaskList projectId={id!} />
        </Grid>
      </Grid>
    </>
  );
};

export default ProjectDetails;