export interface Parametre {
  id: string;
  code: string;
  libelle: string;
  description?: string;
  type_parametre: 'GENERAL' | 'MODULE' | 'UTILISATEUR';
  module?: string;
  valeur: any;
  modifiable: boolean;
  visible: boolean;
  ordre: number;
  categorie?: string;
}

export interface ConfigurationModule {
  id: string;
  module: string;
  actif: boolean;
  configuration?: any;
  ordre_affichage: number;
  icone?: string;
  couleur?: string;
  roles_autorises: string[];
}