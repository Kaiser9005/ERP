import pytest
from datetime import datetime, timedelta
from uuid import uuid4

from models.hr_formation import Formation, SessionFormation, ParticipationFormation, Evaluation
from services.hr_formation_service import HRFormationService
from schemas.hr_formation import (
    FormationCreate, SessionFormationCreate,
    ParticipationFormationCreate, EvaluationCreate
)

@pytest.fixture
def formation_service(db_session):
    return HRFormationService(db_session)

@pytest.fixture
def formation_data():
    return {
        "titre": "Formation Test",
        "description": "Description test",
        "type": "technique",
        "duree": 8,
        "competences_requises": {"niveau": "debutant"},
        "competences_acquises": {"technique": "base"},
        "materiel_requis": {"ordinateur": True},
        "conditions_meteo": {"exterieur": False}
    }

@pytest.fixture
def session_data(formation_id):
    return {
        "formation_id": formation_id,
        "date_debut": datetime.now(),
        "date_fin": datetime.now() + timedelta(hours=8),
        "lieu": "Salle Test",
        "formateur": "Jean Test",
        "statut": "planifie",
        "nb_places": 10,
        "notes": "Notes test"
    }

class TestFormationService:
    def test_create_formation(self, formation_service, formation_data):
        formation_create = FormationCreate(**formation_data)
        formation = formation_service.create_formation(formation_create)
        
        assert formation.titre == formation_data["titre"]
        assert formation.type == formation_data["type"]
        assert formation.duree == formation_data["duree"]

    def test_get_formation(self, formation_service, formation_data):
        formation_create = FormationCreate(**formation_data)
        created = formation_service.create_formation(formation_create)
        
        retrieved = formation_service.get_formation(created.id)
        assert retrieved is not None
        assert retrieved.id == created.id
        assert retrieved.titre == created.titre

    def test_get_formations(self, formation_service, formation_data):
        formation_create = FormationCreate(**formation_data)
        formation_service.create_formation(formation_create)
        
        formations = formation_service.get_formations()
        assert len(formations) > 0

    def test_update_formation(self, formation_service, formation_data):
        formation_create = FormationCreate(**formation_data)
        created = formation_service.create_formation(formation_create)
        
        new_title = "Formation Mise à Jour"
        updated = formation_service.update_formation(
            created.id,
            FormationCreate(
                **{**formation_data, "titre": new_title}
            )
        )
        
        assert updated.titre == new_title

    def test_delete_formation(self, formation_service, formation_data):
        formation_create = FormationCreate(**formation_data)
        created = formation_service.create_formation(formation_create)
        
        assert formation_service.delete_formation(created.id) is True
        assert formation_service.get_formation(created.id) is None

class TestSessionService:
    def test_create_session(self, formation_service, formation_data, session_data):
        formation_create = FormationCreate(**formation_data)
        formation = formation_service.create_formation(formation_create)
        
        session_create = SessionFormationCreate(**{
            **session_data,
            "formation_id": str(formation.id)
        })
        session = formation_service.create_session(session_create)
        
        assert session.formation_id == str(formation.id)
        assert session.lieu == session_data["lieu"]

    def test_get_sessions(self, formation_service, formation_data, session_data):
        formation_create = FormationCreate(**formation_data)
        formation = formation_service.create_formation(formation_create)
        
        session_create = SessionFormationCreate(**{
            **session_data,
            "formation_id": str(formation.id)
        })
        formation_service.create_session(session_create)
        
        sessions = formation_service.get_sessions()
        assert len(sessions) > 0

class TestParticipationService:
    def test_create_participation(
        self,
        formation_service,
        formation_data,
        session_data
    ):
        # Créer une formation
        formation_create = FormationCreate(**formation_data)
        formation = formation_service.create_formation(formation_create)
        
        # Créer une session
        session_create = SessionFormationCreate(**{
            **session_data,
            "formation_id": str(formation.id)
        })
        session = formation_service.create_session(session_create)
        
        # Créer une participation
        participation_data = {
            "session_id": str(session.id),
            "employee_id": str(uuid4()),
            "statut": "inscrit"
        }
        participation_create = ParticipationFormationCreate(**participation_data)
        participation = formation_service.create_participation(participation_create)
        
        assert participation.session_id == str(session.id)
        assert participation.statut == "inscrit"

class TestEvaluationService:
    def test_create_evaluation(self, formation_service):
        evaluation_data = {
            "employee_id": str(uuid4()),
            "evaluateur_id": str(uuid4()),
            "date_evaluation": datetime.now(),
            "type": "formation",
            "competences": {"technique": 4},
            "objectifs": {"objectif1": "atteint"},
            "performances": {"performance1": 85},
            "note_globale": 85,
            "statut": "brouillon"
        }
        evaluation_create = EvaluationCreate(**evaluation_data)
        evaluation = formation_service.create_evaluation(evaluation_create)
        
        assert evaluation.employee_id == evaluation_data["employee_id"]
        assert evaluation.note_globale == evaluation_data["note_globale"]

    def test_get_employee_evaluations_summary(
        self,
        formation_service
    ):
        employee_id = str(uuid4())
        
        # Créer quelques évaluations
        for i in range(3):
            evaluation_data = {
                "employee_id": employee_id,
                "evaluateur_id": str(uuid4()),
                "date_evaluation": datetime.now(),
                "type": "formation",
                "competences": {"technique": 4},
                "objectifs": {"objectif1": "atteint"},
                "performances": {"performance1": 85},
                "note_globale": 80 + i,
                "points_forts": f"Point fort {i}",
                "points_amelioration": f"Point amélioration {i}",
                "statut": "valide"
            }
            formation_service.create_evaluation(
                EvaluationCreate(**evaluation_data)
            )
        
        summary = formation_service.get_employee_evaluations_summary(
            employee_id
        )
        
        assert summary["nombre_evaluations"] == 3
        assert summary["moyenne_globale"] is not None
        assert len(summary["points_forts"]) > 0
        assert len(summary["points_amelioration"]) > 0

    def test_get_formation_statistics(
        self,
        formation_service,
        formation_data,
        session_data
    ):
        # Créer une formation
        formation_create = FormationCreate(**formation_data)
        formation = formation_service.create_formation(formation_create)
        
        # Créer une session
        session_create = SessionFormationCreate(**{
            **session_data,
            "formation_id": str(formation.id)
        })
        session = formation_service.create_session(session_create)
        
        # Créer quelques participations
        for i in range(3):
            participation_data = {
                "session_id": str(session.id),
                "employee_id": str(uuid4()),
                "statut": "complete",
                "note": 80 + i,
                "certification_obtenue": True
            }
            formation_service.create_participation(
                ParticipationFormationCreate(**participation_data)
            )
        
        stats = formation_service.get_formation_statistics(formation.id)
        
        assert stats["nombre_sessions"] == 1
        assert stats["nombre_participants"] == 3
        assert stats["taux_reussite"] == 100
        assert stats["note_moyenne"] is not None
