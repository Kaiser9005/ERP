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
  Chip,
  Alert,
  CircularProgress
} from '@mui/material';
import { Edit, Delete } from '@mui/icons-material';
import { useQuery } from '@tanstack/react-query';
import { getEmployees } from '../../services/hr';
import { queryKeys } from '../../config/queryClient';
import { Employee } from '../../types/hr';

const getStatutColor = (statut: Employee['statut']): 'success' | 'info' | 'warning' | 'error' | 'default' => {
  switch (statut) {
    case 'actif':
      return 'success';
    case 'conge':
      return 'info';
    case 'formation':
      return 'warning';
    case 'inactif':
      return 'error';
    default:
      return 'default';
  }
};

const formatDate = (dateStr: string): string => {
  return new Date(dateStr).toLocaleDateString('fr-FR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });
};

const EmployeesList: React.FC = () => {
  const { data: employees, isLoading, error } = useQuery({
    queryKey: queryKeys.hr.employees(),
    queryFn: getEmployees
  });

  if (isLoading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Alert severity="error" sx={{ mb: 2 }}>
        Une erreur est survenue lors du chargement des employés
      </Alert>
    );
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
              <TableCell>Email</TableCell>
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
                <TableCell>{employee.email}</TableCell>
                <TableCell>{formatDate(employee.dateEmbauche)}</TableCell>
                <TableCell>
                  <Chip 
                    label={employee.statut} 
                    color={getStatutColor(employee.statut)}
                    size="small"
                  />
                </TableCell>
                <TableCell>
                  <IconButton 
                    size="small" 
                    color="primary"
                    aria-label="Modifier l'employé"
                  >
                    <Edit />
                  </IconButton>
                  <IconButton 
                    size="small" 
                    color="error"
                    aria-label="Supprimer l'employé"
                  >
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
