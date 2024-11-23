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
  CircularProgress,
  Tooltip
} from '@mui/material';
import { Check, Close, RemoveRedEye } from '@mui/icons-material';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { getLeaves, approveLeave, rejectLeave } from '../../services/hr';
import { queryKeys } from '../../config/queryClient';
import { Leave, LeaveStatus } from '../../types/hr';

const getStatutColor = (statut: LeaveStatus): 'success' | 'error' | 'warning' | 'default' => {
  switch (statut) {
    case 'approuve':
      return 'success';
    case 'refuse':
      return 'error';
    case 'en_attente':
      return 'warning';
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

const LeaveRequests: React.FC = () => {
  const queryClient = useQueryClient();

  const { data: leaves, isLoading, error } = useQuery({
    queryKey: queryKeys.hr.leaves(),
    queryFn: getLeaves
  });

  const approveMutation = useMutation({
    mutationFn: approveLeave,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.hr.leaves() });
    }
  });

  const rejectMutation = useMutation({
    mutationFn: ({ id, motif }: { id: string; motif: string }) => rejectLeave(id, motif),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.hr.leaves() });
    }
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
        Une erreur est survenue lors du chargement des demandes de congés
      </Alert>
    );
  }

  return (
    <Box>
      <Typography variant="h6" gutterBottom>
        Demandes de Congés
      </Typography>
      
      {(approveMutation.error || rejectMutation.error) && (
        <Alert severity="error" sx={{ mb: 2 }}>
          Une erreur est survenue lors du traitement de la demande
        </Alert>
      )}
      
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Type</TableCell>
              <TableCell>Date Début</TableCell>
              <TableCell>Date Fin</TableCell>
              <TableCell>Motif</TableCell>
              <TableCell>Statut</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {leaves?.map((leave) => (
              <TableRow key={leave.id}>
                <TableCell>{leave.type}</TableCell>
                <TableCell>{formatDate(leave.dateDebut)}</TableCell>
                <TableCell>{formatDate(leave.dateFin)}</TableCell>
                <TableCell>{leave.motif}</TableCell>
                <TableCell>
                  <Chip 
                    label={leave.statut} 
                    color={getStatutColor(leave.statut)}
                    size="small"
                  />
                </TableCell>
                <TableCell>
                  {leave.statut === 'en_attente' ? (
                    <>
                      <Tooltip title="Approuver">
                        <IconButton 
                          size="small" 
                          color="success"
                          onClick={() => approveMutation.mutate(leave.id)}
                          disabled={approveMutation.isPending}
                        >
                          <Check />
                        </IconButton>
                      </Tooltip>
                      <Tooltip title="Refuser">
                        <IconButton 
                          size="small" 
                          color="error"
                          onClick={() => rejectMutation.mutate({ id: leave.id, motif: 'Refusé par le responsable' })}
                          disabled={rejectMutation.isPending}
                        >
                          <Close />
                        </IconButton>
                      </Tooltip>
                    </>
                  ) : (
                    <Tooltip title="Voir détails">
                      <IconButton 
                        size="small" 
                        color="primary"
                      >
                        <RemoveRedEye />
                      </IconButton>
                    </Tooltip>
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
