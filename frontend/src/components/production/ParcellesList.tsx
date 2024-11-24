import React from 'react';
import {
  Card,
  CardContent,
  Typography,
  Box,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  IconButton,
  Chip,
  Button
} from '@mui/material';
import { Edit, Visibility } from '@mui/icons-material';
import { useQuery } from 'react-query';
import { useNavigate } from 'react-router-dom';
import { productionService } from '../../services/production';
import { Parcelle, CultureType, ParcelleStatus } from '../../types/production';

const getCultureTypeLabel = (type: CultureType) => {
  switch (type) {
    case CultureType.PALMIER:
      return 'Palmier à huile';
    case CultureType.PAPAYE:
      return 'Papaye';
    default:
      return type;
  }
};

const getStatusColor = (status: ParcelleStatus) => {
  switch (status) {
    case ParcelleStatus.ACTIVE:
      return 'success';
    case ParcelleStatus.EN_PREPARATION:
      return 'warning';
    case ParcelleStatus.EN_REPOS:
      return 'error';
    default:
      return 'default';
  }
};

const ParcellesList: React.FC = () => {
  const navigate = useNavigate();
  const { data: parcelles, isLoading } = useQuery(
    'parcelles',
    productionService.getParcelles
  );

  if (isLoading) {
    return <Typography>Chargement...</Typography>;
  }

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h5">
          Liste des Parcelles
        </Typography>
        <Button
          variant="contained"
          color="primary"
          onClick={() => navigate('/production/parcelles/new')}
        >
          Nouvelle Parcelle
        </Button>
      </Box>

      <Card>
        <CardContent>
          <TableContainer component={Paper}>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Code</TableCell>
                  <TableCell>Culture</TableCell>
                  <TableCell>Surface (ha)</TableCell>
                  <TableCell>Date Plantation</TableCell>
                  <TableCell>Statut</TableCell>
                  <TableCell>Actions</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {parcelles?.map((parcelle: Parcelle) => (
                  <TableRow key={parcelle.id}>
                    <TableCell>{parcelle.code}</TableCell>
                    <TableCell>{getCultureTypeLabel(parcelle.culture_type)}</TableCell>
                    <TableCell>{parcelle.surface_hectares}</TableCell>
                    <TableCell>
                      {new Date(parcelle.date_plantation).toLocaleDateString()}
                    </TableCell>
                    <TableCell>
                      <Chip
                        label={parcelle.statut}
                        size="small"
                        color={getStatusColor(parcelle.statut)}
                      />
                    </TableCell>
                    <TableCell>
                      <IconButton
                        size="small"
                        color="primary"
                        onClick={() => navigate(`/production/parcelles/${parcelle.id}`)}
                        title="Voir les détails"
                      >
                        <Visibility />
                      </IconButton>
                      <IconButton
                        size="small"
                        color="primary"
                        onClick={() => navigate(`/production/parcelles/${parcelle.id}/edit`)}
                        title="Modifier"
                      >
                        <Edit />
                      </IconButton>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </CardContent>
      </Card>
    </Box>
  );
};

export default ParcellesList;
