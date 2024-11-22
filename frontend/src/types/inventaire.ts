export interface Produit {
  id: string;
  code: string;
  nom: string;
  description?: string;
  categorie: 'INTRANT' | 'EQUIPEMENT' | 'RECOLTE' | 'EMBALLAGE' | 'PIECE_RECHANGE';
  unite_mesure: 'KG' | 'LITRE' | 'UNITE' | 'TONNE' | 'METRE';
  prix_unitaire: number;
  seuil_alerte: number;
  specifications?: Record<string, any>;
}

export interface Responsable {
  id: string;
  nom: string;
  prenom: string;
}

export interface MouvementStock {
  id: string;
  date_mouvement: string;
  type_mouvement: 'ENTREE' | 'SORTIE' | 'TRANSFERT';
  quantite: number;
  reference_document?: string;
  responsable: Responsable;
  produit_id: string;
  produit: Produit;
  entrepot_source_id?: string;
  entrepot_destination_id?: string;
  cout_unitaire?: number;
  notes?: string;
}

export interface CreateMouvementStock {
  produit_id: string;
  type_mouvement: 'ENTREE' | 'SORTIE' | 'TRANSFERT';
  quantite: number;
  reference_document?: string;
  entrepot_source_id?: string;
  entrepot_destination_id?: string;
  cout_unitaire?: number;
  notes?: string;
}

export interface StockLevel {
  quantite: number;
  valeur_unitaire: number;
  emplacement?: string;
  lot?: string;
  date_derniere_maj: string;
}

export interface Stock {
  id: string;
  produit_id: string;
  produit: Produit;
  quantite: number;
  valeur_unitaire: number;
  emplacement?: string;
  lot?: string;
  date_derniere_maj: string;
}

export interface StatsInventaire {
  total_produits: number;
  valeur_totale: number;
  produits_sous_seuil: number;
  mouvements_recents: number;
  repartition_categories: Record<string, number>;
  evolution_stock: {
    date: string;
    valeur: number;
  }[];
  valueVariation: Variation;
  turnoverRate: number;
  turnoverVariation: Variation;
  alerts: number;
  alertsVariation: Variation;
  movements: number;
  movementsVariation: Variation;
}

export interface Variation {
  value: number;
  type: 'increase' | 'decrease';
}

export interface Entrepot {
  id: string;
  code: string;
  nom: string;
  localisation: string;
  description?: string;
  responsable_id?: string;
  responsable?: Responsable;
}

// Type alias pour la compatibilité avec les anciens composants
export type StockMovement = MouvementStock;
