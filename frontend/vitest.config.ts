/// <reference types="vitest" />
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { resolve } from 'path';

// Configuration commune
const commonConfig = {
  globals: true,
  environment: 'jsdom',
  setupFiles: ['./src/test/setup.ts'],
  coverage: {
    provider: 'v8',
    reporter: ['text', 'json', 'html'],
    exclude: [
      'node_modules/',
      'src/test/setup.ts',
      '**/*.d.ts',
      '**/*.test.{ts,tsx}',
      '**/__mocks__/**',
    ],
  },
};

// Configuration spécifique pour les tests de composants
const componentTestConfig = {
  ...commonConfig,
  include: [
    'src/components/**/*.{test,spec}.{ts,tsx}',
    'src/pages/**/*.{test,spec}.{ts,tsx}',
  ],
  environment: 'happy-dom',
  setupFiles: [
    './src/test/setup.ts',
    './src/test/setupComponents.ts',
  ],
};

// Configuration pour les tests d'intégration
const integrationTestConfig = {
  ...commonConfig,
  include: [
    'src/services/**/*.{test,spec}.{ts,tsx}',
    'src/hooks/**/*.{test,spec}.{ts,tsx}',
  ],
  testTimeout: 10000,
  setupFiles: [
    './src/test/setup.ts',
    './src/test/setupIntegration.ts',
  ],
};

// Configuration pour les tests de performance
const performanceTestConfig = {
  ...commonConfig,
  include: ['**/*.perf.{ts,tsx}'],
  testTimeout: 30000,
  setupFiles: [
    './src/test/setup.ts',
    './src/test/setupPerformance.ts',
  ],
};

// Configuration pour les tests WebSocket
const websocketTestConfig = {
  ...commonConfig,
  include: ['**/*.ws.{test,spec}.{ts,tsx}'],
  setupFiles: [
    './src/test/setup.ts',
    './src/test/setupWebsocket.ts',
  ],
};

// Configuration pour les tests IoT
const iotTestConfig = {
  ...commonConfig,
  include: [
    'src/components/production/**/*.{test,spec}.{ts,tsx}',
    'src/services/iot/**/*.{test,spec}.{ts,tsx}',
  ],
  setupFiles: [
    './src/test/setup.ts',
    './src/test/setupIoT.ts',
  ],
};

// Configuration pour les tests Analytics
const analyticsTestConfig = {
  ...commonConfig,
  include: [
    'src/components/analytics/**/*.{test,spec}.{ts,tsx}',
    'src/services/analytics/**/*.{test,spec}.{ts,tsx}',
  ],
  setupFiles: [
    './src/test/setup.ts',
    './src/test/setupAnalytics.ts',
  ],
};

// Configuration principale
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': resolve(__dirname, './src'),
    },
  },
  test: {
    ...commonConfig,
    include: ['src/**/*.{test,spec}.{ts,tsx}'],
    globals: true,
    environment: 'jsdom',
    setupFiles: ['./src/test/setup.ts'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      exclude: [
        'node_modules/',
        'src/test/setup.ts',
        '**/*.d.ts',
        '**/*.test.{ts,tsx}',
        '**/__mocks__/**',
      ],
      lines: 80,
      functions: 80,
      branches: 75,
      statements: 80,
    },
    deps: {
      inline: [
        '@visx/visx',
        'victory',
        'plotly.js-dist',
        'nivo',
      ],
    },
  },
});
