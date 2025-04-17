// src/services/studyHubService.js
import { apiClient } from '@/services/apiService';

const studyHubService = {
    // Schedule methods
    getSchedules: async () => {
        try {
            const response = await apiClient.get('/api/study/schedules');
            return response.data;
        } catch (error) {
            console.error('Error fetching schedules:', error);
            throw error;
        }
    },

    createSchedule: async (scheduleData) => {
        try {
            const response = await apiClient.post('/api/study/schedules/create', scheduleData);
            return response.data;
        } catch (error) {
            console.error('Error creating schedule:', error);
            throw error;
        }
    },

    generateAISchedule: async (scheduleData) => {
        try {
            const response = await apiClient.post('/api/study/schedules/generate', scheduleData);
            return response.data;
        } catch (error) {
            console.error('Error generating AI schedule:', error);
            throw error;
        }
    },

    updateSchedule: async (scheduleId, updateData) => {
        try {
            const response = await apiClient.put(`/api/study/schedules/${scheduleId}`, updateData);
            return response.data;
        } catch (error) {
            console.error('Error updating schedule:', error);
            throw error;
        }
    },

    deleteSchedule: async (scheduleId) => {
        try {
            const response = await apiClient.delete(`/api/study/schedules/${scheduleId}`);
            return response.data;
        } catch (error) {
            console.error('Error deleting schedule:', error);
            throw error;
        }
    },

    // Session methods
    getSessions: async (startDate, endDate) => {
        try {
            let url = '/api/study/sessions';
            if (startDate && endDate) {
                url += `?start_date=${startDate}&end_date=${endDate}`;
            }
            const response = await apiClient.get(url);
            return response.data;
        } catch (error) {
            console.error('Error fetching sessions:', error);
            throw error;
        }
    },

    startSession: async (sessionId) => {
        try {
            const response = await apiClient.post(`/api/study/sessions/${sessionId}/start`);
            return response.data;
        } catch (error) {
            console.error('Error starting session:', error);
            throw error;
        }
    },

    completeSession: async (sessionId, feedbackData) => {
        try {
            const response = await apiClient.post(`/api/study/sessions/${sessionId}/complete`, feedbackData);
            return response.data;
        } catch (error) {
            console.error('Error completing session:', error);
            throw error;
        }
    },

    rescheduleSession: async (sessionId, rescheduleData) => {
        try {
            const response = await apiClient.post(`/api/study/sessions/${sessionId}/reschedule`, rescheduleData);
            return response.data;
        } catch (error) {
            console.error('Error rescheduling session:', error);
            throw error;
        }
    },

    // Achievements and Analytics
    getAchievements: async () => {
        try {
            const response = await apiClient.get('/api/study/achievements');
            return response.data;
        } catch (error) {
            console.error('Error fetching achievements:', error);
            throw error;
        }
    },

    getStreak: async () => {
        try {
            const response = await apiClient.get('/api/study/streak');
            return response.data;
        } catch (error) {
            console.error('Error fetching streak data:', error);
            throw error;
        }
    },

    getAnalytics: async () => {
        try {
            const response = await apiClient.get('/api/study/analytics');
            return response.data;
        } catch (error) {
            console.error('Error fetching analytics data:', error);
            throw error;
        }
    },

    // AI Tips
    getTips: async () => {
        try {
            const response = await apiClient.get('/api/study/tips');
            return response.data;
        } catch (error) {
            console.error('Error fetching AI tips:', error);
            throw error;
        }
    },

    acceptTip: async (tipId) => {
        try {
            const response = await apiClient.post(`/api/study/tips/${tipId}/accept`);
            return response.data;
        } catch (error) {
            console.error('Error accepting tip:', error);
            throw error;
        }
    },

    rejectTip: async (tipId) => {
        try {
            const response = await apiClient.post(`/api/study/tips/${tipId}/reject`);
            return response.data;
        } catch (error) {
            console.error('Error rejecting tip:', error);
            throw error;
        }
    }
};

export default studyHubService;