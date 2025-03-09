<template>
  <div
      class="mobile-calendar-sidebar"
      :class="{
      'expanded': isExpanded,
      'collapsed': !isExpanded,
      'dark-mode': isDarkMode
    }"
  >
    <!-- Collapsed state toggle button (visible when sidebar is collapsed) -->
    <button
        v-if="!isExpanded"
        @click="toggleSidebar"
        class="toggle-sidebar-btn expand-btn"
        aria-label="Show calendar"
    >
      <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
        <line x1="16" y1="2" x2="16" y2="6"></line>
        <line x1="8" y1="2" x2="8" y2="6"></line>
        <line x1="3" y1="10" x2="21" y2="10"></line>
      </svg>
      <span>Calendar</span>
    </button>

    <!-- Main sidebar content (visible when expanded) -->
    <div class="sidebar-content">
      <!-- Header with collapse button -->
      <div class="sidebar-header">
        <h2>Calendar</h2>
        <button
            @click="toggleSidebar"
            class="toggle-sidebar-btn collapse-btn"
            aria-label="Hide calendar"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M9 18l6-6-6-6" />
          </svg>
          <span>Hide</span>
        </button>
      </div>

      <!-- Month navigation and calendar -->
      <div class="calendar-section">
        <div class="month-navigator">
          <button @click="previousMonth" class="nav-btn" aria-label="Previous month">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M15 18l-6-6 6-6" />
            </svg>
          </button>
          <span class="current-month">{{ formatMonthYear(currentDate) }}</span>
          <button @click="nextMonth" class="nav-btn" aria-label="Next month">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M9 18l6-6-6-6" />
            </svg>
          </button>
        </div>

        <!-- Calendar component - using vc-calendar for larger screens and simplified grid for mobile -->
        <div class="calendar-wrapper">
          <div v-if="isMobileView" class="mobile-calendar-grid">
            <!-- Mobile calendar grid -->
            <div class="mobile-calendar-header">
              <div v-for="day in weekdayLabels" :key="day" class="weekday-label">
                {{ day }}
              </div>
            </div>
            <div class="mobile-calendar-days">
              <div
                  v-for="(day, index) in monthDays"
                  :key="index"
                  class="mobile-calendar-day"
                  :class="{
                  'today': isToday(day.date),
                  'other-month': !day.currentMonth,
                  'selected': isSelectedDate(day.date),
                  'has-events': hasEvents(day.date)
                }"
                  @click="onDayClick(day.date)"
              >
                <span class="day-number">{{ day.day }}</span>
                <span v-if="hasEvents(day.date)" class="event-indicator"></span>
              </div>
            </div>
          </div>

          <vc-calendar
              v-else
              v-model="currentDate"
              is-inline
              @dayclick="onDayClick"
              class="custom-calendar"
              :attributes="calendarAttributes"
          />
        </div>
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
          <p>No events scheduled</p>
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
    </div>

    <!-- Modal for creating/editing events -->
    <transition name="modal">
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
    </transition>

    <!-- Delete confirmation modal -->
    <transition name="modal">
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
    </transition>
  </div>
</template>

<script>
import axios from 'axios';
import { nextTick } from 'vue';
import { notify } from '@/services/toastService.js';
import { API_URL } from '@/config.js';

