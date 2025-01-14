import React from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Avatar,
  Grid,
  Button,
  TextField,
  IconButton,
  Divider,
} from '@mui/material';
import { Edit, Save, Cancel } from '@mui/icons-material';
import { useAuth } from '../hooks/useAuth';

const Profile: React.FC = () => {
  const { user, updateProfile } = useAuth();
  const [editing, setEditing] = React.useState(false);
  const [formData, setFormData] = React.useState({
    name: user?.name || '',
    email: user?.email || '',
    department: user?.department || '',
  });

  const handleEdit = () => {
    setEditing(true);
  };

  const handleCancel = () => {
    setFormData({
      name: user?.name || '',
      email: user?.email || '',
      department: user?.department || '',
    });
    setEditing(false);
  };

  const handleSave = async () => {
    try {
      await updateProfile(formData);
      setEditing(false);
    } catch (error) {
      console.error('Error updating profile:', error);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  return (
    <Box sx={{ maxWidth: 800, mx: 'auto', p: 3 }}>
      <Card>
        <CardContent>
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 4 }}>
            <Avatar
              src={user?.avatar}
              sx={{ width: 100, height: 100, mr: 3 }}
            />
            <Box>
              <Typography variant="h5" gutterBottom>
                {user?.name}
              </Typography>
              <Typography color="textSecondary">
                {user?.role}
              </Typography>
            </Box>
            {!editing && (
              <IconButton
                sx={{ ml: 'auto' }}
                onClick={handleEdit}
                color="primary"
              >
                <Edit />
              </IconButton>
            )}
          </Box>

          <Divider sx={{ my: 3 }} />

          <Grid container spacing={3}>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="الاسم"
                name="name"
                value={formData.name}
                onChange={handleChange}
                disabled={!editing}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="البريد الإلكتروني"
                name="email"
                value={formData.email}
                onChange={handleChange}
                disabled={!editing}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="القسم"
                name="department"
                value={formData.department}
                onChange={handleChange}
                disabled={!editing}
              />
            </Grid>
          </Grid>

          {editing && (
            <Box sx={{ mt: 3, display: 'flex', gap: 2, justifyContent: 'flex-end' }}>
              <Button
                variant="outlined"
                color="error"
                startIcon={<Cancel />}
                onClick={handleCancel}
              >
                إلغاء
              </Button>
              <Button
                variant="contained"
                color="primary"
                startIcon={<Save />}
                onClick={handleSave}
              >
                حفظ
              </Button>
            </Box>
          )}
        </CardContent>
      </Card>
    </Box>
  );
};

export default Profile;
