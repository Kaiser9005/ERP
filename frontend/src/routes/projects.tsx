import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import TaskList from '../components/projects/TaskList';
import TaskForm from '../components/projects/TaskForm';
import TaskWeatherDetails from '../components/projects/TaskWeatherDetails';

const ProjectRoutes: React.FC = () => {
  return (
    <Routes>
      {/* Liste des tâches du projet */}
      <Route 
        path=":projectId/tasks" 
        element={<TaskList />} 
      />

      {/* Création d'une nouvelle tâche */}
      <Route 
        path=":projectId/tasks/create" 
        element={<TaskForm />} 
      />

      {/* Édition d'une tâche existante */}
      <Route 
        path=":projectId/tasks/:taskId/edit" 
        element={<TaskForm />} 
      />

      {/* Détails météo d'une tâche */}
      <Route 
        path=":projectId/tasks/:taskId/weather" 
        element={<TaskWeatherDetails />} 
      />

      {/* Redirection par défaut vers la liste des tâches */}
      <Route 
        path=":projectId" 
        element={<Navigate to="tasks" replace />} 
      />
    </Routes>
  );
};

export default ProjectRoutes;
