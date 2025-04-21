<template>
  <div class="study-hub-sidebar" :class="{ 'collapsed': isCollapsed }">
    <!-- Collapse Toggle Button -->
    <button @click="toggleSidebar" class="collapse-toggle" :title="isCollapsed ? 'Expand sidebar' : 'Collapse sidebar'">
      <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M15 18l-6-6 6-6" v-if="!isCollapsed" />
        <path d="M9 18l6-6-6-6" v-else />
      </svg>
    </button>

    <div class="sidebar-content">
      <!-- Header Section -->
      <div class="sidebar-header">
        <h2>Study Hub</h2>
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

      <!-- Active Schedule Card -->
      <div v-if="activeSchedule" class="active-schedule">
        <div class="card-header">
          <h3>Active Schedule</h3>
          <div class="header-actions">
            <button @click="changeSchedule" class="change-schedule-btn" title="Change active schedule">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M17 3a2.828 2.828 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5L17 3z"></path>
              </svg>
              Change
            </button>
            <span class="badge">{{ activeSchedule.is_ai_generated ? 'AI Generated' : 'Custom' }}</span>
          </div>
        </div>

        <div class="schedule-info">
          <div class="schedule-name">{{ activeSchedule.name }}</div>
          <div class="schedule-dates">
            {{ formatDate(new Date(activeSchedule.start_date)) }} - {{ formatDate(new Date(activeSchedule.end_date)) }}
          </div>

          <!-- Progress Bar -->
          <div class="progress-container">
            <div class="progress-label">
              <span>Progress</span>
              <span>{{ completionStats.rate }}%</span>
            </div>
            <div class="progress-bar">
              <div class="progress-value" :style="{ width: completionStats.rate + '%' }"></div>
            </div>
          </div>

          <div class="schedule-stats">
            <div class="stat">
              <span class="value">{{ completionStats.total }}</span>
              <span class="label">Sessions</span>
            </div>
            <div class="stat">
              <span class="value">{{ completionStats.completed }}</span>
              <span class="label">Completed</span>
            </div>
            <div class="stat">
              <span class="value">{{ completionStats.missed || 0 }}</span>
              <span class="label">Missed</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Upcoming Study Sessions Card -->
      <div v-if="upcomingSessions.length > 0" class="upcoming-sessions">
        <div class="card-header">
          <h3>Upcoming Sessions</h3>
          <div class="header-actions">
            <button @click="viewAllSessions" class="view-all-btn" title="View all sessions">
              View All
            </button>
            <button @click="refreshSessions" class="refresh-btn" title="Refresh sessions">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M23 4v6h-6"></path>
                <path d="M1 20v-6h6"></path>
                <path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"></path>
              </svg>
            </button>
          </div>
        </div>

        <div class="sessions-list">
          <div
              v-for="session in upcomingSessions.slice(0, 5)"
              :key="session.id"
              class="session-card"
              :class="[
              getSessionStatusClass(session),
              { 'active-now': isSessionActive(session) }
            ]"
          >
            <div class="session-time">
              <div class="session-date">{{ formatDateShort(new Date(session.date)) }}</div>
              <div class="session-hours">{{ session.startTime }} - {{ session.endTime }}</div>

              <!-- Countdown timer for in-progress sessions -->
              <div v-if="isSessionActive(session)" class="session-countdown">
                {{ getSessionCountdown(session) }} remaining
              </div>
            </div>

            <div class="session-content">
              <div class="session-title">{{ session.title }}</div>
              <div class="session-module">{{ getModuleName(session.module) }}</div>
            </div>

            <div class="session-actions">
              <!-- Only show complete button for active or planned sessions -->
              <button
                  v-if="isSessionActive(session) || session.status === 'planned'"
                  @click="markSessionCompleted(session)"
                  class="action-btn complete-btn"
                  title="Mark as completed"
              >
                <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <polyline points="20 6 9 17 4 12"></polyline>
                </svg>
              </button>

              <!-- Only show missed button for active or planned sessions -->
              <button
                  v-if="isSessionActive(session) || session.status === 'planned'"
                  @click="markSessionMissed(session)"
                  class="action-btn missed-btn"
                  title="Mark as missed"
              >
                <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <line x1="18" y1="6" x2="6" y2="18"></line>
                  <line x1="6" y1="6" x2="18" y2="18"></line>
                </svg>
              </button>

              <!-- Reschedule button for missed sessions -->
              <button
                  v-if="session.status === 'missed'"
                  @click="rescheduleSession(session)"
                  class="action-btn reschedule-btn"
                  title="Reschedule session"
              >
                <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <circle cx="12" cy="12" r="10"></circle>
                  <polyline points="12 6 12 12 16 14"></polyline>
                </svg>
              </button>
            </div>

            <!-- Status indicators -->
            <div class="session-status">
              <span v-if="session.status === 'in_progress'" class="status in-progress">In Progress</span>
              <span v-else-if="session.status === 'completed'" class="status completed">
                Completed
                <span class="completion-time" v-if="session.completed_at">
                  {{ formatCompletionTime(session.completed_at) }}
                </span>
              </span>
              <span v-else-if="session.status === 'missed'" class="status missed">Missed</span>
              <span v-else-if="isSessionActive(session)" class="status active">Active Now</span>
              <span v-else class="status planned">Planned</span>
            </div>
          </div>

          <!-- Show more indicator if there are more than 5 sessions -->
          <div v-if="upcomingSessions.length > 5" class="more-sessions">
            <button @click="viewAllSessions" class="more-btn">
              + {{ upcomingSessions.length - 5 }} more sessions
            </button>
          </div>
        </div>
      </div>

      <!-- Events section for selected date -->
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
    </div>

    <!-- Session Completion Modal -->
    <div v-if="showSessionFeedbackModal" class="modal-overlay" @click.self="closeSessionFeedbackModal">
      <div class="modal-container">
        <div class="modal-header">
          <h2>Session Feedback</h2>
          <button @click="closeSessionFeedbackModal" class="close-btn">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="submitSessionFeedback">
            <div class="session-details">
              <div class="session-title">{{ sessionToComplete?.title }}</div>
              <div class="session-time">{{ formatDateShort(new Date(sessionToComplete?.date || '')) }} | {{ sessionToComplete?.startTime }} - {{ sessionToComplete?.endTime }}</div>
            </div>

            <div class="form-group">
              <label for="productivity">How productive was this session? (1-5)*</label>
              <div class="rating-buttons">
                <button
                    v-for="n in 5"
                    :key="n"
                    type="button"
                    :class="['rating-btn', { active: sessionFeedback.productivity === n }]"
                    @click="sessionFeedback.productivity = n"
                >
                  {{ n }}
                </button>
              </div>
            </div>

            <div class="form-group">
              <label for="difficulty">How difficult was the material? (1-5)</label>
              <div class="rating-buttons">
                <button
                    v-for="n in 5"
                    :key="n"
                    type="button"
                    :class="['rating-btn', { active: sessionFeedback.difficulty === n }]"
                    @click="sessionFeedback.difficulty = n"
                >
                  {{ n }}
                </button>
              </div>
            </div>

            <div class="form-group">
              <label for="session-notes">Notes (optional)</label>
              <textarea
                  id="session-notes"
                  v-model="sessionFeedback.notes"
                  placeholder="What did you learn or accomplish?"
                  rows="3"
              ></textarea>
            </div>

            <div class="form-group">
              <label>Topics Covered:</label>
              <div class="tags-input">
                <input
                    type="text"
                    v-model="topicInput"
                    @keydown.enter.prevent="addTopic"
                    placeholder="Enter topic and press Enter"
                />
                <div class="tags-container">
                  <span v-for="(topic, index) in sessionFeedback.topics" :key="index" class="tag">
                    {{ topic }}
                    <button type="button" @click="removeTopic(index)" class="remove-tag">×</button>
                  </span>
                </div>
              </div>
            </div>

            <div class="form-actions">
              <button type="button" @click="closeSessionFeedbackModal" class="cancel-btn">Cancel</button>
              <button type="submit" class="save-btn" :disabled="submitFeedbackLoading">
                <span v-if="submitFeedbackLoading">Saving...</span>
                <span v-else>Submit Feedback</span>
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

    <!-- Reschedule Session Modal -->
    <div v-if="showRescheduleModal" class="modal-overlay" @click.self="closeRescheduleModal">
      <div class="modal-container">
        <div class="modal-header">
          <h2>Reschedule Session</h2>
          <button @click="closeRescheduleModal" class="close-btn">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="submitReschedule">
            <div class="session-details">
              <div class="session-title">{{ sessionToReschedule?.title }}</div>
              <div class="session-module">{{ getModuleName(sessionToReschedule?.module) }}</div>
            </div>

            <div class="form-group">
              <label for="reschedule-date">New Date*</label>
              <input
                  type="date"
                  id="reschedule-date"
                  v-model="rescheduleForm.date"
                  required
              />
            </div>

            <div class="form-row">
              <div class="form-group">
                <label for="reschedule-start-time">Start Time*</label>
                <input
                    type="time"
                    id="reschedule-start-time"
                    v-model="rescheduleForm.startTime"
                    required
                />
              </div>

              <div class="form-group">
                <label for="reschedule-end-time">End Time*</label>
                <input
                    type="time"
                    id="reschedule-end-time"
                    v-model="rescheduleForm.endTime"
                    required
                />
              </div>
            </div>

            <div class="form-actions">
              <button type="button" @click="closeRescheduleModal" class="cancel-btn">Cancel</button>
              <button type="submit" class="save-btn" :disabled="rescheduleLoading">
                <span v-if="rescheduleLoading">Rescheduling...</span>
                <span v-else>Reschedule Session</span>
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { nextTick } from 'vue';
import { notify } from '@/services/toastService.js';
import { API_URL } from '@/config.js';

