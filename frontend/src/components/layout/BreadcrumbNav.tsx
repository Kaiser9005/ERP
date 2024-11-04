import React from 'react';
import { Breadcrumbs, Link, Typography } from '@mui/material';
import { Link as RouterLink, useLocation } from 'react-router-dom';
import { NavigateNext } from '@mui/icons-material';

const routeLabels: Record<string, string> = {
  dashboard: 'Tableau de bord',
  parametrage: 'Paramétrage',
  general: 'Général',
  modules: 'Modules',
  production: 'Production',
  inventaire: 'Inventaire',
  employes: 'Employés',
  finance: 'Finance'
};

const BreadcrumbNav: React.FC = () => {
  const location = useLocation();
  const pathnames = location.pathname.split('/').filter((x) => x);

  return (
    <Breadcrumbs 
      separator={<NavigateNext fontSize="small" />}
      aria-label="breadcrumb"
      sx={{ mb: 3 }}
    >
      <Link
        component={RouterLink}
        to="/"
        color="inherit"
        underline="hover"
      >
        Accueil
      </Link>
      {pathnames.map((value, index) => {
        const last = index === pathnames.length - 1;
        const to = `/${pathnames.slice(0, index + 1).join('/')}`;
        const label = routeLabels[value] || value;

        return last ? (
          <Typography color="text.primary" key={to}>
            {label}
          </Typography>
        ) : (
          <Link
            component={RouterLink}
            to={to}
            color="inherit"
            underline="hover"
            key={to}
          >
            {label}
          </Link>
        );
      })}
    </Breadcrumbs>
  );
};

export default BreadcrumbNav;