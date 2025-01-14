import { useState } from 'react';
import {
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  Button,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  MenuItem,
  FormControl,
  InputLabel,
  Select,
  Paper,
  Chip,
} from '@mui/material';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Event as EventIcon,
  Person as PersonIcon,
  LocalHospital as HospitalIcon,
  NavigateBefore,
  NavigateNext,
} from '@mui/icons-material';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import axios from 'axios';
import {
  Calendar,
  Views,
  momentLocalizer,
} from 'react-big-calendar';
import moment from 'moment';
import 'react-big-calendar/lib/css/react-big-calendar.css';

const localizer = momentLocalizer(moment);

const eventTypes = [
  { value: 'APPOINTMENT', label: 'Patient Appointment' },
  { value: 'SURGERY', label: 'Surgery' },
  { value: 'MAINTENANCE', label: 'Equipment Maintenance' },
  { value: 'MEETING', label: 'Staff Meeting' },
  { value: 'OTHER', label: 'Other' },
];

interface ScheduleEvent {
  id: number;
  title: string;
  start: Date;
  end: Date;
  type: string;
  resourceId?: number;
  description?: string;
  status: string;
}

export default function Schedule() {
  const [openDialog, setOpenDialog] = useState(false);
  const [selectedEvent, setSelectedEvent] = useState<ScheduleEvent | null>(null);
  const [view, setView] = useState(Views.WEEK);
  const [date, setDate] = useState(new Date());
  const queryClient = useQueryClient();

  const { data: events, isLoading } = useQuery('schedule-events', () =>
    axios.get('/api/schedule/').then((res) =>
      res.data.map((event: any) => ({
        ...event,
        start: new Date(event.start),
        end: new Date(event.end),
      }))
    )
  );

  const { data: resources } = useQuery('resources', () =>
    axios.get('/api/resources/').then((res) => res.data)
  );

  const addEventMutation = useMutation(
    (newEvent: Partial<ScheduleEvent>) =>
      axios.post('/api/schedule/', newEvent),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('schedule-events');
        setOpenDialog(false);
      },
    }
  );

  const updateEventMutation = useMutation(
    (updatedEvent: Partial<ScheduleEvent>) =>
      axios.put(`/api/schedule/${selectedEvent?.id}/`, updatedEvent),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('schedule-events');
        setOpenDialog(false);
      },
    }
  );

  const handleAddEvent = () => {
    setSelectedEvent(null);
    setOpenDialog(true);
  };

  const handleEventSelect = (event: ScheduleEvent) => {
    setSelectedEvent(event);
    setOpenDialog(true);
  };

  const handleSubmit = (event: React.FormEvent) => {
    event.preventDefault();
    const formData = new FormData(event.target as HTMLFormElement);
    const eventData = Object.fromEntries(formData.entries());

    const processedData = {
      ...eventData,
      start: new Date(eventData.start as string),
      end: new Date(eventData.end as string),
    };

    if (selectedEvent) {
      updateEventMutation.mutate(processedData);
    } else {
      addEventMutation.mutate(processedData);
    }
  };

  const eventStyleGetter = (event: ScheduleEvent) => {
    let backgroundColor = '#2196f3';
    switch (event.type) {
      case 'APPOINTMENT':
        backgroundColor = '#4caf50';
        break;
      case 'SURGERY':
        backgroundColor = '#f44336';
        break;
      case 'MAINTENANCE':
        backgroundColor = '#ff9800';
        break;
      case 'MEETING':
        backgroundColor = '#9c27b0';
        break;
    }

    return {
      style: {
        backgroundColor,
        borderRadius: '4px',
      },
    };
  };

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4">Schedule</Typography>
        <Box>
          <Button
            variant="outlined"
            startIcon={<NavigateBefore />}
            onClick={() => setDate(moment(date).subtract(1, view).toDate())}
            sx={{ mr: 1 }}
          >
            Previous
          </Button>
          <Button
            variant="outlined"
            endIcon={<NavigateNext />}
            onClick={() => setDate(moment(date).add(1, view).toDate())}
            sx={{ mr: 2 }}
          >
            Next
          </Button>
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            onClick={handleAddEvent}
          >
            Add Event
          </Button>
        </Box>
      </Box>

      <Card>
        <CardContent>
          <Box sx={{ height: 'calc(100vh - 250px)' }}>
            <Calendar
              localizer={localizer}
              events={events || []}
              startAccessor="start"
              endAccessor="end"
              style={{ height: '100%' }}
              onSelectEvent={handleEventSelect}
              onNavigate={setDate}
              date={date}
              view={view}
              onView={setView as any}
              eventPropGetter={eventStyleGetter}
              views={['month', 'week', 'day', 'agenda']}
              tooltipAccessor={(event: ScheduleEvent) => event.description}
              resourceIdAccessor="resourceId"
              resources={resources}
            />
          </Box>
        </CardContent>
      </Card>

      <Dialog open={openDialog} onClose={() => setOpenDialog(false)} maxWidth="md" fullWidth>
        <form onSubmit={handleSubmit}>
          <DialogTitle>
            {selectedEvent ? 'Edit Event' : 'Add New Event'}
          </DialogTitle>
          <DialogContent>
            <Grid container spacing={2} sx={{ mt: 1 }}>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="Title"
                  name="title"
                  defaultValue={selectedEvent?.title}
                  required
                />
              </Grid>
              <Grid item xs={12}>
                <FormControl fullWidth required>
                  <InputLabel>Event Type</InputLabel>
                  <Select
                    name="type"
                    defaultValue={selectedEvent?.type || ''}
                  >
                    {eventTypes.map((type) => (
                      <MenuItem key={type.value} value={type.value}>
                        {type.label}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Start Time"
                  type="datetime-local"
                  name="start"
                  defaultValue={
                    selectedEvent
                      ? moment(selectedEvent.start).format('YYYY-MM-DDTHH:mm')
                      : moment().format('YYYY-MM-DDTHH:mm')
                  }
                  InputLabelProps={{ shrink: true }}
                  required
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="End Time"
                  type="datetime-local"
                  name="end"
                  defaultValue={
                    selectedEvent
                      ? moment(selectedEvent.end).format('YYYY-MM-DDTHH:mm')
                      : moment().add(1, 'hour').format('YYYY-MM-DDTHH:mm')
                  }
                  InputLabelProps={{ shrink: true }}
                  required
                />
              </Grid>
              <Grid item xs={12}>
                <FormControl fullWidth>
                  <InputLabel>Resource</InputLabel>
                  <Select
                    name="resourceId"
                    defaultValue={selectedEvent?.resourceId || ''}
                  >
                    {resources?.map((resource: any) => (
                      <MenuItem key={resource.id} value={resource.id}>
                        {resource.name}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="Description"
                  name="description"
                  multiline
                  rows={4}
                  defaultValue={selectedEvent?.description}
                />
              </Grid>
            </Grid>
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setOpenDialog(false)}>Cancel</Button>
            <Button
              type="submit"
              variant="contained"
              startIcon={selectedEvent ? <EditIcon /> : <AddIcon />}
            >
              {selectedEvent ? 'Update' : 'Add'} Event
            </Button>
          </DialogActions>
        </form>
      </Dialog>
    </Box>
  );
}
