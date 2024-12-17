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
  Typography,
  Box,
  Divider,
} from '@mui/material';
import { Balance } from '../../../types/comptabilite';
import { getBilan } from '../../../services/comptabilite';
import { formatCurrency, formatDate } from '../../../utils/format';

const Bilan: React.FC = () => {
  const [dateFin, setDateFin] = useState(
    new Date().toISOString().split('T')[0]
  );
  const [bilan, setBilan] = useState<Balance | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSearch = async () => {
    setLoading(true);
    try {
      const data = await getBilan(new Date(dateFin));
      setBilan(data);
    } catch (error) {
      console.error('Erreur lors du chargement du bilan:', error);
    } finally {
      setLoading(false);
    }
  };

  const renderSection = (section: Record<string, { libelle: string, montant: number }>) => {
    return Object.entries(section).map(([numero, compte]) => (
      <TableRow key={numero}>
        <TableCell>{numero}</TableCell>
        <TableCell>{compte.libelle}</TableCell>
        <TableCell align="right">{formatCurrency(compte.montant)}</TableCell>
      </TableRow>
    ));
  };

  return (
    <Paper sx={{ p: 2 }}>
      <Grid container spacing={2} sx={{ mb: 3 }}>
        <Grid item xs={12} md={9}>
          <TextField
            label="Date de fin d'exercice"
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
            Générer le Bilan
          </Button>
        </Grid>
      </Grid>

      {bilan && (
        <>
          <Typography variant="h6" gutterBottom>
            Bilan Comptable
          </Typography>
          <Typography variant="subtitle2" gutterBottom>
            Arrêté au {formatDate(dateFin)}
          </Typography>

          <Grid container spacing={3}>
            {/* Actif */}
            <Grid item xs={12} md={6}>
              <Typography variant="h6" sx={{ mb: 2 }}>Actif</Typography>
              <TableContainer>
                <Table size="small">
                  <TableHead>
                    <TableRow>
                      <TableCell>N° Compte</TableCell>
                      <TableCell>Libellé</TableCell>
                      <TableCell align="right">Montant</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {renderSection(bilan.actif)}
                    <TableRow>
                      <TableCell colSpan={2}>
                        <Typography variant="subtitle1">Total Actif</Typography>
                      </TableCell>
                      <TableCell align="right">
                        <Typography variant="subtitle1">
                          {formatCurrency(bilan.total_actif)}
                        </Typography>
                      </TableCell>
                    </TableRow>
                  </TableBody>
                </Table>
              </TableContainer>
            </Grid>

            {/* Passif */}
            <Grid item xs={12} md={6}>
              <Typography variant="h6" sx={{ mb: 2 }}>Passif</Typography>
              <TableContainer>
                <Table size="small">
                  <TableHead>
                    <TableRow>
                      <TableCell>N° Compte</TableCell>
                      <TableCell>Libellé</TableCell>
                      <TableCell align="right">Montant</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {renderSection(bilan.passif)}
                    <TableRow>
                      <TableCell colSpan={2}>
                        <Typography variant="subtitle1">Total Passif</Typography>
                      </TableCell>
                      <TableCell align="right">
                        <Typography variant="subtitle1">
                          {formatCurrency(bilan.total_passif)}
                        </Typography>
                      </TableCell>
                    </TableRow>
                  </TableBody>
                </Table>
              </TableContainer>
            </Grid>
          </Grid>

          <Divider sx={{ my: 3 }} />

          {/* Équilibre du Bilan */}
          <Grid container spacing={2}>
            <Grid item xs={12}>
              <Typography variant="h6">Équilibre du Bilan</Typography>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 2 }}>
                <Typography variant="subtitle1">Total Actif</Typography>
                <Typography variant="subtitle1">
                  {formatCurrency(bilan.total_actif)}
                </Typography>
              </Box>
              <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                <Typography variant="subtitle1">Total Passif</Typography>
                <Typography variant="subtitle1">
                  {formatCurrency(bilan.total_passif)}
                </Typography>
              </Box>
              <Divider sx={{ my: 1 }} />
              <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                <Typography variant="h6">Écart</Typography>
                <Typography 
                  variant="h6" 
                  color={
                    Math.abs(bilan.total_actif - bilan.total_passif) < 0.01 
                      ? 'primary' 
                      : 'error'
                  }
                >
                  {formatCurrency(Math.abs(bilan.total_actif - bilan.total_passif))}
                </Typography>
              </Box>
            </Grid>
          </Grid>
        </>
      )}

      {!bilan && !loading && (
        <Box sx={{ p: 2, textAlign: 'center' }}>
          <Typography variant="body1" color="text.secondary">
            Sélectionnez une date pour générer le bilan
          </Typography>
        </Box>
      )}
    </Paper>
  );
};

export default Bilan;
