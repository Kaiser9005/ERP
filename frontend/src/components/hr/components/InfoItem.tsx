import React from 'react';
import { Box, Typography } from '@mui/material';

interface InfoItemProps {
  icon: React.ReactNode;
  label: string;
  value: string | number;
}

const InfoItem: React.FC<InfoItemProps> = ({ icon, label, value }) => (
  <Box display="flex" alignItems="center" mb={2}>
    <Box
      sx={{
        mr: 2,
        display: 'flex',
        alignItems: 'center',
        color: 'primary.main'
      }}
    >
      {icon}
    </Box>
    <Box>
      <Typography variant="caption" color="text.secondary">
        {label}
      </Typography>
      <Typography>{value}</Typography>
    </Box>
  </Box>
);

export default InfoItem;
