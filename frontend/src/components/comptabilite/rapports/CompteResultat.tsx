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
import { CompteResultatType } from '../../../types/comptabilite';
import { getCompteResultat } from '../../../services/comptabilite';
import { formatCurrency, formatDate } from '../../../utils/format';

const CompteResultat: React.FC = () => {
  const [dateDebut, setDateDebut] = useState<string>(
    new Date(new Date().getFullYear(), 0, 1)
      .toISOString()
      .split('T')[0]
  );
  const [dateFin, setDateFin] = useState<string>(
    new Date().toISOString().split('T')[0]
  );
  const [compteResultat, setCompteResultat] = useState<CompteResultatType | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSearch = async () => {
    setLoading(true);
    try {
      const data = await getCompteResultat(new Date(dateDebut), new Date(dateFin));
      setCompteResultat(data);
    } catch (error) {
      console.error('Erreur lors du chargement du compte de résultat:', error);
    } finally {
      setLoading(false);
    }
  };

  const renderSection = (section: Record<string, { libelle: string; montant: number }>) => {
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
        <Grid item xs={12} md={4}>
          <TextField
            label="Date début"
            type="date"
            value={dateDebut}
            onChange={(e) => setDateDebut(e.target.value)}
            fullWidth
          />
        </Grid>
        <Grid item xs={12} md={4}>
          <TextField
            label="Date fin"
            type="date"
            value={dateFin}
            onChange={(e) => setDateFin(e.target.value)}
            fullWidth
          />
        </Grid>
        <Grid item xs={12} md={4}>
          <Button
            variant="contained"
            onClick={handleSearch}
            disabled={loading}
            fullWidth
            sx={{ height: '100%' }}
          >
            Générer le Compte de Résultat
          </Button>
        </Grid>
      </Grid>

      {compteResultat && (
        <>
          <Typography variant="h6" gutterBottom>
            Compte de Résultat
          </Typography>
          <Typography variant="subtitle2" gutterBottom>
            Du {formatDate(dateDebut)} au {formatDate(dateFin)}
          </Typography>

          <Grid container spacing={3}>
            {/* Produits */}
            <Grid item xs={12} md={6}>
              <Typography variant="h6" sx={{ mb: 2 }}>Produits</Typography>
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
                    {renderSection(compteResultat.produits)}
                    <TableRow>
                      <TableCell colSpan={2}>
                        <Typography variant="subtitle1">Total Produits</Typography>
                      </TableCell>
                      <TableCell align="right">
                        <Typography variant="subtitle1">
                          {formatCurrency(compteResultat.total_produits)}
                        </Typography>
                      </TableCell>
                    </TableRow>
                  </TableBody>
                </Table>
              </TableContainer>
            </Grid>

            {/* Charges */}
            <Grid item xs={12} md={6}>
              <Typography variant="h6" sx={{ mb: 2 }}>Charges</Typography>
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
                    {renderSection(compteResultat.charges)}
                    <TableRow>
                      <TableCell colSpan={2}>
                        <Typography variant="subtitle1">Total Charges</Typography>
                      </TableCell>
                      <TableCell align="right">
                        <Typography variant="subtitle1">
                          {formatCurrency(compteResultat.total_charges)}
                        </Typography>
                      </TableCell>
                    </TableRow>
                  </TableBody>
                </Table>
              </TableContainer>
            </Grid>
          </Grid>

          <Divider sx={{ my: 3 }} />

          {/* Résultat Net */}
          <Grid container spacing={2}>
            <Grid item xs={12}>
              <Typography variant="h6">Résultat Net</Typography>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 2 }}>
                <Typography variant="subtitle1">Total Produits</Typography>
                <Typography variant="subtitle1">
                  {formatCurrency(compteResultat.total_produits)}
                </Typography>
              </Box>
              <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                <Typography variant="subtitle1">Total Charges</Typography>
                <Typography variant="subtitle1">
                  {formatCurrency(compteResultat.total_charges)}
                </Typography>
              </Box>
              <Divider sx={{ my: 1 }} />
              <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                <Typography variant="h6">Résultat Net</Typography>
                <Typography 
                  variant="h6" 
                  color={compteResultat.resultat_net >= 0 ? 'primary' : 'error'}
                >
                  {formatCurrency(compteResultat.resultat_net)}
                </Typography>
              </Box>
              <Typography 
                variant="body2" 
                color={compteResultat.resultat_net >= 0 ? 'primary' : 'error'}
                sx={{ textAlign: 'right', mt: 1 }}
              >
                {compteResultat.resultat_net >= 0 
                  ? 'Bénéfice' 
                  : 'Perte'}
              </Typography>
            </Grid>
          </Grid>
        </>
      )}

      {!compteResultat && !loading && (
        <Box sx={{ p: 2, textAlign: 'center' }}>
          <Typography variant="body1" color="text.secondary">
            Sélectionnez une période pour générer le compte de résultat
          </Typography>
        </Box>
      )}
    </Paper>
  );
};

export default CompteResultat;
