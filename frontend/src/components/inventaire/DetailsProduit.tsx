import React, { useState } from 'react';
import {
  Card,
  CardContent,
  Grid,
  Typography,
  Chip,
  Box,
  Button,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  CircularProgress,
  Alert,
  TablePagination,
  TableSortLabel,
  TextField,
  InputAdornment,
  Tooltip,
  IconButton
} from '@mui/material';
import { useParams, useNavigate } from 'react-router-dom';
import { useQuery } from 'react-query';
import { getProduit, getProductMovements } from '../../services/inventaire';
import PageHeader from '../layout/PageHeader';
import { Edit, Search, FileDownload, Info } from '@mui/icons-material';
import { format } from 'date-fns';
import { fr } from 'date-fns/locale';
import DialogueMouvementStock from './DialogueMouvementStock';
import { CategoryProduit, TypeMouvement } from '../../types/inventaire';

type SortField = 'date' | 'type' | 'quantite';
type SortOrder = 'asc' | 'desc';

const ROWS_PER_PAGE_OPTIONS = [5, 10, 25];

const DetailsProduit: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [movementDialogOpen, setMovementDialogOpen] = useState(false);
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [sortField, setSortField] = useState<SortField>('date');
  const [sortOrder, setSortOrder] = useState<SortOrder>('desc');
  const [searchTerm, setSearchTerm] = useState('');

  const { data: product, isLoading: isLoadingProduct, error: productError } = useQuery(
    ['product', id],
    () => id ? getProduit(id) : Promise.reject('No ID provided'),
    {
      enabled: !!id
    }
  );

  const { data: movements, isLoading: isLoadingMovements, error: movementsError } = useQuery(
    ['product-movements', id],
    () => id ? getProductMovements(id) : Promise.reject('No ID provided'),
    {
      enabled: !!id
    }
  );

  const handleSort = (field: SortField) => {
    if (field === sortField) {
      setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc');
    } else {
      setSortField(field);
      setSortOrder('asc');
    }
  };

  const filteredAndSortedMovements = movements
    ?.filter(movement => 
      movement.reference_document?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      movement.responsable.nom.toLowerCase().includes(searchTerm.toLowerCase()) ||
      movement.responsable.prenom.toLowerCase().includes(searchTerm.toLowerCase())
    )
    .sort((a, b) => {
      const compareValue = (va: any, vb: any) => {
        if (va < vb) return sortOrder === 'asc' ? -1 : 1;
        if (va > vb) return sortOrder === 'asc' ? 1 : -1;
        return 0;
      };

      switch (sortField) {
        case 'date':
          return compareValue(new Date(a.date_mouvement), new Date(b.date_mouvement));
        case 'type':
          return compareValue(a.type_mouvement, b.type_mouvement);
        case 'quantite':
          return compareValue(a.quantite, b.quantite);
        default:
          return 0;
      }
    });

  const exportData = () => {
    if (!product || !movements) return;

    const csvContent = [
      ['Date', 'Type', 'Quantité', 'Référence', 'Responsable'].join(','),
      ...movements.map(m => [
        format(new Date(m.date_mouvement), 'Pp', { locale: fr }),
        m.type_mouvement,
        m.quantite,
        m.reference_document || '',
        `${m.responsable.nom} ${m.responsable.prenom}`
      ].join(','))
    ].join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = `mouvements_${product.code}_${format(new Date(), 'yyyy-MM-dd')}.csv`;
    link.click();
  };

  if (isLoadingProduct || isLoadingMovements) {
    return (
      <Box 
        display="flex" 
        justifyContent="center" 
        alignItems="center" 
        minHeight="200px"
        role="status"
        aria-label="Chargement des données du produit"
      >
        <CircularProgress />
        <Typography sx={{ ml: 2 }}>
          Chargement des données...
        </Typography>
      </Box>
    );
  }

  if (productError || movementsError || !product) {
    return (
      <Alert 
        severity="error"
        role="alert"
        sx={{ m: 2 }}
      >
        Une erreur est survenue lors du chargement des données. Veuillez réessayer plus tard.
      </Alert>
    );
  }

  return (
    <>
      <PageHeader
        title={`Produit ${product.code}`}
        subtitle="Détails et mouvements"
        action={{
          label: "Modifier",
          onClick: () => navigate(`/inventaire/produits/${id}/edit`),
          icon: <Edit />
        }}
      />

      <Grid container spacing={3}>
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Informations Générales
              </Typography>

              <Box sx={{ '& > *': { mb: 2 } }}>
                <Box>
                  <Typography color="text.secondary" gutterBottom>
                    Catégorie
                  </Typography>
                  <Chip
                    label={CategoryProduit[product.categorie]}
                    color="primary"
                    aria-label={`Catégorie: ${CategoryProduit[product.categorie]}`}
                  />
                </Box>

                <Box>
                  <Typography color="text.secondary" gutterBottom>
                    Unité de Mesure
                  </Typography>
                  <Typography variant="body1">
                    {product.unite_mesure}
                  </Typography>
                </Box>

                <Box>
                  <Typography color="text.secondary" gutterBottom>
                    Prix Unitaire
                  </Typography>
                  <Typography variant="h6">
                    {new Intl.NumberFormat('fr-FR', {
                      style: 'currency',
                      currency: 'XAF'
                    }).format(product.prix_unitaire)}
                  </Typography>
                </Box>

                <Box>
                  <Typography color="text.secondary" gutterBottom>
                    Seuil d'Alerte
                  </Typography>
                  <Typography variant="body1">
                    {product.seuil_alerte} {product.unite_mesure}
                  </Typography>
                </Box>
              </Box>

              <Button
                variant="contained"
                fullWidth
                onClick={() => setMovementDialogOpen(true)}
                aria-label="Créer un nouveau mouvement de stock"
              >
                Nouveau Mouvement
              </Button>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={8}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3, gap: 2 }}>
                <Typography variant="h6">
                  Historique des Mouvements
                </Typography>
                
                <Box sx={{ display: 'flex', gap: 2 }}>
                  <TextField
                    size="small"
                    placeholder="Rechercher..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    InputProps={{
                      startAdornment: (
                        <InputAdornment position="start">
                          <Search aria-hidden="true" />
                        </InputAdornment>
                      ),
                    }}
                    aria-label="Rechercher dans l'historique"
                  />
                  
                  <Tooltip title="Exporter les données">
                    <IconButton 
                      onClick={exportData}
                      aria-label="Exporter l'historique en CSV"
                    >
                      <FileDownload />
                    </IconButton>
                  </Tooltip>
                </Box>
              </Box>

              <Table aria-label="Historique des mouvements de stock">
                <TableHead>
                  <TableRow>
                    <TableCell>
                      <TableSortLabel
                        active={sortField === 'date'}
                        direction={sortField === 'date' ? sortOrder : 'asc'}
                        onClick={() => handleSort('date')}
                      >
                        Date
                      </TableSortLabel>
                    </TableCell>
                    <TableCell>
                      <TableSortLabel
                        active={sortField === 'type'}
                        direction={sortField === 'type' ? sortOrder : 'asc'}
                        onClick={() => handleSort('type')}
                      >
                        Type
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
                    <TableCell>
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                        Référence
                        <Tooltip title="Numéro du document associé au mouvement">
                          <Info fontSize="small" />
                        </Tooltip>
                      </Box>
                    </TableCell>
                    <TableCell>Responsable</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {filteredAndSortedMovements
                    ?.slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
                    .map(movement => (
                    <TableRow key={movement.id}>
                      <TableCell>
                        {format(new Date(movement.date_mouvement), 'Pp', { locale: fr })}
                      </TableCell>
                      <TableCell>
                        <Chip
                          size="small"
                          label={movement.type_mouvement}
                          color={movement.type_mouvement === TypeMouvement.ENTREE ? 'success' : 'error'}
                        />
                      </TableCell>
                      <TableCell align="right">
                        {movement.quantite} {product.unite_mesure}
                      </TableCell>
                      <TableCell>{movement.reference_document}</TableCell>
                      <TableCell>
                        {movement.responsable.nom} {movement.responsable.prenom}
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>

              <TablePagination
                component="div"
                count={filteredAndSortedMovements?.length || 0}
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
              />
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <DialogueMouvementStock
        open={movementDialogOpen}
        onClose={() => setMovementDialogOpen(false)}
        productId={id || null}
      />
    </>
  );
};

export default DetailsProduit;
