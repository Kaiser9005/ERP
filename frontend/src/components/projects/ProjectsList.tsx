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
  TextField,
  InputAdornment,
  IconButton,
  LinearProgress
} from '@mui/material';
import { Edit, Search, Visibility } from '@mui/icons-material';
import { useQuery } from 'react-query';
import { getProjects } from '../../services/projects';
import { useNavigate } from 'react-router-dom';
import { format } from 'date-fns';
import { fr } from 'date-fns/locale';

const ProjectsList: React.FC = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const navigate = useNavigate();
  const { data: projects } = useQuery('projects', getProjects);

  const filteredProjects = projects?.filter(project =>
    project.nom.toLowerCase().includes(searchTerm.toLowerCase()) ||
    project.code.toLowerCase().includes(searchTerm.toLowerCase())
  );

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

  const calculateProgress = (project: any) => {
    const completedTasks = project.taches?.filter((t: any) => t.statut === 'TERMINE').length || 0;
    const totalTasks = project.taches?.length || 1;
    return (completedTasks / totalTasks) * 100;
  };

  return (
    <Card>
      <CardContent>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
          <Typography variant="h6">Projets</Typography>
          <TextField
            size="small"
            placeholder="Rechercher..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <Search />
                </InputAdornment>
              ),
            }}
          />
        </Box>

        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Code</TableCell>
              <TableCell>Projet</TableCell>
              <TableCell>Responsable</TableCell>
              <TableCell>Échéance</TableCell>
              <TableCell>Progression</TableCell>
              <TableCell>Statut</TableCell>
              <TableCell align="right">Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {filteredProjects?.map((project) => (
              <TableRow key={project.id}>
                <TableCell>{project.code}</TableCell>
                <TableCell>
                  <Typography variant="subtitle2">
                    {project.nom}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    {project.description}
                  </Typography>
                </TableCell>
                <TableCell>{project.responsable.nom}</TableCell>
                <TableCell>
                  {format(new Date(project.date_fin_prevue), 'PP', { locale: fr })}
                </TableCell>
                <TableCell>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <LinearProgress
                      variant="determinate"
                      value={calculateProgress(project)}
                      sx={{ flexGrow: 1 }}
                    />
                    <Typography variant="body2">
                      {Math.round(calculateProgress(project))}%
                    </Typography>
                  </Box>
                </TableCell>
                <TableCell>
                  <Chip
                    size="small"
                    label={project.statut}
                    color={getStatusColor(project.statut)}
                  />
                </TableCell>
                <TableCell align="right">
                  <IconButton
                    size="small"
                    onClick={() => navigate(`/projects/${project.id}`)}
                  >
                    <Visibility />
                  </IconButton>
                  <IconButton
                    size="small"
                    onClick={() => navigate(`/projects/${project.id}/edit`)}
                  >
                    <Edit />
                  </IconButton>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </CardContent>
    </Card>
  );
};

export default ProjectsList;