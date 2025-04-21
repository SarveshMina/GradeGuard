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
          v-tippy="{ content: 'Show Calendar Sidebar', placement: 'left' }"
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
                  :class="{ active: currentView === 'dayGridMonth' }"
                  @click="setView('dayGridMonth')"
                  v-tippy="{ content: 'Month View', placement: 'bottom' }"
              >
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                  <line x1="16" y1="2" x2="16" y2="6"></line>
                  <line x1="8" y1="2" x2="8" y2="6"></line>
                  <line x1="3" y1="10" x2="21" y2="10"></line>
                </svg>
                <span>Month</span>
              </button>
              <button
                  class="view-btn"
                  :class="{ active: currentView === 'timeGridWeek' }"
                  @click="setView('timeGridWeek')"
                  v-tippy="{ content: 'Week View', placement: 'bottom' }"
              >
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                  <line x1="8" y1="2" x2="8" y2="6"></line>
                  <line x1="16" y1="2" x2="16" y2="6"></line>
                  <line x1="3" y1="10" x2="21" y2="10"></line>
                  <line x1="3" y1="16" x2="7" y2="16"></line>
                  <line x1="11" y1="16" x2="15" y2="16"></line>
                  <line x1="19" y1="16" x2="21" y2="16"></line>
                </svg>
                <span>Week</span>
              </button>
              <button
                  class="view-btn"
                  :class="{ active: currentView === 'timeGridDay' }"
                  @click="setView('timeGridDay')"
                  v-tippy="{ content: 'Day View', placement: 'bottom' }"
              >
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                  <line x1="16" y1="2" x2="16" y2="6"></line>
                  <line x1="8" y1="2" x2="8" y2="6"></line>
                  <line x1="3" y1="10" x2="21" y2="10"></line>
                  <line x1="12" y1="12" x2="12" y2="16"></line>
                </svg>
                <span>Day</span>
              </button>
            </div>
            <button
                class="add-event-button bounce-on-hover"
                @click="openCreateEventModal"
                v-tippy="{ content: 'Add New Event', placement: 'left' }"
            >
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
              <button
                  @click="toggleFilterPanel"
                  class="filter-button"
                  :class="{'active': showFilterPanel}"
                  v-tippy="{ content: 'Filter Events', placement: 'left' }"
              >
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
            <div class="filter-section">
              <h3>Reminders</h3>
              <div class="filter-options">
                <label class="checkbox-container">
                  <input
                      type="checkbox"
                      v-model="filters.showWithReminders"
                      @change="applyFilters"
                  />
                  <span class="checkmark"></span>
                  Show Events With Reminders
                </label>
              </div>
            </div>
            <div class="filter-section">
              <h3>Date Range</h3>
              <div class="date-range-picker">
                <div class="date-input-group">
                  <label>From</label>
                  <div class="custom-date-input">
                    <input
                        type="date"
                        v-model="filters.dateFrom"
                        @change="applyFilters"
                    />
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                      <line x1="16" y1="2" x2="16" y2="6"></line>
                      <line x1="8" y1="2" x2="8" y2="6"></line>
                      <line x1="3" y1="10" x2="21" y2="10"></line>
                    </svg>
                  </div>
                </div>
                <div class="date-input-group">
                  <label>To</label>
                  <div class="custom-date-input">
                    <input
                        type="date"
                        v-model="filters.dateTo"
                        @change="applyFilters"
                    />
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                      <line x1="16" y1="2" x2="16" y2="6"></line>
                      <line x1="8" y1="2" x2="8" y2="6"></line>
                      <line x1="3" y1="10" x2="21" y2="10"></line>
                    </svg>
                  </div>
                </div>
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

          <!-- FullCalendar Component -->
          <div class="fullcalendar-container animate-fade-in">
            <FullCalendar
                ref="fullCalendar"
                :options="calendarOptions"
                @dateClick="handleDateClick"
                @eventClick="handleEventClick"
                @eventDrop="handleEventDrop"
                @eventResize="handleEventResize"
            />
          </div>
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
              v-tippy="{ content: 'Hide Sidebar', placement: 'left' }"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M9 18l6-6-6-6" />
            </svg>
            <span class="toggle-text">Hide</span>
          </button>
          <CalendarSidebar
              :events="filteredEvents"
              :selected-date="selectedDate"
              :reminders="reminders"
              @day-click="selectDate"
              @add-event="openCreateEventModal"
              @edit-event="editEvent"
              @delete-event="confirmDeleteEvent"
              @toggle-completion="toggleEventCompletion"
              @view-reminders="openRemindersModal"
          />
        </aside>
      </transition>
    </div>

    <!-- Create/Edit Event Modal -->
    <transition name="modal-fade">
      <div v-if="showEventModal" class="modal-overlay" @click.self="closeEventModal">
        <div class="modal-container improved-modal">
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
                    v-model="eventForm.dateFormatted"
                    class="native-date-input"
                    required
                />
              </div>
              <div class="form-group">
                <label for="eventType">Event Type</label>
                <select id="eventType" v-model="eventForm.type" class="native-select">
                  <option v-for="type in eventTypes" :key="type.value" :value="type.value">
                    {{ type.label }}
                  </option>
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
                    class="native-time-input"
                />
              </div>
              <div class="form-group">
                <label for="endTime">End Time</label>
                <input
                    type="time"
                    id="endTime"
                    v-model="eventForm.end_time"
                    class="native-time-input"
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

            <div class="form-group">
              <label for="eventLocation">Location</label>
              <input
                  type="text"
                  id="eventLocation"
                  v-model="eventForm.location"
                  placeholder="Event location (optional)"
              />
            </div>

            <div class="form-group checkbox-group" v-if="isEditMode">
              <label class="checkbox-container">
                <input type="checkbox" v-model="eventForm.completed" />
                <span class="checkmark"></span>
                Mark as Completed
              </label>
            </div>

            <!-- Event Reminder Section -->
            <div class="form-group" v-if="isEditMode">
              <div class="reminder-section-header">
                <label>Event Reminders</label>
                <button type="button" @click="openAddReminderForm" class="add-reminder-button">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <line x1="12" y1="5" x2="12" y2="19"></line>
                    <line x1="5" y1="12" x2="19" y2="12"></line>
                  </svg>
                  Add Reminder
                </button>
              </div>

              <div class="add-reminder-form" v-if="showAddReminderForm">
                <div class="form-row">
                  <div class="form-group">
                    <label for="reminderDays">Remind me</label>
                    <select id="reminderDays" v-model="reminderForm.days_before" class="native-select">
                      <option value="0">On the day</option>
                      <option value="1">1 day before</option>
                      <option value="2">2 days before</option>
                      <option value="3">3 days before</option>
                      <option value="7">1 week before</option>
                      <option value="14">2 weeks before</option>
                    </select>
                  </div>
                  <div class="form-group reminder-actions">
                    <button type="button" @click="cancelAddReminder" class="cancel-reminder-button">
                      Cancel
                    </button>
                    <button type="button" @click="saveReminder" class="save-reminder-button">
                      Save Reminder
                    </button>
                  </div>
                </div>
              </div>

              <div class="event-reminders-list" v-if="getEventReminders(eventForm.id).length > 0">
                <div v-for="reminder in getEventReminders(eventForm.id)" :key="reminder.id" class="reminder-item">
                  <div class="reminder-info">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path>
                      <path d="M13.73 21a2 2 0 0 1-3.46 0"></path>
                    </svg>
                    <span>{{ formatReminderTime(reminder) }}</span>
                  </div>
                  <button type="button" @click="deleteReminder(reminder.id)" class="delete-reminder-button">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <line x1="18" y1="6" x2="6" y2="18"></line>
                      <line x1="6" y1="6" x2="18" y2="18"></line>
                    </svg>
                  </button>
                </div>
              </div>
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
              <div class="action-buttons">
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
        <div class="modal-container improved-modal">
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

                <div class="event-details-item" v-if="selectedEvent?.location">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path>
                    <circle cx="12" cy="10" r="3"></circle>
                  </svg>
                  <span>{{ selectedEvent?.location }}</span>
                </div>

                <div class="event-details-description" v-if="selectedEvent?.description">
                  <h4>Description</h4>
                  <p>{{ selectedEvent?.description }}</p>
                </div>

                <div class="event-status" v-if="selectedEvent?.completed">
                  <span class="status-badge">Completed</span>
                </div>

                <!-- Event Reminders Section -->
                <div class="event-reminders" v-if="selectedEvent && getEventReminders(selectedEvent.id).length > 0">
                  <h4>Reminders</h4>
                  <div class="reminder-list">
                    <div v-for="reminder in getEventReminders(selectedEvent.id)" :key="reminder.id" class="reminder-item">
                      <div class="reminder-info">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                          <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path>
                          <path d="M13.73 21a2 2 0 0 1-3.46 0"></path>
                        </svg>
                        <span>{{ formatReminderTime(reminder) }}</span>
                      </div>
                      <button type="button" @click="deleteReminder(reminder.id)" class="delete-reminder-button">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                          <line x1="18" y1="6" x2="6" y2="18"></line>
                          <line x1="6" y1="6" x2="18" y2="18"></line>
                        </svg>
                      </button>
                    </div>
                  </div>
                </div>

                <!-- Add Quick Reminder Button -->
                <div class="quick-add-reminder" v-if="selectedEvent">
                  <button @click="quickAddReminder" class="quick-reminder-button">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path>
                      <path d="M13.73 21a2 2 0 0 1-3.46 0"></path>
                    </svg>
                    Add Reminder
                  </button>
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
              <div class="action-buttons">
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
        <div class="modal-container delete-confirm-modal improved-modal animate-pop-in">
          <div class="modal-header">
            <h2>Confirm Delete</h2>
          </div>
          <div class="modal-body">
            <div class="delete-confirm-content">
              <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="warning-icon">
                <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path>
                <line x1="12" y1="9" x2="12" y2="13"></line>
                <line x1="12" y1="17" x2="12.01" y2="17"></line>
              </svg>
              <p>Are you sure you want to delete this event?</p>
              <p class="event-name">{{ selectedEvent?.title }}</p>
              <p class="delete-warning">This action cannot be undone.</p>
            </div>
          </div>
          <div class="modal-footer">
            <div class="delete-actions">
              <button @click="showDeleteConfirmModal = false" class="cancel-button">
                Cancel
              </button>
              <button @click="deleteEvent" class="delete-button confirm-delete-button" :disabled="isDeleting">
                <span v-if="isDeleting">Deleting...</span>
                <span v-else>Delete</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </transition>

    <!-- Reminders Modal -->
    <transition name="modal-fade">
      <div v-if="showRemindersModal" class="modal-overlay" @click.self="closeRemindersModal">
        <div class="modal-container improved-modal">
          <div class="modal-header">
            <h2>Your Reminders</h2>
            <button @click="closeRemindersModal" class="close-modal-btn">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <line x1="18" y1="6" x2="6" y2="18"></line>
                <line x1="6" y1="6" x2="18" y2="18"></line>
              </svg>
            </button>
          </div>
          <div class="modal-body">
            <div class="reminders-list animate-fade-in">
              <!-- Upcoming Reminders -->
              <div class="reminders-section">
                <h3>Upcoming Reminders</h3>
                <div v-if="upcomingReminders.length === 0" class="no-reminders">
                  <p>You don't have any upcoming reminders.</p>
                </div>
                <div v-else class="reminder-items">
                  <div v-for="reminder in upcomingReminders" :key="reminder.id" class="reminder-list-item">
                    <div class="reminder-details">
                      <div class="reminder-event-title">{{ getEventTitleById(reminder.event_id) }}</div>
                      <div class="reminder-date">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                          <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                          <line x1="16" y1="2" x2="16" y2="6"></line>
                          <line x1="8" y1="2" x2="8" y2="6"></line>
                          <line x1="3" y1="10" x2="21" y2="10"></line>
                        </svg>
                        <span>{{ formatEventDate(getEventById(reminder.event_id)) }}</span>
                      </div>
                      <div class="reminder-time">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                          <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path>
                          <path d="M13.73 21a2 2 0 0 1-3.46 0"></path>
                        </svg>
                        <span>{{ formatReminderTime(reminder) }}</span>
                      </div>
                      <div v-if="reminder.sent" class="reminder-status sent">
                        <span>Sent</span>
                      </div>
                      <div v-else class="reminder-status pending">
                        <span>Pending</span>
                      </div>
                    </div>
                    <div class="reminder-actions">
                      <button @click="editEventFromReminder(reminder.event_id)" class="edit-event-button">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                          <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                          <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
                        </svg>
                      </button>
                      <button @click="deleteReminder(reminder.id)" class="delete-reminder-button">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                          <polyline points="3 6 5 6 21 6"></polyline>
                          <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                        </svg>
                      </button>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Sent Reminders -->
              <div class="reminders-section">
                <h3>Sent Reminders</h3>
                <div v-if="sentReminders.length === 0" class="no-reminders">
                  <p>You don't have any sent reminders.</p>
                </div>
                <div v-else class="reminder-items">
                  <div v-for="reminder in sentReminders" :key="reminder.id" class="reminder-list-item sent">
                    <div class="reminder-details">
                      <div class="reminder-event-title">{{ getEventTitleById(reminder.event_id) }}</div>
                      <div class="reminder-date">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                          <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                          <line x1="16" y1="2" x2="16" y2="6"></line>
                          <line x1="8" y1="2" x2="8" y2="6"></line>
                          <line x1="3" y1="10" x2="21" y2="10"></line>
                        </svg>
                        <span>{{ formatEventDate(getEventById(reminder.event_id)) }}</span>
                      </div>
                      <div class="reminder-time">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                          <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path>
                          <path d="M13.73 21a2 2 0 0 1-3.46 0"></path>
                        </svg>
                        <span>Sent on {{ formatSentReminderDate(reminder) }}</span>
                      </div>
                    </div>
                    <div class="reminder-actions">
                      <button @click="deleteReminder(reminder.id)" class="delete-reminder-button">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                          <polyline points="3 6 5 6 21 6"></polyline>
                          <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                        </svg>
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button @click="closeRemindersModal" class="close-button">
              Close
            </button>
          </div>
        </div>
      </div>
    </transition>

    <!-- Quick Add Reminder Modal -->
    <transition name="modal-fade">
      <div v-if="showQuickAddReminderModal" class="modal-overlay" @click.self="closeQuickAddReminderModal">
        <div class="modal-container quick-reminder-modal improved-modal animate-pop-in">
          <div class="modal-header">
            <h2>Add Reminder</h2>
            <button @click="closeQuickAddReminderModal" class="close-modal-btn">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <line x1="18" y1="6" x2="6" y2="18"></line>
                <line x1="6" y1="6" x2="18" y2="18"></line>
              </svg>
            </button>
          </div>
          <div class="modal-body">
            <div class="quick-reminder-content">
              <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path>
                <path d="M13.73 21a2 2 0 0 1-3.46 0"></path>
              </svg>
              <p class="reminder-event-name">{{ selectedEvent?.title }}</p>
              <div class="form-group">
                <label for="quickReminderDays">Remind me:</label>
                <div class="custom-select" :class="{ 'open': showQuickReminderDropdown }">
                  <div class="select-selected" @click="toggleQuickReminderDropdown">
                    <span>{{ formatReminderOption(reminderForm.days_before) }}</span>
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <polyline points="6 9 12 15 18 9"></polyline>
                    </svg>
                  </div>
                  <div v-if="showQuickReminderDropdown" class="select-items">
                    <div
                        v-for="option in [
                          {value: '0', label: 'On the day'},
                          {value: '1', label: '1 day before'},
                          {value: '2', label: '2 days before'},
                          {value: '3', label: '3 days before'},
                          {value: '7', label: '1 week before'},
                          {value: '14', label: '2 weeks before'}
                        ]"
                        :key="option.value"
                        class="select-item"
                        :class="{ 'selected': reminderForm.days_before.toString() === option.value }"
                        @click="selectQuickReminderOption(option.value)"
                    >
                      {{ option.label }}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <div class="reminder-modal-actions">
              <button @click="closeQuickAddReminderModal" class="cancel-button">
                Cancel
              </button>
              <button @click="saveQuickReminder" class="save-button" :disabled="isCreatingReminder">
                <span v-if="isCreatingReminder">Creating...</span>
                <span v-else>Add Reminder</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </transition>

    <!-- Keyboard Shortcuts Modal -->
    <transition name="modal-fade">
      <div v-if="showShortcutsModal" class="modal-overlay" @click.self="closeShortcutsModal">
        <div class="modal-container shortcuts-modal improved-modal">
          <div class="modal-header">
            <h2>Keyboard Shortcuts</h2>
            <button @click="closeShortcutsModal" class="close-modal-btn">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <line x1="18" y1="6" x2="6" y2="18"></line>
                <line x1="6" y1="6" x2="18" y2="18"></line>
              </svg>
            </button>
          </div>
          <div class="modal-body">
            <div class="shortcuts-list">
              <div class="shortcuts-section">
                <h3>Navigation</h3>
                <div class="shortcut-item">
                  <div class="shortcut-keys">
                    <kbd>t</kbd>
                  </div>
                  <div class="shortcut-description">Go to today</div>
                </div>
                <div class="shortcut-item">
                  <div class="shortcut-keys">
                    <kbd>←</kbd>
                  </div>
                  <div class="shortcut-description">Previous day/week/month</div>
                </div>
                <div class="shortcut-item">
                  <div class="shortcut-keys">
                    <kbd>→</kbd>
                  </div>
                  <div class="shortcut-description">Next day/week/month</div>
                </div>
              </div>

              <div class="shortcuts-section">
                <h3>Views</h3>
                <div class="shortcut-item">
                  <div class="shortcut-keys">
                    <kbd>1</kbd> or <kbd>d</kbd>
                  </div>
                  <div class="shortcut-description">Day view</div>
                </div>
                <div class="shortcut-item">
                  <div class="shortcut-keys">
                    <kbd>2</kbd> or <kbd>w</kbd>
                  </div>
                  <div class="shortcut-description">Week view</div>
                </div>
                <div class="shortcut-item">
                  <div class="shortcut-keys">
                    <kbd>3</kbd> or <kbd>m</kbd>
                  </div>
                  <div class="shortcut-description">Month view</div>
                </div>
              </div>

              <div class="shortcuts-section">
                <h3>Events</h3>
                <div class="shortcut-item">
                  <div class="shortcut-keys">
                    <kbd>n</kbd> or <kbd>+</kbd>
                  </div>
                  <div class="shortcut-description">New event</div>
                </div>
                <div class="shortcut-item">
                  <div class="shortcut-keys">
                    <kbd>Esc</kbd>
                  </div>
                  <div class="shortcut-description">Close any modal</div>
                </div>
                <div class="shortcut-item">
                  <div class="shortcut-keys">
                    <kbd>/</kbd>
                  </div>
                  <div class="shortcut-description">Focus search box</div>
                </div>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button @click="closeShortcutsModal" class="close-button">
              Close
            </button>
          </div>
        </div>
      </div>
    </transition>

    <!-- Show confetti animation when marking event as completed -->
    <confetti-explosion
        v-if="showConfetti"
        :particleCount="200"
        :force="0.3"
        :duration="3000"
        :colors="['#9e78ff', '#7b49ff', '#b59dff', '#f8f9fa', '#adb5bd']"
    />

    <!-- Floating action buttons -->
    <div class="floating-action-buttons">
      <button
          @click="showColorPicker = !showColorPicker"
          class="floating-action-button theme-button"
          v-tippy="{ content: 'Theme Settings', placement: 'left' }"
      >
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="12" cy="12" r="10"></circle>
          <circle cx="12" cy="12" r="4"></circle>
        </svg>
      </button>
      <button
          @click="showShortcutsModal = true"
          class="floating-action-button shortcuts-button"
          v-tippy="{ content: 'Keyboard Shortcuts', placement: 'left' }"
      >
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M18 3a3 3 0 0 0-3 3v12a3 3 0 0 0 3 3 3 3 0 0 0 3-3 3 3 0 0 0-3-3H6a3 3 0 0 0-3 3 3 3 0 0 0 3 3 3 3 0 0 0 3-3V6a3 3 0 0 0-3-3 3 3 0 0 0-3 3 3 3 0 0 0 3 3h12a3 3 0 0 0 3-3 3 3 0 0 0-3-3z"></path>
        </svg>
      </button>
      <div v-if="showColorPicker" class="color-picker-panel">
        <div class="color-theme-options">
          <button
              class="color-option"
              :class="{ active: primaryColor === '#9e78ff' }"
              @click="setPrimaryColor('#9e78ff')"
              style="background-color: #9e78ff"
          ></button>
          <button
              class="color-option"
              :class="{ active: primaryColor === '#ff6b6b' }"
              @click="setPrimaryColor('#ff6b6b')"
              style="background-color: #ff6b6b"
          ></button>
          <button
              class="color-option"
              :class="{ active: primaryColor === '#4caf50' }"
              @click="setPrimaryColor('#4caf50')"
              style="background-color: #4caf50"
          ></button>
          <button
              class="color-option"
              :class="{ active: primaryColor === '#2196f3' }"
              @click="setPrimaryColor('#2196f3')"
              style="background-color: #2196f3"
          ></button>
          <button
              class="color-option"
              :class="{ active: primaryColor === '#ff9800' }"
              @click="setPrimaryColor('#ff9800')"
              style="background-color: #ff9800"
          ></button>
        </div>
        <div class="theme-toggle">
          <label class="theme-toggle-label">
            <input type="checkbox" v-model="darkMode" @change="toggleDarkMode">
            <span class="slider"></span>
            <span class="toggle-text">Dark Mode</span>
          </label>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { notify } from "@/services/toastService.js";
