import React from 'react';
import {
  Card,
  CardContent,
  Typography,
  Box,
  Grid,
  Chip,
  Divider,
  Button,
  Alert,
  CircularProgress
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
import { useQuery } from '@tanstack/react-query';
import { useParams, useNavigate } from 'react-router-dom';
import { getEmployee } from '../../services/hr';
import { queryKeys } from '../../config/queryClient';
import { Employee, EmployeeStatus } from '../../types/hr';
import InfoItem from './components/InfoItem';

const getStatutColor = (statut: EmployeeStatus): 'success' | 'error' | 'warning' | 'info' | 'default' => {
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

const EmployeeDetails: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();

  const { data: employee, isLoading, error } = useQuery({
    queryKey: queryKeys.hr.employee(id!),
    queryFn: () => getEmployee(id!),
    enabled: !!id
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
        Une erreur est survenue lors du chargement des détails de l'employé
      </Alert>
    );
  }

  if (!employee) {
    return (
      <Alert severity="info" sx={{ mb: 2 }}>
        Employé non trouvé
      </Alert>
    );
  }

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
                value={formatDate(employee.dateEmbauche)}
              />
            </Grid>
          </Grid>

          <Divider sx={{ my: 3 }} />

          <Box>
            <Typography variant="subtitle1" gutterBottom>
              Informations complémentaires
            </Typography>
            <Grid container spacing={2}>
              {employee.adresse && (
                <>
                  <Grid item xs={12} sm={6}>
                    <Typography variant="body2" color="text.secondary">
                      Adresse
                    </Typography>
                    <Typography>
                      {employee.adresse.rue}<br />
                      {employee.adresse.codePostal} {employee.adresse.ville}<br />
                      {employee.adresse.pays}
                    </Typography>
                  </Grid>
                </>
              )}
              {employee.formation && (
                <Grid item xs={12} sm={6}>
                  <Typography variant="body2" color="text.secondary">
                    Formation
                  </Typography>
                  <Typography>
                    Niveau: {employee.formation.niveau}<br />
                    {employee.formation.certifications.length > 0 && (
                      <>
                        Certifications:<br />
                        {employee.formation.certifications.join(', ')}
                      </>
                    )}
                  </Typography>
                </Grid>
              )}
            </Grid>
          </Box>
        </CardContent>
      </Card>
    </Box>
  );
};

export default EmployeeDetails;
