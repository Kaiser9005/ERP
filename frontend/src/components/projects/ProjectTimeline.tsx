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
import { getProjectTimeline } from '../../services/projects';
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

const ProjectTimeline: React.FC = () => {
  const { data: events } = useQuery('project-timeline', getProjectTimeline);

  const getEventStyle = (event: any) => {
    switch (event.type) {
      case 'PROJECT_START':
        return { backgroundColor: '#4CAF50' };
      case 'PROJECT_END':
        return { backgroundColor: '#F44336' };
      case 'MILESTONE':
        return { backgroundColor: '#2196F3' };
      default:
        return { backgroundColor: '#9E9E9E' };
    }
  };

  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Timeline des Projets
        </Typography>
        <Box sx={{ height: 400 }}>
          <Calendar
            localizer={localizer}
            events={events || []}
            startAccessor="start"
            endAccessor="end"
            eventPropGetter={(event) => ({
              style: getEventStyle(event)
            })}
            messages={{
              today: "Aujourd'hui",
              previous: "Précédent",
              next: "Suivant",
              month: "Mois",
              week: "Semaine",
              day: "Jour",
              agenda: "Agenda",
              date: "Date",
              time: "Heure",
              event: "Événement",
              noEventsInRange: "Aucun événement dans cette période"
            }}
          />
        </Box>
      </CardContent>
    </Card>
  );
};

export default ProjectTimeline;