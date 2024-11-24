"""
Module de gestion des processus de clôture comptable et financière
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

class GestionCloture:
    """Gestion des processus de clôture comptable et financière"""
    
    def __init__(self, db: Session):
        self.db = db

    async def executer_cloture_mensuelle(
        self,
        periode: str,
        utilisateur_id: str
    ) -> Dict[str, Any]:
        """Exécute le processus de clôture mensuelle"""
        # Vérification des conditions préalables
        validation = await self._verifier_conditions_cloture(periode)
        if not validation.is_valid:
            raise ValueError(f"Conditions de clôture non remplies: {validation.errors}")
            
        # Validation des écritures en attente
        ecritures_validees = await self._valider_ecritures_attente(
            periode,
            utilisateur_id
        )
        
        # Génération des écritures de clôture
        ecritures_cloture = await self._generer_ecritures_cloture(periode)
        
        # Calcul des totaux de la période
        totaux = await self._calculer_totaux_periode(periode)
        
        # Gel des écritures de la période
        await self._geler_ecritures(periode)
        
        # Génération des états de clôture
        etats = await self._generer_etats_cloture(
            periode,
            totaux,
            ecritures_validees,
            ecritures_cloture
        )
        
        # Archivage des documents
        await self._archiver_documents(periode, etats)
        
        return {
            "periode": periode,
            "statut": "CLOTURE",
            "date_cloture": datetime.utcnow().isoformat(),
            "utilisateur_id": utilisateur_id,
            "totaux": totaux,
            "etats": etats,
            "ecritures_validees": len(ecritures_validees),
            "ecritures_cloture": len(ecritures_cloture)
        }

    async def _verifier_conditions_cloture(self, periode: str) -> ValidationResult:
        """Vérifie les conditions nécessaires à la clôture"""
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
            
        # Vérification des provisions obligatoires
        provisions = await self._verifier_provisions_obligatoires(periode)
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

    async def _generer_ecritures_cloture(
        self,
        periode: str
    ) -> List[EcritureComptable]:
        """Génère les écritures de clôture de la période"""
        ecritures_cloture = []
        
        # Écritures de régularisation des charges
        regularisations = await self._calculer_regularisations_charges(periode)
        ecritures_cloture.extend(regularisations)
        
        # Écritures de variation des stocks
        variations = await self._calculer_variations_stocks(periode)
        ecritures_cloture.extend(variations)
        
        # Écritures de provisions
        provisions = await self._calculer_provisions(periode)
        ecritures_cloture.extend(provisions)
        
        # Écritures d'amortissements
        amortissements = await self._calculer_amortissements(periode)
        ecritures_cloture.extend(amortissements)
        
        # Sauvegarde des écritures
        for ecriture in ecritures_cloture:
            self.db.add(ecriture)
            
        self.db.commit()
        return ecritures_cloture

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

    async def _generer_etats_cloture(
        self,
        periode: str,
        totaux: Dict[str, Any],
        ecritures_validees: List[EcritureComptable],
        ecritures_cloture: List[EcritureComptable]
    ) -> Dict[str, Any]:
        """Génère les états de clôture"""
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
                "provisions": await self._generer_detail_provisions(periode)
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
        
        # Génération du rapport de clôture
        await self._generer_rapport_cloture(periode, archive_path, etats)
