import React, { useState } from 'react';
import {
  Paper,
  Grid,
  TextField,
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
import { TypeCompteComptable, CompteBalance } from '../../../types/comptabilite';
import { getBalance } from '../../../services/comptabilite';
import { formatCurrency } from '../../../utils/format';

interface QueryError {
  message: string;
}

const typeComptes = [
  { value: TypeCompteComptable.ACTIF, label: 'Actif' },
  { value: TypeCompteComptable.PASSIF, label: 'Passif' },
  { value: TypeCompteComptable.CHARGE, label: 'Charges' },
  { value: TypeCompteComptable.PRODUIT, label: 'Produits' }
];

const Balance: React.FC = () => {
  const [selectedType, setSelectedType] = useState<TypeCompteComptable | ''>('');
  const [dateDebut, setDateDebut] = useState(
    new Date(new Date().getFullYear(), new Date().getMonth(), 1)
      .toISOString()
      .split('T')[0]
  );
  const [dateFin, setDateFin] = useState(
    new Date().toISOString().split('T')[0]
  );

  const { data: comptes = [], isLoading, error } = useQuery<CompteBalance[], QueryError>({
    queryKey: ['balance', dateDebut, dateFin, selectedType],
    queryFn: () => getBalance({
      date_debut: new Date(dateDebut),
      date_fin: new Date(dateFin),
      type_compte: selectedType || undefined
    })
  });

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

  if (error) {
    return (
      <Alert severity="error" sx={{ mb: 3 }}>
        {error.message || 'Erreur lors du chargement de la balance'}
      </Alert>
    );
  }

  return (
    <Paper component="div" sx={{ p: 2 }}>
      <Grid container spacing={2} sx={{ mb: 3 }}>
        <Grid item xs={12} md={4}>
          <TextField
            label="Type de compte"
            select
            fullWidth
            value={selectedType}
            onChange={(e) => setSelectedType(e.target.value as TypeCompteComptable | '')}
          >
            <MenuItem value="">Tous</MenuItem>
            {typeComptes.map((type) => (
              <MenuItem key={type.value} value={type.value}>
                {type.label}
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
      </Grid>

      {isLoading ? (
        <Box component="div" sx={{ display: 'flex', justifyContent: 'center', my: 3 }}>
          <CircularProgress />
        </Box>
      ) : comptes.length > 0 ? (
        <>
          <Typography variant="h6" component="div" gutterBottom>
            Balance des comptes
          </Typography>

          <TableContainer component="div">
            <Table size="small">
              <TableHead>
                <TableRow>
                  <TableCell>Numéro</TableCell>
                  <TableCell>Libellé</TableCell>
                  <TableCell>Type</TableCell>
                  <TableCell align="right">Débit</TableCell>
                  <TableCell align="right">Crédit</TableCell>
                  <TableCell align="right">Solde</TableCell>
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
                    <TableCell align="right">{formatCurrency(compte.solde)}</TableCell>
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
                      {formatCurrency(calculateTotals().solde)}
                    </Typography>
                  </TableCell>
                </TableRow>
              </TableBody>
            </Table>
          </TableContainer>
        </>
      ) : (
        <Box component="div" sx={{ p: 2, textAlign: 'center' }}>
          <Typography variant="body1" component="div" color="text.secondary">
            Aucune donnée disponible pour la période sélectionnée
          </Typography>
        </Box>
      )}
    </Paper>
  );
};

export default Balance;
