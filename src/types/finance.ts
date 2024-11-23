import { UUID } from './common';

// Types de base
export enum TypeTransaction {
  RECETTE = "RECETTE",
  DEPENSE = "DEPENSE",
  VIREMENT = "VIREMENT"
}

export enum StatutTransaction {
  EN_ATTENTE = "EN_ATTENTE",
  VALIDEE = "VALIDEE",
  REJETEE = "REJETEE",
  ANNULEE = "ANNULEE"
}

export enum CategorieTransaction {
  VENTE = "VENTE",
  ACHAT_INTRANT = "ACHAT_INTRANT",
  SALAIRE = "SALAIRE",
  MAINTENANCE = "MAINTENANCE",
  TRANSPORT = "TRANSPORT",
  AUTRE = "AUTRE"
}

export enum TypeCompte {
  BANQUE = "BANQUE",
  CAISSE = "CAISSE",
  EPARGNE = "EPARGNE"
}

// Interfaces principales
export interface Transaction {
  id: UUID;
  reference: string;
  date_transaction: string;
  type_transaction: TypeTransaction;
  categorie: CategorieTransaction;
  montant: number;
  devise: string;
  description?: string;
  statut: StatutTransaction;
  compte_source_id?: UUID;
  compte_destination_id?: UUID;
  piece_jointe?: string;
  metadata?: Record<string, any>;
  validee_par_id?: UUID;
  date_validation?: string;
}

export interface Compte {
  id: UUID;
  numero: string;
  libelle: string;
  type_compte: TypeCompte;
  devise: string;
  solde: number;
  banque?: string;
  iban?: string;
  swift?: string;
  actif: boolean;
  description?: string;
  metadata?: Record<string, any>;
}

export interface Budget {
  id: UUID;
  periode: string;
  categorie: CategorieTransaction;
  montant_prevu: number;
  montant_realise: number;
  notes?: string;
  metadata?: Record<string, any>;
}

// Types pour les données de tableau de bord
export interface CashFlowData {
  labels: string[];
  recettes: number[];
  depenses: number[];
  solde: number[];
  previsions: number[];
  impact_meteo: number[];
}

export interface FinanceStats {
  revenue: number;
  revenueVariation: number;
  profit: number;
  profitVariation: number;
  cashflow: number;
  cashflowVariation: number;
  expenses: number;
  expensesVariation: number;
  periode: string;
}

// Types pour les formulaires
export interface TransactionFormData {
  reference?: string;
  date_transaction: string;
  type_transaction: TypeTransaction;
  categorie: CategorieTransaction;
  montant: number;
  devise?: string;
  description?: string;
  compte_source_id?: UUID;
  compte_destination_id?: UUID;
  piece_jointe?: File;
}

export interface CompteFormData {
  numero: string;
  libelle: string;
  type_compte: TypeCompte;
  devise: string;
  banque?: string;
  iban?: string;
  swift?: string;
  description?: string;
}

export interface BudgetFormData {
  periode: string;
  categorie: CategorieTransaction;
  montant_prevu: number;
  notes?: string;
}

// Types pour les filtres
export interface TransactionFilter {
  dateDebut?: string;
  dateFin?: string;
  type?: TypeTransaction;
  categorie?: CategorieTransaction;
  statut?: StatutTransaction;
  montantMin?: number;
  montantMax?: number;
  devise?: string;
  recherche?: string;
}

export interface CompteFilter {
  type?: TypeCompte;
  devise?: string;
  actif?: boolean;
  recherche?: string;
}

export interface BudgetFilter {
  periode?: string;
  categorie?: CategorieTransaction;
}

// Types pour les réponses API
export interface TransactionResponse {
  transaction: Transaction;
  message: string;
}

export interface CompteResponse {
  compte: Compte;
  message: string;
}

export interface BudgetResponse {
  budget: Budget;
  message: string;
}

export interface TransactionListResponse {
  transactions: Transaction[];
  total: number;
  page: number;
  pageSize: number;
}

export interface CompteListResponse {
  comptes: Compte[];
  total: number;
  page: number;
  pageSize: number;
}

export interface BudgetListResponse {
  budgets: Budget[];
  total: number;
  page: number;
  pageSize: number;
}
