import React from 'react';
import { Grid } from '@mui/material';
import PageHeader from '../layout/PageHeader';
import EmployeeStats from './EmployeeStats';
import EmployeesList from './EmployeesList';
import LeaveRequests from './LeaveRequests';
import AttendanceOverview from './AttendanceOverview';
import { Add } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';

const HRPage: React.FC = () => {
  const navigate = useNavigate();

  return (
    <>
      <PageHeader
        title="Ressources Humaines"
        subtitle="Gestion des employés et des présences"
        action={{
          label: "Nouvel Employé",
          onClick: () => navigate('/hr/employees/new'),
          icon: <Add />
        }}
      />

      <Grid container spacing={3}>
        {/* Statistiques RH */}
        <Grid item xs={12}>
          <EmployeeStats />
        </Grid>

        {/* Liste des employés */}
        <Grid item xs={12} lg={8}>
          <EmployeesList />
        </Grid>

        {/* Demandes de congés */}
        <Grid item xs={12} lg={4}>
          <LeaveRequests />
        </Grid>

        {/* Aperçu des présences */}
        <Grid item xs={12}>
          <AttendanceOverview />
        </Grid>
      </Grid>
    </>
  );
};

export default HRPage;