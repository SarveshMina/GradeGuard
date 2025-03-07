<template>
  <div class="calendar-sidebar">
    <div class="sidebar-header">
      <h2>Calendar</h2>
      <div class="month-navigator">
        <button @click="previousMonth" class="nav-btn">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M15 18l-6-6 6-6" />
          </svg>
        </button>
        <span class="current-month">{{ formatMonthYear(currentDate) }}</span>
        <button @click="nextMonth" class="nav-btn">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M9 18l6-6-6-6" />
          </svg>
        </button>
      </div>
    </div>

    <!-- Calendar -->
    <div class="calendar-wrapper">
      <vc-calendar
          v-model="currentDate"
          is-inline
          @dayclick="onDayClick"
          class="custom-calendar"
          :attributes="calendarAttributes"
      />
    </div>

    <!-- Today's Quick View -->
    <div class="today-summary">
      <div class="date-pill">Today</div>
      <div class="quick-stats">
        <div class="stat-item">
          <div class="stat-value">{{ todayEvents.length }}</div>
          <div class="stat-label">Events</div>
        </div>
        <div class="stat-item">
          <div class="stat-value">{{ calculateStudyHours() }}h</div>
          <div class="stat-label">Study</div>
        </div>
      </div>
    </div>

    <!-- Events section -->
    <div v-if="activeDate" class="events-container">
      <div class="events-header">
        <h3>{{ formatDate(activeDate) }}</h3>
        <button @click="openCreateEventModal" class="add-event-btn" title="Add new event">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="12" y1="5" x2="12" y2="19"></line>
            <line x1="5" y1="12" x2="19" y2="12"></line>
          </svg>
        </button>
      </div>

      <div v-if="loadingEvents" class="loading-events">
        <div class="loading-spinner"></div>
        <p>Loading events...</p>
      </div>

      <div v-else-if="eventsForSelectedDate.length === 0" class="no-events">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="empty-icon">
          <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
          <line x1="16" y1="2" x2="16" y2="6"></line>
          <line x1="8" y1="2" x2="8" y2="6"></line>
          <line x1="3" y1="10" x2="21" y2="10"></line>
        </svg>
        <p>No events scheduled for this day</p>
        <button @click="openCreateEventModal('study')" class="schedule-btn">Schedule Study Time</button>
      </div>

      <div v-else class="events-list">
        <div
            v-for="event in eventsForSelectedDate"
            :key="event.id"
            class="event-card"
            :class="getEventClass(event)"
        >
          <div class="event-dot"></div>
          <div class="event-content">
            <div class="event-time">
              {{ formatEventTime(event) }}
            </div>
            <div class="event-title">{{ event.title }}</div>
            <div class="event-description">{{ event.description }}</div>
          </div>
          <div class="event-actions">
            <button @click="openEditEventModal(event)" class="action-btn edit-btn" title="Edit event">
              <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
              </svg>
            </button>
            <button @click="confirmDeleteEvent(event)" class="action-btn delete-btn" title="Delete event">
              <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="3 6 5 6 21 6"></polyline>
                <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                <line x1="10" y1="11" x2="10" y2="17"></line>
                <line x1="14" y1="11" x2="14" y2="17"></line>
              </svg>
            </button>
            <button
                @click="toggleEventCompletion(event)"
                class="action-btn complete-btn"
                :class="{ 'completed': event.completed }"
                :title="event.completed ? 'Mark as incomplete' : 'Mark as complete'"
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Event Form Modal (Create/Edit) -->
    <div v-if="showEventModal" class="modal-overlay" @click.self="closeEventModal">
      <div class="modal-container">
        <div class="modal-header">
          <h2>{{ editMode ? 'Edit Event' : 'Create New Event' }}</h2>
          <button @click="closeEventModal" class="close-btn">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="saveEvent">
            <div class="form-group">
              <label for="event-title">Event Title*</label>
              <input
                  type="text"
                  id="event-title"
                  v-model="eventForm.title"
                  placeholder="Enter event title"
                  required
              />
            </div>

            <div class="form-group">
              <label for="event-description">Description</label>
              <textarea
                  id="event-description"
                  v-model="eventForm.description"
                  placeholder="Enter event description"
                  rows="3"
              ></textarea>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label for="event-date">Date*</label>
                <input
                    type="date"
                    id="event-date"
                    v-model="eventForm.date"
                    required
                />
              </div>

              <div class="form-group">
                <label for="event-type">Event Type*</label>
                <select id="event-type" v-model="eventForm.type" required>
                  <option value="general">General</option>
                  <option value="study">Study Session</option>
                  <option value="assignment">Assignment</option>
                  <option value="exam">Exam</option>
                  <option value="meeting">Meeting</option>
                </select>
              </div>
            </div>

            <div class="form-group">
              <div class="checkbox-group">
                <input type="checkbox" id="all-day" v-model="eventForm.all_day">
                <label for="all-day">All Day Event</label>
              </div>
            </div>

            <div v-if="!eventForm.all_day" class="form-row">
              <div class="form-group">
                <label for="start-time">Start Time*</label>
                <input
                    type="time"
                    id="start-time"
                    v-model="eventForm.start_time"
                    :required="!eventForm.all_day"
                />
              </div>

              <div class="form-group">
                <label for="end-time">End Time*</label>
                <input
                    type="time"
                    id="end-time"
                    v-model="eventForm.end_time"
                    :required="!eventForm.all_day"
                />
              </div>
            </div>

            <div class="form-group">
              <label for="event-color">Color</label>
              <div class="color-picker">
                <div
                    v-for="color in availableColors"
                    :key="color.value"
                    class="color-option"
                    :class="{ active: eventForm.color === color.value }"
                    :style="{ backgroundColor: color.value }"
                    @click="eventForm.color = color.value"
                ></div>
              </div>
            </div>

            <div class="form-actions">
              <button type="button" @click="closeEventModal" class="cancel-btn">Cancel</button>
              <button type="submit" class="save-btn" :disabled="submitting">
                <span v-if="submitting">Saving...</span>
                <span v-else>{{ editMode ? 'Update Event' : 'Create Event' }}</span>
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Confirmation Modal for Delete -->
    <div v-if="showDeleteConfirmation" class="modal-overlay" @click.self="showDeleteConfirmation = false">
      <div class="modal-container confirmation-modal">
        <div class="modal-header">
          <h2>Confirm Delete</h2>
          <button @click="showDeleteConfirmation = false" class="close-btn">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>
        <div class="modal-body">
          <p>Are you sure you want to delete this event?</p>
          <div class="event-to-delete" v-if="eventToDelete">
            <div class="event-title">{{ eventToDelete.title }}</div>
            <div class="event-date">{{ formatDate(new Date(eventToDelete.date)) }}</div>
          </div>
          <div class="confirmation-actions">
            <button @click="showDeleteConfirmation = false" class="cancel-btn">Cancel</button>
            <button @click="deleteEvent" class="delete-confirm-btn" :disabled="deleting">
              <span v-if="deleting">Deleting...</span>
              <span v-else>Delete Event</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { notify } from '@/services/toastService.js';
