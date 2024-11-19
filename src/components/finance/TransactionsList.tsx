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
import { useQuery } from '@tanstack/react-query';
import { getTransactions, Transaction } from '../../services/finance';
import { useNavigate } from 'react-router-dom';
import { format } from 'date-fns';
import { fr } from 'date-fns/locale';

const TransactionsList: React.FC = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const navigate = useNavigate();
  const { data: transactions = [] } = useQuery<Transaction[]>(['transactions'], getTransactions);

  const filteredTransactions = transactions.filter(transaction =>
    transaction.description?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    transaction.reference.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const getTransactionColor = (type: string) => {
    switch (type) {
      case 'RECETTE':
        return 'success';
      case 'DEPENSE':
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
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
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
              <TableCell align="right">Montant</TableCell>
              <TableCell>Type</TableCell>
              <TableCell>Statut</TableCell>
              <TableCell align="right">Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {filteredTransactions.map((transaction) => (
              <TableRow key={transaction.id}>
                <TableCell>
                  {format(new Date(transaction.date_transaction), 'Pp', { locale: fr })}
                </TableCell>
                <TableCell>{transaction.reference}</TableCell>
                <TableCell>{transaction.description}</TableCell>
                <TableCell align="right">
                  {new Intl.NumberFormat('fr-FR', {
                    style: 'currency',
                    currency: 'XAF'
                  }).format(transaction.montant)}
                </TableCell>
                <TableCell>
                  <Chip
                    size="small"
                    label={transaction.type_transaction}
                    color={getTransactionColor(transaction.type_transaction)}
                  />
                </TableCell>
                <TableCell>
                  <Chip
                    size="small"
                    label={transaction.statut}
                    variant="outlined"
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
                    onClick={() => navigate(`/finance/transactions/${transaction.id}/edit`)}
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

export default TransactionsList;
