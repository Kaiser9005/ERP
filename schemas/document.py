from pydantic import BaseModel, UUID4
from datetime import datetime
from typing import Optional, Dict
from models.document import TypeDocument

class DocumentBase(BaseModel):
    nom: str
    type_document: TypeDocument
    description: Optional[str]
    module: Optional[str]
    reference_id: Optional[UUID4]
    metadata: Optional[Dict]

class DocumentCreate(DocumentBase):
    pass

class DocumentResponse(DocumentBase):
    id: UUID4
    chemin_fichier: str
    taille: int
    type_mime: str
    uploaded_by_id: UUID4
    created_at: datetime
    
    class Config:
        orm_mode = True