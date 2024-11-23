import { QueryClient } from '@tanstack/react-query';

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5, // 5 minutes
      gcTime: 1000 * 60 * 30, // 30 minutes (remplace cacheTime)
      retry: 3,
      retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000),
      refetchOnWindowFocus: false,
      refetchOnMount: true
    },
    mutations: {
      retry: 2,
      retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000)
    }
  }
});

// Clés de requête communes
export const queryKeys = {
  // Production
  production: {
    all: ['production'] as const,
    parcelles: () => [...queryKeys.production.all, 'parcelles'] as const,
    parcelle: (id: string) => [...queryKeys.production.parcelles(), id] as const,
    cycles: (parcelleId: string) => [...queryKeys.production.parcelle(parcelleId), 'cycles'] as const,
    recoltes: (parcelleId: string) => [...queryKeys.production.parcelle(parcelleId), 'recoltes'] as const,
    stats: () => [...queryKeys.production.all, 'stats'] as const
  },

  // Gestion de Projets
  projects: {
    all: ['projects'] as const,
    list: () => [...queryKeys.projects.all, 'list'] as const,
    detail: (id: string) => [...queryKeys.projects.all, id] as const,
    tasks: (projectId: string) => [...queryKeys.projects.detail(projectId), 'tasks'] as const,
    task: (projectId: string, taskId: string) => [...queryKeys.projects.tasks(projectId), taskId] as const,
    comments: (taskId: string) => ['tasks', taskId, 'comments'] as const,
    documents: (projectId: string) => [...queryKeys.projects.detail(projectId), 'documents'] as const,
    stats: () => [...queryKeys.projects.all, 'stats'] as const,
    weather: (projectId: string) => [...queryKeys.projects.detail(projectId), 'weather'] as const
  },

  // Finance
  finance: {
    all: ['finance'] as const,
    stats: () => [...queryKeys.finance.all, 'stats'] as const,
    transactions: () => [...queryKeys.finance.all, 'transactions'] as const,
    transaction: (id: string) => [...queryKeys.finance.transactions(), id] as const,
    budget: () => [...queryKeys.finance.all, 'budget'] as const,
    cashflow: () => [...queryKeys.finance.all, 'cashflow'] as const,
    projections: () => [...queryKeys.finance.all, 'projections'] as const,
    budgetAnalysis: (periode: string) => [...queryKeys.finance.budget(), 'analysis', periode] as const
  },

  // Comptabilité
  comptabilite: {
    all: ['comptabilite'] as const,
    comptes: () => [...queryKeys.comptabilite.all, 'comptes'] as const,
    compte: (id: string) => [...queryKeys.comptabilite.comptes(), id] as const,
    ecritures: () => [...queryKeys.comptabilite.all, 'ecritures'] as const,
    ecriture: (id: string) => [...queryKeys.comptabilite.ecritures(), id] as const,
    balance: () => [...queryKeys.comptabilite.all, 'balance'] as const,
    grandLivre: () => [...queryKeys.comptabilite.all, 'grand-livre'] as const,
    budgetAnalysis: (periode: string) => [...queryKeys.comptabilite.all, 'budget', 'analysis', periode] as const
  },

  // Ressources Humaines
  hr: {
    all: ['hr'] as const,
    employees: () => [...queryKeys.hr.all, 'employees'] as const,
    employee: (id: string) => [...queryKeys.hr.employees(), id] as const,
    stats: () => [...queryKeys.hr.all, 'stats'] as const,
    leaves: () => [...queryKeys.hr.all, 'leaves'] as const,
    leave: (id: string) => [...queryKeys.hr.leaves(), id] as const,
    attendance: () => [...queryKeys.hr.all, 'attendance'] as const,
    training: () => [...queryKeys.hr.all, 'training'] as const
  },

  // Inventaire
  inventory: {
    all: ['inventory'] as const,
    products: () => [...queryKeys.inventory.all, 'products'] as const,
    product: (id: string) => [...queryKeys.inventory.products(), id] as const,
    movements: () => [...queryKeys.inventory.all, 'movements'] as const,
    movement: (id: string) => [...queryKeys.inventory.movements(), id] as const,
    stats: () => [...queryKeys.inventory.all, 'stats'] as const,
    alerts: () => [...queryKeys.inventory.all, 'alerts'] as const
  },

  // Paramétrage
  parametrage: {
    all: ['parametrage'] as const,
    general: () => [...queryKeys.parametrage.all, 'general'] as const,
    modules: () => [...queryKeys.parametrage.all, 'modules'] as const,
    users: () => [...queryKeys.parametrage.all, 'users'] as const,
    roles: () => [...queryKeys.parametrage.all, 'roles'] as const
  },

  // Météo (utilisé par plusieurs modules)
  weather: {
    all: ['weather'] as const,
    current: () => [...queryKeys.weather.all, 'current'] as const,
    forecast: () => [...queryKeys.weather.all, 'forecast'] as const,
    alerts: () => [...queryKeys.weather.all, 'alerts'] as const,
    agricultural: () => [...queryKeys.weather.all, 'agricultural'] as const
  }
} as const;
