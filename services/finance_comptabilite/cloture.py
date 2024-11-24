"""
Module de gestion des processus de clôture comptable et financière avec ML
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
    JournalComptable,
    ExerciceComptable,
    StatutEcriture
)
from models.finance import Transaction, Budget
from models.production import Parcelle
from services.finance_comptabilite.analyse import AnalyseFinanceCompta
from services.cache_service import CacheService
import os
import json

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

class GestionCloture:
    """Gestion des processus de clôture comptable et financière avec ML"""
    
    def __init__(self, db: Session):
        self.db = db
        self.analyse = AnalyseFinanceCompta(db)
        self.cache = CacheService()

    async def executer_cloture_mensuelle(
        self,
        periode: str,
        utilisateur_id: str
    ) -> Dict[str, Any]:
        """Exécute le processus de clôture mensuelle avec ML"""
        # Cache key
        cache_key = f"cloture_ml_{periode}"
        cached = await self.cache.get(cache_key)
        if cached:
            return cached
            
        # Vérification des conditions préalables
        validation = await self._verifier_conditions_cloture(periode)
        if not validation.is_valid:
            raise ValueError(f"Conditions de clôture non remplies: {validation.errors}")
            
        # Analyse ML
        analyse_ml = await self.analyse.get_analyse_parcelle(
            parcelle_id=None,  # Analyse globale
            date_debut=datetime.strptime(periode, "%Y-%m").date(),
            date_fin=datetime.strptime(periode, "%Y-%m").date() + timedelta(days=30),
            include_predictions=True
        )
        
        # Optimisation ML
        optimization = await self.analyse.optimize_costs(
            target_date=datetime.strptime(periode, "%Y-%m").date()
        )
            
        # Validation des écritures en attente
        ecritures_validees = await self._valider_ecritures_attente(
            periode,
            utilisateur_id
        )
        
        # Génération des écritures de clôture avec ML
        ecritures_cloture = await self._generer_ecritures_cloture_ml(
            periode,
            analyse_ml,
            optimization
        )
        
        # Calcul des totaux de la période
        totaux = await self._calculer_totaux_periode(periode)
        
        # Gel des écritures de la période
        await self._geler_ecritures(periode)
        
        # Génération des états de clôture avec ML
        etats = await self._generer_etats_cloture_ml(
            periode,
            totaux,
            ecritures_validees,
            ecritures_cloture,
            analyse_ml,
            optimization
        )
        
        # Archivage des documents
        await self._archiver_documents(periode, etats)
        
        resultat = {
            "periode": periode,
            "statut": "CLOTURE",
            "date_cloture": datetime.utcnow().isoformat(),
            "utilisateur_id": utilisateur_id,
            "totaux": totaux,
            "etats": etats,
            "ecritures_validees": len(ecritures_validees),
            "ecritures_cloture": len(ecritures_cloture),
            "ml_analysis": analyse_ml["ml_analysis"],
            "optimization": optimization,
            "recommendations": await self._generate_cloture_recommendations(
                totaux,
                analyse_ml,
                optimization
            )
        }
        
        # Cache result
        await self.cache.set(cache_key, resultat, expire=3600)
        return resultat

    async def _verifier_conditions_cloture(self, periode: str) -> ValidationResult:
        """Vérifie les conditions nécessaires à la clôture avec ML"""
        errors = []
        warnings = []
        
        # Vérification de l'équilibre des comptes
        balance = await self._verifier_equilibre_comptes(periode)
        if not balance["equilibre"]:
            errors.append(
                f"Comptes non équilibrés: différence de {balance['difference']}"
            )
            
        # Vérification des écritures en attente
        ecritures_attente = await self._compter_ecritures_attente(periode)
        if ecritures_attente > 0:
            errors.append(
                f"{ecritures_attente} écritures en attente de validation"
            )
            
        # Vérification des rapprochements bancaires
        rapprochements = await self._verifier_rapprochements(periode)
        if not rapprochements["complet"]:
            warnings.append(
                f"Rapprochements bancaires incomplets: {rapprochements['manquants']} relevés manquants"
            )
            
        # Vérification des provisions obligatoires avec ML
        provisions = await self._verifier_provisions_obligatoires_ml(periode)
        if not provisions["complet"]:
            errors.append(
                f"Provisions obligatoires manquantes: {provisions['manquantes']}"
            )
            
        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )

    async def _valider_ecritures_attente(
        self,
        periode: str,
        utilisateur_id: str
    ) -> List[EcritureComptable]:
        """Valide les écritures en attente de la période"""
        ecritures = self.db.query(EcritureComptable).filter(
            EcritureComptable.periode == periode,
            EcritureComptable.statut == StatutEcriture.BROUILLON
        ).all()
        
        for ecriture in ecritures:
            ecriture.statut = StatutEcriture.VALIDEE
            ecriture.validee_par_id = utilisateur_id
            ecriture.date_validation = datetime.utcnow()
            
        self.db.commit()
        return ecritures

    async def _generer_ecritures_cloture_ml(
        self,
        periode: str,
        analyse_ml: Dict[str, Any],
        optimization: Dict[str, Any]
    ) -> List[EcritureComptable]:
        """Génère les écritures de clôture avec ML"""
        ecritures_cloture = []
        
        # Écritures de régularisation des charges avec ML
        regularisations = await self._calculer_regularisations_charges_ml(
            periode,
            analyse_ml,
            optimization
        )
        ecritures_cloture.extend(regularisations)
        
        # Écritures de variation des stocks avec ML
        variations = await self._calculer_variations_stocks_ml(
            periode,
            analyse_ml
        )
        ecritures_cloture.extend(variations)
        
        # Écritures de provisions avec ML
        provisions = await self._calculer_provisions_ml(
            periode,
            analyse_ml,
            optimization
        )
        ecritures_cloture.extend(provisions)
        
        # Écritures d'amortissements avec ML
        amortissements = await self._calculer_amortissements_ml(
            periode,
            analyse_ml
        )
        ecritures_cloture.extend(amortissements)
        
        # Sauvegarde des écritures
        for ecriture in ecritures_cloture:
            self.db.add(ecriture)
            
        self.db.commit()
        return ecritures_cloture

    async def _calculer_regularisations_charges_ml(
        self,
        periode: str,
        analyse_ml: Dict[str, Any],
        optimization: Dict[str, Any]
    ) -> List[EcritureComptable]:
        """Calcule les régularisations de charges avec ML"""
        regularisations = []
        
        # Récupération des charges à régulariser
        charges = self.db.query(EcritureComptable).filter(
            EcritureComptable.periode == periode,
            EcritureComptable.type_compte == TypeCompte.CHARGE
        ).all()
        
        # Ajustement ML des régularisations
        if "charge_adjustments" in analyse_ml["ml_analysis"]:
            adjustments = analyse_ml["ml_analysis"]["charge_adjustments"]
            for charge in charges:
                if charge.categorie in adjustments:
                    adj_data = adjustments[charge.categorie]
                    montant_ajuste = charge.montant * adj_data.get("factor", 1.0)
                    
                    regularisations.append(
                        EcritureComptable(
                            compte_id=charge.compte_id,
                            date=datetime.now(),
                            libelle=f"Régularisation ML - {charge.libelle}",
                            montant=montant_ajuste - charge.montant,
                            sens="DEBIT" if montant_ajuste > charge.montant else "CREDIT"
                        )
                    )
                    
        return regularisations

    async def _calculer_variations_stocks_ml(
        self,
        periode: str,
        analyse_ml: Dict[str, Any]
    ) -> List[EcritureComptable]:
        """Calcule les variations de stocks avec ML"""
        variations = []
        
        # Prédictions ML des variations
        if "stock_predictions" in analyse_ml["ml_analysis"]:
            predictions = analyse_ml["ml_analysis"]["stock_predictions"]
            for categorie, pred in predictions.items():
                variations.append(
                    EcritureComptable(
                        compte_id=self._get_compte_variation_stock(categorie),
                        date=datetime.now(),
                        libelle=f"Variation stock ML - {categorie}",
                        montant=pred["variation"],
                        sens="DEBIT" if pred["variation"] > 0 else "CREDIT"
                    )
                )
                
        return variations

    async def _calculer_provisions_ml(
        self,
        periode: str,
        analyse_ml: Dict[str, Any],
        optimization: Dict[str, Any]
    ) -> List[EcritureComptable]:
        """Calcule les provisions avec ML"""
        provisions = []
        
        # Calcul ML des provisions
        if "provision_recommendations" in analyse_ml["ml_analysis"]:
            recommendations = analyse_ml["ml_analysis"]["provision_recommendations"]
            for rec in recommendations:
                # Optimisation du montant
                montant = rec["amount"]
                if "provision_optimizations" in optimization:
                    if rec["category"] in optimization["provision_optimizations"]:
                        opt_data = optimization["provision_optimizations"][rec["category"]]
                        montant = opt_data.get("optimized_amount", montant)
                
                provisions.append(
                    EcritureComptable(
                        compte_id=self._get_compte_provision(rec["category"]),
                        date=datetime.now(),
                        libelle=f"Provision ML - {rec['description']}",
                        montant=montant,
                        sens="DEBIT",
                        ml_confidence=rec.get("confidence", 0.8)
                    )
                )
                
        return provisions

    async def _calculer_amortissements_ml(
        self,
        periode: str,
        analyse_ml: Dict[str, Any]
    ) -> List[EcritureComptable]:
        """Calcule les amortissements avec ML"""
        amortissements = []
        
        # Calcul ML des amortissements
        if "amortization_predictions" in analyse_ml["ml_analysis"]:
            predictions = analyse_ml["ml_analysis"]["amortization_predictions"]
            for pred in predictions:
                amortissements.append(
                    EcritureComptable(
                        compte_id=self._get_compte_amortissement(pred["category"]),
                        date=datetime.now(),
                        libelle=f"Amortissement ML - {pred['description']}",
                        montant=pred["amount"],
                        sens="DEBIT",
                        ml_confidence=pred.get("confidence", 0.8)
                    )
                )
                
        return amortissements

    async def _calculer_totaux_periode(self, periode: str) -> Dict[str, Any]:
        """Calcule les totaux de la période"""
        totaux = {
            "charges": {},
            "produits": {},
            "resultat": 0,
            "tresorerie": {},
            "bilan": {
                "actif": {},
                "passif": {}
            }
        }
        
        # Calcul des charges par catégorie
        charges = self.db.query(
            EcritureComptable.categorie,
            func.sum(EcritureComptable.debit)
        ).filter(
            EcritureComptable.periode == periode,
            EcritureComptable.type_compte == TypeCompte.CHARGE
        ).group_by(EcritureComptable.categorie).all()
        
        for categorie, montant in charges:
            totaux["charges"][categorie] = float(montant)
            
        # Calcul des produits par catégorie
        produits = self.db.query(
            EcritureComptable.categorie,
            func.sum(EcritureComptable.credit)
        ).filter(
            EcritureComptable.periode == periode,
            EcritureComptable.type_compte == TypeCompte.PRODUIT
        ).group_by(EcritureComptable.categorie).all()
        
        for categorie, montant in produits:
            totaux["produits"][categorie] = float(montant)
            
        # Calcul du résultat
        totaux["resultat"] = (
            sum(totaux["produits"].values()) - 
            sum(totaux["charges"].values())
        )
        
        return totaux

    async def _geler_ecritures(self, periode: str) -> None:
        """Gèle les écritures de la période"""
        self.db.query(EcritureComptable).filter(
            EcritureComptable.periode == periode
        ).update({
            "modifiable": False
        })
        
        self.db.commit()

    async def _generer_etats_cloture_ml(
        self,
        periode: str,
        totaux: Dict[str, Any],
        ecritures_validees: List[EcritureComptable],
        ecritures_cloture: List[EcritureComptable],
        analyse_ml: Dict[str, Any],
        optimization: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Génère les états de clôture avec ML"""
        return {
            "grand_livre": await self._generer_grand_livre(periode),
            "balance": await self._generer_balance(periode),
            "compte_resultat": await self._generer_compte_resultat(periode, totaux),
            "bilan": await self._generer_bilan(periode, totaux),
            "annexes": {
                "detail_ecritures": {
                    "validees": [e.to_dict() for e in ecritures_validees],
                    "cloture": [e.to_dict() for e in ecritures_cloture]
                },
                "rapprochements": await self._generer_rapprochements(periode),
                "provisions": await self._generer_detail_provisions_ml(
                    periode,
                    analyse_ml,
                    optimization
                )
            },
            "ml_analysis": {
                "predictions": analyse_ml["ml_analysis"].get("predictions", {}),
                "risk_factors": analyse_ml["ml_analysis"].get("risk_factors", []),
                "optimization_results": optimization.get("results", {})
            }
        }

    async def _archiver_documents(
        self,
        periode: str,
        etats: Dict[str, Any]
    ) -> None:
        """Archive les documents de clôture"""
        # Création du dossier d'archive
        archive_path = f"archives/cloture/{periode}"
        os.makedirs(archive_path, exist_ok=True)
        
        # Sauvegarde des états
        for nom_etat, contenu in etats.items():
            with open(f"{archive_path}/{nom_etat}.json", "w") as f:
                json.dump(contenu, f, indent=2)
                
        # Archivage des pièces justificatives
        await self._archiver_pieces_justificatives(periode, archive_path)
        
        # Génération du rapport de clôture avec ML
        await self._generer_rapport_cloture_ml(periode, archive_path, etats)

    async def _generate_cloture_recommendations(
        self,
        totaux: Dict[str, Any],
        analyse_ml: Dict[str, Any],
        optimization: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Génère des recommandations ML pour la clôture"""
        recommendations = []
        
        # Recommandations ML
        if "recommendations" in analyse_ml["ml_analysis"]:
            for rec in analyse_ml["ml_analysis"]["recommendations"]:
                if rec["type"] == "CLOSING":
                    recommendations.append({
                        "type": "ML",
                        "priority": rec["priority"],
                        "description": rec["description"],
                        "actions": rec["actions"],
                        "expected_impact": rec.get("expected_impact")
                    })
                    
        # Recommandations optimisation
        if "closing_optimizations" in optimization:
            for opt in optimization["closing_optimizations"]:
                recommendations.append({
                    "type": "OPTIMIZATION",
                    "priority": "HIGH",
                    "description": opt["description"],
                    "actions": opt["actions"],
                    "expected_impact": {
                        "savings": opt.get("savings", 0),
                        "timeline": opt.get("timeline", "N/A")
                    }
                })
                
        # Recommandations basées sur les totaux
        if totaux["resultat"] < 0:
            recommendations.append({
                "type": "ALERT",
                "priority": "HIGH",
                "description": "Résultat négatif",
                "actions": [
                    "Analyser causes",
                    "Optimiser coûts",
                    "Revoir pricing"
                ]
            })
            
        return recommendations
