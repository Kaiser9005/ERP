import { render } from '@testing-library/react';
import { ThemeProvider } from '@mui/material';
import { theme } from '../../../theme';
import { MLPredictionsChart } from '../MLPredictionsChart';

const mockPredictions = {
  hr: {
    predictions: [],
    confidence: 0.85,
    risk_level: 0.15,
    recommended_actions: []
  },
  production: {
    predictions: [],
    confidence: 0.82,
    risk_level: 0.18,
    recommended_actions: []
  },
  finance: {
    predictions: [],
    confidence: 0.88,
    risk_level: 0.12,
    recommended_actions: []
  },
  inventory: {
    predictions: [],
    confidence: 0.90,
    risk_level: 0.10,
    recommended_actions: []
  },
  cross_module: {
    predictions: [],
    confidence: 0.85,
    risk_level: 0.15,
    correlations: {},
    impacts: {},
    recommended_actions: []
  }
};

describe('MLPredictionsChart', () => {
  it('rend le graphique avec les données de prédiction', () => {
    const { container } = render(
      <ThemeProvider theme={theme}>
        <MLPredictionsChart predictions={mockPredictions} />
      </ThemeProvider>
    );

    // Vérifie que le conteneur du graphique est présent
    expect(container.querySelector('.recharts-wrapper')).toBeInTheDocument();

    // Vérifie que les deux lignes (confiance et risque) sont présentes
    const lines = container.querySelectorAll('.recharts-line');
    expect(lines).toHaveLength(2);
  });

  it('affiche la légende avec les bonnes étiquettes', () => {
    const { container } = render(
      <ThemeProvider theme={theme}>
        <MLPredictionsChart predictions={mockPredictions} />
      </ThemeProvider>
    );

    const legendItems = container.querySelectorAll('.recharts-legend-item');
    expect(legendItems[0]).toHaveTextContent('Confiance');
    expect(legendItems[1]).toHaveTextContent('Risque');
  });

  it('affiche les bonnes valeurs sur les axes', () => {
    const { container } = render(
      <ThemeProvider theme={theme}>
        <MLPredictionsChart predictions={mockPredictions} />
      </ThemeProvider>
    );

    // Vérifie les labels de l'axe X
    const xAxisLabels = container.querySelectorAll('.recharts-xAxis .recharts-cartesian-axis-tick-value');
    expect(xAxisLabels[0]).toHaveTextContent('RH');
    expect(xAxisLabels[1]).toHaveTextContent('Production');
    expect(xAxisLabels[2]).toHaveTextContent('Finance');
    expect(xAxisLabels[3]).toHaveTextContent('Inventaire');

    // Vérifie les valeurs de l'axe Y
    const yAxisLabels = container.querySelectorAll('.recharts-yAxis .recharts-cartesian-axis-tick-value');
    expect(yAxisLabels[0]).toHaveTextContent('0%');
    expect(yAxisLabels[yAxisLabels.length - 1]).toHaveTextContent('100%');
  });

  it('utilise les bonnes couleurs du thème', () => {
    const { container } = render(
      <ThemeProvider theme={theme}>
        <MLPredictionsChart predictions={mockPredictions} />
      </ThemeProvider>
    );

    const lines = container.querySelectorAll('.recharts-line path');
    const confidenceLine = lines[0];
    const riskLine = lines[1];

    expect(confidenceLine).toHaveAttribute('stroke', theme.palette.primary.main);
    expect(riskLine).toHaveAttribute('stroke', theme.palette.error.main);
  });

  it('maintient les proportions responsives', () => {
    const { container } = render(
      <ThemeProvider theme={theme}>
        <MLPredictionsChart predictions={mockPredictions} />
      </ThemeProvider>
    );

    const wrapper = container.querySelector('.recharts-responsive-container');
    expect(wrapper).toHaveStyle({ width: '100%', height: '300px' });
  });

  it('affiche le tooltip au survol', () => {
    const { container } = render(
      <ThemeProvider theme={theme}>
        <MLPredictionsChart predictions={mockPredictions} />
      </ThemeProvider>
    );

    // Vérifie que le composant tooltip est présent
    expect(container.querySelector('.recharts-tooltip-wrapper')).toBeInTheDocument();
  });
});
