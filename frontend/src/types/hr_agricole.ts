import { UUID } from './common';

// Types de base
export type TypePersonnel = 'PERMANENT' | 'SAISONNIER' | 'TEMPORAIRE' | 'STAGIAIRE';

export type SpecialiteAgricole = 'CULTURE' | 'ELEVAGE' | 'MARAICHAGE' | 'ARBORICULTURE' | 'MAINTENANCE' | 'LOGISTIQUE';

export type NiveauCompetence = 'DEBUTANT' | 'INTERMEDIAIRE' | 'AVANCE' | 'EXPERT';

export type TypeCertification = 'PHYTOSANITAIRE' | 'SECURITE' | 'CONDUITE_ENGINS' | 'BIO' | 'QUALITE';

// Interfaces principales
export interface CompetenceAgricole {
  id: UUID;
  employe_id: UUID;
  specialite: SpecialiteAgricole;
  niveau: NiveauCompetence;
  cultures: string[];
  equipements: string[];
  date_acquisition: string;
  date_mise_a_jour?: string;
  validite?: string;
  commentaire?: string;
  donnees_supplementaires: Record<string, any>;
}

export interface CertificationAgricole {
  id: UUID;
  competence_id: UUID;
  type_certification: TypeCertification;
  organisme: string;
  numero?: string;
  date_obtention: string;
  date_expiration?: string;
  niveau?: string;
  document_id?: UUID;
  commentaire?: string;
  donnees_supplementaires: Record<string, any>;
}

export interface AffectationParcelle {
  id: UUID;
  employe_id: UUID;
  parcelle_id: UUID;
  date_debut: string;
  date_fin?: string;
  role: string;
  responsabilites: string[];
  objectifs: Record<string, any>;
  restrictions_meteo: string[];
  equipements_requis: string[];
  commentaire?: string;
  donnees_supplementaires: Record<string, any>;
}

export interface ConditionTravailAgricole {
  id: UUID;
  employe_id: UUID;
  date: string;
  temperature?: number;
  humidite?: number;
  precipitation: boolean;
  vent?: number;
  exposition_soleil?: number;
  charge_physique?: number;
  equipements_protection: string[];
  incidents: Array<{
    type: string;
    duree?: number;
    mesures_prises: string[];
  }>;
  commentaire?: string;
  donnees_supplementaires: Record<string, any>;
}

export interface FormationAgricole {
  id: UUID;
  formation_id: UUID;
  specialite: SpecialiteAgricole;
  cultures_concernees: string[];
  equipements_concernes: string[];
  conditions_meteo: {
    temperature_min?: number;
    temperature_max?: number;
    conditions_optimales?: string[];
  };
  pratiques_specifiques: string[];
  evaluation_terrain: boolean;
  resultats_evaluation: {
    pratique?: number;
    theorie?: number;
    [key: string]: any;
  };
  commentaire?: string;
  donnees_supplementaires: Record<string, any>;
}

export interface EvaluationAgricole {
  id: UUID;
  evaluation_id: UUID;
  performances_cultures: Record<string, {
    rendement?: number;
    qualite?: number;
    techniques?: string[];
    [key: string]: any;
  }>;
  maitrise_equipements: Record<string, NiveauCompetence>;
  respect_securite: {
    epi?: number;
    procedures?: number;
    [key: string]: any;
  };
  adaptabilite_meteo: Record<string, NiveauCompetence>;
  gestion_ressources: Record<string, number>;
  qualite_travail: {
    precision?: number;
    rapidite?: number;
    [key: string]: any;
  };
  commentaire?: string;
  donnees_supplementaires: Record<string, any>;
}

// Types pour la création/mise à jour
export type CompetenceAgricoleCreate = Omit<CompetenceAgricole, 'id'>;
export type CompetenceAgricoleUpdate = Partial<CompetenceAgricoleCreate>;

export type CertificationAgricoleCreate = Omit<CertificationAgricole, 'id'>;
export type CertificationAgricoleUpdate = Partial<CertificationAgricoleCreate>;

export type AffectationParcelleCreate = Omit<AffectationParcelle, 'id'>;
export type AffectationParcelleUpdate = Partial<AffectationParcelleCreate>;

export type ConditionTravailAgricoleCreate = Omit<ConditionTravailAgricole, 'id'>;
export type ConditionTravailAgricoleUpdate = Partial<ConditionTravailAgricoleCreate>;

export type FormationAgricoleCreate = Omit<FormationAgricole, 'id'>;
export type FormationAgricoleUpdate = Partial<FormationAgricoleCreate>;

export type EvaluationAgricoleCreate = Omit<EvaluationAgricole, 'id'>;
export type EvaluationAgricoleUpdate = Partial<EvaluationAgricoleCreate>;

// Types utilitaires
export interface ValidationCompetence {
  valide: boolean;
}

export interface CompetenceARenouveler extends CompetenceAgricole {
  jours_restants: number;
}

export interface CertificationARenouveler extends CertificationAgricole {
  jours_restants: number;
}

// Types pour les statistiques
export interface StatistiquesCompetences {
  total: number;
  par_specialite: Record<SpecialiteAgricole, number>;
  par_niveau: Record<NiveauCompetence, number>;
  a_renouveler: number;
}

export interface StatistiquesCertifications {
  total: number;
  par_type: Record<TypeCertification, number>;
  valides: number;
  expirees: number;
  a_renouveler: number;
}

export interface StatistiquesFormations {
  total: number;
  par_specialite: Record<SpecialiteAgricole, number>;
  reussies: number;
  en_cours: number;
  planifiees: number;
}

export interface StatistiquesConditionsTravail {
  moyenne_temperature: number;
  moyenne_humidite: number;
  jours_precipitation: number;
  moyenne_charge_physique: number;
  incidents_total: number;
  incidents_par_type: Record<string, number>;
}

// Types pour les filtres
export interface FiltresRHAgricole {
  specialites?: SpecialiteAgricole[];
  niveaux?: NiveauCompetence[];
  types_certification?: TypeCertification[];
  date_debut?: string;
  date_fin?: string;
  valides_seulement?: boolean;
  a_renouveler?: boolean;
  delai_renouvellement?: number;
}

// Types pour le tri
export type ChampTriRHAgricole = 
  | 'date_acquisition'
  | 'date_obtention'
  | 'date_debut'
  | 'niveau'
  | 'specialite'
  | 'type_certification';

export interface OptionsTriRHAgricole {
  champ: ChampTriRHAgricole;
  ordre: 'asc' | 'desc';
}

// Types pour la pagination
export interface PaginationRHAgricole {
  page: number;
  limite: number;
  total: number;
}
