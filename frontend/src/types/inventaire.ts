export enum CategoryProduit {
  INTRANT = 'INTRANT',
  PRODUIT_FINI = 'PRODUIT_FINI',
  MATERIEL = 'MATERIEL',
  FOURNITURE = 'FOURNITURE'
}

export enum UniteMesure {
  KG = 'KG',
  L = 'L',
  UNITE = 'UNITE',
  CARTON = 'CARTON'
}

export enum TypeMouvement {
  ENTREE = 'ENTREE',
  SORTIE = 'SORTIE',
  TRANSFERT = 'TRANSFERT'
}

export enum PeriodeInventaire {
  JOUR = 'jour',
  SEMAINE = 'semaine',
  MOIS = 'mois',
  ANNEE = 'annee',
  PERSONNALISE = 'personnalise'
}

export enum SeuilStock {
  BAS = 'bas',
  NORMAL = 'normal',
  ELEVE = 'eleve'
}

export interface FiltresInventaire {
  periode?: PeriodeInventaire;
  categorie?: CategoryProduit;
  dateDebut?: string;
  dateFin?: string;
  fournisseur?: string;
  seuilStock?: SeuilStock;
  type_mouvement?: TypeMouvement;
  recherche?: string;
}

export interface PrevisionStock {
  date: string;
  valeur_reelle: number;
  valeur_prevue: number;
  categorie?: CategoryProduit;
  produit_id?: string;
}

export interface Produit {
  id: string;
  code: string;
  nom: string;
  categorie: CategoryProduit;
  unite_mesure: UniteMesure;
  seuil_alerte: number;
  prix_unitaire: number;
  quantite_stock?: number;
  description?: string;
  emplacement?: string;
  specifications?: Record<string, any>;
  date_derniere_maj?: string;
}

export interface MouvementStock {
  id: string;
  produit_id: string;
  produit: Produit;
  type_mouvement: TypeMouvement;
  quantite: number;
  entrepot_source_id?: string;
  entrepot_destination_id?: string;
  responsable_id?: string;
  responsable: {
    id: string;
    nom: string;
    prenom: string;
  };
  reference_document?: string;
  notes?: string;
  cout_unitaire?: number;
  date_mouvement: string;
}

export interface Stock {
  id: string;
  produit_id: string;
  quantite: number;
  valeur_unitaire: number;
  emplacement?: string;
  lot?: string;
  date_derniere_maj: string;
}

export interface StatsInventaire {
  total_produits: number;
  stock_faible: number;
  valeur_totale: number;
  mouvements: {
    entrees: number;
    sorties: number;
  };
  valeur_stock: {
    valeur: number;
    type: 'hausse' | 'baisse';
  };
  rotation_stock: {
    valeur: number;
    type: 'hausse' | 'baisse';
  };
}
