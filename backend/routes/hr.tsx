import { RouteObject } from 'react-router-dom';
import HRPage from '../components/hr/HRPage';
import EmployeeForm from '../components/hr/EmployeeForm';
import EmployeeDetails from '../components/hr/EmployeeDetails';
import LeaveRequestForm from '../components/hr/LeaveRequestForm';

export const hrRoutes: RouteObject[] = [
  {
    path: 'hr',
    children: [
      {
        index: true,
        element: <HRPage />
      },
      {
        path: 'employees/new',
        element: <EmployeeForm />
      },
      {
        path: 'employees/:id',
        element: <EmployeeDetails />
      },
      {
        path: 'employees/:id/edit',
        element: <EmployeeForm />
      },
      {
        path: 'leave-requests/new',
        element: <LeaveRequestForm />
      }
    ]
  }
];