import React from 'react';
import {
  Card,
  CardContent,
  Typography,
  Grid,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  Chip,
  Box,
  IconButton
} from '@mui/material';
import { Edit, Today } from '@mui/icons-material';
import { useQuery } from 'react-query';
import { getAttendanceOverview } from '../../services/hr';
import { format } from 'date-fns';
import { fr } from 'date-fns/locale';
import AttendanceChart from './AttendanceChart';

const AttendanceOverview: React.FC = () => {
  const { data: attendance } = useQuery('attendance-overview', getAttendanceOverview);

  const getStatusColor = (type: string) => {
    switch (type) {
      case 'PRESENT':
        return 'success';
      case 'ABSENT':
        return 'error';
      case 'RETARD':
        return 'warning';
      case 'CONGE':
        return 'info';
      default:
        return 'default';
    }
  };

  return (
    <Grid container spacing={3}>
      <Grid item xs={12} lg={8}>
        <Card>
          <CardContent>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
              <Typography variant="h6">Présences du Jour</Typography>
              <IconButton>
                <Today />
              </IconButton>
            </Box>

            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Employé</TableCell>
                  <TableCell>Département</TableCell>
                  <TableCell>Arrivée</TableCell>
                  <TableCell>Départ</TableCell>
                  <TableCell>Statut</TableCell>
                  <TableCell align="right">Actions</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {attendance?.daily.map((record) => (
                  <TableRow key={record.id}>
                    <TableCell>
                      {record.employe.prenom} {record.employe.nom}
                    </TableCell>
                    <TableCell>{record.employe.departement}</TableCell>
                    <TableCell>
                      {record.heure_arrivee ? 
                        format(new Date(record.heure_arrivee), 'HH:mm', { locale: fr }) :
                        '-'
                      }
                    </TableCell>
                    <TableCell>
                      {record.heure_depart ? 
                        format(new Date(record.heure_depart), 'HH:mm', { locale: fr }) :
                        '-'
                      }
                    </TableCell>
                    <TableCell>
                      <Chip
                        size="small"
                        label={record.type_presence}
                        color={getStatusColor(record.type_presence)}
                      />
                    </TableCell>
                    <TableCell align="right">
                      <IconButton size="small">
                        <Edit />
                      </IconButton>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        </Card>
      </Grid>

      <Grid item xs={12} lg={4}>
        <AttendanceChart data={attendance?.stats} />
      </Grid>
    </Grid>
  );
};

export default AttendanceOverview;