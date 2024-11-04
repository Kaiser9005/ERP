import { getParametres, updateParametre, getModulesConfiguration, updateModuleConfiguration } from '../parametrage';
import { api } from '../api';

jest.mock('../api');

describe('Service Paramétrage', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('getParametres', () => {
    it('récupère les paramètres avec le type spécifié', async () => {
      const mockResponse = { data: [{ id: '1', code: 'PARAM1' }] };
      (api.get as jest.Mock).mockResolvedValue(mockResponse);

      const result = await getParametres('GENERAL');
      
      expect(api.get).toHaveBeenCalledWith('/parametrage/parametres', {
        params: { type: 'GENERAL' }
      });
      expect(result).toEqual(mockResponse.data);
    });

    it('gère les erreurs de requête', async () => {
      (api.get as jest.Mock).mockRejectedValue(new Error('Erreur API'));

      await expect(getParametres()).rejects.toThrow('Erreur API');
    });
  });

  describe('updateParametre', () => {
    it('met à jour un paramètre', async () => {
      const mockResponse = { data: { id: '1', code: 'PARAM1', valeur: 'new value' } };
      (api.put as jest.Mock).mockResolvedValue(mockResponse);

      const result = await updateParametre({ id: '1', valeur: 'new value' });
      
      expect(api.put).toHaveBeenCalledWith('/parametrage/parametres/1', {
        valeur: 'new value'
      });
      expect(result).toEqual(mockResponse.data);
    });
  });

  describe('getModulesConfiguration', () => {
    it('récupère la configuration des modules', async () => {
      const mockResponse = { data: [{ id: '1', module: 'PRODUCTION' }] };
      (api.get as jest.Mock).mockResolvedValue(mockResponse);

      const result = await getModulesConfiguration();
      
      expect(api.get).toHaveBeenCalledWith('/parametrage/modules/configuration');
      expect(result).toEqual(mockResponse.data);
    });
  });

  describe('updateModuleConfiguration', () => {
    it('met à jour la configuration d\'un module', async () => {
      const mockResponse = { data: { module: 'PRODUCTION', actif: true } };
      (api.put as jest.Mock).mockResolvedValue(mockResponse);

      const result = await updateModuleConfiguration({
        module: 'PRODUCTION',
        actif: true
      });
      
      expect(api.put).toHaveBeenCalledWith('/parametrage/modules/PRODUCTION/configuration', {
        module: 'PRODUCTION',
        actif: true
      });
      expect(result).toEqual(mockResponse.data);
    });
  });
});