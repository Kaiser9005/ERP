import { QueryClient } from '@tanstack/react-query';

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5, // 5 minutes
      retry: 1,
      refetchOnWindowFocus: false
    }
  }
});

export const queryKeys = {
  finance: {
    stats: () => ['finance', 'stats'],
    transactions: (filters?: any) => ['finance', 'transactions', filters],
    transaction: (id: string) => ['finance', 'transaction', id],
    cashflow: (periode?: string) => ['finance', 'cashflow', periode],
    budgets: (filters?: any) => ['finance', 'budgets', filters],
    budget: (id: string) => ['finance', 'budget', id]
  },
  comptabilite: {
    comptes: () => ['comptabilite', 'comptes'],
    compte: (id: string) => ['comptabilite', 'compte', id],
    grandLivre: (params: { compte_id: string; date_debut: string; date_fin: string }) => 
      ['comptabilite', 'grandLivre', params],
    balance: (params: { date_debut: string; date_fin: string; type_compte?: string }) => 
      ['comptabilite', 'balance', params],
    journaux: (params: { date_debut: string; date_fin: string; journal?: string }) => 
      ['comptabilite', 'journaux', params]
  },
  production: {
    stats: () => ['production', 'stats'],
    parcelles: () => ['production', 'parcelles'],
    parcelle: (id: string) => ['production', 'parcelle', id],
    recoltes: (filters?: any) => ['production', 'recoltes', filters],
    meteo: () => ['production', 'meteo'],
    rapports: (filters?: any) => ['production', 'rapports', filters]
  },
  projets: {
    stats: () => ['projets', 'stats'],
    liste: (filters?: any) => ['projets', 'liste', filters],
    detail: (id: string) => ['projets', 'detail', id],
    taches: (projetId?: string, filters?: any) => ['projets', 'taches', projetId, filters],
    tache: (id: string) => ['projets', 'tache', id],
    ressources: (projetId: string) => ['projets', 'ressources', projetId],
    planning: (filters?: any) => ['projets', 'planning', filters],
    rapports: (projetId: string, type: string) => ['projets', 'rapports', projetId, type],
    documents: (projetId: string) => ['projets', 'documents', projetId],
    activites: (projetId: string) => ['projets', 'activites', projetId],
    risques: (projetId: string) => ['projets', 'risques', projetId],
    meteo: (projetId: string) => ['projets', 'meteo', projetId]
  },
  inventaire: {
    stats: () => ['inventaire', 'stats'],
    produits: (filters?: any) => ['inventaire', 'produits', filters],
    produit: (id: string) => ['inventaire', 'produit', id],
    mouvements: (filters?: any) => ['inventaire', 'mouvements', filters],
    stock: (produitId: string) => ['inventaire', 'stock', produitId],
    alertes: () => ['inventaire', 'alertes'],
    rapports: (type: string, params?: any) => ['inventaire', 'rapports', type, params]
  },
  rh: {
    stats: () => ['rh', 'stats'],
    employes: () => ['rh', 'employes'],
    employe: (id: string) => ['rh', 'employe', id],
    presences: (filters?: any) => ['rh', 'presences', filters],
    conges: (filters?: any) => ['rh', 'conges', filters],
    paie: (periode: string) => ['rh', 'paie', periode],
    formations: () => ['rh', 'formations'],
    evaluations: (employeId: string) => ['rh', 'evaluations', employeId],
    documents: (employeId: string) => ['rh', 'documents', employeId]
  },
  parametrage: {
    modules: () => ['parametrage', 'modules'],
    utilisateurs: () => ['parametrage', 'utilisateurs'],
    roles: () => ['parametrage', 'roles'],
    permissions: () => ['parametrage', 'permissions'],
    configurations: (module: string) => ['parametrage', 'configurations', module],
    workflow: (type: string) => ['parametrage', 'workflow', type],
    notifications: () => ['parametrage', 'notifications']
  }
};
