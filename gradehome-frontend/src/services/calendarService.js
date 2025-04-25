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