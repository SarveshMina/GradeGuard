// src/services/userProfileService.js
import apiClient from './apiService';

const userProfileService = {
    async getUserProfile() {
        try {
            const response = await apiClient.get('/user/profile');
            return response.data;
        } catch (error) {
            console.error('Error fetching user profile:', error);
            throw error;
        }
    },

    async updateProfile(profileData) {
        try {
            const response = await apiClient.put('/user/profile', profileData);
            return response.data;
        } catch (error) {
            console.error('Error updating user profile:', error);
            throw error;
        }
    },

    async uploadAvatar(formData) {
        try {
            const response = await apiClient.post('/user/upload-avatar', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            });
            return response.data;
        } catch (error) {
            console.error('Error uploading avatar:', error);
            throw error;
        }
    }
};

export default userProfileService;