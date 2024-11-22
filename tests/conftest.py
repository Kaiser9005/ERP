import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from datetime import datetime, timedelta
from typing import Generator, Dict, Any
import sys
from pathlib import Path

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
