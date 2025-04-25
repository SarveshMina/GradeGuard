// Service for all GradeRadar API calls
import apiClient from './apiService';

export const gradeRadarService = {
  // Get universities
  getUniversities() {
    return apiClient.get('/graderadar/universities');
  },
  
  // Get university degrees
  getUniversityDegrees(university) {
    return apiClient.get(`/graderadar/university/degrees?university=${encodeURIComponent(university)}`);
  },
  
  // Get modules for a degree
  getDegreeModules(university, degree) {
    return apiClient.get(`/graderadar/modules?university=${encodeURIComponent(university)}&degree=${encodeURIComponent(degree)}`);
  },
  
  // Get module details
  getModuleDetails(moduleId) {
    return apiClient.get(`/graderadar/module?module_id=${moduleId}`);
  },
  
  // Submit review
  submitReview(reviewData) {
    return apiClient.post('/graderadar/reviews', reviewData);
  },
  
  // Delete review
  deleteReview(reviewId) {
    return apiClient.delete(`/graderadar/reviews/${reviewId}`);
  },
  
  // Get user's reviews
  getUserReviews() {
    return apiClient.get('/graderadar/user/reviews');
  },
  
  // Get module suggestions
  getModuleSuggestions(query) {
    return apiClient.get(`/modules/suggestions?query=${encodeURIComponent(query)}`);
  },
  
  // Get anonymous module suggestions
  getAnonymousModuleSuggestions(university, query) {
    return apiClient.get(`/modules/suggestions/anonymous?university=${encodeURIComponent(university)}&query=${encodeURIComponent(query)}`);
  },

  // NEW METHODS FOR GRADERADAR INTEGRATION

  /**
   * Search for modules based on criteria
   * @param {Object} params - Search parameters (university, degree, code, name)
   * @returns {Promise} Promise with search results
   */
  searchModules(params) {
    // Convert params object to query string
    const queryParams = new URLSearchParams();
    if (params.university) queryParams.append('university', params.university);
    if (params.degree) queryParams.append('degree', params.degree);
    if (params.code) queryParams.append('code', params.code);
    if (params.name) queryParams.append('name', params.name);
    
    return apiClient.get(`/graderadar/search/modules?${queryParams.toString()}`);
  },

  /**
   * Add a new module to GradeRadar
   * @param {Object} moduleData - The module data to add
   * @returns {Promise} Promise with the created module
   */
  addModule(moduleData) {
    return apiClient.post('/graderadar/modules', moduleData);
  },

  /**
   * Update module details
   * @param {string} moduleId - The ID of the module to update
   * @param {Object} moduleData - The updated module data
   * @returns {Promise} Promise with the updated module
   */
  updateModule(moduleId, moduleData) {
    return apiClient.put(`/graderadar/modules/${moduleId}`, moduleData);
  },

  /**
   * Get user's GradeRadar profile
   * @returns {Promise} Promise with user's profile data
   */
  getUserProfile() {
    return apiClient.get('/graderadar/user/profile');
  },

  /**
   * Update user's GradeRadar profile
   * @param {Object} profileData - The profile data to update
   * @returns {Promise} Promise with the updated profile
   */
  updateUserProfile(profileData) {
    return apiClient.put('/graderadar/user/profile', profileData);
  },
  
  /**
   * Get community statistics
   * @returns {Promise} Promise with community statistics
   */
  getCommunityStats() {
    return apiClient.get('/graderadar/stats');
  },
  
  /**
   * Check if a module exists in GradeRadar
   * @param {string} moduleCode - The module code
   * @param {string} university - The university name
   * @returns {Promise} Promise with the module if it exists
   */
  checkModuleExists(moduleCode, university) {
    return apiClient.get(`/graderadar/module/check?code=${encodeURIComponent(moduleCode)}&university=${encodeURIComponent(university)}`);
  },
  
  /**
   * Get reviews for a specific module
   * @param {string} moduleId - The ID of the module
   * @returns {Promise} Promise with the module reviews
   */
  getModuleReviews(moduleId) {
    return apiClient.get(`/graderadar/module/${moduleId}/reviews`);
  }
};

export default gradeRadarService;