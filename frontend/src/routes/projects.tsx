import React from 'react';
import { Routes, Route } from 'react-router-dom';
import ProjectStats from '../components/projects/ProjectStats';
import TaskList from '../components/projects/TaskList';
import TaskForm from '../components/projects/TaskForm';
import TaskWeatherDetails from '../components/projects/TaskWeatherDetails';

const ProjectRoutes: React.FC = () => {
  return (
    <Routes>
      <Route path="/" element={<ProjectStats />} />
      <Route path="/tasks" element={<TaskList />} />
      <Route path="/tasks/new" element={<TaskForm />} />
      <Route path="/tasks/:id" element={<TaskForm />} />
      <Route path="/tasks/:id/weather" element={<TaskWeatherDetails />} />
    </Routes>
  );
};

export default ProjectRoutes;
