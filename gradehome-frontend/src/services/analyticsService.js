// src/services/analyticsService.js
import apiClient from './apiService';

const analyticsService = {
  /**
   * Get overview of all universities with student counts and degrees
   * @returns {Promise<Array>} List of universities with analytics data
   */
  async getUniversitiesOverview() {
    try {
      const response = await apiClient.get('/api/analytics/universities');
      return response.data;
    } catch (error) {
      console.error('Error fetching universities analytics:', error);
      throw error;
    }
  },
  
  /**
   * Get details for a specific degree within a university
   * @param {string} university - The university name
   * @param {string} degree - The degree name
   * @returns {Promise<Object>} Degree details with module analytics
   */
  async getDegreeDetails(university, degree) {
    try {
      const response = await apiClient.get('/api/analytics/university/degree', { 
        params: { university, degree }
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching degree analytics:', error);
      throw error;
    }
  },
  
  /**
   * Get detailed analytics for a specific module
   * @param {string} moduleId - The unique module identifier
   * @returns {Promise<Object>} Module analytics details including grade distribution
   */
  async getModuleDetails(moduleId) {
    try {
      const response = await apiClient.get('/api/analytics/module', { 
        params: { module_id: moduleId }
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching module analytics:', error);
      throw error;
    }
  },

  /**
   * Update university module data when a student adds/updates a module
   * This is automatically called by the backend when modules are updated,
   * but can be called directly for analytics-specific updates
   * @param {Object} moduleData - The module data to update analytics for
   * @returns {Promise<Object>} Updated analytics data
   */
  async updateModuleAnalytics(moduleData) {
    try {
      const response = await apiClient.post('/api/analytics/update-module', moduleData);
      return response.data;
    } catch (error) {
      console.error('Error updating module analytics:', error);
      throw error;
    }
  }
};

export default analyticsService;