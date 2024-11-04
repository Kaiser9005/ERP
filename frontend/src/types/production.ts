export interface Parcelle {
  id: string;
  code: string;
  culture_type: 'PALMIER' | 'PAPAYE';
  surface_hectares: number;
  date_plantation: string;
  statut: 'ACTIVE' | 'EN_REPOS' | 'EN_PREPARATION';
  coordonnees_gps?: {
    latitude: number;
    longitude: number;
  };
  responsable_id: string;
}

export interface ProductionStats {
  total: number;
  variation: {
    value: number;
    type: 'increase' | 'decrease';
  };
  rendement: number;
  rendementVariation: {
    value: number;
    type: 'increase' | 'decrease';
  };
  parcellesActives: number;
  parcellesVariation: {
    value: number;
    type: 'increase' | 'decrease';
  };
  cyclesEnCours: number;
  cyclesVariation: {
    value: number;
    type: 'increase' | 'decrease';
  };
}

export interface ProductionEvent {
  id: string;
  title: string;
  start: Date;
  end: Date;
  type: 'RECOLTE' | 'TRAITEMENT' | 'MAINTENANCE';
  parcelle_id: string;
  description?: string;
  color?: string;
}