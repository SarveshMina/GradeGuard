<template>
  <div class="dashboard" :class="{ 'dark-mode': darkMode, 'animate-in': animateIn }">
    <!-- Dashboard NavBar at the top -->
    <DashboardNavBar
        :userName="userProfile.firstName || 'User'"
        :userEmail="userProfile.email || 'user@example.com'"
        :userAvatar="userProfile.avatar"
        :isMobile="isMobile"
        @logout="handleLogout"
    />

    <!-- Layout container: main content and sidebar -->
    <div
        class="dashboard-layout"
        @touchstart="handleTouchStart"
        @touchmove="handleTouchMove"
        @touchend="handleTouchEnd"
    >
      <!-- Floating collapse button that appears when sidebar is hidden -->
      <button
          v-if="!sidebarVisible"
          @click="toggleSidebar"
          class="sidebar-toggle sidebar-show-button pulse-animation"
          aria-label="Show sidebar"
      >
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M15 18l-6-6 6-6" />
        </svg>
        <span class="toggle-text">Calendar</span>
      </button>

      <!-- Main Content Area -->
      <div class="dashboard-main-content" :class="{ 'expanded': !sidebarVisible }">
        <div class="dashboard-header">
          <h1 class="animate-fade-in">Calendar</h1>
          <div class="calendar-actions">
            <div class="view-selector">
              <button
                  class="view-btn"
                  :class="{ active: currentView === 'month' }"
                  @click="setView('month')"
              >
                Month
              </button>
              <button
                  class="view-btn"
                  :class="{ active: currentView === 'week' }"
                  @click="setView('week')"
              >
                Week
              </button>
              <button
                  class="view-btn"
                  :class="{ active: currentView === 'day' }"
                  @click="setView('day')"
              >
                Day
              </button>
            </div>
            <button class="add-event-button bounce-on-hover" @click="openCreateEventModal">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <line x1="12" y1="5" x2="12" y2="19"></line>
                <line x1="5" y1="12" x2="19" y2="12"></line>
              </svg>
              <span>Add Event</span>
            </button>
          </div>
        </div>

        <!-- If not logged in -->
        <div v-if="notLoggedIn" class="center-content auth-prompt animate-fade-in">
          <div class="auth-card">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="pulse-animation">
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
              <circle cx="12" cy="7" r="4"></circle>
            </svg>
            <h2>Welcome to GradeGuard</h2>
            <p>Please sign in to access your calendar.</p>
            <a href="/login" class="login-button bounce-on-hover">Go to Login</a>
          </div>
        </div>

        <!-- Loading state -->
        <div v-else-if="loading" class="loading-container">
          <div class="loading-spinner"></div>
          <p class="animate-fade-in">Loading your calendar...</p>
        </div>

        <!-- Calendar content -->
        <div v-else class="calendar-content">
          <!-- Search and Filter Bar -->
          <div class="search-filter-container animate-slide-down">
            <div class="search-box">
              <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="11" cy="11" r="8"></circle>
                <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
              </svg>
              <input
                  type="text"
                  v-model="searchQuery"
                  placeholder="Search events..."
                  @input="applyFilters"
              />
              <button v-if="searchQuery" @click="clearSearch" class="clear-search">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <line x1="18" y1="6" x2="6" y2="18"></line>
                  <line x1="6" y1="6" x2="18" y2="18"></line>
                </svg>
              </button>
            </div>
            <div class="filter-box">
              <button @click="toggleFilterPanel" class="filter-button" :class="{'active': showFilterPanel}">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"></polygon>
                </svg>
                <span>Filter</span>
                <span v-if="activeFilterCount > 0" class="filter-count">{{ activeFilterCount }}</span>
              </button>
            </div>
          </div>

          <!-- Filter Panel -->
          <div v-if="showFilterPanel" class="filter-panel animate-fade-in">
            <div class="filter-section">
              <h3>Event Type</h3>
              <div class="filter-options">
                <label class="checkbox-container" v-for="type in eventTypes" :key="type.value">
                  <input
                      type="checkbox"
                      v-model="filters.types"
                      :value="type.value"
                      @change="applyFilters"
                  />
                  <span class="checkmark" :style="{ backgroundColor: type.color }"></span>
                  {{ type.label }}
                </label>
              </div>
            </div>
            <div class="filter-section">
              <h3>Status</h3>
              <div class="filter-options">
                <label class="checkbox-container">
                  <input
                      type="checkbox"
                      v-model="filters.showCompleted"
                      @change="applyFilters"
                  />
                  <span class="checkmark"></span>
                  Show Completed
                </label>
                <label class="checkbox-container">
                  <input
                      type="checkbox"
                      v-model="filters.showIncomplete"
                      @change="applyFilters"
                  />
                  <span class="checkmark"></span>
                  Show Incomplete
                </label>
              </div>
            </div>
            <div class="filter-section">
              <h3>Time Frame</h3>
              <div class="filter-options">
                <label class="checkbox-container">
                  <input
                      type="checkbox"
                      v-model="filters.showAllDay"
                      @change="applyFilters"
                  />
                  <span class="checkmark"></span>
                  All Day Events
                </label>
                <label class="checkbox-container">
                  <input
                      type="checkbox"
                      v-model="filters.showTimedEvents"
                      @change="applyFilters"
                  />
                  <span class="checkmark"></span>
                  Timed Events
                </label>
              </div>
            </div>
            <div class="filter-actions">
              <button @click="resetFilters" class="reset-filter-button">
                Reset Filters
              </button>
              <button @click="showFilterPanel = false" class="apply-filter-button">
                Apply Filters
              </button>
            </div>
          </div>

          <!-- No Results Message -->
          <div v-if="filteredEvents.length === 0 && !loading && (searchQuery || activeFilterCount > 0)" class="no-results animate-fade-in">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="pulse-animation">
              <circle cx="12" cy="12" r="10"></circle>
              <line x1="12" y1="8" x2="12" y2="12"></line>
              <line x1="12" y1="16" x2="12.01" y2="16"></line>
            </svg>
            <h3>No events match your search</h3>
            <p>Try adjusting your search or filters to find what you're looking for.</p>
            <button @click="resetFilters" class="reset-search-button bounce-on-hover">Reset All Filters</button>
          </div>

          <div class="calendar-header animate-slide-down">
            <div class="month-navigator">
              <button @click="navigatePrevious" class="nav-btn">
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M15 18l-6-6 6-6" />
                </svg>
              </button>
              <button @click="navigateToday" class="today-btn pulse-animation">Today</button>
              <button @click="navigateNext" class="nav-btn">
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M9 18l6-6-6-6" />
                </svg>
              </button>
              <span class="current-period">{{ formatCurrentPeriod() }}</span>
            </div>
          </div>

          <!-- Views Container with Transitions -->
          <transition
              :name="viewTransitionName"
              mode="out-in"
          >
            <!-- Month View -->
            <div v-if="currentView === 'month'" key="month" class="month-view">
              <div class="month-grid-header">
                <div class="day-header" v-for="day in weekdays" :key="day">{{ isMobile ? day.slice(0,3) : day }}</div>
              </div>
              <div class="month-grid">
                <div
                    v-for="(day, index) in monthDays"
                    :key="index"
                    class="day-cell"
                    :class="{
                    'today': isToday(day.date),
                    'different-month': !day.isCurrentMonth,
                    'selected': isSelectedDate(day.date)
                  }"
                    @click="selectDate(day.date)"
                >
                  <div class="day-number">{{ formatDayNumber(day.date) }}</div>
                  <div class="day-events">
                    <div
                        v-for="event in getFilteredEventsForDay(day.date).slice(0, isMobile ? 1 : 2)"
                        :key="event.id"
                        class="day-event-pill"
                        :class="getEventClass(event)"
                        @click.stop="openEventDetails(event)"
                    >
                      {{ event.title }}
                    </div>
                    <div v-if="getFilteredEventsForDay(day.date).length > (isMobile ? 1 : 2)" class="more-events">
                      +{{ getFilteredEventsForDay(day.date).length - (isMobile ? 1 : 2) }} more
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Week View -->
            <div v-else-if="currentView === 'week'" key="week" class="week-view">
              <div class="week-grid-header">
                <div class="time-column-header"></div>
                <div class="day-column-header" v-for="(day, index) in weekDays" :key="index" :class="{ 'today': isToday(day.date) }">
                  <div class="day-name">{{ isMobile ? formatDayName(day.date).slice(0,1) : formatDayName(day.date) }}</div>
                  <div class="day-number">{{ formatDayNumber(day.date) }}</div>
                </div>
              </div>
              <div class="week-grid">
                <div class="time-column">
                  <div class="time-cell" v-for="hour in displayHours" :key="hour">
                    {{ formatHour(hour) }}
                  </div>
                </div>
                <div class="day-columns">
                  <div
                      class="day-column"
                      v-for="(day, dayIndex) in weekDays"
                      :key="dayIndex"
                      :class="{ 'today': isToday(day.date) }"
                  >
                    <div
                        class="time-cell"
                        v-for="hour in displayHours"
                        :key="`${dayIndex}-${hour}`"
                        @click="createEventAtTime(day.date, hour)"
                    ></div>
                    <div
                        v-for="event in getFilteredEventsForDay(day.date)"
                        :key="event.id"
                        class="week-event animate-pop-in"
                        :class="getEventClass(event)"
                        :style="calculateEventPosition(event)"
                        @click="openEventDetails(event)"
                    >
                      <div class="event-time">{{ formatEventTime(event) }}</div>
                      <div class="event-title">{{ event.title }}</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Day View -->
            <div v-else-if="currentView === 'day'" key="day" class="day-view">
              <div class="day-view-header">
                <div class="current-day">
                  {{ formatFullDate(selectedDate) }}
                </div>
              </div>
              <div class="day-view-grid">
                <div class="time-column">
                  <div class="time-cell" v-for="hour in displayHours" :key="hour">
                    {{ formatHour(hour) }}
                  </div>
                </div>
                <div class="events-column">
                  <div
                      class="time-cell"
                      v-for="hour in displayHours"
                      :key="hour"
                      @click="createEventAtTime(selectedDate, hour)"
                  ></div>
                  <div
                      v-for="event in getFilteredEventsForDay(selectedDate)"
                      :key="event.id"
                      class="day-event animate-pop-in"
                      :class="getEventClass(event)"
                      :style="calculateEventPosition(event)"
                      @click="openEventDetails(event)"
                  >
                    <div class="event-time">{{ formatEventTime(event) }}</div>
                    <div class="event-title">{{ event.title }}</div>
                    <div class="event-description">{{ event.description }}</div>
                  </div>
                </div>
              </div>
            </div>
          </transition>
        </div>
      </div>

      <!-- Sidebar with Calendar -->
      <transition name="slide">
        <aside v-if="sidebarVisible" class="dashboard-sidebar">
          <!-- Hide sidebar button -->
          <button
              @click="toggleSidebar"
              class="sidebar-toggle sidebar-hide-button"
              aria-label="Hide sidebar"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M9 18l6-6-6-6" />
            </svg>
            <span class="toggle-text">Hide</span>
          </button>
          <CalendarSidebar
              :events="filteredEvents"
              :selected-date="selectedDate"
              @day-click="selectDate"
              @add-event="openCreateEventModal"
              @edit-event="editEvent"
              @delete-event="confirmDeleteEvent"
              @toggle-completion="toggleEventCompletion"
          />
        </aside>
      </transition>
    </div>

    <!-- Create/Edit Event Modal -->
    <transition name="modal-fade">
      <div v-if="showEventModal" class="modal-overlay" @click.self="closeEventModal">
        <div class="modal-container">
          <div class="modal-header">
            <h2>{{ isEditMode ? 'Edit Event' : 'Create New Event' }}</h2>
            <button @click="closeEventModal" class="close-modal-btn">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <line x1="18" y1="6" x2="6" y2="18"></line>
                <line x1="6" y1="6" x2="18" y2="18"></line>
              </svg>
            </button>
          </div>
          <div class="modal-body">
            <div class="form-group">
              <label for="eventTitle">Event Title*</label>
              <input
                  type="text"
                  id="eventTitle"
                  v-model="eventForm.title"
                  placeholder="Add a title for your event"
                  required
              />
            </div>

            <div class="form-row">
              <div class="form-group">
                <label for="eventDate">Date*</label>
                <input
                    type="date"
                    id="eventDate"
                    v-model="eventForm.date"
                    required
                />
              </div>
              <div class="form-group">
                <label for="eventType">Event Type</label>
                <select id="eventType" v-model="eventForm.type">
                  <option value="general">General</option>
                  <option value="assignment">Assignment</option>
                  <option value="exam">Exam</option>
                  <option value="study">Study</option>
                  <option value="meeting">Meeting</option>
                  <option value="celebration">Celebration</option>
                </select>
              </div>
            </div>

            <div class="form-row">
              <div class="form-group checkbox-group">
                <label class="checkbox-container">
                  <input type="checkbox" v-model="eventForm.all_day" />
                  <span class="checkmark"></span>
                  All Day Event
                </label>
              </div>
            </div>

            <div class="form-row" v-if="!eventForm.all_day">
              <div class="form-group">
                <label for="startTime">Start Time</label>
                <input
                    type="time"
                    id="startTime"
                    v-model="eventForm.start_time"
                />
              </div>
              <div class="form-group">
                <label for="endTime">End Time</label>
                <input
                    type="time"
                    id="endTime"
                    v-model="eventForm.end_time"
                />
              </div>
            </div>

            <div class="form-group">
              <label for="eventDescription">Description</label>
              <textarea
                  id="eventDescription"
                  v-model="eventForm.description"
                  rows="4"
                  placeholder="Add details about your event"
              ></textarea>
            </div>

            <div class="form-group checkbox-group" v-if="isEditMode">
              <label class="checkbox-container">
                <input type="checkbox" v-model="eventForm.completed" />
                <span class="checkmark"></span>
                Mark as Completed
              </label>
            </div>
          </div>
          <div class="modal-footer">
            <div class="modal-actions">
              <button v-if="isEditMode" @click="confirmDeleteEvent" class="delete-button">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <polyline points="3 6 5 6 21 6"></polyline>
                  <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                  <line x1="10" y1="11" x2="10" y2="17"></line>
                  <line x1="14" y1="11" x2="14" y2="17"></line>
                </svg>
                Delete
              </button>
              <div>
                <button @click="closeEventModal" class="cancel-button">
                  Cancel
                </button>
                <button @click="saveEvent" class="save-button bounce-on-hover" :disabled="isSaving">
                  <span v-if="isSaving">Saving...</span>
                  <span v-else>{{ isEditMode ? 'Update Event' : 'Create Event' }}</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </transition>

    <!-- Event Details Modal -->
    <transition name="modal-fade">
      <div v-if="showEventDetailsModal" class="modal-overlay" @click.self="closeEventDetailsModal">
        <div class="modal-container">
          <div class="modal-header">
            <h2>Event Details</h2>
            <button @click="closeEventDetailsModal" class="close-modal-btn">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <line x1="18" y1="6" x2="6" y2="18"></line>
                <line x1="6" y1="6" x2="18" y2="18"></line>
              </svg>
            </button>
          </div>
          <div class="modal-body">
            <div class="event-details animate-fade-in">
              <div class="event-details-header" :class="getEventClass(selectedEvent)">
                <h3>{{ selectedEvent?.title }}</h3>
                <span class="event-badge">{{ getEventTypeLabel(selectedEvent?.type) }}</span>
              </div>

              <div class="event-details-content">
                <div class="event-details-item">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                    <line x1="16" y1="2" x2="16" y2="6"></line>
                    <line x1="8" y1="2" x2="8" y2="6"></line>
                    <line x1="3" y1="10" x2="21" y2="10"></line>
                  </svg>
                  <span>{{ formatEventDate(selectedEvent) }}</span>
                </div>

                <div class="event-details-item" v-if="!selectedEvent?.all_day">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="12" cy="12" r="10"></circle>
                    <polyline points="12 6 12 12 16 14"></polyline>
                  </svg>
                  <span>{{ formatEventTime(selectedEvent) }}</span>
                </div>

                <div class="event-details-item" v-else>
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="12" cy="12" r="10"></circle>
                    <line x1="12" y1="8" x2="12" y2="12"></line>
                    <line x1="12" y1="16" x2="12.01" y2="16"></line>
                  </svg>
                  <span>All Day</span>
                </div>

                <div class="event-details-description" v-if="selectedEvent?.description">
                  <h4>Description</h4>
                  <p>{{ selectedEvent?.description }}</p>
                </div>

                <div class="event-status" v-if="selectedEvent?.completed">
                  <span class="status-badge">Completed</span>
                </div>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <div class="modal-actions">
              <button @click="confirmDeleteEvent" class="delete-button">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <polyline points="3 6 5 6 21 6"></polyline>
                  <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                  <line x1="10" y1="11" x2="10" y2="17"></line>
                  <line x1="14" y1="11" x2="14" y2="17"></line>
                </svg>
                Delete
              </button>
              <div>
                <button @click="closeEventDetailsModal" class="cancel-button">
                  Close
                </button>
                <button @click="editEvent(selectedEvent)" class="save-button">
                  Edit Event
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </transition>

    <!-- Delete Confirmation Modal -->
    <transition name="modal-fade">
      <div v-if="showDeleteConfirmModal" class="modal-overlay">
        <div class="modal-container delete-confirm-modal animate-pop-in">
          <div class="modal-header">
            <h2>Confirm Delete</h2>
          </div>
          <div class="modal-body">
            <p>Are you sure you want to delete this event?</p>
            <p class="event-name">{{ selectedEvent?.title }}</p>
            <p class="delete-warning">This action cannot be undone.</p>
          </div>
          <div class="modal-footer">
            <button @click="showDeleteConfirmModal = false" class="cancel-button">
              Cancel
            </button>
            <button @click="deleteEvent" class="delete-button" :disabled="isDeleting">
              <span v-if="isDeleting">Deleting...</span>
              <span v-else>Delete</span>
            </button>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
