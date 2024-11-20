import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import { QueryClient, QueryClientProvider } from 'react-query';
import ActivitesRecentes from '../ActivitesRecentes';

// Mock de fetch
global.fetch = jest.fn();

describe('ActivitesRecentes', () => {
  const queryClient = new QueryClient();
  const mockActivites = [
    {
      id: '1',
      type: 'PRODUCTION',
      description: 'Récolte parcelle A terminée',
      date: '2024-01-15T10:30:00Z',
      statut: 'TERMINE'
    },
    {
      id: '2',
      type: 'FINANCE',
      description: 'Paiement fournisseur en attente',
      date: '2024-01-15T09:15:00Z',
      statut: 'EN_COURS'
    },
    {
      id: '3',
      type: 'INVENTAIRE',
      description: 'Mise à jour stock engrais',
      date: '2024-01-15T08:45:00Z',
      statut: 'TERMINE'
    }
  ];

  beforeEach(() => {
    (global.fetch as jest.Mock).mockImplementation(() =>
      Promise.resolve({
        json: () => Promise.resolve(mockActivites)
      })
    );
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  it('affiche la liste des activités récentes', async () => {
    render(
      <QueryClientProvider client={queryClient}>
        <ActivitesRecentes />
      </QueryClientProvider>
    );

    // Vérifie le titre
    expect(screen.getByText('Activités Récentes')).toBeInTheDocument();

    // Vérifie les activités
    expect(await screen.findByText('Récolte parcelle A terminée')).toBeInTheDocument();
    expect(screen.getByText('Paiement fournisseur en attente')).toBeInTheDocument();
    expect(screen.getByText('Mise à jour stock engrais')).toBeInTheDocument();

    // Vérifie les types et statuts
    expect(screen.getByText('PRODUCTION')).toBeInTheDocument();
    expect(screen.getByText('FINANCE')).toBeInTheDocument();
    expect(screen.getByText('INVENTAIRE')).toBeInTheDocument();
    expect(screen.getAllByText('TERMINE')).toHaveLength(2);
    expect(screen.getByText('EN COURS')).toBeInTheDocument();
  });

  it('affiche un message quand il n\'y a pas d\'activités', async () => {
    (global.fetch as jest.Mock).mockImplementation(() =>
      Promise.resolve({
        json: () => Promise.resolve([])
      })
    );

    render(
      <QueryClientProvider client={queryClient}>
        <ActivitesRecentes />
      </QueryClientProvider>
    );

    expect(await screen.findByText('Aucune activité récente')).toBeInTheDocument();
  });

  it('affiche un message de chargement', () => {
    (global.fetch as jest.Mock).mockImplementation(() =>
      new Promise(() => {}) // Promise qui ne se résout jamais
    );

    render(
      <QueryClientProvider client={queryClient}>
        <ActivitesRecentes />
      </QueryClientProvider>
    );

    expect(screen.getByText('Chargement des activités...')).toBeInTheDocument();
  });

  it('formate correctement les dates', async () => {
    render(
      <QueryClientProvider client={queryClient}>
        <ActivitesRecentes />
      </QueryClientProvider>
    );

    // Vérifie le format de date en français
    expect(await screen.findByText(/15 janvier 2024 à 10:30/)).toBeInTheDocument();
    expect(screen.getByText(/15 janvier 2024 à 09:15/)).toBeInTheDocument();
    expect(screen.getByText(/15 janvier 2024 à 08:45/)).toBeInTheDocument();
  });
});
