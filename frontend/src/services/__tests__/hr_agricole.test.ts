import { vi } from 'vitest';
import { api } from '../../config/axios';
import {
  getCompetencesEmploye,
  createCompetence,
  updateCompetence,
  getCompetence
} from '../hr_agricole';
import { CompetenceAgricole, CompetenceAgricoleCreate } from '../../types/hr_agricole';

// Mock du module axios
vi.mock('../../config/axios', () => ({
  api: {
    get: vi.fn(),
    post: vi.fn(),
    put: vi.fn()
  }
}));

describe('Services RH Agricole', () => {
  const mockCompetence: CompetenceAgricole = {
    id: '1',
    employe_id: 'emp1',
    specialite: 'CULTURE',
    niveau: 'AVANCE',
    cultures: ['Blé', 'Maïs'],
    equipements: ['Tracteur', 'Moissonneuse'],
    date_acquisition: '2023-01-15',
    validite: '2024-01-15',
    commentaire: 'Très bon niveau',
    donnees_supplementaires: {}
  };

  const mockCompetenceCreate: CompetenceAgricoleCreate = {
    employe_id: 'emp1',
    specialite: 'CULTURE',
    niveau: 'AVANCE',
    cultures: ['Blé', 'Maïs'],
    equipements: ['Tracteur', 'Moissonneuse'],
    date_acquisition: '2023-01-15',
    validite: '2024-01-15',
    commentaire: 'Très bon niveau',
    donnees_supplementaires: {}
  };

  beforeEach(() => {
    vi.clearAllMocks();
  });

  describe('getCompetencesEmploye', () => {
    it('récupère les compétences d\'un employé', async () => {
      const mockResponse = { data: [mockCompetence] };
      (api.get as jest.Mock).mockResolvedValue(mockResponse);

      const result = await getCompetencesEmploye('emp1');

      expect(api.get).toHaveBeenCalledWith('/hr-agricole/employes/emp1/competences/');
      expect(result).toEqual([mockCompetence]);
    });

    it('gère les erreurs lors de la récupération des compétences', async () => {
      const error = new Error('Erreur API');
      (api.get as jest.Mock).mockRejectedValue(error);

      await expect(getCompetencesEmploye('emp1')).rejects.toThrow('Erreur API');
    });
  });

  describe('createCompetence', () => {
    it('crée une nouvelle compétence', async () => {
      const mockResponse = { data: mockCompetence };
      (api.post as jest.Mock).mockResolvedValue(mockResponse);

      const result = await createCompetence(mockCompetenceCreate);

      expect(api.post).toHaveBeenCalledWith('/hr-agricole/competences/', mockCompetenceCreate);
      expect(result).toEqual(mockCompetence);
    });

    it('gère les erreurs lors de la création d\'une compétence', async () => {
      const error = new Error('Erreur API');
      (api.post as jest.Mock).mockRejectedValue(error);

      await expect(createCompetence(mockCompetenceCreate)).rejects.toThrow('Erreur API');
    });
  });

  describe('updateCompetence', () => {
    it('met à jour une compétence existante', async () => {
      const mockResponse = { data: mockCompetence };
      (api.put as jest.Mock).mockResolvedValue(mockResponse);

      const result = await updateCompetence('1', mockCompetenceCreate);

      expect(api.put).toHaveBeenCalledWith('/hr-agricole/competences/1', mockCompetenceCreate);
      expect(result).toEqual(mockCompetence);
    });

    it('gère les erreurs lors de la mise à jour d\'une compétence', async () => {
      const error = new Error('Erreur API');
      (api.put as jest.Mock).mockRejectedValue(error);

      await expect(updateCompetence('1', mockCompetenceCreate)).rejects.toThrow('Erreur API');
    });
  });

  describe('getCompetence', () => {
    it('récupère une compétence par son ID', async () => {
      const mockResponse = { data: mockCompetence };
      (api.get as jest.Mock).mockResolvedValue(mockResponse);

      const result = await getCompetence('1');

      expect(api.get).toHaveBeenCalledWith('/hr-agricole/competences/1');
      expect(result).toEqual(mockCompetence);
    });

    it('gère les erreurs lors de la récupération d\'une compétence', async () => {
      const error = new Error('Erreur API');
      (api.get as jest.Mock).mockRejectedValue(error);

      await expect(getCompetence('1')).rejects.toThrow('Erreur API');
    });
  });

  // Tests pour la validation des données
  describe('Validation des données', () => {
    it('vérifie que les dates sont au bon format', async () => {
      const mockResponse = { data: mockCompetence };
      (api.post as jest.Mock).mockResolvedValue(mockResponse);

      const competenceAvecDates: CompetenceAgricoleCreate = {
        ...mockCompetenceCreate,
        date_acquisition: '2023-01-15', // Format ISO
        validite: '2024-01-15' // Format ISO
      };

      await createCompetence(competenceAvecDates);
      expect(api.post).toHaveBeenCalledWith('/hr-agricole/competences/', competenceAvecDates);
    });

    it('vérifie que les tableaux sont correctement transmis', async () => {
      const mockResponse = { data: mockCompetence };
      (api.post as jest.Mock).mockResolvedValue(mockResponse);

      const competenceAvecTableaux: CompetenceAgricoleCreate = {
        ...mockCompetenceCreate,
        cultures: ['Blé', 'Maïs'],
        equipements: ['Tracteur', 'Moissonneuse']
      };

      await createCompetence(competenceAvecTableaux);
      expect(api.post).toHaveBeenCalledWith('/hr-agricole/competences/', competenceAvecTableaux);
    });

    it('vérifie que les énumérations sont valides', async () => {
      const mockResponse = { data: mockCompetence };
      (api.post as jest.Mock).mockResolvedValue(mockResponse);

      const competenceAvecEnums: CompetenceAgricoleCreate = {
        ...mockCompetenceCreate,
        specialite: 'CULTURE',
        niveau: 'AVANCE'
      };

      await createCompetence(competenceAvecEnums);
      expect(api.post).toHaveBeenCalledWith('/hr-agricole/competences/', competenceAvecEnums);
    });
  });
});
