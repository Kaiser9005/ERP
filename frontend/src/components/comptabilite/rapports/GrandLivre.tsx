import React, { useState, useEffect } from 'react';
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
import { CompteComptable, LigneGrandLivre } from '../../../types/comptabilite';
import { getComptes, getGrandLivre } from '../../../services/comptabilite';
import { formatCurrency, formatDate } from '../../../utils/format';

const GrandLivre: React.FC = () => {
  const [comptes, setComptes] = useState<CompteComptable[]>([]);
  const [selectedCompte, setSelectedCompte] = useState<string>('');
  const [dateDebut, setDateDebut] = useState(
    new Date(new Date().getFullYear(), new Date().getMonth(), 1)
      .toISOString()
      .split('T')[0]
  );
  const [dateFin, setDateFin] = useState(
    new Date().toISOString().split('T')[0]
  );
  const [lignes, setLignes] = useState<LigneGrandLivre[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadComptes();
  }, []);

  const loadComptes = async () => {
    try {
      const data = await getComptes();
      setComptes(data);
    } catch (error) {
      console.error('Erreur lors du chargement des comptes:', error);
    }
  };

  const handleSearch = async () => {
    if (!selectedCompte) return;

    setLoading(true);
    try {
      const data = await getGrandLivre({
        compteId: selectedCompte,
        dateDebut,
        dateFin
      });
      setLignes(data);
    } catch (error) {
      console.error('Erreur lors du chargement du grand livre:', error);
    } finally {
      setLoading(false);
    }
  };

  const calculateTotals = () => {
    return lignes.reduce(
      (acc, ligne) => ({
        debit: acc.debit + ligne.debit,
        credit: acc.credit + ligne.credit,
      }),
      { debit: 0, credit: 0 }
    );
  };

  const getCompteInfo = () => {
    const compte = comptes.find(c => c.id === selectedCompte);
    return compte ? `${compte.numero} - ${compte.libelle}` : '';
  };

  return (
    <Paper sx={{ p: 2 }}>
      <Grid container spacing={2} sx={{ mb: 3 }}>
        <Grid item xs={12} md={4}>
          <TextField
            label="Compte"
            select
            fullWidth
            value={selectedCompte}
            onChange={(e) => setSelectedCompte(e.target.value)}
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
        <Grid item xs={12} md={2}>
          <Button
            variant="contained"
            onClick={handleSearch}
            disabled={!selectedCompte || loading}
            fullWidth
            sx={{ height: '100%' }}
          >
            Rechercher
          </Button>
        </Grid>
      </Grid>

      {selectedCompte && lignes.length > 0 && (
        <>
          <Typography variant="h6" gutterBottom>
            Grand Livre : {getCompteInfo()}
          </Typography>
          <Typography variant="subtitle2" gutterBottom>
            Période du {formatDate(dateDebut)} au {formatDate(dateFin)}
          </Typography>

          <TableContainer sx={{ mt: 2 }}>
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
                    <TableCell align="right">{formatCurrency(ligne.debit)}</TableCell>
                    <TableCell align="right">{formatCurrency(ligne.credit)}</TableCell>
                    <TableCell align="right">{formatCurrency(ligne.solde)}</TableCell>
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
                      {formatCurrency(lignes[lignes.length - 1]?.solde || 0)}
                    </Typography>
                  </TableCell>
                </TableRow>
              </TableBody>
            </Table>
          </TableContainer>
        </>
      )}

      {selectedCompte && lignes.length === 0 && !loading && (
        <Box sx={{ p: 2, textAlign: 'center' }}>
          <Typography variant="body1" color="text.secondary">
            Aucune écriture pour la période sélectionnée
          </Typography>
        </Box>
      )}
    </Paper>
  );
};

export default GrandLivre;
