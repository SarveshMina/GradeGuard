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