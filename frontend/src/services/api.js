/**
 * API Service Layer
 * Handles all HTTP requests to the backend
 */
import axios from 'axios';
import { auth } from '../utils/auth';

// Create axios instance with base configuration
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:5000/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor - Add JWT token to headers
// TEMPORARILY DISABLED - No authentication required
api.interceptors.request.use(
  (config) => {
    // const token = auth.getToken();
    // if (token) {
    //   config.headers.Authorization = `Bearer ${token}`;
    // }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor - Handle errors globally
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid
      auth.logout();
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Authentication API
export const authAPI = {
  register: async (username, email, password) => {
    const response = await api.post('/auth/register', {
      username,
      email,
      password,
    });
    return response.data;
  },

  login: async (username, password) => {
    const response = await api.post('/auth/login', {
      username,
      password,
    });
    return response.data;
  },

  getMe: async () => {
    const response = await api.get('/auth/me');
    return response.data;
  },
};

// Detection API
export const detectionAPI = {
  detectImage: async (imageFile) => {
    const formData = new FormData();
    formData.append('image', imageFile);
    
    const response = await api.post('/detect/image', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  detectVideo: async (videoFile) => {
    const formData = new FormData();
    formData.append('video', videoFile);
    
    const response = await api.post('/detect/video', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  detectCamera: async (base64Image) => {
    const response = await api.post('/detect/camera', {
      image: base64Image,
    });
    return response.data;
  },
};

// History API
export const historyAPI = {
  getAll: async () => {
    const response = await api.get('/history');
    return response.data;
  },
};

// Stats API
export const statsAPI = {
  getStats: async () => {
    const response = await api.get('/stats');
    return response.data;
  },
};

export default api;
