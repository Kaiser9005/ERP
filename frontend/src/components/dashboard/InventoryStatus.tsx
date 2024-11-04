import React from 'react';
import {
  Box,
  Typography,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  Chip,
  LinearProgress
} from '@mui/material';
import { useQuery } from 'react-query';
import { getInventoryStatus } from '../../services/inventory';

const InventoryStatus: React.FC = () => {
  const { data: inventory } = useQuery('inventory-status', getInventoryStatus);

  const getStockLevel = (current: number, threshold: number) => {
    const ratio = current / threshold;
    if (ratio <= 0.25) return 'error';
    if (ratio <= 0.5) return 'warning';
    return 'success';
  };

  return (
    <Box>
      <Typography variant="h6" gutterBottom>
        État des Stocks
      </Typography>
      <Table size="small">
        <TableHead>
          <TableRow>
            <TableCell>Produit</TableCell>
            <TableCell align="right">Stock</TableCell>
            <TableCell align="right">Niveau</TableCell>
            <TableCell align="right">Statut</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {inventory?.items.map((item) => (
            <TableRow key={item.id}>
              <TableCell>{item.name}</TableCell>
              <TableCell align="right">
                {item.quantity} {item.unit}
              </TableCell>
              <TableCell align="right" sx={{ width: 100 }}>
                <LinearProgress
                  variant="determinate"
                  value={(item.quantity / item.threshold) * 100}
                  color={getStockLevel(item.quantity, item.threshold)}
                />
              </TableCell>
              <TableCell align="right">
                <Chip
                  size="small"
                  label={item.quantity <= item.threshold ? 'Alerte' : 'Normal'}
                  color={getStockLevel(item.quantity, item.threshold)}
                />
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </Box>
  );
};

export default InventoryStatus;