import React from 'react';
import {
  Card,
  CardContent,
  Grid,
  Typography,
  Chip,
  Box,
  Button,
  Link
} from '@mui/material';
import { useParams, useNavigate } from 'react-router-dom';
import { useQuery } from 'react-query';
import { getTransaction } from '../../services/finance';
import PageHeader from '../layout/PageHeader';
import { Edit, Download } from '@mui/icons-material';
import { format } from 'date-fns';
import { fr } from 'date-fns/locale';

const TransactionDetails: React.FC = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { data: transaction } = useQuery(['transaction', id], () => getTransaction(id!));

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'VALIDEE':
        return 'success';
      case 'EN_ATTENTE':
        return 'warning';
      case 'REJETEE':
        return 'error';
      default:
        return 'default';
    }
  };

  const getTypeColor = (type: string) => {
    switch (type) {
      case 'RECETTE':
        return 'success';
      case 'DEPENSE':
        return 'error';
      case 'VIREMENT':
        return 'info';
      default:
        return 'default';
    }
  };

  return (
    <>
      <PageHeader
        title={`Transaction ${transaction?.reference}`}
        subtitle="Détails de la transaction"
        action={{
          label: "Modifier",
          onClick: () => navigate(`/finance/transactions/${id}/edit`),
          icon: <Edit />
        }}
      />

      <Grid container spacing={3}>
        <Grid item xs={12} md={8}>
          <Card>
            <CardContent>
              <Grid container spacing={3}>
                <Grid item xs={12} sm={6}>
                  <Typography color="text.secondary" gutterBottom>
                    Date
                  </Typography>
                  <Typography variant="body1">
                    {transaction?.date_transaction &&
                      format(new Date(transaction.date_transaction), 'Pp', { locale: fr })}
                  </Typography>
                </Grid>

                <Grid item xs={12} sm={6}>
                  <Typography color="text.secondary" gutterBottom>
                    Montant
                  </Typography>
                  <Typography variant="h5">
                    {new Intl.NumberFormat('fr-FR', {
                      style: 'currency',
                      currency: 'XAF'
                    }).format(transaction?.montant || 0)}
                  </Typography>
                </Grid>

                <Grid item xs={12} sm={6}>
                  <Typography color="text.secondary" gutterBottom>
                    Type
                  </Typography>
                  <Chip
                    label={transaction?.type_transaction}
                    color={getTypeColor(transaction?.type_transaction || '')}
                  />
                </Grid>

                <Grid item xs={12} sm={6}>
                  <Typography color="text.secondary" gutterBottom>
                    Statut
                  </Typography>
                  <Chip
                    label={transaction?.statut}
                    color={getStatusColor(transaction?.statut || '')}
                  />
                </Grid>

                <Grid item xs={12}>
                  <Typography color="text.secondary" gutterBottom>
                    Description
                  </Typography>
                  <Typography variant="body1">
                    {transaction?.description || '-'}
                  </Typography>
                </Grid>

                {transaction?.piece_jointe && (
                  <Grid item xs={12}>
                    <Typography color="text.secondary" gutterBottom>
                      Pièce Jointe
                    </Typography>
                    <Link
                      href={transaction.piece_jointe}
                      target="_blank"
                      rel="noopener noreferrer"
                      sx={{ display: 'flex', alignItems: 'center', gap: 1 }}
                    >
                      <Download /> Télécharger
                    </Link>
                  </Grid>
                )}
              </Grid>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Informations Complémentaires
              </Typography>

              {transaction?.compte_source && (
                <Box sx={{ mb: 2 }}>
                  <Typography color="text.secondary" gutterBottom>
                    Compte Source
                  </Typography>
                  <Typography variant="body1">
                    {transaction.compte_source.libelle}
                  </Typography>
                </Box>
              )}

              {transaction?.compte_destination && (
                <Box sx={{ mb: 2 }}>
                  <Typography color="text.secondary" gutterBottom>
                    Compte Destination
                  </Typography>
                  <Typography variant="body1">
                    {transaction.compte_destination.libelle}
                  </Typography>
                </Box>
              )}

              {transaction?.validee_par && (
                <Box>
                  <Typography color="text.secondary" gutterBottom>
                    Validée par
                  </Typography>
                  <Typography variant="body1">
                    {transaction.validee_par.nom} {transaction.validee_par.prenom}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    {transaction.date_validation &&
                      format(new Date(transaction.date_validation), 'Pp', { locale: fr })}
                  </Typography>
                </Box>
              )}
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </>
  );
};

export default TransactionDetails;