from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
from db.database import get_db
from models.auth import Utilisateur
from models.document import Document, TypeDocument
from schemas.document import DocumentCreate, DocumentResponse
from api.v1.endpoints.auth import get_current_user
from services.storage_service import StorageService

router = APIRouter()

@router.post("/upload", response_model=DocumentResponse)
async def upload_document(
    file: UploadFile = File(...),
    type_document: TypeDocument = TypeDocument.PIECE_JOINTE,
    description: Optional[str] = None,
    module: Optional[str] = None,
    reference_id: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_user)
):
    """Upload un nouveau document"""
    storage = StorageService()
    
    try:
        # Sauvegarder le fichier
        file_path = await storage.save_file(
            file,
            f"documents/{module or 'general'}/{datetime.now().year}/{datetime.now().month}"
        )
        
        # Créer l'entrée dans la base de données
        document = Document(
            nom=file.filename,
            type_document=type_document,
            description=description,
            chemin_fichier=file_path,
            taille=await storage._get_file_size(file),
            type_mime=file.content_type,
            module=module,
            reference_id=reference_id,
            uploaded_by_id=current_user.id
        )
        
        db.add(document)
        db.commit()
        db.refresh(document)
        return document
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erreur lors de l'upload du fichier")

@router.get("/", response_model=List[DocumentResponse])
async def get_documents(
    module: Optional[str] = None,
    type_document: Optional[TypeDocument] = None,
    reference_id: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_user)
):
    """Récupère la liste des documents"""
    query = db.query(Document)
    if module:
        query = query.filter(Document.module == module)
    if type_document:
        query = query.filter(Document.type_document == type_document)
    if reference_id:
        query = query.filter(Document.reference_id == reference_id)
    return query.order_by(Document.created_at.desc()).all()

@router.delete("/{document_id}")
async def delete_document(
    document_id: str,
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_user)
):
    """Supprime un document"""
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document non trouvé")
    
    storage = StorageService()
    if await storage.delete_file(document.chemin_fichier):
        db.delete(document)
        db.commit()
        return {"status": "success"}
    
    raise HTTPException(status_code=500, detail="Erreur lors de la suppression du fichier")