import { Task } from './task';

export enum ProjectStatus {
  PLANIFIE = "PLANIFIE",
  EN_COURS = "EN_COURS",
  EN_PAUSE = "EN_PAUSE",
  TERMINE = "TERMINE",
  ANNULE = "ANNULE"
}

export interface ProjectStats {
  projets_actifs: number;
  total_projets: number;
  variation_projets_actifs: number;
  taches_completees: number;
  total_taches: number;
  taches_retard: number;
  variation_taches_retard: number;
  heures_travaillees: number;
  variation_heures: number;
  repartition: {
    en_cours: number;
    en_attente: number;
    termines: number;
    en_retard: number;
  };
  taux_completion: number;
  projets_termines: number;
}

export interface ProjectBase {
  code: string;
  nom: string;
  description?: string;
  date_debut: string;
  date_fin_prevue: string;
  date_fin_reelle?: string;
  statut: ProjectStatus;
  budget?: number;
  responsable_id: string;
  objectifs?: Array<{
    description: string;
    criteres_succes?: string;
    date_cible?: string;
    statut?: string;
  }>;
  risques?: Array<{
    description: string;
    impact: 'FAIBLE' | 'MOYEN' | 'ELEVE';
    probabilite: 'FAIBLE' | 'MOYENNE' | 'ELEVEE';
    mitigation?: string;
    statut?: string;
  }>;
}

export interface Project extends ProjectBase {
  id: string;
  created_at: string;
  updated_at: string;
  taches?: Task[];
  documents?: ProjectDocument[];
}

export interface ProjectDocument {
  id: string;
  projet_id: string;
  nom: string;
  type: string;
  chemin_fichier: string;
  date_upload: string;
  uploaded_by_id: string;
}

export interface ProjectList {
  projects: Project[];
  total: number;
  page: number;
  size: number;
  total_pages: number;
}
