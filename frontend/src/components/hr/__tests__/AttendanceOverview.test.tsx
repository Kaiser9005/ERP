import React from 'react';
import { render, screen } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from 'react-query';
import AttendanceOverview from '../AttendanceOverview';
import { getAttendanceOverview } from '../../../services/hr';

jest.mock('../../../services/hr');

const mockAttendance = {
  daily: [
    {
      id: '1',
      employe: {
        id: '1',
        nom: 'Doe',
        prenom: 'John',
        departement: 'PRODUCTION'
      },
      type_presence: 'PRESENT',
      heure_arrivee: '2024-01-20T08:00:00Z',
      heure_depart: '2024-01-20T17:00:00Z'
    }
  ],
  stats: {
    presents: 15,
    absents: 3,
    retards: 2,
    conges: 5
  }
};

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

describe('AttendanceOverview', () => {
  beforeEach(() => {
    (getAttendanceOverview as jest.Mock).mockResolvedValue(mockAttendance);
  });

  it('affiche le titre', async () => {
    renderWithProviders(<AttendanceOverview />);
    
    expect(screen.getByText('Présences du Jour')).toBeInTheDocument();
  });

  it('affiche la liste des présences', async () => {
    renderWithProviders(<AttendanceOverview />);
    
    expect(await screen.findByText('John Doe')).toBeInTheDocument();
    expect(await screen.findByText('PRODUCTION')).toBeInTheDocument();
  });

  it('affiche les heures correctement', async () => {
    renderWithProviders(<AttendanceOverview />);
    
    expect(await screen.findByText('08:00')).toBeInTheDocument();
    expect(await screen.findByText('17:00')).toBeInTheDocument();
  });

  it('affiche les statuts avec les bonnes couleurs', async () => {
    renderWithProviders(<AttendanceOverview />);
    
    const statusChip = await screen.findByText('PRESENT');
    expect(statusChip).toHaveClass('MuiChip-colorSuccess');
  });

  it('gère les erreurs de chargement', async () => {
    (getAttendanceOverview as jest.Mock).mockRejectedValue(new Error('Erreur de chargement'));
    
    renderWithProviders(<AttendanceOverview />);
    
    expect(await screen.findByText('Erreur de chargement des présences')).toBeInTheDocument();
  });
});