import DashboardNavBar from "@/components/DashboardNavBar.vue";
import CalendarSidebar from "@/components/CalendarSideBar.vue";
import { getDarkModePreference } from "@/services/darkModeService.js";
import { API_URL } from "@/config.js";
import ConfettiExplosion from 'vue-confetti-explosion';
import VueTippy from 'vue-tippy';

// FullCalendar imports
import FullCalendar from '@fullcalendar/vue3';
import dayGridPlugin from '@fullcalendar/daygrid';
import timeGridPlugin from '@fullcalendar/timegrid';
import interactionPlugin from '@fullcalendar/interaction';
import listPlugin from '@fullcalendar/list';

export default {
  name: "Calendar",
  components: {
    DashboardNavBar,
    CalendarSidebar,
    ConfettiExplosion,
    FullCalendar
  },
  provide() {
    return {
      openSchedulerModal: this.openSchedulerModal
    };
  },
  data() {
    return {
      darkMode: false,
      notLoggedIn: false,
      loading: true,
      sidebarVisible: true,
      isMobile: false,
      animateIn: true,

      // Custom theme
      primaryColor: '#9e78ff',
      showColorPicker: false,

      // Animation and interaction state
      hoveredEvent: null,
      showConfetti: false,
      showShortcutsModal: false,

      // User data
      userProfile: {
        firstName: "",
        email: "",
        avatar: ""
      },

      // Calendar state
      currentView: 'dayGridMonth', // FullCalendar view type: 'dayGridMonth', 'timeGridWeek', 'timeGridDay'
      selectedDate: new Date(),
      events: [],
      filteredEvents: [],

      // FullCalendar options
      calendarOptions: {
        plugins: [dayGridPlugin, timeGridPlugin, interactionPlugin, listPlugin],
        initialView: 'dayGridMonth',
        headerToolbar: false, // We're using our custom header
        height: 'auto',
        editable: true,
        selectable: true,
        selectMirror: true,
        nowIndicator: true,
        dayMaxEvents: true,
        weekNumbers: false,
        events: [], // Will be populated from filteredEvents
        // Theme options for FullCalendar
        themeSystem: 'standard',
        firstDay: 0, // Sunday (0) or Monday (1) as first day
        // Callbacks will be defined in methods
      },

      // Reminders
      reminders: [],
      showAddReminderForm: false,
      showQuickAddReminderModal: false,
      showRemindersModal: false,
      isCreatingReminder: false,

      // Reminder form
      reminderForm: {
        days_before: 1
      },

      // Search and Filter state
      searchQuery: '',
      showFilterPanel: false,
      filters: {
        types: [], // Array of event types to filter by
        showCompleted: true,
        showIncomplete: true,
        showAllDay: true,
        showTimedEvents: true,
        showWithReminders: false, // Filter for events with reminders
        dateFrom: null,
        dateTo: null,
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

      // Custom dropdown states
      showTypeDropdown: false,
      showReminderDropdown: false,
      showQuickReminderDropdown: false,

      // Form data
      eventForm: {
        id: null,
        title: '',
        description: '',
        date: new Date(),
        dateFormatted: this.formatDateForInput(new Date()),
        all_day: false,
        start_time: '09:00',
        end_time: '10:00',
        type: 'general',
        completed: false,
        location: ''
      },

      // Calendar settings
      calendarSettings: {
        firstDayOfWeek: 'sunday',
        defaultEventDuration: '60',
        defaultEventType: 'general',
        timeFormat: '12h',
        dateFormat: 'MM/DD/YYYY'
      },

      // Default values for new events
      defaultEventType: 'general',
      defaultDuration: 60,

      // Touch gestures
      touchStartX: 0,
      touchEndX: 0
    };
  },
  computed: {
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

      // Count reminders filter
      if (this.filters.showWithReminders) {
        count++;
      }

      // Count date range filters
      if (this.filters.dateFrom || this.filters.dateTo) {
        count++;
      }

      // Count search query
      if (this.searchQuery.trim() !== '') {
        count++;
      }

      return count;
    },

    // Reminders computations
    upcomingReminders() {
      // Filter reminders that haven't been sent yet
      return this.reminders.filter(reminder => !reminder.sent);
    },

    sentReminders() {
      // Filter reminders that have been sent
      return this.reminders.filter(reminder => reminder.sent);
    },

    dateFormatted: {
      get() {
        if (!this.eventForm.date) return '';
        const date = new Date(this.eventForm.date);
        return this.formatDateForInput(date);
      },
      set(value) {
        this.eventForm.date = new Date(value);
      }
    }
  },
  watch: {
    // Watch for changes to filteredEvents to update FullCalendar
    filteredEvents: {
      handler(newEvents) {
        // Convert to FullCalendar event format
        const fcEvents = newEvents.map(event => this.convertToFullCalendarEvent(event));

        // Update the calendar events
        const calendarApi = this.$refs.fullCalendar?.getApi();
        if (calendarApi) {
          calendarApi.removeAllEvents();
          calendarApi.addEventSource(fcEvents);
        } else {
          // If calendar not initialized yet, update the options
          this.calendarOptions.events = fcEvents;
        }
      },
      deep: true
    },

    // Watch for current view changes to update FullCalendar
    currentView(newView) {
      const calendarApi = this.$refs.fullCalendar?.getApi();
      if (calendarApi) {
        calendarApi.changeView(newView);

        // Update localStorage
        localStorage.setItem('calendarView', newView);
      }
    },

    // Watch for selectedDate changes to navigate FullCalendar
    selectedDate(newDate) {
      const calendarApi = this.$refs.fullCalendar?.getApi();
      if (calendarApi) {
        calendarApi.gotoDate(newDate);
      }
    },

    // Add watchers for dropdowns
    showTypeDropdown(val) {
      if (val) {
        document.addEventListener('click', this.handleClickOutsideTypeDropdown);
      } else {
        document.removeEventListener('click', this.handleClickOutsideTypeDropdown);
      }
    },

    showReminderDropdown(val) {
      if (val) {
        document.addEventListener('click', this.handleClickOutsideReminderDropdown);
      } else {
        document.removeEventListener('click', this.handleClickOutsideReminderDropdown);
      }
    },

    showQuickReminderDropdown(val) {
      if (val) {
        document.addEventListener('click', this.handleClickOutsideQuickReminderDropdown);
      } else {
        document.removeEventListener('click', this.handleClickOutsideQuickReminderDropdown);
      }
    }
  },
  async mounted() {
    this.darkMode = getDarkModePreference();
    this.checkMobile();

    window.addEventListener("resize", this.checkMobile);
    window.addEventListener('darkModeChange', this.onDarkModeChange);

    // Add listener for calendar settings changes
    window.addEventListener('calendarSettingsChanged', this.applyCalendarSettings);

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
      this.currentView = this.convertOldViewToFullCalendarView(storedCalendarView);
      this.calendarOptions.initialView = this.currentView;
    }

    // Load primary color from localStorage
    const storedPrimaryColor = localStorage.getItem('primaryColor');
    if (storedPrimaryColor) {
      this.setPrimaryColor(storedPrimaryColor, false);
    }

    // Initialize calendar settings
    this.initializeCalendarSettings();

    // Initialize keyboard shortcuts
    this.initKeyboardShortcuts();

    // Initialize FullCalendar with custom options
    this.setupFullCalendarOptions();

    await this.fetchUserProfile();
    await this.fetchEvents();
    await this.fetchReminders();
  },
  beforeUnmount() {
    window.removeEventListener("resize", this.checkMobile);
    window.removeEventListener('darkModeChange', this.onDarkModeChange);
    window.removeEventListener('calendarSettingsChanged', this.applyCalendarSettings);
    window.removeEventListener('keydown', this.handleKeyDown);

    // Clean up any remaining event listeners
    document.removeEventListener('click', this.handleClickOutsideTypeDropdown);
    document.removeEventListener('click', this.handleClickOutsideReminderDropdown);
    document.removeEventListener('click', this.handleClickOutsideQuickReminderDropdown);
  },
  methods: {
    // Initialize FullCalendar options
    setupFullCalendarOptions() {
      // Merge with existing options
      this.calendarOptions = {
        ...this.calendarOptions,
        eventClick: this.handleEventClick,
        dateClick: this.handleDateClick,
        eventDrop: this.handleEventDrop,
        eventResize: this.handleEventResize,
        datesSet: this.handleDatesSet,
        eventClassNames: this.getEventClassNames,
        eventDidMount: this.handleEventDidMount,
        businessHours: {
          daysOfWeek: [1, 2, 3, 4, 5], // Monday - Friday
          startTime: '08:00',
          endTime: '18:00',
        },
        slotMinTime: '06:00:00',
        slotMaxTime: '22:00:00',
        allDaySlot: true,
        eventTimeFormat: {
          hour: '2-digit',
          minute: '2-digit',
          meridiem: this.calendarSettings.timeFormat === '12h'
        },
        // Custom rendering
        eventContent: this.renderEventContent
      };
    },

    // Convert event to FullCalendar format
    convertToFullCalendarEvent(event) {
      // Get color based on event type
      const eventTypeInfo = this.eventTypes.find(type => type.value === event.type) || this.eventTypes[0];

      // Create a FullCalendar event object
      return {
        id: event.id.toString(),
        title: event.title,
        start: event.all_day ? event.date : `${event.date}T${event.start_time}`,
        end: event.all_day ? event.date : `${event.date}T${event.end_time}`,
        allDay: event.all_day,
        backgroundColor: eventTypeInfo.color,
        borderColor: eventTypeInfo.color,
        textColor: '#ffffff',
        extendedProps: {
          description: event.description,
          location: event.location,
          type: event.type,
          completed: event.completed,
          originalEvent: event, // Store the original event for reference
          hasReminder: this.hasReminder(event.id)
        }
      };
    },

    // Convert old view names to FullCalendar view names
    convertOldViewToFullCalendarView(oldView) {
      const viewMap = {
        'month': 'dayGridMonth',
        'week': 'timeGridWeek',
        'day': 'timeGridDay'
      };

      return viewMap[oldView] || 'dayGridMonth';
    },

    // FullCalendar handlers
    handleEventClick(info) {
      // Get the original event data
      const eventId = parseInt(info.event.id);
      const originalEvent = this.events.find(e => e.id === eventId);

      if (originalEvent) {
        this.selectedEvent = originalEvent;
        this.showEventDetailsModal = true;
      }
    },

    handleDateClick(info) {
      this.selectedDate = new Date(info.date);

      // If clicking on a day cell, open the create event modal
      if (info.view.type === 'dayGridMonth') {
        // Set up new event at the clicked date
        this.openCreateEventModalWithDate(info.date);
      } else {
        // For week or day view, set the time too
        const hour = new Date(info.date).getHours();
        this.createEventAtTime(info.date, hour);
      }
    },

    handleEventDrop(info) {
      // Get the original event
      const eventId = parseInt(info.event.id);
      const originalEvent = this.events.find(e => e.id === eventId);

      if (!originalEvent) return;

      // Create updated event object
      const updatedEvent = { ...originalEvent };

      // Update date and times
      const newStart = info.event.start;
      if (updatedEvent.all_day) {
        updatedEvent.date = this.formatDateISO(newStart);
      } else {
        updatedEvent.date = this.formatDateISO(newStart);

        // Update time
        updatedEvent.start_time = `${String(newStart.getHours()).padStart(2, '0')}:${String(newStart.getMinutes()).padStart(2, '0')}`;

        // Calculate new end time based on the duration
        if (info.event.end) {
          const newEnd = info.event.end;
          updatedEvent.end_time = `${String(newEnd.getHours()).padStart(2, '0')}:${String(newEnd.getMinutes()).padStart(2, '0')}`;
        } else {
          // If no end time, use default duration
          const endTime = new Date(newStart);
          endTime.setMinutes(endTime.getMinutes() + this.defaultDuration);
          updatedEvent.end_time = `${String(endTime.getHours()).padStart(2, '0')}:${String(endTime.getMinutes()).padStart(2, '0')}`;
        }
      }

      // Update the event via API
      this.updateEventAfterDrop(updatedEvent);
    },

    handleEventResize(info) {
      // Get the original event
      const eventId = parseInt(info.event.id);
      const originalEvent = this.events.find(e => e.id === eventId);

      if (!originalEvent || originalEvent.all_day) return;

      // Create updated event object
      const updatedEvent = { ...originalEvent };

      // Update end time
      if (info.event.end) {
        const newEnd = info.event.end;
        updatedEvent.end_time = `${String(newEnd.getHours()).padStart(2, '0')}:${String(newEnd.getMinutes()).padStart(2, '0')}`;

        // Update the event via API
        this.updateEventAfterDrop(updatedEvent);
      }
    },

    handleDatesSet(info) {
      // Update the selected date based on the current view
      this.selectedDate = info.start;

      // Store the current date for navigation
      const middleDate = new Date(info.start.getTime() + (info.end.getTime() - info.start.getTime()) / 2);
      this.currentDate = middleDate;
    },

    // Custom event rendering
    getEventClassNames(info) {
      const classes = [];

      // Add event type class
      if (info.event.extendedProps.type) {
        classes.push(`${info.event.extendedProps.type}-event`);
      }

      // Add completed class
      if (info.event.extendedProps.completed) {
        classes.push('completed-event');
      }

      // Add reminder class
      if (info.event.extendedProps.hasReminder) {
        classes.push('has-reminder');
      }

      return classes;
    },

    handleEventDidMount(info) {
      // Add reminder indicator if the event has reminders
      if (info.event.extendedProps.hasReminder) {
        const eventEl = info.el;
        const reminderIcon = document.createElement('span');
        reminderIcon.className = 'reminder-indicator';
        reminderIcon.textContent = '⏰';
        reminderIcon.title = 'Has reminder';

        // Add to the title element
        const titleEl = eventEl.querySelector('.fc-event-title');
        if (titleEl) {
          titleEl.appendChild(reminderIcon);
        }
      }
    },

    renderEventContent(info) {
      // By default, use FullCalendar's rendering
      return null;
    },

    // Theme and appearance methods
    setPrimaryColor(color, saveToStorage = true) {
      this.primaryColor = color;
      document.documentElement.style.setProperty('--primary-color', color);

      // Calculate darker and lighter variants
      const darkerColor = this.adjustColorBrightness(color, -30);
      const lighterColor = this.adjustColorBrightness(color, 30);

      document.documentElement.style.setProperty('--primary-dark', darkerColor);
      document.documentElement.style.setProperty('--primary-light', lighterColor);

      if (saveToStorage) {
        localStorage.setItem('primaryColor', color);
      }

      // Update FullCalendar theme colors
      this.updateCalendarThemeColors();
    },

    updateCalendarThemeColors() {
      // Apply custom CSS to FullCalendar elements
      document.documentElement.style.setProperty('--fc-button-bg-color', this.primaryColor);
      document.documentElement.style.setProperty('--fc-button-border-color', this.primaryColor);
      document.documentElement.style.setProperty('--fc-button-hover-bg-color', this.adjustColorBrightness(this.primaryColor, -20));
      document.documentElement.style.setProperty('--fc-button-hover-border-color', this.adjustColorBrightness(this.primaryColor, -20));
      document.documentElement.style.setProperty('--fc-today-bg-color', this.adjustColorBrightness(this.primaryColor, 60, 0.2));
    },

    adjustColorBrightness(hex, percent, alpha = 1) {
      // Convert hex to RGB
      let r = parseInt(hex.substring(1, 3), 16);
      let g = parseInt(hex.substring(3, 5), 16);
      let b = parseInt(hex.substring(5, 7), 16);

      // Adjust brightness
      r = this.clamp(r + percent);
      g = this.clamp(g + percent);
      b = this.clamp(b + percent);

      if (alpha < 1) {
        // Return rgba for transparency
        return `rgba(${r}, ${g}, ${b}, ${alpha})`;
      } else {
        // Convert back to hex
        return `#${r.toString(16).padStart(2, '0')}${g.toString(16).padStart(2, '0')}${b.toString(16).padStart(2, '0')}`;
      }
    },

    clamp(value) {
      return Math.max(0, Math.min(255, value));
    },

    toggleDarkMode() {
      // Update localStorage and dispatch event
      localStorage.setItem('darkMode', this.darkMode ? 'dark' : 'light');
      window.dispatchEvent(new CustomEvent('darkModeChange', {
        detail: { isDark: this.darkMode }
      }));

      // Update FullCalendar theme
      this.updateFullCalendarDarkMode();
    },

    updateFullCalendarDarkMode() {
      if (this.darkMode) {
        // Apply dark mode styles to FullCalendar
        document.body.classList.add('fc-dark');
        document.documentElement.style.setProperty('--fc-page-bg-color', '#121212');
        document.documentElement.style.setProperty('--fc-border-color', '#444444');
        document.documentElement.style.setProperty('--fc-neutral-bg-color', '#2c2c2c');
        document.documentElement.style.setProperty('--fc-list-event-hover-bg-color', '#333333');
        document.documentElement.style.setProperty('--fc-neutral-text-color', '#f8f9fa');
        document.documentElement.style.setProperty('--fc-event-border-color', 'rgba(255, 255, 255, 0.1)');
      } else {
        // Revert to light mode
        document.body.classList.remove('fc-dark');
        document.documentElement.style.setProperty('--fc-page-bg-color', '');
        document.documentElement.style.setProperty('--fc-border-color', '');
        document.documentElement.style.setProperty('--fc-neutral-bg-color', '');
        document.documentElement.style.setProperty('--fc-list-event-hover-bg-color', '');
        document.documentElement.style.setProperty('--fc-neutral-text-color', '');
        document.documentElement.style.setProperty('--fc-event-border-color', '');
      }
    },

    // UI Helpers
    toggleSidebar() {
      this.sidebarVisible = !this.sidebarVisible;
      localStorage.setItem('sidebarVisible', this.sidebarVisible);

      // Trigger window resize to force FullCalendar to redraw
      setTimeout(() => {
        window.dispatchEvent(new Event('resize'));
      }, 300);
    },

    onDarkModeChange(event) {
      this.darkMode = event.detail.isDark;
      this.updateFullCalendarDarkMode();
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

      // Update FullCalendar view based on screen size
      if (this.isMobile && this.currentView === 'timeGridWeek') {
        this.setView('dayGridMonth');
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
          }
        } else {
          // Swipe left - next period or hide sidebar
          if (this.sidebarVisible) {
            this.toggleSidebar();
          } else {
            this.navigateNext();
          }
        }
      }
    },

    // View transitions
    setView(view) {
      if (view === this.currentView) return;
      this.currentView = view;

      // The calendar API will be updated through the watch
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
        showTimedEvents: true,
        showWithReminders: false,
        dateFrom: null,
        dateTo: null
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
            (event.description && event.description.toLowerCase().includes(query)) ||
            (event.location && event.location.toLowerCase().includes(query))
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

      // Apply reminders filter
      if (this.filters.showWithReminders) {
        const eventIdsWithReminders = this.reminders.map(r => r.event_id);
        result = result.filter(event => eventIdsWithReminders.includes(event.id));
      }

      // Apply date range filters
      if (this.filters.dateFrom) {
        const fromDate = new Date(this.filters.dateFrom);
        result = result.filter(event => {
          const eventDate = new Date(event.date);
          return eventDate >= fromDate;
        });
      }

      if (this.filters.dateTo) {
        const toDate = new Date(this.filters.dateTo);
        toDate.setHours(23, 59, 59, 999); // End of day
        result = result.filter(event => {
          const eventDate = new Date(event.date);
          return eventDate <= toDate;
        });
      }

      this.filteredEvents = result;
    },

    getFilteredEventsForDay(date) {
      const dateStr = this.formatDateISO(date);
      return this.filteredEvents.filter(event => event.date === dateStr);
    },

    // Keyboard shortcuts
    initKeyboardShortcuts() {
      window.addEventListener('keydown', this.handleKeyDown);
    },

    handleKeyDown(event) {
      // Skip if user is typing in an input field
      if (event.target.tagName === 'INPUT' ||
          event.target.tagName === 'TEXTAREA' ||
          event.target.tagName === 'SELECT') {
        return;
      }

      switch (event.key) {
        case 't':
          this.navigateToday();
          break;
        case 'ArrowLeft':
          this.navigatePrevious();
          break;
        case 'ArrowRight':
          this.navigateNext();
          break;
        case 'd':
        case '1':
          this.setView('timeGridDay');
          break;
        case 'w':
        case '2':
          this.setView('timeGridWeek');
          break;
        case 'm':
        case '3':
          this.setView('dayGridMonth');
          break;
        case 'n':
        case '+':
          this.openCreateEventModal();
          break;
        case 'Escape':
          this.closeAllModals();
          break;
        case '/':
          event.preventDefault();
          document.querySelector('.search-box input').focus();
          break;
        case '?':
          this.showShortcutsModal = true;
          break;
      }
    },

    closeAllModals() {
      this.showEventModal = false;
      this.showEventDetailsModal = false;
      this.showDeleteConfirmModal = false;
      this.showQuickAddReminderModal = false;
      this.showRemindersModal = false;
      this.showShortcutsModal = false;
      this.showFilterPanel = false;
      this.showColorPicker = false;
      this.showReminderDropdown = false;
      this.showQuickReminderDropdown = false;
    },

    closeShortcutsModal() {
      this.showShortcutsModal = false;
    },

    // Calendar Settings Methods
    /**
     * Initialize calendar settings from localStorage or use defaults
     */
    initializeCalendarSettings() {
      try {
        // Try to get settings from localStorage (fallback to defaults)
        const settingsStr = localStorage.getItem('calendarSettings');
        let settings = {};

        if (settingsStr) {
          settings = JSON.parse(settingsStr);
        }

        // Apply settings with defaults
        this.calendarSettings = {
          firstDayOfWeek: settings.firstDayOfWeek || 'sunday',
          defaultEventDuration: settings.defaultEventDuration || '60',
          defaultEventType: settings.defaultEventType || 'general',
          timeFormat: settings.timeFormat || '12h',
          dateFormat: settings.dateFormat || 'MM/DD/YYYY'
        };

        // Apply to the calendar
        this.applyCalendarSettings();
      } catch (error) {
        console.error("Error initializing calendar settings:", error);
        // Use hardcoded defaults if there's an error
      }
    },

    /**
     * Apply calendar settings when they change
     * @param {CustomEvent} event - Optional event with new settings
     */
    applyCalendarSettings(event) {
      // If called as an event handler, update settings from event
      if (event?.detail) {
        this.calendarSettings = {
          ...this.calendarSettings,
          ...event.detail
        };

        // Save to localStorage for persistence
        localStorage.setItem('calendarSettings', JSON.stringify(this.calendarSettings));
      }

      // Apply first day of week to FullCalendar
      const firstDay = this.calendarSettings.firstDayOfWeek === 'monday' ? 1 : 0;
      if (this.calendarOptions) {
        this.calendarOptions.firstDay = firstDay;

        // Update time format
        this.calendarOptions.eventTimeFormat = {
          hour: '2-digit',
          minute: '2-digit',
          meridiem: this.calendarSettings.timeFormat === '12h'
        };

        // Apply to calendar if already mounted
        const calendarApi = this.$refs.fullCalendar?.getApi();
        if (calendarApi) {
          calendarApi.setOption('firstDay', firstDay);
          calendarApi.setOption('eventTimeFormat', this.calendarOptions.eventTimeFormat);
        }
      }

      // Update event form defaults
      this.updateEventDefaults();
    },

    /**
     * Update form defaults for creating new events
     */
    updateEventDefaults() {
      // Event duration in minutes
      const duration = parseInt(this.calendarSettings.defaultEventDuration, 10) || 60;

      // Set default event type for new events
      this.defaultEventType = this.calendarSettings.defaultEventType;

      // Update default duration
      this.defaultDuration = duration;
    },

    /**
     * Calculate default end time based on start time and duration
     */
    calculateDefaultEndTime(startTime) {
      if (!startTime) return '10:00';

      const [hours, minutes] = startTime.split(':').map(num => parseInt(num, 10));
      const startDate = new Date();
      startDate.setHours(hours, minutes, 0, 0);

      const duration = this.defaultDuration || 60;
      const endDate = new Date(startDate.getTime() + duration * 60000);
      return `${String(endDate.getHours()).padStart(2, '0')}:${String(endDate.getMinutes()).padStart(2, '0')}`;
    },

    // Navigation methods
    navigatePrevious() {
      const calendarApi = this.$refs.fullCalendar?.getApi();
      if (calendarApi) {
        calendarApi.prev();
      }
    },

    navigateNext() {
      const calendarApi = this.$refs.fullCalendar?.getApi();
      if (calendarApi) {
        calendarApi.next();
      }
    },

    navigateToday() {
      const calendarApi = this.$refs.fullCalendar?.getApi();
      if (calendarApi) {
        calendarApi.today();
        this.selectedDate = new Date();
      }
    },

    selectDate(date) {
      this.selectedDate = new Date(date);

      // Navigate the calendar to the selected date
      const calendarApi = this.$refs.fullCalendar?.getApi();
      if (calendarApi) {
        calendarApi.gotoDate(date);
      }
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

          // Show confetti animation when marking as completed
          if (updatedEvent.completed) {
            this.triggerConfetti();
          }
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

    async fetchReminders() {
      try {
        const response = await axios.get(`${API_URL}/reminders`, {
          withCredentials: true,
        });

        this.reminders = response.data;
      } catch (error) {
        console.error("Error fetching reminders:", error);
        notify({ type: "error", message: "Failed to load reminders. Please try again." });
      }
    },

    async createNewEvent() {
      this.isSaving = true;
      try {
        // Format for API
        const eventData = {
          title: this.eventForm.title,
          description: this.eventForm.description || null,
          date: this.formatDateISO(this.eventForm.date instanceof Date ? this.eventForm.date : new Date(this.eventForm.date)),
          all_day: this.eventForm.all_day,
          start_time: this.eventForm.all_day ? null : this.eventForm.start_time,
          end_time: this.eventForm.all_day ? null : this.eventForm.end_time,
          type: this.eventForm.type,
          completed: this.eventForm.completed,
          location: this.eventForm.location || null
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

        notify({
          type: "success",
          message: "Event created successfully!",
          duration: 3000
        });
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
          date: this.formatDateISO(this.eventForm.date instanceof Date ? this.eventForm.date : new Date(this.eventForm.date)),
          all_day: this.eventForm.all_day,
          start_time: this.eventForm.all_day ? null : this.eventForm.start_time,
          end_time: this.eventForm.all_day ? null : this.eventForm.end_time,
          type: this.eventForm.type,
          completed: this.eventForm.completed,
          location: this.eventForm.location || null
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

    async updateEventAfterDrop(updatedEvent) {
      try {
        const response = await axios.put(
            `${API_URL}/calendar/events/${updatedEvent.id}`,
            updatedEvent,
            { withCredentials: true }
        );

        // Update local event
        const index = this.events.findIndex(e => e.id === updatedEvent.id);
        if (index !== -1) {
          this.events[index] = response.data;
          this.applyFilters(); // Update filtered events
        }

        notify({
          type: "success",
          message: "Event moved successfully!",
          duration: 2000
        });
      } catch (error) {
        console.error("Error updating event:", error);
        notify({ type: "error", message: "Failed to move event. Please try again." });

        // Revert the drop in the calendar
        const calendarApi = this.$refs.fullCalendar?.getApi();
        if (calendarApi) {
          calendarApi.refetchEvents();
        }
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

        // Also remove any reminders associated with this event
        this.reminders = this.reminders.filter(r => r.event_id !== this.selectedEvent.id);

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

    // Event Form Methods
    openCreateEventModal() {
      // Reset form with defaults from settings
      this.isEditMode = false;
      const today = new Date();
      this.eventForm = {
        id: null,
        title: '',
        description: '',
        date: this.selectedDate,
        dateFormatted: this.formatDateForInput(this.selectedDate),
        all_day: false,
        start_time: '09:00',
        end_time: this.calculateDefaultEndTime('09:00'),
        type: this.defaultEventType || 'general',
        completed: false,
        location: ''
      };
      this.showEventModal = true;
    },

    openCreateEventModalWithDate(date) {
      // Set up new event at the clicked date
      this.isEditMode = false;
      this.eventForm = {
        id: null,
        title: '',
        description: '',
        date: new Date(date),
        dateFormatted: this.formatDateForInput(new Date(date)),
        all_day: false,
        start_time: '09:00',
        end_time: this.calculateDefaultEndTime('09:00'),
        type: this.defaultEventType || 'general',
        completed: false,
        location: ''
      };
      this.showEventModal = true;
    },

    createEventAtTime(date, hour) {
      // Set up new event at the clicked time
      this.isEditMode = false;

      const startHour = hour < 10 ? `0${hour}` : `${hour}`;
      const startTime = `${startHour}:00`;

      this.eventForm = {
        id: null,
        title: '',
        description: '',
        date: new Date(date),
        dateFormatted: this.formatDateForInput(new Date(date)),
        all_day: false,
        start_time: startTime,
        end_time: this.calculateDefaultEndTime(startTime),
        type: this.defaultEventType || 'general',
        completed: false,
        location: ''
      };

      this.showEventModal = true;
    },

    editEvent(event) {
      this.isEditMode = true;
      const eventDate = new Date(event.date);
      this.eventForm = {
        id: event.id,
        title: event.title,
        description: event.description || '',
        date: eventDate,
        dateFormatted: this.formatDateForInput(eventDate),
        all_day: event.all_day,
        start_time: event.start_time || '09:00',
        end_time: event.end_time || '10:00',
        type: event.type || 'general',
        completed: event.completed || false,
        location: event.location || ''
      };
      this.closeEventDetailsModal();
      this.showEventModal = true;
    },

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

    closeEventModal() {
      this.showEventModal = false;
      this.showAddReminderForm = false;
    },

    openEventDetailsModal(event) {
      this.selectedEvent = event;
      this.showEventDetailsModal = true;
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

    // Reminder methods
    hasReminder(eventId) {
      return this.reminders.some(r => r.event_id === eventId);
    },

    getEventReminders(eventId) {
      if (!eventId) return [];
      return this.reminders.filter(r => r.event_id === eventId);
    },

    getEventById(eventId) {
      return this.events.find(e => e.id === eventId);
    },

    getEventTitleById(eventId) {
      const event = this.getEventById(eventId);
      return event ? event.title : 'Unknown Event';
    },

    openAddReminderForm() {
      this.showAddReminderForm = true;
      this.reminderForm.days_before = 1;
    },

    cancelAddReminder() {
      this.showAddReminderForm = false;
    },

    openRemindersModal() {
      this.showRemindersModal = true;
    },

    closeRemindersModal() {
      this.showRemindersModal = false;
    },

    quickAddReminder() {
      this.reminderForm.days_before = 1;
      this.showQuickAddReminderModal = true;
    },

    closeQuickAddReminderModal() {
      this.showQuickAddReminderModal = false;
    },

    async saveReminder() {
      if (!this.eventForm.id) return;

      this.isCreatingReminder = true;
      try {
        const reminderData = {
          event_id: this.eventForm.id,
          days_before: parseInt(this.reminderForm.days_before)
        };

        const response = await axios.post(
            `${API_URL}/reminders/event`,
            reminderData,
            { withCredentials: true }
        );

        // Update local reminders
        await this.fetchReminders();

        this.showAddReminderForm = false;
        notify({ type: "success", message: "Reminder added successfully!" });
      } catch (error) {
        console.error("Error creating reminder:", error);
        notify({ type: "error", message: "Failed to add reminder. Please try again." });
      } finally {
        this.isCreatingReminder = false;
      }
    },

    async saveQuickReminder() {
      if (!this.selectedEvent) return;

      this.isCreatingReminder = true;
      try {
        const reminderData = {
          event_id: this.selectedEvent.id,
          days_before: parseInt(this.reminderForm.days_before)
        };

        const response = await axios.post(
            `${API_URL}/reminders/event`,
            reminderData,
            { withCredentials: true }
        );

        // Update local reminders
        await this.fetchReminders();

        this.closeQuickAddReminderModal();
        notify({ type: "success", message: "Reminder added successfully!" });
      } catch (error) {
        console.error("Error creating reminder:", error);
        notify({ type: "error", message: "Failed to add reminder. Please try again." });
      } finally {
        this.isCreatingReminder = false;
      }
    },

    async deleteReminder(reminderId) {
      try {
        await axios.delete(
            `${API_URL}/reminders/${reminderId}`,
            { withCredentials: true }
        );

        // Remove from local reminders
        this.reminders = this.reminders.filter(r => r.id !== reminderId);

        notify({ type: "success", message: "Reminder deleted successfully!" });
      } catch (error) {
        console.error("Error deleting reminder:", error);
        notify({ type: "error", message: "Failed to delete reminder. Please try again." });
      }
    },

    editEventFromReminder(eventId) {
      const event = this.getEventById(eventId);
      if (event) {
        this.closeRemindersModal();
        this.editEvent(event);
      }
    },

    // Dropdown handling methods
    toggleQuickReminderDropdown() {
      this.showQuickReminderDropdown = !this.showQuickReminderDropdown;
    },

    selectQuickReminderOption(value) {
      this.reminderForm.days_before = parseInt(value);
      this.showQuickReminderDropdown = false;
    },

    formatReminderOption(days) {
      const daysValue = parseInt(days);

      switch(daysValue) {
        case 0: return 'On the day';
        case 1: return '1 day before';
        case 2: return '2 days before';
        case 3: return '3 days before';
        case 7: return '1 week before';
        case 14: return '2 weeks before';
        default: return `${daysValue} days before`;
      }
    },

    // Click outside handlers for dropdowns
    handleClickOutsideTypeDropdown(event) {
      const dropdown = this.$el.querySelector('.select-items');
      const button = this.$el.querySelector('.select-selected');

      if (!dropdown || !button) return;

      if (!dropdown.contains(event.target) && !button.contains(event.target)) {
        this.showTypeDropdown = false;
      }
    },

    handleClickOutsideReminderDropdown(event) {
      // Find the specific dropdown we're working with
      const dropdown = this.$el.querySelector('.add-reminder-form .select-items');
      const button = this.$el.querySelector('.add-reminder-form .select-selected');

      if (!dropdown || !button) return;

      if (!dropdown.contains(event.target) && !button.contains(event.target)) {
        this.showReminderDropdown = false;
      }
    },

    handleClickOutsideQuickReminderDropdown(event) {
      const dropdown = this.$el.querySelector('.quick-reminder-modal .select-items');
      const button = this.$el.querySelector('.quick-reminder-modal .select-selected');

      if (!dropdown || !button) return;

      if (!dropdown.contains(event.target) && !button.contains(event.target)) {
        this.showQuickReminderDropdown = false;
      }
    },

    // Helper functions and formatters
    formatReminderTime(reminder) {
      if (!reminder) return '';

      const days = parseInt(reminder.days_before || 0);

      if (days === 0) {
        return 'On the day of the event';
      } else if (days === 1) {
        return '1 day before the event';
      } else if (days === 7) {
        return '1 week before the event';
      } else if (days === 14) {
        return '2 weeks before the event';
      } else {
        return `${days} days before the event`;
      }
    },

    formatSentReminderDate(reminder) {
      if (!reminder || !reminder.sent_at) return '';

      return new Date(reminder.sent_at).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    },

    // Formatting methods
    formatDateISO(date) {
      const d = new Date(date);
      return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
    },

    formatDateForInput(date) {
      const d = new Date(date);
      const year = d.getFullYear();
      const month = String(d.getMonth() + 1).padStart(2, '0');
      const day = String(d.getDate()).padStart(2, '0');
      return `${year}-${month}-${day}`;
    },

    formatDate(date) {
      return new Date(date).toLocaleDateString('en-US', {
        weekday: 'long',
        month: 'long',
        day: 'numeric',
        year: 'numeric'
      });
    },

    formatEventDate(event) {
      if (!event) return '';

      // Get the date format from settings
      const format = this.calendarSettings.dateFormat || 'MM/DD/YYYY';
      const d = new Date(event.date);

      // Display in long format for event details
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

      if (event.start_time && event.end_time) {
        return `${this.formatTime(event.start_time)} - ${this.formatTime(event.end_time)}`;
      }

      return '';
    },

    formatTime(timeStr) {
      if (!timeStr) return '';

      const [hours, minutes] = timeStr.split(':');
      const hour = parseInt(hours, 10);

      if (this.calendarSettings.timeFormat === '24h') {
        return `${hours}:${minutes}`;
      } else {
        // 12-hour format
        const period = hour >= 12 ? 'PM' : 'AM';
        const hour12 = hour % 12 || 12;
        return `${hour12}:${minutes} ${period}`;
      }
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

    // Visual effects
    triggerConfetti() {
      this.showConfetti = true;
      setTimeout(() => {
        this.showConfetti = false;
      }, 3000);
    }
  }
};
</script>

<style scoped>
/* ======== Base Dashboard Styles & CSS Variables ======== */
:root {
  --primary-color: #9e78ff;
  --primary-dark: #7b49ff;
  --primary-light: #b59dff;
  --bg-light: #f8f9fa;
  --bg-card: #ffffff;
  --bg-input: #f1f3f5;
  --bg-hover: #e9ecef;
  --text-primary: #343a40;
  --text-secondary: #6c757d;
  --border-color: #dee2e6;
  --border-color-light: #e9ecef;
  --error-color: #f44336;
  --success-color: #4CAF50;
  --warning-color: #ff9800;
  --box-shadow-sm: 0 2px 4px rgba(0, 0, 0, 0.05);
  --box-shadow-md: 0 4px 6px rgba(0, 0, 0, 0.07);
  --box-shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.1);
  --transition-speed: 0.3s;
  --border-radius: 6px;
  --border-radius-lg: 12px;
  --border-radius-xl: 16px;
  --shadow-sm: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);
  --shadow-md: 0 3px 6px rgba(0,0,0,0.16), 0 3px 6px rgba(0,0,0,0.23);
  --shadow-lg: 0 10px 20px rgba(0,0,0,0.19), 0 6px 6px rgba(0,0,0,0.23);
  --shadow-xl: 0 14px 28px rgba(0,0,0,0.25), 0 10px 10px rgba(0,0,0,0.22);

  /* FullCalendar variables */
  --fc-border-color: var(--border-color);
  --fc-page-bg-color: var(--bg-card);
  --fc-neutral-bg-color: var(--bg-input);
  --fc-button-bg-color: var(--primary-color);
  --fc-button-border-color: var(--primary-color);
  --fc-button-text-color: #fff;
  --fc-button-hover-bg-color: var(--primary-dark);
  --fc-button-hover-border-color: var(--primary-dark);
  --fc-button-active-bg-color: var(--primary-dark);
  --fc-today-bg-color: rgba(158, 120, 255, 0.1);
  --fc-event-bg-color: var(--primary-color);
  --fc-event-border-color: var(--primary-dark);
  --fc-event-text-color: #fff;
  --fc-event-selected-overlay-color: rgba(0, 0, 0, 0.25);
  --fc-neutral-text-color: var(--text-secondary);
  --fc-list-event-hover-bg-color: var(--bg-hover);
}

.dashboard {
  min-height: 100vh;
  background-color: var(--bg-light);
  color: var(--text-primary);
  transition: background-color var(--transition-speed) ease,
  color var(--transition-speed) ease;
  overflow-x: hidden;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.dark-mode {
  --bg-light: #121212;
  --bg-card: #1e1e1e;
  --bg-input: #2c2c2c;
  --bg-hover: #333333;
  --text-primary: #f8f9fa;
  --text-secondary: #adb5bd;
  --border-color: #444444;
  --border-color-light: #555555;
  --shadow-sm: 0 1px 3px rgba(0,0,0,0.3);
  --shadow-md: 0 3px 6px rgba(0,0,0,0.4);
  --shadow-lg: 0 10px 20px rgba(0,0,0,0.5);

  /* FullCalendar dark mode variables */
  --fc-page-bg-color: var(--bg-card);
  --fc-neutral-bg-color: var(--bg-input);
  --fc-border-color: var(--border-color);
  --fc-neutral-text-color: var(--text-secondary);
  --fc-list-event-hover-bg-color: var(--bg-hover);
}

.dashboard-layout {
  display: flex;
  flex-direction: row;
  position: relative;
  padding-top: 70px; /* Space for fixed navbar */
  min-height: calc(100vh - 70px);
}

/* ======== Animation Classes ======== */
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

.hover-effect {
  transform: translateY(-2px) scale(1.01);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  z-index: 10;
}

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

@keyframes fadeScale {
  0% {
    opacity: 0;
    transform: scale(0.95);
  }
  100% {
    opacity: 1;
    transform: scale(1);
  }
}

@keyframes shimmer {
  0% {
    background-position: -100% 0;
  }
  100% {
    background-position: 100% 0;
  }
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* ======== View Transitions ======== */
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
  transition: transform 0.4s cubic-bezier(0.25, 0.8, 0.25, 1), opacity 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
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
  transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
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

/* ======== Modal Transitions ======== */
.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}

.modal-fade-enter-active .modal-container {
  animation: modalEnter 0.4s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
}

.modal-fade-leave-active .modal-container {
  animation: modalLeave 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) forwards;
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

/* ======== Main Content Styles ======== */
.dashboard-main-content {
  flex: 1;
  padding: 2rem;
  transition: all var(--transition-speed) cubic-bezier(0.25, 0.8, 0.25, 1);
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03);
}

.dashboard-main-content.expanded {
  margin-right: 0;
}

/* ======== Dashboard Header ======== */
.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.dashboard-header h1 {
  font-size: 1.75rem;
  font-weight: 700;
  background: linear-gradient(90deg, var(--primary-dark), var(--primary-light));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-fill-color: transparent;
  margin: 0;
  letter-spacing: -0.02em;
  position: relative;
  padding-bottom: 0.5rem;
}

.dashboard-header h1::after {
  content: '';
  position: absolute;
  left: 0;
  bottom: 0;
  width: 40px;
  height: 3px;
  background: var(--primary-color);
  border-radius: 3px;
}

.dark-mode .dashboard-header h1 {
  background: linear-gradient(90deg, var(--primary-light), #ffffff);
  -webkit-background-clip: text;
  background-clip: text;
}

/* ======== Calendar Actions ======== */
.calendar-actions {
  display: flex;
  align-items: center;
  gap: 1.25rem;
}

.view-selector {
  display: flex;
  border-radius: var(--border-radius);
  overflow: hidden;
  border: 1px solid var(--border-color);
  background-color: var(--bg-card);
  box-shadow: var(--shadow-sm);
  position: relative;
  z-index: 1;
}

.view-btn {
  background-color: var(--bg-card);
  color: var(--text-secondary);
  border: none;
  padding: 0.6rem 1.25rem;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  font-size: 0.9rem;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  position: relative;
  overflow: hidden;
}

.view-btn:not(:last-child) {
  border-right: 1px solid var(--border-color-light);
}

/* Button hover effect with subtle animation */
.view-btn:hover:not(.active, .ai-btn) {
  background-color: var(--bg-hover);
  color: var(--text-primary);
}

.view-btn:hover::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 3px;
  background-color: var(--primary-color);
  transform: scaleX(1);
  transition: transform 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.view-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: var(--primary-color);
  opacity: 0;
  z-index: -1;
  transition: opacity 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.view-btn.active::before {
  opacity: 1;
}

.view-btn svg {
  width: 14px;
  height: 14px;
  transition: transform 0.3s ease;
}

.view-btn:hover svg {
  transform: scale(1.1);
}

.view-btn.active {
  background-color: var(--primary-color);
  color: white;
  font-weight: 600;
  box-shadow: 0 0 0 2px rgba(123, 73, 255, 0.2);
}

.view-btn.ai-btn::after {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: linear-gradient(
      to right,
      rgba(255, 255, 255, 0) 0%,
      rgba(255, 255, 255, 0.3) 50%,
      rgba(255, 255, 255, 0) 100%
  );
  transform: rotate(30deg);
  animation: shimmer 4s infinite;
  pointer-events: none;
}

.view-btn.ai-btn:hover {
  background-color: var(--primary-dark);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(123, 73, 255, 0.4);
}

/* Add Event Button */
.add-event-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background-color: var(--primary-color);
  color: white;
  border: none;
  border-radius: var(--border-radius);
  padding: 0.7rem 1.25rem;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  font-weight: 500;
  box-shadow: 0 2px 4px rgba(123, 73, 255, 0.2);
  position: relative;
  overflow: hidden;
}

.add-event-button::after {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: linear-gradient(
      to right,
      rgba(255, 255, 255, 0) 0%,
      rgba(255, 255, 255, 0.3) 50%,
      rgba(255, 255, 255, 0) 100%
  );
  transform: rotate(30deg);
  animation: shimmer 3s infinite;
  pointer-events: none;
}

.add-event-button:hover {
  background-color: var(--primary-dark);
  transform: translateY(-2px);
  box-shadow: 0 4px 10px rgba(123, 73, 255, 0.3);
}

.add-event-button:active {
  transform: translateY(0);
  box-shadow: 0 2px 4px rgba(123, 73, 255, 0.2);
}

/* ======== Sidebar Styles ======== */
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
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  z-index: 10;
}

.toggle-text {
  font-size: 14px;
  font-weight: 500;
}

.sidebar-toggle:hover {
  background-color: var(--primary-dark);
  transform: scale(1.05);
  box-shadow: 0 4px 8px rgba(123, 73, 255, 0.3);
}

.sidebar-toggle:active {
  transform: scale(0.97);
}

.sidebar-show-button {
  position: fixed;
  right: 2rem;
  top: 6rem;
  box-shadow: 0 3px 12px rgba(123, 73, 255, 0.3);
}

.sidebar-hide-button {
  position: absolute;
  top: 1rem;
  right: 1rem;
  z-index: 20;
}

/* Sidebar container */
.dashboard-sidebar {
  width: 320px;
  background-color: var(--bg-card);
  border-left: 1px solid var(--border-color);
  box-shadow: var(--shadow-md);
  transition: all var(--transition-speed) cubic-bezier(0.25, 0.8, 0.25, 1);
  position: relative;
  overflow: hidden;
  z-index: 100;
}

/* Slide transition for sidebar */
.slide-enter-active,
.slide-leave-active {
  transition: transform var(--transition-speed) cubic-bezier(0.25, 0.8, 0.25, 1),
  opacity var(--transition-speed) cubic-bezier(0.25, 0.8, 0.25, 1);
}

.slide-enter-from,
.slide-leave-to {
  transform: translateX(100%);
  opacity: 0;
}

/* ======== Loading and Auth States ======== */
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
  border: 4px solid rgba(123, 73, 255, 0.1);
  border-radius: 50%;
  border-top-color: var(--primary-color);
  animation: spin 1.2s cubic-bezier(0.5, 0, 0.5, 1) infinite;
  margin-bottom: 1rem;
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
  box-shadow: var(--shadow-lg);
  text-align: center;
  max-width: 400px;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.5rem;
  transition: transform 0.3s cubic-bezier(0.25, 0.8, 0.25, 1), box-shadow 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.auth-card:hover {
  transform: translateY(-5px);
  box-shadow: var(--shadow-xl);
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
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  position: relative;
  overflow: hidden;
}

.login-button::after {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: linear-gradient(
      to right,
      rgba(255, 255, 255, 0) 0%,
      rgba(255, 255, 255, 0.3) 50%,
      rgba(255, 255, 255, 0) 100%
  );
  transform: rotate(30deg);
  animation: shimmer 3s infinite;
  pointer-events: none;
}

.login-button:hover {
  background: var(--primary-dark);
  transform: translateY(-3px);
  box-shadow: var(--shadow-md);
}

/* ======== Calendar Content ======== */
.calendar-content {
  background-color: var(--bg-card);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow-md);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  position: relative; /* For view transitions */
  border: 1px solid var(--border-color);
  transition: box-shadow 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.calendar-content:hover {
  box-shadow: var(--shadow-lg);
}

/* ======== FullCalendar Styles ======== */
.fullcalendar-container {
  padding: 1rem;
  transition: all 0.3s ease;
  height: 800px;
}

/* Customize FullCalendar elements */
:deep(.fc) {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  --fc-small-font-size: 0.85em;
  --fc-page-bg-color: var(--bg-card);
  --fc-neutral-bg-color: var(--bg-input);
  --fc-border-color: var(--border-color);
}

:deep(.fc .fc-toolbar-title) {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--primary-dark);
}

:deep(.fc-theme-standard .fc-scrollgrid) {
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  overflow: hidden;
}

:deep(.fc-theme-standard th) {
  background-color: var(--bg-input);
  padding: 0.75rem;
  font-weight: 600;
  color: var(--text-secondary);
}

:deep(.fc-col-header-cell-cushion) {
  padding: 8px;
  font-weight: 600;
  color: var(--text-secondary);
}

:deep(.fc-daygrid-day-number) {
  font-weight: 500;
  padding: 8px;
  color: var(--text-primary);
}

:deep(.fc-timegrid-slot-label-cushion) {
  font-size: 0.85rem;
  color: var(--text-secondary);
}

:deep(.fc-timegrid-now-indicator-line) {
  border-color: var(--error-color);
}

:deep(.fc-timegrid-now-indicator-arrow) {
  border-color: var(--error-color);
  background-color: var(--error-color);
}

/* Event styling */
:deep(.fc-event) {
  border-radius: var(--border-radius);
  border-width: 1px;
  box-shadow: var(--shadow-sm);
  transition: transform 0.2s, box-shadow 0.2s;
}

:deep(.fc-event:hover) {
  transform: translateY(-2px) scale(1.01);
  box-shadow: var(--shadow-md);
  z-index: 10 !important;
}

:deep(.fc-daygrid-event-dot) {
  border-color: var(--primary-color);
}

:deep(.fc-h-event) {
  background-color: var(--primary-color);
  border-color: var(--primary-dark);
}

:deep(.fc-event-title) {
  font-weight: 500;
  padding: 2px 0;
}

:deep(.fc-event-time) {
  font-weight: 600;
}

/* Custom event types */
:deep(.general-event) {
  background-color: #2196F3 !important;
  border-color: #0d47a1 !important;
}

:deep(.assignment-event) {
  background-color: #F44336 !important;
  border-color: #b71c1c !important;
}

:deep(.exam-event) {
  background-color: #E91E63 !important;
  border-color: #880e4f !important;
}

:deep(.study-event) {
  background-color: #4CAF50 !important;
  border-color: #1b5e20 !important;
}

:deep(.meeting-event) {
  background-color: #673AB7 !important;
  border-color: #311b92 !important;
}

:deep(.celebration-event) {
  background-color: #FF9800 !important;
  border-color: #e65100 !important;
}

:deep(.completed-event) {
  opacity: 0.7;
  text-decoration: line-through;
}

:deep(.has-reminder .fc-event-title::after) {
  content: "⏰";
  margin-left: 4px;
  font-size: 0.8em;
}

:deep(.fc-day-today) {
  background-color: var(--fc-today-bg-color) !important;
  font-weight: bold;
}

/* FullCalendar responsive adjustments */
@media (max-width: 768px) {
  .fullcalendar-container {
    height: 600px;
  }

  :deep(.fc-toolbar) {
    flex-direction: column;
    gap: 8px;
  }

  :deep(.fc-toolbar-chunk) {
    display: flex;
    justify-content: center;
  }
}

@media (max-width: 480px) {
  .fullcalendar-container {
    height: 500px;
    padding: 0.5rem;
  }

  :deep(.fc-toolbar-title) {
    font-size: 1rem !important;
  }

  :deep(.fc-col-header-cell-cushion) {
    padding: 4px;
  }

  :deep(.fc-daygrid-day-number) {
    padding: 4px;
  }
}

/* ======== Search and Filter Styles ======== */
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
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.search-box:focus-within {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(123, 73, 255, 0.1);
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
  transition: all 0.2s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.clear-search:hover {
  color: var(--text-primary);
  transform: rotate(90deg);
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
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  font-weight: 500;
  position: relative;
}

.filter-button.active {
  background-color: var(--bg-hover);
  border-color: var(--primary-color);
  color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(123, 73, 255, 0.1);
}

.filter-button svg {
  transition: transform 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.filter-button.active svg {
  transform: rotate(180deg);
  color: var(--primary-color);
}

.filter-button:hover {
  background-color: var(--bg-hover);
  border-color: var(--border-color-light);
}

.filter-count {
  position: absolute;
  top: -8px;
  right: -8px;
  background-color: var(--primary-color);
  color: white;
  width: 22px;
  height: 22px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  font-weight: bold;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.filter-panel {
  background-color: var(--bg-card);
  border-radius: var(--border-radius);
  padding: 1.5rem;
  margin-bottom: 1.5rem;
  border: 1px solid var(--border-color);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  animation: fadeIn 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.filter-section {
  margin-bottom: 1.5rem;
}

.filter-section h3 {
  font-size: 1rem;
  margin: 0 0 0.75rem;
  color: var(--text-secondary);
  font-weight: 500;
  position: relative;
  padding-left: 0.75rem;
}

.filter-section h3::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 3px;
  background-color: var(--primary-color);
  border-radius: 3px;
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
}

.reset-filter-button {
  background-color: transparent;
  color: var(--text-secondary);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  padding: 0.5rem 1rem;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  font-weight: 500;
}

.reset-filter-button:hover {
  background-color: var(--bg-hover);
  border-color: var(--text-secondary);
  color: var(--text-primary);
}

.apply-filter-button {
  background-color: var(--primary-color);
  color: white;
  border: none;
  border-radius: var(--border-radius);
  padding: 0.5rem 1rem;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  font-weight: 500;
}

.apply-filter-button:hover {
  background-color: var(--primary-dark);
  transform: translateY(-2px);
  box-shadow: 0 3px 6px rgba(123, 73, 255, 0.2);
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

.native-date-input,
.native-time-input,
.native-select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  background-color: var(--bg-input);
  color: var(--text-primary);
  font-family: inherit;
  font-size: 1rem;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.native-date-input:focus,
.native-time-input:focus,
.native-select:focus {
  border-color: var(--primary-color);
  outline: none;
  box-shadow: 0 0 0 3px rgba(123, 73, 255, 0.1);
}

.reset-search-button {
  background-color: var(--primary-color);
  color: white;
  border: none;
  border-radius: var(--border-radius);
  padding: 0.5rem 1.5rem;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  font-weight: 500;
  position: relative;
  overflow: hidden;
}

.reset-search-button::after {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: linear-gradient(
      to right,
      rgba(255, 255, 255, 0) 0%,
      rgba(255, 255, 255, 0.3) 50%,
      rgba(255, 255, 255, 0) 100%
  );
  transform: rotate(30deg);
  animation: shimmer 3s infinite;
  pointer-events: none;
}

.reset-search-button:hover {
  background-color: var(--primary-dark);
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(123, 73, 255, 0.3);
}

/* ======== Modal Styles ======== */
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
  backdrop-filter: blur(3px);
}

/* Improved Modal Styles */
.modal-container {
  background-color: var(--bg-card);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow-xl);
  width: 90%;
  max-width: 600px;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  border: 1px solid var(--border-color);
}

.improved-modal {
  border-radius: 16px;
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.2);
  border: none;
}

.delete-confirm-modal {
  max-width: 400px;
}

.quick-reminder-modal,
.more-events-modal {
  max-width: 450px;
}

.shortcuts-modal {
  max-width: 500px;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid var(--border-color);
  background-color: var(--bg-card);
}

.modal-header h2 {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--text-primary);
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
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.close-modal-btn:hover {
  background-color: var(--bg-hover);
  color: var(--text-primary);
  transform: rotate(90deg);
}

.modal-body {
  padding: 1.5rem;
  overflow-y: auto;
  position: relative;
  max-height: calc(90vh - 130px); /* Subtract header & footer heights */
}

.modal-footer {
  padding: 1.5rem;
  border-top: 1px solid var(--border-color);
  background-color: var(--bg-card);
}

.modal-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.action-buttons {
  display: flex;
  gap: 1rem;
}

/* Delete confirmation modal */
.delete-confirm-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 1rem;
}

.warning-icon {
  color: var(--error-color);
  margin-bottom: 1.5rem;
}

.delete-actions {
  display: flex;
  justify-content: center;
  gap: 1rem;
}

.confirm-delete-button {
  background-color: var(--error-color);
  color: white;
  border: none;
}

.confirm-delete-button:hover {
  background-color: #d32f2f;
}

/* Quick reminder modal styles */
.quick-reminder-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 1rem;
}

.reminder-modal-actions {
  display: flex;
  justify-content: center;
  gap: 1rem;
}

/* ======== Form Styles ======== */
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
  color: var(--text-primary);
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  background-color: var(--bg-input);
  color: var(--text-primary);
  font-family: inherit;
  font-size: 1rem;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  border-color: var(--primary-color);
  outline: none;
  box-shadow: 0 0 0 3px rgba(123, 73, 255, 0.1);
}

