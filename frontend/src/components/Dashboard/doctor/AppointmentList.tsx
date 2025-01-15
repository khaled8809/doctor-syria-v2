import React from 'react';
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Chip,
  IconButton,
  Tooltip,
  Box
} from '@mui/material';
import {
  CheckCircle,
  Cancel,
  AccessTime,
  Edit,
  Message
} from '@mui/icons-material';

interface Appointment {
  id: string;
  patientName: string;
  time: string;
  type: string;
  status: 'pending' | 'completed' | 'cancelled';
  notes?: string;
}

interface AppointmentListProps {
  appointments: Appointment[];
  onAppointmentUpdate: (id: string, status: string) => void;
}

export const AppointmentList: React.FC<AppointmentListProps> = ({
  appointments,
  onAppointmentUpdate
}) => {
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'success';
      case 'cancelled':
        return 'error';
      default:
        return 'warning';
    }
  };

  const getStatusLabel = (status: string) => {
    switch (status) {
      case 'completed':
        return 'مكتمل';
      case 'cancelled':
        return 'ملغي';
      default:
        return 'قيد الانتظار';
    }
  };

  return (
    <TableContainer component={Paper}>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>المريض</TableCell>
            <TableCell>الوقت</TableCell>
            <TableCell>النوع</TableCell>
            <TableCell>الحالة</TableCell>
            <TableCell>إجراءات</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {appointments.map((appointment) => (
            <TableRow key={appointment.id}>
              <TableCell>{appointment.patientName}</TableCell>
              <TableCell>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                  <AccessTime fontSize="small" />
                  {appointment.time}
                </Box>
              </TableCell>
              <TableCell>{appointment.type}</TableCell>
              <TableCell>
                <Chip
                  label={getStatusLabel(appointment.status)}
                  color={getStatusColor(appointment.status) as any}
                  size="small"
                />
              </TableCell>
              <TableCell>
                <Box sx={{ display: 'flex', gap: 1 }}>
                  <Tooltip title="اكتمال">
                    <IconButton
                      size="small"
                      color="success"
                      onClick={() => onAppointmentUpdate(appointment.id, 'completed')}
                    >
                      <CheckCircle />
                    </IconButton>
                  </Tooltip>
                  <Tooltip title="إلغاء">
                    <IconButton
                      size="small"
                      color="error"
                      onClick={() => onAppointmentUpdate(appointment.id, 'cancelled')}
                    >
                      <Cancel />
                    </IconButton>
                  </Tooltip>
                  <Tooltip title="تعديل">
                    <IconButton size="small">
                      <Edit />
                    </IconButton>
                  </Tooltip>
                  <Tooltip title="رسالة">
                    <IconButton size="small">
                      <Message />
                    </IconButton>
                  </Tooltip>
                </Box>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

export default AppointmentList;
