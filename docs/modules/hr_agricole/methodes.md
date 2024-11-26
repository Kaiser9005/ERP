# Méthodes du Service RH Agricole

## Vue d'ensemble

Le service `hr_agricole` fournit toutes les méthodes nécessaires pour interagir avec l'API RH agricole.

## Import

```typescript
import { 
  createCompetence,
  getCompetence,
  updateCompetence,
  // ...
} from '@services/hr_agricole';
```

## Méthodes Compétences

| Méthode | Description | Paramètres | Retour |
|---------|-------------|------------|--------|
| createCompetence | Crée une nouvelle compétence | CompetenceAgricoleCreate | Promise<CompetenceAgricole> |
| getCompetence | Récupère une compétence | id: UUID | Promise<CompetenceAgricole> |
| getCompetencesEmploye | Liste les compétences d'un employé | employeId: UUID | Promise<CompetenceAgricole[]> |
| updateCompetence | Met à jour une compétence | id: UUID, competence: CompetenceAgricoleUpdate | Promise<CompetenceAgricole> |
| deleteCompetence | Supprime une compétence | id: UUID | Promise<void> |

## Méthodes Certifications

| Méthode | Description | Paramètres | Retour |
|---------|-------------|------------|--------|
| createCertification | Crée une certification | CertificationAgricoleCreate | Promise<CertificationAgricole> |
| getCertification | Récupère une certification | id: UUID | Promise<CertificationAgricole> |
| getCertificationsCompetence | Liste les certifications d'une compétence | competenceId: UUID | Promise<CertificationAgricole[]> |
| updateCertification | Met à jour une certification | id: UUID, certification: CertificationAgricoleUpdate | Promise<CertificationAgricole> |
| deleteCertification | Supprime une certification | id: UUID | Promise<void> |

## Méthodes Affectations

| Méthode | Description | Paramètres | Retour |
|---------|-------------|------------|--------|
| createAffectation | Crée une affectation | AffectationParcelleCreate | Promise<AffectationParcelle> |
| getAffectation | Récupère une affectation | id: UUID | Promise<AffectationParcelle> |
| getAffectationsEmploye | Liste les affectations d'un employé | employeId: UUID | Promise<AffectationParcelle[]> |
| getAffectationsParcelle | Liste les affectations d'une parcelle | parcelleId: UUID | Promise<AffectationParcelle[]> |
| updateAffectation | Met à jour une affectation | id: UUID, affectation: AffectationParcelleUpdate | Promise<AffectationParcelle> |
| deleteAffectation | Supprime une affectation | id: UUID | Promise<void> |

## Méthodes Statistiques

| Méthode | Description | Paramètres | Retour |
|---------|-------------|------------|--------|
| getStatistiquesCompetences | Statistiques des compétences | - | Promise<StatistiquesCompetences> |
| getStatistiquesCertifications | Statistiques des certifications | - | Promise<StatistiquesCertifications> |
| getStatistiquesFormations | Statistiques des formations | - | Promise<StatistiquesFormations> |
| getStatistiquesConditionsTravail | Statistiques des conditions de travail | dateDebut: string, dateFin: string | Promise<StatistiquesConditionsTravail> |

## Méthodes Utilitaires

| Méthode | Description | Paramètres | Retour |
|---------|-------------|------------|--------|
| checkCompetenceValidite | Vérifie la validité d'une compétence | competenceId: UUID | Promise<ValidationCompetence> |
| getCompetencesARenouveler | Liste les compétences à renouveler | delaiJours?: number | Promise<CompetenceARenouveler[]> |
| getCertificationsARenouveler | Liste les certifications à renouveler | delaiJours?: number | Promise<CertificationARenouveler[]> |
| validateCompetence | Valide une compétence | competenceId: UUID | Promise<ValidationCompetence> |
| renewCompetence | Renouvelle une compétence | competenceId: UUID, dateExpiration: string | Promise<CompetenceAgricole> |

