import React, { useState } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  TextField,
  MenuItem,
  Box,
  LinearProgress,
  Typography
} from '@mui/material';
import { useDropzone } from 'react-dropzone';
import { useMutation, useQueryClient } from 'react-query';
import { uploadDocument } from '../../services/documents';
import { LoadingButton } from '@mui/lab';

interface DocumentUploadDialogProps {
  open: boolean;
  onClose: () => void;
  module?: string;
  referenceId?: string;
}

const DocumentUploadDialog: React.FC<DocumentUploadDialogProps> = ({
  open,
  onClose,
  module,
  referenceId
}) => {
  const [file, setFile] = useState<File | null>(null);
  const [type, setType] = useState('PIECE_JOINTE');
  const [description, setDescription] = useState('');
  const queryClient = useQueryClient();

  const { getRootProps, getInputProps } = useDropzone({
    onDrop: (acceptedFiles) => {
      setFile(acceptedFiles[0]);
    },
    maxFiles: 1
  });

  const mutation = useMutation(uploadDocument, {
    onSuccess: () => {
      queryClient.invalidateQueries(['documents', module, referenceId]);
      onClose();
      setFile(null);
      setDescription('');
      setType('PIECE_JOINTE');
    }
  });

  const handleSubmit = () => {
    if (file) {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('type_document', type);
      formData.append('description', description);
      if (module) formData.append('module', module);
      if (referenceId) formData.append('reference_id', referenceId);

      mutation.mutate(formData);
    }
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <DialogTitle>Nouveau Document</DialogTitle>
      
      <DialogContent>
        <Box sx={{ mb: 3 }}>
          <Box
            {...getRootProps()}
            sx={{
              border: '2px dashed',
              borderColor: 'primary.main',
              borderRadius: 1,
              p: 3,
              textAlign: 'center',
              cursor: 'pointer',
              mb: 2
            }}
          >
            <input {...getInputProps()} />
            {file ? (
              <Typography>{file.name}</Typography>
            ) : (
              <Typography>
                Glissez un fichier ici ou cliquez pour sélectionner
              </Typography>
            )}
          </Box>

          {mutation.isLoading && (
            <LinearProgress sx={{ mt: 1 }} />
          )}
        </Box>

        <TextField
          select
          label="Type de Document"
          value={type}
          onChange={(e) => setType(e.target.value)}
          fullWidth
          margin="normal"
        >
          <MenuItem value="PIECE_JOINTE">Pièce Jointe</MenuItem>
          <MenuItem value="FACTURE">Facture</MenuItem>
          <MenuItem value="BON_LIVRAISON">Bon de Livraison</MenuItem>
          <MenuItem value="CONTRAT">Contrat</MenuItem>
          <MenuItem value="RAPPORT">Rapport</MenuItem>
          <MenuItem value="AUTRE">Autre</MenuItem>
        </TextField>

        <TextField
          label="Description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          fullWidth
          margin="normal"
          multiline
          rows={3}
        />
      </DialogContent>

      <DialogActions>
        <Button onClick={onClose}>
          Annuler
        </Button>
        <LoadingButton
          variant="contained"
          onClick={handleSubmit}
          loading={mutation.isLoading}
          disabled={!file}
        >
          Téléverser
        </LoadingButton>
      </DialogActions>
    </Dialog>
  );
};

export default DocumentUploadDialog;