import { api } from './api';

export interface Product {
  id: string;
  code: string;
  nom: string;
  categorie: 'INTRANT' | 'EQUIPEMENT' | 'RECOLTE' | 'EMBALLAGE' | 'PIECE_RECHANGE';
  description?: string;
  unite_mesure: 'KG' | 'LITRE' | 'UNITE' | 'TONNE' | 'METRE';
  seuil_alerte?: number;
  prix_unitaire?: number;
  specifications?: Record<string, any>;
}

export interface Responsable {
  id: string;
  nom: string;
  prenom: string;
}

export interface StockMovement {
  id: string;
  produit_id: string;
  type_mouvement: 'ENTREE' | 'SORTIE' | 'TRANSFERT';
  quantite: number;
  entrepot_source_id?: string;
  entrepot_destination_id?: string;
  responsable_id: string;
  responsable?: Responsable;
  reference_document?: string;
  notes?: string;
  cout_unitaire?: number;
  date_mouvement: string;
}

export interface Stock {
  id: string;
  produit_id: string;
  entrepot_id: string;
  quantite: number;
  valeur_unitaire?: number;
  emplacement?: string;
  lot?: string;
  date_derniere_maj: string;
}

export interface Variation {
  value: number;
  type: 'increase' | 'decrease';
}

export interface InventoryStats {
  total_products: number;
  low_stock_alerts: number;
  total_value: number;
  totalValue: number; // Alias pour la compatibilité
  valueVariation: Variation;
  movements_today: number;
  movements: number; // Alias pour la compatibilité
  movementsVariation: Variation;
  stock_by_category: Record<string, number>;
  recent_movements: StockMovement[];
  turnoverRate: number;
  turnoverVariation: Variation;
  alerts: number; // Alias pour la compatibilité
  alertsVariation: Variation;
}

// Produits
export const getProducts = async (): Promise<Product[]> => {
  const response = await api.get('/api/v1/inventory/products');
  return response.data;
};

export const getProduct = async (id: string): Promise<Product> => {
  const response = await api.get(`/api/v1/inventory/products/${id}`);
  return response.data;
};

export const createProduct = async (product: Omit<Product, 'id'>): Promise<Product> => {
  const response = await api.post('/api/v1/inventory/products', product);
  return response.data;
};

export const updateProduct = async (id: string, product: Partial<Product>): Promise<Product> => {
  const response = await api.put(`/api/v1/inventory/products/${id}`, product);
  return response.data;
};

export const deleteProduct = async (id: string): Promise<void> => {
  await api.delete(`/api/v1/inventory/products/${id}`);
};

// Mouvements de stock
export const getStockMovements = async (): Promise<StockMovement[]> => {
  const response = await api.get('/api/v1/inventory/movements');
  return response.data;
};

export const getProductMovements = async (productId: string): Promise<StockMovement[]> => {
  const response = await api.get(`/api/v1/inventory/movements/product/${productId}`);
  return response.data;
};

export const createStockMovement = async (movement: Omit<StockMovement, 'id' | 'date_mouvement'>): Promise<StockMovement> => {
  const response = await api.post('/api/v1/inventory/movements', movement);
  return response.data;
};

// Stock
export const getStockLevels = async (): Promise<Stock[]> => {
  const response = await api.get('/api/v1/inventory/stock');
  return response.data;
};

export const getProductStock = async (productId: string): Promise<Stock[]> => {
  const response = await api.get(`/api/v1/inventory/stock/product/${productId}`);
  return response.data;
};

// Statistiques
export const getInventoryStats = async (): Promise<InventoryStats> => {
  const response = await api.get('/api/v1/inventory/stats');
  return response.data;
};

// Alertes
export const getLowStockAlerts = async (): Promise<Product[]> => {
  const response = await api.get('/api/v1/inventory/alerts/low-stock');
  return response.data;
};

// Utilitaires
export const getStockValue = async (productId: string): Promise<number> => {
  const response = await api.get(`/api/v1/inventory/stock/value/${productId}`);
  return response.data.value;
};

export const validateStockMovement = async (movement: Omit<StockMovement, 'id' | 'date_mouvement'>): Promise<boolean> => {
  const response = await api.post('/api/v1/inventory/movements/validate', movement);
  return response.data.valid;
};
