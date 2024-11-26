import { AxiosError } from 'axios';
import { api } from '../config/axios';
import { Contract, ContractCreate, ContractUpdate, ContractStats } from '../types/contract';

const BASE_URL = '/hr/contracts';

export const contractService = {
    // Création d'un nouveau contrat
    async createContract(contract: ContractCreate): Promise<Contract> {
        try {
            const { data } = await api.post<Contract>(BASE_URL, contract);
            return data;
        } catch (error) {
            if (error instanceof AxiosError) {
                throw new Error(error.response?.data?.detail || 'Erreur lors de la création du contrat');
            }
            throw error;
        }
    },

    // Récupération d'un contrat par ID
    async getContract(id: string): Promise<Contract> {
        try {
            const { data } = await api.get<Contract>(`${BASE_URL}/${id}`);
            return data;
        } catch (error) {
            if (error instanceof AxiosError) {
                throw new Error(error.response?.data?.detail || 'Erreur lors de la récupération du contrat');
            }
            throw error;
        }
    },

    // Récupération des contrats d'un employé
    async getEmployeeContracts(employeeId: string): Promise<Contract[]> {
        try {
            const { data } = await api.get<Contract[]>(`${BASE_URL}/employee/${employeeId}`);
            return data;
        } catch (error) {
            if (error instanceof AxiosError) {
                throw new Error(error.response?.data?.detail || 'Erreur lors de la récupération des contrats');
            }
            throw error;
        }
    },

    // Récupération des contrats actifs
    async getActiveContracts(): Promise<Contract[]> {
        try {
            const { data } = await api.get<Contract[]>(`${BASE_URL}/active`);
            return data;
        } catch (error) {
            if (error instanceof AxiosError) {
                throw new Error(error.response?.data?.detail || 'Erreur lors de la récupération des contrats actifs');
            }
            throw error;
        }
    },

    // Mise à jour d'un contrat
    async updateContract(id: string, contract: ContractUpdate): Promise<Contract> {
        try {
            const { data } = await api.patch<Contract>(`${BASE_URL}/${id}`, contract);
            return data;
        } catch (error) {
            if (error instanceof AxiosError) {
                throw new Error(error.response?.data?.detail || 'Erreur lors de la mise à jour du contrat');
            }
            throw error;
        }
    },

    // Terminer un contrat
    async terminateContract(id: string, endDate: string): Promise<Contract> {
        try {
            const { data } = await api.post<Contract>(`${BASE_URL}/${id}/terminate`, { end_date: endDate });
            return data;
        } catch (error) {
            if (error instanceof AxiosError) {
                throw new Error(error.response?.data?.detail || 'Erreur lors de la terminaison du contrat');
            }
            throw error;
        }
    },

    // Récupération des contrats qui expirent bientôt
    async getExpiringContracts(days: number): Promise<Contract[]> {
        try {
            const { data } = await api.get<Contract[]>(`${BASE_URL}/expiring/${days}`);
            return data;
        } catch (error) {
            if (error instanceof AxiosError) {
                throw new Error(error.response?.data?.detail || 'Erreur lors de la récupération des contrats expirants');
            }
            throw error;
        }
    },

    // Calcul des statistiques des contrats
    calculateStats(contracts: Contract[]): ContractStats {
        const stats: ContractStats = {
            totalContracts: contracts.length,
            activeContracts: contracts.filter(c => c.is_active).length,
            byType: {
                CDI: 0,
                CDD: 0,
                Saisonnier: 0
            },
            byDepartment: {},
            averageWage: 0,
            expiringContracts: 0
        };

        let totalWage = 0;

        contracts.forEach(contract => {
            // Stats par type
            stats.byType[contract.type as keyof typeof stats.byType]++;

            // Stats par département
            stats.byDepartment[contract.department] = (stats.byDepartment[contract.department] || 0) + 1;

            // Calcul du salaire moyen
            totalWage += contract.wage;

            // Contrats expirants (dans les 30 jours)
            if (contract.is_active && contract.end_date) {
                const endDate = new Date(contract.end_date);
                const today = new Date();
                const diffDays = Math.ceil((endDate.getTime() - today.getTime()) / (1000 * 60 * 60 * 24));
                if (diffDays <= 30 && diffDays > 0) {
                    stats.expiringContracts++;
                }
            }
        });

        stats.averageWage = contracts.length > 0 ? totalWage / contracts.length : 0;

        return stats;
    }
};
