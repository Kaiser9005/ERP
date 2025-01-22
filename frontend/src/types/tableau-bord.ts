export interface StatsModule {
  timestamp: string;
  modules: {
    rh: ResumRH;
    production: ResumeProduction;
    finance: ResumeFinance;
    inventaire: ResumeInventaire;
    meteo: ResumeMeteo;
    projets: ResumeProjets;
  };
  alertes: Alerte[];
  predictions: PredictionsML;
}

export interface ResumRH {
  total_employes: number;
  contrats_actifs: number;
  formations_terminees: number;
  taux_completion_formation: number;
  activites_recentes: Activite[];
}

export interface ResumeProduction {
  production_journaliere: number;
  taux_efficacite: number;
  capteurs_actifs: number;
  metriques_qualite: MetriquesQualite;
  activites_recentes: Activite[];
}

export interface ResumeFinance {
  revenu_journalier: number;
  depenses_mensuelles: number;
  tresorerie: number;
  statut_budget: StatutBudget;
  transactions_recentes: Transaction[];
}

export interface ResumeInventaire {
  total_articles: number;
  articles_stock_bas: ArticleStock[];
  valeur_stock: number;
  mouvements_recents: MouvementStock[];
}

export interface ResumeMeteo {
  conditions_actuelles: ConditionsMeteo;
  previsions_journalieres: PrevisionMeteo[];
  alertes: AlerteMeteo[];
  impact_production: ImpactProduction;
}

export interface ResumeProjets {
  projets_actifs: number;
  predictions_completion: PredictionCompletion[];
  optimisation_ressources: OptimisationRessources;
  activites_recentes: Activite[];
}

export interface Activite {
  id: string;
  type: string;
  description: string;
  horodatage: string;
  utilisateur: string;
  module: string;
  statut: string;
}

export interface MetriquesQualite {
  score_global: number;
  taux_defauts: number;
  taux_conformite: number;
  score_efficacite: number;
}

export interface StatutBudget {
  actuel: number;
  prevu: number;
  ecart: number;
  statut: 'inferieur' | 'superieur' | 'conforme';
}

export interface Transaction {
  id: string;
  montant: number;
  type: string;
  categorie: string;
  horodatage: string;
  description: string;
}

export interface ArticleStock {
  id: string;
  nom: string;
  quantite_actuelle: number;
  quantite_minimale: number;
  unite: string;
  derniere_maj: string;
}

export interface MouvementStock {
  id: string;
  article_id: string;
  type: 'entree' | 'sortie';
  quantite: number;
  horodatage: string;
  raison: string;
}

export interface ConditionsMeteo {
  temperature: number;
  humidite: number;
  vitesse_vent: number;
  precipitation: number;
  condition: string;
}

export interface PrevisionMeteo {
  date: string;
  temperature_max: number;
  temperature_min: number;
  probabilite_precipitation: number;
  condition: string;
}

export interface AlerteMeteo {
  id: string;
  type: string;
  severite: 'faible' | 'moyenne' | 'elevee';
  description: string;
  debut: string;
  fin: string;
}

export interface ImpactProduction {
  niveau_risque: 'faible' | 'moyen' | 'eleve';
  zones_affectees: string[];
  recommandations: string[];
}

export interface PredictionCompletion {
  projet_id: string;
  nom_projet: string;
  completion_prevue: string;
  confiance: number;
  facteurs_risque: string[];
}

export interface OptimisationRessources {
  recommandations: string[];
  economies_potentielles: number;
  gain_efficacite: number;
}

export interface Alerte {
  id: string;
  module: string;
  type: string;
  severite: 'faible' | 'moyenne' | 'elevee';
  message: string;
  horodatage: string;
  statut: 'active' | 'reconnue' | 'resolue';
  priorite: number;
}

export interface PredictionsML {
  production: {
    prevision_sortie: number;
    prediction_qualite: number;
    predictions_maintenance: string[];
  };
  finance: {
    prevision_revenus: number;
    prevision_depenses: number;
    prediction_tresorerie: number;
  };
  inventaire: {
    predictions_stock: PredictionStock[];
    recommandations_reapprovisionnement: string[];
  };
  rh: {
    prevision_presence: number;
    besoins_formation: string[];
    predictions_performance: string[];
  };
}

export interface PredictionStock {
  article_id: string;
  nom_article: string;
  quantite_prevue: number;
  confiance: number;
  seuil_reapprovisionnement: number;
}

export type TypeModule = 'rh' | 'production' | 'finance' | 'inventaire' | 'meteo' | 'projets';

export interface DetailsModule {
  module: TypeModule;
  etendu: boolean;
}