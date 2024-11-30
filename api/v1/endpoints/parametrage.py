from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.database import get_db
from models.parametrage import ModuleSysteme, ParametreSysteme
from schemas.parametrage import (
    ModuleSystemeCreate,
    ModuleSystemeUpdate,
    ModuleSystemeResponse,
    ParametreSystemeCreate,
    ParametreSystemeUpdate,
    ParametreSystemeResponse
)

router = APIRouter()

@router.get("/modules/", response_model=List[ModuleSystemeResponse])
def get_modules(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Récupère la liste des modules système"""
    modules = db.query(ModuleSysteme).offset(skip).limit(limit).all()
    return modules

@router.post("/modules/", response_model=ModuleSystemeResponse)
def create_module(
    module: ModuleSystemeCreate,
    db: Session = Depends(get_db)
):
    """Crée un nouveau module système"""
    db_module = ModuleSysteme(**module.dict())
    db.add(db_module)
    db.commit()
    db.refresh(db_module)
    return db_module

@router.get("/modules/{module_id}", response_model=ModuleSystemeResponse)
def get_module(
    module_id: str,
    db: Session = Depends(get_db)
):
    """Récupère un module système par son ID"""
    module = db.query(ModuleSysteme).filter(ModuleSysteme.id == module_id).first()
    if not module:
        raise HTTPException(status_code=404, detail="Module non trouvé")
    return module

@router.put("/modules/{module_id}", response_model=ModuleSystemeResponse)
def update_module(
    module_id: str,
    module_update: ModuleSystemeUpdate,
    db: Session = Depends(get_db)
):
    """Met à jour un module système"""
    module = db.query(ModuleSysteme).filter(ModuleSysteme.id == module_id).first()
    if not module:
        raise HTTPException(status_code=404, detail="Module non trouvé")
    
    for field, value in module_update.dict(exclude_unset=True).items():
        setattr(module, field, value)
    
    db.commit()
    db.refresh(module)
    return module

@router.delete("/modules/{module_id}")
def delete_module(
    module_id: str,
    db: Session = Depends(get_db)
):
    """Supprime un module système"""
    module = db.query(ModuleSysteme).filter(ModuleSysteme.id == module_id).first()
    if not module:
        raise HTTPException(status_code=404, detail="Module non trouvé")
    
    db.delete(module)
    db.commit()
    return {"message": "Module supprimé avec succès"}

@router.get("/parametres/", response_model=List[ParametreSystemeResponse])
def get_parametres(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Récupère la liste des paramètres système"""
    parametres = db.query(ParametreSysteme).offset(skip).limit(limit).all()
    return parametres

@router.post("/parametres/", response_model=ParametreSystemeResponse)
def create_parametre(
    parametre: ParametreSystemeCreate,
    db: Session = Depends(get_db)
):
    """Crée un nouveau paramètre système"""
    db_parametre = ParametreSysteme(**parametre.dict())
    db.add(db_parametre)
    db.commit()
    db.refresh(db_parametre)
    return db_parametre

@router.get("/parametres/{parametre_id}", response_model=ParametreSystemeResponse)
def get_parametre(
    parametre_id: str,
    db: Session = Depends(get_db)
):
    """Récupère un paramètre système par son ID"""
    parametre = db.query(ParametreSysteme).filter(ParametreSysteme.id == parametre_id).first()
    if not parametre:
        raise HTTPException(status_code=404, detail="Paramètre non trouvé")
    return parametre

@router.put("/parametres/{parametre_id}", response_model=ParametreSystemeResponse)
def update_parametre(
    parametre_id: str,
    parametre_update: ParametreSystemeUpdate,
    db: Session = Depends(get_db)
):
    """Met à jour un paramètre système"""
    parametre = db.query(ParametreSysteme).filter(ParametreSysteme.id == parametre_id).first()
    if not parametre:
        raise HTTPException(status_code=404, detail="Paramètre non trouvé")
    
    for field, value in parametre_update.dict(exclude_unset=True).items():
        setattr(parametre, field, value)
    
    db.commit()
    db.refresh(parametre)
    return parametre

@router.delete("/parametres/{parametre_id}")
def delete_parametre(
    parametre_id: str,
    db: Session = Depends(get_db)
):
    """Supprime un paramètre système"""
    parametre = db.query(ParametreSysteme).filter(ParametreSysteme.id == parametre_id).first()
    if not parametre:
        raise HTTPException(status_code=404, detail="Paramètre non trouvé")
    
    db.delete(parametre)
    db.commit()
    return {"message": "Paramètre supprimé avec succès"}
