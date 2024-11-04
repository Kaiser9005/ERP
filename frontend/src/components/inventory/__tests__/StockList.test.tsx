import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from 'react-query';
import StockList from '../StockList';
import { getStocks } from '../../../services/inventory';

jest.mock('../../../services/inventory');

const mockStocks = [
  {
    id: '1',
    code: 'PRD001',
    name: 'Engrais NPK',
    quantity: 500,
    unit: 'kg',
    value: 750000,
    threshold: 100
  },
  {
    id: '2',
    code: 'PRD002',
    name: 'Pesticide',
    quantity: 50,
    unit: 'L',
    value: 250000,
    threshold: 100
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

describe('StockList', () => {
  beforeEach(() => {
    (getStocks as jest.Mock).mockResolvedValue(mockStocks);
  });

  it('affiche la liste des stocks', async () => {
    renderWithProviders(<StockList />);
    
    expect(await screen.findByText('PRD001')).toBeInTheDocument();
    expect(await screen.findByText('Engrais NPK')).toBeInTheDocument();
  });

  it('permet la recherche de produits', async () => {
    renderWithProviders(<StockList />);
    
    const searchInput = screen.getByPlaceholderText('Rechercher...');
    fireEvent.change(searchInput, { target: { value: 'Engrais' } });
    
    expect(screen.getByText('Engrais NPK')).toBeInTheDocument();
    expect(screen.queryByText('Pesticide')).not.toBeInTheDocument();
  });

  it('affiche les statuts de stock corrects', async () => {
    renderWithProviders(<StockList />);
    
    const normalChip = await screen.findByText('Normal');
    const alertChip = await screen.findByText('Alerte');
    
    expect(normalChip).toHaveClass('MuiChip-colorSuccess');
    expect(alertChip).toHaveClass('MuiChip-colorError');
  });

  it('ouvre le dialogue de mouvement au clic sur le bouton', async () => {
    renderWithProviders(<StockList />);
    
    const addButton = await screen.findByTestId('add-movement-button');
    fireEvent.click(addButton);
    
    expect(screen.getByTestId('stock-movement-dialog')).toBeInTheDocument();
  });
});