## Méthodes de Recherche

| Méthode | Description | Paramètres | Retour |
|---------|-------------|------------|--------|
| rechercherCompetences | Recherche de compétences | filtres: FiltresRHAgricole, tri: OptionsTriRHAgricole, pagination: PaginationRHAgricole | Promise<{ data: CompetenceAgricole[]; pagination: PaginationRHAgricole }> |
| rechercherCertifications | Recherche de certifications | filtres: FiltresRHAgricole, tri: OptionsTriRHAgricole, pagination: PaginationRHAgricole | Promise<{ data: CertificationAgricole[]; pagination: PaginationRHAgricole }> |

## Méthodes Météo

| Méthode | Description | Paramètres | Retour |
|---------|-------------|------------|--------|
| getConditionsMeteo | Récupère les conditions météo | parcelleId: UUID, date: string | Promise<ConditionsMeteo> |
| getPrevisionsMeteo | Récupère les prévisions météo | parcelleId: UUID, nombreJours: number | Promise<PrevisionMeteo[]> |
| getHistoriqueMeteo | Récupère l'historique météo | parcelleId: UUID, dateDebut: string, dateFin: string | Promise<HistoriqueMeteo[]> |

## Méthodes Formation

| Méthode | Description | Paramètres | Retour |
|---------|-------------|------------|--------|
| createFormation | Crée une formation | FormationAgricoleCreate | Promise<FormationAgricole> |
| getFormation | Récupère une formation | id: UUID | Promise<FormationAgricole> |
| getFormationsEmploye | Liste les formations d'un employé | employeId: UUID | Promise<FormationAgricole[]> |
| updateFormation | Met à jour une formation | id: UUID, formation: FormationAgricoleUpdate | Promise<FormationAgricole> |
| deleteFormation | Supprime une formation | id: UUID | Promise<void> |
| validateFormation | Valide une formation | formationId: UUID | Promise<FormationAgricole> |

## Méthodes Évaluation

| Méthode | Description | Paramètres | Retour |
|---------|-------------|------------|--------|
| createEvaluation | Crée une évaluation | EvaluationAgricoleCreate | Promise<EvaluationAgricole> |
| getEvaluation | Récupère une évaluation | id: UUID | Promise<EvaluationAgricole> |
| getEvaluationsEmploye | Liste les évaluations d'un employé | employeId: UUID | Promise<EvaluationAgricole[]> |
| updateEvaluation | Met à jour une évaluation | id: UUID, evaluation: EvaluationAgricoleUpdate | Promise<EvaluationAgricole> |
| deleteEvaluation | Supprime une évaluation | id: UUID | Promise<void> |

## Méthodes Planification

| Méthode | Description | Paramètres | Retour |
|---------|-------------|------------|--------|
| planifierFormation | Planifie une formation | PlanificationFormationCreate | Promise<PlanificationFormation> |
| getPlanificationFormation | Récupère une planification | id: UUID | Promise<PlanificationFormation> |
| getPlanificationsEmploye | Liste les planifications d'un employé | employeId: UUID | Promise<PlanificationFormation[]> |
| updatePlanification | Met à jour une planification | id: UUID, planification: PlanificationFormationUpdate | Promise<PlanificationFormation> |
| deletePlanification | Supprime une planification | id: UUID | Promise<void> |

## Méthodes Rapports

| Méthode | Description | Paramètres | Retour |
|---------|-------------|------------|--------|
| generateRapportCompetences | Génère un rapport de compétences | options: OptionsRapportCompetences | Promise<RapportCompetences> |
| generateRapportFormations | Génère un rapport de formations | options: OptionsRapportFormations | Promise<RapportFormations> |
| generateRapportEvaluations | Génère un rapport d'évaluations | options: OptionsRapportEvaluations | Promise<RapportEvaluations> |
| exportRapport | Exporte un rapport | rapportId: UUID, format: FormatExport | Promise<string> |
