import React from 'react';
import {
  Card,
  CardContent,
  Typography,
  Box,
  Grid,
  Chip,
  Button,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper
} from '@mui/material';
import { useParams, useNavigate } from 'react-router-dom';
import { useQuery } from 'react-query';
import { productionService } from '../../services/production';
import { Agriculture, WaterDrop, Thermostat } from '@mui/icons-material';
import { Parcelle, ProductionEvent, Recolte, QualiteRecolte, ParcelleStatus } from '../../types/production';

interface MeteoData {
  temperature: number;
  humidite: number;
  precipitation: number;
}

interface ParcelleWithDetails extends Parcelle {
  events?: ProductionEvent[];
  recoltes?: Recolte[];
}

const MeteoWidget: React.FC<{ data: MeteoData }> = ({ data }) => (
  <Box>
    <Typography variant="subtitle1" gutterBottom>
      Conditions Météo Actuelles
    </Typography>
    <Grid container spacing={2}>
      <Grid item xs={4}>
        <Box display="flex" alignItems="center">
          <Thermostat color="primary" sx={{ mr: 1 }} />
          <Box>
            <Typography variant="body2" color="text.secondary">
              Température
            </Typography>
            <Typography>{data.temperature}°C</Typography>
          </Box>
        </Box>
      </Grid>
      <Grid item xs={4}>
        <Box display="flex" alignItems="center">
          <WaterDrop color="info" sx={{ mr: 1 }} />
          <Box>
            <Typography variant="body2" color="text.secondary">
              Humidité
            </Typography>
            <Typography>{data.humidite}%</Typography>
          </Box>
        </Box>
      </Grid>
      <Grid item xs={4}>
        <Box display="flex" alignItems="center">
          <Agriculture color="success" sx={{ mr: 1 }} />
          <Box>
            <Typography variant="body2" color="text.secondary">
              Précipitations
            </Typography>
            <Typography>{data.precipitation} mm</Typography>
          </Box>
        </Box>
      </Grid>
    </Grid>
  </Box>
);

const ParcelleDetails: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { data: parcelle, isLoading } = useQuery<ParcelleWithDetails>(
    ['parcelle', id],
    () => productionService.getParcelle(id!)
  );

  if (isLoading) {
    return <Typography>Chargement...</Typography>;
  }

  if (!parcelle) {
    return <Typography>Parcelle non trouvée</Typography>;
  }

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h5">
          Détails de la Parcelle
        </Typography>
        <Button
          variant="outlined"
          onClick={() => navigate('/production/parcelles')}
        >
          Retour à la liste
        </Button>
      </Box>

      <Grid container spacing={3}>
        <Grid item xs={12} md={8}>
          <Card>
            <CardContent>
              <Box mb={3}>
                <Typography variant="h6" gutterBottom>
                  {parcelle.code} - {parcelle.culture_type}
                </Typography>
                <Chip
                  label={parcelle.statut}
                  color={parcelle.statut === ParcelleStatus.ACTIVE ? 'success' : 'default'}
                  size="small"
                />
              </Box>

              <Grid container spacing={2}>
                <Grid item xs={12} sm={6}>
                  <Typography variant="body2" color="text.secondary">
                    Surface
                  </Typography>
                  <Typography>{parcelle.surface_hectares} hectares</Typography>
                </Grid>
                <Grid item xs={12} sm={6}>
                  <Typography variant="body2" color="text.secondary">
                    Date de plantation
                  </Typography>
                  <Typography>
                    {new Date(parcelle.date_plantation).toLocaleDateString()}
                  </Typography>
                </Grid>
              </Grid>

              <Box mt={3}>
                <MeteoWidget
                  data={{
                    temperature: 28,
                    humidite: 65,
                    precipitation: 2.5
                  }}
                />
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Dernières Activités
              </Typography>
              {parcelle.events?.map((event) => (
                <Box key={event.id} mb={2}>
                  <Typography variant="subtitle2">
                    {event.type}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    {new Date(event.date_debut).toLocaleDateString()}
                  </Typography>
                  <Typography variant="body2">
                    {event.description}
                  </Typography>
                </Box>
              ))}
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Historique des Récoltes
              </Typography>
              <TableContainer component={Paper}>
                <Table>
                  <TableHead>
                    <TableRow>
                      <TableCell>Date</TableCell>
                      <TableCell>Quantité (kg)</TableCell>
                      <TableCell>Qualité</TableCell>
                      <TableCell>Notes</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {parcelle.recoltes?.map((recolte) => (
                      <TableRow key={recolte.id}>
                        <TableCell>
                          {new Date(recolte.date_recolte).toLocaleDateString()}
                        </TableCell>
                        <TableCell>{recolte.quantite_kg}</TableCell>
                        <TableCell>
                          <Chip
                            label={recolte.qualite}
                            size="small"
                            color={
                              recolte.qualite === QualiteRecolte.A ? 'success' :
                              recolte.qualite === QualiteRecolte.B ? 'primary' :
                              'warning'
                            }
                          />
                        </TableCell>
                        <TableCell>{recolte.notes}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default ParcelleDetails;
