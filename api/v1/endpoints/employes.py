from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from db.database import get_db
from models.hr import Employe
from schemas.employe import EmployeCreate, EmployeUpdate, EmployeResponse

router = APIRouter()

@router.get("/", response_model=List[EmployeResponse])
def get_employes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    employes = db.query(Employe).offset(skip).limit(limit).all()
    return employes

@router.post("/", response_model=EmployeResponse)
def create_employe(employe: EmployeCreate, db: Session = Depends(get_db)):
    db_employe = Employe(**employe.dict())
    db.add(db_employe)
    db.commit()
    db.refresh(db_employe)
    return db_employe

@router.get("/{employe_id}", response_model=EmployeResponse)
def get_employe(employe_id: str, db: Session = Depends(get_db)):
    employe = db.query(Employe).filter(Employe.id == employe_id).first()
    if employe is None:
        raise HTTPException(status_code=404, detail="Employé non trouvé")
    return employe