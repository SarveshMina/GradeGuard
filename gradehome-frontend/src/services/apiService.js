// src/services/apiService.js
import axios from 'axios';
import { API_URL } from '@/config.js';

// Create axios instance with default config
const apiClient = axios.create({
    baseURL: API_URL,
    withCredentials: true, // Important for cookies
    headers: {
        'Content-Type': 'application/json'
    }
});

// Add interceptors for error handling
apiClient.interceptors.response.use(
    response => response,
    error => {
        if (error.response && error.response.status === 401) {
            // Redirect to login if unauthorized
            window.location.href = '/login';
        }
        return Promise.reject(error);
    }
);

export default apiClient;
