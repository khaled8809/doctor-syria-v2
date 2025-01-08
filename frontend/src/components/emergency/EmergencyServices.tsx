import React, { useState, useEffect } from 'react';
import {
  Box,
  Container,
  Grid,
  Paper,
  Typography,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  IconButton,
  Alert,
  CircularProgress,
  Card,
  CardContent,
  Chip,
} from '@mui/material';
import {
  LocalHospital,
  Ambulance,
  VideoCall,
  MedicalServices,
  LocationOn,
  Phone,
  Navigation,
} from '@mui/icons-material';
import { useTranslation } from 'react-i18next';
import { GoogleMap, LoadScript, Marker } from '@react-google-maps/api';

interface Hospital {
  id: string;
  name: string;
  location: {
    lat: number;
    lng: number;
  };
  distance: number;
  emergencyAvailable: boolean;
  waitingTime: number;
  phoneNumber: string;
}

interface EmergencyContact {
  id: string;
  name: string;
  relation: string;
  phoneNumber: string;
}

const EmergencyServices: React.FC = () => {
  const { t } = useTranslation();
  const [userLocation, setUserLocation] = useState<{ lat: number; lng: number } | null>(null);
  const [nearbyHospitals, setNearbyHospitals] = useState<Hospital[]>([]);
  const [selectedHospital, setSelectedHospital] = useState<Hospital | null>(null);
  const [emergencyContacts, setEmergencyContacts] = useState<EmergencyContact[]>([]);
  const [showVideoCall, setShowVideoCall] = useState(false);
  const [loading, setLoading] = useState(false);
  const [emergencyRequested, setEmergencyRequested] = useState(false);

  useEffect(() => {
    // Get user's location
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          setUserLocation({
            lat: position.coords.latitude,
            lng: position.coords.longitude,
          });
          fetchNearbyHospitals(position.coords.latitude, position.coords.longitude);
        },
        (error) => {
          console.error('Error getting location:', error);
        }
      );
    }

    // Load emergency contacts
    const savedContacts = localStorage.getItem('emergencyContacts');
    if (savedContacts) {
      setEmergencyContacts(JSON.parse(savedContacts));
    }
  }, []);

  const fetchNearbyHospitals = async (lat: number, lng: number) => {
    // This would be replaced with actual API call to backend
    const mockHospitals: Hospital[] = [
      {
        id: '1',
        name: 'مستشفى دمشق التخصصي',
        location: { lat: lat + 0.01, lng: lng + 0.01 },
        distance: 1.2,
        emergencyAvailable: true,
        waitingTime: 15,
        phoneNumber: '+963-11-1234567',
      },
      {
        id: '2',
        name: 'مستشفى الأسد الجامعي',
        location: { lat: lat - 0.01, lng: lng - 0.01 },
        distance: 2.5,
        emergencyAvailable: true,
        waitingTime: 30,
        phoneNumber: '+963-11-7654321',
      },
    ];
    setNearbyHospitals(mockHospitals);
  };

  const requestAmbulance = async (hospital: Hospital) => {
    setLoading(true);
    try {
      // This would be replaced with actual API call
      await new Promise(resolve => setTimeout(resolve, 2000));
      setEmergencyRequested(true);
      setSelectedHospital(hospital);
    } catch (error) {
      console.error('Error requesting ambulance:', error);
    } finally {
      setLoading(false);
    }
  };

  const startEmergencyVideoCall = () => {
    setShowVideoCall(true);
    // Implement video call functionality
  };

  const renderMap = () => {
    if (!userLocation) return null;

    return (
      <LoadScript googleMapsApiKey="YOUR_GOOGLE_MAPS_API_KEY">
        <GoogleMap
          center={userLocation}
          zoom={13}
          mapContainerStyle={{ width: '100%', height: '400px' }}
        >
          {/* User Location Marker */}
          <Marker
            position={userLocation}
            icon={{
              url: '/assets/images/user-location.png',
              scaledSize: new window.google.maps.Size(30, 30),
            }}
          />

          {/* Hospital Markers */}
          {nearbyHospitals.map(hospital => (
            <Marker
              key={hospital.id}
              position={hospital.location}
              onClick={() => setSelectedHospital(hospital)}
              icon={{
                url: '/assets/images/hospital-marker.png',
                scaledSize: new window.google.maps.Size(30, 30),
              }}
            />
          ))}
        </GoogleMap>
      </LoadScript>
    );
  };

  return (
    <Container maxWidth="lg">
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" gutterBottom>
          {t('emergency.title')}
        </Typography>
        
        {/* Emergency Actions */}
        <Grid container spacing={3} sx={{ mb: 4 }}>
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Box sx={{ textAlign: 'center' }}>
                  <IconButton
                    color="error"
                    size="large"
                    onClick={() => requestAmbulance(nearbyHospitals[0])}
                    disabled={loading || emergencyRequested}
                    sx={{ mb: 2 }}
                  >
                    <Ambulance sx={{ fontSize: 48 }} />
                  </IconButton>
                  <Typography variant="h6" gutterBottom>
                    {t('emergency.requestAmbulance')}
                  </Typography>
                  {loading && <CircularProgress size={24} sx={{ mt: 1 }} />}
                  {emergencyRequested && (
                    <Alert severity="success" sx={{ mt: 2 }}>
                      {t('emergency.ambulanceRequested')}
                    </Alert>
                  )}
                </Box>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Box sx={{ textAlign: 'center' }}>
                  <IconButton
                    color="primary"
                    size="large"
                    onClick={startEmergencyVideoCall}
                    sx={{ mb: 2 }}
                  >
                    <VideoCall sx={{ fontSize: 48 }} />
                  </IconButton>
                  <Typography variant="h6" gutterBottom>
                    {t('emergency.videoCall')}
                  </Typography>
                </Box>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Box sx={{ textAlign: 'center' }}>
                  <IconButton
                    color="primary"
                    size="large"
                    sx={{ mb: 2 }}
                  >
                    <MedicalServices sx={{ fontSize: 48 }} />
                  </IconButton>
                  <Typography variant="h6" gutterBottom>
                    {t('emergency.firstAid')}
                  </Typography>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        </Grid>

        {/* Map and Hospitals List */}
        <Grid container spacing={3}>
          <Grid item xs={12} md={8}>
            <Paper sx={{ p: 2 }}>
              <Typography variant="h6" gutterBottom>
                {t('emergency.nearbyHospitals')}
              </Typography>
              {renderMap()}
            </Paper>
          </Grid>

          <Grid item xs={12} md={4}>
            <Paper sx={{ p: 2 }}>
              <Typography variant="h6" gutterBottom>
                {t('emergency.hospitalsList')}
              </Typography>
              <List>
                {nearbyHospitals.map(hospital => (
                  <ListItem
                    key={hospital.id}
                    sx={{
                      border: 1,
                      borderColor: 'divider',
                      borderRadius: 1,
                      mb: 1,
                    }}
                  >
                    <ListItemIcon>
                      <LocalHospital />
                    </ListItemIcon>
                    <ListItemText
                      primary={hospital.name}
                      secondary={
                        <React.Fragment>
                          <Box sx={{ mb: 1 }}>
                            <Chip
                              size="small"
                              icon={<LocationOn />}
                              label={`${hospital.distance} km`}
                              sx={{ mr: 1 }}
                            />
                            <Chip
                              size="small"
                              icon={<AccessTime />}
                              label={`${hospital.waitingTime} min`}
                            />
                          </Box>
                          <Button
                            variant="outlined"
                            size="small"
                            startIcon={<Phone />}
                            href={`tel:${hospital.phoneNumber}`}
                          >
                            {hospital.phoneNumber}
                          </Button>
                        </React.Fragment>
                      }
                    />
                    <Button
                      variant="contained"
                      color="primary"
                      startIcon={<Navigation />}
                      onClick={() => {
                        window.open(
                          `https://www.google.com/maps/dir/?api=1&destination=${hospital.location.lat},${hospital.location.lng}`,
                          '_blank'
                        );
                      }}
                    >
                      {t('emergency.directions')}
                    </Button>
                  </ListItem>
                ))}
              </List>
            </Paper>
          </Grid>
        </Grid>
      </Box>

      {/* Video Call Dialog */}
      <Dialog
        open={showVideoCall}
        onClose={() => setShowVideoCall(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>{t('emergency.videoCall')}</DialogTitle>
        <DialogContent>
          {/* Video call component would go here */}
          <Box sx={{ height: 400, bgcolor: 'grey.200', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <Typography>{t('emergency.connectingToDoctor')}</Typography>
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setShowVideoCall(false)} color="error">
            {t('common.endCall')}
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
};

export default EmergencyServices;
