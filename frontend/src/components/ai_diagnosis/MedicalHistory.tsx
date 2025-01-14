import React, { useState } from 'react';
import {
  Timeline,
  TimelineItem,
  TimelineSeparator,
  TimelineConnector,
  TimelineContent,
  TimelineDot,
  TimelineOppositeContent,
} from '@mui/lab';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Chip,
  IconButton,
  Collapse,
  Button,
  useTheme,
} from '@mui/material';
import {
  MedicalServices,
  ExpandMore as ExpandMoreIcon,
  LocalHospital,
  Assignment,
  Warning,
  CheckCircle,
} from '@mui/icons-material';
import { format } from 'date-fns';
import { ar } from 'date-fns/locale';

interface MedicalRecord {
  id: number;
  date: string;
  diagnosis: {
    name: string;
    confidence: number;
    risk_level: number;
  };
  symptoms: Array<{
    name: string;
    severity: number;
  }>;
  recommendations: string;
  doctor: {
    name: string;
    specialization: string;
  };
  followUp?: {
    date: string;
    notes: string;
  };
}

interface MedicalHistoryProps {
  patientId: number;
  records: MedicalRecord[];
  onFollowUpClick: (recordId: number) => void;
}

export default function MedicalHistory({
  patientId,
  records,
  onFollowUpClick,
}: MedicalHistoryProps) {
  const theme = useTheme();
  const [expandedRecords, setExpandedRecords] = useState<number[]>([]);

  const toggleRecord = (recordId: number) => {
    setExpandedRecords((prev) =>
      prev.includes(recordId)
        ? prev.filter((id) => id !== recordId)
        : [...prev, recordId]
    );
  };

  const getRiskLevelIcon = (level: number) => {
    switch (level) {
      case 3:
        return <Warning color="error" />;
      case 2:
        return <Warning color="warning" />;
      default:
        return <CheckCircle color="success" />;
    }
  };

  const formatDate = (dateString: string) => {
    return format(new Date(dateString), 'PPP', { locale: ar });
  };

  return (
    <Box sx={{ mt: 4 }}>
      <Typography variant="h6" gutterBottom>
        السجل الطبي
      </Typography>

      <Timeline position="alternate">
        {records.map((record) => (
          <TimelineItem key={record.id}>
            <TimelineOppositeContent color="text.secondary">
              {formatDate(record.date)}
            </TimelineOppositeContent>

            <TimelineSeparator>
              <TimelineDot color={record.diagnosis.risk_level === 3 ? 'error' : 'primary'}>
                <MedicalServices />
              </TimelineDot>
              <TimelineConnector />
            </TimelineSeparator>

            <TimelineContent>
              <Card>
                <CardContent>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <Typography variant="h6" component="div">
                      {record.diagnosis.name}
                    </Typography>
                    <Box>
                      <Chip
                        icon={getRiskLevelIcon(record.diagnosis.risk_level)}
                        label={`مستوى الخطر: ${record.diagnosis.risk_level}/3`}
                        color={record.diagnosis.risk_level === 3 ? 'error' : 'default'}
                        size="small"
                        sx={{ mr: 1 }}
                      />
                      <Chip
                        label={`${record.diagnosis.confidence}% ثقة`}
                        color={record.diagnosis.confidence > 80 ? 'success' : 'warning'}
                        size="small"
                      />
                    </Box>
                  </Box>

                  <Typography color="text.secondary" sx={{ mt: 1 }}>
                    الطبيب: {record.doctor.name} - {record.doctor.specialization}
                  </Typography>

                  <IconButton
                    onClick={() => toggleRecord(record.id)}
                    sx={{
                      transform: expandedRecords.includes(record.id)
                        ? 'rotate(180deg)'
                        : 'rotate(0deg)',
                      transition: theme.transitions.create('transform'),
                    }}
                  >
                    <ExpandMoreIcon />
                  </IconButton>

                  <Collapse in={expandedRecords.includes(record.id)}>
                    <Box sx={{ mt: 2 }}>
                      <Typography variant="subtitle2" gutterBottom>
                        الأعراض:
                      </Typography>
                      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, mb: 2 }}>
                        {record.symptoms.map((symptom, index) => (
                          <Chip
                            key={index}
                            label={`${symptom.name} (${symptom.severity}/3)`}
                            size="small"
                          />
                        ))}
                      </Box>

                      <Typography variant="subtitle2" gutterBottom>
                        التوصيات:
                      </Typography>
                      <Typography variant="body2" color="text.secondary" paragraph>
                        {record.recommendations}
                      </Typography>

                      {record.followUp && (
                        <Box sx={{ mt: 2, bgcolor: 'action.hover', p: 2, borderRadius: 1 }}>
                          <Typography variant="subtitle2" gutterBottom>
                            متابعة بتاريخ {formatDate(record.followUp.date)}:
                          </Typography>
                          <Typography variant="body2" color="text.secondary">
                            {record.followUp.notes}
                          </Typography>
                        </Box>
                      )}

                      <Box sx={{ mt: 2, display: 'flex', gap: 1 }}>
                        <Button
                          startIcon={<LocalHospital />}
                          variant="outlined"
                          size="small"
                          onClick={() => onFollowUpClick(record.id)}
                        >
                          إضافة متابعة
                        </Button>
                        <Button
                          startIcon={<Assignment />}
                          variant="outlined"
                          size="small"
                        >
                          عرض التقرير الكامل
                        </Button>
                      </Box>
                    </Box>
                  </Collapse>
                </CardContent>
              </Card>
            </TimelineContent>
          </TimelineItem>
        ))}
      </Timeline>
    </Box>
  );
}
