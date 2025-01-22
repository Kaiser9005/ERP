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
  Grid,
  Typography,
  Box,
} from '@mui/material';
import { Visibility } from '@mui/icons-material';
import { JournalComptable, EcritureComptable } from '../../types/comptabilite';
import { getJournaux, getJournalEcritures } from '../../services/comptabilite';
import { formatCurrency, formatDate } from '../../utils/format';

const JournauxList: React.FC = () => {
  const [journaux, setJournaux] = useState<JournalComptable[]>([]);
  const [selectedJournal, setSelectedJournal] = useState<JournalComptable | null>(null);
  const [ecritures, setEcritures] = useState<EcritureComptable[]>([]);
  const [openDialog, setOpenDialog] = useState(false);
  const [dateDebut, setDateDebut] = useState(
    new Date(new Date().getFullYear(), new Date().getMonth(), 1)
      .toISOString()
      .split('T')[0]
  );
  const [dateFin, setDateFin] = useState(
    new Date().toISOString().split('T')[0]
  );

  useEffect(() => {
    loadJournaux();
  }, []);

  const loadJournaux = async () => {
    try {
      const data = await getJournaux();
      setJournaux(data);
    } catch (error) {
      console.error('Erreur lors du chargement des journaux:', error);
    }
  };

  const handleOpenDialog = async (journal: JournalComptable) => {
    setSelectedJournal(journal);
    try {
      const data = await getJournalEcritures(journal.id, {
        date_debut: new Date(dateDebut),
        date_fin: new Date(dateFin)
      });
      const ecrituresData: EcritureComptable[] = data;
      setEcritures(ecrituresData);
      setOpenDialog(true);
    } catch (error) {
      console.error('Erreur lors du chargement des écritures:', error);
    }
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
    setSelectedJournal(null);
    setEcritures([]);
  };

  const handleDateChange = async () => {
    if (selectedJournal) {
      try {
        const data = await getJournalEcritures(selectedJournal.id, {
          date_debut: new Date(dateDebut),
          date_fin: new Date(dateFin)
        });
        const ecrituresData: EcritureComptable[] = data;
        setEcritures(ecrituresData);
      } catch (error) {
        console.error('Erreur lors du chargement des écritures:', error);
      }
    }
  };

  const calculateTotals = () => {
    let totalDebit = 0;
    let totalCredit = 0;
  
    ecritures.forEach((ecriture) => {
      ecriture.lignes.forEach((ligne) => {
        totalDebit += ligne.debit;
        totalCredit += ligne.credit;
      });
    });
  
    return { debit: totalDebit, credit: totalCredit };
  };

  return (
    <>
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Code</TableCell>
              <TableCell>Libellé</TableCell>
              <TableCell>Type</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {journaux.map((journal) => (
              <TableRow key={journal.id}>
                <TableCell>{journal.code}</TableCell>
                <TableCell>{journal.libelle}</TableCell>
                <TableCell>{journal.type}</TableCell>
                <TableCell>
                  <IconButton 
                    onClick={() => handleOpenDialog(journal)}
                    size="small"
                    title="Consulter le journal"
                  >
                    <Visibility />
                  </IconButton>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      <Dialog 
        open={openDialog} 
        onClose={handleCloseDialog}
        maxWidth="lg"
        fullWidth
      >
        <DialogTitle>
          Journal {selectedJournal?.code} - {selectedJournal?.libelle}
        </DialogTitle>
        <DialogContent>
          <Grid container spacing={2} sx={{ mb: 2, mt: 1 }}>
            <Grid item xs={12} md={5}>
              <TextField
                label="Date début"
                type="date"
                value={dateDebut}
                onChange={(e) => setDateDebut(e.target.value)}
                fullWidth
              />
            </Grid>
            <Grid item xs={12} md={5}>
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
                onClick={handleDateChange}
                fullWidth
                sx={{ height: '100%' }}
              >
                Actualiser
              </Button>
            </Grid>
          </Grid>

          <TableContainer>
            <Table size="small">
              <TableHead>
                <TableRow>
                  <TableCell>Date</TableCell>
                  <TableCell>N° Pièce</TableCell>
                  <TableCell>Compte</TableCell>
                  <TableCell>Libellé</TableCell>
                  <TableCell align="right">Débit</TableCell>
                  <TableCell align="right">Crédit</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
              {ecritures.map((ecriture) => (
                ecriture.lignes.map((ligne, index) => (
                  <TableRow key={`${ecriture.id}-${index}`}>
                    <TableCell>{formatDate(ecriture.date_ecriture)}</TableCell>
                    <TableCell>{}</TableCell> {/* Mettre à jour si le type EcritureComptable est modifié pour inclure numero_piece */}
                    <TableCell>{ligne.compte_id}</TableCell>
                    <TableCell>{ligne.libelle}</TableCell>
                    <TableCell align="right">{formatCurrency(ligne.debit)}</TableCell>
                    <TableCell align="right">{formatCurrency(ligne.credit)}</TableCell>
                  </TableRow>
                ))
              ))}
                {ecritures.length > 0 && (
                  <TableRow>
                    <TableCell colSpan={4}>
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
                  </TableRow>
                )}
              </TableBody>
            </Table>
          </TableContainer>

          {ecritures.length === 0 && (
            <Box sx={{ p: 2, textAlign: 'center' }}>
              <Typography variant="body1" color="text.secondary">
                Aucune écriture pour la période sélectionnée
              </Typography>
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>Fermer</Button>
        </DialogActions>
      </Dialog>
    </>
  );
};

export default JournauxList;
