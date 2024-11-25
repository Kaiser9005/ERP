import { api } from '@config/axios';
import {
  CompetenceAgricole,
  CompetenceAgricoleCreate,
  CompetenceAgricoleUpdate,
  CertificationAgricole,
  CertificationAgricoleCreate,
  CertificationAgricoleUpdate,
  AffectationParcelle,
  AffectationParcelleCreate,
  AffectationParcelleUpdate,
  ConditionTravailAgricole,
  ConditionTravailAgricoleCreate,
  ConditionTravailAgricoleUpdate,
  FormationAgricole,
  FormationAgricoleCreate,
  FormationAgricoleUpdate,
  EvaluationAgricole,
  EvaluationAgricoleCreate,
  EvaluationAgricoleUpdate,
  ValidationCompetence,
  CompetenceARenouveler,
  CertificationARenouveler,
  FiltresRHAgricole,
  OptionsTriRHAgricole,
  PaginationRHAgricole,
  StatistiquesCompetences,
  StatistiquesCertifications,
  StatistiquesFormations,
  StatistiquesConditionsTravail
} from '../types/hr_agricole';
import { UUID } from '../types/common';

const BASE_URL = '/hr-agricole';

// Compétences
export const createCompetence = async (competence: CompetenceAgricoleCreate): Promise<CompetenceAgricole> => {
  const response = await api.post<CompetenceAgricole>(`${BASE_URL}/competences/`, competence);
  return response.data;
};

export const getCompetence = async (id: UUID): Promise<CompetenceAgricole> => {
  const response = await api.get<CompetenceAgricole>(`${BASE_URL}/competences/${id}`);
  return response.data;
};

export const getCompetencesEmploye = async (employeId: UUID): Promise<CompetenceAgricole[]> => {
  const response = await api.get<CompetenceAgricole[]>(`${BASE_URL}/employes/${employeId}/competences/`);
  return response.data;
};

export const updateCompetence = async (id: UUID, competence: CompetenceAgricoleUpdate): Promise<CompetenceAgricole> => {
  const response = await api.put<CompetenceAgricole>(`${BASE_URL}/competences/${id}`, competence);
  return response.data;
};

// Certifications
export const createCertification = async (certification: CertificationAgricoleCreate): Promise<CertificationAgricole> => {
  const response = await api.post<CertificationAgricole>(`${BASE_URL}/certifications/`, certification);
  return response.data;
};

export const getCertification = async (id: UUID): Promise<CertificationAgricole> => {
  const response = await api.get<CertificationAgricole>(`${BASE_URL}/certifications/${id}`);
  return response.data;
};

export const getCertificationsCompetence = async (competenceId: UUID): Promise<CertificationAgricole[]> => {
  const response = await api.get<CertificationAgricole[]>(`${BASE_URL}/competences/${competenceId}/certifications/`);
  return response.data;
};

export const updateCertification = async (id: UUID, certification: CertificationAgricoleUpdate): Promise<CertificationAgricole> => {
  const response = await api.put<CertificationAgricole>(`${BASE_URL}/certifications/${id}`, certification);
  return response.data;
};

// Affectations
export const createAffectation = async (affectation: AffectationParcelleCreate): Promise<AffectationParcelle> => {
  const response = await api.post<AffectationParcelle>(`${BASE_URL}/affectations/`, affectation);
  return response.data;
};

export const getAffectation = async (id: UUID): Promise<AffectationParcelle> => {
  const response = await api.get<AffectationParcelle>(`${BASE_URL}/affectations/${id}`);
  return response.data;
};

export const getAffectationsEmploye = async (employeId: UUID): Promise<AffectationParcelle[]> => {
  const response = await api.get<AffectationParcelle[]>(`${BASE_URL}/employes/${employeId}/affectations/`);
  return response.data;
};

export const getAffectationsParcelle = async (parcelleId: UUID): Promise<AffectationParcelle[]> => {
  const response = await api.get<AffectationParcelle[]>(`${BASE_URL}/parcelles/${parcelleId}/affectations/`);
  return response.data;
};

export const updateAffectation = async (id: UUID, affectation: AffectationParcelleUpdate): Promise<AffectationParcelle> => {
  const response = await api.put<AffectationParcelle>(`${BASE_URL}/affectations/${id}`, affectation);
  return response.data;
};

// Conditions de travail
export const createConditionTravail = async (condition: ConditionTravailAgricoleCreate): Promise<ConditionTravailAgricole> => {
  const response = await api.post<ConditionTravailAgricole>(`${BASE_URL}/conditions-travail/`, condition);
  return response.data;
};

export const getConditionTravail = async (id: UUID): Promise<ConditionTravailAgricole> => {
  const response = await api.get<ConditionTravailAgricole>(`${BASE_URL}/conditions-travail/${id}`);
  return response.data;
};

export const getConditionsTravailEmploye = async (
  employeId: UUID,
  dateDebut: string,
  dateFin: string
): Promise<ConditionTravailAgricole[]> => {
  const response = await api.get<ConditionTravailAgricole[]>(
    `${BASE_URL}/employes/${employeId}/conditions-travail/`,
    { params: { date_debut: dateDebut, date_fin: dateFin } }
  );
  return response.data;
};

