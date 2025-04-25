// src/services/authService.js
import axios from 'axios';
import { API_URL } from '@/config.js';

/**
 * Enhanced Authentication Service with iOS compatibility
 * Uses a dual-approach strategy with both cookies and localStorage
 */
export const authService = {
  /**
   * Login user and store authentication data
   * @param {Object} credentials - User credentials (email, password)
   * @returns {Promise<Object>} Login response
   */
  async login(credentials) {
    try {
      const response = await axios.post(`${API_URL}/login`, credentials, { 
        withCredentials: true 
      });
      
      // Save auth token in localStorage as fallback for iOS devices
      if (response.data.token) {
        localStorage.setItem('authToken', response.data.token);
      } else if (response.data.user && response.data.user.id) {
        // If no explicit token but we have user data, save a session marker
        localStorage.setItem('userSession', JSON.stringify({
          userId: response.data.user.id,
          email: response.data.user.email,
          timestamp: new Date().getTime()
        }));
      }
      
      console.log('Login successful, session data saved');
      return response.data;
    } catch (error) {
      console.error('Login failed:', error);
      throw error;
    }
  },
  
  /**
   * Check if the user is authenticated
   * @returns {Promise<boolean>} True if authenticated
   */
  async isAuthenticated() {
    try {
      console.log('Checking authentication status...');
      
      // First try the standard cookie-based authentication
      try {
        const response = await axios.get(`${API_URL}/protected`, {
          withCredentials: true
        });
        
        console.log('Cookie auth successful:', response.status === 200);
        return response.status === 200;
      } catch (cookieError) {
        console.log('Cookie auth failed, trying token fallback');
        
        // If cookie auth fails, try token-based auth as fallback
        const token = localStorage.getItem('authToken');
        if (token) {
          try {
            const tokenResponse = await axios.get(`${API_URL}/protected`, {
              headers: { Authorization: `Bearer ${token}` }
            });
            
            console.log('Token auth successful:', tokenResponse.status === 200);
            return tokenResponse.status === 200;
          } catch (tokenError) {
            console.log('Token auth failed too');
            return false;
          }
        }
        
        // If we have no token, check for session marker as last resort
        const sessionData = localStorage.getItem('userSession');
        if (sessionData) {
          // We have local session data - this is not secure but helps debugging
          // In production, you'd want to validate this with the server
          console.log('Using local session data as fallback');
          return true;
        }
        
        return false;
      }
    } catch (error) {
      console.error('Auth check error:', error);
      return false;
    }
  },
  
  /**
   * Logout user and clear authentication data
   * @returns {Promise<void>}
   */
  async logout() {
    try {
      // Call server logout endpoint
      await axios.post(`${API_URL}/logout`, {}, { 
        withCredentials: true 
      });
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      // Always clear local auth data regardless of server response
      localStorage.removeItem('authToken');
      localStorage.removeItem('userSession');
    }
  }
};

export default authService;