import { render } from '@testing-library/react';
import { ThemeProvider } from '@mui/material';
import { theme } from '../../../theme';
import { CorrelationsChart } from '../CorrelationsChart';

const mockCorrelations = {
  hr_production: 0.85,
  production_finance: 0.75,
  weather_global: 0.65,
  inventory_finance: 0.80
};

describe('CorrelationsChart', () => {
  it('rend le graphique avec les données de corrélation', () => {
    const { container } = render(
      <ThemeProvider theme={theme}>
        <CorrelationsChart correlations={mockCorrelations} />
      </ThemeProvider>
    );

    // Vérifie que le conteneur du graphique est présent
    expect(container.querySelector('.recharts-wrapper')).toBeInTheDocument();

    // Vérifie que toutes les barres sont présentes
    const bars = container.querySelectorAll('.recharts-bar-rectangle');
    expect(bars).toHaveLength(4);
  });

  it('affiche les bonnes valeurs sur les axes', () => {
    const { container } = render(
      <ThemeProvider theme={theme}>
        <CorrelationsChart correlations={mockCorrelations} />
      </ThemeProvider>
    );

    // Vérifie les labels de l'axe X
    const xAxisLabels = container.querySelectorAll('.recharts-xAxis .recharts-cartesian-axis-tick-value');
    expect(xAxisLabels[0]).toHaveTextContent('RH-Production');
    expect(xAxisLabels[1]).toHaveTextContent('Production-Finance');
    expect(xAxisLabels[2]).toHaveTextContent('Météo-Global');
    expect(xAxisLabels[3]).toHaveTextContent('Inventaire-Finance');

    // Vérifie les valeurs de l'axe Y
    const yAxisLabels = container.querySelectorAll('.recharts-yAxis .recharts-cartesian-axis-tick-value');
    expect(yAxisLabels[0]).toHaveTextContent('0%');
    expect(yAxisLabels[yAxisLabels.length - 1]).toHaveTextContent('100%');
  });

  it('utilise les bonnes couleurs du thème', () => {
    const { container } = render(
      <ThemeProvider theme={theme}>
        <CorrelationsChart correlations={mockCorrelations} />
      </ThemeProvider>
    );

    const bars = container.querySelectorAll('.recharts-bar-rectangle path');
    bars.forEach((bar) => {
      const fill = bar.getAttribute('fill');
      expect(fill).toMatch(/^#[0-9A-F]{6}$/i); // Vérifie que c'est une couleur hex valide
    });
  });

  it('maintient les proportions responsives', () => {
    const { container } = render(
      <ThemeProvider theme={theme}>
        <CorrelationsChart correlations={mockCorrelations} />
      </ThemeProvider>
    );

    const wrapper = container.querySelector('.recharts-responsive-container');
    expect(wrapper).toHaveStyle({ width: '100%', height: '300px' });
  });
});
