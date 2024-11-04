import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from 'react-query';
import DocumentUploadDialog from '../DocumentUploadDialog';
import { uploadDocument } from '../../../services/documents';

jest.mock('../../../services/documents');

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: false,
    },
  },
});

const mockOnClose = jest.fn();

const renderWithProviders = (component: React.ReactElement) => {
  return render(
    <QueryClientProvider client={queryClient}>
      {component}
    </QueryClientProvider>
  );
};

describe('DocumentUploadDialog', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('affiche le dialogue quand il est ouvert', () => {
    renderWithProviders(
      <DocumentUploadDialog 
        open={true}
        onClose={mockOnClose}
      />
    );
    
    expect(screen.getByText('Nouveau Document')).toBeInTheDocument();
    expect(screen.getByText('Glissez un fichier ici ou cliquez pour sélectionner')).toBeInTheDocument();
  });

  it('permet la sélection du type de document', () => {
    renderWithProviders(
      <DocumentUploadDialog 
        open={true}
        onClose={mockOnClose}
      />
    );
    
    const typeSelect = screen.getByLabelText('Type de Document');
    fireEvent.mouseDown(typeSelect);
    
    expect(screen.getByText('Facture')).toBeInTheDocument();
    expect(screen.getByText('Contrat')).toBeInTheDocument();
    expect(screen.getByText('Rapport')).toBeInTheDocument();
  });

  it('permet l\'ajout d\'une description', () => {
    renderWithProviders(
      <DocumentUploadDialog 
        open={true}
        onClose={mockOnClose}
      />
    );
    
    const descriptionInput = screen.getByLabelText('Description');
    fireEvent.change(descriptionInput, { target: { value: 'Test description' } });
    
    expect(descriptionInput).toHaveValue('Test description');
  });

  it('désactive le bouton de téléversement sans fichier', () => {
    renderWithProviders(
      <DocumentUploadDialog 
        open={true}
        onClose={mockOnClose}
      />
    );
    
    const submitButton = screen.getByText('Téléverser');
    expect(submitButton).toBeDisabled();
  });

  it('gère le téléversement de fichier', async () => {
    (uploadDocument as jest.Mock).mockResolvedValue({ id: '1' });

    renderWithProviders(
      <DocumentUploadDialog 
        open={true}
        onClose={mockOnClose}
      />
    );
    
    const file = new File(['test'], 'test.pdf', { type: 'application/pdf' });
    const input = screen.getByRole('textbox', { hidden: true });
    
    Object.defineProperty(input, 'files', {
      value: [file]
    });
    
    fireEvent.drop(input);
    
    expect(screen.getByText('test.pdf')).toBeInTheDocument();
    
    const submitButton = screen.getByText('Téléverser');
    expect(submitButton).not.toBeDisabled();
    
    fireEvent.click(submitButton);
    
    await waitFor(() => {
      expect(uploadDocument).toHaveBeenCalled();
      expect(mockOnClose).toHaveBeenCalled();
    });
  });
});