import { useState } from 'react';
import {
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  Button,
  IconButton,
  Avatar,
  Chip,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  MenuItem,
  FormControl,
  InputLabel,
  Select,
  Tabs,
  Tab,
} from '@mui/material';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Event as EventIcon,
  Person as PersonIcon,
  LocalHospital as HospitalIcon,
  Inventory as InventoryIcon,
} from '@mui/icons-material';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import axios from 'axios';

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;
  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      {...other}
    >
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );
}

const resourceTypes = {
  STAFF: [
    { value: 'DOCTOR', label: 'Doctor' },
    { value: 'NURSE', label: 'Nurse' },
    { value: 'TECHNICIAN', label: 'Technician' },
    { value: 'ADMIN', label: 'Administrative' },
  ],
  EQUIPMENT: [
    { value: 'MEDICAL', label: 'Medical Equipment' },
    { value: 'SURGICAL', label: 'Surgical Equipment' },
    { value: 'LAB', label: 'Laboratory Equipment' },
    { value: 'OTHER', label: 'Other Equipment' },
  ],
  INVENTORY: [
    { value: 'MEDICINE', label: 'Medicine' },
    { value: 'SUPPLIES', label: 'Medical Supplies' },
    { value: 'CONSUMABLES', label: 'Consumables' },
    { value: 'OTHER', label: 'Other Items' },
  ],
};

