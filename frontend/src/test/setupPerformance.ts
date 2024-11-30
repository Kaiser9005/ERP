import '@testing-library/jest-dom';
import { expect, afterEach, vi, beforeAll, afterAll } from 'vitest';
import { cleanup, render } from '@testing-library/react';
import matchers from '@testing-library/jest-dom/matchers';
import type { Mock } from 'vitest';

// Étend les assertions de Vitest avec les matchers de testing-library
expect.extend(matchers);

// Configuration pour les tests de performance
beforeAll(() => {
  // Désactiver les logs pendant les tests de performance
  console.log = () => {};
  console.info = () => {};
  console.warn = () => {};
  
  // Mock de matchMedia pour Material-UI
  Object.defineProperty(window, 'matchMedia', {
    writable: true,
    value: vi.fn().mockImplementation(query => ({
      matches: false,
      media: query,
      onchange: null,
      addListener: vi.fn(),
      removeListener: vi.fn(),
      addEventListener: vi.fn(),
      removeEventListener: vi.fn(),
      dispatchEvent: vi.fn(),
    })),
  });

  // Configuration des timeouts pour les tests de performance
  vi.setConfig({
    testTimeout: 30000,
    hookTimeout: 30000,
  });

  // Mock des APIs de performance
  Object.defineProperty(window, 'performance', {
    value: {
      mark: vi.fn(),
      measure: vi.fn(),
      getEntriesByName: vi.fn(),
      getEntriesByType: vi.fn(),
      clearMarks: vi.fn(),
      clearMeasures: vi.fn(),
      now: () => Date.now(),
      timeOrigin: Date.now(),
      timing: {
        navigationStart: Date.now(),
      },
    },
    configurable: true,
  });

  // Mock de requestAnimationFrame pour les animations
  const rAF: Mock = vi.fn((callback: FrameRequestCallback) => {
    return window.setTimeout(() => callback(Date.now()), 0);
  });
  window.requestAnimationFrame = rAF as unknown as typeof window.requestAnimationFrame;

  // Mock de cancelAnimationFrame
  window.cancelAnimationFrame = vi.fn((id: number) => {
    clearTimeout(id);
  });
});

// Nettoyer après chaque test
afterEach(() => {
  cleanup();
  vi.clearAllMocks();
  
  // Nettoyer la mémoire entre les tests
  if (global.gc) {
    global.gc();
  }
});

// Nettoyer après tous les tests
afterAll(() => {
  vi.restoreAllMocks();
});

// Utilitaires pour les tests de performance
export const measurePerformance = async (callback: () => Promise<void> | void) => {
  const start = Date.now();
  await callback();
  return Date.now() - start;
};

export const assertPerformance = (duration: number, threshold: number) => {
  expect(duration).toBeLessThan(threshold);
};

// Helper pour mesurer le temps de rendu des composants
export const measureRenderTime = async (component: React.ReactElement) => {
  const start = Date.now();
  const { rerender } = render(component);
  const initialRender = Date.now() - start;
  
  const rerenderStart = Date.now();
  await rerender(component);
  const rerenderTime = Date.now() - rerenderStart;
  
  return {
    initialRender,
    rerenderTime,
  };
};

// Helper pour mesurer les performances de requêtes API
export const measureApiCall = async <T>(apiCall: () => Promise<T>) => {
  const start = Date.now();
  await apiCall();
  return Date.now() - start;
};

// Helper pour mesurer l'utilisation mémoire
export const measureMemoryUsage = () => {
  if (global.gc) {
    global.gc();
  }
  return process.memoryUsage();
};
