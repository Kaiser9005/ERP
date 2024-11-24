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
import { getProduit, getProductMovements } from '../../services/inventaire';
import PageHeader from '../layout/PageHeader';
import { Edit } from '@mui/icons-material';
import { format } from 'date-fns';
import { fr } from 'date-fns/locale';
import DialogueMouvementStock from './DialogueMouvementStock';
import { CategoryProduit, TypeMouvement } from '../../types/inventaire';

const DetailsProduit: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [movementDialogOpen, setMovementDialogOpen] = useState(false);

  const { data: product, isLoading: isLoadingProduct } = useQuery(
    ['product', id],
    () => id ? getProduit(id) : Promise.reject('No ID provided'),
    {
      enabled: !!id
    }
  );

  const { data: movements, isLoading: isLoadingMovements } = useQuery(
    ['product-movements', id],
    () => id ? getProductMovements(id) : Promise.reject('No ID provided'),
    {
      enabled: !!id
    }
  );

  if (isLoadingProduct || isLoadingMovements || !product) {
    return null; // TODO: Add loading spinner
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
                  {movements?.map(movement => (
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