import { API_URL } from '@/config.js';

export default {
  name: 'CalendarSidebar',
  props: {
    // The events array can be passed from parent
    events: {
      type: Array,
      default: () => []
    },
    // Optional selected date from parent (for synchronization)
    selectedDate: {
      type: Date,
      default: null
    }
  },
  data() {
    return {
      currentDate: new Date(),
      internalSelectedDate: new Date(), // Internal date for when no prop is provided
      loadingEvents: false,
      showEventModal: false,
      editMode: false,
      eventToEdit: null,
      submitting: false,
      showDeleteConfirmation: false,
      eventToDelete: null,
      deleting: false,
      availableColors: [
        { name: 'Purple', value: '#7b49ff' },
        { name: 'Blue', value: '#2196f3' },
        { name: 'Green', value: '#4caf50' },
        { name: 'Red', value: '#f44336' },
        { name: 'Orange', value: '#ff9100' },
        { name: 'Pink', value: '#e91e63' },
        { name: 'Teal', value: '#009688' }
      ],
      eventForm: {
        title: '',
        description: '',
        date: '',
        type: 'general',
        all_day: true,
        start_time: '09:00',
        end_time: '10:00',
        color: '#7b49ff',
        completed: false
      },
      internalEvents: [] // Used when no events prop is provided
    }
  },
  computed: {
    // Use the selected date from props if available, otherwise use internal
    activeDate() {
      return this.selectedDate || this.internalSelectedDate;
    },

    eventsForSelectedDate() {
      if (!this.activeDate) return [];

      const dateString = this.formatDateISO(this.activeDate);
      // Use events from props if available, otherwise use internal events
      const eventsArray = this.events.length > 0 ? this.events : this.internalEvents;
      return eventsArray.filter(event => event.date === dateString);
    },

    todayEvents() {
      const today = this.formatDateISO(new Date());
      // Use events from props if available, otherwise use internal events
      const eventsArray = this.events.length > 0 ? this.events : this.internalEvents;
      return eventsArray.filter(event => event.date === today);
    },

    calendarAttributes() {
      // Create attributes for calendar dots and highlights
      const attributes = [];

      // Add highlight for the actively selected date
      attributes.push({
        dates: this.activeDate,
        highlight: {
          color: 'purple',
          fillMode: 'light'
        }
      });

      // Group events by date
      const eventsArray = this.events.length > 0 ? this.events : this.internalEvents;
      const eventsByDate = {};

      eventsArray.forEach(event => {
        if (!eventsByDate[event.date]) {
          eventsByDate[event.date] = [];
        }
        eventsByDate[event.date].push(event);
      });

      // Create dot attributes for dates with events
      Object.keys(eventsByDate).forEach(date => {
        const events = eventsByDate[date];

        // Get event counts and types for styling
        const count = events.length;
        const hasCompleted = events.some(e => e.completed);
        const hasIncomplete = events.some(e => !e.completed);

        // Create dot color based on count and completion status
        let dotColor = '#7b49ff'; // Default purple

        if (count > 3) {
          dotColor = '#7b49ff'; // Keep purple for many events
        } else if (hasCompleted && !hasIncomplete) {
          dotColor = '#4caf50'; // All completed = green
        } else if (hasCompleted && hasIncomplete) {
          dotColor = '#ff9100'; // Some completed = orange
        }

        attributes.push({
          dates: new Date(date),
          dot: {
            color: dotColor,
            className: count > 3 ? 'event-dot-highlight' : ''
          }
        });
      });

      return attributes;
    }
  },
  watch: {
    // Watch for changes to the selectedDate prop
    selectedDate(newDate) {
      if (newDate) {
        // Update the calendar current date if month/year changes
        const currentMonth = this.currentDate.getMonth();
        const selectedMonth = newDate.getMonth();
        const currentYear = this.currentDate.getFullYear();
        const selectedYear = newDate.getFullYear();

        if (currentMonth !== selectedMonth || currentYear !== selectedYear) {
          this.currentDate = new Date(newDate);
        }
      }
    }
  },
  async mounted() {
    // Select today's date by default
    this.onDayClick({ date: new Date() });

    // If we're not using the events prop, fetch events
    if (this.events.length === 0) {
      await this.fetchEvents();
    }
  },
  methods: {
    async fetchEvents(startDate = null, endDate = null) {
      // Only fetch if we're not using the events prop
      if (this.events.length > 0) return;

      try {
        this.loadingEvents = true;
        let url = `${API_URL}/calendar/events`;

        // Add date range parameters if provided
        const params = new URLSearchParams();
        if (startDate) params.append('start_date', startDate);
        if (endDate) params.append('end_date', endDate);

        if (params.toString()) {
          url += `?${params.toString()}`;
        }

        const response = await axios.get(url, { withCredentials: true });
        this.internalEvents = response.data;
      } catch (error) {
        console.error('Error fetching events:', error);
        notify({ type: 'error', message: 'Failed to load events. Please try again.' });
      } finally {
        this.loadingEvents = false;
      }
    },

    onDayClick({ date }) {
      if (this.selectedDate) {
        // If we're using props, emit the event to parent
        this.$emit('day-click', date);
      } else {
        // Otherwise update our internal state
        this.internalSelectedDate = date;
      }

      // If month has changed, fetch events for the new month
      const currentMonth = this.currentDate.getMonth();
      const selectedMonth = date.getMonth();

      if (currentMonth !== selectedMonth && this.events.length === 0) {
        const firstDay = new Date(date.getFullYear(), date.getMonth(), 1);
        const lastDay = new Date(date.getFullYear(), date.getMonth() + 1, 0);

        this.fetchEvents(
            this.formatDateISO(firstDay),
            this.formatDateISO(lastDay)
        );
      }
    },

    openCreateEventModal(type = 'general') {
      // Check if we're in parent-controlled mode
      if (this.events.length > 0) {
        // Emit event to parent
        this.$emit('add-event', type);
        return;
      }

      // Otherwise handle internally
      this.editMode = false;
      this.eventToEdit = null;

      // Reset form with defaults
      this.eventForm = {
        title: '',
        description: '',
        date: this.formatDateISO(this.activeDate),
        type: type || 'general',
        all_day: true,
        start_time: '09:00',
        end_time: '10:00',
        color: '#7b49ff',
        completed: false
      };

      this.showEventModal = true;
    },

    openEditEventModal(event) {
      // Check if we're in parent-controlled mode
      if (this.events.length > 0) {
        // Emit event to parent
        this.$emit('edit-event', event);
        return;
      }

      // Otherwise handle internally
      this.editMode = true;
      this.eventToEdit = event;

      // Populate form with event data
      this.eventForm = {
        title: event.title,
        description: event.description || '',
        date: event.date,
        type: event.type || 'general',
        all_day: event.all_day,
        start_time: event.start_time || '09:00',
        end_time: event.end_time || '10:00',
        color: event.color || '#7b49ff',
        completed: event.completed || false
      };

      this.showEventModal = true;
    },

    closeEventModal() {
      this.showEventModal = false;
      this.editMode = false;
      this.eventToEdit = null;
    },

    async saveEvent() {
      // Only handle if we're not using parent events
      if (this.events.length > 0) return;

      try {
        this.submitting = true;

        // Prepare event data
        const eventData = {
          title: this.eventForm.title,
          description: this.eventForm.description,
          date: this.eventForm.date,
          type: this.eventForm.type,
          all_day: this.eventForm.all_day,
          completed: this.eventForm.completed,
          color: this.eventForm.color
        };

        // Add time fields if not an all-day event
        if (!this.eventForm.all_day) {
          eventData.start_time = this.eventForm.start_time;
          eventData.end_time = this.eventForm.end_time;
        }

        let response;

        if (this.editMode && this.eventToEdit) {
          // Update existing event
          response = await axios.put(
              `${API_URL}/calendar/events/${this.eventToEdit.id}`,
              eventData,
              { withCredentials: true }
          );

          // Update local state
          const index = this.internalEvents.findIndex(e => e.id === this.eventToEdit.id);
          if (index !== -1) {
            this.internalEvents[index] = response.data;
          }

          notify({ type: 'success', message: 'Event updated successfully!' });
        } else {
          // Create new event
          response = await axios.post(
              `${API_URL}/calendar/events`,
              eventData,
              { withCredentials: true }
          );

          // Add to local state
          this.internalEvents.push(response.data);

          notify({ type: 'success', message: 'Event created successfully!' });
        }

        // Close the modal
        this.closeEventModal();
      } catch (error) {
        console.error('Error saving event:', error);
        notify({ type: 'error', message: 'Failed to save event. Please try again.' });
      } finally {
        this.submitting = false;
      }
    },

    confirmDeleteEvent(event) {
      // Check if we're in parent-controlled mode
      if (this.events.length > 0) {
        // Emit event to parent
        this.$emit('delete-event', event);
        return;
      }

      // Otherwise handle internally
      this.eventToDelete = event;
      this.showDeleteConfirmation = true;
    },

    async deleteEvent() {
      // Only handle if we're not using parent events
      if (this.events.length > 0 || !this.eventToDelete) return;

      try {
        this.deleting = true;

        await axios.delete(
            `${API_URL}/calendar/events/${this.eventToDelete.id}`,
            { withCredentials: true }
        );

        // Remove from local events array
        this.internalEvents = this.internalEvents.filter(e => e.id !== this.eventToDelete.id);

        notify({ type: 'success', message: 'Event deleted successfully!' });

        // Close confirmation modal
        this.showDeleteConfirmation = false;
        this.eventToDelete = null;
      } catch (error) {
        console.error('Error deleting event:', error);
        notify({ type: 'error', message: 'Failed to delete event. Please try again.' });
      } finally {
        this.deleting = false;
      }
    },

    async toggleEventCompletion(event) {
      // Check if we're in parent-controlled mode
      if (this.events.length > 0) {
        // Emit event to parent
        this.$emit('toggle-completion', event);
        return;
      }

      try {
        const updatedEvent = { ...event, completed: !event.completed };

        await axios.put(
            `${API_URL}/calendar/events/${event.id}`,
            updatedEvent,
            { withCredentials: true }
        );

        // Update local state
        const index = this.internalEvents.findIndex(e => e.id === event.id);
        if (index !== -1) {
          this.internalEvents[index].completed = !event.completed;
        }

        notify({
          type: 'success',
          message: updatedEvent.completed ? 'Event marked as completed!' : 'Event marked as incomplete!'
        });
      } catch (error) {
        console.error('Error updating event completion:', error);
        notify({ type: 'error', message: 'Failed to update event. Please try again.' });
      }
    },

    formatDate(date) {
      if (!date) return '';
      return new Date(date).toLocaleDateString('en-US', {
        weekday: 'long',
        month: 'long',
        day: 'numeric'
      });
    },

    formatMonthYear(date) {
      if (!date) return '';
      return new Date(date).toLocaleDateString('en-US', {
        month: 'long',
        year: 'numeric'
      });
    },

    formatDateISO(date) {
      if (!date) return '';
      const d = new Date(date);
      return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
    },

    formatEventTime(event) {
      if (event.all_day) return 'All Day';

      return `${this.formatTime(event.start_time)} - ${this.formatTime(event.end_time)}`;
    },

    formatTime(timeString) {
      if (!timeString) return '';

      // Convert 24-hour time format to 12-hour format with AM/PM
      const [hours, minutes] = timeString.split(':');
      const hour = parseInt(hours, 10);
      const period = hour >= 12 ? 'PM' : 'AM';
      const hour12 = hour % 12 || 12;
      return `${hour12}:${minutes} ${period}`;
    },

    getEventClass(event) {
      // Return CSS class based on event type
      const typeMap = {
        'celebration': 'celebration-event',
        'meeting': 'meeting-event',
        'assignment': 'assignment-event',
        'study': 'study-event',
        'exam': 'exam-event',
        'general': 'general-event'
      };

      const baseClass = typeMap[event.type] || 'general-event';
      return {
        [baseClass]: true,
        'completed-event': event.completed
      };
    },

    calculateStudyHours() {
      // Use the appropriate events array
      const eventsArray = this.events.length > 0 ? this.events : this.internalEvents;

      // Calculate study hours for today
      return eventsArray
          .filter(event => event.type === 'study' && !event.all_day)
          .reduce((total, event) => {
            if (!event.start_time || !event.end_time) return total;

            const start = event.start_time.split(':').map(Number);
            const end = event.end_time.split(':').map(Number);
            const hours = end[0] - start[0] + (end[1] - start[1]) / 60;
            return total + (hours > 0 ? hours : 0);
          }, 0)
          .toFixed(1);
    },

    previousMonth() {
      const date = new Date(this.currentDate);
      date.setMonth(date.getMonth() - 1);
      this.currentDate = date;

      // Only fetch events if we're not using parent's events
      if (this.events.length === 0) {
        // Fetch events for the new month
        const firstDay = new Date(date.getFullYear(), date.getMonth(), 1);
        const lastDay = new Date(date.getFullYear(), date.getMonth() + 1, 0);

        this.fetchEvents(
            this.formatDateISO(firstDay),
            this.formatDateISO(lastDay)
        );
      }
    },

    nextMonth() {
      const date = new Date(this.currentDate);
      date.setMonth(date.getMonth() + 1);
      this.currentDate = date;

      // Only fetch events if we're not using parent's events
      if (this.events.length === 0) {
        // Fetch events for the new month
        const firstDay = new Date(date.getFullYear(), date.getMonth(), 1);
        const lastDay = new Date(date.getFullYear(), date.getMonth() + 1, 0);

        this.fetchEvents(
            this.formatDateISO(firstDay),
            this.formatDateISO(lastDay)
        );
      }
    }
  }
}
</script>

