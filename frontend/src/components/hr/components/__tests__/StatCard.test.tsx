import React from 'react';
import { render, screen } from '@testing-library/react';
import { ThemeProvider, createTheme } from '@mui/material';
import { School } from '@mui/icons-material';
import StatCard from '../StatCard';

const theme = createTheme();

describe('StatCard', () => {
  const defaultProps = {
    title: 'Test Stat',
    value: 1234,
    icon: <School />,
    color: 'primary' as const
  };

  const renderWithTheme = (ui: React.ReactElement) => {
    return render(
      <ThemeProvider theme={theme}>
        {ui}
      </ThemeProvider>
    );
  };

  it('affiche le titre et la valeur', () => {
    renderWithTheme(<StatCard {...defaultProps} />);
    expect(screen.getByText('Test Stat')).toBeInTheDocument();
    expect(screen.getByText('1 234')).toBeInTheDocument();
  });

  it('formate correctement les valeurs monétaires', () => {
    renderWithTheme(
      <StatCard
        {...defaultProps}
        value={1234.56}
        format="currency"
      />
    );
    expect(screen.getByText('1 234,56 €')).toBeInTheDocument();
  });

  it('formate correctement les pourcentages', () => {
    renderWithTheme(
      <StatCard
        {...defaultProps}
        value={75.5}
        format="percentage"
      />
    );
    expect(screen.getByText('75,5%')).toBeInTheDocument();
  });

  it('affiche une variation positive', () => {
    renderWithTheme(
      <StatCard
        {...defaultProps}
        variation={{
          valeur: 12.5,
          type: 'hausse'
        }}
      />
    );
    expect(screen.getByText('12,5%')).toBeInTheDocument();
    expect(screen.getByText(/Augmentation/)).toBeInTheDocument();
  });

  it('affiche une variation négative', () => {
    renderWithTheme(
      <StatCard
        {...defaultProps}
        variation={{
          valeur: -5.3,
          type: 'baisse'
        }}
      />
    );
    expect(screen.getByText('-5,3%')).toBeInTheDocument();
    expect(screen.getByText(/Diminution/)).toBeInTheDocument();
  });

  it('utilise la bonne couleur', () => {
    const { container } = renderWithTheme(
      <StatCard
        {...defaultProps}
        color="success"
      />
    );
    // Vérifie que la classe de couleur success est appliquée
    expect(container.querySelector('.MuiBox-root')).toHaveStyle({
      backgroundColor: theme.palette.success.light
    });
  });
});
