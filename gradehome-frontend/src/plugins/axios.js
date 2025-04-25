// src/plugins/axios.js
import axios from 'axios';

/**
 * Configure Axios with enhanced interceptors for iOS compatibility
 * This will automatically add token authentication as fallback when cookies don't work
 */
export function setupAxios() {
  // Set default settings
  axios.defaults.withCredentials = true;
  
  // Request interceptor
  axios.interceptors.request.use(config => {
    // Log request for debugging
    if (import.meta.env.DEV) {
      console.log(`Request to ${config.url}`, config);
    }
    
    // Check if this is an API call
    if (config.url && config.url.includes('/api/')) {
      // If Authorization header isn't already set, try to add token from localStorage
      if (!config.headers.Authorization) {
        const token = localStorage.getItem('authToken');
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
          if (import.meta.env.DEV) {
            console.log('Added fallback token to request');
          }
        }
      }
    }
    
    return config;
  }, error => {
    console.error('Request error:', error);
    return Promise.reject(error);
  });
  
  // Response interceptor
  axios.interceptors.response.use(response => {
    // Log response for debugging
    if (import.meta.env.DEV) {
      console.log(`Response from ${response.config.url}`, response);
    }
    
    // Check for authentication token in response and save it
    if (response.data && response.data.token) {
      localStorage.setItem('authToken', response.data.token);
    }
    
    return response;
  }, error => {
    // Log error for debugging
    if (import.meta.env.DEV) {
      console.error('Response error:', error.response || error);
    }
    
    // Handle session expiration (401 errors)
    if (error.response && error.response.status === 401) {
      // Clear local authentication data
      localStorage.removeItem('authToken');
      localStorage.removeItem('userSession');
      
      // If not already on login page, redirect there
      const currentPath = window.location.pathname;
      if (!currentPath.includes('/login')) {
        window.location.href = '/login?session=expired';
      }
    }
    
    return Promise.reject(error);
  });
}

export default setupAxios;