<style scoped>
/* Enhanced Calendar Sidebar Styles */
:root {
  --primary-color: #673ab7;
  --primary-dark: #512da8;
  --primary-light: #9575cd;
  --primary-color-transparent: rgba(103, 58, 183, 0.15);
  --primary-gradient: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-dark) 100%);
  --text-primary: #333333;
  --text-secondary: #666666;
  --text-muted: #888888;
  --border-color: #e0e0e0;
  --bg-light: #ffffff;
  --bg-card: #ffffff;
  --bg-input: #f5f7fa;
  --bg-muted: #f0f0f0;
  --bg-hover: #f9f9f9;
  --success-color: #4caf50;
  --warning-color: #ff9800;
  --error-color: #f44336;
  --transition-speed: 0.3s;
  --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 16px rgba(0, 0, 0, 0.1);
  --shadow-lg: 0 8px 24px rgba(0, 0, 0, 0.12);
  --border-radius: 12px;
  --border-radius-lg: 16px;
  --font-family: 'Montserrat', sans-serif;
}

.dark-mode {
  --text-primary: #f5f7fa;
  --text-secondary: #d0d0d0;
  --text-muted: #a0a0a0;
  --border-color: #3f4156;
  --bg-light: #232535;
  --bg-card: #2a2d3e;
  --bg-input: #1e2030;
  --bg-muted: #323546;
  --bg-hover: #3c4052;
  --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.2);
  --shadow-md: 0 4px 16px rgba(0, 0, 0, 0.3);
  --shadow-lg: 0 8px 24px rgba(0, 0, 0, 0.4);
}

