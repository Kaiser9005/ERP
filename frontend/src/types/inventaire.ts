export interface Product {
  id: string;
  code: string;
  nom: string;
  description?: string;
  categorie: string;
  unite_mesure: string;
  prix_unitaire: number;
  seuil_alerte: number;
  specifications?: Record<string, any>;
}

export interface StockMovement {
  id: string;
  date_mouvement: string;
  type_mouvement: 'ENTREE' | 'SORTIE';
  quantite: number;
  reference_document?: string;
  responsable: {
    id: string;
    nom: string;
    prenom: string;
  };
  produit_id: string;
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
  produit: Product;
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
}

export interface MouvementStock extends StockMovement {
  produit: Product;
}
