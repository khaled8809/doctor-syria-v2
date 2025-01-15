import { useState } from 'react';
import {
  Box,
  Paper,
  Typography,
  TextField,
  Button,
  IconButton,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TablePagination,
  Chip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Grid,
  InputAdornment,
  Menu,
  MenuItem,
} from '@mui/material';
import {
  Search,
  Add,
  Edit,
  Delete,
  MoreVert,
  FileDownload,
  Visibility,
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';

interface Patient {
  id: string;
  name: string;
  age: number;
  gender: string;
  phone: string;
  email: string;
  lastVisit: string;
  status: 'active' | 'inactive' | 'pending';
}

const DUMMY_PATIENTS: Patient[] = [
  {
    id: '1',
    name: 'أحمد محمد',
    age: 35,
    gender: 'ذكر',
    phone: '0912345678',
    email: 'ahmed@example.com',
    lastVisit: '2025-01-10',
    status: 'active',
  },
  {
    id: '2',
    name: 'سارة أحمد',
    age: 28,
    gender: 'أنثى',
    phone: '0923456789',
    email: 'sara@example.com',
    lastVisit: '2025-01-12',
    status: 'active',
  },
  // يمكن إضافة المزيد من البيانات الوهمية هنا
];

const Patients = () => {
  const navigate = useNavigate();
  const [patients, setPatients] = useState<Patient[]>(DUMMY_PATIENTS);
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [searchTerm, setSearchTerm] = useState('');
  const [openAddDialog, setOpenAddDialog] = useState(false);
  const [selectedPatient, setSelectedPatient] = useState<Patient | null>(null);
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);

  const handleOpenMenu = (event: React.MouseEvent<HTMLElement>, patient: Patient) => {
    setAnchorEl(event.currentTarget);
    setSelectedPatient(patient);
  };

  const handleCloseMenu = () => {
    setAnchorEl(null);
    setSelectedPatient(null);
  };

  const handleChangePage = (event: unknown, newPage: number) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event: React.ChangeEvent<HTMLInputElement>) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  const filteredPatients = patients.filter((patient) =>
    patient.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    patient.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
    patient.phone.includes(searchTerm)
  );

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active':
        return 'success';
      case 'inactive':
        return 'error';
      case 'pending':
        return 'warning';
      default:
        return 'default';
    }
  };

  const handleAddPatient = () => {
    setOpenAddDialog(true);
  };

  const handleViewPatient = (patientId: string) => {
    navigate(`/patients/${patientId}`);
  };

  return (
    <Box sx={{ p: 3 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h4">المرضى</Typography>
        <Button
          variant="contained"
          startIcon={<Add />}
          onClick={handleAddPatient}
        >
          إضافة مريض
        </Button>
      </Box>

      <Paper sx={{ mb: 3, p: 2 }}>
        <Grid container spacing={2} alignItems="center">
          <Grid item xs={12} sm={6} md={4}>
            <TextField
              fullWidth
              placeholder="بحث عن مريض..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <Search />
                  </InputAdornment>
                ),
              }}
            />
          </Grid>
          <Grid item xs={12} sm={6} md={8}>
            <Box sx={{ display: 'flex', gap: 1, justifyContent: 'flex-end' }}>
              <Button startIcon={<FileDownload />}>تصدير CSV</Button>
            </Box>
          </Grid>
        </Grid>
      </Paper>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>الاسم</TableCell>
              <TableCell>العمر</TableCell>
              <TableCell>الجنس</TableCell>
              <TableCell>رقم الهاتف</TableCell>
              <TableCell>البريد الإلكتروني</TableCell>
              <TableCell>آخر زيارة</TableCell>
              <TableCell>الحالة</TableCell>
              <TableCell>الإجراءات</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {filteredPatients
              .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
              .map((patient) => (
                <TableRow key={patient.id}>
                  <TableCell>{patient.name}</TableCell>
                  <TableCell>{patient.age}</TableCell>
                  <TableCell>{patient.gender}</TableCell>
                  <TableCell>{patient.phone}</TableCell>
                  <TableCell>{patient.email}</TableCell>
                  <TableCell>{patient.lastVisit}</TableCell>
                  <TableCell>
                    <Chip
                      label={
                        patient.status === 'active'
                          ? 'نشط'
                          : patient.status === 'inactive'
                          ? 'غير نشط'
                          : 'معلق'
                      }
                      color={getStatusColor(patient.status)}
                      size="small"
                    />
                  </TableCell>
                  <TableCell>
                    <IconButton
                      onClick={(event) => handleOpenMenu(event, patient)}
                    >
                      <MoreVert />
                    </IconButton>
                  </TableCell>
                </TableRow>
              ))}
          </TableBody>
        </Table>
        <TablePagination
          component="div"
          count={filteredPatients.length}
          page={page}
          onPageChange={handleChangePage}
          rowsPerPage={rowsPerPage}
          onRowsPerPageChange={handleChangeRowsPerPage}
          labelRowsPerPage="عدد الصفوف في الصفحة"
          labelDisplayedRows={({ from, to, count }) =>
            `${from}-${to} من ${count}`
          }
        />
      </TableContainer>

      <Menu
        anchorEl={anchorEl}
        open={Boolean(anchorEl)}
        onClose={handleCloseMenu}
      >
        <MenuItem
          onClick={() => {
            handleViewPatient(selectedPatient?.id || '');
            handleCloseMenu();
          }}
        >
          <Visibility sx={{ mr: 1 }} /> عرض التفاصيل
        </MenuItem>
        <MenuItem onClick={handleCloseMenu}>
          <Edit sx={{ mr: 1 }} /> تعديل
        </MenuItem>
        <MenuItem onClick={handleCloseMenu}>
          <Delete sx={{ mr: 1 }} /> حذف
        </MenuItem>
      </Menu>

      {/* Add Patient Dialog */}
      <Dialog
        open={openAddDialog}
        onClose={() => setOpenAddDialog(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>إضافة مريض جديد</DialogTitle>
        <DialogContent>
          <Grid container spacing={2} sx={{ mt: 1 }}>
            <Grid item xs={12} sm={6}>
              <TextField fullWidth label="الاسم" />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField fullWidth label="العمر" type="number" />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                select
                label="الجنس"
                defaultValue=""
              >
                <MenuItem value="ذكر">ذكر</MenuItem>
                <MenuItem value="أنثى">أنثى</MenuItem>
              </TextField>
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField fullWidth label="رقم الهاتف" />
            </Grid>
            <Grid item xs={12}>
              <TextField fullWidth label="البريد الإلكتروني" />
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenAddDialog(false)}>إلغاء</Button>
          <Button variant="contained" onClick={() => setOpenAddDialog(false)}>
            حفظ
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default Patients;