.calendar-sidebar {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  padding: 1.5rem;
  background-color: var(--bg-light);
  border-radius: var(--border-radius);
  box-shadow: var(--shadow-md);
  height: 100%;
  overflow-y: auto;
  transition: all 0.3s ease;
  position: relative;
  scrollbar-width: thin;
  scrollbar-color: var(--border-color) transparent;
}

.calendar-sidebar::-webkit-scrollbar {
  width: 6px;
}

.calendar-sidebar::-webkit-scrollbar-track {
  background: transparent;
}

.calendar-sidebar::-webkit-scrollbar-thumb {
  background-color: var(--border-color);
  border-radius: 6px;
}

.calendar-sidebar::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 4px;
  background: var(--primary-gradient);
  border-top-left-radius: var(--border-radius);
  border-top-right-radius: var(--border-radius);
}

/* Header styling */
.sidebar-header {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  position: relative;
}

.sidebar-header h2 {
  margin: 0;
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--primary-dark);
  transition: all 0.3s ease;
  position: relative;
  display: inline-block;
  width: fit-content;
}

.sidebar-header h2::after {
  content: '';
  position: absolute;
  left: 0;
  bottom: -4px;
  width: 40px;
  height: 3px;
  background: var(--primary-gradient);
  border-radius: 2px;
}

