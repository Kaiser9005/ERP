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
  IconButton,
  LinearProgress
} from '@mui/material';
import { Edit, Search, Add } from '@mui/icons-material';
import { useQuery } from 'react-query';
import { getStocks } from '../../services/inventory';
import StockMovementDialog from './StockMovementDialog';

const StockList: React.FC = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedProduct, setSelectedProduct] = useState<string | null>(null);
  const { data: stocks } = useQuery('stocks', getStocks);

  const filteredStocks = stocks?.filter(stock =>
    stock.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    stock.code.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const getStockLevel = (current: number, threshold: number) => {
    const ratio = current / threshold;
    if (ratio <= 0.25) return 'error';
    if (ratio <= 0.5) return 'warning';
    return 'success';
  };

  return (
    <Card>
      <CardContent>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
          <Typography variant="h6">État des Stocks</Typography>
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
              <TableCell>Code</TableCell>
              <TableCell>Produit</TableCell>
              <TableCell align="right">Quantité</TableCell>
              <TableCell align="right">Valeur</TableCell>
              <TableCell align="right">Niveau</TableCell>
              <TableCell align="right">Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {filteredStocks?.map((stock) => (
              <TableRow key={stock.id}>
                <TableCell>{stock.code}</TableCell>
                <TableCell>{stock.name}</TableCell>
                <TableCell align="right">
                  {stock.quantity} {stock.unit}
                </TableCell>
                <TableCell align="right">
                  {new Intl.NumberFormat('fr-FR', {
                    style: 'currency',
                    currency: 'XAF'
                  }).format(stock.value)}
                </TableCell>
                <TableCell align="right">
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <LinearProgress
                      variant="determinate"
                      value={(stock.quantity / stock.threshold) * 100}
                      color={getStockLevel(stock.quantity, stock.threshold)}
                      sx={{ flexGrow: 1 }}
                    />
                    <Typography variant="body2">
                      {Math.round((stock.quantity / stock.threshold) * 100)}%
                    </Typography>
                  </Box>
                </TableCell>
                <TableCell align="right">
                  <IconButton
                    size="small"
                    onClick={() => setSelectedProduct(stock.id)}
                  >
                    <Add />
                  </IconButton>
                  <IconButton size="small">
                    <Edit />
                  </IconButton>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>

        <StockMovementDialog
          open={!!selectedProduct}
          onClose={() => setSelectedProduct(null)}
          productId={selectedProduct}
        />
      </CardContent>
    </Card>
  );
};

export default StockList;