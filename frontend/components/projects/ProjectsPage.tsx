import React from 'react';
import { Grid } from '@mui/material';
import PageHeader from '../layout/PageHeader';
import ProjectStats from './ProjectStats';
import ProjectsList from './ProjectsList';
import ProjectTimeline from './ProjectTimeline';
import TasksOverview from './TasksOverview';
import { Add } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';

const ProjectsPage: React.FC = () => {
  const navigate = useNavigate();

  return (
    <>
      <PageHeader
        title="Projets"
        subtitle="Gestion des projets et des tâches"
        action={{
          label: "Nouveau Projet",
          onClick: () => navigate('/projects/new'),
          icon: <Add />
        }}
      />

      <Grid container spacing={3}>
        {/* Statistiques des projets */}
        <Grid item xs={12}>
          <ProjectStats />
        </Grid>

        {/* Liste des projets */}
        <Grid item xs={12} lg={8}>
          <ProjectsList />
        </Grid>

        {/* Aperçu des tâches */}
        <Grid item xs={12} lg={4}>
          <TasksOverview />
        </Grid>

        {/* Timeline des projets */}
        <Grid item xs={12}>
          <ProjectTimeline />
        </Grid>
      </Grid>
    </>
  );
};

export default ProjectsPage;