export default {
  name: 'MobileCalendarSidebar',
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
    },
    // Whether the sidebar should start expanded or collapsed
    initiallyExpanded: {
      type: Boolean,
      default: false
    },
    // Optional screen sizes to consider mobile for the calendar view
    mobileBreakpoint: {
      type: Number,
      default: 768 // Default mobile breakpoint in pixels
    }
  },
  emits: ['day-click', 'add-event', 'edit-event', 'delete-event', 'toggle-completion', 'sidebar-toggle'],
  data() {
    return {
      isExpanded: this.initiallyExpanded,
      isDarkMode: false,
      isMobileView: false,
      screenWidth: 0,
      currentDate: new Date(),
      internalSelectedDate: new Date(),
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
      internalEvents: [], // Used when no events prop is provided
      weekdayLabels: ['S', 'M', 'T', 'W', 'T', 'F', 'S'], // Short labels for mobile
      touchStartX: 0,
      touchEndX: 0,
      swipeThreshold: 100 // Min distance to detect a swipe
    }
  },
  computed: {
    // Returns whether there's a selected date (from props or internal)
    activeDate() {
      return this.selectedDate || this.internalSelectedDate;
    },

    // Generate days for the current month (for mobile calendar view)
    monthDays() {
      const year = this.currentDate.getFullYear();
      const month = this.currentDate.getMonth();
      const daysInMonth = new Date(year, month + 1, 0).getDate();
      const firstDayOfMonth = new Date(year, month, 1).getDay();

      // Days from previous month to fill the first week
      const prevMonthDays = [];
      const prevMonth = month === 0 ? 11 : month - 1;
      const prevMonthYear = month === 0 ? year - 1 : year;
      const daysInPrevMonth = new Date(prevMonthYear, prevMonth + 1, 0).getDate();

      for (let i = 0; i < firstDayOfMonth; i++) {
        const day = daysInPrevMonth - firstDayOfMonth + i + 1;
        prevMonthDays.push({
          day,
          date: new Date(prevMonthYear, prevMonth, day),
          currentMonth: false
        });
      }

      // Current month days
      const currentMonthDays = [];
      for (let i = 1; i <= daysInMonth; i++) {
        currentMonthDays.push({
          day: i,
          date: new Date(year, month, i),
          currentMonth: true
        });
      }

      // Days from next month to complete the grid
      const nextMonthDays = [];
      const totalDaysDisplayed = 42; // 6 rows of 7 days
      const remainingDays = totalDaysDisplayed - prevMonthDays.length - currentMonthDays.length;
      const nextMonth = month === 11 ? 0 : month + 1;
      const nextMonthYear = month === 11 ? year + 1 : year;

      for (let i = 1; i <= remainingDays; i++) {
        nextMonthDays.push({
          day: i,
          date: new Date(nextMonthYear, nextMonth, i),
          currentMonth: false
        });
      }

      return [...prevMonthDays, ...currentMonthDays, ...nextMonthDays];
    },

    // Get events for the selected date
    eventsForSelectedDate() {
      if (!this.activeDate) return [];

      const dateString = this.formatDateISO(this.activeDate);
      // Use events from props if available, otherwise use internal events
      const eventsArray = this.events.length > 0 ? this.events : this.internalEvents;
      return eventsArray.filter(event => event.date === dateString);
    },

    // Get events for today
    todayEvents() {
      const today = this.formatDateISO(new Date());
      // Use events from props if available, otherwise use internal events
      const eventsArray = this.events.length > 0 ? this.events : this.internalEvents;
      return eventsArray.filter(event => event.date === today);
    },

    // Calendar attributes for the v-calendar component
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
    },
    // Listen for changes to the initiallyExpanded prop
    initiallyExpanded(newValue) {
      this.isExpanded = newValue;
    }
  },
  mounted() {
    // Check for dark mode
    this.isDarkMode = document.body.classList.contains('dark-mode');

    // Select today's date by default
    this.onDayClick({ date: new Date() });

    // Check if we're in mobile view
    this.checkScreenSize();

    // Add event listeners
    window.addEventListener('resize', this.checkScreenSize);
    window.addEventListener('darkModeChange', this.onDarkModeChange);

    // Setup swipe detection (for mobile)
    this.$el.addEventListener('touchstart', this.handleTouchStart);
    this.$el.addEventListener('touchend', this.handleTouchEnd);

    // If we're not using the events prop, fetch events
    if (this.events.length === 0) {
      this.fetchEvents();
    }

    // Force a redraw of the calendar if using v-calendar
    nextTick(() => {
      this.applyCalendarTheme();
    });

    // Try to get saved state from localStorage
    const savedExpanded = localStorage.getItem('calendarSidebarExpanded');
    if (savedExpanded !== null) {
      this.isExpanded = savedExpanded === 'true';
    }
  },
  beforeUnmount() {
    // Remove event listeners
    window.removeEventListener('resize', this.checkScreenSize);
    window.removeEventListener('darkModeChange', this.onDarkModeChange);
    this.$el.removeEventListener('touchstart', this.handleTouchStart);
    this.$el.removeEventListener('touchend', this.handleTouchEnd);
  },
  methods: {
    // Toggle sidebar expanded/collapsed state
    toggleSidebar() {
      this.isExpanded = !this.isExpanded;
      // Save preference to localStorage
      localStorage.setItem('calendarSidebarExpanded', this.isExpanded);
      // Emit event to parent
      this.$emit('sidebar-toggle', this.isExpanded);
    },

    // Check screen size to determine if we should use mobile view
    checkScreenSize() {
      this.screenWidth = window.innerWidth;
      this.isMobileView = this.screenWidth <= this.mobileBreakpoint;
    },

    // Handle dark mode changes
    onDarkModeChange(event) {
      this.isDarkMode = event.detail.isDark;
      this.applyCalendarTheme();
    },

    // Apply theme to calendar component
    applyCalendarTheme() {
      // Get the dark mode state
      const isDarkMode = document.body.classList.contains('dark-mode');

      // Apply proper theme to calendar component if using V-Calendar
      if (this.$refs.calendar) {
        const calendarElement = this.$refs.calendar.$el;

        if (isDarkMode) {
          calendarElement.classList.add('vc-dark');
        } else {
          calendarElement.classList.remove('vc-dark');
        }
      }
    },

    // Touch handlers for swipe gestures
    handleTouchStart(e) {
      this.touchStartX = e.changedTouches[0].screenX;
    },

    handleTouchEnd(e) {
      this.touchEndX = e.changedTouches[0].screenX;
      this.handleSwipe();
    },

    handleSwipe() {
      const distance = this.touchStartX - this.touchEndX;

      // If the swipe distance is greater than threshold
      if (Math.abs(distance) > this.swipeThreshold) {
        // Swipe left (collapse sidebar)
        if (distance > 0 && this.isExpanded) {
          this.toggleSidebar();
        }
        // Swipe right (expand sidebar)
        else if (distance < 0 && !this.isExpanded) {
          this.toggleSidebar();
        }
      }
    },

    // Fetch events from API
    async fetchEvents(startDate = null, endDate = null) {
      // Only fetch if we're not using the events prop
      if (this.events.length > 0) return;

      try {
        this.loadingEvents = true;

        // Add date parameters if provided
        const params = {};
        if (startDate) params.start_date = startDate;
        if (endDate) params.end_date = endDate;

        const response = await axios.get(`${API_URL}/calendar/events`, {
          withCredentials: true,
          params
        });

        this.internalEvents = response.data;
      } catch (error) {
        console.error('Error fetching events:', error);
        notify({ type: 'error', message: 'Failed to load events. Please try again.' });
      } finally {
        this.loadingEvents = false;
      }
    },

    // Handler for calendar day clicks
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

    // Month navigation
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
    },

    // Modal management for creating/editing events
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

    // Delete event handling
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

    // Toggle event completion status
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

    // Date and time formatting
    formatDate(date) {
      if (!date) return '';

      // Different format for mobile
      if (this.isMobileView) {
        return new Date(date).toLocaleDateString('en-US', {
          weekday: 'short',
          month: 'short',
          day: 'numeric'
        });
      }

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

    // Helper methods for calendar display
    isToday(date) {
      const today = new Date();
      return date.getDate() === today.getDate() &&
          date.getMonth() === today.getMonth() &&
          date.getFullYear() === today.getFullYear();
    },

    isSelectedDate(date) {
      if (!this.activeDate) return false;

      return date.getDate() === this.activeDate.getDate() &&
          date.getMonth() === this.activeDate.getMonth() &&
          date.getFullYear() === this.activeDate.getFullYear();
    },

    hasEvents(date) {
      const dateString = this.formatDateISO(date);
      const eventsArray = this.events.length > 0 ? this.events : this.internalEvents;
      return eventsArray.some(event => event.date === dateString);
    },

    // Style and class helpers
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
    }
  }
}
</script>

