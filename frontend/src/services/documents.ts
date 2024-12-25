import { api } from '../config/axios';

export interface Document {
  id: string;
  nom: string;
  description?: string;
  type_document: string;
  taille: number;
  chemin_fichier: string;
  created_at: string;
  uploaded_by: {
    id: string;
    nom: string;
    prenom: string;
  };
}

interface GetDocumentsParams {
  module?: string;
  referenceId?: string;
}

export const getDocuments = async ({ module, referenceId }: GetDocumentsParams): Promise<Document[]> => {
  const params = new URLSearchParams();
  if (module) params.append('module', module);
  if (referenceId) params.append('reference_id', referenceId);
  
  const { data } = await api.get<Document[]>('/documents', { params });
  return data;
};

interface DeleteDocumentParams {
  id: string;
  module?: string;
  referenceId?: string;
}

export const deleteDocument = async ({ id, module, referenceId }: DeleteDocumentParams): Promise<void> => {
  const params = new URLSearchParams();
  if (module) params.append('module', module);
  if (referenceId) params.append('reference_id', referenceId);
  
  await api.delete(`/documents/${id}`, { params });
};

export const uploadDocument = async (formData: FormData): Promise<Document> => {
  const { data } = await api.post<Document>('/documents/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  });
  return data;
};