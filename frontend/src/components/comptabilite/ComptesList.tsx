import React, { useState, useEffect } from 'react';
import {
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  IconButton,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  MenuItem,
  Grid,
} from '@mui/material';
import { Edit, Delete } from '@mui/icons-material';
import { CompteComptable, TypeCompte, CompteComptableFormData } from '../../types/comptabilite';
import { getComptes, createCompte, updateCompte } from '../../services/comptabilite';
import { formatCurrency } from '../../utils/format';

const TYPES_COMPTE = ['ACTIF', 'PASSIF', 'CHARGE', 'PRODUIT'] as const;

const ComptesList: React.FC = () => {
  const [comptes, setComptes] = useState<CompteComptable[]>([]);
  const [openDialog, setOpenDialog] = useState(false);
  const [selectedCompte, setSelectedCompte] = useState<CompteComptable | null>(null);
  const [formData, setFormData] = useState<CompteComptableFormData>({
    numero: '',
    libelle: '',
    type_compte: 'ACTIF',
    description: ''
  });

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

  const handleOpenDialog = (compte?: CompteComptable) => {
    if (compte) {
      setSelectedCompte(compte);
      setFormData({
        numero: compte.numero,
        libelle: compte.libelle,
        type_compte: compte.type_compte,
        description: compte.description || ''
      });
    } else {
      setSelectedCompte(null);
      setFormData({
        numero: '',
        libelle: '',
        type_compte: 'ACTIF',
        description: ''
      });
    }
    setOpenDialog(true);
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
    setSelectedCompte(null);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (selectedCompte) {
        await updateCompte(selectedCompte.id, formData);
      } else {
        await createCompte(formData);
      }
      handleCloseDialog();
      loadComptes();
    } catch (error) {
      console.error('Erreur lors de la sauvegarde:', error);
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  return (
    <>
      <Grid container spacing={2} sx={{ mb: 3 }}>
        <Grid item xs={12}>
          <Button
            variant="contained"
            color="primary"
            onClick={() => handleOpenDialog()}
          >
            Nouveau Compte
          </Button>
        </Grid>
      </Grid>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Numéro</TableCell>
              <TableCell>Libellé</TableCell>
              <TableCell>Type</TableCell>
              <TableCell align="right">Solde Débit</TableCell>
              <TableCell align="right">Solde Crédit</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {comptes.map((compte) => (
              <TableRow key={compte.id}>
                <TableCell>{compte.numero}</TableCell>
                <TableCell>{compte.libelle}</TableCell>
                <TableCell>{compte.type_compte}</TableCell>
                <TableCell align="right">{formatCurrency(compte.solde_debit)}</TableCell>
                <TableCell align="right">{formatCurrency(compte.solde_credit)}</TableCell>
                <TableCell>
                  <IconButton onClick={() => handleOpenDialog(compte)} size="small">
                    <Edit />
                  </IconButton>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      <Dialog open={openDialog} onClose={handleCloseDialog} maxWidth="sm" fullWidth>
        <form onSubmit={handleSubmit}>
          <DialogTitle>
            {selectedCompte ? 'Modifier le Compte' : 'Nouveau Compte'}
          </DialogTitle>
          <DialogContent>
            <Grid container spacing={2} sx={{ mt: 1 }}>
              <Grid item xs={12} md={6}>
                <TextField
                  name="numero"
                  label="Numéro"
                  value={formData.numero}
                  onChange={handleInputChange}
                  fullWidth
                  required
                  disabled={!!selectedCompte}
                />
              </Grid>
              <Grid item xs={12} md={6}>
                <TextField
                  name="type_compte"
                  label="Type"
                  value={formData.type_compte}
                  onChange={handleInputChange}
                  select
                  fullWidth
                  required
                >
                  {TYPES_COMPTE.map((type) => (
                    <MenuItem key={type} value={type}>
                      {type}
                    </MenuItem>
                  ))}
                </TextField>
              </Grid>
              <Grid item xs={12}>
                <TextField
                  name="libelle"
                  label="Libellé"
                  value={formData.libelle}
                  onChange={handleInputChange}
                  fullWidth
                  required
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  name="description"
                  label="Description"
                  value={formData.description}
                  onChange={handleInputChange}
                  fullWidth
                  multiline
                  rows={3}
                />
              </Grid>
            </Grid>
          </DialogContent>
          <DialogActions>
            <Button onClick={handleCloseDialog}>Annuler</Button>
            <Button type="submit" variant="contained" color="primary">
              {selectedCompte ? 'Modifier' : 'Créer'}
            </Button>
          </DialogActions>
        </form>
      </Dialog>
    </>
  );
};

export default ComptesList;
