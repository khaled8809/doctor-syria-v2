import React, { useRef } from 'react';
import { useParams } from 'react-router-dom';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Grid,
  Avatar,
  Chip,
  Button,
} from '@mui/material';
import PDFDownloadButton from '../components/common/PDFDownloadButton';
import { usePatient } from '../hooks/usePatient';
import { Patient } from '../types/patient';

const PatientDetails: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const contentRef = useRef<HTMLDivElement>(null);
  const { data: patient, isLoading, error } = usePatient(id || '');

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (error || !patient) {
    return <div>Error loading patient details</div>;
  }

  const handlePrint = () => {
    if (contentRef.current) {
      window.print();
    }
  };

  return (
    <Box sx={{ p: 3 }} ref={contentRef}>
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Box display="flex" justifyContent="space-between" alignItems="center">
            <Typography variant="h4">Patient Details</Typography>
            <Box>
              <Button
                variant="contained"
                color="primary"
                onClick={handlePrint}
                sx={{ mr: 1 }}
              >
                Print
              </Button>
              <PDFDownloadButton content={contentRef} />
            </Box>
          </Box>
        </Grid>

        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" mb={2}>
                <Avatar
                  sx={{ width: 100, height: 100, mr: 2 }}
                  src={patient.photoUrl}
                />
                <Box>
                  <Typography variant="h6">
                    {patient.firstName} {patient.lastName}
                  </Typography>
                  <Typography color="textSecondary">
                    ID: {patient.patientId}
                  </Typography>
                  <Chip
                    label={patient.status}
                    color={patient.status === 'Active' ? 'success' : 'default'}
                    size="small"
                    sx={{ mt: 1 }}
                  />
                </Box>
              </Box>

              <Typography variant="subtitle1" gutterBottom>
                Personal Information
              </Typography>
              <Grid container spacing={1}>
                <Grid item xs={6}>
                  <Typography variant="body2" color="textSecondary">
                    Age
                  </Typography>
                  <Typography variant="body1">{patient.age}</Typography>
                </Grid>
                <Grid item xs={6}>
                  <Typography variant="body2" color="textSecondary">
                    Gender
                  </Typography>
                  <Typography variant="body1">{patient.gender}</Typography>
                </Grid>
                <Grid item xs={12}>
                  <Typography variant="body2" color="textSecondary">
                    Contact
                  </Typography>
                  <Typography variant="body1">{patient.phone}</Typography>
                </Grid>
                <Grid item xs={12}>
                  <Typography variant="body2" color="textSecondary">
                    Address
                  </Typography>
                  <Typography variant="body1">{patient.address}</Typography>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={8}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Medical History
              </Typography>
              {patient.medicalHistory.map((record, index) => (
                <Box key={index} mb={2}>
                  <Typography variant="subtitle1">{record.condition}</Typography>
                  <Typography variant="body2" color="textSecondary">
                    Diagnosed: {new Date(record.diagnosedDate).toLocaleDateString()}
                  </Typography>
                  <Typography variant="body2">{record.notes}</Typography>
                </Box>
              ))}
            </CardContent>
          </Card>

          <Card sx={{ mt: 2 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Recent Visits
              </Typography>
              {patient.visits.map((visit, index) => (
                <Box key={index} mb={2}>
                  <Typography variant="subtitle1">
                    {new Date(visit.date).toLocaleDateString()}
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    Doctor: {visit.doctor}
                  </Typography>
                  <Typography variant="body2">{visit.reason}</Typography>
                  <Typography variant="body2">{visit.notes}</Typography>
                </Box>
              ))}
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default PatientDetails;