.form-group input:hover,
.form-group select:hover,
.form-group textarea:hover {
  border-color: var(--primary-light);
}

/* Custom Date Input styles */
.custom-date-input {
  position: relative;
  display: flex;
  align-items: center;
}

.custom-date-input input {
  padding-right: 2.5rem;
}

.custom-date-input svg {
  position: absolute;
  right: 0.75rem;
  color: var(--text-secondary);
  pointer-events: none;
}

/* Custom Select styles */
.custom-select {
  position: relative;
  width: 100%;
  z-index: 100;
}

.select-selected {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.85rem 1rem;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  background-color: var(--bg-input);
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  font-size: 0.95rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.select-selected:hover {
  border-color: var(--primary-light);
  background-color: var(--bg-hover);
}

.custom-select.open .select-selected {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(123, 73, 255, 0.1);
  border-radius: var(--border-radius) var(--border-radius) 0 0;
}

.select-selected svg {
  transition: transform 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  color: var(--primary-color);
  width: 16px;
  height: 16px;
}

.custom-select.open .select-selected svg {
  transform: rotate(180deg);
}

.select-items {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background-color: var(--bg-card);
  border-radius: 0 0 var(--border-radius) var(--border-radius);
  border: 1px solid var(--primary-color);
  border-top: none;
  margin-top: -1px;
  /* Remove max-height to show all options */
  max-height: none;
  overflow-y: visible;
  box-shadow: 0 5px 12px rgba(0, 0, 0, 0.15);
  z-index: 9999;
  animation: slideDown 0.2s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.select-item {
  padding: 0.85rem 1rem;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.25, 0.8, 0.25, 1);
  display: flex;
  align-items: center;
  gap: 0.75rem;
  border-bottom: 1px solid var(--border-color-light);
  position: relative;
  z-index: 1;
}

.select-item:last-child {
  border-bottom: none;
}

.select-item:hover {
  background-color: var(--bg-hover);
}

.select-item.selected {
  background-color: rgba(123, 73, 255, 0.1);
  font-weight: 500;
  color: var(--primary-color);
}

/* Date range picker in filter panel */
.date-range-picker {
  display: flex;
  gap: 1rem;
}

.date-input-group {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

/* Checkbox styles */
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

/* Custom checkbox styles */
.checkbox-container {
  position: relative;
  padding-left: 28px;
  cursor: pointer;
}

.checkbox-container input {
  position: absolute;
  opacity: 0;
  cursor: pointer;
  height: 0;
  width: 0;
}

.checkmark {
  position: absolute;
  top: 0;
  left: 0;
  height: 18px;
  width: 18px;
  background-color: var(--bg-input);
  border: 1px solid var(--border-color);
  border-radius: 4px;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.checkbox-container:hover input ~ .checkmark {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(123, 73, 255, 0.1);
}

.checkbox-container input:checked ~ .checkmark {
  background-color: var(--primary-color);
  border-color: var(--primary-color);
}

.checkmark:after {
  content: "";
  position: absolute;
  display: none;
}

.checkbox-container input:checked ~ .checkmark:after {
  display: block;
}

.checkbox-container .checkmark:after {
  left: 6px;
  top: 2px;
  width: 5px;
  height: 10px;
  border: solid white;
  border-width: 0 2px 2px 0;
  transform: rotate(45deg);
  animation: fadeIn 0.2s cubic-bezier(0.25, 0.8, 0.25, 1);
}

/* ======== Button Styles ======== */
.cancel-button,
.save-button,
.delete-button,
.close-button,
.view-day-button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border-radius: var(--border-radius);
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.cancel-button {
  background-color: transparent;
  color: var(--text-secondary);
  border: 1px solid var(--border-color);
}

.cancel-button:hover {
  background-color: var(--bg-hover);
  color: var(--text-primary);
  border-color: var(--text-secondary);
}

.save-button {
  background-color: var(--primary-color);
  color: white;
  border: none;
  box-shadow: 0 2px 4px rgba(123, 73, 255, 0.2);
  position: relative;
  overflow: hidden;
}

.save-button::after {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: linear-gradient(
      to right,
      rgba(255, 255, 255, 0) 0%,
      rgba(255, 255, 255, 0.3) 50%,
      rgba(255, 255, 255, 0) 100%
  );
  transform: rotate(30deg);
  animation: shimmer 3s infinite;
  pointer-events: none;
}

.save-button:hover {
  background-color: var(--primary-dark);
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(123, 73, 255, 0.3);
}

.save-button:disabled {
  background-color: var(--border-color);
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.save-button:disabled::after {
  display: none;
}

.delete-button {
  background-color: transparent;
  color: var(--error-color);
  border: 1px solid var(--error-color);
}

.delete-button:hover {
  background-color: rgba(244, 67, 54, 0.05);
  box-shadow: 0 0 0 3px rgba(244, 67, 54, 0.1);
}

.delete-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.close-button {
  background-color: var(--primary-color);
  color: white;
  border: none;
  margin: 0 auto;
}

.close-button:hover {
  background-color: var(--primary-dark);
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(123, 73, 255, 0.3);
}

.view-day-button {
  background-color: var(--primary-light);
  color: white;
  border: none;
  margin-right: 1rem;
}

.view-day-button:hover {
  background-color: var(--primary-color);
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(123, 73, 255, 0.3);
}

/* ======== Event Details Styles ======== */
.event-details-header {
  padding: 1.75rem;
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
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-weight: 500;
  letter-spacing: 0.02em;
  backdrop-filter: blur(5px);
}

.event-details-content {
  padding: 1.5rem;
}

.event-details-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
  color: var(--text-primary);
}

.event-details-item svg {
  color: var(--primary-color);
}

.event-details-description {
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid var(--border-color-light);
}

.event-details-description h4 {
  font-size: 1rem;
  margin: 0 0 0.75rem;
  color: var(--text-primary);
}

.event-details-description p {
  margin: 0;
  white-space: pre-line;
  color: var(--text-secondary);
  line-height: 1.6;
}

.event-status {
  margin-top: 1.5rem;
  margin-bottom: 1.5rem;
}

.status-badge {
  display: inline-block;
  background-color: var(--success-color);
  color: white;
  font-size: 0.75rem;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-weight: 500;
}

/* ======== Delete Confirmation Styles ======== */
.event-name {
  font-weight: 600;
  text-align: center;
  margin: 1rem 0;
  font-size: 1.1rem;
  color: var(--text-primary);
}

.delete-warning {
  color: var(--error-color);
  font-size: 0.875rem;
  text-align: center;
  margin-top: 1rem;
}

/* ======== Reminder Styles ======== */
.reminder-indicator {
  margin-left: 0.25rem;
  font-size: 0.75rem;
}

.reminder-section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.reminder-section-header label {
  font-weight: 600;
  color: var(--text-primary);
}

.add-reminder-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background-color: var(--primary-color);
  color: white;
  border: none;
  border-radius: var(--border-radius);
  padding: 0.4rem 0.8rem;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.add-reminder-button:hover {
  background-color: var(--primary-dark);
  transform: translateY(-2px);
  box-shadow: 0 3px 6px rgba(123, 73, 255, 0.2);
}

.add-reminder-form {
  background-color: var(--bg-input);
  border-radius: var(--border-radius);
  padding: 1rem;
  margin-bottom: 1rem;
  border: 1px solid var(--border-color);
  animation: fadeIn 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.reminder-actions {
  display: flex;
  align-items: flex-end;
  gap: 0.5rem;
}

.cancel-reminder-button {
  background-color: transparent;
  color: var(--text-secondary);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  padding: 0.5rem 1rem;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.cancel-reminder-button:hover {
  background-color: var(--bg-hover);
  border-color: var(--text-secondary);
}

.save-reminder-button {
  background-color: var(--primary-color);
  color: white;
  border: none;
  border-radius: var(--border-radius);
  padding: 0.5rem 1rem;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.save-reminder-button:hover {
  background-color: var(--primary-dark);
  transform: translateY(-2px);
  box-shadow: 0 3px 6px rgba(123, 73, 255, 0.2);
}

.event-reminders-list {
  margin-top: 1rem;
}

.reminder-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: var(--bg-input);
  border-radius: var(--border-radius);
  padding: 0.75rem 1rem;
  margin-bottom: 0.5rem;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  border-left: 3px solid var(--primary-color);
}

.reminder-item:hover {
  background-color: var(--bg-hover);
  transform: translateX(2px);
}

.reminder-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.reminder-info svg {
  color: var(--primary-color);
}

.delete-reminder-button {
  background-color: transparent;
  color: var(--error-color);
  border: none;
  padding: 0.5rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.delete-reminder-button:hover {
  background-color: rgba(244, 67, 54, 0.1);
  transform: rotate(90deg);
}

.event-reminders {
  margin-top: 1.5rem;
  border-top: 1px solid var(--border-color);
  padding-top: 1.5rem;
}

.event-reminders h4 {
  font-size: 1rem;
  margin: 0 0 1rem;
  color: var(--text-primary);
}

.reminder-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.quick-add-reminder {
  margin-top: 1.5rem;
  display: flex;
  justify-content: center;
}

.quick-reminder-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background-color: var(--bg-input);
  color: var(--primary-color);
  border: 1px dashed var(--primary-color);
  border-radius: var(--border-radius);
  padding: 0.5rem 1rem;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.quick-reminder-button:hover {
  background-color: rgba(123, 73, 255, 0.05);
  transform: translateY(-2px);
}

.reminder-event-name {
  font-weight: 600;
  font-size: 1.1rem;
  text-align: center;
  margin-bottom: 1.5rem;
  color: var(--primary-dark);
  position: relative;
  padding-bottom: 0.5rem;
}

.reminder-event-name::after {
  content: '';
  position: absolute;
  left: 50%;
  bottom: 0;
  width: 50px;
  height: 2px;
  background: var(--primary-color);
  transform: translateX(-50%);
  border-radius: 2px;
}

/* ======== Reminders Modal Styles ======== */
.reminders-list {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.reminders-section h3 {
  font-size: 1.1rem;
  margin: 0 0 1rem;
  color: var(--primary-dark);
  border-bottom: 1px solid var(--border-color);
  padding-bottom: 0.5rem;
  position: relative;
}

.reminders-section h3::after {
  content: '';
  position: absolute;
  left: 0;
  bottom: -1px;
  width: 40px;
  height: 3px;
  background: var(--primary-color);
  border-radius: 3px;
}

.no-reminders {
  padding: 1.5rem;
  text-align: center;
  color: var(--text-secondary);
  background-color: var(--bg-input);
  border-radius: var(--border-radius);
  border: 1px dashed var(--border-color);
}

.reminder-items {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.reminder-list-item {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  background-color: var(--bg-input);
  border-radius: var(--border-radius);
  padding: 1rem;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  border-left: 4px solid var(--primary-color);
}

.reminder-list-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.05);
}

.reminder-list-item.sent {
  border-left-color: var(--success-color);
  opacity: 0.8;
}

.reminder-details {
  flex: 1;
}

.reminder-event-title {
  font-weight: 600;
  font-size: 1rem;
  margin-bottom: 0.5rem;
  color: var(--text-primary);
}

.reminder-date {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.25rem;
  color: var(--text-secondary);
  font-size: 0.875rem;
}

.reminder-time {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--text-secondary);
  font-size: 0.875rem;
  margin-bottom: 0.5rem;
}

.reminder-status {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 500;
  margin-top: 0.5rem;
}

.reminder-status.pending {
  background-color: rgba(255, 152, 0, 0.1);
  color: #FF9800;
}

.reminder-status.sent {
  background-color: rgba(76, 175, 80, 0.1);
  color: #4CAF50;
}

.reminder-actions {
  display: flex;
  gap: 0.5rem;
}

.edit-event-button {
  background-color: transparent;
  color: var(--primary-color);
  border: 1px solid var(--primary-color);
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.edit-event-button:hover {
  background-color: rgba(123, 73, 255, 0.1);
  transform: rotate(15deg);
}

.center-content {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
}

/* ======== Keyboard Shortcuts Modal ======== */
.shortcuts-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.shortcuts-section h3 {
  font-size: 1rem;
  color: var(--primary-dark);
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid var(--border-color-light);
  position: relative;
}

.shortcuts-section h3::after {
  content: '';
  position: absolute;
  left: 0;
  bottom: -1px;
  width: 40px;
  height: 2px;
  background-color: var(--primary-color);
}

.shortcut-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 0.75rem;
}

.shortcut-keys {
  display: flex;
  gap: 0.5rem;
  align-items: center;
  min-width: 90px;
}

kbd {
  background-color: var(--bg-input);
  border: 1px solid var(--border-color);
  box-shadow: 0 1px 1px rgba(0, 0, 0, 0.2);
  border-radius: 3px;
  padding: 0.25rem 0.5rem;
  font-size: 0.75rem;
  font-family: monospace;
  color: var(--text-primary);
  display: inline-block;
  min-width: 24px;
  text-align: center;
}

.shortcut-description {
  color: var(--text-secondary);
  font-size: 0.875rem;
}

/* ======== Theme Settings ======== */
.floating-action-buttons {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  z-index: 90;
}

.floating-action-button {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--primary-color);
  color: white;
  border: none;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.2);
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.floating-action-button:hover {
  transform: translateY(-3px) rotate(15deg);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
}

.theme-button {
  background-color: var(--primary-color);
}

.shortcuts-button {
  background-color: var(--text-primary);
}

.color-picker-panel {
  position: absolute;
  bottom: 60px;
  right: 0;
  background-color: var(--bg-card);
  border-radius: var(--border-radius);
  padding: 1rem;
  box-shadow: var(--shadow-lg);
  width: 200px;
  animation: fadeScale 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  border: 1px solid var(--border-color);
  z-index: 91;
}

.color-theme-options {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.color-option {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  border: 2px solid transparent;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.color-option:hover {
  transform: scale(1.1);
}

.color-option.active {
  border-color: var(--text-primary);
  box-shadow: 0 0 0 2px rgba(0, 0, 0, 0.1);
}

.theme-toggle {
  padding-top: 0.5rem;
  border-top: 1px solid var(--border-color-light);
}

.theme-toggle-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
}

.theme-toggle-label input {
  display: none;
}

.slider {
  position: relative;
  width: 40px;
  height: 20px;
  background-color: var(--border-color);
  border-radius: 10px;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.slider:before {
  content: '';
  position: absolute;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  left: 2px;
  bottom: 2px;
  background-color: white;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}

input:checked + .slider {
  background-color: var(--primary-color);
}

input:checked + .slider:before {
  transform: translateX(20px);
}

/* ======== Responsive Styles ======== */
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

  .view-btn span {
    display: none;
  }

  .view-btn.ai-btn span {
    display: inline;
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

  .form-row {
    flex-direction: column;
    gap: 1rem;
  }

  .modal-actions {
    flex-direction: column-reverse;
    gap: 1rem;
  }

  .action-buttons {
    display: flex;
    gap: 1rem;
    width: 100%;
  }

  .modal-actions button {
    flex: 1;
  }

  .delete-actions {
    flex-direction: row;
    width: 100%;
  }

  .delete-actions button {
    flex: 1;
  }

  .reminder-modal-actions {
    flex-direction: row;
    width: 100%;
  }

  .reminder-modal-actions button {
    flex: 1;
  }

  .sidebar-show-button {
    right: 1rem;
    top: 5rem;
  }

  .reminder-actions {
    flex-direction: column;
    width: 100%;
  }

  .reminder-list-item {
    flex-direction: column;
  }

  .reminder-actions {
    display: flex;
    flex-direction: row;
    width: 100%;
    margin-top: 0.75rem;
  }

  .reminder-actions button {
    flex: 1;
  }

  .floating-action-buttons {
    bottom: 1rem;
    right: 1rem;
  }

  .floating-action-button {
    width: 40px;
    height: 40px;
  }

  .color-picker-panel {
    right: auto;
    left: 0;
    transform: translateX(-70%);
  }

  .select-selected,
  .custom-date-picker,
  .custom-time-picker {
    padding: 0.75rem;
  }

  .select-item,
  .time-option {
    padding: 0.75rem;
  }
}

@media (max-width: 480px) {
  .dashboard-header h1 {
    font-size: 1.5rem;
  }

  .search-box input {
    font-size: 0.875rem;
    padding: 0.5rem 0;
  }

  .filter-panel {
    padding: 1rem;
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

  .floating-action-buttons {
    bottom: 0.75rem;
    right: 0.75rem;
  }

  .floating-action-button {
    width: 36px;
    height: 36px;
  }

  .floating-action-button svg {
    width: 16px;
    height: 16px;
  }

  .custom-date-picker,
  .custom-time-picker,
  .select-selected {
    font-size: 0.875rem;
    padding: 0.5rem;
  }

  .select-items {
    max-height: 180px;
  }

  .select-item {
    padding: 0.5rem;
    font-size: 0.875rem;
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

  /* Better form inputs for touch */
  .form-group input,
  .form-group select {
    height: 44px;
  }

  .delete-reminder-button {
    min-height: 44px;
    min-width: 44px;
  }

  .edit-event-button {
    min-height: 44px;
    min-width: 44px;
  }

  .floating-action-button {
    width: 56px;
    height: 56px;
  }

  .select-item {
    padding: 12px;  /* Larger touch targets */
    min-height: 44px;
  }

  .select-selected {
    min-height: 44px;
  }
}
</style>