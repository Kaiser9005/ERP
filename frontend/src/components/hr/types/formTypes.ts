import { Control, FieldErrors, Path, UseFormRegister } from 'react-hook-form';
import { Employee, Address, Formation, LeaveType, LeaveStatus } from '../../../types/hr';
import { Metadata, AuditFields } from '../../../types/common';

// Type pour le formulaire qui rend tous les tableaux non-undefined
export type EmployeeFormData = Omit<Employee, 'id'> & {
  competences: string[];
  formation?: Formation & {
    diplomes: string[];
    certifications: string[];
  };
  adresse?: Address;
  metadata?: Metadata;
} & Partial<AuditFields>;

export interface FormSectionProps {
  control: Control<EmployeeFormData>;
  errors: FieldErrors<EmployeeFormData>;
}

// Type pour les chemins de champs
export type EmployeeFormPath = Path<EmployeeFormData>;

// Type pour les champs de formation
export interface FormationFields {
  niveau: string;
  diplomes: string[];
  certifications: string[];
}

// Type pour les valeurs de champs de tableau
export type ArrayFieldValue = {
  id: string;
  value: string;
};

// Type pour le formulaire de congé
export interface LeaveFormData {
  type: LeaveType;
  dateDebut: string;
  dateFin: string;
  motif: string;
  statut: LeaveStatus;
}

// Type pour le formulaire de congé avec dates
export interface LeaveFormInputData {
  type: LeaveType;
  dateDebut: Date;
  dateFin: Date;
  motif: string;
}
