import { useState } from 'react';
import {
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  Button,
  IconButton,
  Tabs,
  Tab,
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
} from '@mui/material';
import {
  Add as AddIcon,
  Download as DownloadIcon,
  Share as ShareIcon,
  Delete as DeleteIcon,
  PictureAsPdf as PdfIcon,
  TableChart as ExcelIcon,
  Article as CsvIcon,
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
      id={`report-tabpanel-${index}`}
      aria-labelledby={`report-tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );
}

const reportTypes = [
  { value: 'FINANCIAL', label: 'Financial Report' },
  { value: 'PERFORMANCE', label: 'Performance Report' },
  { value: 'SATISFACTION', label: 'Patient Satisfaction' },
  { value: 'ANALYTICS', label: 'Analytics Report' },
];

export default function Reports() {
  const [tabValue, setTabValue] = useState(0);
  const [openDialog, setOpenDialog] = useState(false);
  const queryClient = useQueryClient();

  const { data: reports, isLoading } = useQuery('reports', () =>
    axios.get('/api/reports/').then((res) => res.data)
  );

  const generateReportMutation = useMutation(
    (reportData: any) => axios.post('/api/reports/', reportData),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('reports');
        setOpenDialog(false);
      },
    }
  );

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  const handleGenerateReport = (event: React.FormEvent) => {
    event.preventDefault();
    const formData = new FormData(event.target as HTMLFormElement);
    const reportData = Object.fromEntries(formData.entries());
    generateReportMutation.mutate(reportData);
  };

  const handleDownload = (format: string, reportId: number) => {
    axios
      .get(`/api/reports/${reportId}/download/?format=${format}`, {
        responseType: 'blob',
      })
      .then((response) => {
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', `report.${format.toLowerCase()}`);
        document.body.appendChild(link);
        link.click();
        link.remove();
      });
  };

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4">Reports</Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => setOpenDialog(true)}
        >
          Generate Report
        </Button>
      </Box>

      <Card>
        <CardContent>
          <Tabs value={tabValue} onChange={handleTabChange}>
            <Tab label="All Reports" />
            <Tab label="Financial" />
            <Tab label="Performance" />
            <Tab label="Patient Satisfaction" />
          </Tabs>

          <TabPanel value={tabValue} index={0}>
            <TableContainer component={Paper}>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Title</TableCell>
                    <TableCell>Type</TableCell>
                    <TableCell>Date Range</TableCell>
                    <TableCell>Created At</TableCell>
                    <TableCell>Actions</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {reports?.map((report: any) => (
                    <TableRow key={report.id}>
                      <TableCell>{report.title}</TableCell>
                      <TableCell>{report.report_type}</TableCell>
                      <TableCell>
                        {new Date(report.date_range_start).toLocaleDateString()} -{' '}
                        {new Date(report.date_range_end).toLocaleDateString()}
                      </TableCell>
                      <TableCell>
                        {new Date(report.created_at).toLocaleString()}
                      </TableCell>
                      <TableCell>
                        <IconButton
                          size="small"
                          onClick={() => handleDownload('PDF', report.id)}
                        >
                          <PdfIcon />
                        </IconButton>
                        <IconButton
                          size="small"
                          onClick={() => handleDownload('EXCEL', report.id)}
                        >
                          <ExcelIcon />
                        </IconButton>
                        <IconButton
                          size="small"
                          onClick={() => handleDownload('CSV', report.id)}
                        >
                          <CsvIcon />
                        </IconButton>
                        <IconButton size="small">
                          <ShareIcon />
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
        <form onSubmit={handleGenerateReport}>
          <DialogTitle>Generate New Report</DialogTitle>
          <DialogContent>
            <Grid container spacing={2} sx={{ mt: 1 }}>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="Report Title"
                  name="title"
                  required
                />
              </Grid>
              <Grid item xs={12}>
                <FormControl fullWidth required>
                  <InputLabel>Report Type</InputLabel>
                  <Select name="report_type" defaultValue="">
                    {reportTypes.map((type) => (
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
                  label="Start Date"
                  type="date"
                  name="date_range_start"
                  InputLabelProps={{ shrink: true }}
                  required
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="End Date"
                  type="date"
                  name="date_range_end"
                  InputLabelProps={{ shrink: true }}
                  required
                />
              </Grid>
              <Grid item xs={12}>
                <FormControl fullWidth required>
                  <InputLabel>Export Format</InputLabel>
                  <Select name="export_format" defaultValue="PDF">
                    <MenuItem value="PDF">PDF</MenuItem>
                    <MenuItem value="EXCEL">Excel</MenuItem>
                    <MenuItem value="CSV">CSV</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
            </Grid>
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setOpenDialog(false)}>Cancel</Button>
            <Button
              type="submit"
              variant="contained"
              startIcon={<AddIcon />}
            >
              Generate Report
            </Button>
          </DialogActions>
        </form>
      </Dialog>
    </Box>
  );
}