.month-navigator {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin: 0.5rem 0 1rem;
  background-color: var(--bg-card);
  border-radius: var(--border-radius);
  padding: 0.5rem;
  box-shadow: var(--shadow-sm);
  transition: all 0.3s ease;
}

.month-navigator:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
}

.current-month {
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--primary-dark);
  transition: color 0.3s ease;
  padding: 0.25rem 0.75rem;
  background-color: var(--bg-input);
  border-radius: 20px;
}

.nav-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 38px;
  height: 38px;
  border: none;
  background-color: var(--bg-input);
  color: var(--primary-color);
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  position: relative;
  overflow: hidden;
}

.nav-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle, rgba(103, 58, 183, 0.2) 0%, rgba(255, 255, 255, 0) 70%);
  opacity: 0;
  transform: scale(0);
  transition: transform 0.4s ease, opacity 0.4s ease;
}

.nav-btn:hover::before {
  transform: scale(1.5);
  opacity: 1;
}

.nav-btn:hover {
  background-color: var(--primary-color-transparent);
  transform: scale(1.15);
  box-shadow: 0 4px 10px rgba(103, 58, 183, 0.15);
}

.nav-btn:active {
  transform: scale(0.95);
}

.nav-btn svg {
  position: relative;
  z-index: 1;
  transition: transform 0.3s ease;
}

.nav-btn:hover svg {
  transform: scale(1.1);
}

/* Calendar wrapper */
.calendar-wrapper {
  padding: 0.5rem;
  background-color: var(--bg-card);
  border-radius: var(--border-radius);
  box-shadow: var(--shadow-sm);
  transition: all 0.3s ease;
  overflow: hidden;
}

.calendar-wrapper:hover {
  box-shadow: var(--shadow-md);
}

/* Custom calendar styling */
.custom-calendar {
  font-family: var(--font-family);
  border: none;
  border-radius: var(--border-radius);
  overflow: hidden;
}

/* Today's summary styling */
.today-summary {
  background: var(--primary-gradient);
  border-radius: var(--border-radius);
  padding: 1.25rem;
  color: white;
  box-shadow: 0 8px 20px rgba(103, 58, 183, 0.2);
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease;
}

.today-summary::before {
  content: '';
  position: absolute;
  top: -100px;
  right: -100px;
  width: 200px;
  height: 200px;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.2) 0%, rgba(255, 255, 255, 0) 70%);
  border-radius: 50%;
  opacity: 0;
  transition: opacity 0.5s ease;
}

.today-summary:hover {
  transform: translateY(-5px);
  box-shadow: 0 12px 28px rgba(103, 58, 183, 0.25);
}

.today-summary:hover::before {
  opacity: 1;
}

.date-pill {
  background-color: rgba(255, 255, 255, 0.2);
  border-radius: 20px;
  padding: 0.4rem 1rem;
  font-size: 0.85rem;
  font-weight: 600;
  display: inline-block;
  margin-bottom: 1rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(5px);
  transition: all 0.3s ease;
}

.today-summary:hover .date-pill {
  background-color: rgba(255, 255, 255, 0.3);
  transform: scale(1.05);
}

.quick-stats {
  display: flex;
  justify-content: space-around;
  gap: 1rem;
}

.stat-item {
  text-align: center;
  background-color: rgba(255, 255, 255, 0.1);
  padding: 0.75rem 1rem;
  border-radius: var(--border-radius);
  flex: 1;
  transition: all 0.3s ease;
  backdrop-filter: blur(5px);
}

.stat-item:hover {
  background-color: rgba(255, 255, 255, 0.2);
  transform: translateY(-2px);
}

