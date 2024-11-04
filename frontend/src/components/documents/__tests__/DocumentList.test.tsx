import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from 'react-query';
import DocumentList from '../DocumentList';
import { getDocuments } from '../../../services/documents';

jest.mock('../../../services/documents');

const mockDocuments = [
  {
    id: '1',
    nom: 'document1.pdf',
    type_document: 'PIECE_JOINTE',
    taille: 1024,
    created_at: '2024-01-20T10:00:00Z',
    uploaded_by: {
      nom: 'Doe',
      prenom: 'John'
    }
  }
];

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: false,
    },
  },
});

const renderWithProviders = (component: React.ReactElement) => {
  return render(
    <QueryClientProvider client={queryClient}>
      {component}
    </QueryClientProvider>
  );
};

describe('DocumentList', () => {
  beforeEach(() => {
    (getDocuments as jest.Mock).mockResolvedValue(mockDocuments);
  });

  it('affiche la liste des documents', async () => {
    renderWithProviders(<DocumentList />);
    
    expect(await screen.findByText('document1.pdf')).toBeInTheDocument();
    expect(await screen.findByText('John Doe')).toBeInTheDocument();
  });

  it('permet la recherche de documents', async () => {
    renderWithProviders(<DocumentList />);
    
    const searchInput = screen.getByPlaceholderText('Rechercher...');
    fireEvent.change(searchInput, { target: { value: 'document1' } });
    
    expect(screen.getByText('document1.pdf')).toBeInTheDocument();
  });

  it('affiche le bouton d\'upload', () => {
    renderWithProviders(<DocumentList />);
    
    expect(screen.getByText('Nouveau Document')).toBeInTheDocument();
  });

  it('affiche les actions pour chaque document', async () => {
    renderWithProviders(<DocumentList />);
    
    const downloadButtons = await screen.findAllByRole('button', { name: /télécharger/i });
    const deleteButtons = await screen.findAllByRole('button', { name: /supprimer/i });
    
    expect(downloadButtons).toHaveLength(1);
    expect(deleteButtons).toHaveLength(1);
  });
});