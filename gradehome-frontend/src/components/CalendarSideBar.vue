<!-- src/components/CalendarSidebar.vue -->
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
    <div v-if="selectedDate" class="events-container">
      <div class="events-header">
        <h3>{{ formatDate(selectedDate) }}</h3>
        <button class="add-event-btn">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="12" y1="5" x2="12" y2="19"></line>
            <line x1="5" y1="12" x2="19" y2="12"></line>
          </svg>
        </button>
      </div>

      <div v-if="eventsForSelectedDate.length === 0" class="no-events">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="empty-icon">
          <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
          <line x1="16" y1="2" x2="16" y2="6"></line>
          <line x1="8" y1="2" x2="8" y2="6"></line>
          <line x1="3" y1="10" x2="21" y2="10"></line>
        </svg>
        <p>No events scheduled for this day</p>
        <button class="schedule-btn">Schedule Study Time</button>
      </div>

      <div v-else class="events-list">
        <div
            v-for="(event, index) in eventsForSelectedDate"
            :key="index"
            class="event-card"
            :class="getEventClass(event)"
        >
          <div class="event-dot"></div>
          <div class="event-content">
            <div class="event-time">
              {{ formatTime(event.startTime) }} - {{ formatTime(event.endTime) }}
            </div>
            <div class="event-title">{{ event.title }}</div>
            <div class="event-description">{{ event.description }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CalendarSidebar',
  data() {
    return {
      currentDate: new Date(),
      selectedDate: new Date(),
      // Sample events data (would normally come from API)
      events: [
        {
          date: '2025-04-01',
          startTime: '00:00',
          endTime: '01:00',
          title: 'Happy Birthday',
          description: 'Happy Birthday Saakshi',
          type: 'celebration'
        },
        {
          date: '2025-04-01',
          startTime: '01:00',
          endTime: '02:00',
          title: 'Sample Event',
          description: 'Description for Sample Event',
          type: 'general'
        },
        {
          date: '2025-03-05',
          startTime: '14:30',
          endTime: '16:00',
          title: 'Team Meeting',
          description: 'Weekly team check-in',
          type: 'meeting'
        },
        {
          date: '2025-03-01',
          startTime: '09:00',
          endTime: '11:00',
          title: 'Study Session',
          description: 'Mathematics Module 3',
          type: 'study'
        },
        {
          date: '2025-03-01',
          startTime: '13:00',
          endTime: '15:00',
          title: 'Assignment Work',
          description: 'Computer Science Project',
          type: 'assignment'
        }
      ]
    }
  },
  computed: {
    eventsForSelectedDate() {
      if (!this.selectedDate) return [];

      const dateString = this.formatDateISO(this.selectedDate);
      return this.events.filter(event => event.date === dateString);
    },
    todayEvents() {
      const today = this.formatDateISO(new Date());
      return this.events.filter(event => event.date === today);
    },
    calendarAttributes() {
      // Create a map of dates to event counts
      const eventCounts = {};

      this.events.forEach(event => {
        if (!eventCounts[event.date]) {
          eventCounts[event.date] = 0;
        }
        eventCounts[event.date]++;
      });

      // Create attributes for the calendar
      const attributes = [];

      // For each date with events, create a dot
      Object.keys(eventCounts).forEach(date => {
        attributes.push({
          dates: new Date(date),
          dot: {
            color: eventCounts[date] > 2 ? '#7b49ff' : '#b39ddb',
            className: 'event-dot-highlight'
          }
        });
      });

      return attributes;
    }
  },
  mounted() {
    // Select today's date by default
    this.onDayClick({ date: new Date() });
  },
  methods: {
    onDayClick({ date }) {
      this.selectedDate = date;
      // In a real application, you would fetch events for this date
      // fetchEventsForDate(this.formatDateISO(date));
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
    formatTime(timeString) {
      // Convert 24-hour time format to 12-hour format with AM/PM
      const [hours, minutes] = timeString.split(':');
      const hour = parseInt(hours, 10);
      const period = hour >= 12 ? 'PM' : 'AM';
      const hour12 = hour % 12 || 12;
      return `${hour12}:${minutes} ${period}`;
    },
    getEventClass(event) {
      // Return class based on event type
      const typeMap = {
        'celebration': 'celebration-event',
        'meeting': 'meeting-event',
        'assignment': 'assignment-event',
        'study': 'study-event',
        'general': 'general-event'
      };

      return typeMap[event.type] || 'general-event';
    },
    calculateStudyHours() {
      // Sample calculation - in real app, would calculate actual study time
      return this.todayEvents.filter(event => event.type === 'study').reduce((total, event) => {
        const start = event.startTime.split(':').map(Number);
        const end = event.endTime.split(':').map(Number);
        const hours = end[0] - start[0] + (end[1] - start[1]) / 60;
        return total + hours;
      }, 0).toFixed(1);
    },
    previousMonth() {
      const date = new Date(this.currentDate);
      date.setMonth(date.getMonth() - 1);
      this.currentDate = date;
    },
    nextMonth() {
      const date = new Date(this.currentDate);
      date.setMonth(date.getMonth() + 1);
      this.currentDate = date;
    }
  }
}
</script>

<style scoped>
.calendar-sidebar {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  padding: 1.5rem;
  background-color: #f8f6ff; /* Very light purple for light mode */
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(123, 73, 255, 0.06);
  height: 100%;
  overflow-y: auto;
  transition: all 0.3s ease;
}

/* Dark mode styling */
body.dark-mode .calendar-sidebar {
  background-color: #1a1a2e; /* Dark blue-black background */
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.05);
}

/* Header styling */
.sidebar-header {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.sidebar-header h2 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 600;
  color: #512da8;
}

