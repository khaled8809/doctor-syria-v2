import React, { useState, useRef, useEffect } from 'react';
import {
  Box,
  Paper,
  Typography,
  Button,
  TextField,
  Alert,
  CircularProgress,
  Card,
  CardContent,
  Grid,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  IconButton,
} from '@mui/material';
import {
  CameraAlt as CameraIcon,
  QrCode as QrCodeIcon,
  Print as PrintIcon,
  Close as CloseIcon,
} from '@mui/icons-material';
import { useSnackbar } from 'notistack';
import { useMutation, useQueryClient } from 'react-query';
import axios from 'axios';
import Quagga from 'quagga';

interface Patient {
  id: number;
  national_id: string;
  name: string;
  date_of_birth: string;
  gender: string;
  nationality: string;
}

const BarcodeRegistration = () => {
  const [scanning, setScanning] = useState(false);
  const [manualInput, setManualInput] = useState('');
  const [scannerInitialized, setScannerInitialized] = useState(false);
  const [previewDialogOpen, setPreviewDialogOpen] = useState(false);
  const [registeredPatient, setRegisteredPatient] = useState<Patient | null>(null);

  const scannerRef = useRef<HTMLDivElement>(null);
  const { enqueueSnackbar } = useSnackbar();
  const queryClient = useQueryClient();

  // Register patient mutation
  const registerPatientMutation = useMutation(
    (data: { barcode_data: string }) =>
      axios.post('/api/patients/register-from-barcode/', data),
    {
      onSuccess: (response) => {
        setRegisteredPatient(response.data);
        enqueueSnackbar('Patient registered successfully', { variant: 'success' });
        setScanning(false);
        stopScanner();
      },
      onError: (error: any) => {
        enqueueSnackbar(
          error.response?.data?.message || 'Error registering patient',
          { variant: 'error' }
        );
      },
    }
  );

  // Print patient card mutation
  const printCardMutation = useMutation(
    (patientId: number) =>
      axios.get(`/api/patients/${patientId}/card/`, {
        responseType: 'blob',
      }),
    {
      onSuccess: (response) => {
        // Create blob link to download
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', 'patient-card.pdf');
        document.body.appendChild(link);
        link.click();
        link.remove();
      },
      onError: (error: any) => {
        enqueueSnackbar('Error printing patient card', { variant: 'error' });
      },
    }
  );

  const initializeScanner = () => {
    if (!scannerRef.current) return;

    Quagga.init(
      {
        inputStream: {
          name: 'Live',
          type: 'LiveStream',
          target: scannerRef.current,
          constraints: {
            facingMode: 'environment',
          },
        },
        decoder: {
          readers: ['code_128_reader', 'ean_reader', 'ean_8_reader', 'code_39_reader'],
        },
      },
      (err) => {
        if (err) {
          enqueueSnackbar('Error initializing scanner', { variant: 'error' });
          return;
        }
        setScannerInitialized(true);
        Quagga.start();
      }
    );

    Quagga.onDetected((result) => {
      if (result.codeResult.code) {
        handleBarcodeDetected(result.codeResult.code);
      }
    });
  };

  const stopScanner = () => {
    if (scannerInitialized) {
      Quagga.stop();
      setScannerInitialized(false);
    }
  };

  const handleStartScanning = () => {
    setScanning(true);
    initializeScanner();
  };

  const handleStopScanning = () => {
    setScanning(false);
    stopScanner();
  };

  const handleBarcodeDetected = (barcodeData: string) => {
    registerPatientMutation.mutate({ barcode_data: barcodeData });
  };

  const handleManualSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (manualInput) {
      registerPatientMutation.mutate({ barcode_data: manualInput });
    }
  };

  const handlePrintCard = () => {
    if (registeredPatient) {
      printCardMutation.mutate(registeredPatient.id);
    }
  };

  useEffect(() => {
    return () => {
      stopScanner();
    };
  }, []);

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h5" sx={{ mb: 3 }}>
        Patient Registration via Barcode
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3, mb: 3 }}>
            <Typography variant="h6" gutterBottom>
              Scan National ID
            </Typography>

            {scanning ? (
              <Box sx={{ position: 'relative', mb: 2 }}>
                <div
                  ref={scannerRef}
                  style={{
                    position: 'relative',
                    width: '100%',
                    height: '300px',
                  }}
                />
                <Button
                  variant="contained"
                  color="secondary"
                  onClick={handleStopScanning}
                  sx={{ mt: 2 }}
                >
                  Stop Scanning
                </Button>
              </Box>
            ) : (
              <Button
                variant="contained"
                startIcon={<CameraIcon />}
                onClick={handleStartScanning}
                sx={{ mb: 2 }}
              >
                Start Scanning
              </Button>
            )}

            <Typography variant="subtitle1" sx={{ mt: 3, mb: 2 }}>
              Or Enter ID Manually
            </Typography>

            <form onSubmit={handleManualSubmit}>
              <TextField
                fullWidth
                label="National ID"
                value={manualInput}
                onChange={(e) => setManualInput(e.target.value)}
                sx={{ mb: 2 }}
              />
              <Button
                type="submit"
                variant="contained"
                disabled={!manualInput || registerPatientMutation.isLoading}
              >
                Register
              </Button>
            </form>
          </Paper>
        </Grid>

        <Grid item xs={12} md={6}>
          {registeredPatient && (
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Registered Patient
                </Typography>
                <Grid container spacing={2}>
                  <Grid item xs={6}>
                    <Typography color="textSecondary">Name</Typography>
                    <Typography variant="body1">{registeredPatient.name}</Typography>
                  </Grid>
                  <Grid item xs={6}>
                    <Typography color="textSecondary">National ID</Typography>
                    <Typography variant="body1">
                      {registeredPatient.national_id}
                    </Typography>
                  </Grid>
                  <Grid item xs={6}>
                    <Typography color="textSecondary">Date of Birth</Typography>
                    <Typography variant="body1">
                      {registeredPatient.date_of_birth}
                    </Typography>
                  </Grid>
                  <Grid item xs={6}>
                    <Typography color="textSecondary">Gender</Typography>
                    <Typography variant="body1">{registeredPatient.gender}</Typography>
                  </Grid>
                  <Grid item xs={12}>
                    <Typography color="textSecondary">Nationality</Typography>
                    <Typography variant="body1">
                      {registeredPatient.nationality}
                    </Typography>
                  </Grid>
                </Grid>

                <Box sx={{ mt: 2, display: 'flex', gap: 1 }}>
                  <Button
                    variant="contained"
                    startIcon={<PrintIcon />}
                    onClick={handlePrintCard}
                    disabled={printCardMutation.isLoading}
                  >
                    Print Patient Card
                  </Button>
                  <Button
                    variant="outlined"
                    startIcon={<QrCodeIcon />}
                    onClick={() => setPreviewDialogOpen(true)}
                  >
                    Preview Card
                  </Button>
                </Box>
              </CardContent>
            </Card>
          )}
        </Grid>
      </Grid>

      {/* Preview Dialog */}
      <Dialog
        open={previewDialogOpen}
        onClose={() => setPreviewDialogOpen(false)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>
          Patient Card Preview
          <IconButton
            onClick={() => setPreviewDialogOpen(false)}
            sx={{ position: 'absolute', right: 8, top: 8 }}
          >
            <CloseIcon />
          </IconButton>
        </DialogTitle>
        <DialogContent>
          {registeredPatient && (
            <Box sx={{ p: 2 }}>
              <img
                src={`/api/patients/${registeredPatient.id}/card-preview/`}
                alt="Patient Card"
                style={{ width: '100%', height: 'auto' }}
              />
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setPreviewDialogOpen(false)}>Close</Button>
          <Button
            variant="contained"
            startIcon={<PrintIcon />}
            onClick={handlePrintCard}
          >
            Print Card
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default BarcodeRegistration;
