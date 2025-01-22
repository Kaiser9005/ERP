import { RouteObject } from 'react-router-dom';
import ProjectsPage from '../components/projects/ProjectsPage';
import ProjectForm from '../components/projects/ProjectForm';
import ProjectDetails from '../components/projects/ProjectDetails';

export const projectRoutes: RouteObject[] = [
  {
    path: 'projects',
    children: [
      {
        index: true,
        element: <ProjectsPage />
      },
      {
        path: 'new',
        element: <ProjectForm />
      },
      {
        path: ':id',
        element: <ProjectDetails />
      },
      {
        path: ':id/edit',
        element: <ProjectForm />
      }
    ]
  }
];