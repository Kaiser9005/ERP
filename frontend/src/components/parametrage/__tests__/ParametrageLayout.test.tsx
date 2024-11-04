import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { MemoryRouter, Routes, Route } from 'react-router-dom';
import ParametrageLayout from '../ParametrageLayout';

const renderWithRouter = (component: React.ReactElement) => {
  return render(
    <MemoryRouter initialEntries={['/parametrage/general']}>
      <Routes>
        <Route path="/parametrage/*" element={component} />
      </Routes>
    </MemoryRouter>
  );
};

describe('ParametrageLayout', () => {
  it('affiche les onglets de navigation', () => {
    renderWithRouter(<ParametrageLayout />);
    
    expect(screen.getByText('Paramètres Généraux')).toBeInTheDocument();
    expect(screen.getByText('Modules')).toBeInTheDocument();
    expect(screen.getByText('Système')).toBeInTheDocument();
  });

  it('gère la navigation entre les onglets', () => {
    renderWithRouter(<ParametrageLayout />);
    
    fireEvent.click(screen.getByText('Modules'));
    expect(window.location.pathname).toBe('/parametrage/modules');
  });

  it('affiche l\'onglet actif', () => {
    renderWithRouter(<ParametrageLayout />);
    
    const activeTab = screen.getByRole('tab', { selected: true });
    expect(activeTab).toHaveTextContent('Paramètres Généraux');
  });

  it('affiche le contenu de l\'onglet sélectionné', () => {
    renderWithRouter(
      <ParametrageLayout>
        <div>Contenu de test</div>
      </ParametrageLayout>
    );
    
    expect(screen.getByText('Contenu de test')).toBeInTheDocument();
  });
});