body.dark-mode .sidebar-header h2 {
  color: #b39ddb;
}

.month-navigator {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.5rem;
}

.current-month {
  font-size: 1rem;
  font-weight: 500;
  color: #512da8;
}

body.dark-mode .current-month {
  color: #d1c4e9;
}

.nav-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border: none;
  background-color: #f0eaff;
  color: #7b49ff;
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.2s ease;
}

.nav-btn:hover {
  background-color: #e6dcff;
  transform: scale(1.05);
}

body.dark-mode .nav-btn {
  background-color: #2c2c4c;
  color: #b39ddb;
}

body.dark-mode .nav-btn:hover {
  background-color: #383860;
}

/* Calendar wrapper */
.calendar-wrapper {
  padding: 0.5rem;
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(123, 73, 255, 0.05);
}

body.dark-mode .calendar-wrapper {
  background-color: #23233c;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

/* Custom calendar styling */
.custom-calendar {
  /* VCalendar color variables */
  --vc-day-base-color: #7b49ff;
  --vc-day-hover-color: #8f68ff;
  --vc-day-selected-color: #7b49ff;
  --vc-day-inrange-color: #b39ddb;
  --vc-font-family: -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica, Arial, sans-serif;

  font-family: var(--vc-font-family);
  border: none;
  border-radius: 8px;
}

body.dark-mode .custom-calendar {
  --vc-day-base-color: #b39ddb;
  --vc-day-hover-color: #d1c4e9;
  --vc-day-selected-color: #7b49ff;
  --vc-day-inrange-color: #5e35b1;
  color: #e0e0e0;
  background-color: #23233c;
}

/* Today's summary styling */
.today-summary {
  background: linear-gradient(135deg, #7b49ff 0%, #9170ff 100%);
  border-radius: 10px;
  padding: 1rem;
  color: white;
  box-shadow: 0 4px 12px rgba(123, 73, 255, 0.2);
}

body.dark-mode .today-summary {
  background: linear-gradient(135deg, #5e35b1 0%, #7b49ff 100%);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
}

.date-pill {
  background-color: rgba(255, 255, 255, 0.2);
  border-radius: 20px;
  padding: 0.25rem 0.75rem;
  font-size: 0.85rem;
  font-weight: 500;
  display: inline-block;
  margin-bottom: 0.75rem;
}

.quick-stats {
  display: flex;
  justify-content: space-around;
}

.stat-item {
  text-align: center;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 600;
  line-height: 1.2;
}

.stat-label {
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  opacity: 0.9;
}

/* Events section styling */
.events-container {
  background-color: white;
  border-radius: 10px;
  padding: 1.25rem;
  box-shadow: 0 2px 8px rgba(123, 73, 255, 0.05);
}

body.dark-mode .events-container {
  background-color: #23233c;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
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
  color: #512da8;
}

body.dark-mode .events-header h3 {
  color: #b39ddb;
}

.add-event-btn {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f0eaff;
  color: #7b49ff;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.2s ease;
}

.add-event-btn:hover {
  background-color: #e6dcff;
  transform: scale(1.05);
}

body.dark-mode .add-event-btn {
  background-color: #2c2c4c;
  color: #b39ddb;
}

body.dark-mode .add-event-btn:hover {
  background-color: #383860;
}

/* Empty state styling */
.no-events {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
  padding: 1.5rem 0;
  color: #7e7e7e;
  text-align: center;
}

body.dark-mode .no-events {
  color: #a0a0a0;
}

.empty-icon {
  opacity: 0.5;
  margin-bottom: 0.5rem;
}

.schedule-btn {
  background-color: #f0eaff;
  color: #7b49ff;
  border: none;
  border-radius: 20px;
  padding: 0.5rem 1rem;
  font-size: 0.85rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.schedule-btn:hover {
  background-color: #e6dcff;
}

body.dark-mode .schedule-btn {
  background-color: #2c2c4c;
  color: #b39ddb;
}

body.dark-mode .schedule-btn:hover {
  background-color: #383860;
}

/* Event cards styling */
.events-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.event-card {
  display: flex;
  gap: 0.75rem;
  padding: 0.75rem;
  border-radius: 8px;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  position: relative;
  background-color: #f8f6ff;
}

.event-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 2px 8px rgba(123, 73, 255, 0.1);
}

body.dark-mode .event-card {
  background-color: #2c2c4c;
}

body.dark-mode .event-card:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.event-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  margin-top: 4px;
}

.event-content {
  flex: 1;
}

.event-time {
  font-size: 0.8rem;
  color: #7e7e7e;
  margin-bottom: 0.25rem;
}

body.dark-mode .event-time {
  color: #a0a0a0;
}

.event-title {
  font-weight: 600;
  margin-bottom: 0.25rem;
  color: #333;
}

body.dark-mode .event-title {
  color: #e0e0e0;
}

.event-description {
  font-size: 0.85rem;
  color: #666;
}

body.dark-mode .event-description {
  color: #a0a0a0;
}

/* Event type styles */
.celebration-event .event-dot {
  background-color: #ff9100;
}

.meeting-event .event-dot {
  background-color: #7b49ff;
}

.assignment-event .event-dot {
  background-color: #f44336;
}

.study-event .event-dot {
  background-color: #4caf50;
}

.general-event .event-dot {
  background-color: #2196f3;
}

/* Responsive styles */
@media (max-width: 768px) {
  .calendar-sidebar {
    padding: 1rem;
  }

  .quick-stats {
    flex-wrap: wrap;
  }

  .stat-item {
    flex: 1 0 45%;
    margin-bottom: 0.5rem;
  }
}
</style>