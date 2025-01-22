export interface Parcelle {
    id: string;
    code: string;
    culture_type: string;
    surface_hectares: number;
    statut: string;
    coordonnees_gps: {
      latitude: number;
      longitude: number;
    };
  }
  
  export interface CycleCulture {
    id: string;
    parcelleId: string;
    date_debut: string;
    date_fin: string;
    type_culture: string;
  }
  
  export interface Recolte {
    id: string;
    cycleCultureId: string;
    date_recolte: string;
    quantite: number;
    qualite: string;
  }
  
  export interface ProductionEvent {
    id: string;
    parcelleId: string;
    date: string;
    type: string;
    description: string;
  }
  
  export interface WeatherData {
    temperature: number;
    humidite: number;
    precipitations: number;
    vent: number;
  }