.stat-value {
  font-size: 1.75rem;
  font-weight: 700;
  line-height: 1.2;
  margin-bottom: 0.25rem;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.stat-label {
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-weight: 500;
  opacity: 0.9;
}

/* Events section styling */
.events-container {
  background-color: var(--bg-card);
  border-radius: var(--border-radius);
  padding: 1.5rem;
  box-shadow: var(--shadow-sm);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.events-container::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 4px;
  height: 100%;
  background: var(--primary-gradient);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.events-container:hover {
  box-shadow: var(--shadow-md);
}

.events-container:hover::before {
  opacity: 1;
}

.events-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.25rem;
}

.events-header h3 {
  margin: 0;
  font-size: 1.15rem;
  font-weight: 600;
  color: var(--primary-dark);
  transition: all 0.3s ease;
  position: relative;
  display: inline-block;
}

.events-header h3::after {
  content: '';
  position: absolute;
  left: 0;
  bottom: -4px;
  width: 0;
  height: 2px;
  background: var(--primary-gradient);
  transition: width 0.3s ease;
}

.events-container:hover .events-header h3::after {
  width: 100%;
}

.add-event-btn {
  width: 42px;
  height: 42px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--primary-color);
  color: white;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  box-shadow: 0 4px 10px rgba(103, 58, 183, 0.2);
  position: relative;
  overflow: hidden;
}

.add-event-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.3) 0%, rgba(255, 255, 255, 0) 70%);
  transform: scale(0);
  transition: transform 0.4s ease;
}

.add-event-btn:hover::before {
  transform: scale(1.5);
}

.add-event-btn:hover {
  background-color: var(--primary-dark);
  transform: scale(1.1) rotate(90deg);
  box-shadow: 0 6px 15px rgba(103, 58, 183, 0.3);
}

.add-event-btn:active {
  transform: scale(0.95);
}

.add-event-btn svg {
  position: relative;
  z-index: 1;
  transition: transform 0.3s ease;
}

/* Loading state */
.loading-events {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2.5rem 0;
  color: var(--text-secondary);
}