export default function Resources() {
  const [tabValue, setTabValue] = useState(0);
  const [openDialog, setOpenDialog] = useState(false);
  const [selectedResource, setSelectedResource] = useState<any>(null);
  const queryClient = useQueryClient();

  const { data: resources, isLoading } = useQuery('resources', () =>
    axios.get('/api/resources/').then((res) => res.data)
  );

  const addResourceMutation = useMutation(
    (newResource: any) => axios.post('/api/resources/', newResource),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('resources');
        setOpenDialog(false);
      },
    }
  );

  const updateResourceMutation = useMutation(
    (updatedResource: any) =>
      axios.put(`/api/resources/${selectedResource?.id}/`, updatedResource),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('resources');
        setOpenDialog(false);
      },
    }
  );

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  const handleAddResource = () => {
    setSelectedResource(null);
    setOpenDialog(true);
  };

  const handleEditResource = (resource: any) => {
    setSelectedResource(resource);
    setOpenDialog(true);
  };

  const handleSubmit = (event: React.FormEvent) => {
    event.preventDefault();
    const formData = new FormData(event.target as HTMLFormElement);
    const resourceData = Object.fromEntries(formData.entries());

    if (selectedResource) {
      updateResourceMutation.mutate(resourceData);
    } else {
      addResourceMutation.mutate(resourceData);
    }
  };

  const getResourceIcon = (type: string) => {
    switch (type) {
      case 'STAFF':
        return <PersonIcon />;
      case 'EQUIPMENT':
        return <HospitalIcon />;
      case 'INVENTORY':
        return <InventoryIcon />;
      default:
        return null;
    }
  };

  const getAvailabilityChip = (availability: number) => {
    let color: 'success' | 'warning' | 'error' = 'success';
    if (availability < 30) {
      color = 'error';
    } else if (availability < 70) {
      color = 'warning';
    }
    return <Chip label={`${availability}% Available`} color={color} size="small" />;
  };

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4">Resources</Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={handleAddResource}
        >
          Add Resource
        </Button>
      </Box>

      <Card>
        <CardContent>
          <Tabs value={tabValue} onChange={handleTabChange}>
            <Tab icon={<PersonIcon />} label="Staff" />
            <Tab icon={<HospitalIcon />} label="Equipment" />
            <Tab icon={<InventoryIcon />} label="Inventory" />
          </Tabs>

          <TabPanel value={tabValue} index={0}>
            <TableContainer component={Paper}>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Name</TableCell>
                    <TableCell>Role</TableCell>
                    <TableCell>Department</TableCell>
                    <TableCell>Schedule</TableCell>
                    <TableCell>Status</TableCell>
                    <TableCell>Actions</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {resources?.staff?.map((resource: any) => (
                    <TableRow key={resource.id}>
                      <TableCell>
                        <Box display="flex" alignItems="center" gap={1}>
                          <Avatar>{resource.name[0]}</Avatar>
                          {resource.name}
                        </Box>
                      </TableCell>
                      <TableCell>{resource.role}</TableCell>
                      <TableCell>{resource.department}</TableCell>
                      <TableCell>
                        <IconButton size="small">
                          <EventIcon />
                        </IconButton>
                      </TableCell>
                      <TableCell>{getAvailabilityChip(resource.availability)}</TableCell>
                      <TableCell>
                        <IconButton
                          size="small"
                          onClick={() => handleEditResource(resource)}
                        >
                          <EditIcon />
                        </IconButton>
                        <IconButton size="small">
                          <DeleteIcon />
                        </IconButton>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </TabPanel>

          <TabPanel value={tabValue} index={1}>
            <TableContainer component={Paper}>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Equipment Name</TableCell>
                    <TableCell>Type</TableCell>
                    <TableCell>Location</TableCell>
                    <TableCell>Status</TableCell>
                    <TableCell>Next Maintenance</TableCell>
                    <TableCell>Actions</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {resources?.equipment?.map((resource: any) => (
                    <TableRow key={resource.id}>
                      <TableCell>{resource.name}</TableCell>
                      <TableCell>{resource.type}</TableCell>
                      <TableCell>{resource.location}</TableCell>
                      <TableCell>{getAvailabilityChip(resource.availability)}</TableCell>
                      <TableCell>{new Date(resource.next_maintenance).toLocaleDateString()}</TableCell>
                      <TableCell>
                        <IconButton
                          size="small"
                          onClick={() => handleEditResource(resource)}
                        >
                          <EditIcon />
                        </IconButton>
                        <IconButton size="small">
                          <DeleteIcon />
                        </IconButton>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </TabPanel>

          <TabPanel value={tabValue} index={2}>
            <TableContainer component={Paper}>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Item Name</TableCell>
                    <TableCell>Category</TableCell>
                    <TableCell>Quantity</TableCell>
                    <TableCell>Unit</TableCell>
                    <TableCell>Status</TableCell>
                    <TableCell>Actions</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {resources?.inventory?.map((resource: any) => (
                    <TableRow key={resource.id}>
                      <TableCell>{resource.name}</TableCell>
                      <TableCell>{resource.category}</TableCell>
                      <TableCell>{resource.quantity}</TableCell>
                      <TableCell>{resource.unit}</TableCell>
                      <TableCell>{getAvailabilityChip(resource.availability)}</TableCell>
                      <TableCell>
                        <IconButton
                          size="small"
                          onClick={() => handleEditResource(resource)}
                        >
                          <EditIcon />
                        </IconButton>
                        <IconButton size="small">
                          <DeleteIcon />
                        </IconButton>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </TabPanel>
        </CardContent>
      </Card>

      <Dialog open={openDialog} onClose={() => setOpenDialog(false)} maxWidth="md" fullWidth>
        <form onSubmit={handleSubmit}>
          <DialogTitle>
            {selectedResource ? 'Edit Resource' : 'Add New Resource'}
          </DialogTitle>
          <DialogContent>
            <Grid container spacing={2} sx={{ mt: 1 }}>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="Name"
                  name="name"
                  defaultValue={selectedResource?.name}
                  required
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <FormControl fullWidth required>
                  <InputLabel>Type</InputLabel>
                  <Select
                    name="type"
                    defaultValue={selectedResource?.type || ''}
                  >
                    {resourceTypes[tabValue === 0 ? 'STAFF' : tabValue === 1 ? 'EQUIPMENT' : 'INVENTORY'].map((type) => (
                      <MenuItem key={type.value} value={type.value}>
                        {type.label}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>
              {tabValue === 0 && (
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    label="Department"
                    name="department"
                    defaultValue={selectedResource?.department}
                    required
                  />
                </Grid>
              )}
              {tabValue === 1 && (
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    label="Location"
                    name="location"
                    defaultValue={selectedResource?.location}
                    required
                  />
                </Grid>
              )}
              {tabValue === 2 && (
                <>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      fullWidth
                      label="Quantity"
                      name="quantity"
                      type="number"
                      defaultValue={selectedResource?.quantity}
                      required
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      fullWidth
                      label="Unit"
                      name="unit"
                      defaultValue={selectedResource?.unit}
                      required
                    />
                  </Grid>
                </>
              )}
            </Grid>
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setOpenDialog(false)}>Cancel</Button>
            <Button
              type="submit"
              variant="contained"
              startIcon={selectedResource ? <EditIcon /> : <AddIcon />}
            >
              {selectedResource ? 'Update' : 'Add'} Resource
            </Button>
          </DialogActions>
        </form>
      </Dialog>
    </Box>
  );
}
