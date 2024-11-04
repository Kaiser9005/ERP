import React from 'react';
import { render, screen } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from 'react-query';
import ProductionCalendar from '../ProductionCalendar';
import { getProductionEvents } from '../../../services/production';

jest.mock('../../../services/production');

const mockEvents = [
  {
    id: '1',
    title: 'Récolte P001',
    start: new Date('2024-01-20'),
    end: new Date('2024-01-20'),
    type: 'RECOLTE',
    parcelle_id: '1'
  },
  {
    id: '2',
    title: 'Traitement P002',
    start: new Date('2024-01-22'),
    end: new Date('2024-01-22'),
    type: 'TRAITEMENT',
    parcelle_id: '2'
  }
];

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: false,
    },
  },
});

const renderWithProviders = (component: React.ReactElement) => {
  return render(
    <QueryClientProvider client={queryClient}>
      {component}
    </QueryClientProvider>
  );
};

describe('ProductionCalendar', () => {
  beforeEach(() => {
    (getProductionEvents as jest.Mock).mockResolvedValue(mockEvents);
  });

  it('affiche le calendrier', () => {
    renderWithProviders(<ProductionCalendar />);
    
    expect(screen.getByText('Calendrier de Production')).toBeInTheDocument();
  });

  it('affiche les événements', async () => {
    renderWithProviders(<ProductionCalendar />);
    
    expect(await screen.findByText('Récolte P001')).toBeInTheDocument();
    expect(await screen.findByText('Traitement P002')).toBeInTheDocument();
  });

  it('affiche les contrôles de navigation', () => {
    renderWithProviders(<ProductionCalendar />);
    
    expect(screen.getByText('Aujourd\'hui')).toBeInTheDocument();
    expect(screen.getByText('Mois')).toBeInTheDocument();
    expect(screen.getByText('Semaine')).toBeInTheDocument();
  });

  it('gère les erreurs de chargement', async () => {
    (getProductionEvents as jest.Mock).mockRejectedValue(new Error('Erreur de chargement'));
    
    renderWithProviders(<ProductionCalendar />);
    
    expect(await screen.findByText('Erreur de chargement des événements')).toBeInTheDocument();
  });
});