.loading-spinner {
  width: 36px;
  height: 36px;
  border: 3px solid rgba(103, 58, 183, 0.15);
  border-radius: 50%;
  border-top-color: var(--primary-color);
  animation: spin 1.2s cubic-bezier(0.68, -0.55, 0.265, 1.55) infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-events p {
  font-size: 0.95rem;
  opacity: 0.8;
  animation: pulse 1.5s infinite alternate;
}

@keyframes pulse {
  0% { opacity: 0.5; }
  100% { opacity: 1; }
}

/* Empty state styling */
.no-events {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  padding: 2rem 0;
  color: var(--text-secondary);
  text-align: center;
}

.empty-icon {
  color: var(--primary-color);
  opacity: 0.6;
  margin-bottom: 0.5rem;
  transition: all 0.3s ease;
  animation: float 3s ease-in-out infinite;
}

@keyframes float {
  0% { transform: translateY(0px); }
  50% { transform: translateY(-10px); }
  100% { transform: translateY(0px); }
}

.no-events p {
  font-size: 0.95rem;
  max-width: 80%;
}

.schedule-btn {
  background-color: var(--primary-color-transparent);
  color: var(--primary-color);
  border: none;
  border-radius: 30px;
  padding: 0.75rem 1.5rem;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: var(--shadow-sm);
  margin-top: 0.5rem;
}

.schedule-btn:hover {
  background-color: var(--primary-color);
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(103, 58, 183, 0.2);
}

.schedule-btn:active {
  transform: translateY(0);
}

/* Event cards styling */
.events-list {
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
}

.event-card {
  display: flex;
  gap: 0.85rem;
  padding: 1rem;
  border-radius: var(--border-radius);
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  position: relative;
  background-color: var(--bg-light);
  box-shadow: var(--shadow-sm);
  border-left: 3px solid transparent;
}

.event-card:hover {
  transform: translateY(-3px) translateX(2px);
  box-shadow: var(--shadow-md);
}

.event-dot {
  width: 14px;
  height: 14px;
  border-radius: 50%;
  margin-top: 4px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.event-card:hover .event-dot {
  transform: scale(1.2);
  box-shadow: 0 3px 8px rgba(0, 0, 0, 0.15);
}

.event-content {
  flex: 1;
  min-width: 0; /* For text truncation to work */
}

.event-time {
  font-size: 0.8rem;
  font-weight: 500;
  color: var(--text-secondary);
  margin-bottom: 0.3rem;
  display: flex;
  align-items: center;
  gap: 0.3rem;
}

.event-time::before {
  content: '⏱️';
  font-size: 0.75rem;
  opacity: 0.7;
}

.event-title {
  font-weight: 600;
  margin-bottom: 0.4rem;
  color: var(--text-primary);
  transition: color 0.3s ease;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.event-card:hover .event-title {
  color: var(--primary-color);
}

.event-description {
  font-size: 0.85rem;
  color: var(--text-secondary);
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* Event type styles */
.celebration-event {
  border-left-color: #ff9100;
}

.celebration-event .event-dot {
  background-color: #ff9100;
}

.meeting-event {
  border-left-color: #7b49ff;
}

.meeting-event .event-dot {
  background-color: #7b49ff;
}

.assignment-event {
  border-left-color: #f44336;
}

.assignment-event .event-dot {
  background-color: #f44336;
}

.study-event {
  border-left-color: #4caf50;
}

.study-event .event-dot {
  background-color: #4caf50;
}

.exam-event {
  border-left-color: #e91e63;
}

.exam-event .event-dot {
  background-color: #e91e63;
}

.general-event {
  border-left-color: #2196f3;
}

.general-event .event-dot {
  background-color: #2196f3;
}

/* Completed event styling */
.completed-event {
  opacity: 0.75;
  background-color: var(--bg-muted);
}

.completed-event .event-title {
  text-decoration: line-through;
}

.completed-event .event-dot {
  background-image: linear-gradient(45deg, transparent 46%, var(--text-muted) 46%, var(--text-muted) 54%, transparent 54%);
  background-size: 8px 8px;
}

/* Event actions */
.event-actions {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  opacity: 0;
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  transform: translateX(10px);
}

.event-card:hover .event-actions {
  opacity: 1;
  transform: translateX(0);
}

.action-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  border: none;
  background-color: var(--bg-input);
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: var(--shadow-sm);
}

.edit-btn {
  color: var(--primary-color);
}

.edit-btn:hover {
  background-color: var(--primary-color-transparent);
  transform: scale(1.1);
}

.delete-btn {
  color: var(--error-color);
}

.delete-btn:hover {
  background-color: rgba(244, 67, 54, 0.15);
  transform: scale(1.1);
}

.complete-btn {
  color: var(--success-color);
}

.complete-btn:hover {
  background-color: rgba(76, 175, 80, 0.15);
  transform: scale(1.1);
}

.complete-btn.completed {
  background-color: var(--success-color);
  color: white;
}

.action-btn svg {
  transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.action-btn:hover svg {
  transform: scale(1.2);
}

/* Modal styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(3px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.modal-container {
  background-color: var(--bg-card);
  border-radius: var(--border-radius-lg);
  width: 90%;
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: var(--shadow-lg);
  animation: modalSlideIn 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  transform-origin: center;
  position: relative;
  display: flex;
  flex-direction: column;
}

.modal-container::-webkit-scrollbar {
  width: 6px;
}

.modal-container::-webkit-scrollbar-track {
  background: transparent;
}

.modal-container::-webkit-scrollbar-thumb {
  background-color: var(--border-color);
  border-radius: 6px;
}

.confirmation-modal {
  max-width: 400px;
}

@keyframes modalSlideIn {
  0% {
    opacity: 0;
    transform: scale(0.9) translateY(20px);
  }
  70% {
    opacity: 1;
    transform: scale(1.02) translateY(-5px);
  }
  100% {
    transform: scale(1) translateY(0);
  }
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid var(--border-color);
  position: sticky;
  top: 0;
  background-color: var(--bg-card);
  z-index: 1;
  border-top-left-radius: var(--border-radius-lg);
  border-top-right-radius: var(--border-radius-lg);
}

.modal-header h2 {
  margin: 0;
  font-size: 1.3rem;
  font-weight: 700;
  color: var(--primary-dark);
  position: relative;
  display: inline-block;
}

.modal-header h2::after {
  content: '';
  position: absolute;
  left: 0;
  bottom: -4px;
  width: 30px;
  height: 3px;
  background: var(--primary-gradient);
  border-radius: 2px;
}

.close-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border: none;
  background-color: var(--bg-input);
  color: var(--text-secondary);
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  box-shadow: var(--shadow-sm);
}

.close-btn:hover {
  background-color: rgba(244, 67, 54, 0.15);
  color: var(--error-color);
  transform: rotate(90deg);
}

.modal-body {
  padding: 1.75rem 1.5rem;
  overflow-y: auto;
  flex: 1;
}

/* Form styles */
.form-group {
  margin-bottom: 1.5rem;
}

.form-row {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.form-row .form-group {
  flex: 1;
  margin-bottom: 0;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: var(--text-primary);
  font-size: 0.9rem;
}

.form-group input,
.form-group textarea,
.form-group select {
  width: 100%;
  padding: 0.9rem 1rem;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  background-color: var(--bg-input);
  color: var(--text-primary);
  font-family: inherit;
  font-size: 0.95rem;
  transition: all 0.3s ease;
  box-shadow: var(--shadow-sm);
}

.form-group input:focus,
.form-group textarea:focus,
.form-group select:focus {
  border-color: var(--primary-color);
  outline: none;
  box-shadow: 0 0 0 3px var(--primary-color-transparent);
}

.checkbox-group {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.5rem 0;
}

.checkbox-group input[type="checkbox"] {
  width: 18px;
  height: 18px;
  margin: 0;
  accent-color: var(--primary-color);
  cursor: pointer;
}

.checkbox-group label {
  margin-bottom: 0;
  cursor: pointer;
}

/* Color picker */
.color-picker {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
  padding: 0.5rem 0;
}

.color-option {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  position: relative;
  box-shadow: var(--shadow-sm);
  border: 2px solid var(--bg-card);
}

.color-option:hover {
  transform: scale(1.15);
  box-shadow: var(--shadow-md);
}

.color-option.active {
  transform: scale(1.15);
  box-shadow: 0 0 0 2px var(--bg-card), 0 0 0 4px var(--primary-color);
}

/* Form actions */
.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 2rem;
}

.cancel-btn, .save-btn, .delete-confirm-btn {
  padding: 0.85rem 1.5rem;
  border-radius: var(--border-radius);
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  font-size: 0.95rem;
  min-width: 120px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.cancel-btn {
  background-color: var(--bg-input);
  color: var(--text-secondary);
  border: 1px solid var(--border-color);
}

.cancel-btn:hover {
  background-color: var(--bg-muted);
  color: var(--text-primary);
  transform: translateY(-2px);
}

.save-btn {
  background: var(--primary-gradient);
  color: white;
  border: none;
  box-shadow: 0 4px 10px rgba(103, 58, 183, 0.2);
}

.save-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 15px rgba(103, 58, 183, 0.3);
}

.save-btn:active {
  transform: translateY(0);
}

.save-btn:disabled {
  background: linear-gradient(135deg, #9e9e9e 0%, #757575 100%);
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.delete-confirm-btn {
  background: linear-gradient(135deg, #f44336 0%, #d32f2f 100%);
  color: white;
  border: none;
  box-shadow: 0 4px 10px rgba(244, 67, 54, 0.2);
}

.delete-confirm-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 15px rgba(244, 67, 54, 0.3);
}

.delete-confirm-btn:active {
  transform: translateY(0);
}

.delete-confirm-btn:disabled {
  background: linear-gradient(135deg, #ef9a9a 0%, #e57373 100%);
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

/* Delete confirmation */
.event-to-delete {
  margin: 1.25rem 0;
  padding: 1.25rem;
  background-color: var(--bg-light);
  border-radius: var(--border-radius);
  box-shadow: var(--shadow-sm);
  border-left: 4px solid var(--error-color);
}

.event-to-delete .event-title {
  font-weight: 700;
  margin-bottom: 0.5rem;
  font-size: 1.1rem;
}

.event-to-delete .event-date {
  font-size: 0.9rem;
  color: var(--text-secondary);
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.event-to-delete .event-date::before {
  content: '📅';
  font-size: 0.9rem;
}

.confirmation-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1.5rem;
}

/* Responsive styles */
@media (max-width: 992px) {
  .sidebar-header h2 {
    font-size: 1.6rem;
  }

  .calendar-sidebar {
    padding: 1.25rem;
    gap: 1.25rem;
  }
}

@media (max-width: 768px) {
  .calendar-sidebar {
    padding: 1rem;
    gap: 1rem;
    border-radius: var(--border-radius);
  }

  .sidebar-header h2 {
    font-size: 1.4rem;
  }

  .current-month {
    font-size: 1rem;
    padding: 0.2rem 0.6rem;
  }

  .nav-btn {
    width: 36px;
    height: 36px;
  }

  .form-row {
    flex-direction: column;
    gap: 1.25rem;
  }

  .form-actions {
    flex-direction: column-reverse;
    gap: 0.75rem;
  }

  .cancel-btn, .save-btn, .delete-confirm-btn {
    width: 100%;
    padding: 1rem;
  }

  .confirmation-actions {
    flex-direction: column-reverse;
    gap: 0.75rem;
  }

  .quick-stats {
    gap: 0.75rem;
  }

  .stat-item {
    padding: 0.6rem 0.75rem;
  }

  .stat-value {
    font-size: 1.5rem;
  }

  .event-actions {
    opacity: 1;
    transform: translateX(0);
    flex-direction: row;
  }

  .action-btn {
    width: 30px;
    height: 30px;
  }

  .event-card {
    position: relative;
    padding-right: 50px;
  }

  .event-actions {
    position: absolute;
    right: 10px;
    top: 10px;
  }

  .modal-header h2 {
    font-size: 1.2rem;
  }

  .modal-body {
    padding: 1.25rem;
  }

  .form-group label {
    font-size: 0.85rem;
  }

  .form-group input,
  .form-group textarea,
  .form-group select {
    padding: 0.8rem;
    font-size: 16px; /* Prevents iOS zoom */
  }

  .events-header h3 {
    font-size: 1.1rem;
  }

  .add-event-btn {
    width: 38px;
    height: 38px;
  }
}

@media (max-width: 480px) {
  .calendar-sidebar {
    padding: 0.75rem;
    gap: 0.75rem;
  }

  .sidebar-header h2 {
    font-size: 1.3rem;
  }

  .month-navigator {
    padding: 0.4rem;
    margin: 0.4rem 0 0.75rem;
  }

  .nav-btn {
    width: 32px;
    height: 32px;
  }

  .current-month {
    font-size: 0.9rem;
    padding: 0.15rem 0.5rem;
  }

  .today-summary {
    padding: 1rem;
  }

  .stat-value {
    font-size: 1.4rem;
  }

  .stat-label {
    font-size: 0.7rem;
  }

  .events-container {
    padding: 1.25rem 1rem;
  }

  .modal-header {
    padding: 1rem;
  }

  .modal-body {
    padding: 1rem;
  }

  .event-card {
    padding: 0.75rem;
    padding-right: 45px;
    gap: 0.6rem;
  }

  .event-dot {
    width: 12px;
    height: 12px;
  }

  .event-title {
    font-size: 0.95rem;
  }

  .event-description {
    font-size: 0.8rem;
    -webkit-line-clamp: 1;
  }

  .event-time {
    font-size: 0.75rem;
  }

  .color-option {
    width: 26px;
    height: 26px;
  }

  .action-btn {
    width: 26px;
    height: 26px;
  }
}

/* iOS-specific fixes */
@supports (-webkit-touch-callout: none) {
  .form-group input,
  .form-group select,
  .form-group textarea {
    font-size: 16px; /* Prevents zoom on input focus */
  }

  .checkbox-group input[type="checkbox"] {
    width: 22px;
    height: 22px;
  }
}

/* Animation for touch devices */
@media (hover: none) {
  /* Ensure buttons have visual feedback on mobile */
  .nav-btn:active,
  .add-event-btn:active,
  .action-btn:active,
  .schedule-btn:active {
    transform: scale(0.92);
  }

  .event-card:active {
    background-color: var(--bg-hover);
  }

  /* Make event actions always visible but subtle until tapped */
  .event-actions {
    opacity: 0.7;
  }

  .event-card:active .event-actions {
    opacity: 1;
  }
}
</style>