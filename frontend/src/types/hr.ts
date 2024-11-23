// Types pour le module RH selon l'architecture définie
import { BaseEntity } from './common';

// Types pour les statistiques RH affichées dans le dashboard
export interface EmployeeStats {
  totalEmployees: number;
  employeesVariation: number;
  presentToday: number;
  presenceVariation: number;
  onLeave: number;
  leaveVariation: number;
  inTraining: number;
  trainingVariation: number;
}

export type ContractType = 'cdi' | 'cdd' | 'stage' | 'temporaire';

// Type principal pour les employés
export interface Employee extends BaseEntity {
  matricule: string;
  nom: string;
  prenom: string;
  dateNaissance: string;
  sexe: 'M' | 'F';
  email: string;
  telephone: string;
  poste: string;
  departement: string;
  dateEmbauche: string;
  typeContrat: ContractType;
  salaireBase: number;
  statut: EmployeeStatus;
  competences: string[];
  adresse?: Address;
  formation?: Formation;
}

export type EmployeeStatus = 'actif' | 'inactif' | 'conge' | 'formation';

export interface Address {
  rue: string;
  ville: string;
  codePostal: string;
  pays: string;
}

export interface Formation {
  niveau: string;
  diplomes: string[];
  certifications: string[];
}

// Types pour la gestion des congés
export interface Leave extends BaseEntity {
  employeeId: string;
  type: LeaveType;
  dateDebut: string;
  dateFin: string;
  statut: LeaveStatus;
  motif?: string;
  commentaires?: string;
}

export type LeaveType = 'conge_paye' | 'maladie' | 'formation' | 'autre';
export type LeaveStatus = 'en_attente' | 'approuve' | 'refuse';

// Types pour le suivi des présences
export interface Attendance extends BaseEntity {
  employeeId: string;
  date: string;
  heureArrivee: string;
  heureDepart?: string;
  statut: AttendanceStatus;
  commentaires?: string;
}

export type AttendanceStatus = 'present' | 'absent' | 'retard' | 'conge';

// Types pour la gestion des formations
export interface Training extends BaseEntity {
  titre: string;
  description: string;
  dateDebut: string;
  dateFin: string;
  formateur: string;
  participants: string[];
  statut: TrainingStatus;
  evaluation?: TrainingEvaluation;
}

export type TrainingStatus = 'planifie' | 'en_cours' | 'termine' | 'annule';

export interface TrainingEvaluation {
  note: number;
  commentaires: string;
}
