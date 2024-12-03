export enum CategoryProduit {
  INTRANT = "INTRANT",
  EQUIPEMENT = "EQUIPEMENT",
  RECOLTE = "RECOLTE",
  EMBALLAGE = "EMBALLAGE",
  PIECE_RECHANGE = "PIECE_RECHANGE"
}

export enum UniteMesure {
  KG = "KG",
  LITRE = "LITRE",
  UNITE = "UNITE",
  TONNE = "TONNE",
  METRE = "METRE"
}

export enum TypeMouvement {
  ENTREE = "ENTREE",
  SORTIE = "SORTIE",
  TRANSFERT = "TRANSFERT"
}

export enum PeriodeInventaire {
  JOUR = 'jour',
  SEMAINE = 'semaine',
  MOIS = 'mois',
  ANNEE = 'annee',
  PERSONNALISE = 'personnalise'
}

export interface SeuilStock {
  produit_id: string;
  seuil_min: number;
  seuil_max: number;
  seuil_alerte: number;
  actif: boolean;
  date_modification?: string;
  commentaires?: string;
}

export interface FiltresInventaire {
  periode?: PeriodeInventaire;
  categorie?: CategoryProduit;
  dateDebut?: string;
  dateFin?: string;
  fournisseur?: string;
  type_mouvement?: TypeMouvement;
  recherche?: string;
  skip?: number;
  limit?: number;
}

export interface PrevisionStock {
  date: string;
  valeur_reelle: number;
  valeur_prevue: number;
  categorie?: CategoryProduit;
  produit_id?: string;
}

export interface ConditionsStockage {
  temperature_min: number;
  temperature_max: number;
  humidite_min: number;
  humidite_max: number;
  luminosite_max?: number;
  ventilation_requise: boolean;
}

export interface ConditionsActuelles {
  temperature: number;
  humidite: number;
  luminosite?: number;
  qualite_air?: number;
  derniere_maj: string;
}

export interface Certification {
  nom: string;
  organisme: string;
  date_obtention: string;
  date_expiration: string;
  specifications: Record<string, any>;
}

export interface ControleQualite {
  date_controle: string;
  responsable_id: string;
  resultats: Record<string, any>;
  conforme: boolean;
  actions_requises?: string;
}

export interface Produit {
  id: string;
  code: string;
  nom: string;
  categorie: CategoryProduit;
  description?: string;
  unite_mesure: UniteMesure;
  seuil_alerte?: number;
  prix_unitaire?: number;
  specifications?: Record<string, any>;
  conditions_stockage?: ConditionsStockage;
}

export interface Stock {
  id: string;
  produit_id: string;
  entrepot_id: string;
  quantite: number;
  valeur_unitaire?: number;
  emplacement?: string;
  lot?: string;
  date_peremption?: string;
  origine?: string;
  certifications?: Certification[];
  conditions_actuelles?: ConditionsActuelles;
  capteurs_id?: string[];
  date_derniere_maj: string;
}

export interface MouvementStock {
  id: string;
  produit_id: string;
  type_mouvement: TypeMouvement;
  quantite: number;
  entrepot_source_id?: string;
  entrepot_destination_id?: string;
  responsable_id: string;
  reference_document?: string;
  notes?: string;
  cout_unitaire?: number;
  conditions_transport?: Record<string, any>;
  controle_qualite?: ControleQualite;
  date_mouvement: string;
}

export interface StatsInventaire {
  total_produits: number;
  valeur_totale: number;
  produits_sous_seuil: number;
  mouvements_jour: number;
}

export interface Entrepot {
  id: string;
  nom: string;
  adresse?: string;
  capacite?: number;
  responsable_id?: string;
  conditions_stockage?: ConditionsStockage;
  actif: boolean;
}

export interface InventoryPermissions {
  canCreate: boolean;
  canEdit: boolean;
  canDelete: boolean;
}
