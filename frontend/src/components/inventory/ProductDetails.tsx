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
  TableRow
} from '@mui/material';
import { useParams, useNavigate } from 'react-router-dom';
import { useQuery } from 'react-query';
import { getProduct, getProductMovements } from '../../services/inventory';
import PageHeader from '../layout/PageHeader';
import { Edit } from '@mui/icons-material';
import { format } from 'date-fns';
import { fr } from 'date-fns/locale';
import StockMovementDialog from './StockMovementDialog';

const ProductDetails: React.FC = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [movementDialogOpen, setMovementDialogOpen] = useState(false);

  const { data: product } = useQuery(
    ['product', id],
    () => getProduct(id!)
  );

  const { data: movements } = useQuery(
    ['product-movements', id],
    () => getProductMovements(id!)
  );

  const getStockLevel = (current: number, threshold: number) => {
    const ratio = current / threshold;
    if (ratio <= 0.25) return 'error';
    if (ratio <= 0.5) return 'warning';
    return 'success';
  };

  const formatResponsable = (movement: any) => {
    if (!movement.responsable) {
      return movement.responsable_id;
    }
    return `${movement.responsable.nom} ${movement.responsable.prenom}`;
  };

  return (
    <>
      <PageHeader
        title={`Produit ${product?.code}`}
        subtitle="Détails et mouvements"
        action={{
          label: "Modifier",
          onClick: () => navigate(`/inventory/products/${id}/edit`),
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
                    label={product?.categorie}
                    color="primary"
                  />
                </Box>

                <Box>
                  <Typography color="text.secondary" gutterBottom>
                    Unité de Mesure
                  </Typography>
                  <Typography variant="body1">
                    {product?.unite_mesure}
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
                    }).format(product?.prix_unitaire || 0)}
                  </Typography>
                </Box>

                <Box>
                  <Typography color="text.secondary" gutterBottom>
                    Seuil d'Alerte
                  </Typography>
                  <Typography variant="body1">
                    {product?.seuil_alerte} {product?.unite_mesure}
                  </Typography>
                </Box>
              </Box>

              <Button
                variant="contained"
                fullWidth
                onClick={() => setMovementDialogOpen(true)}
              >
                Nouveau Mouvement
              </Button>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={8}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Historique des Mouvements
              </Typography>

              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Date</TableCell>
                    <TableCell>Type</TableCell>
                    <TableCell align="right">Quantité</TableCell>
                    <TableCell>Référence</TableCell>
                    <TableCell>Responsable</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {movements?.map((movement) => (
                    <TableRow key={movement.id}>
                      <TableCell>
                        {format(new Date(movement.date_mouvement), 'Pp', { locale: fr })}
                      </TableCell>
                      <TableCell>
                        <Chip
                          size="small"
                          label={movement.type_mouvement}
                          color={movement.type_mouvement === 'ENTREE' ? 'success' : 'error'}
                        />
                      </TableCell>
                      <TableCell align="right">
                        {movement.quantite} {product?.unite_mesure}
                      </TableCell>
                      <TableCell>{movement.reference_document}</TableCell>
                      <TableCell>
                        {formatResponsable(movement)}
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <StockMovementDialog
        open={movementDialogOpen}
        onClose={() => setMovementDialogOpen(false)}
        productId={id || null}
      />
    </>
  );
};

export default ProductDetails;
