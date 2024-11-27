import React from 'react';
import { render, screen } from '@testing-library/react';
import WeatherStatCard from '../WeatherStatCard';

describe('WeatherStatCard', () => {
  it('affiche correctement le titre et la valeur', () => {
    render(
      <WeatherStatCard
        title="Température"
        value="32°C"
        status="HIGH"
      />
    );

    expect(screen.getByText('Température')).toBeInTheDocument();
    expect(screen.getByText('32°C')).toBeInTheDocument();
  });

  it('affiche le niveau de risque', () => {
    render(
      <WeatherStatCard
        title="Température"
        value="32°C"
        status="HIGH"
      />
    );

    expect(screen.getByText('Niveau: HIGH')).toBeInTheDocument();
  });

  it('utilise la bonne couleur pour le statut LOW', () => {
    render(
      <WeatherStatCard
        title="Précipitations"
        value="0 mm"
        status="LOW"
      />
    );

    const statusText = screen.getByText('Niveau: LOW');
    expect(statusText).toHaveStyle({ color: 'success.main' });
  });

  it('utilise la bonne couleur pour le statut MEDIUM', () => {
    render(
      <WeatherStatCard
        title="Vent"
        value="15 km/h"
        status="MEDIUM"
      />
    );

    const statusText = screen.getByText('Niveau: MEDIUM');
    expect(statusText).toHaveStyle({ color: 'warning.main' });
  });

  it('utilise la bonne couleur pour le statut HIGH', () => {
    render(
      <WeatherStatCard
        title="Température"
        value="35°C"
        status="HIGH"
      />
    );

    const statusText = screen.getByText('Niveau: HIGH');
    expect(statusText).toHaveStyle({ color: 'error.main' });
  });

  it('affiche l\'icône appropriée pour la température', () => {
    const { container } = render(
      <WeatherStatCard
        title="Température"
        value="32°C"
        status="HIGH"
      />
    );

    expect(container.querySelector('svg')).toBeInTheDocument();
  });

  it('affiche l\'icône appropriée pour les précipitations', () => {
    const { container } = render(
      <WeatherStatCard
        title="Précipitations"
        value="10 mm"
        status="MEDIUM"
      />
    );

    expect(container.querySelector('svg')).toBeInTheDocument();
  });

  it('affiche l\'icône appropriée pour le vent', () => {
    const { container } = render(
      <WeatherStatCard
        title="Vent"
        value="20 km/h"
        status="MEDIUM"
      />
    );

    expect(container.querySelector('svg')).toBeInTheDocument();
  });
});
