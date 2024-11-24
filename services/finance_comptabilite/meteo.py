"""
Module d'intégration des impacts météorologiques sur la finance et la comptabilité
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, date, timedelta
from decimal import Decimal
from sqlalchemy import func, and_, or_
from sqlalchemy.orm import Session

from models.comptabilite import (
    CompteComptable, 
    EcritureComptable,
    TypeCompte,
    JournalComptable
)
from models.finance import Transaction, Budget
from models.production import Parcelle
from services.weather_service import WeatherService

class GestionMeteo:
    """Gestion des impacts météorologiques sur la finance et la comptabilité"""
    
    def __init__(self, db: Session):
        self.db = db
        self.weather_service = WeatherService(db)

    async def _get_meteo_impact(
        self,
        parcelle_id: str,
        date_debut: date,
        date_fin: date
    ) -> Dict[str, Any]:
        """Analyse détaillée de l'impact météo"""
        # Récupération données météo
        meteo_data = await self.weather_service.get_period_stats(date_debut, date_fin)
        
        impact = {
            "score": 0,
            "facteurs": [],
            "couts_additionnels": {},
            "risques": [],
            "opportunites": [],
            "provisions_suggeres": {}
        }
        
        # Analyse précipitations
        if meteo_data.get("precipitation", 0) > 200:
            impact["score"] += 30
            impact["facteurs"].append("Fortes précipitations")
            impact["couts_additionnels"]["IRRIGATION"] = "Réduction possible"
            impact["risques"].append("Risque d'érosion accru")
            impact["provisions_suggeres"]["EROSION"] = self._calculer_provision_erosion(
                meteo_data["precipitation"]
            )
            
        elif meteo_data.get("precipitation", 0) < 50:
            impact["score"] += 25
            impact["facteurs"].append("Faibles précipitations")
            impact["couts_additionnels"]["IRRIGATION"] = "Augmentation nécessaire"
            impact["provisions_suggeres"]["IRRIGATION"] = self._calculer_provision_irrigation(
                meteo_data["precipitation"]
            )
            
        # Analyse température
        temp_moy = meteo_data.get("temperature_avg", 25)
        if temp_moy > 30:
            impact["score"] += 20
            impact["facteurs"].append("Températures élevées")
            impact["couts_additionnels"]["MAINTENANCE"] = "Augmentation probable"
            impact["risques"].append("Stress thermique des cultures")
            impact["provisions_suggeres"]["MAINTENANCE"] = self._calculer_provision_maintenance(
                temp_moy
            )
            
        elif temp_moy < 15:
            impact["score"] += 15
            impact["facteurs"].append("Températures basses")
            impact["risques"].append("Ralentissement de la croissance")
            impact["provisions_suggeres"]["PROTECTION"] = self._calculer_provision_protection(
                temp_moy
            )
            
        # Analyse humidité
        if meteo_data.get("humidity_avg", 60) > 80:
            impact["score"] += 15
            impact["facteurs"].append("Forte humidité")
            impact["risques"].append("Risque accru de maladies")
            impact["couts_additionnels"]["TRAITEMENTS"] = "Augmentation probable"
            impact["provisions_suggeres"]["TRAITEMENTS"] = self._calculer_provision_traitements(
                meteo_data["humidity_avg"]
            )
            
        return impact

    async def _calculer_provision_meteo(
        self,
        impact_meteo: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Calcule les provisions nécessaires basées sur l'impact météo"""
        provisions = {}
        
        for categorie, montant in impact_meteo["provisions_suggeres"].items():
            compte = await self._get_compte_provision_meteo(categorie)
            compte_charge = await self._get_compte_charge_meteo(categorie)
            
            provisions[categorie] = {
                "montant": montant,
                "compte_provision": compte,
                "compte_charge": compte_charge,
                "justification": f"Provision pour risques météo - {categorie}",
                "impact_score": impact_meteo["score"]
            }
            
        return provisions

    def _calculer_provision_erosion(self, precipitation: float) -> float:
        """Calcule la provision pour risque d'érosion"""
        # Base de calcul : 100€ par mm au-dessus du seuil de 200mm
        if precipitation <= 200:
            return 0
        return (precipitation - 200) * 100

    def _calculer_provision_irrigation(self, precipitation: float) -> float:
        """Calcule la provision pour besoins d'irrigation"""
        # Base de calcul : 150€ par mm en dessous du seuil de 50mm
        if precipitation >= 50:
            return 0
        return (50 - precipitation) * 150

    def _calculer_provision_maintenance(self, temperature: float) -> float:
        """Calcule la provision pour maintenance supplémentaire"""
        # Base de calcul : 200€ par degré au-dessus de 30°C
        if temperature <= 30:
            return 0
        return (temperature - 30) * 200

    def _calculer_provision_protection(self, temperature: float) -> float:
        """Calcule la provision pour protection contre le froid"""
        # Base de calcul : 250€ par degré en dessous de 15°C
        if temperature >= 15:
            return 0
        return (15 - temperature) * 250

    def _calculer_provision_traitements(self, humidity: float) -> float:
        """Calcule la provision pour traitements phytosanitaires"""
        # Base de calcul : 180€ par point d'humidité au-dessus de 80%
        if humidity <= 80:
            return 0
        return (humidity - 80) * 180

    async def _get_compte_provision_meteo(self, categorie: str) -> str:
        """Récupère le compte de provision météo approprié"""
        # Mapping des catégories vers les comptes de provision
        mapping_comptes = {
            "EROSION": "1511",      # Provisions pour risques climatiques
            "IRRIGATION": "1512",    # Provisions pour risques d'irrigation
            "MAINTENANCE": "1513",   # Provisions pour risques de maintenance
            "PROTECTION": "1514",    # Provisions pour risques de protection
            "TRAITEMENTS": "1515"    # Provisions pour risques de traitements
        }
        
        compte_numero = mapping_comptes.get(categorie, "1518")  # Compte par défaut
        
        compte = self.db.query(CompteComptable).filter(
            CompteComptable.numero == compte_numero
        ).first()
        
        if not compte:
            raise ValueError(f"Compte de provision {compte_numero} non trouvé")
            
        return compte.id

    async def _get_compte_charge_meteo(self, categorie: str) -> str:
        """Récupère le compte de charge météo approprié"""
        # Mapping des catégories vers les comptes de charge
        mapping_comptes = {
            "EROSION": "6815",      # Dotations aux provisions pour risques climatiques
            "IRRIGATION": "6816",    # Dotations aux provisions pour risques d'irrigation
            "MAINTENANCE": "6817",   # Dotations aux provisions pour risques de maintenance
            "PROTECTION": "6818",    # Dotations aux provisions pour risques de protection
            "TRAITEMENTS": "6819"    # Dotations aux provisions pour risques de traitements
        }
        
        compte_numero = mapping_comptes.get(categorie, "6815")  # Compte par défaut
        
        compte = self.db.query(CompteComptable).filter(
            CompteComptable.numero == compte_numero
        ).first()
        
        if not compte:
            raise ValueError(f"Compte de charge {compte_numero} non trouvé")
            
        return compte.id
