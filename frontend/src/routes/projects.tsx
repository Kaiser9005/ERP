import React from 'react';
import { Routes, Route, useParams } from 'react-router-dom';
import ProjectStats from '../components/projects/ProjectStats';
import TaskList from '../components/projects/TaskList';
import TaskForm from '../components/projects/TaskForm';
import DétailsMétéoTâche from '../components/projects/DétailsMétéoTâche';

const TaskListWrapper: React.FC = () => {
  const { projectId } = useParams<{ projectId: string }>();
  if (!projectId) return null;
  return <TaskList projectId={projectId} />;
};

const ProjectRoutes: React.FC = () => {
  return (
    <Routes>
      <Route path="/" element={<ProjectStats />} />
      <Route path="/:projectId/tasks" element={<TaskListWrapper />} />
      <Route path="/:projectId/tasks/new" element={<TaskForm />} />
      <Route path="/:projectId/tasks/:id" element={<TaskForm />} />
      <Route path="/:projectId/tasks/:id/weather" element={<DétailsMétéoTâche />} />
    </Routes>
  );
};

export default ProjectRoutes;
