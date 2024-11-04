import React, { useState } from 'react';
import {
  Card,
  CardContent,
  Grid,
  Typography,
  Button,
  Chip,
  Box,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  IconButton
} from '@mui/material';
import { Add, Edit, Visibility } from '@mui/icons-material';
import { useParams, useNavigate } from 'react-router-dom';
import { useQuery } from 'react-query';
import { getParcelle, getRecoltes } from '../../services/production';
import PageHeader from '../layout/PageHeader';
import RecolteForm from './RecolteForm';
import { format } from 'date-fns';
import { fr } from 'date-fns/locale';

const ParcelleDetails: React.FC = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [recolteFormOpen, setRecolteFormOpen] = useState(false);

  const { data: parcelle } = useQuery(
    ['parcelle', id],
    () => getParcelle(id!)
  );

  const { data: recoltes } = useQuery(
    ['recoltes', id],
    () => getRecoltes(id!)
  );

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'ACTIVE':
        return 'success';
      case 'EN_REPOS':
        return 'warning';
      case 'EN_PREPARATION':
        return 'info';
      default:
        return 'default';
    }
  };

  return (
    <>
      <PageHeader
        title={`Parcelle ${parcelle?.code}`}
        subtitle="Détails et historique des récoltes"
        action={{
          label: "Modifier",
          onClick: () => navigate(`/production/parcelles/${id}/edit`),
          icon: <Edit />
        }}
      />

      <Grid container spacing={3}>
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Informations Générales
              </Typography>

              <Box sx={{ '& > *': { mb: 2 } }}>
                <Box>
                  <Typography color="text.secondary" gutterBottom>
                    Type de Culture
                  </Typography>
                  <Chip
                    label={parcelle?.culture_type === 'PALMIER' ? 'Palmier à huile' : 'Papaye'}
                    color="primary"
                  />
                </Box>

                <Box>
                  <Typography color="text.secondary" gutterBottom>
                    Statut
                  </Typography>
                  <Chip
                    label={parcelle?.statut}
                    color={getStatusColor(parcelle?.statut)}
                  />
                </Box>

                <Box>
                  <Typography color="text.secondary" gutterBottom>
                    Surface
                  </Typography>
                  <Typography variant="h6">
                    {parcelle?.surface_hectares} ha
                  </Typography>
                </Box>

                <Box>
                  <Typography color="text.secondary" gutterBottom>
                    Date de Plantation
                  </Typography>
                  <Typography>
                    {parcelle?.date_plantation &&
                      format(new Date(parcelle.date_plantation), 'PP', { locale: fr })}
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={8}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
                <Typography variant="h6">
                  Historique des Récoltes
                </Typography>
                <Button
                  variant="contained"
                  startIcon={<Add />}
                  onClick={() => setRecolteFormOpen(true)}
                >
                  Nouvelle Récolte
                </Button>
              </Box>

              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Date</TableCell>
                    <TableCell>Quantité</TableCell>
                    <TableCell>Qualité</TableCell>
                    <TableCell>Actions</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {recoltes?.map((recolte) => (
                    <TableRow key={recolte.id}>
                      <TableCell>
                        {format(new Date(recolte.date_recolte), 'PP', { locale: fr })}
                      </TableCell>
                      <TableCell>{recolte.quantite_kg} kg</TableCell>
                      <TableCell>
                        <Chip
                          size="small"
                          label={recolte.qualite}
                          color={recolte.qualite === 'A' ? 'success' : 'warning'}
                        />
                      </TableCell>
                      <TableCell>
                        <IconButton size="small">
                          <Visibility />
                        </IconButton>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <RecolteForm
        open={recolteFormOpen}
        onClose={() => setRecolteFormOpen(false)}
        parcelleId={id}
      />
    </>
  );
};

export default ParcelleDetails;