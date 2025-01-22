import React from 'react';
import { Grid, Typography, Box } from '@mui/material';
import { InventorySummary } from '../../../types/dashboard';
import StatCard from '../../../components/common/StatCard';
import Inventory2Icon from '@mui/icons-material/Inventory2';
import WarningIcon from '@mui/icons-material/Warning';
import EuroIcon from '@mui/icons-material/Euro';
import LocalShippingIcon from '@mui/icons-material/LocalShipping';

interface InventoryModuleProps {
  data: InventorySummary;
}

const InventoryModule: React.FC<InventoryModuleProps> = ({ data }) => {
  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('fr-FR', {
      style: 'currency',
      currency: 'EUR',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0
    }).format(amount);
  };

  return (
    <Box>
      <Grid container spacing={2}>
        {/* Total des Articles */}
        <Grid item xs={12} sm={6}>
          <StatCard
            title="Total des Articles"
            value={data.total_items}
            icon={<Inventory2Icon />}
            color="primary"
            loading={false}
          />
        </Grid>

        {/* Articles en Stock Faible */}
        <Grid item xs={12} sm={6}>
          <StatCard
            title="Stock Faible"
            value={data.low_stock_items.length}
            icon={<WarningIcon />}
            color="warning"
            loading={false}
          />
        </Grid>

        {/* Valeur du Stock */}
        <Grid item xs={12} sm={6}>
          <StatCard
            title="Valeur du Stock"
            value={data.stock_value}
            unit="€"
            icon={<EuroIcon />}
            color="success"
            loading={false}
          />
        </Grid>

        {/* Mouvements Récents */}
        <Grid item xs={12} sm={6}>
          <StatCard
            title="Mouvements Récents"
            value={data.recent_movements.length}
            icon={<LocalShippingIcon />}
            color="info"
            loading={false}
          />
        </Grid>
      </Grid>

      {/* Articles en Stock Faible */}
      <Box mt={3}>
        <Typography variant="h6" gutterBottom>
          Articles en Stock Faible
        </Typography>
        <Grid container spacing={2}>
          {data.low_stock_items.map((item) => (
            <Grid item xs={12} sm={6} key={item.id}>
              <Box
                sx={{
                  p: 2,
                  borderRadius: 1,
                  bgcolor: 'background.paper',
                  border: 1,
                  borderColor: 'warning.light',
                  '&:hover': {
                    bgcolor: 'action.hover'
                  }
                }}
              >
                <Typography variant="subtitle1" gutterBottom>
                  {item.name}
                </Typography>
                <Box display="flex" justifyContent="space-between" alignItems="center">
                  <Typography variant="body2" color="textSecondary">
                    Stock actuel: {item.current_quantity} {item.unit}
                  </Typography>
                  <Typography variant="body2" color="warning.main">
                    Minimum: {item.minimum_quantity} {item.unit}
                  </Typography>
                </Box>
                <Typography variant="caption" color="textSecondary">
                  Dernière mise à jour: {new Date(item.last_updated).toLocaleString()}
                </Typography>
              </Box>
            </Grid>
          ))}
        </Grid>
      </Box>

      {/* Mouvements Récents */}
      <Box mt={3}>
        <Typography variant="h6" gutterBottom>
          Mouvements Récents
        </Typography>
        <Box>
          {data.recent_movements.map((movement) => (
            <Box
              key={movement.id}
              sx={{
                p: 1,
                mb: 1,
                borderRadius: 1,
                bgcolor: 'background.paper',
                border: 1,
                borderColor: 'divider',
                '&:hover': {
                  bgcolor: 'action.hover'
                }
              }}
            >
              <Box display="flex" justifyContent="space-between" alignItems="center">
                <Box>
                  <Typography variant="body2" color="textSecondary">
                    {new Date(movement.timestamp).toLocaleString()}
                  </Typography>
                  <Typography>
                    {movement.type === 'in' ? 'Entrée' : 'Sortie'} - {movement.reason}
                  </Typography>
                </Box>
                <Typography
                  variant="h6"
                  color={movement.type === 'in' ? 'success.main' : 'warning.main'}
                >
                  {movement.type === 'in' ? '+' : '-'}
                  {movement.quantity}
                </Typography>
              </Box>
            </Box>
          ))}
        </Box>
      </Box>
    </Box>
  );
};

export default InventoryModule;
