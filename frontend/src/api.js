import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || '';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// User operations
export const getUsers = () => api.get('/api/users/');
export const createUser = (userData) => api.post('/api/users/', userData);
export const getUser = (userId) => api.get(`/api/users/${userId}`);

// Task operations
export const getTasks = (userId) => {
  const params = userId ? { user_id: userId } : {};
  return api.get('/api/tasks/', { params });
};
export const createTask = (userId, taskData) => api.post(`/api/users/${userId}/tasks/`, taskData);
export const updateTask = (taskId, taskData) => api.patch(`/api/tasks/${taskId}`, taskData);
export const deleteTask = (taskId) => api.delete(`/api/tasks/${taskId}`);
export const getTasksByPriority = (priority, userId = null) => {
  const params = userId ? { user_id: userId } : {};
  return api.get(`/api/tasks/priority/${priority}`, { params });
};

// Stats
export const getCompletedStats = (userId) => {
  const params = userId ? { user_id: userId } : {};
  return api.get('/api/stats/completed', { params });
};
export const healthCheck = () => api.get('/api/health');

export default api;
