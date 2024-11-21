import React, { useState } from 'react';
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Chip,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Box,
  Typography,
  LinearProgress
} from '@mui/material';
import { useQuery } from '@tanstack/react-query';
import { getMouvements } from '../../services/inventaire';
import type { MouvementStock } from '../../types/inventaire';
import { format } from 'date-fns';
import { fr } from 'date-fns/locale';

const HistoriqueMouvements: React.FC = () => {
  const [typeFilter, setTypeFilter] = useState<string>('TOUS');

  const { data: mouvements, isLoading, error } = useQuery(
    ['mouvements', typeFilter],
    () => getMouvements({
      type: typeFilter === 'TOUS' ? undefined : typeFilter as 'ENTREE' | 'SORTIE'
    })
  );

  if (isLoading) {
    return <LinearProgress />;
  }

  if (error) {
    return (
      <Typography color="error">
        Erreur lors du chargement de l'historique des mouvements
      </Typography>
    );
  }

  const filteredMouvements = mouvements || [];

  return (
    <>
      <Box mb={3} display="flex" gap={2}>
        <FormControl variant="outlined" size="small" sx={{ minWidth: 200 }}>
          <InputLabel>Type de Mouvement</InputLabel>
          <Select
            value={typeFilter}
            onChange={(e) => setTypeFilter(e.target.value as string)}
            label="Type de Mouvement"
          >
            <MenuItem value="TOUS">Tous les mouvements</MenuItem>
            <MenuItem value="ENTREE">Entrées</MenuItem>
            <MenuItem value="SORTIE">Sorties</MenuItem>
          </Select>
        </FormControl>
      </Box>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Date</TableCell>
              <TableCell>Type</TableCell>
              <TableCell>Produit</TableCell>
              <TableCell align="right">Quantité</TableCell>
              <TableCell align="right">Coût Unitaire</TableCell>
              <TableCell>Référence</TableCell>
              <TableCell>Responsable</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {filteredMouvements.map((mouvement) => (
              <TableRow key={mouvement.id}>
                <TableCell>
                  {format(new Date(mouvement.date_mouvement), 'Pp', { locale: fr })}
                </TableCell>
                <TableCell>
                  <Chip
                    label={mouvement.type_mouvement}
                    color={mouvement.type_mouvement === 'ENTREE' ? 'success' : 'error'}
                    size="small"
                  />
                </TableCell>
                <TableCell>{mouvement.produit.nom}</TableCell>
                <TableCell align="right">
                  {mouvement.quantite} {mouvement.produit.unite_mesure}
                </TableCell>
                <TableCell align="right">
                  {mouvement.cout_unitaire
                    ? new Intl.NumberFormat('fr-FR', {
                        style: 'currency',
                        currency: 'XAF'
                      }).format(mouvement.cout_unitaire)
                    : '-'}
                </TableCell>
                <TableCell>{mouvement.reference_document || '-'}</TableCell>
                <TableCell>
                  {mouvement.responsable.prenom} {mouvement.responsable.nom}
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </>
  );
};

export default HistoriqueMouvements;
