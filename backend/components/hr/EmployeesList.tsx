import React from 'react';
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  IconButton,
  Typography,
  Box,
  Chip
} from '@mui/material';
import { Edit, Delete } from '@mui/icons-material';
import { useQuery } from 'react-query';
import { getEmployees, Employee } from '../../services/hr';

const getStatutColor = (statut: Employee['statut']) => {
  switch (statut) {
    case 'ACTIF':
      return 'success';
    case 'CONGE':
      return 'info';
    case 'FORMATION':
      return 'warning';
    case 'INACTIF':
      return 'error';
    default:
      return 'default';
  }
};

const EmployeesList: React.FC = () => {
  const { data: employees, isLoading } = useQuery('employees', getEmployees);

  if (isLoading) {
    return <Typography>Chargement...</Typography>;
  }

  return (
    <Box>
      <Typography variant="h6" gutterBottom>
        Liste des Employés
      </Typography>
      
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Matricule</TableCell>
              <TableCell>Nom</TableCell>
              <TableCell>Prénom</TableCell>
              <TableCell>Poste</TableCell>
              <TableCell>Département</TableCell>
              <TableCell>Type Contrat</TableCell>
              <TableCell>Date d'embauche</TableCell>
              <TableCell>Statut</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {employees?.map((employee) => (
              <TableRow key={employee.id}>
                <TableCell>{employee.matricule}</TableCell>
                <TableCell>{employee.nom}</TableCell>
                <TableCell>{employee.prenom}</TableCell>
                <TableCell>{employee.poste}</TableCell>
                <TableCell>{employee.departement}</TableCell>
                <TableCell>{employee.type_contrat}</TableCell>
                <TableCell>{new Date(employee.date_embauche).toLocaleDateString()}</TableCell>
                <TableCell>
                  <Chip 
                    label={employee.statut} 
                    color={getStatutColor(employee.statut)}
                    size="small"
                  />
                </TableCell>
                <TableCell>
                  <IconButton size="small" color="primary">
                    <Edit />
                  </IconButton>
                  <IconButton size="small" color="error">
                    <Delete />
                  </IconButton>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
};

export default EmployeesList;
