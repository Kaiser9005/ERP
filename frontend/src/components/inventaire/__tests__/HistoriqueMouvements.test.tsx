import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import HistoriqueMouvements from '../HistoriqueMouvements';
import { getMouvements } from '../../../services/inventaire';
import { vi } from 'vitest';
import type { MouvementStock } from '../../../types/inventaire';

declare global {
  namespace Vi {
    interface JestMatchers<T> {
      toBeInTheDocument(): boolean;
      toHaveClass(className: string): boolean;
    }
  }
}

vi.mock('../../../services/inventaire');

const mockMouvements: MouvementStock[] = [
  {
    id: '1',
    date_mouvement: '2024-01-20T10:00:00Z',
    type_mouvement: 'ENTREE',
    quantite: 100,
    reference_document: 'BL-2024-001',
    responsable: {
      id: '1',
      nom: 'Dupont',
      prenom: 'Jean'
    },
    produit_id: '1',
    produit: {
      id: '1',
      code: 'PRD001',
      nom: 'Engrais NPK',
      categorie: 'INTRANT',
      unite_mesure: 'KG',
      prix_unitaire: 1500,
      seuil_alerte: 100,
      specifications: {}
    },
    cout_unitaire: 1500
  },
  {
    id: '2',
    date_mouvement: '2024-01-20T11:00:00Z',
    type_mouvement: 'SORTIE',
    quantite: 20,
    reference_document: 'BS-2024-001',
    responsable: {
      id: '2',
      nom: 'Martin',
      prenom: 'Sophie'
    },
    produit_id: '2',
    produit: {
      id: '2',
      code: 'PRD002',
      nom: 'Pesticide',
      categorie: 'INTRANT',
      unite_mesure: 'LITRE',
      prix_unitaire: 5000,
      seuil_alerte: 20,
      specifications: {}
    },
    cout_unitaire: 5000
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

describe('HistoriqueMouvements', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    (getMouvements as any).mockResolvedValue(mockMouvements);
  });

  it('affiche l\'historique des mouvements', async () => {
    renderWithProviders(<HistoriqueMouvements />);
    
    expect(await screen.findByText('Historique des Mouvements')).toBeInTheDocument();
    expect(await screen.findByText('Engrais NPK')).toBeInTheDocument();
    expect(await screen.findByText('Pesticide')).toBeInTheDocument();
  });

  it('affiche les types de mouvements avec les bonnes couleurs', async () => {
    renderWithProviders(<HistoriqueMouvements />);
    
    const entreeChip = await screen.findByText('ENTREE');
    const sortieChip = await screen.findByText('SORTIE');
    
    expect(entreeChip).toHaveClass('MuiChip-colorSuccess');
    expect(sortieChip).toHaveClass('MuiChip-colorError');
  });

  it('affiche les quantités et références', async () => {
    renderWithProviders(<HistoriqueMouvements />);
    
    expect(await screen.findByText('100 KG')).toBeInTheDocument();
    expect(await screen.findByText('BL-2024-001')).toBeInTheDocument();
  });

  it('affiche les responsables', async () => {
    renderWithProviders(<HistoriqueMouvements />);
    
    expect(await screen.findByText('Jean Dupont')).toBeInTheDocument();
    expect(await screen.findByText('Sophie Martin')).toBeInTheDocument();
  });

  it('affiche les dates relatives', async () => {
    renderWithProviders(<HistoriqueMouvements />);
    
    expect(await screen.findByText(/il y a/)).toBeInTheDocument();
  });

  it('affiche un message de chargement', () => {
    (getMouvements as any).mockReturnValue(new Promise(() => {}));
    renderWithProviders(<HistoriqueMouvements />);
    
    expect(screen.getByText('Chargement...')).toBeInTheDocument();
  });

  it('gère les erreurs de chargement', async () => {
    (getMouvements as any).mockRejectedValue(new Error('Erreur test'));
    renderWithProviders(<HistoriqueMouvements />);
    
    expect(await screen.findByText('Erreur lors du chargement des mouvements')).toBeInTheDocument();
  });
});
