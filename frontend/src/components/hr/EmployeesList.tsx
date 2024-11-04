import React, { useState } from 'react';
import {
  Card,
  CardContent,
  Typography,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  Chip,
  Box,
  TextField,
  InputAdornment,
  IconButton,
  Avatar
} from '@mui/material';
import { Edit, Search, Visibility } from '@mui/icons-material';
import { useQuery } from 'react-query';
import { getEmployees } from '../../services/hr';
import { useNavigate } from 'react-router-dom';

const EmployeesList: React.FC = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const navigate = useNavigate();
  const { data: employees } = useQuery('employees', getEmployees);

  const filteredEmployees = employees?.filter(employee =>
    `${employee.nom} ${employee.prenom}`.toLowerCase().includes(searchTerm.toLowerCase()) ||
    employee.matricule.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'ACTIF':
        return 'success';
      case 'INACTIF':
        return 'error';
      case 'CONGE':
        return 'warning';
      case 'SUSPENDU':
        return 'error';
      default:
        return 'default';
    }
  };

  return (
    <Card>
      <CardContent>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
          <Typography variant="h6">Employés</Typography>
          <TextField
            size="small"
            placeholder="Rechercher..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <Search />
                </InputAdornment>
              ),
            }}
          />
        </Box>

        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Employé</TableCell>
              <TableCell>Matricule</TableCell>
              <TableCell>Département</TableCell>
              <TableCell>Poste</TableCell>
              <TableCell>Statut</TableCell>
              <TableCell align="right">Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {filteredEmployees?.map((employee) => (
              <TableRow key={employee.id}>
                <TableCell>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                    <Avatar>
                      {employee.prenom[0]}{employee.nom[0]}
                    </Avatar>
                    <Box>
                      <Typography variant="subtitle2">
                        {employee.prenom} {employee.nom}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        {employee.email}
                      </Typography>
                    </Box>
                  </Box>
                </TableCell>
                <TableCell>{employee.matricule}</TableCell>
                <TableCell>{employee.departement}</TableCell>
                <TableCell>{employee.poste}</TableCell>
                <TableCell>
                  <Chip
                    size="small"
                    label={employee.statut}
                    color={getStatusColor(employee.statut)}
                  />
                </TableCell>
                <TableCell align="right">
                  <IconButton
                    size="small"
                    onClick={() => navigate(`/hr/employees/${employee.id}`)}
                  >
                    <Visibility />
                  </IconButton>
                  <IconButton
                    size="small"
                    onClick={() => navigate(`/hr/employees/${employee.id}/edit`)}
                  >
                    <Edit />
                  </IconButton>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </CardContent>
    </Card>
  );
};

export default EmployeesList;