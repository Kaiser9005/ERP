import pytest
from datetime import datetime, timedelta
from services.inventory_service import InventoryService
from unittest.mock import AsyncMock, Mock
from fastapi import HTTPException
from models.inventory import Produit, Stock, MouvementStock
from models.parametrage import Entrepot
from schemas.inventaire import MouvementStockCreate, ControleQualite, Certification

@pytest.mark.asyncio
async def test_get_stats(db, test_user, test_data):
    """Test de récupération des statistiques d'inventaire"""
    # Créer un entrepôt de test
    entrepot = Entrepot(
        code="E001",
        nom="Entrepôt Principal",
        localisation="Zone A"
    )
    db.add(entrepot)
    db.commit()

    service = InventoryService(db)
    stats = await service.get_stats()

    assert "totalValue" in stats
    assert "turnoverRate" in stats
    assert "alerts" in stats
    assert "movements" in stats
    assert stats["totalValue"] >= 0

@pytest.mark.asyncio
async def test_create_mouvement_entree(db, test_user, test_data):
    """Test de création d'un mouvement d'entrée"""
    # Créer un entrepôt de test
    entrepot = Entrepot(
        code="E001",
        nom="Entrepôt Principal",
        localisation="Zone A"
    )
    db.add(entrepot)
    db.commit()

    service = InventoryService(db)
    
    mouvement = MouvementStockCreate(
        produit_id=test_data["produit"].id,
        type_mouvement="ENTREE",
        quantite=100,
        entrepot_destination_id=entrepot.id,
        cout_unitaire=1500
    )

    result = await service.create_mouvement(mouvement, test_user.id)
    assert result.id is not None
    assert result.quantite == 100

    # Vérifier la mise à jour du stock
    stock = db.query(Stock).filter(
        Stock.produit_id == test_data["produit"].id,
        Stock.entrepot_id == entrepot.id
    ).first()
    assert stock.quantite == 100
    assert stock.valeur_unitaire == 1500

@pytest.mark.asyncio
async def test_create_mouvement_sortie(db, test_user, test_data):
    """Test de création d'un mouvement de sortie"""
    # Créer un entrepôt de test
    entrepot = Entrepot(
        code="E001",
        nom="Entrepôt Principal",
        localisation="Zone A"
    )
    db.add(entrepot)
    db.commit()

    service = InventoryService(db)
    
    # Créer un stock initial
    stock = Stock(
        produit_id=test_data["produit"].id,
        entrepot_id=entrepot.id,
        quantite=100,
        valeur_unitaire=1500
    )
    db.add(stock)
    db.commit()

    mouvement = MouvementStockCreate(
        produit_id=test_data["produit"].id,
        type_mouvement="SORTIE",
        quantite=50,
        entrepot_source_id=entrepot.id
    )

    result = await service.create_mouvement(mouvement, test_user.id)
    assert result.id is not None
    assert result.quantite == 50

    # Vérifier la mise à jour du stock
    db.refresh(stock)
    assert stock.quantite == 50

@pytest.mark.asyncio
async def test_create_mouvement_sortie_insuffisant(db, test_user, test_data):
    """Test de sortie avec stock insuffisant"""
    # Créer un entrepôt de test
    entrepot = Entrepot(
        code="E001",
        nom="Entrepôt Principal",
        localisation="Zone A"
    )
    db.add(entrepot)
    db.commit()

    service = InventoryService(db)
    
    # Créer un stock initial
    stock = Stock(
        produit_id=test_data["produit"].id,
        entrepot_id=entrepot.id,
        quantite=30,
        valeur_unitaire=1500
    )
    db.add(stock)
    db.commit()

    mouvement = MouvementStockCreate(
        produit_id=test_data["produit"].id,
        type_mouvement="SORTIE",
        quantite=50,
        entrepot_source_id=entrepot.id
    )

    with pytest.raises(ValueError, match="Stock insuffisant"):
        await service.create_mouvement(mouvement, test_user.id)

@pytest.mark.asyncio
async def test_create_mouvement_transfert(db, test_user, test_data):
    """Test de création d'un mouvement de transfert"""
    # Créer les entrepôts de test
    entrepot1 = Entrepot(
        code="E001",
        nom="Entrepôt Principal",
        localisation="Zone A"
    )
    db.add(entrepot1)

    entrepot2 = Entrepot(
        code="E002",
        nom="Entrepôt 2",
        localisation="Zone B"
    )
    db.add(entrepot2)
    db.commit()

    service = InventoryService(db)
    
    # Créer un stock initial
    stock_source = Stock(
        produit_id=test_data["produit"].id,
        entrepot_id=entrepot1.id,
        quantite=100,
        valeur_unitaire=1500
    )
    db.add(stock_source)
    db.commit()

    mouvement = MouvementStockCreate(
        produit_id=test_data["produit"].id,
        type_mouvement="TRANSFERT",
        quantite=50,
        entrepot_source_id=entrepot1.id,
        entrepot_destination_id=entrepot2.id
    )

    result = await service.create_mouvement(mouvement, test_user.id)
    assert result.id is not None

    # Vérifier les stocks
    db.refresh(stock_source)
    assert stock_source.quantite == 50

    stock_dest = db.query(Stock).filter(
        Stock.produit_id == test_data["produit"].id,
        Stock.entrepot_id == entrepot2.id
    ).first()
    assert stock_dest.quantite == 50

