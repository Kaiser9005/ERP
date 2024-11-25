from sqlalchemy.orm import Session
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from models.inventory import Produit, MouvementStock, Stock
from models.iot_sensor import IoTSensor, SensorReading
from schemas.inventaire import (
    MouvementStockCreate, ConditionsActuelles,
    ControleQualite, Certification
)
from sqlalchemy import func
from fastapi import HTTPException

class InventoryService:
    def __init__(self, db: Session, iot_service=None):
        self.db = db
        self.iot_service = iot_service

    async def get_stats(self) -> Dict[str, Any]:
        """Calcule les statistiques d'inventaire"""
        now = datetime.utcnow()
        last_month = now - timedelta(days=30)

        # Valeur totale du stock
        total_value = self.db.query(
            func.sum(Stock.quantite * Stock.valeur_unitaire)
        ).scalar() or 0

        # Nombre de mouvements sur les 30 derniers jours
        movements_count = self.db.query(MouvementStock).filter(
            MouvementStock.date_mouvement >= last_month
        ).count()

        # Nombre de produits sous le seuil d'alerte
        alerts_count = self.db.query(Stock).join(Produit).filter(
            Stock.quantite <= Produit.seuil_alerte
        ).count()

        # Taux de rotation du stock
        total_stock = self.db.query(func.sum(Stock.quantite)).scalar() or 1
        total_output = self.db.query(func.sum(MouvementStock.quantite)).filter(
            MouvementStock.type_mouvement == 'SORTIE',
            MouvementStock.date_mouvement >= last_month
        ).scalar() or 0

        turnover_rate = (total_output / total_stock) * 30  # En jours

        # Alertes conditions stockage
        storage_alerts = await self._check_storage_conditions()

        return {
            "totalValue": total_value,
            "valueVariation": {
                "value": 0,  # À implémenter: comparaison avec période précédente
                "type": "increase"
            },
            "turnoverRate": turnover_rate,
            "turnoverVariation": {
                "value": 0,
                "type": "increase"
            },
            "alerts": alerts_count + len(storage_alerts),
            "alertsVariation": {
                "value": 0,
                "type": "increase"
            },
            "movements": movements_count,
            "movementsVariation": {
                "value": 0,
                "type": "increase"
            },
            "storage_alerts": storage_alerts
        }

    async def create_mouvement(
        self,
        mouvement: MouvementStockCreate,
        user_id: str
    ) -> MouvementStock:
        """Crée un mouvement de stock et met à jour les stocks"""
        # Créer le mouvement
        db_mouvement = MouvementStock(
            **mouvement.dict(),
            responsable_id=user_id
        )
        self.db.add(db_mouvement)

        # Mettre à jour les stocks
        if mouvement.type_mouvement == 'ENTREE':
            await self._handle_entree(mouvement)
        elif mouvement.type_mouvement == 'SORTIE':
            await self._handle_sortie(mouvement)
        elif mouvement.type_mouvement == 'TRANSFERT':
            await self._handle_transfert(mouvement)

        self.db.commit()
        self.db.refresh(db_mouvement)
        return db_mouvement

    async def _handle_entree(self, mouvement: MouvementStockCreate):
        """Gère une entrée de stock"""
        stock = await self._get_or_create_stock(
            mouvement.produit_id,
            mouvement.entrepot_destination_id
        )
        stock.quantite += mouvement.quantite
        if mouvement.cout_unitaire:
            stock.valeur_unitaire = mouvement.cout_unitaire

        # Vérifier les conditions de stockage
        if mouvement.controle_qualite:
            stock.controle_qualite = mouvement.controle_qualite.dict()

        # Mettre à jour la traçabilité
        if mouvement.conditions_transport:
            await self._update_stock_conditions(stock, mouvement.conditions_transport)

    async def _handle_sortie(self, mouvement: MouvementStockCreate):
        """Gère une sortie de stock"""
        stock = await self._get_stock(
            mouvement.produit_id,
            mouvement.entrepot_source_id
        )
        if stock.quantite < mouvement.quantite:
            raise ValueError("Stock insuffisant")
        stock.quantite -= mouvement.quantite

        # Vérifier les conditions avant sortie
        if mouvement.controle_qualite:
            await self._verify_quality_control(stock, mouvement.controle_qualite)

    async def _handle_transfert(self, mouvement: MouvementStockCreate):
        """Gère un transfert de stock"""
        await self._handle_sortie(mouvement)
        await self._handle_entree(mouvement)

    async def _get_stock(self, produit_id: str, entrepot_id: str) -> Stock:
        """Récupère un stock existant"""
        stock = self.db.query(Stock).filter(
            Stock.produit_id == produit_id,
            Stock.entrepot_id == entrepot_id
        ).first()
        if not stock:
            raise ValueError("Stock non trouvé")
        return stock

    async def _get_or_create_stock(self, produit_id: str, entrepot_id: str) -> Stock:
        """Récupère ou crée un stock"""
        stock = self.db.query(Stock).filter(
            Stock.produit_id == produit_id,
            Stock.entrepot_id == entrepot_id
        ).first()
        
        if not stock:
            stock = Stock(
                produit_id=produit_id,
                entrepot_id=entrepot_id,
                quantite=0
            )
            self.db.add(stock)
        
        return stock

    async def _check_storage_conditions(self) -> List[Dict[str, Any]]:
        """Vérifie les conditions de stockage pour tous les stocks"""
        alerts = []
        stocks = self.db.query(Stock).join(Produit).all()

        for stock in stocks:
            if not stock.capteurs_id or not self.iot_service:
                continue

            conditions = await self._get_current_conditions(stock)
            if not conditions:
                continue

            produit = stock.produit
            if not produit.conditions_stockage:
                continue

            required = produit.conditions_stockage
            current = conditions.dict()

            if current['temperature'] < required['temperature_min']:
                alerts.append({
                    "stock_id": stock.id,
                    "type": "temperature",
                    "message": f"Température trop basse: {current['temperature']}°C"
                })
            elif current['temperature'] > required['temperature_max']:
                alerts.append({
                    "stock_id": stock.id,
                    "type": "temperature",
                    "message": f"Température trop élevée: {current['temperature']}°C"
                })

            if current['humidite'] < required['humidite_min']:
                alerts.append({
                    "stock_id": stock.id,
                    "type": "humidite",
                    "message": f"Humidité trop basse: {current['humidite']}%"
                })
            elif current['humidite'] > required['humidite_max']:
                alerts.append({
                    "stock_id": stock.id,
                    "type": "humidite",
                    "message": f"Humidité trop élevée: {current['humidite']}%"
                })

        return alerts

    async def _get_current_conditions(self, stock: Stock) -> Optional[ConditionsActuelles]:
        """Récupère les conditions actuelles d'un stock via les capteurs IoT"""
        if not self.iot_service or not stock.capteurs_id:
            return None

        conditions = {
            "temperature": 0,
            "humidite": 0,
            "luminosite": None,
            "qualite_air": None,
            "derniere_maj": datetime.utcnow()
        }

        # Récupérer les dernières lectures des capteurs
        for sensor_id in stock.capteurs_id:
            sensor = await self.iot_service.get_sensor(sensor_id)
            if not sensor:
                continue

            readings = await self.iot_service.get_sensor_readings(
                sensor_id,
                limit=1
            )
            if not readings:
                continue

            reading = readings[0]
            if sensor.type == "TEMPERATURE":
                conditions["temperature"] = reading.valeur
            elif sensor.type == "HUMIDITE":
                conditions["humidite"] = reading.valeur
            elif sensor.type == "LUMINOSITE":
                conditions["luminosite"] = reading.valeur
            elif sensor.type == "QUALITE_AIR":
                conditions["qualite_air"] = reading.valeur

        return ConditionsActuelles(**conditions)

    async def _verify_quality_control(
        self,
        stock: Stock,
        controle: ControleQualite
    ) -> None:
        """Vérifie le contrôle qualité"""
        if not controle.conforme:
            raise HTTPException(
                status_code=400,
                detail=f"Contrôle qualité non conforme: {controle.actions_requises}"
            )

    async def _update_stock_conditions(
        self,
        stock: Stock,
        conditions: Dict[str, Any]
    ) -> None:
        """Met à jour les conditions de stockage"""
        stock.conditions_actuelles = conditions
        stock.date_derniere_maj = datetime.utcnow()

    async def add_certification(
        self,
        stock_id: str,
        certification: Certification
    ) -> Stock:
        """Ajoute une certification à un stock"""
        stock = self.db.query(Stock).filter(Stock.id == stock_id).first()
        if not stock:
            raise HTTPException(status_code=404, detail="Stock non trouvé")

        if not stock.certifications:
            stock.certifications = []

        stock.certifications.append(certification.dict())
        self.db.commit()
        self.db.refresh(stock)
        return stock

    async def link_sensors(
        self,
        stock_id: str,
        sensor_ids: List[str]
    ) -> Stock:
        """Lie des capteurs IoT à un stock"""
        stock = self.db.query(Stock).filter(Stock.id == stock_id).first()
        if not stock:
            raise HTTPException(status_code=404, detail="Stock non trouvé")

        # Vérifier que les capteurs existent
        if self.iot_service:
            for sensor_id in sensor_ids:
                sensor = await self.iot_service.get_sensor(sensor_id)
                if not sensor:
                    raise HTTPException(
                        status_code=404,
                        detail=f"Capteur {sensor_id} non trouvé"
                    )

        stock.capteurs_id = sensor_ids
        self.db.commit()
        self.db.refresh(stock)
        return stock
