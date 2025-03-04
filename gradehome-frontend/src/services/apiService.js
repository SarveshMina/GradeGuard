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

// src/services/authService.js
import apiClient from './apiService';
import { notify } from './toastService';

export const authService = {
    async login(credentials) {
        try {
            const response = await apiClient.post('/login', credentials);
            return response.data;
        } catch (error) {
            throw error;
        }
    },

    async logout() {
        // For cookie-based auth, we just remove client-side session info
        // A real implementation would invalidate the session on the server
        localStorage.removeItem('userInfo');

        // Redirect to login page
        window.location.href = '/login';
        return true;
    },

    async checkAuth() {
        try {
            const response = await apiClient.get('/protected');
            return response.data;
        } catch (error) {
            throw error;
        }
    }
};

// src/services/profileService.js
import apiClient from './apiService';

export const profileService = {
    async getProfile() {
        try {
            const response = await apiClient.get('/user/profile');
            return response.data;
        } catch (error) {
            throw error;
        }
    },

    async updateProfile(profileData) {
        try {
            const response = await apiClient.put('/user/profile', profileData);
            return response.data;
        } catch (error) {
            throw error;
        }
    },

    async getAvatarUploadUrl(filename) {
        try {
            const response = await apiClient.post('/user/avatar-upload', { filename });
            return response.data;
        } catch (error) {
            throw error;
        }
    }
};

// src/services/calendarService.js
import apiClient from './apiService';

export const calendarService = {
    async getEvents(startDate, endDate) {
        try {
            const params = {};
            if (startDate) params.start_date = startDate;
            if (endDate) params.end_date = endDate;

            const response = await apiClient.get('/calendar/events', { params });
            return response.data;
        } catch (error) {
            throw error;
        }
    },

    async createEvent(eventData) {
        try {
            const response = await apiClient.post('/calendar/events', eventData);
            return response.data;
        } catch (error) {
            throw error;
        }
    },

    async updateEvent(id, eventData) {
        try {
            const response = await apiClient.put(`/calendar/events/${id}`, eventData);
            return response.data;
        } catch (error) {
            throw error;
        }
    },

    async deleteEvent(id) {
        try {
            const response = await apiClient.delete(`/calendar/events/${id}`);
            return response.data;
        } catch (error) {
            throw error;
        }
    }
};

// src/services/settingsService.js
import apiClient from './apiService';

export const settingsService = {
    async getSettings() {
        try {
            const response = await apiClient.get('/user/settings');
            return response.data;
        } catch (error) {
            throw error;
        }
    },

    async updateSettings(settingsData) {
        try {
            const response = await apiClient.put('/user/settings', settingsData);
            return response.data;
        } catch (error) {
            throw error;
        }
    },

    async changePassword(passwordData) {
        try {
            const response = await apiClient.put('/user/password', passwordData);
            return response.data;
        } catch (error) {
            throw error;
        }
    }
};