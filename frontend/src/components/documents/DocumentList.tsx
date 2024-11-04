import React, { useState } from 'react';
import {
  Card,
  CardContent,
  Typography,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  Chip,
  Box,
  IconButton,
  Button,
  TextField,
  InputAdornment
} from '@mui/material';
import { Download, Delete, Search, Upload } from '@mui/icons-material';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import { getDocuments, deleteDocument } from '../../services/documents';
import { format } from 'date-fns';
import { fr } from 'date-fns/locale';
import DocumentUploadDialog from './DocumentUploadDialog';

interface DocumentListProps {
  module?: string;
  referenceId?: string;
}

const DocumentList: React.FC<DocumentListProps> = ({ module, referenceId }) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [uploadDialogOpen, setUploadDialogOpen] = useState(false);
  const queryClient = useQueryClient();

  const { data: documents, isLoading } = useQuery(
    ['documents', module, referenceId],
    () => getDocuments({ module, referenceId })
  );

  const deleteMutation = useMutation(deleteDocument, {
    onSuccess: () => {
      queryClient.invalidateQueries(['documents', module, referenceId]);
    }
  });

  const filteredDocuments = documents?.filter(doc =>
    doc.nom.toLowerCase().includes(searchTerm.toLowerCase()) ||
    doc.description?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const handleDownload = (path: string) => {
    window.open(path, '_blank');
  };

  const handleDelete = (id: string) => {
    if (window.confirm('Voulez-vous vraiment supprimer ce document ?')) {
      deleteMutation.mutate(id);
    }
  };

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return `${parseFloat((bytes / Math.pow(k, i)).toFixed(2))} ${sizes[i]}`;
  };

  return (
    <Card>
      <CardContent>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
          <Typography variant="h6">Documents</Typography>
          <Box sx={{ display: 'flex', gap: 2 }}>
            <TextField
              size="small"
              placeholder="Rechercher..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <Search />
                  </InputAdornment>
                ),
              }}
            />
            <Button
              variant="contained"
              startIcon={<Upload />}
              onClick={() => setUploadDialogOpen(true)}
            >
              Nouveau Document
            </Button>
          </Box>
        </Box>

        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Nom</TableCell>
              <TableCell>Type</TableCell>
              <TableCell>Taille</TableCell>
              <TableCell>Ajouté le</TableCell>
              <TableCell>Par</TableCell>
              <TableCell align="right">Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {filteredDocuments?.map((doc) => (
              <TableRow key={doc.id}>
                <TableCell>{doc.nom}</TableCell>
                <TableCell>
                  <Chip
                    size="small"
                    label={doc.type_document}
                    color="primary"
                  />
                </TableCell>
                <TableCell>{formatFileSize(doc.taille)}</TableCell>
                <TableCell>
                  {format(new Date(doc.created_at), 'Pp', { locale: fr })}
                </TableCell>
                <TableCell>
                  {doc.uploaded_by.prenom} {doc.uploaded_by.nom}
                </TableCell>
                <TableCell align="right">
                  <IconButton
                    size="small"
                    onClick={() => handleDownload(doc.chemin_fichier)}
                  >
                    <Download />
                  </IconButton>
                  <IconButton
                    size="small"
                    onClick={() => handleDelete(doc.id)}
                  >
                    <Delete />
                  </IconButton>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>

        <DocumentUploadDialog
          open={uploadDialogOpen}
          onClose={() => setUploadDialogOpen(false)}
          module={module}
          referenceId={referenceId}
        />
      </CardContent>
    </Card>
  );
};

export default DocumentList;