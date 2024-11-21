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
import { getStocks } from '../../services/inventaire';
import type { Stock } from '../../types/inventaire';

const ListeStock: React.FC = () => {
  const [categorieFilter, setCategorieFilter] = useState<string>('TOUS');
  const [seuilFilter, setSeuilFilter] = useState<string>('TOUS');

  const { data: stocks, isLoading, error } = useQuery(
    ['stocks', categorieFilter, seuilFilter],
    () => getStocks({
      categorie: categorieFilter === 'TOUS' ? undefined : categorieFilter,
      seuil_alerte: seuilFilter === 'TOUS' ? undefined : seuilFilter === 'SOUS_SEUIL'
    })
  );

  if (isLoading) {
    return <LinearProgress />;
  }

  if (error) {
    return (
      <Typography color="error">
        Erreur lors du chargement des stocks
      </Typography>
    );
  }

  const filteredStocks = stocks || [];

  return (
    <>
      <Box mb={3} display="flex" gap={2}>
        <FormControl variant="outlined" size="small" sx={{ minWidth: 200 }}>
          <InputLabel>Catégorie</InputLabel>
          <Select
            value={categorieFilter}
            onChange={(e) => setCategorieFilter(e.target.value as string)}
            label="Catégorie"
          >
            <MenuItem value="TOUS">Toutes les catégories</MenuItem>
            <MenuItem value="INTRANT">Intrants</MenuItem>
            <MenuItem value="MATERIEL">Matériel</MenuItem>
            <MenuItem value="PRODUIT">Produits</MenuItem>
          </Select>
        </FormControl>

        <FormControl variant="outlined" size="small" sx={{ minWidth: 200 }}>
          <InputLabel>Niveau de Stock</InputLabel>
          <Select
            value={seuilFilter}
            onChange={(e) => setSeuilFilter(e.target.value as string)}
            label="Niveau de Stock"
          >
            <MenuItem value="TOUS">Tous les niveaux</MenuItem>
            <MenuItem value="SOUS_SEUIL">Sous le seuil d'alerte</MenuItem>
            <MenuItem value="AU_DESSUS">Au-dessus du seuil</MenuItem>
          </Select>
        </FormControl>
      </Box>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Code</TableCell>
              <TableCell>Nom</TableCell>
              <TableCell>Catégorie</TableCell>
              <TableCell align="right">Quantité</TableCell>
              <TableCell align="right">Seuil d'Alerte</TableCell>
              <TableCell align="right">Valeur Unitaire</TableCell>
              <TableCell>Statut</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {filteredStocks.map((stock) => {
              const sousSeuilAlerte = stock.quantite <= stock.produit.seuil_alerte;
              return (
                <TableRow key={stock.id}>
                  <TableCell>{stock.produit.code}</TableCell>
                  <TableCell>{stock.produit.nom}</TableCell>
                  <TableCell>{stock.produit.categorie}</TableCell>
                  <TableCell align="right">
                    {stock.quantite} {stock.produit.unite_mesure}
                  </TableCell>
                  <TableCell align="right">
                    {stock.produit.seuil_alerte} {stock.produit.unite_mesure}
                  </TableCell>
                  <TableCell align="right">
                    {new Intl.NumberFormat('fr-FR', {
                      style: 'currency',
                      currency: 'XAF'
                    }).format(stock.valeur_unitaire)}
                  </TableCell>
                  <TableCell>
                    <Chip
                      label={sousSeuilAlerte ? 'Sous Seuil' : 'Normal'}
                      color={sousSeuilAlerte ? 'error' : 'success'}
                      size="small"
                    />
                  </TableCell>
                </TableRow>
              );
            })}
          </TableBody>
        </Table>
      </TableContainer>
    </>
  );
};

export default ListeStock;