export const updateConditionTravail = async (
  id: UUID,
  condition: ConditionTravailAgricoleUpdate
): Promise<ConditionTravailAgricole> => {
  const response = await api.put<ConditionTravailAgricole>(`${BASE_URL}/conditions-travail/${id}`, condition);
  return response.data;
};

// Formations agricoles
export const createFormationAgricole = async (formation: FormationAgricoleCreate): Promise<FormationAgricole> => {
  const response = await api.post<FormationAgricole>(`${BASE_URL}/formations-agricoles/`, formation);
  return response.data;
};

export const getFormationAgricole = async (id: UUID): Promise<FormationAgricole> => {
  const response = await api.get<FormationAgricole>(`${BASE_URL}/formations-agricoles/${id}`);
  return response.data;
};

export const getFormationsAgricolesFormation = async (formationId: UUID): Promise<FormationAgricole[]> => {
  const response = await api.get<FormationAgricole[]>(`${BASE_URL}/formations/${formationId}/details-agricoles/`);
  return response.data;
};

export const updateFormationAgricole = async (
  id: UUID,
  formation: FormationAgricoleUpdate
): Promise<FormationAgricole> => {
  const response = await api.put<FormationAgricole>(`${BASE_URL}/formations-agricoles/${id}`, formation);
  return response.data;
};

// Évaluations agricoles
export const createEvaluationAgricole = async (evaluation: EvaluationAgricoleCreate): Promise<EvaluationAgricole> => {
  const response = await api.post<EvaluationAgricole>(`${BASE_URL}/evaluations-agricoles/`, evaluation);
  return response.data;
};

export const getEvaluationAgricole = async (id: UUID): Promise<EvaluationAgricole> => {
  const response = await api.get<EvaluationAgricole>(`${BASE_URL}/evaluations-agricoles/${id}`);
  return response.data;
};

export const getEvaluationsAgricolesEvaluation = async (evaluationId: UUID): Promise<EvaluationAgricole[]> => {
  const response = await api.get<EvaluationAgricole[]>(`${BASE_URL}/evaluations/${evaluationId}/details-agricoles/`);
  return response.data;
};

export const updateEvaluationAgricole = async (
  id: UUID,
  evaluation: EvaluationAgricoleUpdate
): Promise<EvaluationAgricole> => {
  const response = await api.put<EvaluationAgricole>(`${BASE_URL}/evaluations-agricoles/${id}`, evaluation);
  return response.data;
};

// Utilitaires
export const checkCompetenceValidite = async (competenceId: UUID): Promise<ValidationCompetence> => {
  const response = await api.get<ValidationCompetence>(`${BASE_URL}/competences/${competenceId}/validite/`);
  return response.data;
};

export const getCompetencesARenouveler = async (delaiJours: number = 30): Promise<CompetenceARenouveler[]> => {
  const response = await api.get<CompetenceARenouveler[]>(`${BASE_URL}/competences/a-renouveler/`, {
    params: { delai_jours: delaiJours }
  });
  return response.data;
};

export const getCertificationsARenouveler = async (delaiJours: number = 30): Promise<CertificationARenouveler[]> => {
  const response = await api.get<CertificationARenouveler[]>(`${BASE_URL}/certifications/a-renouveler/`, {
    params: { delai_jours: delaiJours }
  });
  return response.data;
};

// Statistiques
export const getStatistiquesCompetences = async (): Promise<StatistiquesCompetences> => {
  const response = await api.get<StatistiquesCompetences>(`${BASE_URL}/statistiques/competences/`);
  return response.data;
};

export const getStatistiquesCertifications = async (): Promise<StatistiquesCertifications> => {
  const response = await api.get<StatistiquesCertifications>(`${BASE_URL}/statistiques/certifications/`);
  return response.data;
};

export const getStatistiquesFormations = async (): Promise<StatistiquesFormations> => {
  const response = await api.get<StatistiquesFormations>(`${BASE_URL}/statistiques/formations/`);
  return response.data;
};

export const getStatistiquesConditionsTravail = async (
  dateDebut: string,
  dateFin: string
): Promise<StatistiquesConditionsTravail> => {
  const response = await api.get<StatistiquesConditionsTravail>(`${BASE_URL}/statistiques/conditions-travail/`, {
    params: { date_debut: dateDebut, date_fin: dateFin }
  });
  return response.data;
};

// Recherche et filtrage
export const rechercherCompetences = async (
  filtres: FiltresRHAgricole,
  tri: OptionsTriRHAgricole,
  pagination: PaginationRHAgricole
): Promise<{ data: CompetenceAgricole[]; pagination: PaginationRHAgricole }> => {
  const response = await api.get<{ data: CompetenceAgricole[]; pagination: PaginationRHAgricole }>(
    `${BASE_URL}/competences/recherche/`,
    { params: { ...filtres, ...tri, ...pagination } }
  );
  return response.data;
};

export const rechercherCertifications = async (
  filtres: FiltresRHAgricole,
  tri: OptionsTriRHAgricole,
  pagination: PaginationRHAgricole
): Promise<{ data: CertificationAgricole[]; pagination: PaginationRHAgricole }> => {
  const response = await api.get<{ data: CertificationAgricole[]; pagination: PaginationRHAgricole }>(
    `${BASE_URL}/certifications/recherche/`,
    { params: { ...filtres, ...tri, ...pagination } }
  );
  return response.data;
};
