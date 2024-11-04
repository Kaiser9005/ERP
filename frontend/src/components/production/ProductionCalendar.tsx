import React from 'react';
import {
  Card,
  CardContent,
  Typography,
  Box
} from '@mui/material';
import { Calendar, dateFnsLocalizer } from 'react-big-calendar';
import format from 'date-fns/format';
import parse from 'date-fns/parse';
import startOfWeek from 'date-fns/startOfWeek';
import getDay from 'date-fns/getDay';
import fr from 'date-fns/locale/fr';
import { useQuery } from 'react-query';
import { getProductionEvents } from '../../services/production';
import 'react-big-calendar/lib/css/react-big-calendar.css';

const locales = {
  'fr': fr,
};

const localizer = dateFnsLocalizer({
  format,
  parse,
  startOfWeek,
  getDay,
  locales,
});

const ProductionCalendar: React.FC = () => {
  const { data: events, isLoading } = useQuery('production-events', getProductionEvents);

  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Calendrier de Production
        </Typography>
        <Box sx={{ height: 600 }}>
          <Calendar
            localizer={localizer}
            events={events || []}
            startAccessor="start"
            endAccessor="end"
            style={{ height: '100%' }}
            views={['month', 'week', 'day']}
            messages={{
              next: "Suivant",
              previous: "Précédent",
              today: "Aujourd'hui",
              month: "Mois",
              week: "Semaine",
              day: "Jour"
            }}
          />
        </Box>
      </CardContent>
    </Card>
  );
};

export default ProductionCalendar;