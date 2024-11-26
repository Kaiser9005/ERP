import React from 'react';
import { useQuery } from '@tanstack/react-query';
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  IconButton,
  Tooltip,
} from '@mui/material';
import { Edit as EditIcon, Delete as DeleteIcon, CheckCircle as ValidateIcon } from '@mui/icons-material';
import { format } from 'date-fns';
import { fr } from 'date-fns/locale';
import { PayrollSlip } from '../../../types/payroll';
import { payrollService } from '../../../services/payroll';

interface PayrollListProps {
  onEdit: (id: string) => void;
  onDelete: (id: string) => void;
  onValidate: (id: string) => void;
}

export const PayrollList: React.FC<PayrollListProps> = ({ onEdit, onDelete, onValidate }) => {
  const { data: payrolls, isLoading, error } = useQuery<PayrollSlip[]>({
    queryKey: ['payrolls'],
    queryFn: async () => {
      const currentDate = new Date();
      const startDate = format(new Date(currentDate.getFullYear(), currentDate.getMonth(), 1), 'yyyy-MM-dd');
      const endDate = format(new Date(currentDate.getFullYear(), currentDate.getMonth() + 1, 0), 'yyyy-MM-dd');
      
      return payrollService.getByPeriod({ start_date: startDate, end_date: endDate });
    }
  });

  if (isLoading) {
    return <div>Chargement des fiches de paie...</div>;
  }

  if (error) {
    return <div>Erreur lors du chargement des fiches de paie</div>;
  }

  const formatMoney = (amount: number) => {
    return new Intl.NumberFormat('fr-FR', { style: 'currency', currency: 'EUR' }).format(amount);
  };

  const formatDate = (date: string) => {
    return format(new Date(date), 'dd MMMM yyyy', { locale: fr });
  };

  return (
    <Paper sx={{ width: '100%', overflow: 'hidden' }}>
      <TableContainer sx={{ maxHeight: 440 }}>
        <Table stickyHeader>
          <TableHead>
            <TableRow>
              <TableCell>Période</TableCell>
              <TableCell>Heures travaillées</TableCell>
              <TableCell>Salaire brut</TableCell>
              <TableCell>Salaire net</TableCell>
              <TableCell>Statut</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {payrolls?.map((payroll) => (
              <TableRow key={payroll.id} hover>
                <TableCell>
                  {formatDate(payroll.period_start)} - {formatDate(payroll.period_end)}
                </TableCell>
                <TableCell>
                  {payroll.worked_hours}h 
                  {payroll.overtime_hours > 0 && ` (+ ${payroll.overtime_hours}h sup.)`}
                </TableCell>
                <TableCell>{formatMoney(payroll.gross_total)}</TableCell>
                <TableCell>{formatMoney(payroll.net_total)}</TableCell>
                <TableCell>
                  {payroll.is_paid ? (
                    <span style={{ color: 'green' }}>Payée le {formatDate(payroll.payment_date!)}</span>
                  ) : (
                    <span style={{ color: 'orange' }}>En attente</span>
                  )}
                </TableCell>
                <TableCell>
                  <Tooltip title="Modifier">
                    <IconButton 
                      onClick={() => onEdit(payroll.id)}
                      disabled={payroll.is_paid}
                    >
                      <EditIcon />
                    </IconButton>
                  </Tooltip>
                  <Tooltip title="Supprimer">
                    <IconButton 
                      onClick={() => onDelete(payroll.id)}
                      disabled={payroll.is_paid}
                      color="error"
                    >
                      <DeleteIcon />
                    </IconButton>
                  </Tooltip>
                  {!payroll.is_paid && (
                    <Tooltip title="Valider le paiement">
                      <IconButton 
                        onClick={() => onValidate(payroll.id)}
                        color="success"
                      >
                        <ValidateIcon />
                      </IconButton>
                    </Tooltip>
                  )}
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Paper>
  );
};
