import pytest
from datetime import datetime, timedelta
from uuid import uuid4

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from models.hr_formation import Formation, SessionFormation, ParticipationFormation
from services.hr_formation_service import HRFormationService
from schemas.hr_formation import FormationCreate, SessionFormationCreate, ParticipationFormationCreate

@pytest.fixture
def formation_service(db_session: Session):
    return HRFormationService(db_session)

@pytest.fixture
def test_formation(formation_service: HRFormationService):
    formation_data = {
        "titre": "Formation Test Integration",
        "description": "Description test integration",
        "type": "technique",
        "duree": 8,
        "competences_requises": {"niveau": "debutant"},
        "competences_acquises": {"technique": "base"},
        "materiel_requis": {"ordinateur": True},
        "conditions_meteo": {"exterieur": False}
    }
    return formation_service.create_formation(FormationCreate(**formation_data))

@pytest.fixture
def test_session(formation_service: HRFormationService, test_formation: Formation):
    session_data = {
        "formation_id": str(test_formation.id),
        "date_debut": datetime.now(),
        "date_fin": datetime.now() + timedelta(hours=8),
        "lieu": "Salle Test Integration",
        "formateur": "Jean Test Integration",
        "statut": "planifie",
        "nb_places": 10,
        "notes": "Notes test integration"
    }
    return formation_service.create_session(SessionFormationCreate(**session_data))

class TestFormationIntegration:
    def test_formation_workflow(self, client: TestClient, test_formation: Formation):
        # Récupérer la formation via l'API
        response = client.get(f"/api/v1/hr/formation/formations/{test_formation.id}")
        assert response.status_code == 200
        formation_data = response.json()
        assert formation_data["titre"] == test_formation.titre

        # Mettre à jour la formation
        update_data = {
            "titre": "Formation Test Integration Updated",
            "description": "Description mise à jour"
        }
        response = client.put(
            f"/api/v1/hr/formation/formations/{test_formation.id}",
            json=update_data
        )
        assert response.status_code == 200
        updated_data = response.json()
        assert updated_data["titre"] == update_data["titre"]

        # Vérifier la liste des formations
        response = client.get("/api/v1/hr/formation/formations/")
        assert response.status_code == 200
        formations = response.json()
        assert len(formations) > 0
        assert any(f["id"] == str(test_formation.id) for f in formations)

    def test_session_workflow(
        self,
        client: TestClient,
        test_formation: Formation,
        test_session: SessionFormation
    ):
        # Récupérer la session via l'API
        response = client.get(f"/api/v1/hr/formation/sessions/{test_session.id}")
        assert response.status_code == 200
        session_data = response.json()
        assert session_data["lieu"] == test_session.lieu

        # Mettre à jour la session
        update_data = {
            "lieu": "Nouvelle Salle",
            "notes": "Notes mises à jour"
        }
        response = client.put(
            f"/api/v1/hr/formation/sessions/{test_session.id}",
            json=update_data
        )
        assert response.status_code == 200
        updated_data = response.json()
        assert updated_data["lieu"] == update_data["lieu"]

        # Vérifier la liste des sessions
        response = client.get("/api/v1/hr/formation/sessions/")
        assert response.status_code == 200
        sessions = response.json()
        assert len(sessions) > 0
        assert any(s["id"] == str(test_session.id) for s in sessions)

    def test_participation_workflow(
        self,
        client: TestClient,
        test_session: SessionFormation,
        formation_service: HRFormationService
    ):
        # Créer une participation
        employee_id = str(uuid4())
        participation_data = {
            "session_id": str(test_session.id),
            "employee_id": employee_id,
            "statut": "inscrit"
        }
        response = client.post(
            "/api/v1/hr/formation/participations/",
            json=participation_data
        )
        assert response.status_code == 201
        participation = response.json()
        participation_id = participation["id"]

        # Mettre à jour la participation
        update_data = {
            "statut": "present",
            "note": 85,
            "certification_obtenue": True
        }
        response = client.put(
            f"/api/v1/hr/formation/participations/{participation_id}",
            json=update_data
        )
        assert response.status_code == 200
        updated_data = response.json()
        assert updated_data["statut"] == update_data["statut"]
        assert updated_data["note"] == update_data["note"]

        # Vérifier l'historique des formations de l'employé
        response = client.get(
            f"/api/v1/hr/formation/employee/{employee_id}/formations"
        )
        assert response.status_code == 200
        history = response.json()
        assert len(history) > 0
        assert history[0]["participation"]["id"] == participation_id

    def test_formation_statistics(
        self,
        client: TestClient,
        test_formation: Formation,
        test_session: SessionFormation,
        formation_service: HRFormationService
    ):
        # Créer plusieurs participations
        for i in range(3):
            participation_data = {
                "session_id": str(test_session.id),
                "employee_id": str(uuid4()),
                "statut": "complete",
                "note": 80 + i,
                "certification_obtenue": True
            }
            formation_service.create_participation(
                ParticipationFormationCreate(**participation_data)
            )

        # Vérifier les statistiques
        response = client.get(
            f"/api/v1/hr/formation/formations/{test_formation.id}/statistics"
        )
        assert response.status_code == 200
        stats = response.json()
        assert stats["nombre_sessions"] == 1
        assert stats["nombre_participants"] == 3
        assert stats["taux_reussite"] == 100
        assert stats["note_moyenne"] is not None

    def test_evaluation_workflow(self, client: TestClient):
        # Créer une évaluation
        employee_id = str(uuid4())
        evaluation_data = {
            "employee_id": employee_id,
            "evaluateur_id": str(uuid4()),
            "date_evaluation": datetime.now().isoformat(),
            "type": "formation",
            "competences": {"technique": 4},
            "objectifs": {"objectif1": "atteint"},
            "performances": {"performance1": 85},
            "note_globale": 85,
            "points_forts": "Points forts test",
            "points_amelioration": "Points à améliorer test",
            "statut": "brouillon"
        }
        response = client.post(
            "/api/v1/hr/formation/evaluations/",
            json=evaluation_data
        )
        assert response.status_code == 201
        evaluation = response.json()
        evaluation_id = evaluation["id"]

        # Mettre à jour l'évaluation
        update_data = {
            "statut": "valide",
            "note_globale": 90
        }
        response = client.put(
            f"/api/v1/hr/formation/evaluations/{evaluation_id}",
            json=update_data
        )
        assert response.status_code == 200
        updated_data = response.json()
        assert updated_data["statut"] == update_data["statut"]
        assert updated_data["note_globale"] == update_data["note_globale"]

        # Vérifier le résumé des évaluations
        response = client.get(
            f"/api/v1/hr/formation/employee/{employee_id}/evaluations/summary"
        )
        assert response.status_code == 200
        summary = response.json()
        assert summary["nombre_evaluations"] == 1
        assert summary["moyenne_globale"] == 90
