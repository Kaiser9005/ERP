import * as yup from 'yup';
import { EmployeeFormData } from '../types/formTypes';

export const employeeSchema: yup.ObjectSchema<EmployeeFormData> = yup.object().shape({
  matricule: yup.string().required('Le matricule est requis'),
  nom: yup.string().required('Le nom est requis'),
  prenom: yup.string().required('Le prénom est requis'),
  dateNaissance: yup.string().required('La date de naissance est requise'),
  sexe: yup.string().oneOf(['M', 'F']).required('Le sexe est requis'),
  email: yup.string().email('Email invalide').required('L\'email est requis'),
  telephone: yup.string().required('Le téléphone est requis'),
  departement: yup.string().required('Le département est requis'),
  poste: yup.string().required('Le poste est requis'),
  dateEmbauche: yup.string().required('La date d\'embauche est requise'),
  typeContrat: yup.string()
    .oneOf(['cdi', 'cdd', 'stage', 'temporaire'])
    .required('Le type de contrat est requis'),
  salaireBase: yup.number()
    .required('Le salaire de base est requis')
    .min(0, 'Le salaire doit être positif'),
  statut: yup.string()
    .oneOf(['actif', 'conge', 'formation', 'inactif'])
    .default('actif'),
  competences: yup.array().of(yup.string().required()).default([]),
  adresse: yup.object({
    rue: yup.string().required('L\'adresse est requise'),
    ville: yup.string().required('La ville est requise'),
    codePostal: yup.string().required('Le code postal est requis'),
    pays: yup.string().required('Le pays est requis')
  }).optional(),
  formation: yup.object({
    niveau: yup.string().required('Le niveau est requis'),
    diplomes: yup.array().of(yup.string().required()).default([]),
    certifications: yup.array().of(yup.string().required()).default([])
  }).optional(),
  metadata: yup.mixed().optional(),
  created_at: yup.string().optional(),
  updated_at: yup.string().optional(),
  created_by_id: yup.string().optional(),
  updated_by_id: yup.string().optional()
});
