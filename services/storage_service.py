import os
import shutil
from datetime import datetime
from fastapi import UploadFile
from typing import Optional
from pathlib import Path
from core.config import STORAGE_CONFIG

class StorageService:
    """Service de gestion du stockage des fichiers"""
    
    def __init__(self):
        self.storage_path = Path(STORAGE_CONFIG["storage_path"])
        self.max_size = STORAGE_CONFIG["max_file_size_mb"] * 1024 * 1024
        self.allowed_extensions = STORAGE_CONFIG["allowed_extensions"]

    async def save_file(
        self,
        file: UploadFile,
        subfolder: str,
        filename: Optional[str] = None
    ) -> str:
        """Sauvegarde un fichier uploadé"""
        # Vérifier la taille du fichier
        file_size = await self._get_file_size(file)
        if file_size > self.max_size:
            raise ValueError(f"Fichier trop volumineux (max {STORAGE_CONFIG['max_file_size_mb']}MB)")

        # Vérifier l'extension
        ext = self._get_extension(file.filename)
        if ext not in self.allowed_extensions:
            raise ValueError(f"Type de fichier non autorisé. Extensions permises: {', '.join(self.allowed_extensions)}")

        # Créer le dossier de destination
        dest_folder = self.storage_path / subfolder
        dest_folder.mkdir(parents=True, exist_ok=True)

        # Générer le nom du fichier
        if not filename:
            filename = self._generate_filename(file.filename)
        
        # Chemin complet du fichier
        file_path = dest_folder / filename

        # Sauvegarder le fichier
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return str(file_path.relative_to(self.storage_path))

    async def delete_file(self, file_path: str) -> bool:
        """Supprime un fichier"""
        full_path = self.storage_path / file_path
        try:
            if full_path.exists():
                full_path.unlink()
                return True
            return False
        except Exception:
            return False

    async def _get_file_size(self, file: UploadFile) -> int:
        """Récupère la taille d'un fichier uploadé"""
        file.file.seek(0, 2)  # Aller à la fin du fichier
        size = file.file.tell()  # Récupérer la position
        file.file.seek(0)  # Retourner au début
        return size

    def _get_extension(self, filename: str) -> str:
        """Récupère l'extension d'un fichier"""
        return os.path.splitext(filename)[1].lower()

    def _generate_filename(self, original_filename: str) -> str:
        """Génère un nom de fichier unique"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        name, ext = os.path.splitext(original_filename)
        return f"{name}_{timestamp}{ext}"