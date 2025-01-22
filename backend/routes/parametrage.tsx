import { RouteObject } from 'react-router-dom';
import ParametrageLayout from '../components/parametrage/ParametrageLayout';
import ParametresGeneraux from '../components/parametrage/ParametresGeneraux';
import ConfigurationModules from '../components/parametrage/ConfigurationModules';

export const parametrageRoutes: RouteObject[] = [
  {
    path: 'parametrage',
    element: <ParametrageLayout />,
    children: [
      {
        path: 'general',
        element: <ParametresGeneraux />
      },
      {
        path: 'modules',
        element: <ConfigurationModules />
      }
    ]
  }
];