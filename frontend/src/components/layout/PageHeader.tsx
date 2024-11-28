import React from 'react';
import { Box, Typography, Button } from '@mui/material';

interface PageHeaderProps {
  title: string;
  subtitle?: string;
  action?: {
    label: string;
    onClick: () => void;
    icon?: React.ReactNode;
    'aria-label'?: string;
  };
}

const PageHeader: React.FC<PageHeaderProps> = ({ title, subtitle, action }) => {
  return (
    <Box
      sx={{
        mb: 4,
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
      }}
    >
      <Box>
        <Typography variant="h4" component="h1" gutterBottom>
          {title}
        </Typography>
        {subtitle && (
          <Typography variant="subtitle1" color="text.secondary">
            {subtitle}
          </Typography>
        )}
      </Box>
      {action && (
        <Button
          variant="contained"
          onClick={action.onClick}
          startIcon={action.icon}
          aria-label={action['aria-label'] || action.label}
        >
          {action.label}
        </Button>
      )}
    </Box>
  );
};

export default PageHeader;
