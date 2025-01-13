import React from 'react';
import { Snackbar, Alert, IconButton } from '@mui/material';
import { Close as CloseIcon } from '@mui/icons-material';
import { useNotifications } from '../../../hooks/useNotifications';

const NotificationSystem: React.FC = () => {
  const { notifications, removeNotification } = useNotifications();

  const handleClose = (id: string) => {
    removeNotification(id);
  };

  return (
    <>
      {notifications.map((notification) => (
        <Snackbar
          key={notification.id}
          open={true}
          autoHideDuration={notification.duration || 6000}
          onClose={() => handleClose(notification.id)}
          anchorOrigin={{ vertical: 'top', horizontal: 'left' }}
        >
          <Alert
            severity={notification.type}
            action={
              <IconButton
                size="small"
                color="inherit"
                onClick={() => handleClose(notification.id)}
              >
                <CloseIcon fontSize="small" />
              </IconButton>
            }
          >
            {notification.message}
          </Alert>
        </Snackbar>
      ))}
    </>
  );
};

export default NotificationSystem;
