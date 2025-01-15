import React from 'react';
import {
  Badge,
  IconButton,
  Menu,
  MenuItem,
  Typography,
  Box,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Divider,
} from '@mui/material';
import {
  Notifications,
  Info,
  Warning,
  Error,
  CheckCircle,
} from '@mui/icons-material';
import { useNotifications } from '../../hooks/useNotifications';
import { formatDistanceToNow } from 'date-fns';
import { arSA } from 'date-fns/locale';

const NotificationBadge: React.FC = () => {
  const [anchorEl, setAnchorEl] = React.useState<null | HTMLElement>(null);
  const { notifications, markAsRead, clearAll } = useNotifications();
  const unreadCount = notifications.filter((n) => !n.read).length;

  const handleClick = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const getNotificationIcon = (type: string) => {
    switch (type) {
      case 'info':
        return <Info color="info" />;
      case 'warning':
        return <Warning color="warning" />;
      case 'error':
        return <Error color="error" />;
      case 'success':
        return <CheckCircle color="success" />;
      default:
        return <Info />;
    }
  };

  const handleNotificationClick = (id: string) => {
    markAsRead(id);
    handleClose();
  };

  return (
    <>
      <IconButton color="inherit" onClick={handleClick}>
        <Badge badgeContent={unreadCount} color="error">
          <Notifications />
        </Badge>
      </IconButton>
      <Menu
        anchorEl={anchorEl}
        open={Boolean(anchorEl)}
        onClose={handleClose}
        PaperProps={{
          sx: {
            width: 360,
            maxHeight: 500,
          },
        }}
        transformOrigin={{ horizontal: 'right', vertical: 'top' }}
        anchorOrigin={{ horizontal: 'right', vertical: 'bottom' }}
      >
        <Box sx={{ p: 2, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <Typography variant="h6">الإشعارات</Typography>
          {notifications.length > 0 && (
            <Typography
              variant="body2"
              sx={{ cursor: 'pointer', color: 'primary.main' }}
              onClick={() => {
                clearAll();
                handleClose();
              }}
            >
              مسح الكل
            </Typography>
          )}
        </Box>
        <Divider />
        {notifications.length === 0 ? (
          <Box sx={{ p: 2, textAlign: 'center' }}>
            <Typography variant="body2" color="text.secondary">
              لا توجد إشعارات جديدة
            </Typography>
          </Box>
        ) : (
          <List sx={{ p: 0 }}>
            {notifications.map((notification) => (
              <React.Fragment key={notification.id}>
                <ListItem
                  button
                  onClick={() => handleNotificationClick(notification.id)}
                  sx={{
                    backgroundColor: notification.read ? 'inherit' : 'action.hover',
                  }}
                >
                  <ListItemIcon>{getNotificationIcon(notification.type)}</ListItemIcon>
                  <ListItemText
                    primary={notification.message}
                    secondary={formatDistanceToNow(new Date(notification.timestamp), {
                      addSuffix: true,
                      locale: arSA,
                    })}
                  />
                </ListItem>
                <Divider />
              </React.Fragment>
            ))}
          </List>
        )}
      </Menu>
    </>
  );
};

export default NotificationBadge;
