import { useState, useEffect } from 'react';
import {
  Box,
  IconButton,
  Badge,
  Menu,
  MenuItem,
  Typography,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Divider,
  Button,
  Chip,
  Popover,
  CircularProgress,
} from '@mui/material';
import {
  Notifications as NotificationsIcon,
  Event as EventIcon,
  Build as BuildIcon,
  Assignment as TaskIcon,
  Description as ReportIcon,
  Warning as AlertIcon,
  Message as MessageIcon,
  Science as ScienceIcon,
  CheckCircle as ReadIcon,
  Delete as DeleteIcon,
} from '@mui/icons-material';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import axios from 'axios';
import { formatDistanceToNow } from 'date-fns';
import { io } from 'socket.io-client';

interface Notification {
  id: number;
  title: string;
  message: string;
  notification_type: string;
  priority: string;
  is_read: boolean;
  created_at: string;
}

const NotificationCenter = () => {
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
  const [selectedNotification, setSelectedNotification] = useState<Notification | null>(null);
  const [detailsAnchorEl, setDetailsAnchorEl] = useState<null | HTMLElement>(null);
  const queryClient = useQueryClient();

  const { data: notifications, isLoading } = useQuery('notifications', () =>
    axios.get('/api/notifications/').then((res) => res.data)
  );

  const markAsReadMutation = useMutation(
    (id: number) => axios.post(`/api/notifications/${id}/mark-read/`),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('notifications');
      },
    }
  );

  const markAllAsReadMutation = useMutation(
    () => axios.post('/api/notifications/mark-all-read/'),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('notifications');
      },
    }
  );

  const archiveNotificationMutation = useMutation(
    (id: number) => axios.post(`/api/notifications/${id}/archive/`),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('notifications');
      },
    }
  );

  useEffect(() => {
    const socket = io('/notifications');
    
    socket.on('notification', (notification: Notification) => {
      queryClient.invalidateQueries('notifications');
      // Show browser notification if permission granted
      if (Notification.permission === 'granted') {
        new Notification(notification.title, {
          body: notification.message,
        });
      }
    });

    return () => {
      socket.disconnect();
    };
  }, []);

  const handleClick = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const handleNotificationClick = (
    event: React.MouseEvent<HTMLElement>,
    notification: Notification
  ) => {
    setSelectedNotification(notification);
    setDetailsAnchorEl(event.currentTarget);
    if (!notification.is_read) {
      markAsReadMutation.mutate(notification.id);
    }
  };

  const handleDetailsClose = () => {
    setDetailsAnchorEl(null);
    setSelectedNotification(null);
  };

  const getNotificationIcon = (type: string) => {
    switch (type) {
      case 'APPOINTMENT':
        return <EventIcon />;
      case 'MAINTENANCE':
        return <BuildIcon />;
      case 'TASK':
        return <TaskIcon />;
      case 'REPORT':
        return <ReportIcon />;
      case 'ALERT':
        return <AlertIcon />;
      case 'MESSAGE':
        return <MessageIcon />;
      case 'AI_PREDICTION':
        return <ScienceIcon />;
      default:
        return <NotificationsIcon />;
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'URGENT':
        return 'error';
      case 'HIGH':
        return 'warning';
      case 'MEDIUM':
        return 'info';
      case 'LOW':
        return 'success';
      default:
        return 'default';
    }
  };

  const unreadCount = notifications?.filter(
    (n: Notification) => !n.is_read
  ).length;

  return (
    <>
      <IconButton color="inherit" onClick={handleClick}>
        <Badge badgeContent={unreadCount} color="error">
          <NotificationsIcon />
        </Badge>
      </IconButton>

      <Menu
        anchorEl={anchorEl}
        open={Boolean(anchorEl)}
        onClose={handleClose}
        PaperProps={{
          style: {
            width: 360,
            maxHeight: 500,
          },
        }}
      >
        <Box sx={{ p: 2, display: 'flex', justifyContent: 'space-between' }}>
          <Typography variant="h6">Notifications</Typography>
          <Button
            size="small"
            onClick={() => markAllAsReadMutation.mutate()}
            startIcon={<ReadIcon />}
          >
            Mark all as read
          </Button>
        </Box>
        <Divider />
        {isLoading ? (
          <Box sx={{ p: 2, textAlign: 'center' }}>
            <CircularProgress size={24} />
          </Box>
        ) : notifications?.length === 0 ? (
          <Box sx={{ p: 2, textAlign: 'center' }}>
            <Typography color="textSecondary">No notifications</Typography>
          </Box>
        ) : (
          <List sx={{ p: 0 }}>
            {notifications?.map((notification: Notification) => (
              <ListItem
                key={notification.id}
                button
                onClick={(e) => handleNotificationClick(e, notification)}
                sx={{
                  backgroundColor: notification.is_read
                    ? 'transparent'
                    : 'action.hover',
                }}
              >
                <ListItemIcon>{getNotificationIcon(notification.notification_type)}</ListItemIcon>
                <ListItemText
                  primary={notification.title}
                  secondary={
                    <>
                      <Typography
                        component="span"
                        variant="body2"
                        color="textSecondary"
                      >
                        {formatDistanceToNow(new Date(notification.created_at), {
                          addSuffix: true,
                        })}
                      </Typography>
                      <Chip
                        size="small"
                        label={notification.priority}
                        color={getPriorityColor(notification.priority)}
                        sx={{ ml: 1 }}
                      />
                    </>
                  }
                />
              </ListItem>
            ))}
          </List>
        )}
      </Menu>

      <Popover
        open={Boolean(detailsAnchorEl)}
        anchorEl={detailsAnchorEl}
        onClose={handleDetailsClose}
        anchorOrigin={{
          vertical: 'bottom',
          horizontal: 'center',
        }}
        transformOrigin={{
          vertical: 'top',
          horizontal: 'center',
        }}
      >
        {selectedNotification && (
          <Box sx={{ p: 2, maxWidth: 400 }}>
            <Typography variant="h6" gutterBottom>
              {selectedNotification.title}
            </Typography>
            <Typography variant="body1" paragraph>
              {selectedNotification.message}
            </Typography>
            <Box
              sx={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
              }}
            >
              <Typography variant="caption" color="textSecondary">
                {formatDistanceToNow(new Date(selectedNotification.created_at), {
                  addSuffix: true,
                })}
              </Typography>
              <Button
                size="small"
                startIcon={<DeleteIcon />}
                onClick={() => {
                  archiveNotificationMutation.mutate(selectedNotification.id);
                  handleDetailsClose();
                }}
              >
                Archive
              </Button>
            </Box>
          </Box>
        )}
      </Popover>
    </>
  );
};

export default NotificationCenter;
