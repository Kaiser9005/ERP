import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { PayrollPage } from '../components/hr/payroll/PayrollPage';
import EmployeesList from '../components/hr/EmployeesList';
import { ContractsPage } from '../components/hr/ContractsPage';
import LeaveRequests from '../components/hr/LeaveRequests';
import AttendanceOverview from '../components/hr/AttendanceOverview';
import CompetencesAgricoles from '../components/hr/agricole/CompetencesAgricoles';
import { FormationPage } from '../components/hr/formation/FormationPage';

const HRRoutes: React.FC = () => {
  return (
    <Routes>
      <Route path="/" element={<EmployeesList />} />
      <Route path="/contrats" element={<ContractsPage />} />
      <Route path="/conges" element={<LeaveRequests />} />
      <Route path="/presences" element={<AttendanceOverview />} />
      <Route path="/competences" element={<CompetencesAgricoles employeId="current" />} />
      <Route path="/paie" element={<PayrollPage />} />
      <Route path="/formations" element={<FormationPage />} />
    </Routes>
  );
};

export default HRRoutes;
