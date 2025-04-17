// src/services/moduleService.js
import apiClient from './apiService';

const moduleService = {
    async getAllModules() {
        try {
            const response = await apiClient.get('/api/modules');
            return response.data;
        } catch (error) {
            console.error('Error fetching modules:', error);
            throw error;
        }
    },

    async getModuleById(moduleId) {
        try {
            const response = await apiClient.get(`/api/modules/${moduleId}`);
            return response.data;
        } catch (error) {
            console.error(`Error fetching module ${moduleId}:`, error);
            throw error;
        }
    },

    async createModule(moduleData) {
        try {
            const response = await apiClient.post('/api/modules', moduleData);
            return response.data;
        } catch (error) {
            console.error('Error creating module:', error);
            throw error;
        }
    },

    async updateModule(moduleId, moduleData) {
        try {
            const response = await apiClient.put(`/api/modules/${moduleId}`, moduleData);
            return response.data;
        } catch (error) {
            console.error(`Error updating module ${moduleId}:`, error);
            throw error;
        }
    },

    async deleteModule(moduleId) {
        try {
            const response = await apiClient.delete(`/api/modules/${moduleId}`);
            return response.data;
        } catch (error) {
            console.error(`Error deleting module ${moduleId}:`, error);
            throw error;
        }
    }
};

export default moduleService;