export default {
  name: 'StudyHubSidebar',
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
      isCollapsed: false,
      currentDate: new Date(),
      internalSelectedDate: new Date(), // Internal date when no prop is provided
      loadingEvents: false,
      showEventModal: false,
      editMode: false,
      eventToEdit: null,
      submitting: false,
      showDeleteConfirmation: false,
      eventToDelete: null,
      deleting: false,

      // Reschedule modal state
      showRescheduleModal: false,
      sessionToReschedule: null,
      rescheduleForm: {
        date: '',
        startTime: '',
        endTime: ''
      },
      rescheduleLoading: false,

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

      // StudyHub specific data
      activeSchedule: null,
      upcomingSessions: [],
      userModules: [],
      loadingSessions: false,
      refreshInterval: null,
      countdownInterval: null,

      // Session Feedback Modal
      showSessionFeedbackModal: false,
      sessionToComplete: null,
      sessionFeedback: {
        productivity: 3,
        difficulty: 3,
        notes: '',
        topics: []
      },
      topicInput: '',
      submitFeedbackLoading: false,

      // Stats tracking
      completionStats: {
        total: 0,
        completed: 0,
        missed: 0,
        rate: 0
      }
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

      // Group sessions by date
      const sessionsByDate = {};
      this.upcomingSessions.forEach(session => {
        if (!sessionsByDate[session.date]) {
          sessionsByDate[session.date] = [];
        }
        sessionsByDate[session.date].push(session);
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

      // Create dot attributes for dates with study sessions
      Object.keys(sessionsByDate).forEach(date => {
        const sessions = sessionsByDate[date];
        const hasActiveSession = sessions.some(s => this.isSessionActive(s));
        const hasCompletedSession = sessions.some(s => s.status === 'completed');
        const hasMissedSession = sessions.some(s => s.status === 'missed');

        let sessionDotColor = '#4caf50'; // Default green

        if (hasActiveSession) {
          sessionDotColor = '#ff9100'; // Orange for active
        } else if (hasMissedSession && !hasCompletedSession) {
          sessionDotColor = '#f44336'; // Red for all missed
        } else if (hasMissedSession && hasCompletedSession) {
          sessionDotColor = '#ff9100'; // Orange for mixed
        } else if (hasCompletedSession) {
          sessionDotColor = '#4caf50'; // Green for completed
        }

        // Only add if we don't already have an event dot for this date
        if (!eventsByDate[date]) {
          attributes.push({
            dates: new Date(date),
            dot: {
              color: sessionDotColor,
              className: sessions.length > 3 ? 'event-dot-highlight' : ''
            }
          });
        }
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

    // Fetch study data
    await this.fetchActiveSchedule();
    await this.fetchUserModules();
    await this.fetchUpcomingSessions();

    // Force a redraw of the calendar
    await nextTick();

    // Apply custom styling for calendar components based on dark mode
    this.applyCalendarTheme();

    // Listen for dark mode changes
    window.addEventListener('darkModeChange', this.onDarkModeChange);

    // Set up refresh interval to check for active sessions every minute
    this.refreshInterval = setInterval(() => {
      this.updateSessionStatuses();
      this.fetchUpcomingSessions();
    }, 60000); // Every minute

    // Start the countdown timer for any active sessions
    this.countdownInterval = setInterval(() => {
      // This will update the countdown timer every second
      this.$forceUpdate();
    }, 1000);

    // Check if sidebar collapse state is stored in localStorage
    const storedCollapseState = localStorage.getItem('studyHubSidebarCollapsed');
    if (storedCollapseState) {
      this.isCollapsed = storedCollapseState === 'true';
    }
  },
  beforeUnmount() {
    window.removeEventListener('darkModeChange', this.onDarkModeChange);

    // Clear intervals
    if (this.refreshInterval) {
      clearInterval(this.refreshInterval);
    }

    if (this.countdownInterval) {
      clearInterval(this.countdownInterval);
    }
  },
  methods: {
    toggleSidebar() {
      this.isCollapsed = !this.isCollapsed;
      // Store collapse state in localStorage
      localStorage.setItem('studyHubSidebarCollapsed', this.isCollapsed);

      // Emit event to parent so they can adjust layout if needed
      this.$emit('toggle-collapse', this.isCollapsed);
    },

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

    async fetchActiveSchedule() {
      try {
        const response = await axios.get(`${API_URL}/study/schedules/active`, {
          withCredentials: true
        });
        this.activeSchedule = response.data;

        // Calculate completion statistics if we have an active schedule
        if (this.activeSchedule) {
          await this.calculateCompletionStats();
        }
      } catch (error) {
        console.error('Error fetching active schedule:', error);
        // Don't show error notification as it's normal to not have an active schedule
      }
    },

    async fetchUserModules() {
      try {
        const response = await axios.get(`${API_URL}/modules`, {
          withCredentials: true
        });
        this.userModules = response.data;
      } catch (error) {
        console.error('Error fetching modules:', error);
        // Don't show error notification for this non-critical resource
      }
    },

    async fetchUpcomingSessions() {
      try {
        this.loadingSessions = true;
        const response = await axios.get(`${API_URL}/study/sessions/current`, {
          withCredentials: true
        });
        this.upcomingSessions = response.data;

        // Sort sessions by date and time
        this.upcomingSessions.sort((a, b) => {
          // First compare by date
          if (a.date < b.date) return -1;
          if (a.date > b.date) return 1;

          // If same date, compare by time
          return a.startTime.localeCompare(b.startTime);
        });
      } catch (error) {
        console.error('Error fetching upcoming sessions:', error);
        notify({ type: 'error', message: 'Failed to load study sessions' });
      } finally {
        this.loadingSessions = false;
      }
    },

    async calculateCompletionStats() {
      try {
        if (!this.activeSchedule) {
          this.completionStats = { total: 0, completed: 0, missed: 0, rate: 0 };
          return;
        }

        // Get all sessions for the active schedule
        const response = await axios.get(`${API_URL}/study/sessions`, {
          withCredentials: true,
          params: { schedule_id: this.activeSchedule.id }
        });

        const sessions = response.data;
        const total = sessions.length;
        const completed = sessions.filter(s => s.status === 'completed').length;
        const missed = sessions.filter(s => s.status === 'missed').length;
        const rate = total > 0 ? Math.round((completed / total) * 100) : 0;

        this.completionStats = { total, completed, missed, rate };
      } catch (error) {
        console.error('Error calculating completion stats:', error);
        this.completionStats = { total: 0, completed: 0, missed: 0, rate: 0 };
      }
    },

    async updateSessionStatuses() {
      try {
        // This will check for sessions that need to be marked as in_progress or missed
        await axios.post(`${API_URL}/study/sessions/update-statuses`, {}, {
          withCredentials: true
        });

        // Refresh the sessions to get updated statuses
        await this.fetchUpcomingSessions();
      } catch (error) {
        console.error('Error updating session statuses:', error);
      }
    },

    isSessionActive(session) {
      // Check if the session is currently active (happening right now)
      if (session.status === 'in_progress') return true;

      const now = new Date();
      const sessionDate = new Date(session.date);

      // Check if it's the same day
      if (now.toDateString() !== sessionDate.toDateString()) return false;

      // Parse times
      const [startHours, startMinutes] = session.startTime.split(':').map(Number);
      const [endHours, endMinutes] = session.endTime.split(':').map(Number);

      // Create Date objects for start and end times
      const startTime = new Date(sessionDate);
      startTime.setHours(startHours, startMinutes, 0);

      const endTime = new Date(sessionDate);
      endTime.setHours(endHours, endMinutes, 0);

      // Check if current time is between start and end
      return now >= startTime && now <= endTime;
    },

    getSessionCountdown(session) {
      if (!this.isSessionActive(session)) return '';

      const now = new Date();
      const sessionDate = new Date(session.date);
      const [endHours, endMinutes] = session.endTime.split(':').map(Number);

      const endTime = new Date(sessionDate);
      endTime.setHours(endHours, endMinutes, 0);

      // Calculate the time difference in milliseconds
      const diff = endTime - now;

      // Convert to minutes and seconds
      if (diff <= 0) return '0:00';

      const minutes = Math.floor(diff / 60000);
      const seconds = Math.floor((diff % 60000) / 1000);

      return `${minutes}:${seconds.toString().padStart(2, '0')}`;
    },

    getSessionStatusClass(session) {
      if (session.status === 'completed') return 'completed-session';
      if (session.status === 'missed') return 'missed-session';
      if (session.status === 'in_progress' || this.isSessionActive(session)) return 'active-session';
      return 'planned-session';
    },

    getModuleName(moduleId) {
      const module = this.userModules.find(m => m.id === moduleId);
      return module ? module.name : 'Unknown Module';
    },

    async markSessionCompleted(session) {
      // Show feedback modal to collect session feedback
      this.sessionToComplete = session;
      this.sessionFeedback = {
        productivity: 3,
        difficulty: 3,
        notes: '',
        topics: []
      };
      this.topicInput = '';
      this.showSessionFeedbackModal = true;
    },

    async markSessionMissed(session) {
      try {
        await axios.post(`${API_URL}/study/sessions/${session.id}/miss`, {}, {
          withCredentials: true
        });

        // Update session in upcomingSessions array
        const index = this.upcomingSessions.findIndex(s => s.id === session.id);
        if (index !== -1) {
          this.upcomingSessions[index].status = 'missed';
          this.upcomingSessions[index].missed = true;
        }

        // Refresh completion stats
        await this.calculateCompletionStats();

        notify({ type: 'success', message: 'Session marked as missed' });
      } catch (error) {
        console.error('Error marking session as missed:', error);
        notify({ type: 'error', message: 'Failed to update session status' });
      }
    },

    rescheduleSession(session) {
      this.sessionToReschedule = session;

      // Initialize the form with the session's current date and time
      this.rescheduleForm = {
        date: session.date,
        startTime: session.startTime,
        endTime: session.endTime
      };

      // Set the date to tomorrow by default
      const tomorrow = new Date();
      tomorrow.setDate(tomorrow.getDate() + 1);
      this.rescheduleForm.date = this.formatDateISO(tomorrow);

      this.showRescheduleModal = true;
    },

    async submitReschedule() {
      if (!this.sessionToReschedule) return;

      try {
        this.rescheduleLoading = true;

        // Prepare the data for the API
        const rescheduleData = {
          date: this.rescheduleForm.date,
          startTime: this.rescheduleForm.startTime,
          endTime: this.rescheduleForm.endTime
        };

        // Call the API to reschedule the session
        await axios.post(
            `${API_URL}/study/sessions/${this.sessionToReschedule.id}/reschedule`,
            rescheduleData,
            { withCredentials: true }
        );

        // Refresh sessions and stats
        await this.fetchUpcomingSessions();
        await this.calculateCompletionStats();

        notify({ type: 'success', message: 'Session rescheduled successfully!' });
        this.closeRescheduleModal();
      } catch (error) {
        console.error('Error rescheduling session:', error);
        notify({ type: 'error', message: 'Failed to reschedule session. Please try again.' });
      } finally {
        this.rescheduleLoading = false;
      }
    },

    closeRescheduleModal() {
      this.showRescheduleModal = false;
      this.sessionToReschedule = null;
      this.rescheduleForm = {
        date: '',
        startTime: '',
        endTime: ''
      };
    },

    closeSessionFeedbackModal() {
      this.showSessionFeedbackModal = false;
      this.sessionToComplete = null;
    },

    async submitSessionFeedback() {
      if (!this.sessionToComplete) return;

      try {
        this.submitFeedbackLoading = true;

        await axios.post(`${API_URL}/study/sessions/${this.sessionToComplete.id}/complete`,
            this.sessionFeedback,
            { withCredentials: true }
        );

        // Update session in upcomingSessions array
        const index = this.upcomingSessions.findIndex(s => s.id === this.sessionToComplete.id);
        if (index !== -1) {
          this.upcomingSessions[index].status = 'completed';
          this.upcomingSessions[index].completed = true;
          this.upcomingSessions[index].completed_at = new Date().toISOString();
        }

        // Refresh completion stats
        await this.calculateCompletionStats();

        notify({ type: 'success', message: 'Session completed successfully!' });
        this.closeSessionFeedbackModal();
      } catch (error) {
        console.error('Error completing session:', error);
        notify({ type: 'error', message: 'Failed to complete session' });
      } finally {
        this.submitFeedbackLoading = false;
      }
    },

    addTopic() {
      if (!this.topicInput.trim()) return;

      // Prevent duplicates
      if (!this.sessionFeedback.topics.includes(this.topicInput.trim())) {
        this.sessionFeedback.topics.push(this.topicInput.trim());
      }

      this.topicInput = '';
    },

    removeTopic(index) {
      this.sessionFeedback.topics.splice(index, 1);
    },

    refreshSessions() {
      this.fetchUpcomingSessions();
      this.updateSessionStatuses();
      notify({ type: 'info', message: 'Refreshing sessions...' });
    },

    changeSchedule() {
      // Emit event to parent component to open schedule selection modal
      this.$emit('change-schedule');

      // Navigate to schedules tab
      this.$emit('navigate', 'schedule');
    },

    viewAllSessions() {
      // Navigate to schedule tab
      this.$emit('navigate', 'schedule');
    },

    formatCompletionTime(timestamp) {
      if (!timestamp) return '';

      const date = new Date(timestamp);
      return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    },

    applyCalendarTheme() {
      // Get the dark mode state from parent or localStorage
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

    onDarkModeChange() {
      this.applyCalendarTheme();
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

    formatDateShort(date) {
      if (!date) return '';
      return new Date(date).toLocaleDateString('en-US', {
        month: 'short',
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
      const eventsHours = eventsArray
          .filter(event => event.type === 'study' && !event.all_day)
          .reduce((total, event) => {
            if (!event.start_time || !event.end_time) return total;

            const start = event.start_time.split(':').map(Number);
            const end = event.end_time.split(':').map(Number);
            const hours = end[0] - start[0] + (end[1] - start[1]) / 60;
            return total + (hours > 0 ? hours : 0);
          }, 0);

      // Calculate study hours from sessions
      const today = this.formatDateISO(new Date());
      const sessionsHours = this.upcomingSessions
          .filter(session => session.date === today)
          .reduce((total, session) => {
            if (!session.startTime || !session.endTime) return total;

            const start = session.startTime.split(':').map(Number);
            const end = session.endTime.split(':').map(Number);
            const hours = end[0] - start[0] + (end[1] - start[1]) / 60;
            return total + (hours > 0 ? hours : 0);
          }, 0);

      // Return total study hours
      return (eventsHours + sessionsHours).toFixed(1);
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
/* Enhanced Study Hub Sidebar Styles */
:root {
  --primary-color: #9e78ff;
  --primary-dark: #7b49ff;
  --primary-light: #b59dff;
  --primary-color-transparent: rgba(158, 120, 255, 0.15);
  --primary-gradient: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-dark) 100%);
  --text-primary: #343a40;
  --text-secondary: #6c757d;
  --text-muted: #adb5bd;
  --border-color: #dee2e6;
  --border-color-light: #e9ecef;
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
  --font-family: 'Inter', sans-serif;
}

/* Dark mode variables */
.dark-mode {
  --text-primary: #f8f9fa;
  --text-secondary: #adb5bd;
  --text-muted: #6c757d;
  --border-color: #444444;
  --border-color-light: #555555;
  --bg-light: #121212;
  --bg-card: #1e1e1e;
  --bg-input: #2c2c2c;
  --bg-muted: #333333;
  --bg-hover: #333333;
  --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.2);
  --shadow-md: 0 4px 16px rgba(0, 0, 0, 0.3);
  --shadow-lg: 0 8px 24px rgba(0, 0, 0, 0.4);
}

.study-hub-sidebar {
  display: flex;
  flex-direction: column;
  height: 100%;
  width: 320px;
  background-color: var(--bg-light);
  border-right: 1px solid var(--border-color);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

/* Collapsed state */
.study-hub-sidebar.collapsed {
  width: 60px;
}

.sidebar-content {
  flex: 1;
  overflow-y: auto;
  padding: 1.5rem;
  gap: 1.5rem;
  display: flex;
  flex-direction: column;
  scrollbar-width: thin;
  scrollbar-color: var(--border-color) transparent;
}

.sidebar-content::-webkit-scrollbar {
  width: 6px;
}

.sidebar-content::-webkit-scrollbar-track {
  background: transparent;
}

.sidebar-content::-webkit-scrollbar-thumb {
  background-color: var(--border-color);
  border-radius: 6px;
}

/* Collapse toggle button */
.collapse-toggle {
  position: absolute;
  top: 10px;
  right: 10px;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background-color: var(--bg-card);
  color: var(--text-secondary);
  border: 1px solid var(--border-color);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10;
  transition: all 0.3s ease;
}

.collapse-toggle:hover {
  background-color: var(--bg-hover);
  color: var(--primary-color);
  transform: scale(1.1);
}

/* Hide sidebar content when collapsed */
.study-hub-sidebar.collapsed .sidebar-content > * {
  display: none;
}

.study-hub-sidebar.collapsed .sidebar-content::after {
  content: 'Study Hub';
  writing-mode: vertical-lr;
  transform: rotate(180deg);
  text-align: center;
  display: block;
  font-size: 1.2rem;
  font-weight: 600;
  color: var(--primary-color);
  margin: auto;
  height: 100%;
  padding: 1rem 0;
}

/* Header Section */
.sidebar-header {
  margin-bottom: 1rem;
}

.sidebar-header h2 {
  margin: 0 0 1rem 0;
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--primary-color);
  position: relative;
  display: inline-block;
}

.sidebar-header h2::after {
  content: '';
  position: absolute;
  left: 0;
  bottom: -5px;
  width: 40px;
  height: 3px;
  background: var(--primary-gradient);
  border-radius: 2px;
}

.month-navigator {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: var(--bg-card);
  border-radius: var(--border-radius);
  padding: 0.5rem;
  box-shadow: var(--shadow-sm);
  transition: all 0.3s ease;
}

.month-navigator:hover {
  box-shadow: var(--shadow-md);
}

.current-month {
  font-size: 1.05rem;
  font-weight: 600;
  color: var(--primary-dark);
  padding: 0.25rem 0.75rem;
  background-color: var(--bg-input);
  border-radius: 20px;
}

.nav-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border: none;
  background-color: var(--bg-input);
  color: var(--primary-color);
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.3s ease;
}

.nav-btn:hover {
  background-color: var(--primary-color-transparent);
  transform: scale(1.1);
}

/* Calendar wrapper */
.calendar-wrapper {
  padding: 0.5rem;
  background-color: var(--bg-card);
  border-radius: var(--border-radius);
  box-shadow: var(--shadow-sm);
  margin-bottom: 1.5rem;
  transition: all 0.3s ease;
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

/* V-Calendar customization */
:deep(.vc-container) {
  --gray-900: var(--text-primary);
  --gray-800: var(--text-primary);
  --gray-700: var(--text-secondary);
  --gray-600: var(--text-secondary);
  --gray-500: var(--text-muted);
  --gray-400: var(--border-color);
  --gray-300: var(--bg-muted);
  --gray-200: var(--bg-input);
  --gray-100: var(--bg-card);
  --blue-500: var(--primary-color);
  --blue-600: var(--primary-dark);
  border: none;
  font-family: var(--font-family);
}

:deep(.vc-highlight-content-light) {
  color: white !important;
  background-color: var(--primary-color) !important;
}

:deep(.vc-day-content:hover) {
  background-color: var(--primary-color-transparent);
  color: var(--primary-dark);
}

:deep(.vc-day-content:focus) {
  background-color: var(--primary-color-transparent);
}

:deep(.vc-weeks) {
  padding: 0;
}

:deep(.vc-weekday) {
  color: var(--text-secondary);
  font-weight: 600;
}

:deep(.vc-day) {
  min-height: 30px;
}

:deep(.vc-nav-title) {
  color: var(--text-primary);
  font-weight: 600;
}

:deep(.vc-nav-arrow) {
  color: var(--primary-color);
}

:deep(.vc-nav-popover-container) {
  border: 1px solid var(--border-color);
  background-color: var(--bg-card);
  color: var(--text-primary);
  border-radius: var(--border-radius);
  box-shadow: var(--shadow-md);
}

:deep(.vc-day-box-center-center) {
  font-size: 0.9rem;
}

:deep(.vc-dot) {
  width: 6px;
  height: 6px;
  margin: 1px 3px;
}

:deep(.event-dot-highlight) {
  width: 8px;
  height: 8px;
}

/* Today's summary styling */
.today-summary {
  background: var(--primary-gradient);
  border-radius: var(--border-radius);
  padding: 1.25rem;
  box-shadow: 0 8px 20px rgba(158, 120, 255, 0.2);
  color: white;
  position: relative;
  overflow: hidden;
  margin-bottom: 1.5rem;
  transition: all 0.3s ease;
}

.today-summary:hover {
  transform: translateY(-5px);
  box-shadow: 0 12px 28px rgba(158, 120, 255, 0.25);
}

.date-pill {
  background-color: rgba(255, 255, 255, 0.2);
  border-radius: 20px;
  padding: 0.4rem 1rem;
  font-size: 0.85rem;
  font-weight: 700;
  display: inline-block;
  margin-bottom: 1rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
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
}

.stat-item:hover {
  background-color: rgba(255, 255, 255, 0.2);
}

.stat-value {
  font-size: 1.75rem;
  font-weight: 700;
  margin-bottom: 0.25rem;
}

.stat-label {
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-weight: 500;
  opacity: 0.8;
}

/* Active Schedule Card & Upcoming Sessions Styling */
.active-schedule, .upcoming-sessions {
  background-color: var(--bg-card);
  border-radius: var(--border-radius);
  padding: 1.25rem;
  box-shadow: var(--shadow-sm);
  margin-bottom: 1.5rem;
  transition: all 0.3s ease;
}

.active-schedule:hover, .upcoming-sessions:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-3px);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.card-header h3 {
  margin: 0;
  font-size: 1.15rem;
  font-weight: 600;
  color: var(--primary-dark);
  position: relative;
  display: inline-block;
}

.card-header h3::after {
  content: '';
  position: absolute;
  left: 0;
  bottom: -4px;
  width: 30px;
  height: 2px;
  background: var(--primary-gradient);
  border-radius: 2px;
}

.badge {
  background-color: var(--primary-color-transparent);
  color: var(--primary-color);
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 600;
}

.change-schedule-btn, .view-all-btn {
  font-size: 0.8rem;
  padding: 0.4rem 0.8rem;
  background-color: var(--bg-input);
  color: var(--text-secondary);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.35rem;
  transition: all 0.3s ease;
}

.change-schedule-btn:hover, .view-all-btn:hover {
  background-color: var(--bg-hover);
  color: var(--primary-color);
  border-color: var(--primary-color-transparent);
}

.change-schedule-btn svg, .view-all-btn svg {
  transition: transform 0.3s ease;
}

.change-schedule-btn:hover svg, .view-all-btn:hover svg {
  transform: scale(1.2);
}

.refresh-btn {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--bg-input);
  color: var(--text-secondary);
  border: 1px solid var(--border-color);
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.3s ease;
}

.refresh-btn:hover {
  background-color: var(--primary-color-transparent);
  color: var(--primary-color);
  transform: rotate(180deg);
  border-color: var(--primary-color-transparent);
}

.schedule-info {
  margin-bottom: 1rem;
}

.schedule-name {
  font-weight: 700;
  font-size: 1.1rem;
  margin-bottom: 0.5rem;
  color: var(--text-primary);
}

.schedule-dates {
  font-size: 0.85rem;
  color: var(--text-secondary);
  margin-bottom: 1rem;
}

/* Progress bar */
.progress-container {
  margin-bottom: 1rem;
}

.progress-label {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
  font-size: 0.85rem;
  color: var(--text-secondary);
}

.progress-bar {
  height: 8px;
  background-color: var(--bg-input);
  border-radius: 4px;
  overflow: hidden;
}

.progress-value {
  height: 100%;
  background: var(--primary-gradient);
  border-radius: 4px;
  transition: width 0.5s ease;
}

.schedule-stats {
  display: flex;
  justify-content: space-between;
  gap: 0.75rem;
  background-color: var(--bg-input);
  padding: 0.75rem;
  border-radius: var(--border-radius);
}

.stat {
  text-align: center;
  flex: 1;
}

.stat .value {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--primary-dark);
  display: block;
  margin-bottom: 0.25rem;
}

.stat .label {
  font-size: 0.75rem;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* Sessions List Styling */
.sessions-list {
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
  max-height: 450px;
  overflow-y: auto;
  padding-right: 0.25rem;
  margin-bottom: 0.5rem;
}

.sessions-list::-webkit-scrollbar {
  width: 4px;
}

.sessions-list::-webkit-scrollbar-track {
  background: transparent;
}

.sessions-list::-webkit-scrollbar-thumb {
  background-color: var(--primary-color-transparent);
  border-radius: 4px;
}

.session-card {
  display: flex;
  gap: 0.75rem;
  padding: 0.85rem;
  border-radius: var(--border-radius);
  background-color: var(--bg-light);
  box-shadow: var(--shadow-sm);
  transition: all 0.3s ease;
  position: relative;
  border-left: 3px solid var(--border-color);
}

.planned-session {
  border-left-color: var(--text-secondary);
}

.active-session, .session-card.active-now {
  border-left-color: var(--warning-color);
  background-color: rgba(255, 152, 0, 0.05);
}

.completed-session {
  border-left-color: var(--success-color);
  opacity: 0.8;
}

.missed-session {
  border-left-color: var(--error-color);
  opacity: 0.7;
}

.session-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.session-time {
  min-width: 80px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.session-date {
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--text-secondary);
  margin-bottom: 0.25rem;
}

.session-hours {
  font-size: 0.7rem;
  color: var(--text-muted);
  background-color: var(--bg-input);
  padding: 0.15rem 0.5rem;
  border-radius: 3px;
  display: inline-block;
}

.session-countdown {
  font-size: 0.7rem;
  color: var(--warning-color);
  margin-top: 0.35rem;
  font-weight: 600;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% { opacity: 0.7; }
  50% { opacity: 1; }
  100% { opacity: 0.7; }
}

.session-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  overflow: hidden;
}

.session-title {
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 0.2rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.session-module {
  font-size: 0.75rem;
  color: var(--text-secondary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.session-actions {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  opacity: 0;
  transform: translateX(10px);
  transition: all 0.3s ease;
}

.session-card:hover .session-actions {
  opacity: 1;
  transform: translateX(0);
}

.action-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  border: 1px solid var(--border-color);
  background-color: var(--bg-input);
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.complete-btn {
  color: var(--success-color);
}

.complete-btn:hover, .complete-btn.completed {
  background-color: rgba(76, 175, 80, 0.15);
  color: var(--success-color);
  border-color: var(--success-color);
}

.missed-btn {
  color: var(--error-color);
}

.missed-btn:hover {
  background-color: rgba(244, 67, 54, 0.15);
  color: var(--error-color);
  border-color: var(--error-color);
}

.reschedule-btn {
  color: var(--warning-color);
}

.reschedule-btn:hover {
  background-color: rgba(255, 152, 0, 0.15);
  color: var(--warning-color);
  border-color: var(--warning-color);
}

.edit-btn {
  color: var(--primary-color);
}

.edit-btn:hover {
  background-color: var(--primary-color-transparent);
  color: var(--primary-color);
  border-color: var(--primary-color);
}

.delete-btn {
  color: var(--error-color);
}

.delete-btn:hover {
  background-color: rgba(244, 67, 54, 0.15);
  color: var(--error-color);
  border-color: var(--error-color);
}

.session-status {
  position: absolute;
  top: 0.25rem;
  right: 0.25rem;
  font-size: 0.65rem;
  letter-spacing: 0.5px;
  font-weight: 600;
}

.status {
  padding: 0.15rem 0.5rem;
  border-radius: 3px;
}

.status.planned {
  background-color: var(--bg-input);
  color: var(--text-secondary);
}

.status.active, .status.in-progress {
  background-color: rgba(255, 152, 0, 0.15);
  color: var(--warning-color);
}

.status.completed {
  background-color: rgba(76, 175, 80, 0.15);
  color: var(--success-color);
}

.status.missed {
  background-color: rgba(244, 67, 54, 0.15);
  color: var(--error-color);
}

.completion-time {
  font-size: 0.6rem;
  margin-left: 0.35rem;
  opacity: 0.8;
}

/* More sessions button */
.more-sessions {
  text-align: center;
  padding: 0.5rem 0;
}

.more-btn {
  border: none;
  background: transparent;
  color: var(--primary-color);
  font-size: 0.85rem;
  cursor: pointer;
  transition: all 0.3s ease;
  padding: 0.35rem 0.75rem;
  border-radius: var(--border-radius);
}

.more-btn:hover {
  background-color: var(--primary-color-transparent);
  text-decoration: underline;
}

/* Events section styling */
.events-container {
  background-color: var(--bg-card);
  border-radius: var(--border-radius);
  padding: 1.25rem;
  box-shadow: var(--shadow-sm);
  margin-bottom: 1.5rem;
  transition: all 0.3s ease;
}

.events-container:hover {
  box-shadow: var(--shadow-md);
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
  box-shadow: 0 4px 10px rgba(158, 120, 255, 0.2);
  transition: all 0.3s ease;
}

.add-event-btn:hover {
  background-color: var(--primary-dark);
  transform: scale(1.1);
  box-shadow: 0 6px 15px rgba(158, 120, 255, 0.3);
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
  border: 3px solid var(--primary-color-transparent);
  border-radius: 50%;
  border-top-color: var(--primary-color);
  animation: spin 1.2s ease infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
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
}

.schedule-btn {
  background-color: var(--primary-color-transparent);
  color: var(--primary-color);
  border: 1px solid var(--border-color);
  border-radius: 30px;
  padding: 0.75rem 1.5rem;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.schedule-btn:hover {
  background-color: var(--primary-color);
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(158, 120, 255, 0.2);
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
  transition: all 0.3s ease;
  position: relative;
  background-color: var(--bg-light);
  box-shadow: var(--shadow-sm);
  border-left: 3px solid transparent;
}

.event-card:hover {
  transform: translateY(-3px);
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
  box-shadow: 0 4px 10px rgba(158, 120, 255, 0.2);
}

.save-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 15px rgba(158, 120, 255, 0.3);
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

/* Session details */
.session-details {
  margin-bottom: 1.5rem;
  padding: 1rem;
  background-color: var(--bg-input);
  border-radius: var(--border-radius);
  border-left: 3px solid var(--primary-color);
}

.session-details .session-title {
  font-size: 1.1rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  color: var(--text-primary);
}

.session-details .session-time {
  font-size: 0.9rem;
  color: var(--text-secondary);
  min-width: auto;
}

/* Rating buttons */
.rating-buttons {
  display: flex;
  gap: 0.5rem;
  margin-top: 0.5rem;
}

.rating-btn {
  flex: 1;
  padding: 0.65rem 0;
  border: 1px solid var(--border-color);
  background-color: var(--bg-input);
  color: var(--text-secondary);
  border-radius: var(--border-radius);
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.rating-btn:hover {
  border-color: var(--primary-color);
  color: var(--primary-color);
}

.rating-btn.active {
  background-color: var(--primary-color);
  color: white;
  border-color: var(--primary-color);
}

/* Tags input */
.tags-input {
  margin-top: 0.5rem;
}

.tags-input input {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  background-color: var(--bg-input);
  color: var(--text-primary);
  font-family: inherit;
  transition: all 0.3s ease;
}

.tags-input input:focus {
  border-color: var(--primary-color);
  outline: none;
  box-shadow: 0 0 0 3px var(--primary-color-transparent);
}

.tags-container {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: 0.75rem;
}

.tag {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.25rem 0.75rem;
  background-color: var(--primary-color-transparent);
  color: var(--primary-color);
  border-radius: 20px;
  font-size: 0.85rem;
}

.remove-tag {
  background: none;
  border: none;
  font-size: 1.1rem;
  line-height: 1;
  cursor: pointer;
  color: inherit;
  padding: 0;
  margin: 0;
}

/* Responsive styles */
@media (max-width: 992px) {
  .study-hub-sidebar {
    width: 280px;
  }

  .sidebar-header h2 {
    font-size: 1.4rem;
  }

  .sidebar-content {
    padding: 1.25rem;
    gap: 1.25rem;
  }
}

@media (max-width: 768px) {
  .study-hub-sidebar {
    width: 250px;
  }

  .sidebar-content {
    padding: 1rem;
    gap: 1rem;
  }

  .sidebar-header h2 {
    font-size: 1.3rem;
  }

  .current-month {
    font-size: 0.9rem;
    padding: 0.2rem 0.6rem;
  }

  .nav-btn {
    width: 32px;
    height: 32px;
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
    padding: 0.75rem;
  }

  .confirmation-actions {
    flex-direction: column-reverse;
    gap: 0.75rem;
  }

  /* Improved Quick Stats for mobile */
  .quick-stats {
    gap: 0.5rem;
  }

  .stat-item {
    padding: 0.6rem 0.4rem;
  }

  .stat-value {
    font-size: 1.4rem;
  }

  .event-actions {
    opacity: 1;
    transform: translateX(0);
    flex-direction: row;
  }

  .event-card {
    position: relative;
    padding-right: 40px;
  }

  .event-actions {
    position: absolute;
    right: 8px;
    top: 50%;
    transform: translateY(-50%);
  }

  .modal-header h2 {
    font-size: 1.2rem;
  }

  .modal-body {
    padding: 1.25rem;
  }

  .events-header h3 {
    font-size: 1.1rem;
  }

  .add-event-btn {
    width: 32px;
    height: 32px;
  }
}

@media (max-width: 480px) {
  .study-hub-sidebar {
    width: 100%;  /* Full width on very small screens */
  }

  .sidebar-content {
    padding: 0.75rem;
    gap: 0.75rem;
  }

  .sidebar-header h2 {
    font-size: 1.2rem;
  }

  .month-navigator {
    padding: 0.4rem;
    margin: 0.4rem 0 0.75rem;
  }

  .nav-btn {
    width: 30px;
    height: 30px;
  }

  .current-month {
    font-size: 0.85rem;
    padding: 0.15rem 0.5rem;
  }

  .today-summary {
    padding: 1rem;
  }

  .date-pill {
    font-size: 0.8rem;
    padding: 0.3rem 0.75rem;
  }

  .stat-value {
    font-size: 1.3rem;
  }

  .stat-label {
    font-size: 0.7rem;
  }

  .events-container {
    padding: 1rem;
  }

  .modal-header {
    padding: 1rem;
  }

  .modal-body {
    padding: 1rem;
  }

  .event-card {
    padding: 0.75rem;
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

  .calendar-wrapper {
    padding: 0.25rem;
  }
}

/* Animation for touch devices */
@media (hover: none) {
  /* Ensure buttons have visual feedback on mobile */
  .nav-btn:active,
  .add-event-btn:active,
  .action-btn:active,
  .schedule-btn:active,
  .save-btn:active,
  .cancel-btn:active {
    transform: scale(0.92);
  }

  .event-card:active {
    background-color: var(--bg-hover);
  }

  /* Make event actions always visible but subtle until tapped */
  .event-actions, .session-actions {
    opacity: 0.7;
  }

  .event-card:active .event-actions,
  .session-card:active .session-actions {
    opacity: 1;
  }
}
</style>