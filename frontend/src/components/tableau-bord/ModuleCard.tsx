import React from 'react';
import { Card, CardContent, CardHeader, IconButton, Collapse, Box, Typography } from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import RefreshIcon from '@mui/icons-material/Refresh';
import { ModuleType } from '../../types/dashboard';

interface ModuleCardProps {
  title: string;
  module: ModuleType;
  expanded: boolean;
  onExpand: () => void;
  onRefresh: () => void;
  loading?: boolean;
  error?: string;
  children: React.ReactNode;
}

export const ModuleCard: React.FC<ModuleCardProps> = ({
  title,
  module,
  expanded,
  onExpand,
  onRefresh,
  loading,
  error,
  children
}) => {
  return (
    <Card 
      sx={{ 
        mb: 2,
        opacity: loading ? 0.7 : 1,
        transition: 'opacity 0.3s ease'
      }}
    >
      <CardHeader
        title={title}
        action={
          <Box>
            <IconButton 
              onClick={onRefresh}
              disabled={loading}
              sx={{ mr: 1 }}
            >
              <RefreshIcon />
            </IconButton>
            <IconButton
              onClick={onExpand}
              sx={{
                transform: expanded ? 'rotate(180deg)' : 'rotate(0deg)',
                transition: 'transform 0.3s ease'
              }}
            >
              <ExpandMoreIcon />
            </IconButton>
          </Box>
        }
      />
      <Collapse in={expanded}>
        <CardContent>
          {error ? (
            <Typography color="error">
              {error}
            </Typography>
          ) : (
            children
          )}
        </CardContent>
      </Collapse>
    </Card>
  );
};

export default ModuleCard;
