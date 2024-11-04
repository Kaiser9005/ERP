from sqlalchemy.orm import Session
from typing import Dict, Any
from datetime import datetime, timedelta
from models.inventory import Produit, MouvementStock, Stock
from schemas.inventory import MouvementStockCreate
from sqlalchemy import func

class InventoryService:
    def __init__(self, db: Session):
        self.db = db

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
            "alerts": alerts_count,
            "alertsVariation": {
                "value": 0,
                "type": "increase"
            },
            "movements": movements_count,
            "movementsVariation": {
                "value": 0,
                "type": "increase"
            }
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
            self._handle_entree(mouvement)
        elif mouvement.type_mouvement == 'SORTIE':
            self._handle_sortie(mouvement)
        elif mouvement.type_mouvement == 'TRANSFERT':
            self._handle_transfert(mouvement)

        self.db.commit()
        self.db.refresh(db_mouvement)
        return db_mouvement

    def _handle_entree(self, mouvement: MouvementStockCreate):
        """Gère une entrée de stock"""
        stock = self._get_or_create_stock(
            mouvement.produit_id,
            mouvement.entrepot_destination_id
        )
        stock.quantite += mouvement.quantite
        if mouvement.cout_unitaire:
            stock.valeur_unitaire = mouvement.cout_unitaire

    def _handle_sortie(self, mouvement: MouvementStockCreate):
        """Gère une sortie de stock"""
        stock = self._get_stock(
            mouvement.produit_id,
            mouvement.entrepot_source_id
        )
        if stock.quantite < mouvement.quantite:
            raise ValueError("Stock insuffisant")
        stock.quantite -= mouvement.quantite

    def _handle_transfert(self, mouvement: MouvementStockCreate):
        """Gère un transfert de stock"""
        self._handle_sortie(mouvement)
        self._handle_entree(mouvement)

    def _get_stock(self, produit_id: str, entrepot_id: str) -> Stock:
        """Récupère un stock existant"""
        stock = self.db.query(Stock).filter(
            Stock.produit_id == produit_id,
            Stock.entrepot_id == entrepot_id
        ).first()
        if not stock:
            raise ValueError("Stock non trouvé")
        return stock

    def _get_or_create_stock(self, produit_id: str, entrepot_id: str) -> Stock:
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