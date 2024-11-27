import React, { useState } from 'react';
import {
  Card,
  CardContent,
  Typography,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  Box,
  TextField,
  InputAdornment,
  IconButton,
  LinearProgress,
  CircularProgress,
  TablePagination,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  TableSortLabel,
  Tooltip
} from '@mui/material';
import { Edit, Search, Add } from '@mui/icons-material';
import { useQuery } from 'react-query';
import { getStocks } from '../../services/inventaire';
import DialogueMouvementStock from './DialogueMouvementStock';
import { Stock, Produit, CategoryProduit } from '../../types/inventaire';

type SortField = 'code' | 'nom' | 'quantite' | 'valeur';
type SortOrder = 'asc' | 'desc';

const ROWS_PER_PAGE_OPTIONS = [10, 25, 50];

const ListeStock: React.FC = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedProduct, setSelectedProduct] = useState<string | null>(null);
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [selectedCategory, setSelectedCategory] = useState<CategoryProduit | ''>('');
  const [sortField, setSortField] = useState<SortField>('code');
  const [sortOrder, setSortOrder] = useState<SortOrder>('asc');

  const { data: stocks = [], isLoading, isError } = useQuery<(Stock & { produit: Produit })[]>('stocks', getStocks);

  const handleSort = (field: SortField) => {
    if (field === sortField) {
      setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc');
    } else {
      setSortField(field);
      setSortOrder('asc');
    }
  };

  const filteredStocks = stocks
    .filter(stock => 
      (stock.produit.nom.toLowerCase().includes(searchTerm.toLowerCase()) ||
      stock.produit.code.toLowerCase().includes(searchTerm.toLowerCase())) &&
      (!selectedCategory || stock.produit.categorie === selectedCategory)
    )
    .sort((a, b) => {
      const compareValue = (va: any, vb: any) => {
        if (va < vb) return sortOrder === 'asc' ? -1 : 1;
        if (va > vb) return sortOrder === 'asc' ? 1 : -1;
        return 0;
      };

      switch (sortField) {
        case 'code':
          return compareValue(a.produit.code, b.produit.code);
        case 'nom':
          return compareValue(a.produit.nom, b.produit.nom);
        case 'quantite':
          return compareValue(a.quantite, b.quantite);
        case 'valeur':
          return compareValue(a.valeur_unitaire * a.quantite, b.valeur_unitaire * b.quantite);
        default:
          return 0;
      }
    });

  const getStockLevel = (current: number, threshold: number) => {
    const ratio = current / threshold;
    if (ratio <= 0.25) return 'error';
    if (ratio <= 0.5) return 'warning';
    return 'success';
  };

  const getStockLevelLabel = (current: number, threshold: number) => {
    const ratio = current / threshold;
    if (ratio <= 0.25) return 'Stock critique';
    if (ratio <= 0.5) return 'Stock faible';
    return 'Stock normal';
  };

  if (isLoading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px" data-testid="chargement-stocks">
        <CircularProgress aria-label="Chargement des stocks" />
        <Typography sx={{ ml: 2 }}>Chargement des stocks en cours...</Typography>
      </Box>
    );
  }

  if (isError) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px" data-testid="erreur-stocks">
        <Typography color="error">
          Une erreur est survenue lors du chargement des stocks. Veuillez réessayer plus tard.
        </Typography>
      </Box>
    );
  }

  return (
    <Card>
      <CardContent>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3, gap: 2 }}>
          <Typography variant="h6" component="h1">État des Stocks</Typography>
          <Box sx={{ display: 'flex', gap: 2 }}>
            <FormControl size="small" sx={{ minWidth: 150 }}>
              <InputLabel id="categorie-select-label">Catégorie</InputLabel>
              <Select
                labelId="categorie-select-label"
                value={selectedCategory}
                label="Catégorie"
                onChange={(e) => setSelectedCategory(e.target.value as CategoryProduit | '')}
                data-testid="filtre-categorie"
              >
                <MenuItem value="">Toutes les catégories</MenuItem>
                {Object.values(CategoryProduit).map((cat) => (
                  <MenuItem key={cat} value={cat}>{cat}</MenuItem>
                ))}
              </Select>
            </FormControl>
            <TextField
              size="small"
              placeholder="Rechercher un produit..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <Search aria-hidden="true" />
                  </InputAdornment>
                ),
              }}
              aria-label="Rechercher un produit"
            />
          </Box>
        </Box>

        <Table data-testid="table-stocks" aria-label="Liste des stocks">
          <TableHead>
            <TableRow>
              <TableCell>
                <TableSortLabel
                  active={sortField === 'code'}
                  direction={sortField === 'code' ? sortOrder : 'asc'}
                  onClick={() => handleSort('code')}
                >
                  Code
                </TableSortLabel>
              </TableCell>
              <TableCell>
                <TableSortLabel
                  active={sortField === 'nom'}
                  direction={sortField === 'nom' ? sortOrder : 'asc'}
                  onClick={() => handleSort('nom')}
                >
                  Produit
                </TableSortLabel>
              </TableCell>
              <TableCell align="right">
                <TableSortLabel
                  active={sortField === 'quantite'}
                  direction={sortField === 'quantite' ? sortOrder : 'asc'}
                  onClick={() => handleSort('quantite')}
                >
                  Quantité
                </TableSortLabel>
              </TableCell>
              <TableCell align="right">
                <TableSortLabel
                  active={sortField === 'valeur'}
                  direction={sortField === 'valeur' ? sortOrder : 'asc'}
                  onClick={() => handleSort('valeur')}
                >
                  Valeur
                </TableSortLabel>
              </TableCell>
              <TableCell align="right">Niveau de stock</TableCell>
              <TableCell align="right">Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {filteredStocks
              .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
              .map((stock) => (
                <TableRow key={stock.id} data-testid={`stock-${stock.id}`}>
                  <TableCell>{stock.produit.code}</TableCell>
                  <TableCell>{stock.produit.nom}</TableCell>
                  <TableCell align="right">
                    {stock.quantite} {stock.produit.unite_mesure}
                  </TableCell>
                  <TableCell align="right">
                    {new Intl.NumberFormat('fr-FR', {
                      style: 'currency',
                      currency: 'XAF'
                    }).format(stock.valeur_unitaire * stock.quantite)}
                  </TableCell>
                  <TableCell align="right">
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      <Tooltip title={getStockLevelLabel(stock.quantite, stock.produit.seuil_alerte)}>
                        <LinearProgress
                          variant="determinate"
                          value={(stock.quantite / stock.produit.seuil_alerte) * 100}
                          color={getStockLevel(stock.quantite, stock.produit.seuil_alerte)}
                          sx={{ flexGrow: 1 }}
                          data-testid={`statut-${stock.id}`}
                          aria-label={`Niveau de stock: ${Math.round((stock.quantite / stock.produit.seuil_alerte) * 100)}%`}
                        />
                      </Tooltip>
                      <Typography variant="body2">
                        {Math.round((stock.quantite / stock.produit.seuil_alerte) * 100)}%
                      </Typography>
                    </Box>
                  </TableCell>
                  <TableCell align="right">
                    <Tooltip title="Ajouter un mouvement">
                      <IconButton
                        size="small"
                        onClick={() => setSelectedProduct(stock.id)}
                        aria-label={`Ajouter un mouvement pour ${stock.produit.nom}`}
                      >
                        <Add />
                      </IconButton>
                    </Tooltip>
                    <Tooltip title="Modifier le produit">
                      <IconButton 
                        size="small"
                        aria-label={`Modifier ${stock.produit.nom}`}
                      >
                        <Edit />
                      </IconButton>
                    </Tooltip>
                  </TableCell>
                </TableRow>
            ))}
          </TableBody>
        </Table>

        <TablePagination
          component="div"
          count={filteredStocks.length}
          page={page}
          onPageChange={(_, newPage) => setPage(newPage)}
          rowsPerPage={rowsPerPage}
          onRowsPerPageChange={(e) => {
            setRowsPerPage(parseInt(e.target.value, 10));
            setPage(0);
          }}
          rowsPerPageOptions={ROWS_PER_PAGE_OPTIONS}
          labelRowsPerPage="Lignes par page"
          labelDisplayedRows={({ from, to, count }) => `${from}-${to} sur ${count}`}
          getItemAriaLabel={(type) => {
            if (type === 'first') return 'Aller à la première page';
            if (type === 'last') return 'Aller à la dernière page';
            if (type === 'next') return 'Aller à la page suivante';
            return 'Aller à la page précédente';
          }}
        />

        <DialogueMouvementStock
          open={!!selectedProduct}
          onClose={() => setSelectedProduct(null)}
          productId={selectedProduct}
        />
      </CardContent>
    </Card>
  );
};

export default ListeStock;
