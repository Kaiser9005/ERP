import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import HistoriqueMouvements from '../HistoriqueMouvements';
import { getMouvements, getTendances } from '../../../services/inventaire';
import { vi } from 'vitest';
import { 
  MouvementStock, 
  TypeMouvement, 
  CategoryProduit, 
  UniteMesure 
} from '../../../types/inventaire';

vi.mock('react-i18next', () => ({
  useTranslation: () => ({
    t: (key: string) => key,
    i18n: { changeLanguage: vi.fn() }
  })
}));

vi.mock('../../../services/inventaire');

const mockMouvements: MouvementStock[] = [
  {
    id: '1',
    date_mouvement: '2024-01-20T10:00:00Z',
    type_mouvement: TypeMouvement.ENTREE,
    quantite: 100,
    reference_document: 'BL-2024-001',
    responsable_id: '1',
    produit_id: '1',
    produit: {
      id: '1',
      code: 'PRD001',
      nom: 'Engrais NPK',
      categorie: CategoryProduit.INTRANT,
      unite_mesure: UniteMesure.KG,
      prix_unitaire: 1500,
      seuil_alerte: 100,
      specifications: {}
    },
    cout_unitaire: 1500
  },
  {
    id: '2',
    date_mouvement: '2024-01-20T11:00:00Z',
    type_mouvement: TypeMouvement.SORTIE,
    quantite: 20,
    reference_document: 'BS-2024-001',
    responsable_id: '2',
    produit_id: '2',
    cout_unitaire: 5000
  }
];

const mockTendances = [
  { date: '2024-01-19', entrees: 50, sorties: 30 },
  { date: '2024-01-20', entrees: 100, sorties: 20 }
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
    (getTendances as any).mockResolvedValue(mockTendances);
  });

  it('affiche l\'historique des mouvements', async () => {
    renderWithProviders(<HistoriqueMouvements />);
    
    expect(await screen.findByText('inventaire.mouvements.titre')).toBeInTheDocument();
    expect(await screen.findByText('Engrais NPK')).toBeInTheDocument();
    expect(await screen.findByText('Pesticide')).toBeInTheDocument();
  });

  it('affiche les types de mouvements avec les bonnes couleurs', async () => {
    renderWithProviders(<HistoriqueMouvements />);
    
    const entreeChip = await screen.findByText(TypeMouvement.ENTREE);
    const sortieChip = await screen.findByText(TypeMouvement.SORTIE);
    
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
    
    expect(screen.getByText('commun.chargement')).toBeInTheDocument();
  });

  it('gère les erreurs de chargement', async () => {
    (getMouvements as any).mockRejectedValue(new Error('Erreur test'));
    renderWithProviders(<HistoriqueMouvements />);
    
    expect(await screen.findByText('inventaire.mouvements.erreurChargement')).toBeInTheDocument();
  });

  it('filtre les mouvements par type', async () => {
    renderWithProviders(<HistoriqueMouvements />);
    
    const select = await screen.findByLabelText('inventaire.mouvements.filtres.type');
    fireEvent.mouseDown(select);
    
    const entreeOption = await screen.findByText('inventaire.mouvements.types.entree');
    fireEvent.click(entreeOption);
    
    expect(getMouvements).toHaveBeenCalledWith(expect.objectContaining({
      type_mouvement: TypeMouvement.ENTREE
    }));
  });

  it('filtre les mouvements par recherche', async () => {
    renderWithProviders(<HistoriqueMouvements />);
    
    const searchInput = await screen.findByPlaceholderText('inventaire.mouvements.filtres.recherche');
    fireEvent.change(searchInput, { target: { value: 'Engrais' } });
    
    expect(await screen.findByText('Engrais NPK')).toBeInTheDocument();
    expect(screen.queryByText('Pesticide')).not.toBeInTheDocument();
  });

  it('affiche le graphique des tendances', async () => {
    renderWithProviders(<HistoriqueMouvements />);
    
    expect(await screen.findByText('inventaire.mouvements.graphiques.titre')).toBeInTheDocument();
    expect(await screen.findByText('inventaire.mouvements.graphiques.entrees')).toBeInTheDocument();
    expect(await screen.findByText('inventaire.mouvements.graphiques.sorties')).toBeInTheDocument();
  });
});