<style scoped>
/* Mobile Calendar Sidebar Styles */
.mobile-calendar-sidebar {
  position: relative;
  background-color: var(--bg-light);
  color: var(--text-primary);
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  height: 100%;
  overflow: hidden;
  z-index: 10;
}

/* Sidebar state transitions */
.mobile-calendar-sidebar.expanded {
  width: 340px;
  box-shadow: var(--shadow-lg);
  border-left: 1px solid var(--border-color);
}

.mobile-calendar-sidebar.collapsed {
  width: 0;
  overflow: hidden;
}

/* The toggle button visible when sidebar is collapsed */
.toggle-sidebar-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  background-color: var(--primary-color);
  color: white;
  border: none;
  border-radius: 50px;
  padding: 10px 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  z-index: 100;
  box-shadow: var(--shadow-md);
}

.toggle-sidebar-btn:hover {
  background-color: var(--primary-dark);
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}

.toggle-sidebar-btn:active {
  transform: translateY(0);
}

.expand-btn {
  position: fixed;
  top: 5rem;
  right: 1rem;
}

.collapse-btn {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background-color: transparent;
  color: var(--text-secondary);
  box-shadow: none;
  padding: 8px;
  border-radius: 50%;
}

.collapse-btn:hover {
  background-color: var(--bg-hover);
  color: var(--primary-color);
  transform: scale(1.1);
  box-shadow: none;
}

