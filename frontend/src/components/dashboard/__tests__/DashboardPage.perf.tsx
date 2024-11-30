import { describe, it, expect } from 'vitest';
import { render, waitFor } from '@testing-library/react';
import DashboardPage from '../DashboardPage';
import {
  measureRenderTime,
  assertPerformance,
  measurePerformance,
  measureMemoryUsage,
  measureApiCall,
} from '../../../test/setupPerformance';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: false,
      staleTime: 0,
      gcTime: 0,
    },
  },
});

const wrapper = ({ children }: { children: React.ReactNode }) => (
  <QueryClientProvider client={queryClient}>
    {children}
  </QueryClientProvider>
);

describe('DashboardPage Performance Tests', () => {
  it('devrait se rendre rapidement', async () => {
    const { initialRender, rerenderTime } = await measureRenderTime(
      <DashboardPage />
    );

    // Le rendu initial devrait prendre moins de 200ms
    assertPerformance(initialRender, 200);
    
    // Le re-rendu devrait être plus rapide
    assertPerformance(rerenderTime, 100);
  });

  it('devrait charger les données rapidement', async () => {
    const duration = await measureApiCall(async () => {
      const response = await fetch('/api/v1/dashboard/stats');
      return response.json();
    });

    // L'appel API devrait prendre moins de 300ms
    assertPerformance(duration, 300);
  });

  it('devrait avoir une utilisation mémoire raisonnable', () => {
    const memoryBefore = measureMemoryUsage();
    
    render(
      <QueryClientProvider client={queryClient}>
        <DashboardPage />
      </QueryClientProvider>
    );
    
    const memoryAfter = measureMemoryUsage();
    
    // L'augmentation de la mémoire heap ne devrait pas dépasser 10MB
    const heapIncrease = memoryAfter.heapUsed - memoryBefore.heapUsed;
    expect(heapIncrease).toBeLessThan(10 * 1024 * 1024); // 10MB en bytes
  });

  it('devrait gérer efficacement les mises à jour fréquentes', async () => {
    const { rerender } = render(
      <QueryClientProvider client={queryClient}>
        <DashboardPage />
      </QueryClientProvider>
    );

    const updateTimes: number[] = [];

    // Mesurer 10 re-rendus consécutifs
    for (let i = 0; i < 10; i++) {
      const start = performance.now();
      await rerender(
        <QueryClientProvider client={queryClient}>
          <DashboardPage />
        </QueryClientProvider>
      );
      updateTimes.push(performance.now() - start);
    }

    // Calculer la moyenne des temps de mise à jour
    const averageUpdateTime = updateTimes.reduce((a, b) => a + b) / updateTimes.length;
    
    // La moyenne devrait être inférieure à 50ms
    expect(averageUpdateTime).toBeLessThan(50);
  });

  it('devrait charger les graphiques rapidement', async () => {
    const renderChart = async () => {
      const { container } = render(
        <QueryClientProvider client={queryClient}>
          <DashboardPage />
        </QueryClientProvider>
      );
      
      // Attendre que les graphiques soient chargés
      await waitFor(() => {
        expect(container.querySelector('.recharts-surface')).toBeInTheDocument();
      });
    };

    const duration = await measurePerformance(renderChart);
    
    // Le chargement des graphiques devrait prendre moins de 500ms
    assertPerformance(duration, 500);
  });
});
