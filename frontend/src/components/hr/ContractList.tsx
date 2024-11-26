import React, { useState } from 'react';
import {
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    Paper,
    IconButton,
    Chip,
    Box,
    Typography,
    FormControl,
    InputLabel,
    Select,
    MenuItem,
    TextField,
    Tooltip
} from '@mui/material';
import { Edit as EditIcon, Delete as DeleteIcon } from '@mui/icons-material';
import { Contract, ContractFilters, ContractType, CONTRACT_TYPES } from '../../types/contract';
import { format } from 'date-fns';
import { fr } from 'date-fns/locale';

interface ContractListProps {
    contracts: Contract[];
    onEdit: (contract: Contract) => void;
    onDelete: (contractId: string) => void;
}

export const ContractList: React.FC<ContractListProps> = ({
    contracts,
    onEdit,
    onDelete
}) => {
    const [filters, setFilters] = useState<ContractFilters>({});

    const filteredContracts = contracts.filter(contract => {
        if (filters.type && contract.type !== filters.type) return false;
        if (filters.department && !contract.department.toLowerCase().includes(filters.department.toLowerCase())) return false;
        if (filters.isActive !== undefined && contract.is_active !== filters.isActive) return false;
        return true;
    });

    const getStatusColor = (contract: Contract) => {
        if (!contract.is_active) return 'default';
        if (contract.end_date) {
            const endDate = new Date(contract.end_date);
            const today = new Date();
            const diffDays = Math.ceil((endDate.getTime() - today.getTime()) / (1000 * 60 * 60 * 24));
            if (diffDays <= 30) return 'warning';
        }
        return 'success';
    };

    const getStatusText = (contract: Contract) => {
        if (!contract.is_active) return 'Terminé';
        if (contract.end_date) {
            const endDate = new Date(contract.end_date);
            const today = new Date();
            const diffDays = Math.ceil((endDate.getTime() - today.getTime()) / (1000 * 60 * 60 * 24));
            if (diffDays <= 30) return `Expire dans ${diffDays} jours`;
        }
        return 'Actif';
    };

    return (
        <Box>
            <Box sx={{ mb: 3, display: 'flex', gap: 2 }}>
                <FormControl size="small" sx={{ minWidth: 120 }}>
                    <InputLabel>Type</InputLabel>
                    <Select
                        value={filters.type || ''}
                        label="Type"
                        onChange={(e) => setFilters({ ...filters, type: e.target.value as ContractType })}
                    >
                        <MenuItem value="">Tous</MenuItem>
                        {CONTRACT_TYPES.map(type => (
                            <MenuItem key={type} value={type}>{type}</MenuItem>
                        ))}
                    </Select>
                </FormControl>

                <TextField
                    size="small"
                    label="Département"
                    value={filters.department || ''}
                    onChange={(e) => setFilters({ ...filters, department: e.target.value })}
                />

                <FormControl size="small" sx={{ minWidth: 120 }}>
                    <InputLabel>Statut</InputLabel>
                    <Select
                        value={filters.isActive === undefined ? '' : filters.isActive}
                        label="Statut"
                        onChange={(e) => setFilters({ ...filters, isActive: e.target.value === '' ? undefined : Boolean(e.target.value) })}
                    >
                        <MenuItem value="">Tous</MenuItem>
                        <MenuItem value="true">Actif</MenuItem>
                        <MenuItem value="false">Terminé</MenuItem>
                    </Select>
                </FormControl>
            </Box>

            <TableContainer component={Paper}>
                <Table>
                    <TableHead>
                        <TableRow>
                            <TableCell>Employé</TableCell>
                            <TableCell>Type</TableCell>
                            <TableCell>Poste</TableCell>
                            <TableCell>Département</TableCell>
                            <TableCell>Date début</TableCell>
                            <TableCell>Date fin</TableCell>
                            <TableCell>Statut</TableCell>
                            <TableCell>Actions</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {filteredContracts.map((contract) => (
                            <TableRow key={contract.id}>
                                <TableCell>{contract.employee_name}</TableCell>
                                <TableCell>{contract.type}</TableCell>
                                <TableCell>{contract.position}</TableCell>
                                <TableCell>{contract.department}</TableCell>
                                <TableCell>
                                    {format(new Date(contract.start_date), 'dd MMM yyyy', { locale: fr })}
                                </TableCell>
                                <TableCell>
                                    {contract.end_date && 
                                        format(new Date(contract.end_date), 'dd MMM yyyy', { locale: fr })}
                                </TableCell>
                                <TableCell>
                                    <Chip 
                                        label={getStatusText(contract)}
                                        color={getStatusColor(contract)}
                                        size="small"
                                    />
                                </TableCell>
                                <TableCell>
                                    <Tooltip title="Modifier">
                                        <IconButton 
                                            size="small" 
                                            onClick={() => onEdit(contract)}
                                            disabled={!contract.is_active}
                                        >
                                            <EditIcon />
                                        </IconButton>
                                    </Tooltip>
                                    <Tooltip title="Supprimer">
                                        <IconButton 
                                            size="small" 
                                            onClick={() => onDelete(contract.id)}
                                            color="error"
                                        >
                                            <DeleteIcon />
                                        </IconButton>
                                    </Tooltip>
                                </TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
                {filteredContracts.length === 0 && (
                    <Box sx={{ p: 2, textAlign: 'center' }}>
                        <Typography variant="body2" color="text.secondary">
                            Aucun contrat trouvé
                        </Typography>
                    </Box>
                )}
            </TableContainer>
        </Box>
    );
};
