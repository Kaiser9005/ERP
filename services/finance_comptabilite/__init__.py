"""
Service d'intégration Finance-Comptabilité
Basé sur les analyses des ERP Odoo et Dolibarr et enrichi des meilleures pratiques
"""

from sqlalchemy.orm import Session
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, date, timedelta
from decimal import Decimal
import os
import json
from sqlalchemy import and_, or_, func, update

from models.comptabilite import (
    CompteComptable, 
    EcritureComptable, 
    TypeCompte,
    JournalComptable,
    StatutEcriture,
    TypeJournal,
    ExerciceComptable
)
from models.production import Parcelle, CycleCulture
from models.iot_sensor import IoTSensor, SensorReading
from models.finance import Transaction, Budget, CategorieTransaction

from services.weather_service import WeatherService
from services.iot_service import IoTService
from services.cache_service import CacheService
from services.storage_service import StorageService

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
        
        # Initialisation des sous-services
        from .analyse import AnalyseFinanceCompta
        from .couts import GestionCouts
        from .meteo import GestionMeteo
        from .iot import GestionIoT
        from .cloture import GestionCloture
        
        self.analyse = AnalyseFinanceCompta(db)
        self.couts = GestionCouts(db)
        self.meteo = GestionMeteo(db)
        self.iot = GestionIoT(db)
        self.cloture = GestionCloture(db)

    # Méthodes déléguées au service d'analyse
    async def get_analyse_parcelle(self, *args, **kwargs):
        return await self.analyse.get_analyse_parcelle(*args, **kwargs)

    async def calculer_rentabilite_parcelle(self, *args, **kwargs):
        return await self.analyse._calculer_rentabilite_parcelle(*args, **kwargs)

    async def generer_recommendations(self, *args, **kwargs):
        return await self.analyse._generer_recommendations(*args, **kwargs)

    # Méthodes déléguées au service de coûts
    async def get_couts_parcelle(self, *args, **kwargs):
        return await self.couts._get_couts_parcelle(*args, **kwargs)

    async def get_compte_charge(self, *args, **kwargs):
        return await self.couts._get_compte_charge(*args, **kwargs)

    async def get_compte_produit(self, *args, **kwargs):
        return await self.couts._get_compte_produit(*args, **kwargs)

    # Méthodes déléguées au service météo
    async def get_meteo_impact(self, *args, **kwargs):
        return await self.meteo._get_meteo_impact(*args, **kwargs)

    async def calculer_provision_meteo(self, *args, **kwargs):
        return await self.meteo._calculer_provision_meteo(*args, **kwargs)

    # Méthodes déléguées au service IoT
    async def get_iot_analysis(self, *args, **kwargs):
        return await self.iot._get_iot_analysis(*args, **kwargs)

    async def analyser_tendance(self, *args, **kwargs):
        return await self.iot._analyser_tendance(*args, **kwargs)

    async def generer_alertes_iot(self, *args, **kwargs):
        return await self.iot._generer_alertes_iot(*args, **kwargs)

    # Méthodes déléguées au service de clôture
    async def executer_cloture_mensuelle(self, *args, **kwargs):
        return await self.cloture.executer_cloture_mensuelle(*args, **kwargs)

    async def verifier_conditions_cloture(self, *args, **kwargs):
        return await self.cloture._verifier_conditions_cloture(*args, **kwargs)

    async def valider_ecritures_attente(self, *args, **kwargs):
        return await self.cloture._valider_ecritures_attente(*args, **kwargs)
