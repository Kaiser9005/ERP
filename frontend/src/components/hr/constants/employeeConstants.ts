import { EmployeeFormData } from '../types/formTypes';

// Départements de l'entreprise
export const DEPARTEMENTS = [
  'Production',
  'Administration',
  'Ressources Humaines',
  'Finance',
  'Logistique',
  'Qualité',
  'Maintenance'
] as const;

// Types de contrat
export const TYPES_CONTRAT = [
  { value: 'cdi', label: 'CDI' },
  { value: 'cdd', label: 'CDD' },
  { value: 'stage', label: 'Stage' },
  { value: 'temporaire', label: 'Temporaire' }
] as const;

// Statuts employé
export const STATUTS = [
  { value: 'actif', label: 'Actif' },
  { value: 'conge', label: 'En Congé' },
  { value: 'formation', label: 'En Formation' },
  { value: 'inactif', label: 'Inactif' }
] as const;

// Valeurs par défaut pour le formulaire employé
export const defaultEmployeeValues: Partial<EmployeeFormData> = {
  sexe: 'M',
  departement: 'Production',
  typeContrat: 'cdi',
  statut: 'actif',
  salaireBase: 0,
  competences: [],
  formation: {
    niveau: '',
    diplomes: [],
    certifications: []
  },
  adresse: {
    rue: '',
    ville: '',
    codePostal: '',
    pays: 'Cameroun'
  }
};

// Messages d'erreur personnalisés
export const ERROR_MESSAGES = {
  required: 'Ce champ est requis',
  email: 'Email invalide',
  phone: 'Numéro de téléphone invalide',
  positiveNumber: 'La valeur doit être positive',
  date: 'Date invalide'
} as const;

// Formats de date
export const DATE_FORMAT = {
  display: 'dd/MM/yyyy',
  parse: 'yyyy-MM-dd'
} as const;

// Configuration des champs du formulaire
export const FORM_FIELDS = {
  matricule: {
    minLength: 3,
    maxLength: 10,
    pattern: /^[A-Z0-9]+$/
  },
  telephone: {
    pattern: /^[+0-9]{8,15}$/
  },
  email: {
    pattern: /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/
  },
  codePostal: {
    pattern: /^[0-9]{5}$/
  }
} as const;
