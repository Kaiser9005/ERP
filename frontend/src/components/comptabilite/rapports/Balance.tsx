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
} from '@mui/material';
import { CompteBalance, TypeCompte } from '../../../types/comptabilite';
import { getBalance } from '../../../services/comptabilite';
import { formatCurrency, formatDate } from '../../../utils/format';

const TYPES_COMPTE = ['TOUS', 'ACTIF', 'PASSIF', 'CHARGE', 'PRODUIT'] as const;

const Balance: React.FC = () => {
  const [dateDebut, setDateDebut] = useState(
    new Date(new Date().getFullYear(), new Date().getMonth(), 1)
      .toISOString()
      .split('T')[0]
  );
  const [dateFin, setDateFin] = useState(
    new Date().toISOString().split('T')[0]
  );
  const [typeCompte, setTypeCompte] = useState<typeof TYPES_COMPTE[number]>('TOUS');
  const [comptes, setComptes] = useState<CompteBalance[]>([]);
  const [loading, setLoading] = useState(false);

  const handleSearch = async () => {
    setLoading(true);
    try {
      const data = await getBalance({
        dateDebut,
        dateFin,
        typeCompte: typeCompte === 'TOUS' ? undefined : typeCompte as TypeCompte
      });
      setComptes(data);
    } catch (error) {
      console.error('Erreur lors du chargement de la balance:', error);
    } finally {
      setLoading(false);
    }
  };

  const calculateTotals = () => {
    return comptes.reduce(
      (acc, compte) => ({
        debit: acc.debit + compte.debit,
        credit: acc.credit + compte.credit,
        solde: acc.solde + compte.solde
      }),
      { debit: 0, credit: 0, solde: 0 }
    );
  };

  return (
    <Paper sx={{ p: 2 }}>
      <Grid container spacing={2} sx={{ mb: 3 }}>
        <Grid item xs={12} md={3}>
          <TextField
            label="Type de compte"
            select
            fullWidth
            value={typeCompte}
            onChange={(e) => setTypeCompte(e.target.value as typeof TYPES_COMPTE[number])}
          >
            {TYPES_COMPTE.map((type) => (
              <MenuItem key={type} value={type}>
                {type}
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
          />
        </Grid>
        <Grid item xs={12} md={3}>
          <TextField
            label="Date fin"
            type="date"
            value={dateFin}
            onChange={(e) => setDateFin(e.target.value)}
            fullWidth
          />
        </Grid>
        <Grid item xs={12} md={3}>
          <Button
            variant="contained"
            onClick={handleSearch}
            disabled={loading}
            fullWidth
            sx={{ height: '100%' }}
          >
            Générer la Balance
          </Button>
        </Grid>
      </Grid>

      {comptes.length > 0 && (
        <>
          <Typography variant="h6" gutterBottom>
            Balance Générale
          </Typography>
          <Typography variant="subtitle2" gutterBottom>
            Période du {formatDate(dateDebut)} au {formatDate(dateFin)}
          </Typography>

          <TableContainer sx={{ mt: 2 }}>
            <Table size="small">
              <TableHead>
                <TableRow>
                  <TableCell>N° Compte</TableCell>
                  <TableCell>Libellé</TableCell>
                  <TableCell>Type</TableCell>
                  <TableCell align="right">Total Débit</TableCell>
                  <TableCell align="right">Total Crédit</TableCell>
                  <TableCell align="right">Solde Débiteur</TableCell>
                  <TableCell align="right">Solde Créditeur</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {comptes.map((compte, index) => (
                  <TableRow key={index}>
                    <TableCell>{compte.compte.numero}</TableCell>
                    <TableCell>{compte.compte.libelle}</TableCell>
                    <TableCell>{compte.compte.type}</TableCell>
                    <TableCell align="right">{formatCurrency(compte.debit)}</TableCell>
                    <TableCell align="right">{formatCurrency(compte.credit)}</TableCell>
                    <TableCell align="right">
                      {compte.solde > 0 ? formatCurrency(compte.solde) : '-'}
                    </TableCell>
                    <TableCell align="right">
                      {compte.solde < 0 ? formatCurrency(-compte.solde) : '-'}
                    </TableCell>
                  </TableRow>
                ))}
                <TableRow>
                  <TableCell colSpan={3}>
                    <Typography variant="subtitle1">Total</Typography>
                  </TableCell>
                  <TableCell align="right">
                    <Typography variant="subtitle1">
                      {formatCurrency(calculateTotals().debit)}
                    </Typography>
                  </TableCell>
                  <TableCell align="right">
                    <Typography variant="subtitle1">
                      {formatCurrency(calculateTotals().credit)}
                    </Typography>
                  </TableCell>
                  <TableCell align="right">
                    <Typography variant="subtitle1">
                      {calculateTotals().solde > 0 ? formatCurrency(calculateTotals().solde) : '-'}
                    </Typography>
                  </TableCell>
                  <TableCell align="right">
                    <Typography variant="subtitle1">
                      {calculateTotals().solde < 0 ? formatCurrency(-calculateTotals().solde) : '-'}
                    </Typography>
                  </TableCell>
                </TableRow>
              </TableBody>
            </Table>
          </TableContainer>
        </>
      )}

      {comptes.length === 0 && !loading && (
        <Box sx={{ p: 2, textAlign: 'center' }}>
          <Typography variant="body1" color="text.secondary">
            Aucune donnée disponible pour la période sélectionnée
          </Typography>
        </Box>
      )}
    </Paper>
  );
};

export default Balance;
