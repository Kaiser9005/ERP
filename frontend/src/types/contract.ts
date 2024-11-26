export interface Contract {
    id: string;
    employee_id: string;
    employee_name: string;
    type: string;
    start_date: string;
    end_date?: string;
    wage: number;
    position: string;
    department: string;
    is_active: boolean;
    created_at: string;
    updated_at: string;
}

export interface ContractCreate {
    employee_id: string;
    type: string;
    start_date: string;
    end_date?: string;
    wage: number;
    position: string;
    department: string;
}

export interface ContractUpdate {
    type?: string;
    start_date?: string;
    end_date?: string;
    wage?: number;
    position?: string;
    department?: string;
    is_active?: boolean;
}

export type ContractType = 'CDI' | 'CDD' | 'Saisonnier';

export const CONTRACT_TYPES: ContractType[] = ['CDI', 'CDD', 'Saisonnier'];

export interface ContractFilters {
    type?: ContractType;
    department?: string;
    isActive?: boolean;
    employeeId?: string;
}

export interface ContractStats {
    totalContracts: number;
    activeContracts: number;
    byType: Record<ContractType, number>;
    byDepartment: Record<string, number>;
    averageWage: number;
    expiringContracts: number;
}
