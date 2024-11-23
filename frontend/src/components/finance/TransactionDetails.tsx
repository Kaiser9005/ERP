import React from 'react';
import {
  Card,
  CardContent,
  Typography,
  Grid,
  Chip,
  Box,
  CircularProgress,
  Alert,
  Link
} from '@mui/material';
import { useQuery } from '@tanstack/react-query';
import { getTransaction } from '../../services/finance';
import { queryKeys } from '../../config/queryClient';
import type { Transaction } from '../../types/finance';

interface TransactionDetailsProps {
  transactionId: string;
}

const TransactionDetails: React.FC<TransactionDetailsProps> = ({ transactionId }) => {
  const { data: transaction, isLoading, error } = useQuery<Transaction>({
    queryKey: queryKeys.finance.transaction(transactionId),
    queryFn: () => getTransaction(transactionId),
    enabled: !!transactionId
  });

  if (isLoading) {
    return (
      <Card>
        <CardContent sx={{ display: 'flex', justifyContent: 'center', p: 3 }}>
          <CircularProgress />
        </CardContent>
      </Card>
    );
  }

  if (error || !transaction) {
    return (
      <Card>
        <CardContent>
          <Alert severity="error">
            Erreur lors du chargement des détails de la transaction
          </Alert>
        </CardContent>
      </Card>
    );
  }

  const getStatusColor = (statut: string) => {
    switch (statut) {
      case 'VALIDEE':
        return 'success';
      case 'EN_ATTENTE':
        return 'warning';
      case 'REJETEE':
        return 'error';
      case 'ANNULEE':
        return 'default';
      default:
        return 'default';
    }
  };

  return (
    <Card>
      <CardContent>
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <Box display="flex" justifyContent="space-between" alignItems="center">
              <Typography variant="h5" gutterBottom>
                Transaction {transaction.reference}
              </Typography>
              <Chip
                label={transaction.statut}
                color={getStatusColor(transaction.statut)}
                variant="outlined"
              />
            </Box>
          </Grid>

          <Grid item xs={12} md={6}>
            <Typography variant="subtitle2" color="text.secondary">
              Date
            </Typography>
            <Typography variant="body1">
              {new Date(transaction.date_transaction).toLocaleDateString('fr-FR', {
                day: 'numeric',
                month: 'long',
                year: 'numeric'
              })}
            </Typography>
          </Grid>

          <Grid item xs={12} md={6}>
            <Typography variant="subtitle2" color="text.secondary">
              Montant
            </Typography>
            <Typography variant="body1">
              {transaction.montant.toLocaleString('fr-FR', {
                style: 'currency',
                currency: 'XAF'
              })}
            </Typography>
          </Grid>

          <Grid item xs={12} md={6}>
            <Typography variant="subtitle2" color="text.secondary">
              Type
            </Typography>
            <Typography variant="body1">
              {transaction.type_transaction}
            </Typography>
          </Grid>

          <Grid item xs={12} md={6}>
            <Typography variant="subtitle2" color="text.secondary">
              Statut
            </Typography>
            <Typography variant="body1">
              {transaction.statut}
            </Typography>
          </Grid>

          <Grid item xs={12}>
            <Typography variant="subtitle2" color="text.secondary">
              Description
            </Typography>
            <Typography variant="body1">
              {transaction.description || 'Aucune description'}
            </Typography>
          </Grid>

          {transaction.piece_jointe && (
            <Grid item xs={12}>
              <Typography variant="subtitle2" color="text.secondary">
                Pièce jointe
              </Typography>
              <Link href={transaction.piece_jointe} target="_blank" rel="noopener">
                Voir le document
              </Link>
            </Grid>
          )}

          <Grid item xs={12} md={6}>
            <Typography variant="subtitle2" color="text.secondary">
              Compte source
            </Typography>
            {transaction.compte_source_id ? (
              <>
                <Typography variant="body1">
                  {transaction.compte_source_id.numero}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {transaction.compte_source_id.libelle}
                </Typography>
              </>
            ) : (
              <Typography variant="body2" color="text.secondary">
                Non spécifié
              </Typography>
            )}
          </Grid>

          <Grid item xs={12} md={6}>
            <Typography variant="subtitle2" color="text.secondary">
              Compte destination
            </Typography>
            {transaction.compte_destination_id ? (
              <>
                <Typography variant="body1">
                  {transaction.compte_destination_id.numero}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {transaction.compte_destination_id.libelle}
                </Typography>
              </>
            ) : (
              <Typography variant="body2" color="text.secondary">
                Non spécifié
              </Typography>
            )}
          </Grid>

          {transaction.validee_par_id && (
            <>
              <Grid item xs={12} md={6}>
                <Typography variant="subtitle2" color="text.secondary">
                  Validée par
                </Typography>
                <Typography variant="body1">
                  {transaction.validee_par_id.nom} {transaction.validee_par_id.prenom}
                </Typography>
              </Grid>
              <Grid item xs={12} md={6}>
                <Typography variant="subtitle2" color="text.secondary">
                  Date de validation
                </Typography>
                <Typography variant="body1">
                  {transaction.date_validation && new Date(transaction.date_validation).toLocaleDateString('fr-FR', {
                    day: 'numeric',
                    month: 'long',
                    year: 'numeric'
                  })}
                </Typography>
              </Grid>
            </>
          )}
        </Grid>
      </CardContent>
    </Card>
  );
};

export default TransactionDetails;
