import { useState, useEffect, useRef } from 'react';
import {
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  Button,
  IconButton,
  TextField,
  List,
  ListItem,
  ListItemText,
  ListItemAvatar,
  Avatar,
  Paper,
  Divider,
  Badge,
  Tabs,
  Tab,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
} from '@mui/material';
import {
  Send as SendIcon,
  VideoCall as VideoCallIcon,
  Call as CallIcon,
  AttachFile as AttachFileIcon,
  Image as ImageIcon,
  Description as FileIcon,
  MoreVert as MoreVertIcon,
  Search as SearchIcon,
} from '@mui/icons-material';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import axios from 'axios';
import { io } from 'socket.io-client';

interface Message {
  id: number;
  sender: {
    id: number;
    name: string;
    avatar: string;
  };
  content: string;
  timestamp: string;
  type: 'TEXT' | 'IMAGE' | 'FILE';
  status: 'SENT' | 'DELIVERED' | 'READ';
}

interface ChatRoom {
  id: number;
  name: string;
  type: 'INDIVIDUAL' | 'GROUP';
  participants: Array<{
    id: number;
    name: string;
    avatar: string;
    status: 'ONLINE' | 'OFFLINE';
  }>;
  lastMessage?: Message;
  unreadCount: number;
}

export default function Communication() {
  const [selectedChat, setSelectedChat] = useState<ChatRoom | null>(null);
  const [message, setMessage] = useState('');
  const [tabValue, setTabValue] = useState(0);
  const [openVideoCall, setOpenVideoCall] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const queryClient = useQueryClient();
  const socket = useRef<any>(null);

  const { data: chatRooms } = useQuery('chat-rooms', () =>
    axios.get('/api/chat-rooms/').then((res) => res.data)
  );

  const { data: messages, isLoading: messagesLoading } = useQuery(
    ['messages', selectedChat?.id],
    () =>
      axios
        .get(`/api/chat-rooms/${selectedChat?.id}/messages/`)
        .then((res) => res.data),
    {
      enabled: !!selectedChat,
    }
  );

  const sendMessageMutation = useMutation(
    (newMessage: any) =>
      axios.post(`/api/chat-rooms/${selectedChat?.id}/messages/`, newMessage),
    {
      onSuccess: () => {
        queryClient.invalidateQueries(['messages', selectedChat?.id]);
        setMessage('');
      },
    }
  );

  useEffect(() => {
    if (selectedChat) {
      socket.current = io('/chat');
      socket.current.emit('join_room', selectedChat.id);

      socket.current.on('new_message', (message: Message) => {
        queryClient.invalidateQueries(['messages', selectedChat.id]);
      });

      return () => {
        socket.current.disconnect();
      };
    }
  }, [selectedChat]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSendMessage = () => {
    if (message.trim()) {
      sendMessageMutation.mutate({
        content: message,
        type: 'TEXT',
      });
    }
  };

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('type', file.type.startsWith('image/') ? 'IMAGE' : 'FILE');

      sendMessageMutation.mutate(formData);
    }
  };

  const formatTime = (timestamp: string) => {
    const date = new Date(timestamp);
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <Box>
      <Typography variant="h4" mb={3}>
        Communication
      </Typography>

      <Grid container spacing={2} sx={{ height: 'calc(100vh - 200px)' }}>
        <Grid item xs={12} md={4}>
          <Card sx={{ height: '100%' }}>
            <CardContent sx={{ height: '100%', p: 0 }}>
              <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
                <Tabs value={tabValue} onChange={(e, v) => setTabValue(v)}>
                  <Tab label="Chats" />
                  <Tab label="Calls" />
                </Tabs>
              </Box>

              <Box sx={{ p: 2 }}>
                <TextField
                  fullWidth
                  size="small"
                  placeholder="Search..."
                  InputProps={{
                    startAdornment: <SearchIcon sx={{ mr: 1 }} />,
                  }}
                />
              </Box>

              <List sx={{ overflow: 'auto', height: 'calc(100% - 112px)' }}>
                {chatRooms?.map((chat: ChatRoom) => (
                  <ListItem
                    key={chat.id}
                    button
                    selected={selectedChat?.id === chat.id}
                    onClick={() => setSelectedChat(chat)}
                  >
                    <ListItemAvatar>
                      <Badge
                        color="success"
                        variant="dot"
                        invisible={
                          chat.participants[0].status === 'OFFLINE'
                        }
                      >
                        <Avatar src={chat.participants[0].avatar}>
                          {chat.name[0]}
                        </Avatar>
                      </Badge>
                    </ListItemAvatar>
                    <ListItemText
                      primary={chat.name}
                      secondary={chat.lastMessage?.content}
                      secondaryTypographyProps={{
                        noWrap: true,
                        style: {
                          width: '200px',
                        },
                      }}
                    />
                    {chat.unreadCount > 0 && (
                      <Badge
                        badgeContent={chat.unreadCount}
                        color="primary"
                        sx={{ ml: 2 }}
                      />
                    )}
                  </ListItem>
                ))}
              </List>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={8}>
          <Card sx={{ height: '100%' }}>
            {selectedChat ? (
              <Box
                sx={{
                  height: '100%',
                  display: 'flex',
                  flexDirection: 'column',
                }}
              >
                <Box
                  sx={{
                    p: 2,
                    borderBottom: 1,
                    borderColor: 'divider',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                  }}
                >
                  <Box display="flex" alignItems="center">
                    <Avatar src={selectedChat.participants[0].avatar} sx={{ mr: 1 }}>
                      {selectedChat.name[0]}
                    </Avatar>
                    <Box>
                      <Typography variant="subtitle1">
                        {selectedChat.name}
                      </Typography>
                      <Typography variant="body2" color="textSecondary">
                        {selectedChat.participants[0].status === 'ONLINE'
                          ? 'Online'
                          : 'Offline'}
                      </Typography>
                    </Box>
                  </Box>
                  <Box>
                    <IconButton onClick={() => setOpenVideoCall(true)}>
                      <VideoCallIcon />
                    </IconButton>
                    <IconButton>
                      <CallIcon />
                    </IconButton>
                    <IconButton>
                      <MoreVertIcon />
                    </IconButton>
                  </Box>
                </Box>

                <Box
                  sx={{
                    flexGrow: 1,
                    overflow: 'auto',
                    p: 2,
                    backgroundColor: 'grey.50',
                  }}
                >
                  {messages?.map((msg: Message) => (
                    <Box
                      key={msg.id}
                      sx={{
                        display: 'flex',
                        justifyContent:
                          msg.sender.id === 1 ? 'flex-end' : 'flex-start',
                        mb: 2,
                      }}
                    >
                      {msg.sender.id !== 1 && (
                        <Avatar
                          src={msg.sender.avatar}
                          sx={{ width: 32, height: 32, mr: 1 }}
                        >
                          {msg.sender.name[0]}
                        </Avatar>
                      )}
                      <Box
                        sx={{
                          maxWidth: '70%',
                        }}
                      >
                        <Paper
                          sx={{
                            p: 2,
                            backgroundColor:
                              msg.sender.id === 1 ? 'primary.main' : 'white',
                            color: msg.sender.id === 1 ? 'white' : 'inherit',
                          }}
                        >
                          {msg.type === 'TEXT' && (
                            <Typography>{msg.content}</Typography>
                          )}
                          {msg.type === 'IMAGE' && (
                            <Box
                              component="img"
                              src={msg.content}
                              sx={{ maxWidth: '100%', borderRadius: 1 }}
                            />
                          )}
                          {msg.type === 'FILE' && (
                            <Button
                              startIcon={<FileIcon />}
                              href={msg.content}
                              target="_blank"
                              sx={{
                                color: msg.sender.id === 1 ? 'white' : 'primary',
                              }}
                            >
                              Download File
                            </Button>
                          )}
                        </Paper>
                        <Typography
                          variant="caption"
                          color="textSecondary"
                          sx={{ ml: 1 }}
                        >
                          {formatTime(msg.timestamp)}
                        </Typography>
                      </Box>
                    </Box>
                  ))}
                  <div ref={messagesEndRef} />
                </Box>

                <Box sx={{ p: 2, backgroundColor: 'background.paper' }}>
                  <Grid container spacing={1}>
                    <Grid item>
                      <input
                        accept="image/*,application/pdf"
                        style={{ display: 'none' }}
                        id="file-input"
                        type="file"
                        onChange={handleFileUpload}
                      />
                      <label htmlFor="file-input">
                        <IconButton component="span">
                          <AttachFileIcon />
                        </IconButton>
                      </label>
                    </Grid>
                    <Grid item xs>
                      <TextField
                        fullWidth
                        placeholder="Type a message..."
                        value={message}
                        onChange={(e) => setMessage(e.target.value)}
                        onKeyPress={(e) => {
                          if (e.key === 'Enter') {
                            handleSendMessage();
                          }
                        }}
                      />
                    </Grid>
                    <Grid item>
                      <IconButton
                        color="primary"
                        onClick={handleSendMessage}
                        disabled={!message.trim()}
                      >
                        <SendIcon />
                      </IconButton>
                    </Grid>
                  </Grid>
                </Box>
              </Box>
            ) : (
              <Box
                sx={{
                  height: '100%',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                }}
              >
                <Typography color="textSecondary">
                  Select a chat to start messaging
                </Typography>
              </Box>
            )}
          </Card>
        </Grid>
      </Grid>

      <Dialog
        open={openVideoCall}
        onClose={() => setOpenVideoCall(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>Video Call</DialogTitle>
        <DialogContent>
          <Box
            sx={{
              width: '100%',
              height: 400,
              backgroundColor: 'grey.900',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
            }}
          >
            <Typography color="white">Video call content will go here</Typography>
          </Box>
        </DialogContent>
        <DialogActions>
          <Button
            variant="contained"
            color="error"
            onClick={() => setOpenVideoCall(false)}
          >
            End Call
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}
