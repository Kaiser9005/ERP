export type TypeCompte = 'ACTIF' | 'PASSIF' | 'CHARGE' | 'PRODUIT';

export type TypeJournal = 'ACHAT' | 'VENTE' | 'BANQUE' | 'CAISSE' | 'OPERATIONS_DIVERSES';

export type StatutEcriture = 'BROUILLON' | 'VALIDEE' | 'ANNULEE';

export interface BudgetData {
  categorie: string;
  prevu: number;
  realise: number;
  ecart: number;
  ecart_percentage: number;
}

export interface BudgetAnalysis {
  total_prevu: number;
  total_realise: number;
  categories: Record<string, BudgetData>;
  weather_impact: {
    score: number;
    factors: string[];
    projections: Record<string, string>;
  };
  recommendations: string[];
}

export interface CashFlowData {
  date: string;
  entrees: number;
  sorties: number;
  solde: number;
  prevision: number;
  impact_meteo: number;
}

export interface CompteComptable {
    id: string;
    numero: string;
    libelle: string;
    type_compte: TypeCompte;
    compte_parent_id?: string;
    solde_debit: number;
    solde_credit: number;
    actif: boolean;
    description?: string;
    metadata?: Record<string, any>;
}

export interface EcritureComptable {
    id: string;
    date_ecriture: string;
    numero_piece: string;
    compte_id: string;
    libelle: string;
    debit: number;
    credit: number;
    statut: StatutEcriture;
    journal_id: string;
    transaction_id?: string;
    periode: string;
    validee_par_id?: string;
    date_validation?: string;
    metadata?: Record<string, any>;
}

export interface JournalComptable {
    id: string;
    code: string;
    libelle: string;
    type_journal: TypeJournal;
    actif: boolean;
    description?: string;
    metadata?: Record<string, any>;
}

export interface ExerciceComptable {
    id: string;
    annee: string;
    date_debut: string;
    date_fin: string;
    cloture: boolean;
    date_cloture?: string;
    cloture_par_id?: string;
    metadata?: Record<string, any>;
}

export interface LigneGrandLivre {
    date: string;
    piece: string;
    libelle: string;
    debit: number;
    credit: number;
    solde: number;
}

export interface CompteBalance {
    compte: {
        numero: string;
        libelle: string;
        type: TypeCompte;
    };
    debit: number;
    credit: number;
    solde: number;
}

export interface BilanCompte {
    libelle: string;
    montant: number;
}

export interface Bilan {
    actif: Record<string, BilanCompte>;
    passif: Record<string, BilanCompte>;
    total_actif: number;
    total_passif: number;
}

export interface CompteResultat {
    produits: Record<string, BilanCompte>;
    charges: Record<string, BilanCompte>;
    total_produits: number;
    total_charges: number;
    resultat_net: number;
}

// Types pour les formulaires
export interface CompteComptableFormData {
    numero: string;
    libelle: string;
    type_compte: TypeCompte;
    compte_parent_id?: string;
    description?: string;
}

export interface EcritureComptableFormData {
    date_ecriture: string;
    numero_piece: string;
    compte_id: string;
    libelle: string;
    debit: number;
    credit: number;
    journal_id: string;
    transaction_id?: string;
}

// Types pour les filtres
export interface ComptabiliteFilters {
    dateDebut?: string;
    dateFin?: string;
    compteId?: string;
    journalId?: string;
    typeCompte?: TypeCompte;
    typeJournal?: TypeJournal;
    statut?: StatutEcriture;
}

// Types pour les statistiques
export interface ComptabiliteStats {
    totalActif: number;
    totalPassif: number;
    resultatPeriode: number;
    nombreEcritures: number;
    nombreComptes: {
        actif: number;
        passif: number;
        charge: number;
        produit: number;
    };
}
