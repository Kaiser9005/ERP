"""Tests d'intégration Production-Inventaire."""

import pytest
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from fastapi import HTTPException

from models.inventory import Produit, Stock, MouvementStock
from models.iot_sensor import IoTSensor, SensorType, SensorStatus
from models.production import Recolte, Parcelle
from services.inventory_service import InventoryService
from services.iot_service import IoTService
from services.production_service import ProductionService
from services.weather_service import WeatherService
from schemas.inventaire import (
    MouvementStockCreate,
    ControleQualite,
    ConditionsActuelles,
    Certification
)

@pytest.fixture
def test_db(test_session: Session):
    """Fixture pour la base de données de test."""
    # Création d'une parcelle de test
    parcelle = Parcelle(
        code="P001",
        surface=1000,
        culture="Palmiers",
        date_plantation=datetime.utcnow() - timedelta(days=100)
    )
    test_session.add(parcelle)

    # Création d'un produit de test
    produit = Produit(
        code="PALM001",
        nom="Huile de Palme",
        type="RECOLTE",
        unite="litres",
        conditions_stockage={
            "temperature_min": 15,
            "temperature_max": 25,
            "humidite_min": 30,
            "humidite_max": 60
        }
    )
    test_session.add(produit)

    # Création d'un entrepôt de test
    entrepot = Stock(
        code="E001",
        nom="Entrepôt Principal",
        capacite=10000
    )
    test_session.add(entrepot)

    # Création des capteurs IoT
    sensors = [
        IoTSensor(
            code=f"SENSOR00{i}",
            type=sensor_type,
            status=SensorStatus.ACTIF,
            parcelle_id=parcelle.id,
            config={},
            seuils_alerte={
                "min": min_val,
                "max": max_val
            }
        )
        for i, (sensor_type, min_val, max_val) in enumerate([
            (SensorType.TEMPERATURE_AIR, 15, 25),
            (SensorType.HUMIDITE_AIR, 30, 60),
            (SensorType.LUMINOSITE, 100, 1000)
        ], 1)
    ]
    for sensor in sensors:
        test_session.add(sensor)

    test_session.commit()

    yield test_session

    # Nettoyage
    test_session.query(MouvementStock).delete()
    test_session.query(Stock).delete()
    test_session.query(Produit).delete()
    test_session.query(IoTSensor).delete()
    test_session.query(Recolte).delete()
    test_session.query(Parcelle).delete()
    test_session.commit()

@pytest.mark.asyncio
async def test_recolte_to_stock_workflow(test_db: Session):
    """Test du workflow complet récolte -> contrôle qualité -> stockage."""
    # Services
    inventory_service = InventoryService(test_db)
    iot_service = IoTService(test_db)
    production_service = ProductionService(test_db)
    
    # 1. Enregistrement d'une récolte
    recolte = await production_service.create_recolte({
        "parcelle_id": test_db.query(Parcelle).first().id,
        "date_recolte": datetime.utcnow(),
        "quantite": 1000,
        "qualite": "A",
        "conditions_recolte": {
            "temperature": 22,
            "humidite": 45,
            "meteo": "ENSOLEILLE"
        }
    })
    assert recolte.quantite == 1000
    assert recolte.qualite == "A"

    # 2. Création du mouvement de stock avec contrôle qualité
    mouvement = await inventory_service.create_mouvement(
        MouvementStockCreate(
            type_mouvement="ENTREE",
            produit_id=test_db.query(Produit).first().id,
            entrepot_destination_id=test_db.query(Stock).first().id,
            quantite=recolte.quantite,
            recolte_id=recolte.id,
            controle_qualite=ControleQualite(
                date_controle=datetime.utcnow(),
                controleur="SYSTEM",
                conforme=True,
                criteres_controle={
                    "aspect": "CONFORME",
                    "humidite": "CONFORME",
                    "impuretes": "CONFORME"
                }
            )
        ),
        "SYSTEM"
    )
    assert mouvement.quantite == 1000
    assert mouvement.controle_qualite["conforme"] == True

    # 3. Vérification du stock
    stock = await inventory_service._get_stock(
        mouvement.produit_id,
        mouvement.entrepot_destination_id
    )
    assert stock.quantite == 1000

    # 4. Ajout certification
    stock = await inventory_service.add_certification(
        stock.id,
        Certification(
            type="BIO",
            date_obtention=datetime.utcnow(),
            validite_mois=12,
            organisme="ECOCERT"
        )
    )
    assert len(stock.certifications) == 1
    assert stock.certifications[0]["type"] == "BIO"

