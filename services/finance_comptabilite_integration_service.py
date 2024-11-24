"""
Service d'intégration Finance-Comptabilité
Basé sur les analyses des ERP Odoo et Dolibarr et enrichi des meilleures pratiques
"""

from sqlalchemy.orm import Session
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, date, timedelta
from decimal import Decimal
from sqlalchemy import and_, or_, func, update
from models.comptabilite import (
    CompteComptable, 
    EcritureComptable, 
    TypeCompte,
    JournalComptable,
    StatutEcriture,
    TypeJournal
)
from models.production import Parcelle, CycleCulture
from models.iot_sensor import IoTSensor, SensorData
from services.weather_service import WeatherService
from services.iot_service import IoTService
from services.cache_service import CacheService
from services.storage_service import StorageService
from core.security import Permission, require_permissions
import asyncio
from functools import lru_cache

class ValidationResult:
    """Résultat de validation"""
    def __init__(
        self,
        is_valid: bool,
        errors: List[str] = None,
        warnings: List[str] = None
    ):
        self.is_valid = is_valid
        self.errors = errors or []
        self.warnings = warnings or []

class MeteoImpact:
    """Impact météorologique"""
    def __init__(
        self,
        score: float,
        facteurs: List[str],
        couts_additionnels: Dict[str, float],
        risques: List[str],
        opportunites: List[str]
    ):
        self.score = score
        self.facteurs = facteurs
        self.couts_additionnels = couts_additionnels
        self.risques = risques
        self.opportunites = opportunites

class AnalyticData:
    """Données analytiques"""
    def __init__(
        self,
        charges_directes: float,
        charges_indirectes: float,
        produits: float,
        marge: float,
        axes: Dict[str, Any]
    ):
        self.charges_directes = charges_directes
        self.charges_indirectes = charges_indirectes
        self.produits = produits
        self.marge = marge
        self.axes = axes

class CloturePeriode:
    """Données de clôture"""
    def __init__(
        self,
        periode: str,
        statut: str,
        totaux: Dict[str, float],
        etats: Dict[str, str]
    ):
        self.periode = periode
        self.statut = statut
        self.totaux = totaux
        self.etats = etats

class FinanceComptabiliteIntegrationService:
    """Service d'intégration entre les modules Finance et Comptabilité"""
    
    def __init__(self, db: Session):
        self.db = db
        self.weather_service = WeatherService(db)
        self.iot_service = IoTService(db)
        self.cache = CacheService()
        self.storage = StorageService()
        
    async def get_analyse_parcelle(
        self,
        parcelle_id: str,
        date_debut: Optional[date] = None,
        date_fin: Optional[date] = None
    ) -> Dict[str, Any]:
        """Analyse financière détaillée d'une parcelle"""
        # Récupération des données de base
        parcelle = self.db.query(Parcelle).get(parcelle_id)
        if not parcelle:
            raise ValueError("Parcelle non trouvée")
            
        # Période par défaut: 30 derniers jours
        if not date_debut:
            date_fin = date.today()
            date_debut = date_fin - timedelta(days=30)
            
        # Analyse des coûts
        couts = await self._get_couts_parcelle(parcelle_id, date_debut, date_fin)
        
        # Données météo et IoT
        meteo_data = await self._get_meteo_impact(parcelle_id, date_debut, date_fin)
        iot_data = await self._get_iot_analysis(parcelle_id, date_debut, date_fin)
        
        # Calcul rentabilité
        rentabilite = await self._calculer_rentabilite_parcelle(
            parcelle_id, 
            couts,
            meteo_data,
            date_debut,
            date_fin
        )
        
        return {
            "parcelle": {
                "id": parcelle.id,
                "code": parcelle.code,
                "surface": parcelle.surface,
                "culture": parcelle.culture_actuelle
            },
            "periode": {
                "debut": date_debut.isoformat(),
                "fin": date_fin.isoformat()
            },
            "couts": couts,
            "meteo_impact": meteo_data,
            "iot_analysis": iot_data,
            "rentabilite": rentabilite,
            "recommendations": await self._generer_recommendations(
                parcelle_id,
                couts,
                meteo_data,
                iot_data
            )
        }