@pytest.mark.asyncio
async def test_check_storage_conditions(db, test_user, test_data):
    """Test de vérification des conditions de stockage"""
    service = InventoryService(db)
    
    # Créer un produit avec conditions de stockage
    produit = test_data["produit"]
    produit.conditions_stockage = {
        "temperature_min": 15,
        "temperature_max": 25,
        "humidite_min": 40,
        "humidite_max": 60
    }
    db.add(produit)
    
    # Créer un stock avec capteurs
    stock = Stock(
        produit_id=produit.id,
        entrepot_id=test_data["entrepot"].id,
        quantite=100,
        capteurs_id=["sensor1", "sensor2"]
    )
    db.add(stock)
    db.commit()

    # Mock IoT service
    mock_iot = AsyncMock()
    mock_iot.get_sensor.return_value = True
    mock_iot.get_sensor_readings.return_value = [
        Mock(type="TEMPERATURE", valeur=30),  # Trop chaud
        Mock(type="HUMIDITE", valeur=35)      # Trop sec
    ]
    service.iot_service = mock_iot

    # Vérifier les alertes
    alerts = await service._check_storage_conditions()
    assert len(alerts) == 2
    assert any(a["type"] == "temperature" for a in alerts)
    assert any(a["type"] == "humidite" for a in alerts)

@pytest.mark.asyncio
async def test_add_certification(db, test_user, test_data):
    """Test d'ajout de certification"""
    service = InventoryService(db)
    
    # Créer un stock
    stock = Stock(
        produit_id=test_data["produit"].id,
        entrepot_id=test_data["entrepot"].id,
        quantite=100
    )
    db.add(stock)
    db.commit()

    # Ajouter une certification
    certification = {
        "type": "BIO",
        "date_obtention": datetime.now().isoformat(),
        "date_expiration": (datetime.now() + timedelta(days=365)).isoformat(),
        "organisme": "Ecocert",
        "numero": "BIO-2024-001"
    }

    result = await service.add_certification(str(stock.id), Certification(**certification))
    assert result.certifications
    assert len(result.certifications) == 1
    assert result.certifications[0]["type"] == "BIO"

@pytest.mark.asyncio
async def test_link_sensors(db, test_user, test_data):
    """Test de liaison des capteurs"""
    service = InventoryService(db)
    
    # Créer un stock
    stock = Stock(
        produit_id=test_data["produit"].id,
        entrepot_id=test_data["entrepot"].id,
        quantite=100
    )
    db.add(stock)
    db.commit()

    # Mock IoT service
    mock_iot = AsyncMock()
    mock_iot.get_sensor.return_value = True
    service.iot_service = mock_iot

    # Lier des capteurs
    sensor_ids = ["sensor1", "sensor2"]
    result = await service.link_sensors(str(stock.id), sensor_ids)
    assert result.capteurs_id == sensor_ids

    # Test avec capteur inexistant
    mock_iot.get_sensor.return_value = None
    with pytest.raises(HTTPException, match="Capteur .* non trouvé"):
        await service.link_sensors(str(stock.id), ["invalid_sensor"])

@pytest.mark.asyncio
async def test_verify_quality_control(db, test_user, test_data):
    """Test de vérification du contrôle qualité"""
    service = InventoryService(db)
    
    # Créer un stock
    stock = Stock(
        produit_id=test_data["produit"].id,
        entrepot_id=test_data["entrepot"].id,
        quantite=100
    )
    db.add(stock)
    db.commit()

    # Test contrôle conforme
    controle_ok = ControleQualite(
        conforme=True,
        date_controle=datetime.now(),
        controleur="John Doe",
        resultats={"test1": "OK", "test2": "OK"}
    )
    await service._verify_quality_control(stock, controle_ok)

    # Test contrôle non conforme
    controle_nok = ControleQualite(
        conforme=False,
        date_controle=datetime.now(),
        controleur="John Doe",
        resultats={"test1": "NOK"},
        actions_requises=["Nettoyage requis"]
    )
    with pytest.raises(HTTPException, match="Contrôle qualité non conforme"):
        await service._verify_quality_control(stock, controle_nok)
