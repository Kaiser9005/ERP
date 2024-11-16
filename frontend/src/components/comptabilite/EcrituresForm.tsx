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
  IconButton,
  MenuItem,
  Typography,
  Alert,
} from '@mui/material';
import { Add as AddIcon, Delete as DeleteIcon } from '@mui/icons-material';
import { 
  EcritureComptableFormData,
  CompteComptable,
  JournalComptable
} from '../../types/comptabilite';
import { 
  getComptes,
  getJournaux,
  createEcriture
} from '../../services/comptabilite';
import { formatCurrency } from '../../utils/format';

interface LigneEcriture {
  compte_id: string;
  libelle: string;
  debit: number;
  credit: number;
}

const EcrituresForm: React.FC = () => {
  const [comptes, setComptes] = useState<CompteComptable[]>([]);
  const [journaux, setJournaux] = useState<JournalComptable[]>([]);
  const [lignes, setLignes] = useState<LigneEcriture[]>([
    { compte_id: '', libelle: '', debit: 0, credit: 0 }
  ]);
  const [journal_id, setJournalId] = useState('');
  const [date_ecriture, setDateEcriture] = useState(
    new Date().toISOString().split('T')[0]
  );
  const [numero_piece, setNumeroPiece] = useState('');
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadInitialData();
  }, []);

  const loadInitialData = async () => {
    try {
      const [comptesData, journauxData] = await Promise.all([
        getComptes(),
        getJournaux()
      ]);
      setComptes(comptesData);
      setJournaux(journauxData);
    } catch (error) {
      console.error('Erreur lors du chargement des données:', error);
      setError('Erreur lors du chargement des données');
    }
  };

  const handleAddLigne = () => {
    setLignes([...lignes, { compte_id: '', libelle: '', debit: 0, credit: 0 }]);
  };

  const handleRemoveLigne = (index: number) => {
    setLignes(lignes.filter((_, i) => i !== index));
  };

  const handleLigneChange = (index: number, field: keyof LigneEcriture, value: string | number) => {
    const newLignes = [...lignes];
    newLignes[index] = {
      ...newLignes[index],
      [field]: field === 'compte_id' || field === 'libelle' ? value : parseFloat(value as string) || 0
    };
    setLignes(newLignes);
  };

  const validateEcriture = (): boolean => {
    // Vérification des champs obligatoires
    if (!journal_id || !date_ecriture || !numero_piece) {
      setError('Veuillez remplir tous les champs obligatoires');
      return false;
    }

    // Vérification de l'équilibre débit/crédit
    const totalDebit = lignes.reduce((sum, ligne) => sum + ligne.debit, 0);
    const totalCredit = lignes.reduce((sum, ligne) => sum + ligne.credit, 0);

    if (totalDebit !== totalCredit) {
      setError('L\'écriture n\'est pas équilibrée');
      return false;
    }

    // Vérification des lignes
    const lignesValides = lignes.every(ligne => 
      ligne.compte_id && 
      ligne.libelle && 
      (ligne.debit > 0 || ligne.credit > 0)
    );

    if (!lignesValides) {
      setError('Veuillez remplir correctement toutes les lignes');
      return false;
    }

    setError(null);
    return true;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateEcriture()) {
      return;
    }

    try {
      // Création des écritures
      for (const ligne of lignes) {
        await createEcriture({
          date_ecriture,
          numero_piece,
          journal_id,
          compte_id: ligne.compte_id,
          libelle: ligne.libelle,
          debit: ligne.debit,
          credit: ligne.credit
        });
      }

      // Réinitialisation du formulaire
      setLignes([{ compte_id: '', libelle: '', debit: 0, credit: 0 }]);
      setNumeroPiece('');
      setError(null);
    } catch (error) {
      console.error('Erreur lors de la création des écritures:', error);
      setError('Erreur lors de la création des écritures');
    }
  };

  const totalDebit = lignes.reduce((sum, ligne) => sum + ligne.debit, 0);
  const totalCredit = lignes.reduce((sum, ligne) => sum + ligne.credit, 0);

  return (
    <Paper sx={{ p: 2 }}>
      <form onSubmit={handleSubmit}>
        <Grid container spacing={2}>
          {error && (
            <Grid item xs={12}>
              <Alert severity="error">{error}</Alert>
            </Grid>
          )}

          <Grid item xs={12} md={4}>
            <TextField
              label="Journal"
              select
              fullWidth
              value={journal_id}
              onChange={(e) => setJournalId(e.target.value)}
              required
            >
              {journaux.map((journal) => (
                <MenuItem key={journal.id} value={journal.id}>
                  {journal.code} - {journal.libelle}
                </MenuItem>
              ))}
            </TextField>
          </Grid>

          <Grid item xs={12} md={4}>
            <TextField
              label="Date"
              type="date"
              fullWidth
              value={date_ecriture}
              onChange={(e) => setDateEcriture(e.target.value)}
              required
            />
          </Grid>

          <Grid item xs={12} md={4}>
            <TextField
              label="N° Pièce"
              fullWidth
              value={numero_piece}
              onChange={(e) => setNumeroPiece(e.target.value)}
              required
            />
          </Grid>

          <Grid item xs={12}>
            <TableContainer>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Compte</TableCell>
                    <TableCell>Libellé</TableCell>
                    <TableCell align="right">Débit</TableCell>
                    <TableCell align="right">Crédit</TableCell>
                    <TableCell></TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {lignes.map((ligne, index) => (
                    <TableRow key={index}>
                      <TableCell>
                        <TextField
                          select
                          fullWidth
                          value={ligne.compte_id}
                          onChange={(e) => handleLigneChange(index, 'compte_id', e.target.value)}
                          required
                        >
                          {comptes.map((compte) => (
                            <MenuItem key={compte.id} value={compte.id}>
                              {compte.numero} - {compte.libelle}
                            </MenuItem>
                          ))}
                        </TextField>
                      </TableCell>
                      <TableCell>
                        <TextField
                          fullWidth
                          value={ligne.libelle}
                          onChange={(e) => handleLigneChange(index, 'libelle', e.target.value)}
                          required
                        />
                      </TableCell>
                      <TableCell align="right">
                        <TextField
                          type="number"
                          value={ligne.debit || ''}
                          onChange={(e) => handleLigneChange(index, 'debit', e.target.value)}
                          inputProps={{ min: 0, step: 0.01 }}
                        />
                      </TableCell>
                      <TableCell align="right">
                        <TextField
                          type="number"
                          value={ligne.credit || ''}
                          onChange={(e) => handleLigneChange(index, 'credit', e.target.value)}
                          inputProps={{ min: 0, step: 0.01 }}
                        />
                      </TableCell>
                      <TableCell>
                        {lignes.length > 1 && (
                          <IconButton onClick={() => handleRemoveLigne(index)} size="small">
                            <DeleteIcon />
                          </IconButton>
                        )}
                      </TableCell>
                    </TableRow>
                  ))}
                  <TableRow>
                    <TableCell colSpan={2}>
                      <Typography variant="subtitle1">Total</Typography>
                    </TableCell>
                    <TableCell align="right">
                      <Typography variant="subtitle1">{formatCurrency(totalDebit)}</Typography>
                    </TableCell>
                    <TableCell align="right">
                      <Typography variant="subtitle1">{formatCurrency(totalCredit)}</Typography>
                    </TableCell>
                    <TableCell></TableCell>
                  </TableRow>
                </TableBody>
              </Table>
            </TableContainer>
          </Grid>

          <Grid item xs={12}>
            <Button
              startIcon={<AddIcon />}
              onClick={handleAddLigne}
              sx={{ mr: 1 }}
            >
              Ajouter une ligne
            </Button>
            <Button
              type="submit"
              variant="contained"
              color="primary"
              disabled={totalDebit !== totalCredit}
            >
              Enregistrer l'écriture
            </Button>
          </Grid>
        </Grid>
      </form>
    </Paper>
  );
};

export default EcrituresForm;
