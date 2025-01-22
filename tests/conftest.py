import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, Table
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from datetime import datetime, timedelta
from typing import Generator, Dict, Any
import sys
from pathlib import Path
from unittest.mock import AsyncMock

# Ajout du répertoire racine au PYTHONPATH
root_dir = str(Path(__file__).parent.parent)
if root_dir not in sys.path:
    sys.path.append(root_dir)

from main import app
from db.database import Base, get_db
from models.auth import Utilisateur, Role, TypeRole, Permission, role_permission

# Base de données en mémoire pour les tests
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Créer uniquement les tables nécessaires pour les tests d'authentification
def setup_test_db():
    # Créer une nouvelle base de métadonnées pour les tests
    from sqlalchemy import MetaData
    metadata = MetaData()
    
    # Copier uniquement les tables nécessaires
    for table in [Utilisateur.__table__, Role.__table__, Permission.__table__, role_permission]:
        table.to_metadata(metadata)
    
    # Créer les tables
    metadata.create_all(bind=engine)

@pytest.fixture(scope="function")
def db() -> Generator[Session, None, None]:
    # Supprimer et recréer les tables avant chaque test
    setup_test_db()
    
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.rollback()  # S'assurer qu'aucune transaction n'est en cours
        db.close()
        # Supprimer les tables après chaque test
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db: Session) -> Generator[TestClient, None, None]:
    def override_get_db():
        try:
            yield db
        finally:
            db.rollback()  # S'assurer qu'aucune transaction n'est en cours
    
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    del app.dependency_overrides[get_db]

@pytest.fixture(scope="function")
def test_user(db: Session) -> Utilisateur:
    role = Role(
        nom="Admin Test",
        type=TypeRole.ADMIN,
        description="Role de test"
    )
    db.add(role)
    db.commit()

    user = Utilisateur(
        email="test@fofal.cm",
        username="testuser",
        hashed_password="hashed_password",
        nom="Test",
        prenom="User",
        role_id=role.id
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@pytest.fixture(scope="function")
def ml_test_data() -> Dict[str, Any]:
    """Données de test pour les services ML"""
    return {
        "production": {
            "yield_prediction": 1200,
            "quality_prediction": 0.95,
            "maintenance_prediction": ["Machine A", "Machine C"]
        },
        "finance": {
            "revenue_prediction": 150000,
            "expense_prediction": 120000,
            "cash_flow_prediction": 30000
        },
        "inventory": {
            "stock_level_predictions": {"item_1": 100, "item_2": 50},
            "reorder_suggestions": ["item_3", "item_4"],
            "optimal_quantities": {"item_1": 150, "item_2": 75}
        },
        "hr": {
            "turnover_prediction": 0.15,
            "hiring_needs": ["Developer", "Manager"],
            "training_recommendations": ["Python", "Leadership"]
        }
    }

@pytest.fixture(scope="function")
def mock_ml_services() -> Dict[str, AsyncMock]:
    """Mock des services pour les tests d'intégration ML"""
    hr_service = AsyncMock()
    hr_service.get_critical_alerts.return_value = [
        {"type": "hr", "message": "Alerte RH", "priority": 2}
    ]
    hr_service.get_total_employees.return_value = 100
    hr_service.get_active_contracts_count.return_value = 95
    hr_service.get_completed_trainings_count.return_value = 50
    hr_service.get_training_completion_rate.return_value = 0.85

    production_service = AsyncMock()
    production_service.get_critical_alerts.return_value = [
        {"type": "production", "message": "Alerte Production", "priority": 1}
    ]
    production_service.get_daily_production.return_value = 1000
    production_service.get_efficiency_rate.return_value = 0.92
    production_service.get_active_sensors_count.return_value = 10

    finance_service = AsyncMock()
    finance_service.get_critical_alerts.return_value = [
        {"type": "finance", "message": "Alerte Finance", "priority": 3}
    ]
    finance_service.get_daily_revenue.return_value = 50000
    finance_service.get_monthly_expenses.return_value = 40000
    finance_service.get_cash_flow.return_value = 10000

    inventory_service = AsyncMock()
    inventory_service.get_critical_alerts.return_value = []
    inventory_service.get_total_items.return_value = 500
    inventory_service.get_low_stock_items.return_value = []
    inventory_service.get_total_stock_value.return_value = 100000

    weather_service = AsyncMock()
    weather_service.get_critical_alerts.return_value = []
    weather_service.get_current_conditions.return_value = {}
    weather_service.get_daily_forecast.return_value = []

    projects_ml_service = AsyncMock()
    projects_ml_service.get_production_predictions.return_value = {
        "yield_prediction": 1200,
        "quality_prediction": 0.95
    }
    projects_ml_service.get_finance_predictions.return_value = {
        "revenue_prediction": 150000,
        "expense_prediction": 120000
    }
    projects_ml_service.get_inventory_predictions.return_value = {
        "stock_level_predictions": {"item_1": 100}
    }
    projects_ml_service.get_hr_predictions.return_value = {
        "turnover_prediction": 0.15
    }

    cache_service = AsyncMock()
    cache_service.get.return_value = None

    return {
        "hr": hr_service,
        "production": production_service,
        "finance": finance_service,
        "inventory": inventory_service,
        "weather": weather_service,
        "projects_ml": projects_ml_service,
        "cache": cache_service
    }

@pytest.fixture(scope="function")
def mock_ml_cache_data() -> Dict[str, Any]:
    """Données de cache pour les tests ML"""
    return {
        "modules": {
            "production": {
                "daily_production": 1000,
                "efficiency_rate": 0.92,
                "active_sensors": 10
            },
            "hr": {
                "total_employees": 100,
                "active_contracts": 95,
                "training_completion": 0.85
            },
            "finance": {
                "daily_revenue": 50000,
                "monthly_expenses": 40000,
                "cash_flow": 10000
            },
            "inventory": {
                "total_items": 500,
                "total_value": 100000
            }
        },
        "alerts": [
            {"type": "production", "message": "Alerte Production", "priority": 1},
            {"type": "hr", "message": "Alerte RH", "priority": 2},
            {"type": "finance", "message": "Alerte Finance", "priority": 3}
        ],
        "predictions": {
            "production": {
                "yield_prediction": 1200,
                "quality_prediction": 0.95
            },
            "finance": {
                "revenue_prediction": 150000,
                "expense_prediction": 120000
            },
            "inventory": {
                "stock_level_predictions": {"item_1": 100}
            },
            "hr": {
                "turnover_prediction": 0.15
            }
        },
        "timestamp": datetime.now().isoformat()
    }
