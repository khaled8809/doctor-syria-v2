import { useState } from 'react';
import {
  Box,
  TextField,
  Typography,
  Paper,
  Link,
  InputAdornment,
  IconButton,
  Alert,
  Grid,
  MenuItem,
} from '@mui/material';
import { Visibility, VisibilityOff } from '@mui/icons-material';
import { useNavigate, Link as RouterLink } from 'react-router-dom';
import { useFormik } from 'formik';
import * as Yup from 'yup';
import LoadingButton from '@mui/lab/LoadingButton';

const validationSchema = Yup.object({
  name: Yup.string().required('الاسم مطلوب'),
  email: Yup.string()
    .email('البريد الإلكتروني غير صالح')
    .required('البريد الإلكتروني مطلوب'),
  password: Yup.string()
    .min(8, 'كلمة المرور يجب أن تكون 8 أحرف على الأقل')
    .required('كلمة المرور مطلوبة'),
  confirmPassword: Yup.string()
    .oneOf([Yup.ref('password')], 'كلمات المرور غير متطابقة')
    .required('تأكيد كلمة المرور مطلوب'),
  role: Yup.string().required('نوع المستخدم مطلوب'),
  specialization: Yup.string().when('role', {
    is: 'doctor',
    then: Yup.string().required('التخصص مطلوب'),
  }),
  licenseNumber: Yup.string().when('role', {
    is: 'doctor',
    then: Yup.string().required('رقم الترخيص مطلوب'),
  }),
});

const Register = () => {
  const navigate = useNavigate();
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const formik = useFormik({
    initialValues: {
      name: '',
      email: '',
      password: '',
      confirmPassword: '',
      role: '',
      specialization: '',
      licenseNumber: '',
    },
    validationSchema,
    onSubmit: async (values) => {
      try {
        // TODO: Implement registration logic
        console.log('Form values:', values);
        navigate('/login');
      } catch (err) {
        setError(err instanceof Error ? err.message : 'حدث خطأ في التسجيل');
      }
    },
  });

  const roles = [
    { value: 'doctor', label: 'طبيب' },
    { value: 'patient', label: 'مريض' },
    { value: 'admin', label: 'مدير' },
  ];

  const specializations = [
    'طب عام',
    'طب أطفال',
    'طب باطني',
    'جراحة عامة',
    'أمراض قلبية',
    'أمراض نسائية وتوليد',
    'طب عيون',
    'طب أسنان',
    'طب نفسي',
    'طب عظام',
  ];

  return (
    <Box
      sx={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        py: 4,
        bgcolor: 'background.default',
      }}
    >
      <Paper
        elevation={3}
        sx={{
          p: 4,
          width: '100%',
          maxWidth: 600,
          mx: 2,
        }}
      >
        <Box
          component="img"
          src="/logo.png"
          alt="Doctor Syria Logo"
          sx={{
            width: 120,
            height: 'auto',
            display: 'block',
            margin: '0 auto 2rem',
          }}
        />

        <Typography variant="h5" align="center" gutterBottom>
          إنشاء حساب جديد
        </Typography>

        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}

        <form onSubmit={formik.handleSubmit}>
          <Grid container spacing={2}>
            <Grid item xs={12}>
              <TextField
                fullWidth
                id="name"
                name="name"
                label="الاسم الكامل"
                value={formik.values.name}
                onChange={formik.handleChange}
                error={formik.touched.name && Boolean(formik.errors.name)}
                helperText={formik.touched.name && formik.errors.name}
              />
            </Grid>

            <Grid item xs={12}>
              <TextField
                fullWidth
                id="email"
                name="email"
                label="البريد الإلكتروني"
                value={formik.values.email}
                onChange={formik.handleChange}
                error={formik.touched.email && Boolean(formik.errors.email)}
                helperText={formik.touched.email && formik.errors.email}
              />
            </Grid>

            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                id="password"
                name="password"
                label="كلمة المرور"
                type={showPassword ? 'text' : 'password'}
                value={formik.values.password}
                onChange={formik.handleChange}
                error={formik.touched.password && Boolean(formik.errors.password)}
                helperText={formik.touched.password && formik.errors.password}
                InputProps={{
                  endAdornment: (
                    <InputAdornment position="end">
                      <IconButton
                        onClick={() => setShowPassword(!showPassword)}
                        edge="end"
                      >
                        {showPassword ? <VisibilityOff /> : <Visibility />}
                      </IconButton>
                    </InputAdornment>
                  ),
                }}
              />
            </Grid>

            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                id="confirmPassword"
                name="confirmPassword"
                label="تأكيد كلمة المرور"
                type={showConfirmPassword ? 'text' : 'password'}
                value={formik.values.confirmPassword}
                onChange={formik.handleChange}
                error={
                  formik.touched.confirmPassword &&
                  Boolean(formik.errors.confirmPassword)
                }
                helperText={
                  formik.touched.confirmPassword && formik.errors.confirmPassword
                }
                InputProps={{
                  endAdornment: (
                    <InputAdornment position="end">
                      <IconButton
                        onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                        edge="end"
                      >
                        {showConfirmPassword ? <VisibilityOff /> : <Visibility />}
                      </IconButton>
                    </InputAdornment>
                  ),
                }}
              />
            </Grid>

            <Grid item xs={12}>
              <TextField
                fullWidth
                select
                id="role"
                name="role"
                label="نوع المستخدم"
                value={formik.values.role}
                onChange={formik.handleChange}
                error={formik.touched.role && Boolean(formik.errors.role)}
                helperText={formik.touched.role && formik.errors.role}
              >
                {roles.map((role) => (
                  <MenuItem key={role.value} value={role.value}>
                    {role.label}
                  </MenuItem>
                ))}
              </TextField>
            </Grid>

            {formik.values.role === 'doctor' && (
              <>
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    select
                    id="specialization"
                    name="specialization"
                    label="التخصص"
                    value={formik.values.specialization}
                    onChange={formik.handleChange}
                    error={
                      formik.touched.specialization &&
                      Boolean(formik.errors.specialization)
                    }
                    helperText={
                      formik.touched.specialization &&
                      formik.errors.specialization
                    }
                  >
                    {specializations.map((spec) => (
                      <MenuItem key={spec} value={spec}>
                        {spec}
                      </MenuItem>
                    ))}
                  </TextField>
                </Grid>

                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    id="licenseNumber"
                    name="licenseNumber"
                    label="رقم الترخيص"
                    value={formik.values.licenseNumber}
                    onChange={formik.handleChange}
                    error={
                      formik.touched.licenseNumber &&
                      Boolean(formik.errors.licenseNumber)
                    }
                    helperText={
                      formik.touched.licenseNumber &&
                      formik.errors.licenseNumber
                    }
                  />
                </Grid>
              </>
            )}
          </Grid>

          <LoadingButton
            fullWidth
            type="submit"
            variant="contained"
            loading={formik.isSubmitting}
            sx={{ mt: 3 }}
          >
            إنشاء حساب
          </LoadingButton>

          <Box sx={{ mt: 2, textAlign: 'center' }}>
            <Typography variant="body2">
              لديك حساب بالفعل؟{' '}
              <Link
                component={RouterLink}
                to="/login"
                sx={{ textDecoration: 'none' }}
              >
                تسجيل الدخول
              </Link>
            </Typography>
          </Box>
        </form>
      </Paper>
    </Box>
  );
};

export default Register;
