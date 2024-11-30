/// <reference types="vitest" />
import { defineConfig } from 'vite';
import { resolve } from 'path';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': resolve(__dirname, './src'),
    },
  },
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: [
      './src/test/setup.ts',
      './src/test/setupIntegration.ts'
    ],
    include: [
      'src/services/**/*.{test,spec}.{ts,tsx}',
      'src/hooks/**/*.{test,spec}.{ts,tsx}',
      'src/store/**/*.{test,spec}.{ts,tsx}',
    ],
    exclude: [
      '**/*.perf.{ts,tsx}',
      '**/*.e2e.{ts,tsx}',
      '**/node_modules/**'
    ],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      exclude: [
        'node_modules/',
        'src/test/',
        '**/*.d.ts',
        '**/*.test.{ts,tsx}',
        '**/__mocks__/**',
      ],
    },
    testTimeout: 10000,
    hookTimeout: 10000,
  },
});
