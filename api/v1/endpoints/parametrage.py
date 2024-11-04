from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict
from db.database import get_db
from models.parametrage import Parametre, ConfigurationModule, ModuleSysteme
from schemas.parametrage import (
    ParametreCreate,
    ParametreUpdate,
    ParametreResponse,
    ConfigurationModuleCreate,
    ConfigurationModuleUpdate,
    ConfigurationModuleResponse
)
from api.v1.endpoints.auth import get_current_user
from models.auth import Utilisateur

router = APIRouter()

@router.get("/parametres", response_model=List[ParametreResponse])
async def get_parametres(
    module: Optional[ModuleSysteme] = None,
    categorie: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_user)
):
    """Récupère la liste des paramètres"""
    query = db.query(Parametre)
    if module:
        query = query.filter(Parametre.module == module)
    if categorie:
        query = query.filter(Parametre.categorie == categorie)
    return query.order_by(Parametre.ordre).all()

@router.post("/parametres", response_model=ParametreResponse)
async def create_parametre(
    parametre: ParametreCreate,
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_user)
):
    """Crée un nouveau paramètre"""
    if db.query(Parametre).filter(Parametre.code == parametre.code).first():
        raise HTTPException(
            status_code=400,
            detail="Un paramètre avec ce code existe déjà"
        )
    
    db_parametre = Parametre(**parametre.dict())
    db.add(db_parametre)
    db.commit()
    db.refresh(db_parametre)
    return db_parametre

@router.put("/parametres/{parametre_id}", response_model=ParametreResponse)
async def update_parametre(
    parametre_id: str,
    parametre: ParametreUpdate,
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_user)
):
    """Met à jour un paramètre"""
    db_parametre = db.query(Parametre).filter(Parametre.id == parametre_id).first()
    if not db_parametre:
        raise HTTPException(status_code=404, detail="Paramètre non trouvé")
    
    if not db_parametre.modifiable:
        raise HTTPException(status_code=400, detail="Ce paramètre n'est pas modifiable")
    
    for key, value in parametre.dict(exclude_unset=True).items():
        setattr(db_parametre, key, value)
    
    db.commit()
    db.refresh(db_parametre)
    return db_parametre

@router.get("/modules/configuration", response_model=List[ConfigurationModuleResponse])
async def get_modules_configuration(
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_user)
):
    """Récupère la configuration de tous les modules"""
    return db.query(ConfigurationModule).order_by(ConfigurationModule.ordre_affichage).all()

@router.put("/modules/{module}/configuration", response_model=ConfigurationModuleResponse)
async def update_module_configuration(
    module: ModuleSysteme,
    config: ConfigurationModuleUpdate,
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_user)
):
    """Met à jour la configuration d'un module"""
    db_config = db.query(ConfigurationModule).filter(
        ConfigurationModule.module == module
    ).first()
    
    if not db_config:
        raise HTTPException(status_code=404, detail="Configuration du module non trouvée")
    
    for key, value in config.dict(exclude_unset=True).items():
        setattr(db_config, key, value)
    
    db.commit()
    db.refresh(db_config)
    return db_config