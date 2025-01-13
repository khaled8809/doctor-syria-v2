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
  Tooltip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  TextField,
  Box,
  Typography
} from '@mui/material';
import {
  CheckCircle,
  Cancel,
  Warning,
  Info,
  Edit,
  LocalHospital
} from '@mui/icons-material';

interface Medication {
  id: string;
  patientName: string;
  roomNumber: string;
  medicationName: string;
  dosage: string;
  frequency: string;
  nextDose: string;
  status: 'pending' | 'given' | 'missed' | 'delayed';
  instructions: string;
  notes?: string;
}

interface MedicationScheduleProps {
  medications: Medication[];
}

export const MedicationSchedule: React.FC<MedicationScheduleProps> = ({ medications }) => {
  const [selectedMed, setSelectedMed] = useState<Medication | null>(null);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [notes, setNotes] = useState('');

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'given':
        return 'success';
      case 'missed':
        return 'error';
      case 'delayed':
        return 'warning';
      default:
        return 'info';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'given':
        return <CheckCircle fontSize="small" />;
      case 'missed':
        return <Cancel fontSize="small" />;
      case 'delayed':
        return <Warning fontSize="small" />;
      default:
        return <Info fontSize="small" />;
    }
  };

  const handleMedicationEdit = (medication: Medication) => {
    setSelectedMed(medication);
    setNotes(medication.notes || '');
    setDialogOpen(true);
  };

  const handleDialogClose = () => {
    setDialogOpen(false);
    setSelectedMed(null);
    setNotes('');
  };

  const handleNotesSave = () => {
    if (selectedMed) {
      // حفظ الملاحظات
      console.log('Notes saved for medication:', selectedMed.id, notes);
    }
    handleDialogClose();
  };

  return (
    <>
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>المريض</TableCell>
              <TableCell>الغرفة</TableCell>
              <TableCell>الدواء</TableCell>
              <TableCell>الجرعة</TableCell>
              <TableCell>التكرار</TableCell>
              <TableCell>الجرعة التالية</TableCell>
              <TableCell>الحالة</TableCell>
              <TableCell>إجراءات</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {medications.map((med) => (
              <TableRow
                key={med.id}
                sx={{
                  '&:hover': {
                    backgroundColor: 'action.hover',
                  },
                }}
              >
                <TableCell>{med.patientName}</TableCell>
                <TableCell>{med.roomNumber}</TableCell>
                <TableCell>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <LocalHospital color="primary" fontSize="small" />
                    {med.medicationName}
                  </Box>
                </TableCell>
                <TableCell>{med.dosage}</TableCell>
                <TableCell>{med.frequency}</TableCell>
                <TableCell>
                  <Typography
                    color={new Date(med.nextDose) < new Date() ? 'error' : 'inherit'}
                  >
                    {med.nextDose}
                  </Typography>
                </TableCell>
                <TableCell>
                  <Chip
                    icon={getStatusIcon(med.status)}
                    label={med.status}
                    color={getStatusColor(med.status)}
                    size="small"
                  />
                </TableCell>
                <TableCell>
                  <Box sx={{ display: 'flex', gap: 1 }}>
                    <Tooltip title="تحديث الحالة">
                      <IconButton
                        size="small"
                        onClick={() => handleMedicationEdit(med)}
                      >
                        <Edit />
                      </IconButton>
                    </Tooltip>
                    <Tooltip title="تفاصيل">
                      <IconButton
                        size="small"
                        onClick={() => {
                          // عرض التفاصيل
                        }}
                      >
                        <Info />
                      </IconButton>
                    </Tooltip>
                  </Box>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      <Dialog open={dialogOpen} onClose={handleDialogClose} maxWidth="sm" fullWidth>
        <DialogTitle>
          تحديث حالة الدواء: {selectedMed?.medicationName}
        </DialogTitle>
        <DialogContent>
          <Box sx={{ mb: 2 }}>
            <Typography variant="subtitle2" gutterBottom>
              التعليمات:
            </Typography>
            <Typography variant="body2" color="text.secondary">
              {selectedMed?.instructions}
            </Typography>
          </Box>
          <TextField
            fullWidth
            multiline
            rows={4}
            label="ملاحظات"
            value={notes}
            onChange={(e) => setNotes(e.target.value)}
            margin="normal"
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleDialogClose}>إلغاء</Button>
          <Button
            variant="contained"
            color="success"
            onClick={() => {
              // تحديث حالة الدواء إلى "تم إعطاؤه"
              handleNotesSave();
            }}
          >
            تم إعطاء الدواء
          </Button>
        </DialogActions>
      </Dialog>
    </>
  );
};

export default MedicationSchedule;
