import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import {
  Container,
  Paper,
  Typography,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  IconButton,
  Button,
  CircularProgress,
  Box,
  Alert,
} from '@mui/material';
import { useDropzone } from 'react-dropzone';
import DownloadIcon from '@mui/icons-material/Download';
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

const TaskList = () => {
  const [error, setError] = useState(null);
  const queryClient = useQueryClient();

  const { data: tasks, isLoading } = useQuery('tasks', async () => {
    const response = await axios.get(`${API_BASE_URL}/tasks/`);
    return response.data;
  });

  const createTaskMutation = useMutation(
    async (formData) => {
      const response = await axios.post(`${API_BASE_URL}/tasks/`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      return response.data;
    },
    {
      onSuccess: () => {
        queryClient.invalidateQueries('tasks');
      },
      onError: (error) => {
        setError(error.response?.data?.error || 'An error occurred');
      },
    }
  );

  const onDrop = async (acceptedFiles) => {
    const file = acceptedFiles[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('input_file', file);
    formData.append('description', `Process ${file.name}`);

    createTaskMutation.mutate(formData);
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
    },
    multiple: false,
  });

  const handleDownload = async (taskId) => {
    try {
      const response = await axios.get(`${API_BASE_URL}/tasks/${taskId}/download/`, {
        responseType: 'blob',
      });
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `compressed_${taskId}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (error) {
      setError('Failed to download file');
    }
  };

  return (
    <Container maxWidth="md" sx={{ mt: 4 }}>
      {error && (
        <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError(null)}>
          {error}
        </Alert>
      )}

      <Paper
        {...getRootProps()}
        sx={{
          p: 3,
          mb: 3,
          textAlign: 'center',
          cursor: 'pointer',
          bgcolor: isDragActive ? 'action.hover' : 'background.paper',
        }}
      >
        <input {...getInputProps()} />
        <Typography variant="h6" gutterBottom>
          {isDragActive
            ? 'Drop the PDF file here'
            : 'Drag and drop a PDF file here, or click to select'}
        </Typography>
        <Typography variant="body2" color="textSecondary">
          Only PDF files are accepted
        </Typography>
      </Paper>

      <Typography variant="h5" gutterBottom>
        Task List
      </Typography>

      {isLoading ? (
        <Box display="flex" justifyContent="center" mt={4}>
          <CircularProgress />
        </Box>
      ) : (
        <List>
          {tasks?.results?.map((task) => (
            <ListItem
              key={task.id}
              divider
              sx={{
                bgcolor: task.status === 'COMPLETED' ? 'success.light' : 'background.paper',
              }}
            >
              <ListItemText
                primary={task.description}
                secondary={
                  <>
                    Status: {task.status}
                    {task.error_message && (
                      <Typography color="error" variant="body2">
                        Error: {task.error_message}
                      </Typography>
                    )}
                  </>
                }
              />
              <ListItemSecondaryAction>
                {task.status === 'COMPLETED' && (
                  <IconButton
                    edge="end"
                    aria-label="download"
                    onClick={() => handleDownload(task.id)}
                  >
                    <DownloadIcon />
                  </IconButton>
                )}
              </ListItemSecondaryAction>
            </ListItem>
          ))}
        </List>
      )}
    </Container>
  );
};

export default TaskList; 