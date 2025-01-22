import '@testing-library/jest-dom';
import { expect, afterEach, vi } from 'vitest';
import { cleanup } from '@testing-library/react';
import matchers from '@testing-library/jest-dom/matchers';

// Étendre les matchers de Vitest avec ceux de @testing-library/jest-dom
expect.extend(matchers);

// Nettoyer après chaque test
afterEach(() => {
  cleanup();
});

// Types pour les mocks
type MediaQueryList = {
  matches: boolean;
  media: string;
  onchange: null | ((this: MediaQueryList, ev: MediaQueryListEvent) => any);
  addListener: (callback: (this: MediaQueryList, ev: MediaQueryListEvent) => any) => void;
  removeListener: (callback: (this: MediaQueryList, ev: MediaQueryListEvent) => any) => void;
  addEventListener: (type: string, listener: EventListener) => void;
  removeEventListener: (type: string, listener: EventListener) => void;
  dispatchEvent: (event: Event) => boolean;
};

// Mock des variables d'environnement
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: vi.fn().mockImplementation((query: string): MediaQueryList => ({
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

// Mock de l'API Intersection Observer
const mockIntersectionObserver = vi.fn();
mockIntersectionObserver.mockReturnValue({
  observe: () => null,
  unobserve: () => null,
  disconnect: () => null,
});
window.IntersectionObserver = mockIntersectionObserver as any;

// Mock de l'API ResizeObserver
const mockResizeObserver = vi.fn();
mockResizeObserver.mockReturnValue({
  observe: () => null,
  unobserve: () => null,
  disconnect: () => null,
});
window.ResizeObserver = mockResizeObserver as any;

// Mock des fonctions de fetch
global.fetch = vi.fn() as any;

// Types pour le localStorage et sessionStorage
interface Storage {
  getItem(key: string): string | null;
  setItem(key: string, value: string): void;
  clear(): void;
  removeItem(key: string): void;
  length: number;
  key(index: number): string | null;
}

// Mock des fonctions de localStorage
const localStorageMock: Storage = {
  getItem: vi.fn(),
  setItem: vi.fn(),
  clear: vi.fn(),
  removeItem: vi.fn(),
  length: 0,
  key: vi.fn(),
};
Object.defineProperty(window, 'localStorage', { value: localStorageMock });

// Mock des fonctions de sessionStorage
const sessionStorageMock: Storage = {
  getItem: vi.fn(),
  setItem: vi.fn(),
  clear: vi.fn(),
  removeItem: vi.fn(),
  length: 0,
  key: vi.fn(),
};
Object.defineProperty(window, 'sessionStorage', { value: sessionStorageMock });
