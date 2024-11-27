import axios from 'axios';
import { 
    Formation, FormationCreate, FormationUpdate,
    SessionFormation, SessionFormationCreate, SessionFormationUpdate,
    ParticipationFormation, ParticipationFormationCreate, ParticipationFormationUpdate,
    Evaluation, EvaluationCreate, EvaluationUpdate,
    FormationStatistics, EvaluationSummary, EmployeeFormationHistory
} from '../types/formation';

const BASE_URL = '/api/v1/hr/formation';

// Services Formation
export const createFormation = async (formation: FormationCreate): Promise<Formation> => {
    const response = await axios.post(`${BASE_URL}/formations/`, formation);
    return response.data;
};

export const getFormations = async (params?: {
    skip?: number;
    limit?: number;
    type?: string;
}): Promise<Formation[]> => {
    const response = await axios.get(`${BASE_URL}/formations/`, { params });
    return response.data;
};

export const getFormation = async (id: string): Promise<Formation> => {
    const response = await axios.get(`${BASE_URL}/formations/${id}`);
    return response.data;
};

export const updateFormation = async (
    id: string,
    formation: FormationUpdate
): Promise<Formation> => {
    const response = await axios.put(`${BASE_URL}/formations/${id}`, formation);
    return response.data;
};

export const deleteFormation = async (id: string): Promise<void> => {
    await axios.delete(`${BASE_URL}/formations/${id}`);
};

// Services Session Formation
export const createSession = async (session: SessionFormationCreate): Promise<SessionFormation> => {
    const response = await axios.post(`${BASE_URL}/sessions/`, session);
    return response.data;
};

export const getSessions = async (params?: {
    skip?: number;
    limit?: number;
    formation_id?: string;
    statut?: string;
    date_debut?: string;
}): Promise<SessionFormation[]> => {
    const response = await axios.get(`${BASE_URL}/sessions/`, { params });
    return response.data;
};

export const getSession = async (id: string): Promise<SessionFormation> => {
    const response = await axios.get(`${BASE_URL}/sessions/${id}`);
    return response.data;
};

export const updateSession = async (
    id: string,
    session: SessionFormationUpdate
): Promise<SessionFormation> => {
    const response = await axios.put(`${BASE_URL}/sessions/${id}`, session);
    return response.data;
};

export const deleteSession = async (id: string): Promise<void> => {
    await axios.delete(`${BASE_URL}/sessions/${id}`);
};

// Services Participation Formation
export const createParticipation = async (
    participation: ParticipationFormationCreate
): Promise<ParticipationFormation> => {
    const response = await axios.post(`${BASE_URL}/participations/`, participation);
    return response.data;
};

export const getParticipations = async (params?: {
    skip?: number;
    limit?: number;
    session_id?: string;
    employee_id?: string;
    statut?: string;
}): Promise<ParticipationFormation[]> => {
    const response = await axios.get(`${BASE_URL}/participations/`, { params });
    return response.data;
};

export const getParticipation = async (id: string): Promise<ParticipationFormation> => {
    const response = await axios.get(`${BASE_URL}/participations/${id}`);
    return response.data;
};

export const updateParticipation = async (
    id: string,
    participation: ParticipationFormationUpdate
): Promise<ParticipationFormation> => {
    const response = await axios.put(`${BASE_URL}/participations/${id}`, participation);
    return response.data;
};

export const deleteParticipation = async (id: string): Promise<void> => {
    await axios.delete(`${BASE_URL}/participations/${id}`);
};

// Services Evaluation
export const createEvaluation = async (evaluation: EvaluationCreate): Promise<Evaluation> => {
    const response = await axios.post(`${BASE_URL}/evaluations/`, evaluation);
    return response.data;
};

export const getEvaluations = async (params?: {
    skip?: number;
    limit?: number;
    employee_id?: string;
    evaluateur_id?: string;
    type?: string;
    statut?: string;
    date_debut?: string;
    date_fin?: string;
}): Promise<Evaluation[]> => {
    const response = await axios.get(`${BASE_URL}/evaluations/`, { params });
    return response.data;
};

export const getEvaluation = async (id: string): Promise<Evaluation> => {
    const response = await axios.get(`${BASE_URL}/evaluations/${id}`);
    return response.data;
};

export const updateEvaluation = async (
    id: string,
    evaluation: EvaluationUpdate
): Promise<Evaluation> => {
    const response = await axios.put(`${BASE_URL}/evaluations/${id}`, evaluation);
    return response.data;
};

export const deleteEvaluation = async (id: string): Promise<void> => {
    await axios.delete(`${BASE_URL}/evaluations/${id}`);
};

// Services Statistiques et Rapports
export const getEmployeeFormationsHistory = async (params: {
    employee_id: string;
    statut?: string;
    type?: string;
}): Promise<EmployeeFormationHistory[]> => {
    const response = await axios.get(`${BASE_URL}/employee/${params.employee_id}/formations`, {
        params: {
            statut: params.statut,
            type: params.type
        }
    });
    return response.data;
};

export const getEmployeeEvaluationsSummary = async (params: {
    employee_id: string;
    date_debut?: string;
    date_fin?: string;
}): Promise<EvaluationSummary> => {
    const response = await axios.get(
        `${BASE_URL}/employee/${params.employee_id}/evaluations/summary`,
        { params }
    );
    return response.data;
};

export const getFormationStatistics = async (
    formation_id: string
): Promise<FormationStatistics> => {
    const response = await axios.get(`${BASE_URL}/formations/${formation_id}/statistics`);
    return response.data;
};
