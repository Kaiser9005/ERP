import React, { useState } from 'react';
import {
  Card,
  CardContent,
  Grid,
  Typography,
  Chip,
  Box,
  Button,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow
} from '@mui/material';
import { useParams, useNavigate } from 'react-router-dom';
import { useQuery } from 'react-query';
import { getEmployee, getEmployeeLeaves } from '../../services/hr';
import PageHeader from '../layout/PageHeader';
import { Edit } from '@mui/icons-material';
import { format } from 'date-fns';
import { fr } from 'date-fns/locale';
import LeaveRequestForm from './LeaveRequestForm';

const EmployeeDetails: React.FC = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [leaveFormOpen, setLeaveFormOpen] = useState(false);

  const { data: employee } = useQuery(
    ['employee', id],
    () => getEmployee(id!)
  );

  const { data: leaves } = useQuery(
    ['employee-leaves', id],
    () => getEmployeeLeaves(id!)
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
    <>
      <PageHeader
        title={`${employee?.prenom} ${employee?.nom}`}
        subtitle={`Matricule: ${employee?.matricule}`}
        action={{
          label: "Modifier",
          onClick: () => navigate(`/hr/employees/${id}/edit`),
          icon: <Edit />
        }}
      />

      <Grid container spacing={3}>
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Informations Personnelles
              </Typography>

              <Box sx={{ '& > *': { mb: 2 } }}>
                <Box>
                  <Typography color="text.secondary" gutterBottom>
                    Date de Naissance
                  </Typography>
                  <Typography>
                    {employee?.date_naissance &&
                      format(new Date(employee.date_naissance), 'PP', { locale: fr })}
                  </Typography>
                </Box>

                <Box>
                  <Typography color="text.secondary" gutterBottom>
                    Email
                  </Typography>
                  <Typography>{employee?.email}</Typography>
                </Box>

                <Box>
                  <Typography color="text.secondary" gutterBottom>
                    Téléphone
                  </Typography>
                  <Typography>{employee?.telephone}</Typography>
                </Box>

                <Box>
                  <Typography color="text.secondary" gutterBottom>
                    Adresse
                  </Typography>
                  <Typography>{employee?.adresse}</Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={8}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
                <Typography variant="h6">
                  Informations Professionnelles
                </Typography>
                <Chip
                  label={employee?.statut}
                  color={getStatusColor(employee?.statut || '')}
                />
              </Box>

              <Grid container spacing={3}>
                <Grid item xs={12} sm={6}>
                  <Typography color="text.secondary" gutterBottom>
                    Département
                  </Typography>
                  <Typography variant="body1">
                    {employee?.departement}
                  </Typography>
                </Grid>

                <Grid item xs={12} sm={6}>
                  <Typography color="text.secondary" gutterBottom>
                    Poste
                  </Typography>
                  <Typography variant="body1">
                    {employee?.poste}
                  </Typography>
                </Grid>

                <Grid item xs={12} sm={6}>
                  <Typography color="text.secondary" gutterBottom>
                    Date d'Embauche
                  </Typography>
                  <Typography variant="body1">
                    {employee?.date_embauche &&
                      format(new Date(employee.date_embauche), 'PP', { locale: fr })}
                  </Typography>
                </Grid>

                <Grid item xs={12} sm={6}>
                  <Typography color="text.secondary" gutterBottom>
                    Type de Contrat
                  </Typography>
                  <Typography variant="body1">
                    {employee?.type_contrat}
                  </Typography>
                </Grid>
              </Grid>
            </CardContent>
          </Card>

          <Card sx={{ mt: 3 }}>
            <CardContent>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
                <Typography variant="h6">
                  Historique des Congés
                </Typography>
                <Button
                  variant="contained"
                  onClick={() => setLeaveFormOpen(true)}
                >
                  Nouvelle Demande
                </Button>
              </Box>

              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Type</TableCell>
                    <TableCell>Début</TableCell>
                    <TableCell>Fin</TableCell>
                    <TableCell>Jours</TableCell>
                    <TableCell>Statut</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {leaves?.map((leave) => (
                    <TableRow key={leave.id}>
                      <TableCell>{leave.type_conge}</TableCell>
                      <TableCell>
                        {format(new Date(leave.date_debut), 'PP', { locale: fr })}
                      </TableCell>
                      <TableCell>
                        {format(new Date(leave.date_fin), 'PP', { locale: fr })}
                      </TableCell>
                      <TableCell>{leave.nb_jours}</TableCell>
                      <TableCell>
                        <Chip
                          size="small"
                          label={leave.statut}
                          color={leave.statut === 'APPROUVE' ? 'success' : 'warning'}
                        />
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <LeaveRequestForm
        open={leaveFormOpen}
        onClose={() => setLeaveFormOpen(false)}
        employeeId={id}
      />
    </>
  );
};

export default EmployeeDetails;