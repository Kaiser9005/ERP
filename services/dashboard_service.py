from sqlalchemy.orm import Session
from typing import Dict, Any, List
from datetime import datetime, timedelta
from models.production import Recolte, Parcelle
from models.inventory import Stock, MouvementStock
from models.hr import Employe
from models.finance import Transaction
from sqlalchemy import func
import aiohttp

class DashboardService:
    def __init__(self, db: Session):
        self.db = db

    async def get_stats(self) -> Dict[str, Any]:
        """Récupère toutes les statistiques pour le tableau de bord"""
        return {
            "production": await self._get_production_stats(),
            "inventory": await self._get_inventory_stats(),
            "finance": await self._get_finance_stats(),
            "hr": await self._get_hr_stats()
        }

    async def _get_production_stats(self) -> Dict[str, Any]:
        """Calcule les statistiques de production"""
        now = datetime.utcnow()
        current_month = now.strftime("%Y-%m")
        last_month = (now - timedelta(days=30)).strftime("%Y-%m")

        current_production = self.db.query(
            func.sum(Recolte.quantite_kg)
        ).filter(
            func.to_char(Recolte.date_recolte, 'YYYY-MM') == current_month
        ).scalar() or 0

        previous_production = self.db.query(
            func.sum(Recolte.quantite_kg)
        ).filter(
            func.to_char(Recolte.date_recolte, 'YYYY-MM') == last_month
        ).scalar() or 0

        return {
            "total": current_production / 1000,  # Conversion en tonnes
            "variation": self._calculate_variation(current_production, previous_production),
            "parcelles_actives": self.db.query(Parcelle).filter(
                Parcelle.statut == "ACTIVE"
            ).count()
        }

    async def _get_inventory_stats(self) -> Dict[str, Any]:
        """Calcule les statistiques d'inventaire"""
        total_value = self.db.query(
            func.sum(Stock.quantite * Stock.valeur_unitaire)
        ).scalar() or 0

        alerts_count = self.db.query(Stock).join(Stock.produit).filter(
            Stock.quantite <= Stock.produit.seuil_alerte
        ).count()

        return {
            "valeur_totale": total_value,
            "alertes": alerts_count,
            "mouvements_jour": self.db.query(MouvementStock).filter(
                func.date(MouvementStock.date_mouvement) == datetime.utcnow().date()
            ).count()
        }

    async def _get_finance_stats(self) -> Dict[str, Any]:
        """Calcule les statistiques financières"""
        now = datetime.utcnow()
        current_month = now.strftime("%Y-%m")

        recettes = self.db.query(
            func.sum(Transaction.montant)
        ).filter(
            Transaction.type_transaction == "RECETTE",
            Transaction.statut == "VALIDEE",
            func.to_char(Transaction.date_transaction, 'YYYY-MM') == current_month
        ).scalar() or 0

        depenses = self.db.query(
            func.sum(Transaction.montant)
        ).filter(
            Transaction.type_transaction == "DEPENSE",
            Transaction.statut == "VALIDEE",
            func.to_char(Transaction.date_transaction, 'YYYY-MM') == current_month
        ).scalar() or 0

        return {
            "recettes": recettes,
            "depenses": depenses,
            "solde": recettes - depenses
        }

    async def _get_hr_stats(self) -> Dict[str, Any]:
        """Calcule les statistiques RH"""
        return {
            "effectif_total": self.db.query(Employe).filter(
                Employe.statut == "ACTIF"
            ).count(),
            "en_conge": self.db.query(Employe).filter(
                Employe.statut == "CONGE"
            ).count()
        }

    async def get_recent_activities(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Récupère les activités récentes tous types confondus"""
        activities = []

        # Récoltes récentes
        recoltes = self.db.query(Recolte).order_by(
            Recolte.date_recolte.desc()
        ).limit(limit).all()

        for recolte in recoltes:
            activities.append({
                "type": "PRODUCTION",
                "titre": f"Récolte - {recolte.parcelle.code}",
                "description": f"Récolte de {recolte.quantite_kg} kg",
                "date": recolte.date_recolte.isoformat()
            })

        # Mouvements de stock récents
        mouvements = self.db.query(MouvementStock).order_by(
            MouvementStock.date_mouvement.desc()
        ).limit(limit).all()

        for mouvement in mouvements:
            activities.append({
                "type": "INVENTORY",
                "titre": f"{mouvement.type_mouvement} - {mouvement.produit.nom}",
                "description": f"Quantité: {mouvement.quantite} {mouvement.produit.unite_mesure}",
                "date": mouvement.date_mouvement.isoformat()
            })

        # Trier par date et limiter
        activities.sort(key=lambda x: x["date"], reverse=True)
        return activities[:limit]

    async def get_weather_data(self) -> Dict[str, Any]:
        """Récupère les données météorologiques pour le site"""
        # Coordonnées de FOFAL
        lat = 4.0511
        lon = 9.7679
        
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://api.openweathermap.org/data/2.5/weather",
                params={
                    "lat": lat,
                    "lon": lon,
                    "units": "metric",
                    "appid": "YOUR_API_KEY"  # À configurer
                }
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "temperature": round(data["main"]["temp"], 1),
                        "humidite": data["main"]["humidity"],
                        "vent": round(data["wind"]["speed"] * 3.6, 1),  # Conversion en km/h
                        "description": data["weather"][0]["description"]
                    }
                return {
                    "temperature": 25.0,
                    "humidite": 80,
                    "vent": 5.0,
                    "description": "Données non disponibles"
                }

    def _calculate_variation(
        self,
        current_value: float,
        previous_value: float
    ) -> Dict[str, Any]:
        """Calcule la variation entre deux valeurs"""
        if previous_value == 0:
            return {
                "value": 0,
                "type": "increase"
            }

        variation = ((current_value - previous_value) / previous_value) * 100
        return {
            "value": abs(round(variation, 1)),
            "type": "increase" if variation >= 0 else "decrease"
        }