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
  Chip,
  Box,
  TextField,
  InputAdornment,
  IconButton
} from '@mui/material';
import { Edit, Search, Visibility } from '@mui/icons-material';
import { useQuery } from 'react-query';
import { getTransactions } from '../../services/finance';
import type { Transaction, TypeTransaction, TransactionListResponse, TransactionFilter } from '../../types/finance';
import { useNavigate } from 'react-router-dom';
import { format } from 'date-fns';
import { fr } from 'date-fns/locale';

const ListeTransactions: React.FC = () => {
  const [recherche, setRecherche] = useState('');
  const navigate = useNavigate();
  const { data, isLoading, error } = useQuery<TransactionListResponse, Error>(
    ['transactions', recherche], 
    () => getTransactions({ filter: recherche } as TransactionFilter),
    {
      onError: (error) => {
        console.error("Erreur lors de la récupération des transactions:", error);
      },
    }
  );

  const transactions = data?.transactions || [];

  const transactionsFiltrees = transactions.filter((transaction: Transaction) =>
    transaction.description?.toLowerCase().includes(recherche.toLowerCase()) ||
    (transaction.reference?.toLowerCase() || '').includes(recherche.toLowerCase())
  );

  const getCouleurTransaction = (type: TypeTransaction) => {
  switch (type) {
    case 'ENTREE':
      return 'success';
    case 'SORTIE':
      return 'error';
    default:
      return 'default';
  }
};

  return (
    <Card>
      <CardContent>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
          <Typography variant="h6">Transactions</Typography>
          <TextField
            size="small"
            placeholder="Rechercher..."
            value={recherche}
            onChange={(e) => setRecherche(e.target.value)}
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <Search />
                </InputAdornment>
              ),
            }}
          />
        </Box>

        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Date</TableCell>
              <TableCell>Référence</TableCell>
              <TableCell>Description</TableCell>
              <TableCell>Catégorie</TableCell>
              <TableCell align="right">Montant</TableCell>
              <TableCell>Type</TableCell>
              <TableCell align="right">Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {transactionsFiltrees.map((transaction) => (
              <TableRow key={transaction.id}>
                <TableCell>
                  {format(new Date(transaction.date), 'Pp', { locale: fr })}
                </TableCell>
                <TableCell>{transaction.reference || '-'}</TableCell>
                <TableCell>{transaction.description}</TableCell>
                <TableCell>{transaction.categorie}</TableCell>
                <TableCell align="right">
                  {new Intl.NumberFormat('fr-FR', {
                    style: 'currency',
                    currency: 'XAF'
                  }).format(transaction.montant)}
                </TableCell>
                <TableCell>
                  <Chip
                    size="small"
                    label={transaction.type}
                    color={getCouleurTransaction(transaction.type as TypeTransaction)}
                  />
                </TableCell>
                <TableCell align="right">
                  <IconButton
                    size="small"
                    onClick={() => navigate(`/finance/transactions/${transaction.id}`)}
                  >
                    <Visibility />
                  </IconButton>
                  <IconButton
                    size="small"
                    onClick={() => navigate(`/finance/transactions/${transaction.id}/modifier`)}
                  >
                    <Edit />
                  </IconButton>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </CardContent>
    </Card>
  );
};

export default ListeTransactions;