import axios from "axios";
import { notify } from "@/services/toastService.js";
import DashboardNavBar from "@/components/DashboardNavBar.vue";
import CalendarSidebar from "@/components/CalendarSideBar.vue";
import { getDarkModePreference } from "@/services/darkModeService.js";
import { API_URL } from "@/config.js";

export default {
  name: "Calendar",
  components: { DashboardNavBar, CalendarSidebar },
  data() {
    return {
      darkMode: false,
      notLoggedIn: false,
      loading: true,
      sidebarVisible: true,
      isMobile: false,
      animateIn: true,

      // Animation state
      viewTransitionName: 'fade',
      touchStartX: 0,
      touchEndX: 0,

      // User data
      userProfile: {
        firstName: "",
        email: "",
        avatar: ""
      },

      // Calendar state
      currentDate: new Date(),
      selectedDate: new Date(),
      currentView: 'month', // 'month', 'week', 'day'
      weekdays: ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
      events: [],
      filteredEvents: [],

      // Search and Filter state
      searchQuery: '',
      showFilterPanel: false,
      filters: {
        types: [], // Array of event types to filter by
        showCompleted: true,
        showIncomplete: true,
        showAllDay: true,
        showTimedEvents: true,
      },
      eventTypes: [
        { value: 'general', label: 'General', color: '#2196F3' },
        { value: 'assignment', label: 'Assignment', color: '#F44336' },
        { value: 'exam', label: 'Exam', color: '#E91E63' },
        { value: 'study', label: 'Study Session', color: '#4CAF50' },
        { value: 'meeting', label: 'Meeting', color: '#673AB7' },
        { value: 'celebration', label: 'Celebration', color: '#FF9800' }
      ],

      // Modal state
      showEventModal: false,
      showEventDetailsModal: false,
      showDeleteConfirmModal: false,
      isEditMode: false,
      isSaving: false,
      isDeleting: false,
      selectedEvent: null,

      // Form data
      eventForm: {
        id: null,
        title: '',
        description: '',
        date: this.formatDateForInput(new Date()),
        all_day: true,
        start_time: '09:00',
        end_time: '10:00',
        type: 'general',
        completed: false
      },

      // For week and day views
      hours: Array.from({ length: 24 }, (_, i) => i),
    };
  },
  computed: {
    monthDays() {
      const year = this.currentDate.getFullYear();
      const month = this.currentDate.getMonth();

      // First day of current month
      const firstDay = new Date(year, month, 1);
      const firstDayOfWeek = firstDay.getDay();

      // Last day of current month
      const lastDay = new Date(year, month + 1, 0);
      const daysInMonth = lastDay.getDate();

      // Days from previous month
      const daysFromPrevMonth = firstDayOfWeek;
      const prevMonth = new Date(year, month, 0);
      const prevMonthDays = prevMonth.getDate();

      const days = [];

      // Add days from previous month
      for (let i = daysFromPrevMonth - 1; i >= 0; i--) {
        const date = new Date(year, month - 1, prevMonthDays - i);
        days.push({
          date,
          isCurrentMonth: false
        });
      }

      // Add days from current month
      for (let i = 1; i <= daysInMonth; i++) {
        const date = new Date(year, month, i);
        days.push({
          date,
          isCurrentMonth: true
        });
      }

      // Add days from next month to complete the grid (6 rows x 7 days = 42 cells)
      const remainingDays = 42 - days.length;
      for (let i = 1; i <= remainingDays; i++) {
        const date = new Date(year, month + 1, i);
        days.push({
          date,
          isCurrentMonth: false
        });
      }

      return days;
    },

    weekDays() {
      const startOfWeek = this.getStartOfWeek(this.currentDate);
      const days = [];

      for (let i = 0; i < 7; i++) {
        const date = new Date(startOfWeek);
        date.setDate(startOfWeek.getDate() + i);
        days.push({ date });
      }

      return days;
    },

    // For mobile optimization: Show limited hours in week/day view
    displayHours() {
      if (!this.isMobile) return this.hours;

      // For mobile, show business hours (8am-8pm) to save space
      return Array.from({ length: 13 }, (_, i) => i + 8);
    },

    // Compute the number of active filters
    activeFilterCount() {
      let count = 0;

      // Count selected event types
      if (this.filters.types.length > 0) {
        count++;
      }

      // Count status filters if not both are selected (which is effectively no filter)
      if (!(this.filters.showCompleted && this.filters.showIncomplete)) {
        count++;
      }

      // Count time frame filters if not both are selected
      if (!(this.filters.showAllDay && this.filters.showTimedEvents)) {
        count++;
      }

      // Count search query
      if (this.searchQuery.trim() !== '') {
        count++;
      }

      return count;
    }
  },
  async mounted() {
    this.darkMode = getDarkModePreference();
    this.checkMobile();

    window.addEventListener("resize", this.checkMobile);
    window.addEventListener('darkModeChange', this.onDarkModeChange);

    // Add initial animation
    this.animateIn = true;
    setTimeout(() => {
      this.animateIn = false;
    }, 800);

    // Try to load sidebar preference from localStorage
    const storedSidebarState = localStorage.getItem('sidebarVisible');
    if (storedSidebarState !== null) {
      this.sidebarVisible = storedSidebarState === 'true';
    }

    // Initialize calendar view preference from localStorage
    const storedCalendarView = localStorage.getItem('calendarView');
    if (storedCalendarView) {
      this.currentView = storedCalendarView;
    }

    await this.fetchUserProfile();
    await this.fetchEvents();
  },
  beforeUnmount() {
    window.removeEventListener("resize", this.checkMobile);
    window.removeEventListener('darkModeChange', this.onDarkModeChange);
  },
  methods: {
    // UI Helpers
    toggleSidebar() {
      this.sidebarVisible = !this.sidebarVisible;
      localStorage.setItem('sidebarVisible', this.sidebarVisible);
    },

    onDarkModeChange(event) {
      this.darkMode = event.detail.isDark;
    },

    handleLogout() {
      this.notLoggedIn = true;
      this.$router.push("/login");
    },

    checkMobile() {
      this.isMobile = window.innerWidth <= 768;
      if (this.isMobile && this.sidebarVisible) {
        this.sidebarVisible = false;
        localStorage.setItem('sidebarVisible', 'false');
      }
    },

    // Touch gestures for mobile
    handleTouchStart(e) {
      this.touchStartX = e.changedTouches[0].screenX;
    },

    handleTouchMove(e) {
      // Prevent default to avoid scrolling while swiping
      if (Math.abs(e.changedTouches[0].screenX - this.touchStartX) > 30) {
        e.preventDefault();
      }
    },

    handleTouchEnd(e) {
      this.touchEndX = e.changedTouches[0].screenX;

      // Minimum swipe distance
      const minSwipeDistance = 100;
      const swipeDistance = this.touchEndX - this.touchStartX;

      // Detect direction
      if (Math.abs(swipeDistance) > minSwipeDistance) {
        if (swipeDistance > 0) {
          // Swipe right - previous period or show sidebar
          if (!this.sidebarVisible && this.touchStartX < 50) {
            this.toggleSidebar();
          } else {
            this.navigatePrevious();
            this.viewTransitionName = 'slide-right';
          }
        } else {
          // Swipe left - next period or hide sidebar
          if (this.sidebarVisible) {
            this.toggleSidebar();
          } else {
            this.navigateNext();
            this.viewTransitionName = 'slide-left';
          }
        }
      }
    },

    // View transitions
    setView(view) {
      if (view === this.currentView) return;

      // Set transition based on view change
      if (
          (this.currentView === 'month' && view === 'week') ||
          (this.currentView === 'week' && view === 'day')
      ) {
        this.viewTransitionName = 'zoom-in';
      } else if (
          (this.currentView === 'day' && view === 'week') ||
          (this.currentView === 'week' && view === 'month')
      ) {
        this.viewTransitionName = 'zoom-out';
      } else {
        this.viewTransitionName = 'fade';
      }

      this.currentView = view;
      localStorage.setItem('calendarView', view);
    },

    // Search and Filter Methods
    toggleFilterPanel() {
      this.showFilterPanel = !this.showFilterPanel;
    },

    clearSearch() {
      this.searchQuery = '';
      this.applyFilters();
    },

    resetFilters() {
      this.searchQuery = '';
      this.filters = {
        types: [],
        showCompleted: true,
        showIncomplete: true,
        showAllDay: true,
        showTimedEvents: true
      };
      this.applyFilters();
      this.showFilterPanel = false;
    },

    applyFilters() {
      // Start with all events
      let result = [...this.events];

      // Apply search query filter
      if (this.searchQuery.trim() !== '') {
        const query = this.searchQuery.toLowerCase().trim();
        result = result.filter(event =>
            event.title.toLowerCase().includes(query) ||
            (event.description && event.description.toLowerCase().includes(query))
        );
      }

      // Apply event type filters
      if (this.filters.types.length > 0) {
        result = result.filter(event => this.filters.types.includes(event.type));
      }

      // Apply completion status filters
      if (!this.filters.showCompleted) {
        result = result.filter(event => !event.completed);
      }

      if (!this.filters.showIncomplete) {
        result = result.filter(event => event.completed);
      }

      // Apply time frame filters
      if (!this.filters.showAllDay) {
        result = result.filter(event => !event.all_day);
      }

      if (!this.filters.showTimedEvents) {
        result = result.filter(event => event.all_day);
      }

      this.filteredEvents = result;
    },

    getFilteredEventsForDay(date) {
      const dateStr = this.formatDateISO(date);
      return this.filteredEvents.filter(event => event.date === dateStr);
    },

    // API Calls
    async fetchUserProfile() {
      try {
        const response = await axios.get(`${API_URL}/user/profile`, {
          withCredentials: true,
        });

        if (response.data) {
          this.userProfile = response.data;
          this.notLoggedIn = false;
        }
      } catch (error) {
        console.error("Error fetching user profile:", error);
        if (error.response?.status === 401) {
          this.notLoggedIn = true;
        }
      }
    },

    async toggleEventCompletion(event) {
      try {
        const updatedEvent = { ...event, completed: !event.completed };

        const response = await axios.put(
            `${API_URL}/calendar/events/${event.id}`,
            updatedEvent,
            { withCredentials: true }
        );

        // Update local state
        const index = this.events.findIndex(e => e.id === event.id);
        if (index !== -1) {
          this.events[index].completed = !event.completed;
          // Also update the filtered events array
          this.applyFilters();
        }

        notify({
          type: "success",
          message: updatedEvent.completed ? 'Event marked as completed!' : 'Event marked as incomplete!'
        });
      } catch (error) {
        console.error('Error updating event completion:', error);
        notify({ type: "error", message: 'Failed to update event. Please try again.' });
      }
    },

    async fetchEvents(startDate = null, endDate = null) {
      this.loading = true;
      try {
        // Add date parameters if provided
        const params = {};
        if (startDate) params.start_date = startDate;
        if (endDate) params.end_date = endDate;

        const response = await axios.get(`${API_URL}/calendar/events`, {
          withCredentials: true,
          params
        });

        this.events = response.data;
        this.filteredEvents = [...this.events]; // Initialize filtered events with all events
        this.notLoggedIn = false;
      } catch (error) {
        console.error("Error fetching events:", error);
        if (error.response?.status === 401) {
          this.notLoggedIn = true;
        } else {
          notify({ type: "error", message: "Failed to load events. Please try again." });
        }
      } finally {
        this.loading = false;
      }
    },

    async createNewEvent() {
      this.isSaving = true;
      try {
        // Format for API
        const eventData = {
          title: this.eventForm.title,
          description: this.eventForm.description || null,
          date: this.eventForm.date,
          all_day: this.eventForm.all_day,
          start_time: this.eventForm.all_day ? null : this.eventForm.start_time,
          end_time: this.eventForm.all_day ? null : this.eventForm.end_time,
          type: this.eventForm.type,
          completed: this.eventForm.completed
        };

        const response = await axios.post(
            `${API_URL}/calendar/events`,
            eventData,
            { withCredentials: true }
        );

        // Important: Use the server-returned event object (with its ID)
        this.events.push(response.data);
        this.applyFilters(); // Update filtered events
        this.closeEventModal();
        notify({ type: "success", message: "Event created successfully!" });
      } catch (error) {
        console.error("Error creating event:", error);
        notify({ type: "error", message: "Failed to create event. Please try again." });
      } finally {
        this.isSaving = false;
      }
    },

    async updateEvent() {
      this.isSaving = true;
      try {
        // Format for API
        const eventData = {
          title: this.eventForm.title,
          description: this.eventForm.description || null,
          date: this.eventForm.date,
          all_day: this.eventForm.all_day,
          start_time: this.eventForm.all_day ? null : this.eventForm.start_time,
          end_time: this.eventForm.all_day ? null : this.eventForm.end_time,
          type: this.eventForm.type,
          completed: this.eventForm.completed
        };

        const response = await axios.put(
            `${API_URL}/calendar/events/${this.eventForm.id}`,
            eventData,
            { withCredentials: true }
        );

        // Update local event
        const index = this.events.findIndex(e => e.id === this.eventForm.id);
        if (index !== -1) {
          this.events[index] = response.data;
          this.applyFilters(); // Update filtered events
        }

        this.closeEventModal();
        notify({ type: "success", message: "Event updated successfully!" });
      } catch (error) {
        console.error("Error updating event:", error);
        notify({ type: "error", message: "Failed to update event. Please try again." });
      } finally {
        this.isSaving = false;
      }
    },

    async deleteEvent() {
      this.isDeleting = true;
      try {
        await axios.delete(
            `${API_URL}/calendar/events/${this.selectedEvent.id}`,
            { withCredentials: true }
        );

        // Remove from local events
        this.events = this.events.filter(e => e.id !== this.selectedEvent.id);
        this.applyFilters(); // Update filtered events

        this.showDeleteConfirmModal = false;
        this.closeEventModal();
        this.closeEventDetailsModal();
        notify({ type: "success", message: "Event deleted successfully!" });
      } catch (error) {
        console.error("Error deleting event:", error);
        notify({ type: "error", message: "Failed to delete event. Please try again." });
      } finally {
        this.isDeleting = false;
      }
    },

    // Event Handlers
    saveEvent() {
      // Validate required fields
      if (!this.eventForm.title) {
        notify({ type: "warning", message: "Event title is required." });
        return;
      }

      if (!this.eventForm.date) {
        notify({ type: "warning", message: "Event date is required." });
        return;
      }

      if (!this.eventForm.all_day) {
        if (!this.eventForm.start_time) {
          notify({ type: "warning", message: "Start time is required for non-all-day events." });
          return;
        }

        if (!this.eventForm.end_time) {
          notify({ type: "warning", message: "End time is required for non-all-day events." });
          return;
        }

        // Validate end time is after start time
        if (this.eventForm.start_time >= this.eventForm.end_time) {
          notify({ type: "warning", message: "End time must be after start time." });
          return;
        }
      }

      if (this.isEditMode) {
        this.updateEvent();
      } else {
        this.createNewEvent();
      }
    },

    openCreateEventModal() {
      // Reset form
      this.isEditMode = false;
      this.eventForm = {
        id: null,
        title: '',
        description: '',
        date: this.formatDateForInput(this.selectedDate),
        all_day: true,
        start_time: '09:00',
        end_time: '10:00',
        type: 'general',
        completed: false
      };
      this.showEventModal = true;
    },

    editEvent(event) {
      this.isEditMode = true;
      this.eventForm = {
        id: event.id,
        title: event.title,
        description: event.description || '',
        date: this.formatDateForInput(new Date(event.date)),
        all_day: event.all_day,
        start_time: event.start_time || '09:00',
        end_time: event.end_time || '10:00',
        type: event.type || 'general',
        completed: event.completed || false
      };
      this.closeEventDetailsModal();
      this.showEventModal = true;
    },

    openEventDetails(event) {
      this.selectedEvent = event;
      this.showEventDetailsModal = true;
    },

    closeEventModal() {
      this.showEventModal = false;
    },

    closeEventDetailsModal() {
      this.showEventDetailsModal = false;
    },

    confirmDeleteEvent() {
      this.showDeleteConfirmModal = true;

      if (this.showEventModal) {
        this.closeEventModal();
      }

      if (this.showEventDetailsModal) {
        this.closeEventDetailsModal();
      }
    },

    // Calendar Navigation
    navigatePrevious() {
      const date = new Date(this.currentDate);

      // Set transition for navigation
      this.viewTransitionName = 'slide-right';

      if (this.currentView === 'month') {
        date.setMonth(date.getMonth() - 1);
      } else if (this.currentView === 'week') {
        date.setDate(date.getDate() - 7);
      } else if (this.currentView === 'day') {
        date.setDate(date.getDate() - 1);
      }

      this.currentDate = date;
    },

    navigateNext() {
      const date = new Date(this.currentDate);

      // Set transition for navigation
      this.viewTransitionName = 'slide-left';

      if (this.currentView === 'month') {
        date.setMonth(date.getMonth() + 1);
      } else if (this.currentView === 'week') {
        date.setDate(date.getDate() + 7);
      } else if (this.currentView === 'day') {
        date.setDate(date.getDate() + 1);
      }

      this.currentDate = date;
    },

    navigateToday() {
      // Set transition for navigation
      this.viewTransitionName = 'fade';
      this.currentDate = new Date();
      this.selectedDate = new Date();
    },

    selectDate(date) {
      this.selectedDate = new Date(date);

      if (this.currentView === 'month') {
        // Update current month if selected date is in a different month
        const currentMonth = this.currentDate.getMonth();
        const selectedMonth = this.selectedDate.getMonth();

        if (currentMonth !== selectedMonth) {
          this.currentDate = new Date(this.selectedDate);
        }
      }

      // If day view, update the current date
      if (this.currentView === 'day') {
        this.currentDate = new Date(this.selectedDate);
      }
    },

    // Event helpers
    getEventsForDay(date) {
      const dateStr = this.formatDateISO(date);
      return this.events.filter(event => event.date === dateStr);
    },

    getEventClass(event) {
      if (!event) return '';

      const typeMap = {
        'general': 'general-event',
        'assignment': 'assignment-event',
        'exam': 'exam-event',
        'study': 'study-event',
        'meeting': 'meeting-event',
        'celebration': 'celebration-event'
      };

      return [
        typeMap[event.type] || 'general-event',
        event.completed ? 'completed-event' : ''
      ].join(' ');
    },

    getEventTypeLabel(type) {
      const typeLabelMap = {
        'general': 'General',
        'assignment': 'Assignment',
        'exam': 'Exam',
        'study': 'Study Session',
        'meeting': 'Meeting',
        'celebration': 'Celebration'
      };

      return typeLabelMap[type] || 'General';
    },

    calculateEventPosition(event) {
      if (event.all_day) {
        return {
          top: '0',
          height: '30px'
        };
      }

      // Calculate position based on start and end times
      const startParts = event.start_time?.split(':') || ['0', '0'];
      const endParts = event.end_time?.split(':') || ['0', '0'];

      const startHour = parseInt(startParts[0]);
      const startMinute = parseInt(startParts[1]);
      const endHour = parseInt(endParts[0]);
      const endMinute = parseInt(endParts[1]);

      // Each hour is 60px height in our grid
      const hourHeight = 60;

      // Adjust for mobile display hours if needed
      let topOffset = 0;
      if (this.isMobile && startHour < 8) {
        // If event starts before our mobile view starts, adjust
        topOffset = 0;
      } else if (this.isMobile) {
        // For mobile, adjust based on our display hours (starts at 8am)
        topOffset = (startHour - 8) * hourHeight + (startMinute / 60 * hourHeight);
      } else {
        // Regular calculation for desktop
        topOffset = startHour * hourHeight + (startMinute / 60 * hourHeight);
      }

      // Calculate height (end time - start time in hours * hourHeight)
      const durationHours = (endHour - startHour) + (endMinute - startMinute) / 60;
      const height = durationHours * hourHeight;

      return {
        top: `${topOffset}px`,
        height: `${height}px`
      };
    },

    createEventAtTime(date, hour) {
      // Set up new event at the clicked time
      this.isEditMode = false;

      const startHour = hour < 10 ? `0${hour}` : `${hour}`;
      const endHour = hour < 9 ? `0${hour + 1}` : `${hour + 1}`;

      this.eventForm = {
        id: null,
        title: '',
        description: '',
        date: this.formatDateForInput(new Date(date)),
        all_day: false,
        start_time: `${startHour}:00`,
        end_time: `${endHour}:00`,
        type: 'general',
        completed: false
      };

      this.showEventModal = true;
    },

    // Date formatting helpers
    isToday(date) {
      const today = new Date();
      return date.getDate() === today.getDate() &&
          date.getMonth() === today.getMonth() &&
          date.getFullYear() === today.getFullYear();
    },

    isSelectedDate(date) {
      return date.getDate() === this.selectedDate.getDate() &&
          date.getMonth() === this.selectedDate.getMonth() &&
          date.getFullYear() === this.selectedDate.getFullYear();
    },

    formatDayNumber(date) {
      return date.getDate();
    },

    formatDayName(date) {
      return date.toLocaleDateString('en-US', { weekday: 'short' });
    },

    formatHour(hour) {
      // Format hour in 12-hour format with AM/PM
      if (hour === 0) return '12 AM';
      if (hour === 12) return '12 PM';
      return hour < 12 ? `${hour} AM` : `${hour - 12} PM`;
    },

    formatCurrentPeriod() {
      if (this.currentView === 'month') {
        return this.currentDate.toLocaleDateString('en-US', { month: 'long', year: 'numeric' });
      } else if (this.currentView === 'week') {
        const start = this.weekDays[0].date;
        const end = this.weekDays[6].date;

        // Format like "Mar 1 - Mar 7, 2023"
        const startStr = start.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
        const endStr = end.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });

        return `${startStr} - ${endStr}`;
      } else if (this.currentView === 'day') {
        return this.currentDate.toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric', year: 'numeric' });
      }

      return '';
    },

    formatDateISO(date) {
      const d = new Date(date);
      return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
    },

    formatDateForInput(date) {
      return this.formatDateISO(date);
    },

    formatFullDate(date) {
      return new Date(date).toLocaleDateString('en-US', {
        weekday: 'long',
        month: 'long',
        day: 'numeric',
        year: 'numeric'
      });
    },

    formatEventDate(event) {
      if (!event) return '';

      return new Date(event.date).toLocaleDateString('en-US', {
        weekday: 'long',
        month: 'long',
        day: 'numeric',
        year: 'numeric'
      });
    },

    formatEventTime(event) {
      if (!event) return '';
      if (event.all_day) return 'All Day';

      const formatTime = (timeStr) => {
        const [hours, minutes] = timeStr.split(':');
        const hour = parseInt(hours, 10);
        const period = hour >= 12 ? 'PM' : 'AM';
        const hour12 = hour % 12 || 12;
        return `${hour12}:${minutes} ${period}`;
      };

      if (event.start_time && event.end_time) {
        return `${formatTime(event.start_time)} - ${formatTime(event.end_time)}`;
      }

      return '';
    },

    // Helper functions
    getStartOfWeek(date) {
      const d = new Date(date);
      const day = d.getDay(); // 0 for Sunday, 1 for Monday, etc.
      const diff = d.getDate() - day;

      return new Date(d.setDate(diff));
    },

    getMonthStartDate() {
      return new Date(this.currentDate.getFullYear(), this.currentDate.getMonth(), 1);
    },

    getMonthEndDate() {
      return new Date(this.currentDate.getFullYear(), this.currentDate.getMonth() + 1, 0);
    }
  }
};
</script>