/* Main sidebar content */
.sidebar-content {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  padding: 1.5rem;
  height: 100%;
  overflow-y: auto;
  scrollbar-width: thin;
  scrollbar-color: var(--border-color) transparent;
}

.sidebar-content::-webkit-scrollbar {
  width: 4px;
}

.sidebar-content::-webkit-scrollbar-track {
  background: transparent;
}

.sidebar-content::-webkit-scrollbar-thumb {
  background-color: var(--border-color);
  border-radius: 6px;
}

/* Header styling */
.sidebar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: relative;
}

.sidebar-header h2 {
  margin: 0;
  font-size: 1.4rem;
  font-weight: 700;
  color: var(--primary-dark);
  position: relative;
  display: inline-block;
}

.dark-mode .sidebar-header h2 {
  color: var(--primary-light);
}

.sidebar-header h2::after {
  content: '';
  position: absolute;
  left: 0;
  bottom: -4px;
  width: 30px;
  height: 3px;
  background: var(--primary-gradient);
  border-radius: 2px;
}

/* Calendar section styling */
.calendar-section {
  background-color: var(--bg-card);
  border-radius: var(--border-radius);
  box-shadow: var(--shadow-sm);
  overflow: hidden;
  transition: all 0.3s ease;
}

.calendar-section:hover {
  box-shadow: var(--shadow-md);
}

.month-navigator {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.75rem 1rem;
  border-bottom: 1px solid var(--border-color);
}

.current-month {
  font-size: 1rem;
  font-weight: 600;
  color: var(--primary-dark);
}

.nav-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border: none;
  background-color: var(--bg-input);
  color: var(--primary-color);
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.nav-btn:hover {
  background-color: var(--primary-color-transparent);
  transform: scale(1.1);
}

.nav-btn:active {
  transform: scale(0.95);
}

.calendar-wrapper {
  padding: 0.5rem;
}

/* Mobile calendar grid */
.mobile-calendar-grid {
  width: 100%;
}

.mobile-calendar-header {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  text-align: center;
  font-weight: 600;
  font-size: 0.75rem;
  color: var(--text-secondary);
  margin-bottom: 0.5rem;
}

.weekday-label {
  padding: 0.25rem;
}

.mobile-calendar-days {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 2px;
}

.mobile-calendar-day {
  aspect-ratio: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  position: relative;
  cursor: pointer;
  border-radius: 50%;
  transition: all 0.2s ease;
  font-size: 0.875rem;
}

.mobile-calendar-day:hover {
  background-color: var(--bg-hover);
}

.mobile-calendar-day.today {
  font-weight: bold;
  color: var(--primary-color);
}

.mobile-calendar-day.selected {
  background-color: var(--primary-color);
  color: white;
}

.mobile-calendar-day.other-month {
  color: var(--text-muted);
}

.event-indicator {
  position: absolute;
  bottom: 2px;
  width: 4px;
  height: 4px;
  border-radius: 50%;
  background-color: var(--primary-color);
}

/* Today's summary styling */
.today-summary {
  background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-dark) 100%);
  border-radius: var(--border-radius);
  padding: 1.25rem;
  box-shadow: 0 8px 20px rgba(103, 58, 183, 0.2);
  color: white;
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease;
}

.today-summary:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 28px rgba(103, 58, 183, 0.3);
}

.date-pill {
  background-color: rgba(255, 255, 255, 0.2);
  border-radius: 20px;
  padding: 0.4rem 1rem;
  font-size: 0.85rem;
  font-weight: 700;
  display: inline-block;
  margin-bottom: 1rem;
  backdrop-filter: blur(5px);
}

.quick-stats {
  display: flex;
  justify-content: space-around;
  gap: 1rem;
}

.stat-item {
  text-align: center;
  background-color: rgba(255, 255, 255, 0.15);
  padding: 0.75rem;
  border-radius: var(--border-radius);
  flex: 1;
  transition: all 0.3s ease;
  backdrop-filter: blur(5px);
}

.stat-item:hover {
  background-color: rgba(255, 255, 255, 0.25);
  transform: translateY(-2px);
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 700;
  line-height: 1.2;
  margin-bottom: 0.25rem;
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
  padding: 1.25rem;
  box-shadow: var(--shadow-sm);
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 200px;
  transition: all 0.3s ease;
}

