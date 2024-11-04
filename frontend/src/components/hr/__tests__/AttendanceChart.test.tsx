import React from 'react';
import { render, screen } from '@testing-library/react';
import AttendanceChart from '../AttendanceChart';

const mockData = {
  presents: 15,
  absents: 3,
  retards: 2,
  conges: 5
};

describe('AttendanceChart', () => {
  it('affiche le titre', () => {
    render(<AttendanceChart data={mockData} />);
    
    expect(screen.getByText('Répartition des Présences')).toBeInTheDocument();
  });

  it('affiche le total', () => {
    render(<AttendanceChart data={mockData} />);
    
    expect(screen.getByText('25')).toBeInTheDocument();
    expect(screen.getByText('Total')).toBeInTheDocument();
  });

  it('affiche la légende', () => {
    render(<AttendanceChart data={mockData} />);
    
    expect(screen.getByText('Présents')).toBeInTheDocument();
    expect(screen.getByText('Absents')).toBeInTheDocument();
    expect(screen.getByText('Retards')).toBeInTheDocument();
    expect(screen.getByText('Congés')).toBeInTheDocument();
  });

  it('gère l\'absence de données', () => {
    render(<AttendanceChart />);
    
    expect(screen.getByText('0')).toBeInTheDocument();
  });
});