<style scoped>
.dashboard {
  min-height: 100vh;
  background-color: var(--bg-light);
  color: var(--text-primary);
  transition: background-color var(--transition-speed) ease,
  color var(--transition-speed) ease;
  overflow-x: hidden;
}

.dashboard-layout {
  display: flex;
  flex-direction: row;
  position: relative;
  padding-top: 70px; /* Space for fixed navbar */
  min-height: calc(100vh - 70px);
}

/* Animation classes */
.animate-in {
  animation: fadeSlide 0.8s ease-out;
}

.animate-fade-in {
  animation: fadeIn 0.4s ease-out;
}

.animate-slide-down {
  animation: slideDown 0.4s ease-out;
}

.animate-pop-in {
  animation: popIn 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.pulse-animation {
  animation: pulse 2s infinite;
}

.bounce-on-hover:hover {
  animation: bounce 0.5s ease;
}

/* Animation keyframes */
@keyframes fadeSlide {
  0% {
    opacity: 0;
    transform: translateY(10px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeIn {
  0% { opacity: 0; }
  100% { opacity: 1; }
}

@keyframes slideDown {
  0% {
    opacity: 0;
    transform: translateY(-20px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes popIn {
  0% {
    opacity: 0;
    transform: scale(0.9);
  }
  70% {
    transform: scale(1.05);
  }
  100% {
    opacity: 1;
    transform: scale(1);
  }
}

@keyframes pulse {
  0% {
    transform: scale(1);
    opacity: 1;
  }
  50% {
    transform: scale(1.05);
    opacity: 0.8;
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
}

@keyframes bounce {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-5px);
  }
}

/* View transitions */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.slide-left-enter-active,
.slide-left-leave-active,
.slide-right-enter-active,
.slide-right-leave-active {
  transition: transform 0.3s ease, opacity 0.3s ease;
  position: absolute;
  width: 100%;
}

.slide-left-enter-from {
  opacity: 0;
  transform: translateX(50px);
}

.slide-left-leave-to {
  opacity: 0;
  transform: translateX(-50px);
}

.slide-right-enter-from {
  opacity: 0;
  transform: translateX(-50px);
}

.slide-right-leave-to {
  opacity: 0;
  transform: translateX(50px);
}

.zoom-in-enter-active,
.zoom-in-leave-active,
.zoom-out-enter-active,
.zoom-out-leave-active {
  transition: all 0.3s ease;
  position: absolute;
  width: 100%;
}

.zoom-in-enter-from {
  opacity: 0;
  transform: scale(0.95);
}

.zoom-in-leave-to {
  opacity: 0;
  transform: scale(1.05);
}

.zoom-out-enter-from {
  opacity: 0;
  transform: scale(1.05);
}

.zoom-out-leave-to {
  opacity: 0;
  transform: scale(0.95);
}

/* Modal transitions */
.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.3s ease;
}

.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}

.modal-fade-enter-active .modal-container {
  animation: modalEnter 0.3s ease forwards;
}

.modal-fade-leave-active .modal-container {
  animation: modalLeave 0.3s ease forwards;
}

@keyframes modalEnter {
  0% {
    opacity: 0;
    transform: scale(0.9) translateY(30px);
  }
  100% {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

@keyframes modalLeave {
  0% {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
  100% {
    opacity: 0;
    transform: scale(0.9) translateY(30px);
  }
}

/* Main content styles */
.dashboard-main-content {
  flex: 1;
  padding: 2rem;
  transition: all var(--transition-speed) ease;
}

.dashboard-main-content.expanded {
  margin-right: 0;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.dashboard-header h1 {
  font-size: 1.75rem;
  font-weight: 600;
  color: var(--primary-dark);
  margin: 0;
}

body.dark-mode .dashboard-header h1 {
  color: var(--primary-light);
}

/* Calendar actions */
.calendar-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.view-selector {
  display: flex;
  border-radius: var(--border-radius);
  overflow: hidden;
  border: 1px solid var(--border-color);
}

.view-btn {
  background-color: var(--bg-card);
  color: var(--text-secondary);
  border: none;
  padding: 0.5rem 1rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.view-btn.active {
  background-color: var(--primary-color);
  color: white;
}

.add-event-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background-color: var(--primary-color);
  color: white;
  border: none;
  border-radius: var(--border-radius);
  padding: 0.5rem 1rem;
  cursor: pointer;
  transition: all 0.2s ease;
  font-weight: 500;
}

.add-event-button:hover {
  background-color: var(--primary-dark);
  transform: translateY(-2px);
}

/* Sidebar toggle buttons */
.sidebar-toggle {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  background-color: var(--primary-color);
  color: white;
  border: none;
  border-radius: 20px;
  padding: 0.6rem 1.2rem;
  cursor: pointer;
  font-weight: 500;
  box-shadow: var(--shadow-sm);
  transition: all 0.2s ease;
  z-index: 10;
}

.toggle-text {
  font-size: 14px;
  font-weight: 500;
}

.sidebar-toggle:hover {
  background-color: var(--primary-dark);
  transform: scale(1.05);
}

.sidebar-show-button {
  position: fixed;
  right: 2rem;
  top: 6rem;
  box-shadow: 0 2px 10px rgba(123, 73, 255, 0.3);
}

.sidebar-hide-button {
  position: absolute;
  top: 1rem;
  right: 1rem;
  z-index: 20;
}

/* Sidebar styles */
.dashboard-sidebar {
  width: 320px;
  background-color: var(--bg-card);
  border-left: 1px solid var(--border-color);
  box-shadow: var(--shadow-sm);
  transition: all var(--transition-speed) ease;
  position: relative;
  overflow: hidden;
  z-index: 100;
}

/* Slide transition for sidebar */
.slide-enter-active,
.slide-leave-active {
  transition: transform var(--transition-speed) ease,
  opacity var(--transition-speed) ease;
}

.slide-enter-from,
.slide-leave-to {
  transform: translateX(100%);
  opacity: 0;
}

/* Loading and auth states */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 50vh;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid rgba(0, 0, 0, 0.1);
  border-radius: 50%;
  border-top-color: var(--primary-color);
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.auth-prompt {
  padding: 2rem;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.auth-card {
  background-color: var(--bg-card);
  border-radius: var(--border-radius-lg);
  padding: 3rem 2rem;
  box-shadow: var(--shadow-md);
  text-align: center;
  max-width: 400px;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.5rem;
}

.auth-card svg {
  color: var(--primary-color);
}

.auth-card h2 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--primary-dark);
}

.auth-card p {
  margin: 0;
  color: var(--text-secondary);
}

.login-button {
  display: inline-block;
  background: var(--primary-color);
  color: white;
  padding: 0.75rem 1.5rem;
  border-radius: 24px;
  text-decoration: none;
  font-weight: 500;
  box-shadow: var(--shadow-sm);
  transition: all 0.2s ease;
}

.login-button:hover {
  background: var(--primary-dark);
  transform: translateY(-2px);
}

/* Calendar content */
.calendar-content {
  background-color: var(--bg-card);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow-md);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  position: relative; /* For view transitions */
}

.calendar-header {
  padding: 1.5rem;
  border-bottom: 1px solid var(--border-color);
}

.month-navigator {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.nav-btn, .today-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--bg-input);
  color: var(--text-primary);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  cursor: pointer;
  transition: all 0.2s ease;
}

.nav-btn {
  width: 40px;
  height: 40px;
}

.today-btn {
  padding: 0 1rem;
  height: 40px;
  font-weight: 500;
}

.nav-btn:hover, .today-btn:hover {
  background-color: var(--bg-hover);
  border-color: var(--primary-color);
}

.current-period {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--primary-dark);
  margin-left: 0.5rem;
}

/* Month View */
.month-view {
  display: flex;
  flex-direction: column;
  flex: 1;
}

.month-grid-header {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  border-bottom: 1px solid var(--border-color);
}

.day-header {
  padding: 1rem;
  text-align: center;
  font-weight: 500;
  color: var(--text-secondary);
}

.month-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  grid-template-rows: repeat(6, 1fr);
  flex: 1;
  min-height: 600px;
}

.day-cell {
  border-right: 1px solid var(--border-color);
  border-bottom: 1px solid var(--border-color);
  padding: 0.5rem;
  position: relative;
  min-height: 100px;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.day-cell:nth-child(7n) {
  border-right: none;
}

.day-cell:nth-last-child(-n+7) {
  border-bottom: none;
}

.day-cell:hover {
  background-color: var(--bg-hover);
}

.day-cell.today {
  background-color: rgba(123, 73, 255, 0.05);
}

.day-cell.selected {
  background-color: rgba(123, 73, 255, 0.1);
}

.day-cell.different-month {
  opacity: 0.5;
}

.day-number {
  font-weight: 500;
  margin-bottom: 0.5rem;
}

.today .day-number {
  display: inline-block;
  background-color: var(--primary-color);
  color: white;
  width: 25px;
  height: 25px;
  border-radius: 50%;
  text-align: center;
  line-height: 25px;
}

.day-events {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  overflow: hidden;
}

.day-event-pill {
  font-size: 0.75rem;
  padding: 0.125rem 0.375rem;
  border-radius: var(--border-radius);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  background-color: #e0e0e0;
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.day-event-pill:hover {
  transform: translateY(-1px);
  box-shadow: var(--shadow-sm);
}

.more-events {
  font-size: 0.75rem;
  color: var(--text-secondary);
  margin-top: 0.25rem;
  text-align: center;
}

/* Week View */
.week-view {
  display: flex;
  flex-direction: column;
  height: 800px;
}

.week-grid-header {
  display: flex;
  border-bottom: 1px solid var(--border-color);
}

.time-column-header {
  width: 60px;
  flex-shrink: 0;
}

.day-column-header {
  flex: 1;
  padding: 0.75rem;
  text-align: center;
  border-left: 1px solid var(--border-color);
}

.day-name {
  font-weight: 500;
  color: var(--text-secondary);
}

.day-number {
  font-weight: 600;
  font-size: 1.25rem;
}

.today .day-name, .today .day-number {
  color: var(--primary-color);
}

.week-grid {
  display: flex;
  flex: 1;
  overflow-y: auto;
  position: relative;
}

.time-column {
  width: 60px;
  flex-shrink: 0;
  border-right: 1px solid var(--border-color);
}

.time-cell {
  height: 60px;
  padding: 0.25rem;
  text-align: center;
  color: var(--text-secondary);
  font-size: 0.75rem;
  border-bottom: 1px solid var(--border-color-light);
  position: relative;
}

.day-columns {
  display: flex;
  flex: 1;
}

.day-column {
  flex: 1;
  position: relative;
  border-right: 1px solid var(--border-color-light);
}

.day-column:last-child {
  border-right: none;
}

.day-column .time-cell {
  border-left: none;
  cursor: pointer;
}

.day-column .time-cell:hover {
  background-color: var(--bg-hover);
}

.week-event {
  position: absolute;
  width: calc(100% - 8px);
  margin-left: 4px;
  border-radius: var(--border-radius);
  padding: 0.25rem;
  overflow: hidden;
  cursor: pointer;
  font-size: 0.75rem;
  z-index: 5;
  box-shadow: var(--shadow-sm);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.week-event:hover {
  transform: translateY(-2px) scale(1.01);
  box-shadow: var(--shadow-md);
  z-index: 10;
}

.week-event .event-time {
  font-weight: 500;
  margin-bottom: 0.25rem;
}

.week-event .event-title {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* Day View */
.day-view {
  display: flex;
  flex-direction: column;
  height: 800px;
}

.day-view-header {
  padding: 1rem;
  text-align: center;
  border-bottom: 1px solid var(--border-color);
}

.current-day {
  font-weight: 600;
  font-size: 1.25rem;
  color: var(--primary-dark);
}

.day-view-grid {
  display: flex;
  flex: 1;
  overflow-y: auto;
}

.events-column {
  flex: 1;
  position: relative;
}

.day-event {
  position: absolute;
  width: calc(100% - 8px);
  margin-left: 4px;
  border-radius: var(--border-radius);
  padding: 0.5rem;
  overflow: hidden;
  cursor: pointer;
  font-size: 0.875rem;
  z-index: 5;
  box-shadow: var(--shadow-sm);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.day-event:hover {
  transform: translateY(-2px) scale(1.01);
  box-shadow: var(--shadow-md);
  z-index: 10;
}

.day-event .event-time {
  font-weight: 500;
  margin-bottom: 0.25rem;
}

.day-event .event-title {
  font-weight: 600;
  margin-bottom: 0.25rem;
}

.day-event .event-description {
  font-size: 0.75rem;
  opacity: 0.8;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* Event Colors */
.general-event {
  background-color: #2196F3;
  color: white;
}

.assignment-event {
  background-color: #F44336;
  color: white;
}

.exam-event {
  background-color: #E91E63;
  color: white;
}

.study-event {
  background-color: #4CAF50;
  color: white;
}

.meeting-event {
  background-color: #673AB7;
  color: white;
}

.celebration-event {
  background-color: #FF9800;
  color: white;
}

.completed-event {
  opacity: 0.7;
  text-decoration: line-through;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-container {
  background-color: var(--bg-card);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow-lg);
  width: 90%;
  max-width: 600px;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
}

.delete-confirm-modal {
  max-width: 400px;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid var(--border-color);
}

.modal-header h2 {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 600;
}

.close-modal-btn {
  background: transparent;
  border: none;
  color: var(--text-secondary);
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.close-modal-btn:hover {
  background-color: rgba(0, 0, 0, 0.05);
  color: var(--text-primary);
}

.modal-body {
  padding: 1.5rem;
  overflow-y: auto;
}

.modal-footer {
  padding: 1.5rem;
  border-top: 1px solid var(--border-color);
}

.modal-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* Form Styles */
.form-group {
  margin-bottom: 1.5rem;
}

.form-row {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.form-group input, .form-group select, .form-group textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  background-color: var(--bg-input);
  color: var(--text-primary);
  font-family: inherit;
  font-size: 1rem;
  transition: border-color 0.3s ease;
}

.form-group input:focus, .form-group select:focus, .form-group textarea:focus {
  border-color: var(--primary-color);
  outline: none;
  box-shadow: 0 0 0 3px rgba(123, 73, 255, 0.1);
}

.checkbox-group {
  display: flex;
  align-items: center;
}

.checkbox-container {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  user-select: none;
}

.checkbox-container input {
  width: auto;
  margin-right: 0.5rem;
}

/* Buttons */
.cancel-button, .save-button, .delete-button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border-radius: var(--border-radius);
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.cancel-button {
  background-color: transparent;
  color: var(--text-secondary);
  border: 1px solid var(--border-color);
}

.cancel-button:hover {
  background-color: rgba(0, 0, 0, 0.05);
}

.save-button {
  background-color: var(--primary-color);
  color: white;
  border: none;
}

.save-button:hover {
  background-color: var(--primary-dark);
  transform: translateY(-2px);
}

.save-button:disabled {
  background-color: var(--border-color);
  cursor: not-allowed;
  transform: none;
}

.delete-button {
  background-color: transparent;
  color: var(--error-color);
  border: 1px solid var(--error-color);
}

.delete-button:hover {
  background-color: rgba(244, 67, 54, 0.05);
}

.delete-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Event Details */
.event-details-header {
  padding: 1.5rem;
  border-radius: var(--border-radius) var(--border-radius) 0 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.event-details-header h3 {
  margin: 0;
  color: white;
  font-size: 1.25rem;
  font-weight: 600;
}

.event-badge {
  background-color: rgba(255, 255, 255, 0.2);
  color: white;
  font-size: 0.75rem;
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
}

.event-details-content {
  padding: 1.5rem;
}

.event-details-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.event-details-item svg {
  color: var(--primary-color);
}

.event-details-description {
  margin-top: 1.5rem;
}

.event-details-description h4 {
  font-size: 1rem;
  margin: 0 0 0.5rem;
}

.event-details-description p {
  margin: 0;
  white-space: pre-line;
}

.event-status {
  margin-top: 1.5rem;
}

.status-badge {
  display: inline-block;
  background-color: var(--success-color);
  color: white;
  font-size: 0.75rem;
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
}

/* Delete confirmation */
.event-name {
  font-weight: 600;
  text-align: center;
  margin: 1rem 0;
  font-size: 1.1rem;
}

.delete-warning {
  color: var(--error-color);
  font-size: 0.875rem;
  text-align: center;
  margin-top: 1rem;
}

/* Search and Filter Styles */
.search-filter-container {
  display: flex;
  margin-bottom: 1rem;
  gap: 1rem;
  align-items: center;
}

.search-box {
  flex: 1;
  display: flex;
  align-items: center;
  background-color: var(--bg-input);
  border-radius: var(--border-radius);
  padding: 0 1rem;
  border: 1px solid var(--border-color);
  transition: all 0.2s ease;
}

.search-box:focus-within {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 2px rgba(123, 73, 255, 0.1);
}

.search-box svg {
  color: var(--text-secondary);
  margin-right: 0.5rem;
}

.search-box input {
  flex: 1;
  padding: 0.75rem 0;
  border: none;
  background: transparent;
  color: var(--text-primary);
  font-size: 1rem;
  outline: none;
  width: 100%;
}

.clear-search {
  background: transparent;
  border: none;
  color: var(--text-secondary);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.clear-search:hover {
  color: var(--text-primary);
}

.filter-box {
  display: flex;
  align-items: center;
}

.filter-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background-color: var(--bg-input);
  color: var(--text-primary);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  padding: 0.75rem 1rem;
  cursor: pointer;
  transition: all 0.2s ease;
  font-weight: 500;
  position: relative;
}

.filter-button.active {
  background-color: var(--bg-hover);
  border-color: var(--primary-color);
  color: var(--primary-color);
}

.filter-button svg {
  transition: transform 0.2s ease;
}

.filter-button.active svg {
  transform: rotate(180deg);
  color: var(--primary-color);
}

.filter-count {
  position: absolute;
  top: -8px;
  right: -8px;
  background-color: var(--primary-color);
  color: white;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  font-weight: bold;
}

.filter-panel {
  background-color: var(--bg-card);
  border-radius: var(--border-radius);
  padding: 1.5rem;
  margin-bottom: 1.5rem;
  border: 1px solid var(--border-color);
  box-shadow: var(--shadow-md);
  animation: fadeIn 0.3s ease;
}

.filter-section {
  margin-bottom: 1.5rem;
}

.filter-section h3 {
  font-size: 1rem;
  margin: 0 0 0.75rem;
  color: var(--text-secondary);
}

.filter-options {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}

.filter-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1.5rem;
}

.reset-filter-button {
  background-color: transparent;
  color: var(--text-secondary);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  padding: 0.5rem 1rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.reset-filter-button:hover {
  background-color: var(--bg-hover);
}

.apply-filter-button {
  background-color: var(--primary-color);
  color: white;
  border: none;
  border-radius: var(--border-radius);
  padding: 0.5rem 1rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.apply-filter-button:hover {
  background-color: var(--primary-dark);
}

.no-results {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  text-align: center;
  color: var(--text-secondary);
}

.no-results svg {
  color: var(--text-secondary);
  margin-bottom: 1rem;
}

.no-results h3 {
  font-size: 1.25rem;
  margin: 0.5rem 0;
  color: var(--text-primary);
}

.no-results p {
  margin: 0.25rem 0 1.5rem;
}

.reset-search-button {
  background-color: var(--primary-color);
  color: white;
  border: none;
  border-radius: var(--border-radius);
  padding: 0.5rem 1.5rem;
  cursor: pointer;
  transition: all 0.2s ease;
  font-weight: 500;
}

.reset-search-button:hover {
  background-color: var(--primary-dark);
  transform: translateY(-2px);
}

/* Responsive styles */
@media (max-width: 768px) {
  .dashboard-main-content {
    padding: 1rem;
  }

  .dashboard-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .calendar-actions {
    width: 100%;
    justify-content: space-between;
  }

  .view-btn {
    padding: 0.5rem 0.75rem;
    font-size: 0.875rem;
  }

  .add-event-button {
    padding: 0.5rem 0.75rem;
    font-size: 0.875rem;
  }

  .add-event-button span {
    display: none;
  }

  .add-event-button svg {
    margin-right: 0;
  }

  .search-filter-container {
    flex-direction: column;
    align-items: stretch;
  }

  .filter-options {
    flex-direction: column;
    gap: 0.75rem;
  }

  .filter-actions {
    flex-direction: column;
  }

  .filter-actions button {
    width: 100%;
  }

  .month-grid {
    min-height: 400px;
  }

  .day-cell {
    min-height: 80px;
    padding: 0.25rem;
  }

  .form-row {
    flex-direction: column;
    gap: 1rem;
  }

  .modal-actions {
    flex-direction: column-reverse;
    gap: 1rem;
  }

  .modal-actions > div {
    display: flex;
    gap: 1rem;
    width: 100%;
  }

  .modal-actions button {
    flex: 1;
  }

  .sidebar-show-button {
    right: 1rem;
    top: 5rem;
  }

  .current-period {
    font-size: 1rem;
  }

  .week-view,
  .day-view {
    height: 600px;
  }

  .week-grid-header,
  .day-view-header {
    font-size: 0.875rem;
  }

  .day-column-header {
    padding: 0.5rem 0.25rem;
  }

  .day-name {
    font-size: 0.75rem;
  }

  .day-number {
    font-size: 1rem;
  }
}

@media (max-width: 480px) {
  .dashboard-header h1 {
    font-size: 1.5rem;
  }

  .day-header {
    padding: 0.5rem 0.25rem;
    font-size: 0.75rem;
  }

  .search-box input {
    font-size: 0.875rem;
    padding: 0.5rem 0;
  }

  .current-period {
    font-size: 0.875rem;
  }

  .filter-panel {
    padding: 1rem;
  }

  .month-grid {
    min-height: 300px;
  }

  .day-cell {
    min-height: 60px;
    padding: 0.25rem;
  }

  .day-event-pill {
    font-size: 0.7rem;
    padding: 0.1rem 0.25rem;
  }

  .more-events {
    font-size: 0.7rem;
  }

  .week-event,
  .day-event {
    font-size: 0.7rem;
    padding: 0.125rem;
  }

  .event-time {
    margin-bottom: 0.125rem !important;
  }

  .modal-header,
  .modal-body,
  .modal-footer {
    padding: 1rem;
  }

  .modal-header h2 {
    font-size: 1.125rem;
  }

  .cancel-button,
  .save-button,
  .delete-button {
    padding: 0.5rem 1rem;
    font-size: 0.875rem;
  }

  .week-view,
  .day-view {
    height: 500px;
  }

  .time-cell {
    height: 50px;
    font-size: 0.7rem;
  }
}

/* Touch-friendly improvements for mobile */
@media (hover: none) and (pointer: coarse) {
  /* Larger touch targets */
  .view-btn,
  .nav-btn,
  .today-btn {
    min-height: 44px;
  }

  .day-cell {
    min-height: 60px;
  }

  .day-event-pill,
  .week-event,
  .day-event {
    padding-top: 0.375rem;
    padding-bottom: 0.375rem;
  }

  /* Better form inputs for touch */
  .form-group input,
  .form-group select {
    height: 44px;
  }

  /* Remove hover effects that don't work well on touch */
  .day-event-pill:hover,
  .week-event:hover,
  .day-event:hover {
    transform: none;
  }

  /* Add active state for touch feedback */
  .day-event-pill:active,
  .week-event:active,
  .day-event:active {
    transform: scale(0.98);
    opacity: 0.9;
  }
}
</style>