.events-container:hover {
  box-shadow: var(--shadow-md);
}

.events-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.events-header h3 {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--primary-dark);
}

.dark-mode .events-header h3 {
  color: var(--primary-light);
}

.add-event-btn {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--primary-color);
  color: white;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  box-shadow: 0 2px 5px rgba(103, 58, 183, 0.2);
}

.add-event-btn:hover {
  background-color: var(--primary-dark);
  transform: scale(1.1);
  box-shadow: 0 4px 8px rgba(103, 58, 183, 0.3);
}

.add-event-btn:active {
  transform: scale(0.95);
}

/* Loading and empty state styling */
.loading-events {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem 0;
  color: var(--text-secondary);
  flex: 1;
}

.loading-spinner {
  width: 32px;
  height: 32px;
  border: 3px solid rgba(103, 58, 183, 0.1);
  border-radius: 50%;
  border-top-color: var(--primary-color);
  animation: spin 1s ease-in-out infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.no-events {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem 0;
  color: var(--text-secondary);
  flex: 1;
  text-align: center;
}

.empty-icon {
  color: var(--primary-color);
  opacity: 0.6;
  margin-bottom: 1rem;
}

.schedule-btn {
  margin-top: 1rem;
  padding: 0.6rem 1.2rem;
  background-color: var(--primary-color-transparent);
  color: var(--primary-color);
  border: none;
  border-radius: 20px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.schedule-btn:hover {
  background-color: var(--primary-color);
  color: white;
  transform: translateY(-2px);
}

/* Events list styling */
.events-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  flex: 1;
  overflow-y: auto;
}

.event-card {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  padding: 0.75rem;
  border-radius: var(--border-radius);
  background-color: var(--bg-light);
  box-shadow: var(--shadow-sm);
  transition: all 0.3s ease;
  border-left: 3px solid transparent;
  position: relative;
}

.event-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.event-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  margin-top: 0.25rem;
}

.event-content {
  flex: 1;
  min-width: 0; /* Ensure text truncation works */
}

.event-time {
  font-size: 0.75rem;
  color: var(--text-secondary);
  margin-bottom: 0.25rem;
}

