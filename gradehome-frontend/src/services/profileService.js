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