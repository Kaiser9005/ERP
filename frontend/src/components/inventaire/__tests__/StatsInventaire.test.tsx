import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from 'react-query';
import StatsInventaire from '../StatsInventaire';
import { getStatsInventaire, getMouvements, getStocks } from '../../../services/inventaire';

// Mock des services
jest.mock('../../../services/inventaire');
jest.mock('react-i18next', () => ({
  useTranslation: () => ({
    t: (key: string) => key,
    i18n: { changeLanguage: jest.fn() }
  })
}));

const mockStatsInventaire = {
  total_produits: 150,
  stock_faible: 5,
  valeur_totale: 1000000,
  mouvements: {
    entrees: 50,
    sorties: 30
  },
  valeur_stock: {
    valeur: 10,
    type: 'hausse' as const
  },
  rotation_stock: {
    valeur: 5,
    type: 'hausse' as const
  }
};

const mockMouvements = [
  {
    id: '1',
    produit_id: '1',
    type_mouvement: 'ENTREE',
    quantite: 10,
    date_mouvement: '2024-03-15',
    responsable: {
      id: '1',
      nom: 'Doe',
      prenom: 'John'
    }
  }
];

const mockStocks = [
  {
    id: '1',
    produit_id: '1',
    quantite: 100,
    valeur_unitaire: 1000,
    date_derniere_maj: '2024-03-15',
    produit: {
      id: '1',
      code: 'PROD1',
      nom: 'Produit 1',
      categorie: 'INTRANT',
      unite_mesure: 'KG',
      seuil_alerte: 10,
      prix_unitaire: 1000
    }
  }
];

describe('StatsInventaire', () => {
  let queryClient: QueryClient;

  beforeEach(() => {
    queryClient = new QueryClient({
      defaultOptions: {
        queries: {
          retry: false,
        },
      },
    });

    (getStatsInventaire as jest.Mock).mockResolvedValue(mockStatsInventaire);
    (getMouvements as jest.Mock).mockResolvedValue(mockMouvements);
    (getStocks as jest.Mock).mockResolvedValue(mockStocks);
  });

  const renderComponent = () => {
    return render(
      <QueryClientProvider client={queryClient}>
        <StatsInventaire />
      </QueryClientProvider>
    );
  };

  it('affiche les statistiques principales', async () => {
    renderComponent();

    expect(await screen.findByText('inventaire.valeurTotale')).toBeInTheDocument();
    expect(await screen.findByText('inventaire.tauxRotation')).toBeInTheDocument();
    expect(await screen.findByText('inventaire.alertes')).toBeInTheDocument();
    expect(await screen.findByText('inventaire.mouvements')).toBeInTheDocument();
  });

  it('permet de changer la période', async () => {
    renderComponent();

    const periodeSelect = await screen.findByLabelText('commun.periode');
    fireEvent.mouseDown(periodeSelect);
    
    const optionSemaine = await screen.findByText('commun.periodes.semaine');
    fireEvent.click(optionSemaine);
    
    expect(periodeSelect).toHaveValue('semaine');
  });

  it('permet de changer la catégorie', async () => {
    renderComponent();

    const categorieSelect = await screen.findByLabelText('inventaire.categorie');
    fireEvent.mouseDown(categorieSelect);
    
    const optionIntrant = await screen.findByText('inventaire.categories.intrant');
    fireEvent.click(optionIntrant);
    
    expect(categorieSelect).toHaveValue('INTRANT');
  });

  it('affiche le bouton d\'export', async () => {
    renderComponent();
    
    expect(await screen.findByText('commun.exporter')).toBeInTheDocument();
  });

  it('affiche les graphiques', async () => {
    renderComponent();

    expect(await screen.findByText('inventaire.graphiques.mouvements')).toBeInTheDocument();
    expect(await screen.findByText('inventaire.graphiques.stocksParCategorie')).toBeInTheDocument();
  });

  it('est accessible', async () => {
    renderComponent();

    // Vérifie la présence des attributs ARIA
    expect(screen.getByRole('region')).toHaveAttribute('aria-label', 'inventaire.statistiques');
    expect(screen.getAllByRole('img')).toHaveLength(2);
  });
});
