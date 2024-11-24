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
import { Check, Close, RemoveRedEye } from '@mui/icons-material';
import { useQuery } from 'react-query';
import { getLeaveRequests, LeaveRequest } from '../../services/hr';

const getStatutColor = (statut: LeaveRequest['statut']) => {
  switch (statut) {
    case 'APPROUVE':
      return 'success';
    case 'REFUSE':
      return 'error';
    case 'EN_ATTENTE':
      return 'warning';
    default:
      return 'default';
  }
};

const LeaveRequests: React.FC = () => {
  const { data: requests, isLoading } = useQuery('leave-requests', getLeaveRequests);

  if (isLoading) {
    return <Typography>Chargement...</Typography>;
  }

  return (
    <Box>
      <Typography variant="h6" gutterBottom>
        Demandes de Congés
      </Typography>
      
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Type</TableCell>
              <TableCell>Date Début</TableCell>
              <TableCell>Date Fin</TableCell>
              <TableCell>Motif</TableCell>
              <TableCell>Statut</TableCell>
              <TableCell>Date Validation</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {requests?.map((request) => (
              <TableRow key={request.id}>
                <TableCell>{request.type_conge}</TableCell>
                <TableCell>{new Date(request.date_debut).toLocaleDateString()}</TableCell>
                <TableCell>{new Date(request.date_fin).toLocaleDateString()}</TableCell>
                <TableCell>{request.motif}</TableCell>
                <TableCell>
                  <Chip 
                    label={request.statut} 
                    color={getStatutColor(request.statut)}
                    size="small"
                  />
                </TableCell>
                <TableCell>
                  {request.date_validation ? 
                    new Date(request.date_validation).toLocaleDateString() : 
                    '-'
                  }
                </TableCell>
                <TableCell>
                  {request.statut === 'EN_ATTENTE' ? (
                    <>
                      <IconButton size="small" color="success" title="Approuver">
                        <Check />
                      </IconButton>
                      <IconButton size="small" color="error" title="Refuser">
                        <Close />
                      </IconButton>
                    </>
                  ) : (
                    <IconButton size="small" color="primary" title="Voir détails">
                      <RemoveRedEye />
                    </IconButton>
                  )}
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
};

export default LeaveRequests;
