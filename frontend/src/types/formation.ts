export interface Formation {
    id: string;
    titre: string;
    description?: string;
    type: 'technique' | 'securite' | 'agricole';
    duree: number;
    competences_requises?: Record<string, any>;
    competences_acquises?: Record<string, any>;
    materiel_requis?: Record<string, any>;
    conditions_meteo?: Record<string, any>;
    created_at: string;
    updated_at: string;
}

export interface FormationCreate {
    titre: string;
    description?: string;
    type: 'technique' | 'securite' | 'agricole';
    duree: number;
    competences_requises?: Record<string, any>;
    competences_acquises?: Record<string, any>;
    materiel_requis?: Record<string, any>;
    conditions_meteo?: Record<string, any>;
}

export interface FormationUpdate {
    titre?: string;
    description?: string;
    type?: 'technique' | 'securite' | 'agricole';
    duree?: number;
    competences_requises?: Record<string, any>;
    competences_acquises?: Record<string, any>;
    materiel_requis?: Record<string, any>;
    conditions_meteo?: Record<string, any>;
}

export interface SessionFormation {
    id: string;
    formation_id: string;
    date_debut: string;
    date_fin: string;
    lieu?: string;
    formateur?: string;
    statut: 'planifie' | 'en_cours' | 'termine' | 'annule';
    nb_places?: number;
    notes?: string;
    created_at: string;
    updated_at: string;
    formation: Formation;
}

export interface SessionFormationCreate {
    formation_id: string;
    date_debut: string;
    date_fin: string;
    lieu?: string;
    formateur?: string;
    statut?: 'planifie' | 'en_cours' | 'termine' | 'annule';
    nb_places?: number;
    notes?: string;
}

export interface SessionFormationUpdate {
    formation_id?: string;
    date_debut?: string;
    date_fin?: string;
    lieu?: string;
    formateur?: string;
    statut?: 'planifie' | 'en_cours' | 'termine' | 'annule';
    nb_places?: number;
    notes?: string;
}

export interface ParticipationFormation {
    id: string;
    session_id: string;
    employee_id: string;
    statut: 'inscrit' | 'present' | 'absent' | 'complete';
    note?: number;
    commentaires?: string;
    certification_obtenue: boolean;
    date_certification?: string;
    created_at: string;
    updated_at: string;
    session: SessionFormation;
}

export interface ParticipationFormationCreate {
    session_id: string;
    employee_id: string;
    statut?: 'inscrit' | 'present' | 'absent' | 'complete';
    note?: number;
    commentaires?: string;
    certification_obtenue?: boolean;
    date_certification?: string;
}

export interface ParticipationFormationUpdate {
    session_id?: string;
    employee_id?: string;
    statut?: 'inscrit' | 'present' | 'absent' | 'complete';
    note?: number;
    commentaires?: string;
    certification_obtenue?: boolean;
    date_certification?: string;
}

export interface Evaluation {
    id: string;
    employee_id: string;
    evaluateur_id: string;
    date_evaluation: string;
    type: 'periodique' | 'formation' | 'projet';
    periode_debut?: string;
    periode_fin?: string;
    competences: Record<string, any>;
    objectifs: Record<string, any>;
    performances: Record<string, any>;
    points_forts?: string;
    points_amelioration?: string;
    plan_action?: string;
    note_globale: number;
    statut: 'brouillon' | 'valide' | 'archive';
    created_at: string;
    updated_at: string;
}

export interface EvaluationCreate {
    employee_id: string;
    evaluateur_id: string;
    date_evaluation: string;
    type: 'periodique' | 'formation' | 'projet';
    periode_debut?: string;
    periode_fin?: string;
    competences: Record<string, any>;
    objectifs: Record<string, any>;
    performances: Record<string, any>;
    points_forts?: string;
    points_amelioration?: string;
    plan_action?: string;
    note_globale: number;
    statut?: 'brouillon' | 'valide' | 'archive';
}

export interface EvaluationUpdate {
    employee_id?: string;
    evaluateur_id?: string;
    date_evaluation?: string;
    type?: 'periodique' | 'formation' | 'projet';
    periode_debut?: string;
    periode_fin?: string;
    competences?: Record<string, any>;
    objectifs?: Record<string, any>;
    performances?: Record<string, any>;
    points_forts?: string;
    points_amelioration?: string;
    plan_action?: string;
    note_globale?: number;
    statut?: 'brouillon' | 'valide' | 'archive';
}

export interface FormationStatistics {
    nombre_sessions: number;
    nombre_participants: number;
    taux_reussite: number | null;
    note_moyenne: number | null;
}

export interface EvaluationSummary {
    nombre_evaluations: number;
    moyenne_globale: number | null;
    progression: number | null;
    points_forts: string[];
    points_amelioration: string[];
}

export interface EmployeeFormationHistory {
    formation: Formation;
    session: SessionFormation;
    participation: ParticipationFormation;
}