@pytest.mark.asyncio
async def test_storage_conditions_monitoring(test_db: Session):
    """Test de la surveillance des conditions de stockage."""
    inventory_service = InventoryService(test_db, iot_service=IoTService(test_db))
    
    # 1. Liaison des capteurs au stock
    stock = test_db.query(Stock).first()
    sensors = test_db.query(IoTSensor).all()
    stock = await inventory_service.link_sensors(
        stock.id,
        [sensor.id for sensor in sensors]
    )
    assert len(stock.capteurs_id) == 3

    # 2. Vérification des conditions actuelles
    conditions = await inventory_service._get_current_conditions(stock)
    assert conditions is not None
    assert hasattr(conditions, "temperature")
    assert hasattr(conditions, "humidite")

    # 3. Vérification des alertes
    alerts = await inventory_service._check_storage_conditions()
    assert isinstance(alerts, list)

@pytest.mark.asyncio
async def test_weather_impact_on_storage(test_db: Session):
    """Test de l'impact des conditions météo sur le stockage."""
    inventory_service = InventoryService(
        test_db,
        iot_service=IoTService(test_db, weather_service=WeatherService())
    )
    
    # 1. Création d'un mouvement avec conditions météo
    mouvement = await inventory_service.create_mouvement(
        MouvementStockCreate(
            type_mouvement="ENTREE",
            produit_id=test_db.query(Produit).first().id,
            entrepot_destination_id=test_db.query(Stock).first().id,
            quantite=500,
            conditions_transport={
                "temperature": 22,
                "humidite": 45,
                "duree_transport": 30,
                "type_transport": "REFRIGERE"
            }
        ),
        "SYSTEM"
    )
    assert mouvement.conditions_transport["temperature"] == 22

    # 2. Vérification de l'ajustement des conditions
    stock = await inventory_service._get_stock(
        mouvement.produit_id,
        mouvement.entrepot_destination_id
    )
    assert stock.conditions_actuelles is not None
    assert "temperature" in stock.conditions_actuelles

    # 3. Vérification des alertes météo
    alerts = await inventory_service._check_storage_conditions()
    assert isinstance(alerts, list)

@pytest.mark.asyncio
async def test_quality_control_rejection(test_db: Session):
    """Test du rejet d'un lot pour qualité insuffisante."""
    inventory_service = InventoryService(test_db)
    
    # Tentative de création d'un mouvement avec contrôle qualité non conforme
    with pytest.raises(HTTPException) as exc_info:
        await inventory_service.create_mouvement(
            MouvementStockCreate(
                type_mouvement="ENTREE",
                produit_id=test_db.query(Produit).first().id,
                entrepot_destination_id=test_db.query(Stock).first().id,
                quantite=200,
                controle_qualite=ControleQualite(
                    date_controle=datetime.utcnow(),
                    controleur="SYSTEM",
                    conforme=False,
                    criteres_controle={
                        "aspect": "NON_CONFORME",
                        "humidite": "HORS_NORME",
                        "impuretes": "EXCESSIF"
                    },
                    actions_requises="Lot à détruire"
                )
            ),
            "SYSTEM"
        )
    
    assert exc_info.value.status_code == 400
    assert "non conforme" in str(exc_info.value.detail).lower()

@pytest.mark.asyncio
async def test_stock_statistics_after_movements(test_db: Session):
    """Test des statistiques de stock après mouvements."""
    inventory_service = InventoryService(test_db)
    
    # 1. Création de plusieurs mouvements
    for quantite in [300, 200, -100]:  # Entrées et sortie
        await inventory_service.create_mouvement(
            MouvementStockCreate(
                type_mouvement="ENTREE" if quantite > 0 else "SORTIE",
                produit_id=test_db.query(Produit).first().id,
                entrepot_destination_id=test_db.query(Stock).first().id if quantite > 0 else None,
                entrepot_source_id=test_db.query(Stock).first().id if quantite < 0 else None,
                quantite=abs(quantite)
            ),
            "SYSTEM"
        )

    # 2. Vérification des statistiques
    stats = await inventory_service.get_stats()
    assert stats["movements"] == 3  # Nombre total de mouvements
    assert stats["turnoverRate"] > 0  # Taux de rotation
