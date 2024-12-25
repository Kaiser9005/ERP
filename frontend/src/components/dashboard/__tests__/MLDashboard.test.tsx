import { render, screen } from '@testing-library/react';
import UnifiedDashboard from '../UnifiedDashboard';
import DashboardService from '../../../services/dashboard';

// Mock du service
jest.mock('../../../services/dashboard');

describe('UnifiedDashboard', () => {
  const mockDashboardData = {
    timestamp: new Date().toISOString(),
    alerts: [
      { id: '1', message: 'Alerte test', status: 'pending' }
    ],
    modules: {
      hr: {},
      production: {},
      finance: {},
      inventory: {},
      weather: {},
      projects: {}
    }
  };

  beforeEach(() => {
    // Reset des mocks avant chaque test
    jest.clearAllMocks();
    (DashboardService.getUnifiedDashboard as jest.Mock).mockResolvedValue(mockDashboardData);
    (DashboardService.refreshModule as jest.Mock).mockResolvedValue(undefined);
    (DashboardService.updateAlertStatus as jest.Mock).mockResolvedValue(undefined);
  });

  it('affiche le titre correctement', () => {
    render(<UnifiedDashboard />);
    expect(screen.getByText('Tableau de Bord Unifié')).toBeInTheDocument();
  });

  it('affiche un loader pendant le chargement', () => {
    render(<UnifiedDashboard />);
    expect(screen.getByRole('progressbar')).toBeInTheDocument();
  });

  it('affiche une erreur en cas de problème', async () => {
    const errorMessage = 'Erreur de chargement';
    (DashboardService.getUnifiedDashboard as jest.Mock).mockRejectedValue(new Error(errorMessage));
    
    render(<UnifiedDashboard />);
    expect(await screen.findByText(errorMessage)).toBeInTheDocument();
  });

  it('affiche tous les modules une fois les données chargées', async () => {
    render(<UnifiedDashboard />);
    
    // Vérifie que tous les titres des modules sont présents
    expect(await screen.findByText('Ressources Humaines')).toBeInTheDocument();
    expect(screen.getByText('Production')).toBeInTheDocument();
    expect(screen.getByText('Finance')).toBeInTheDocument();
    expect(screen.getByText('Inventaire')).toBeInTheDocument();
    expect(screen.getByText('Météo')).toBeInTheDocument();
    expect(screen.getByText('Projets')).toBeInTheDocument();
  });
});
