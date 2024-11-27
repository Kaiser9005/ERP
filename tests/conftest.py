import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
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
from models import (
    Utilisateur, Role, TypeRole,
    Parcelle, Recolte, CultureType, ParcelleStatus,
    Produit, Stock, CategoryProduit, UniteMesure
)

# Base de données en mémoire pour les tests
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db() -> Generator[Session, None, None]:
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db: Session) -> Generator[TestClient, None, None]:
    def override_get_db():
        try:
            yield db
        finally:
            pass
    
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
def test_data(db: Session, test_user: Utilisateur) -> Dict[str, Any]:
    # Création d'une parcelle
    parcelle = Parcelle(
        code="P001",
        culture_type=CultureType.PALMIER,
        surface_hectares=10.5,
        date_plantation=datetime.now().date(),
        statut=ParcelleStatus.ACTIVE,
        responsable_id=test_user.id
    )
    db.add(parcelle)

    # Création de récoltes
    for i in range(5):
        recolte = Recolte(
            parcelle_id=parcelle.id,
            date_recolte=(datetime.now() - timedelta(days=i)).date(),
            quantite_kg=500 + i * 100,
            qualite="A",
            equipe_recolte=[str(test_user.id)]
        )
        db.add(recolte)

    # Création de produits et stocks
    produit = Produit(
        code="PRD001",
        nom="Engrais NPK",
        categorie=CategoryProduit.INTRANT,
        unite_mesure=UniteMesure.KG,
        seuil_alerte=100,
        prix_unitaire=1500
    )
    db.add(produit)

    stock = Stock(
        produit_id=produit.id,
        quantite=250,
        valeur_unitaire=1500
    )
    db.add(stock)

    db.commit()
    return {
        "parcelle": parcelle,
        "produit": produit,
        "stock": stock
    }

# Nouvelles fixtures pour les tests ML

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
