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
import { useQuery } from '@tanstack/react-query';
import { getProduit, getMouvementsProduit } from '../../services/inventaire';
import PageHeader from '../layout/PageHeader';
import { Edit } from '@mui/icons-material';
import { format } from 'date-fns';
import { fr } from 'date-fns/locale';
import DialogueMouvementStock from './DialogueMouvementStock';

const DetailsProduit: React.FC = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [dialogueMouvementOuvert, setDialogueMouvementOuvert] = useState(false);

  const { data: produit } = useQuery(
    ['produit', id],
    () => getProduit(id!)
  );

  const { data: mouvements } = useQuery(
    ['mouvements-produit', id],
    () => getMouvementsProduit(id!)
  );

  const getNiveauStock = (actuel: number, seuil: number) => {
    const ratio = actuel / seuil;
    if (ratio <= 0.25) return 'error';
    if (ratio <= 0.5) return 'warning';
    return 'success';
  };

  const formatResponsable = (mouvement: any) => {
    if (!mouvement.responsable) {
      return mouvement.responsable_id;
    }
    return `${mouvement.responsable.nom} ${mouvement.responsable.prenom}`;
  };

  return (
    <>
      <PageHeader
        title={`Produit ${produit?.code}`}
        subtitle="Détails et mouvements"
        action={{
          label: "Modifier",
          onClick: () => navigate(`/inventaire/produits/${id}/modifier`),
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
                    label={produit?.categorie}
                    color="primary"
                  />
                </Box>

                <Box>
                  <Typography color="text.secondary" gutterBottom>
                    Unité de Mesure
                  </Typography>
                  <Typography variant="body1">
                    {produit?.unite_mesure}
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
                    }).format(produit?.prix_unitaire || 0)}
                  </Typography>
                </Box>

                <Box>
                  <Typography color="text.secondary" gutterBottom>
                    Seuil d'Alerte
                  </Typography>
                  <Typography variant="body1">
                    {produit?.seuil_alerte} {produit?.unite_mesure}
                  </Typography>
                </Box>
              </Box>

              <Button
                variant="contained"
                fullWidth
                onClick={() => setDialogueMouvementOuvert(true)}
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
                  {mouvements?.map((mouvement) => (
                    <TableRow key={mouvement.id}>
                      <TableCell>
                        {format(new Date(mouvement.date_mouvement), 'Pp', { locale: fr })}
                      </TableCell>
                      <TableCell>
                        <Chip
                          size="small"
                          label={mouvement.type_mouvement}
                          color={mouvement.type_mouvement === 'ENTREE' ? 'success' : 'error'}
                        />
                      </TableCell>
                      <TableCell align="right">
                        {mouvement.quantite} {produit?.unite_mesure}
                      </TableCell>
                      <TableCell>{mouvement.reference_document}</TableCell>
                      <TableCell>
                        {formatResponsable(mouvement)}
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
        open={dialogueMouvementOuvert}
        onClose={() => setDialogueMouvementOuvert(false)}
        productId={id || null}
      />
    </>
  );
};

export default DetailsProduit;
