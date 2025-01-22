import React from 'react';
import {
  Card,
  CardContent,
  Typography,
  Box,
  Grid,
  Chip,
  Divider,
  Button
} from '@mui/material';
import {
  Email,
  Phone,
  Work,
  Business,
  Today,
  Person,
  AttachMoney
} from '@mui/icons-material';
import { useQuery } from 'react-query';
import { useParams, useNavigate } from 'react-router-dom';
import { getEmployee, Employee } from '../../services/hr';

const InfoItem: React.FC<{
  icon: React.ReactNode;
  label: string;
  value: string | number;
}> = ({ icon, label, value }) => (
  <Box display="flex" alignItems="center" mb={2}>
    <Box
      sx={{
        mr: 2,
        display: 'flex',
        alignItems: 'center',
        color: 'primary.main'
      }}
    >
      {icon}
    </Box>
    <Box>
      <Typography variant="caption" color="text.secondary">
        {label}
      </Typography>
      <Typography>{value}</Typography>
    </Box>
  </Box>
);

const EmployeeDetails: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { data: employee, isLoading } = useQuery(
    ['employee', id],
    () => getEmployee(id!)
  );

  if (isLoading) {
    return <Typography>Chargement...</Typography>;
  }

  if (!employee) {
    return <Typography>Employé non trouvé</Typography>;
  }

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

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h5">
          Détails de l'Employé
        </Typography>
        <Button
          variant="outlined"
          onClick={() => navigate('/hr/employees')}
        >
          Retour à la liste
        </Button>
      </Box>

      <Card>
        <CardContent>
          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <Box mb={3}>
                <Typography variant="h6" gutterBottom>
                  {employee.nom} {employee.prenom}
                </Typography>
                <Chip
                  label={employee.statut}
                  color={getStatutColor(employee.statut)}
                  size="small"
                />
              </Box>

              <InfoItem
                icon={<Person />}
                label="Matricule"
                value={employee.matricule}
              />
              <InfoItem
                icon={<Email />}
                label="Email"
                value={employee.email}
              />
              <InfoItem
                icon={<Phone />}
                label="Téléphone"
                value={employee.telephone}
              />
            </Grid>

            <Grid item xs={12} md={6}>
              <InfoItem
                icon={<Work />}
                label="Poste"
                value={employee.poste}
              />
              <InfoItem
                icon={<Business />}
                label="Département"
                value={employee.departement}
              />
              <InfoItem
                icon={<Today />}
                label="Date d'embauche"
                value={new Date(employee.date_embauche).toLocaleDateString()}
              />
              <InfoItem
                icon={<AttachMoney />}
                label="Salaire de base"
                value={`${employee.salaire_base.toLocaleString()} FCFA`}
              />
            </Grid>
          </Grid>

          <Divider sx={{ my: 3 }} />

          <Box>
            <Typography variant="subtitle1" gutterBottom>
              Informations complémentaires
            </Typography>
            <Grid container spacing={2}>
              <Grid item xs={12} sm={6}>
                <Typography variant="body2" color="text.secondary">
                  Type de contrat
                </Typography>
                <Typography>{employee.type_contrat}</Typography>
              </Grid>
              <Grid item xs={12} sm={6}>
                <Typography variant="body2" color="text.secondary">
                  Date de naissance
                </Typography>
                <Typography>
                  {new Date(employee.date_naissance).toLocaleDateString()}
                </Typography>
              </Grid>
            </Grid>
          </Box>
        </CardContent>
      </Card>
    </Box>
  );
};

export default EmployeeDetails;