.event-title {
  font-weight: 600;
  margin-bottom: 0.25rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.event-description {
  font-size: 0.75rem;
  color: var(--text-secondary);
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Event type styles */
.general-event {
  border-left-color: #2196f3;
}

.general-event .event-dot {
  background-color: #2196f3;
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

.celebration-event {
  border-left-color: #ff9100;
}

.celebration-event .event-dot {
  background-color: #ff9100;
}

.completed-event {
  opacity: 0.75;
}

.completed-event .event-title {
  text-decoration: line-through;
}

/* Event actions */
.event-actions {
  display: flex;
  gap: 0.5rem;
  opacity: 0;
  transition: all 0.3s ease;
  position: absolute;
  right: 0.75rem;
  top: 0.75rem;
}

.event-card:hover .event-actions {
  opacity: 1;
}

.action-btn {
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  background-color: var(--bg-input);
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.edit-btn {
  color: var(--primary-color);
}

.edit-btn:hover {
  background-color: var(--primary-color-transparent);
}

.delete-btn {
  color: var(--error-color);
}

.delete-btn:hover {
  background-color: rgba(244, 67, 54, 0.15);
}

.complete-btn {
  color: var(--success-color);
}

.complete-btn:hover {
  background-color: rgba(76, 175, 80, 0.15);
}

.complete-btn.completed {
  background-color: var(--success-color);
  color: white;
}

/* Modal styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(3px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
}

.modal-enter-active, .modal-leave-active {
  transition: opacity 0.3s;
}

.modal-enter-from, .modal-leave-to {
  opacity: 0;
}

.modal-container {
  background-color: var(--bg-card);
  border-radius: var(--border-radius-lg);
  width: 90%;
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: var(--shadow-lg);
  animation: modalAppear 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}

@keyframes modalAppear {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.confirmation-modal {
  max-width: 400px;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.25rem;
  border-bottom: 1px solid var(--border-color);
}

.modal-header h2 {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 600;
}

.close-btn {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--bg-input);
  border: none;
  color: var(--text-secondary);
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.3s ease;
}

.close-btn:hover {
  background-color: rgba(244, 67, 54, 0.15);
  color: var(--error-color);
  transform: rotate(90deg);
}

.modal-body {
  padding: 1.25rem;
}

/* Form styles */
.form-group {
  margin-bottom: 1.25rem;
}

.form-row {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.25rem;
}

.form-row .form-group {
  flex: 1;
  margin-bottom: 0;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  font-size: 0.875rem;
}

.form-group input,
.form-group textarea,
.form-group select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  background-color: var(--bg-input);
  color: var(--text-primary);
  font-size: 1rem;
  transition: all 0.3s ease;
}

.form-group input:focus,
.form-group textarea:focus,
.form-group select:focus {
  border-color: var(--primary-color);
  outline: none;
  box-shadow: 0 0 0 2px var(--primary-color-transparent);
}

.checkbox-group {
  display: flex;
  align-items: center;
}

.checkbox-group input[type="checkbox"] {
  width: auto;
  margin-right: 0.5rem;
}

/* Color picker */
.color-picker {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.color-option {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  border: 2px solid var(--bg-card);
}

.color-option:hover {
  transform: scale(1.2);
}

.color-option.active {
  border: 2px solid var(--text-primary);
  transform: scale(1.2);
}

/* Form actions */
.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1.5rem;
}

.cancel-btn, .save-btn, .delete-confirm-btn {
  padding: 0.75rem 1.25rem;
  border-radius: var(--border-radius);
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.cancel-btn {
  background-color: var(--bg-input);
  color: var(--text-secondary);
  border: 1px solid var(--border-color);
}

.cancel-btn:hover {
  background-color: var(--bg-hover);
}

.save-btn {
  background-color: var(--primary-color);
  color: white;
  border: none;
  box-shadow: 0 2px 5px rgba(103, 58, 183, 0.2);
}

.save-btn:hover {
  background-color: var(--primary-dark);
  box-shadow: 0 4px 8px rgba(103, 58, 183, 0.3);
  transform: translateY(-2px);
}

.save-btn:disabled {
  background-color: var(--text-muted);
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.delete-confirm-btn {
  background-color: var(--error-color);
  color: white;
  border: none;
}

.delete-confirm-btn:hover {
  background-color: #d32f2f;
  transform: translateY(-2px);
}

.delete-confirm-btn:disabled {
  background-color: #e57373;
  cursor: not-allowed;
  transform: none;
}

/* Event to delete styling */
.event-to-delete {
  margin: 1.25rem 0;
  padding: 1rem;
  background-color: var(--bg-light);
  border-radius: var(--border-radius);
  border-left: 3px solid var(--error-color);
}

.event-to-delete .event-title {
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.event-to-delete .event-date {
  font-size: 0.875rem;
  color: var(--text-secondary);
}

.confirmation-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1.5rem;
}

/* Mobile-specific styles */
@media (max-width: 768px) {
  .mobile-calendar-sidebar.expanded {
    width: 100%;
    position: fixed;
    top: 0;
    left: 0;
    height: 100vh;
    z-index: 1000;
  }

  .collapse-btn {
    top: 1rem;
    right: 1rem;
  }

  .form-row {
    flex-direction: column;
    gap: 1.25rem;
  }

  .form-actions {
    flex-direction: column-reverse;
    gap: 0.75rem;
  }

  .form-actions button {
    width: 100%;
  }

  .confirmation-actions {
    flex-direction: column-reverse;
    gap: 0.75rem;
  }

  .confirmation-actions button {
    width: 100%;
  }

  /* Make event actions always visible on mobile */
  .event-actions {
    opacity: 1;
  }
}

/* Small mobile screens */
@media (max-width: 480px) {
  .sidebar-content {
    padding: 1rem;
    gap: 1rem;
  }

  .sidebar-header h2 {
    font-size: 1.25rem;
  }

  .stat-value {
    font-size: 1.25rem;
  }

  .stat-label {
    font-size: 0.75rem;
  }

  .mobile-calendar-day {
    font-size: 0.8rem;
  }

  .weekday-label {
    font-size: 0.7rem;
  }

  .event-card {
    padding: 0.6rem;
  }

  .event-title {
    font-size: 0.9rem;
  }

  .event-description {
    font-size: 0.7rem;
  }

  .modal-header, .modal-body {
    padding: 1rem;
  }

  .form-group label {
    font-size: 0.8rem;
  }
}

/* iOS-specific fixes */
@supports (-webkit-touch-callout: none) {
  .form-group input,
  .form-group select,
  .form-group textarea {
    font-size: 16px; /* Prevents zoom on input focus */
  }
}
</style>