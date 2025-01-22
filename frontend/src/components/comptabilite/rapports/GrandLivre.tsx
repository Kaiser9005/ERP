import React, { useState } from 'react';
import {
  Paper,
  Grid,
  TextField,
  Button,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  MenuItem,
  Typography,
  Box,
  Alert,
  CircularProgress
} from '@mui/material';
import { useQuery } from '@tanstack/react-query';
import type { CompteComptable, GrandLivreEcriture, GrandLivreResponseType } from '../../../types/comptabilite';
import { getComptes, getGrandLivre } from '../../../services/comptabilite';
import { formatCurrency, formatDate } from '../../../utils/format';
import { queryKeys } from '../../../config/queryClient';

interface QueryError {
  message: string;
}

const GrandLivre: React.FC = () => {
  const [selectedCompte, setSelectedCompte] = useState<string[]>([]);
  const [dateDebut, setDateDebut] = useState(
    new Date(new Date().getFullYear(), new Date().getMonth(), 1)
      .toISOString()
      .split('T')[0]
  );
  const [dateFin, setDateFin] = useState(
    new Date().toISOString().split('T')[0]
  );

  const { data: comptes = [], isLoading: loadingComptes, error: comptesError } = useQuery<CompteComptable[], QueryError>({
    queryKey: queryKeys.comptabilite.comptes(),
    queryFn: () => getComptes()
  });

  const { data: grandLivreData, isLoading: loadingLignes, error: lignesError, refetch: refetchLignes } = useQuery<{ ecritures: GrandLivreEcriture[], solde_initial: number }, QueryError>({
    queryKey: queryKeys.comptabilite.grandLivre({
      compte_id: selectedCompte.join(','),
      date_debut: dateDebut,
      date_fin: dateFin
    }),
    queryFn: () => getGrandLivre({
      compte_id: selectedCompte,
      date_debut: new Date(dateDebut),
      date_fin: new Date(dateFin)
    }),
    enabled: !!selectedCompte
  });

  const lignes = grandLivreData?.ecritures || [];
  const soldeInitial = grandLivreData?.solde_initial || 0;

  const handleSearch = () => {
    if (!selectedCompte) return;
    refetchLignes();
  };

  const calculateTotals = () => {
    return lignes.reduce(
      (acc, ligne) => ({
        debit: acc.debit + (ligne.ecritures[0]?.debit || 0),
        credit: acc.credit + (ligne.ecritures[0]?.credit || 0),
      }),
      { debit: 0, credit: 0 }
    );
  };

  const getCompteInfo = () => {
    const compte = comptes.find(c => selectedCompte.includes(c.id));
    return compte ? `${compte.numero} - ${compte.libelle}` : '';
  };

  if (comptesError) {
    return (
      <Alert severity="error" sx={{ mb: 3 }}>
        {comptesError.message || 'Erreur lors du chargement des comptes'}
      </Alert>
    );
  }

  return (
    <Paper component="div" sx={{ p: 2 }}>
      <Grid container spacing={2} sx={{ mb: 3 }}>
        <Grid item xs={12} md={4}>
          <TextField
            label="Compte"
            select
            fullWidth
            value={selectedCompte[0] || ''}
            onChange={(e) => setSelectedCompte([e.target.value])}
            disabled={loadingComptes}
          >
            {comptes.map((compte) => (
              <MenuItem key={compte.id} value={compte.id}>
                {compte.numero} - {compte.libelle}
              </MenuItem>
            ))}
          </TextField>
        </Grid>
        <Grid item xs={12} md={3}>
          <TextField
            label="Date début"
            type="date"
            value={dateDebut}
            onChange={(e) => setDateDebut(e.target.value)}
            fullWidth
            InputLabelProps={{ shrink: true }}
          />
        </Grid>
        <Grid item xs={12} md={3}>
          <TextField
            label="Date fin"
            type="date"
            value={dateFin}
            onChange={(e) => setDateFin(e.target.value)}
            fullWidth
            InputLabelProps={{ shrink: true }}
          />
        </Grid>
        <Grid item xs={12} md={2}>
          <Button
            variant="contained"
            onClick={handleSearch}
            disabled={!selectedCompte || loadingLignes}
            fullWidth
            sx={{ height: '100%' }}
          >
            Rechercher
          </Button>
        </Grid>
      </Grid>

      {lignesError && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {lignesError.message || 'Erreur lors du chargement du grand livre'}
        </Alert>
      )}

      {loadingLignes && (
        <Box component="div" sx={{ display: 'flex', justifyContent: 'center', my: 3 }}>
          <CircularProgress />
        </Box>
      )}

      {selectedCompte && lignes.length > 0 && (
        <>
          <Typography variant="h6" component="div" gutterBottom>
            Grand Livre : {getCompteInfo()}
          </Typography>
          <Typography variant="subtitle2" component="div" gutterBottom>
            Période du {formatDate(dateDebut)} au {formatDate(dateFin)}
          </Typography>

          <TableContainer component="div" sx={{ mt: 2 }}>
            <Table size="small">
              <TableHead>
                <TableRow>
                  <TableCell>Date</TableCell>
                  <TableCell>Pièce</TableCell>
                  <TableCell>Libellé</TableCell>
                  <TableCell align="right">Débit</TableCell>
                  <TableCell align="right">Crédit</TableCell>
                  <TableCell align="right">Solde</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {lignes.map((ligne, index) => (
                  <TableRow key={index}>
                    <TableCell>{formatDate(ligne.date)}</TableCell>
                    <TableCell>{ligne.piece}</TableCell>
                    <TableCell>{ligne.libelle}</TableCell>
                    <TableCell align="right">{formatCurrency(ligne.ecritures[0]?.debit)}</TableCell>
                    <TableCell align="right">{formatCurrency(ligne.ecritures[0]?.credit)}</TableCell>
                    <TableCell align="right">{formatCurrency(ligne.solde || 0)}</TableCell>
                  </TableRow>
                ))}
                <TableRow>
                  <TableCell colSpan={3}>
                    <Typography variant="subtitle1" component="div">Total</Typography>
                  </TableCell>
                  <TableCell align="right">
                    <Typography variant="subtitle1" component="div">
                      {formatCurrency(calculateTotals().debit)}
                    </Typography>
                  </TableCell>
                  <TableCell align="right">
                    <Typography variant="subtitle1" component="div">
                      {formatCurrency(calculateTotals().credit)}
                    </Typography>
                  </TableCell>
                  <TableCell align="right">
                    <Typography variant="subtitle1" component="div">
                      {formatCurrency(grandLivreData?.solde_initial || 0 + calculateTotals().debit - calculateTotals().credit)}
                    </Typography>
                  </TableCell>
                </TableRow>
              </TableBody>
            </Table>
          </TableContainer>
        </>
      )}

      {selectedCompte && lignes.length === 0 && !loadingLignes && (
        <Box component="div" sx={{ p: 2, textAlign: 'center' }}>
          <Typography variant="body1" component="div" color="text.secondary">
            Aucune écriture pour la période sélectionnée
          </Typography>
        </Box>
      )}
    </Paper>
  );
};

export default GrandLivre;
