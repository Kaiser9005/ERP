# Module Documents - Documentation API

## Upload de Document

### POST /api/v1/documents/upload
Upload un nouveau document.

**Corps de la requête:**
- Multipart form data avec:
  - `file`: Fichier à uploader
  - `type_document`: Type de document (CONTRAT, FACTURE, etc.)
  - `description` (optionnel): Description du document
  - `module` (optionnel): Module associé
  - `reference_id` (optionnel): ID de l'objet associé

**Réponse:**
```json
{
  "id": "uuid",
  "nom": "facture.pdf",
  "type_document": "FACTURE",
  "description": "Facture fournisseur",
  "chemin_fichier": "documents/finance/2024/01/facture_20240120_123456.pdf",
  "taille": 125000,
  "type_mime": "application/pdf",
  "module": "finance",
  "reference_id": "uuid",
  "uploaded_by_id": "uuid",
  "created_at": "2024-01-20T12:34:56Z"
}
```

## Liste des Documents

### GET /api/v1/documents
Récupère la liste des documents.

**Paramètres de requête:**
- `module` (optionnel): Filtre par module
- `type_document` (optionnel): Filtre par type
- `reference_id` (optionnel): Filtre par référence

## Suppression de Document

### DELETE /api/v1/documents/{document_id}
Supprime un document.