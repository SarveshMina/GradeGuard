<template>
  <div class="study-hub" :class="{ 'dark-mode': darkMode }">
    <!-- Include the Dashboard NavBar with real user data -->
    <DashboardNavBar
        :userName="userProfile.firstName || 'User'"
        :userEmail="userProfile.email || 'user@example.com'"
        :userAvatar="userProfile.avatar"
        :isMobile="isMobile"
        @logout="handleLogout"
    />

    <div class="study-hub-layout">
      <!-- Add the Calendar Sidebar component -->
      <CalendarSideBar
          v-if="showSidebar"
          :events="studySessions"
          :selectedDate="selectedDate"
          @day-click="selectDate"
          @add-event="openCreateEventModal"
          @edit-event="openEditEventModal"
          @delete-event="confirmDeleteSchedule"
          @toggle-completion="toggleEventCompletion"
          @change-schedule="showScheduleSelectionModal"
          @navigate="navigateToTab"
          @toggle-collapse="handleSidebarCollapse"
      />

      <div class="study-hub-container" :class="{ 'with-sidebar': showSidebar && !sidebarCollapsed }">
        <div class="study-hub-header">
          <h1>Study Hub</h1>
          <div class="tab-controls">
            <button
                :class="{ active: activeTab === 'schedule' }"
                @click="activeTab = 'schedule'"
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                <line x1="16" y1="2" x2="16" y2="6"></line>
                <line x1="8" y1="2" x2="8" y2="6"></line>
                <line x1="3" y1="10" x2="21" y2="10"></line>
              </svg>
              Study Schedule
            </button>
            <button
                :class="{ active: activeTab === 'analytics' }"
                @click="activeTab = 'analytics'"
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <line x1="18" y1="20" x2="18" y2="10"></line>
                <line x1="12" y1="20" x2="12" y2="4"></line>
                <line x1="6" y1="20" x2="6" y2="14"></line>
              </svg>
              Analytics & Insights
            </button>
            <button
                :class="{ active: activeTab === 'achievements' }"
                @click="activeTab = 'achievements'"
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="8" r="7"></circle>
                <polyline points="8.21 13.89 7 23 12 20 17 23 15.79 13.88"></polyline>
              </svg>
              Achievements
            </button>
            <button
                :class="{ active: activeTab === 'profile' }"
                @click="activeTab = 'profile'"
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                <circle cx="12" cy="7" r="4"></circle>
              </svg>
              Your Profile
            </button>
          </div>

          <!-- Tutorial/Help Button -->
          <div class="header-actions">
            <button @click="toggleSidebar" class="toggle-sidebar-btn" :title="showSidebar ? 'Hide sidebar' : 'Show sidebar'">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                <line x1="9" y1="3" x2="9" y2="21"></line>
              </svg>
              {{ showSidebar ? 'Hide Calendar' : 'Show Calendar' }}
            </button>
            <button @click="showTutorial = true" class="help-button" title="What is this?">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="10"></circle>
                <path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"></path>
                <line x1="12" y1="17" x2="12.01" y2="17"></line>
              </svg>
              What is this?
            </button>
          </div>
        </div>

        <!-- STUDY SCHEDULE TAB -->
        <div v-if="activeTab === 'schedule'" class="study-schedule-tab animate-fade-in">
          <div class="schedule-header">
            <h2>Your Study Schedule</h2>
            <div class="schedule-actions">
              <button @click="showCreateScheduleModal = true" class="schedule-btn">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <line x1="12" y1="5" x2="12" y2="19"></line>
                  <line x1="5" y1="12" x2="19" y2="12"></line>
                </svg>
                Create Schedule
              </button>
              <button @click="showAIScheduleModal = true" class="ai-schedule-btn">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path>
                  <polyline points="7.5 4.21 12 6.81 16.5 4.21"></polyline>
                  <polyline points="7.5 19.79 7.5 14.6 3 12"></polyline>
                  <polyline points="21 12 16.5 14.6 16.5 19.79"></polyline>
                  <polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline>
                  <line x1="12" y1="22.08" x2="12" y2="12"></line>
                </svg>
                Generate with AI
              </button>
            </div>
          </div>

          <!-- Schedules List Section -->
          <div class="schedules-list-section">
            <h3>Your Schedules</h3>
            <div v-if="isLoading" class="loading-container">
              <div class="loading-spinner"></div>
              <p>Loading your schedules...</p>
            </div>
            <div v-else-if="error" class="error-message">
              <p>{{ error }}</p>
              <button @click="fetchData" class="retry-btn">Try Again</button>
            </div>
            <div v-else-if="schedules.length === 0" class="empty-state">
              <p>You don't have any schedules yet. Create your first schedule to get started.</p>
            </div>
            <div v-else class="schedules-list">
              <div v-for="schedule in schedules" :key="schedule.id" class="schedule-card" :class="{'active-schedule': schedule.is_active}">
                <div class="schedule-card-header">
                  <h4>{{ schedule.name }}</h4>
                  <div class="schedule-badges">
                    <span v-if="schedule.is_ai_generated" class="ai-badge">AI</span>
                    <span v-if="schedule.is_active" class="active-badge">Active</span>
                  </div>
                </div>
                <div class="schedule-card-content">
                  <div class="schedule-details">
                    <div class="schedule-detail-item">
                      <span class="detail-label">Date Range:</span>
                      <span class="detail-value">{{ formatDate(schedule.start_date) }} to {{ formatDate(schedule.end_date) }}</span>
                    </div>
                    <div class="schedule-detail-item">
                      <span class="detail-label">Modules:</span>
                      <span class="detail-value">{{ getModuleNames(schedule.modules).join(', ') }}</span>
                    </div>
                    <div class="schedule-detail-item">
                      <span class="detail-label">Study Days:</span>
                      <span class="detail-value">{{ formatDays(schedule.available_days) }}</span>
                    </div>
                  </div>
                  <div class="schedule-card-actions">
                    <button
                        v-if="!schedule.is_active"
                        @click="activateSchedule(schedule.id)"
                        class="activate-btn"
                        title="Set as Active Schedule"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <polyline points="9 11 12 14 22 4"></polyline>
                        <path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"></path>
                      </svg>
                      Activate
                    </button>
                    <button
                        v-if="!schedule.events_created"
                        @click="showCalendarConfirmation(schedule)"
                        class="calendar-btn"
                        title="Add to Calendar"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                        <line x1="16" y1="2" x2="16" y2="6"></line>
                        <line x1="8" y1="2" x2="8" y2="6"></line>
                        <line x1="3" y1="10" x2="21" y2="10"></line>
                        <line x1="12" y1="15" x2="12" y2="19"></line>
                        <line x1="10" y1="17" x2="14" y2="17"></line>
                      </svg>
                      Add to Calendar
                    </button>
                    <button
                        @click="editSchedule(schedule)"
                        class="edit-btn"
                        title="Edit Schedule"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                        <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
                      </svg>
                      Edit
                    </button>
                    <button
                        @click="confirmDeleteSchedule(schedule)"
                        class="delete-btn"
                        title="Delete Schedule"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <polyline points="3 6 5 6 21 6"></polyline>
                        <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                      </svg>
                      Delete
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div v-if="isLoading" class="loading-container">
            <div class="loading-spinner"></div>
            <p>Loading your study schedule...</p>
          </div>

          <div v-else-if="error" class="error-message">
            <p>{{ error }}</p>
            <button @click="fetchData" class="retry-btn">Try Again</button>
          </div>

          <div v-else class="calendar-container">
            <!-- Calendar View Controls -->
            <div class="calendar-controls">
              <div class="view-selector">
                <button
                    class="view-btn"
                    :class="{ active: calendarView === 'month' }"
                    @click="calendarView = 'month'"
                >
                  Month
                </button>
                <button
                    class="view-btn"
                    :class="{ active: calendarView === 'week' }"
                    @click="calendarView = 'week'"
                >
                  Week
                </button>
                <button
                    class="view-btn"
                    :class="{ active: calendarView === 'day' }"
                    @click="calendarView = 'day'"
                >
                  Day
                </button>
              </div>
              <div class="month-navigator">
                <button @click="navigatePrevious" class="nav-btn">
                  <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M15 18l-6-6 6-6" />
                  </svg>
                </button>
                <button @click="navigateToday" class="today-btn">
                  Today
                </button>
                <button @click="navigateNext" class="nav-btn">
                  <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M9 18l6-6-6-6" />
                  </svg>
                </button>
                <span class="current-period">{{ formatCurrentPeriod() }}</span>
              </div>
            </div>

            <!-- Calendar Views -->
            <div class="calendar-view">
              <!-- Month View -->
              <div v-if="calendarView === 'month'" class="month-view">
                <div class="month-grid-header">
                  <div class="day-header" v-for="day in weekdays" :key="day">{{ day }}</div>
                </div>
                <div class="month-grid">
                  <div
                      v-for="(day, index) in monthDays"
                      :key="index"
                      class="day-cell"
                      :class="{
                      'today': isToday(day.date),
                      'different-month': !day.isCurrentMonth,
                      'selected': isSelectedDate(day.date),
                      'has-events': getEventsForDay(day.date).length > 0
                    }"
                      @click="selectDate(day.date)"
                  >
                    <div class="day-number">{{ formatDayNumber(day.date) }}</div>
                    <div class="day-events">
                      <div
                          v-for="(event, eventIndex) in getEventsForDay(day.date).slice(0, 3)"
                          :key="eventIndex"
                          class="day-event-pill"
                          :class="getEventClass(event)"
                          @click.stop="showEventDetails(event)"
                      >
                        <span class="event-title">{{ event.title }}</span>
                        <span v-if="event.module" class="event-module">{{ getModuleName(event.module) }}</span>
                      </div>
                      <div
                          v-if="getEventsForDay(day.date).length > 3"
                          class="more-events"
                          @click.stop="showMoreEvents(day.date)"
                      >
                        +{{ getEventsForDay(day.date).length - 3 }} more
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Week View -->
              <div v-if="calendarView === 'week'" class="week-view">
                <div class="week-grid-header">
                  <div class="time-column-header"></div>
                  <div
                      class="day-column-header"
                      v-for="(day, index) in weekDays"
                      :key="index"
                      :class="{ 'today': isToday(day.date) }"
                  >
                    <div class="day-name">{{ formatDayName(day.date) }}</div>
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
                      <!-- Current time indicator -->
                      <div
                          v-if="isToday(day.date)"
                          class="current-time-indicator"
                          :style="{ top: calculateCurrentTimePosition() }"
                      >
                        <div class="time-dot"></div>
                        <div class="time-line"></div>
                      </div>

                      <div
                          class="time-cell"
                          v-for="hour in displayHours"
                          :key="`${dayIndex}-${hour}`"
                          @click="createEventAtTime(day.date, hour)"
                      ></div>
                      <div
                          v-for="(event, eventIndex) in getEventsForDay(day.date)"
                          :key="eventIndex"
                          class="week-event"
                          :class="getEventClass(event)"
                          :style="calculateEventPosition(event)"
                          @click="showEventDetails(event)"
                      >
                        <div class="event-time">{{ formatEventTime(event) }}</div>
                        <div class="event-title">{{ event.title }}</div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Day View -->
              <div v-if="calendarView === 'day'" class="day-view">
                <div class="day-view-header">
                  <div class="current-day">
                    {{ formatDate(selectedDate) }}
                  </div>
                </div>
                <div class="day-view-grid">
                  <div class="time-column">
                    <div class="time-cell" v-for="hour in displayHours" :key="hour">
                      {{ formatHour(hour) }}
                    </div>
                  </div>
                  <div class="events-column">
                    <!-- Current time indicator -->
                    <div
                        v-if="isToday(selectedDate)"
                        class="current-time-indicator"
                        :style="{ top: calculateCurrentTimePosition() }"
                    >
                      <div class="time-dot"></div>
                      <div class="time-line"></div>
                    </div>

                    <div
                        class="time-cell"
                        v-for="hour in displayHours"
                        :key="hour"
                        @click="createEventAtTime(selectedDate, hour)"
                    ></div>
                    <div
                        v-for="(event, eventIndex) in getEventsForDay(selectedDate)"
                        :key="eventIndex"
                        class="day-event"
                        :class="getEventClass(event)"
                        :style="calculateEventPosition(event)"
                        @click="showEventDetails(event)"
                    >
                      <div class="event-time">{{ formatEventTime(event) }}</div>
                      <div class="event-title">{{ event.title }}</div>
                      <div class="event-description">{{ event.description }}</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- AI Schedule Tips Section -->
          <div class="ai-tips-section" v-if="aiTips.length > 0">
            <h3>AI Schedule Tips</h3>
            <div class="tips-list">
              <div class="tip-card" v-for="(tip, index) in aiTips" :key="index">
                <div class="tip-icon">
                  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path>
                    <circle cx="12" cy="12" r="4"></circle>
                  </svg>
                </div>
                <div class="tip-content">
                  <div class="tip-title">{{ tip.title }}</div>
                  <div class="tip-text">{{ tip.text }}</div>
                </div>
                <div class="tip-actions">
                  <button @click="acceptTip(tip.id)" class="accept-tip-btn">Apply</button>
                  <button @click="rejectTip(tip.id)" class="reject-tip-btn">Ignore</button>
                </div>
              </div>
            </div>
          </div>

          <!-- No Schedule Placeholder -->
          <div v-if="!isLoading && !error && !activeSchedule && schedules.length === 0" class="no-schedule-placeholder">
            <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round">
              <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
              <line x1="16" y1="2" x2="16" y2="6"></line>
              <line x1="8" y1="2" x2="8" y2="6"></line>
              <line x1="3" y1="10" x2="21" y2="10"></line>
            </svg>
            <h3>No Study Schedule Yet</h3>
            <p>Create your first study schedule to get started. You can create one manually or let AI generate a personalized schedule based on your preferences.</p>
            <div class="placeholder-actions">
              <button @click="showCreateScheduleModal = true" class="schedule-btn">Create Schedule</button>
              <button @click="showAIScheduleModal = true" class="ai-schedule-btn">Generate with AI</button>
            </div>
          </div>
        </div>

        <!-- ANALYTICS & INSIGHTS TAB -->
        <div v-if="activeTab === 'analytics'" class="analytics-tab animate-fade-in">
          <h2>Study Analytics & Insights</h2>

          <div v-if="isLoading" class="loading-container">
            <div class="loading-spinner"></div>
            <p>Loading your analytics data...</p>
          </div>

          <div v-else-if="error" class="error-message">
            <p>{{ error }}</p>
            <button @click="fetchData" class="retry-btn">Try Again</button>
          </div>

          <div v-else-if="!hasAnalyticsData" class="no-data-placeholder">
            <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="20" x2="18" y2="10"></line>
              <line x1="12" y1="20" x2="12" y2="4"></line>
              <line x1="6" y1="20" x2="6" y2="14"></line>
            </svg>
            <h3>No Analytics Data Yet</h3>
            <p>Complete some study sessions to see your analytics data here. This will help you track your progress and improve your study habits.</p>
          </div>

          <div v-else class="analytics-grid">
            <!-- Study Overview Card -->
            <div class="analytics-card">
              <h3>Study Overview</h3>
              <div class="stats-overview">
                <div class="stat-item">
                  <div class="stat-value">{{ studyStats.total_sessions_completed || 0 }}</div>
                  <div class="stat-label">Sessions Completed</div>
                </div>
                <div class="stat-item">
                  <div class="stat-value">{{ studyStats.total_study_hours || 0 }}</div>
                  <div class="stat-label">Study Hours</div>
                </div>
                <div class="stat-item">
                  <div class="stat-value">{{ studyStats.completion_rate || 0 }}%</div>
                  <div class="stat-label">Completion Rate</div>
                </div>
                <div class="stat-item">
                  <div class="stat-value">{{ studyStats.avg_productivity_rating || 0 }}/5</div>
                  <div class="stat-label">Avg. Productivity</div>
                </div>
              </div>
            </div>

            <!-- Study Time Distribution by Module -->
            <div class="analytics-card">
              <h3>Study Time by Module</h3>
              <div class="chart-container">
                <ModuleTimeDistributionChart :chartData="moduleTimeDistribution" />
              </div>
            </div>

            <!-- Study Sessions Timeline -->
            <div class="analytics-card">
              <h3>Study Sessions Timeline</h3>
              <div class="chart-container">
                <StudySessionsTimelineChart :chartData="sessionsTimeline" />
              </div>
            </div>

            <!-- Productivity Patterns -->
            <div class="analytics-card">
              <h3>Productivity Patterns</h3>
              <div class="chart-container">
                <ProductivityPatternsChart :chartData="productivityPatterns" />
              </div>
            </div>

            <!-- Detailed Module Stats -->
            <div class="analytics-card full-width">
              <h3>Module Study Statistics</h3>
              <div v-if="moduleStudyStats.length === 0" class="empty-state">
                <p>No module statistics available yet. Complete more study sessions to see data here.</p>
              </div>
              <div v-else class="module-stats-table">
                <div class="module-stats-header">
                  <div class="module-name-cell">Module</div>
                  <div class="module-stat-cell">Study Sessions</div>
                  <div class="module-stat-cell">Total Hours</div>
                  <div class="module-stat-cell">Weekly Average</div>
                  <div class="module-stat-cell">Avg. Productivity</div>
                  <div class="module-stat-cell">Progress</div>
                </div>
                <div v-for="module in moduleStudyStats" :key="module.id" class="module-stats-row">
                  <div class="module-name-cell">{{ module.name }}</div>
                  <div class="module-stat-cell">{{ module.sessions }}</div>
                  <div class="module-stat-cell">{{ module.hours }} hrs</div>
                  <div class="module-stat-cell">{{ module.weeklyAvg }} hrs</div>
                  <div class="module-stat-cell">{{ module.productivity }}/5</div>
                  <div class="module-stat-cell">
                    <div class="progress-bar-small">
                      <div class="progress-value" :style="{ width: module.progress + '%' }">
                        {{ module.progress }}%
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- ACHIEVEMENTS TAB -->
        <div v-if="activeTab === 'achievements'" class="achievements-tab animate-fade-in">
          <h2>Your Achievements</h2>

          <div v-if="isLoading" class="loading-container">
            <div class="loading-spinner"></div>
            <p>Loading your achievements...</p>
          </div>

          <div v-else-if="error" class="error-message">
            <p>{{ error }}</p>
            <button @click="fetchData" class="retry-btn">Try Again</button>
          </div>

          <div v-else>
            <!-- Study Streak Card -->
            <div class="streak-section">
              <div class="streak-card">
                <h3>Current Study Streak</h3>
                <div class="streak-display">
                  <div class="streak-circle">
                    <div class="streak-value">{{ studyStreak.current_streak || 0 }}</div>
                    <div class="streak-label">days</div>
                  </div>
                  <div class="streak-stats">
                    <div class="streak-stat">
                      <div class="stat-label">Longest Streak</div>
                      <div class="stat-value">{{ studyStreak.longest_streak || 0 }} days</div>
                    </div>
                    <div class="streak-stat">
                      <div class="stat-label">Last Study Session</div>
                      <div class="stat-value">{{ formatDate(studyStreak.last_study_date) || 'None yet' }}</div>
                    </div>
                  </div>
                </div>
                <div class="streak-calendar">
                  <div v-for="(day, index) in recentDays" :key="index" class="calendar-day">
                    <div class="day-date">{{ formatDayDate(day.date) }}</div>
                    <div class="day-indicator" :class="{ studied: day.studied }">
                      <svg v-if="day.studied" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M20 6L9 17l-5-5"></path>
                      </svg>
                    </div>
                  </div>
                </div>
              </div>

              <div class="level-card">
                <h3>Study Level</h3>
                <div class="level-display">
                  <div class="level-badge">
                    <div class="level-value">{{ studyStats.level || 1 }}</div>
                    <div class="level-title">{{ getLevelTitle(studyStats.level || 1) }}</div>
                  </div>
                  <div class="xp-info">
                    <div class="xp-progress-bar">
                      <div class="xp-progress" :style="{ width: (studyStats.level_progress_percent || 0) + '%' }">
                        {{ studyStats.level_progress_percent || 0 }}%
                      </div>
                    </div>
                    <div class="xp-text">
                      <span class="xp-current">{{ studyStats.total_xp || 0 }} XP</span>
                      <span class="xp-next">{{ studyStats.xp_for_next_level || 100 }} XP to level {{ (studyStats.level || 1) + 1 }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Achievements List -->
            <div class="achievements-section">
              <div class="achievements-header">
                <h3>Achievements</h3>
                <div class="achievements-filter">
                  <button
                      v-for="category in achievementCategories"
                      :key="category.value"
                      :class="{ active: selectedAchievementCategory === category.value }"
                      @click="selectedAchievementCategory = category.value"
                  >
                    {{ category.label }}
                  </button>
                </div>
              </div>

              <div v-if="achievements.length === 0" class="empty-state">
                <p>Complete study sessions to earn achievements.</p>
              </div>

              <div v-else class="achievements-grid">
                <div
                    v-for="achievement in filteredAchievements"
                    :key="achievement.id"
                    class="achievement-card"
                    :class="{
                  'completed': achievement.status === 'completed',
                  'in-progress': achievement.status === 'in-progress',
                  'locked': achievement.status === 'locked'
                }"
                >
                  <div class="achievement-icon">
                    <img :src="achievement.icon" :alt="achievement.name">
                  </div>
                  <div class="achievement-info">
                    <h4>{{ achievement.name }}</h4>
                    <p>{{ achievement.description }}</p>
                    <div class="achievement-progress">
                      <div class="progress-bar">
                        <div class="progress" :style="{ width: `${achievement.progressPercent}%` }"></div>
                      </div>
                      <div class="progress-text">{{ achievement.progress }} / {{ achievement.target }}</div>
                    </div>
                  </div>
                  <div class="achievement-badge">
                    <span v-if="achievement.status === 'completed'">Completed</span>
                    <span v-else-if="achievement.status === 'in-progress'">In Progress</span>
                    <span v-else>Locked</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- PROFILE TAB -->
        <div v-if="activeTab === 'profile'" class="profile-tab animate-fade-in">
          <h2>Your Profile</h2>

          <!-- Profile Loading State -->
          <div v-if="isLoading" class="loading-container">
            <div class="loading-spinner"></div>
            <p>Loading your profile...</p>
          </div>

          <!-- Profile Error State -->
          <div v-else-if="error" class="error-message">
            <p>{{ error }}</p>
            <button @click="fetchData" class="retry-btn">Try Again</button>
          </div>

          <!-- Profile Content -->
          <div v-else class="profile-content">
            <div class="profile-card">
              <div class="profile-header">
                <div class="profile-avatar">
                  <img v-if="userProfile.avatar" :src="userProfile.avatar" alt="User Avatar">
                  <div v-else class="avatar-placeholder">
                    {{ getInitials(userProfile.firstName, userProfile.lastName) }}
                  </div>
                </div>
                <div class="profile-info">
                  <h3>{{ userProfile.firstName }} {{ userProfile.lastName }}</h3>
                  <p class="user-email">{{ userProfile.email }}</p>
                  <p class="user-role">{{ userProfile.role || 'Student' }}</p>
                  <p class="user-details">
                    {{ userProfile.university || 'University not set' }} | {{ userProfile.degree || 'Degree not set' }}
                  </p>
                </div>
              </div>
              <div class="profile-details">
                <!-- Enrolled Modules Section -->
                <h4>Your Enrolled Modules</h4>
                <div v-if="enrolledModules.length > 0">
                  <ul class="module-list">
                    <li v-for="module in enrolledModules" :key="module.id" class="module-list-item">
                      <div class="module-info">
                        <span class="module-name">{{ module.name }}</span>
                        <span class="module-code">{{ module.code }}</span>
                      </div>
                      <span class="enrolled-badge">Currently Enrolled</span>
                    </li>
                  </ul>
                </div>
                <div v-else class="empty-state">
                  <p>You are not currently enrolled in any modules.</p>
                  <p v-if="availableModules.length > 0" class="empty-state-tip">
                    Tip: Add modules in the Dashboard and mark them as "Currently Enrolled" to see them here.
                  </p>
                </div>

                <h4>Study Preferences</h4>
                <div class="preference-item">
                  <span class="preference-label">Preferred Study Times:</span>
                  <span class="preference-value">{{ formatPreferredTimes(studyPreferences.preferredTimes) }}</span>
                </div>
                <div class="preference-item">
                  <span class="preference-label">Preferred Session Duration:</span>
                  <span class="preference-value">{{ formatDuration(studyPreferences.sessionDuration) }}</span>
                </div>
                <div class="preference-item">
                  <span class="preference-label">Available Study Days:</span>
                  <span class="preference-value">{{ formatStudyDays(studyPreferences.availableDays) }}</span>
                </div>

                <!-- Academic Information Section - Enhanced -->
                <h4>Academic Information</h4>
                <div class="preference-item">
                  <span class="preference-label">Academic Level:</span>
                  <span class="preference-value" :class="{'preference-value-set': userProfile.academicLevel !== 'Not set'}">
                  {{ userProfile.academicLevel || 'Not set' }}
                </span>
                </div>
                <div class="preference-item">
                  <span class="preference-label">Enrollment Type:</span>
                  <span class="preference-value" :class="{'preference-value-set': userProfile.enrollmentType !== 'Not set'}">
                  {{ userProfile.enrollmentType || 'Not set' }}
                </span>
                </div>
                <div class="preference-item">
                  <span class="preference-label">Current Year:</span>
                  <span class="preference-value preference-value-set">Year {{ userProfile.currentYear || '1' }}</span>
                </div>
              </div>
              <div class="profile-actions">
                <router-link to="/settings?section=academic" class="update-preferences-btn">Update Study Preferences</router-link>
                <router-link to="/profile" class="edit-profile-btn">Edit Profile</router-link>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Tutorial Modal (without images) -->
      <div v-if="showTutorial" class="modal-overlay" @click.self="closeTutorial">
        <div class="modal-container tutorial-modal">
          <div class="modal-header">
            <h3>Study Hub Tutorial</h3>
            <button @click="closeTutorial" class="close-modal-btn">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <line x1="18" y1="6" x2="6" y2="18"></line>
                <line x1="6" y1="6" x2="18" y2="18"></line>
              </svg>
            </button>
          </div>
          <div class="modal-body">
            <div class="tutorial-step" v-if="tutorialStep === 1">
              <h4>Welcome to Study Hub!</h4>
              <p>Study Hub helps you organize your study sessions, track your progress, and improve your study habits.</p>
              <div class="tutorial-icon">
                <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round">
                  <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                  <line x1="16" y1="2" x2="16" y2="6"></line>
                  <line x1="8" y1="2" x2="8" y2="6"></line>
                  <line x1="3" y1="10" x2="21" y2="10"></line>
                </svg>
              </div>
              <p>This tutorial will guide you through the main features of Study Hub.</p>
            </div>

            <div class="tutorial-step" v-if="tutorialStep === 2">
              <h4>Study Schedule</h4>
              <div class="tutorial-icon">
                <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round">
                  <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                  <line x1="16" y1="2" x2="16" y2="6"></line>
                  <line x1="8" y1="2" x2="8" y2="6"></line>
                  <line x1="3" y1="10" x2="21" y2="10"></line>
                </svg>
              </div>
              <p>The Study Schedule tab allows you to:</p>
              <ul>
                <li>Create and manage your study schedules</li>
                <li>Generate AI-powered personalized study plans</li>
                <li>View your study sessions in a calendar</li>
                <li>Track your upcoming and completed sessions</li>
              </ul>
            </div>

            <div class="tutorial-step" v-if="tutorialStep === 3">
              <h4>Analytics & Insights</h4>
              <div class="tutorial-icon">
                <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round">
                  <line x1="18" y1="20" x2="18" y2="10"></line>
                  <line x1="12" y1="20" x2="12" y2="4"></line>
                  <line x1="6" y1="20" x2="6" y2="14"></line>
                </svg>
              </div>
              <p>The Analytics tab provides valuable insights about your study habits:</p>
              <ul>
                <li>Track total study hours and completed sessions</li>
                <li>Analyze your productivity patterns</li>
                <li>View time distribution across modules</li>
                <li>Identify your strengths and areas for improvement</li>
              </ul>
            </div>

            <div class="tutorial-step" v-if="tutorialStep === 4">
              <h4>Achievements</h4>
              <div class="tutorial-icon">
                <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round">
                  <circle cx="12" cy="8" r="7"></circle>
                  <polyline points="8.21 13.89 7 23 12 20 17 23 15.79 13.88"></polyline>
                </svg>
              </div>
              <p>The Achievements tab keeps you motivated:</p>
              <ul>
                <li>Earn achievements by completing study goals</li>
                <li>Track your study streak</li>
                <li>Level up by earning XP from study sessions</li>
                <li>Challenge yourself to unlock all achievements</li>
              </ul>
            </div>

            <div class="tutorial-step" v-if="tutorialStep === 5">
              <h4>Your Profile</h4>
              <div class="tutorial-icon">
                <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                  <circle cx="12" cy="7" r="4"></circle>
                </svg>
              </div>
              <p>The Profile tab shows your personal information:</p>
              <ul>
                <li>View your enrolled modules</li>
                <li>See your study preferences</li>
                <li>Access academic information</li>
                <li>Update your profile and preferences</li>
              </ul>
            </div>

            <div class="tutorial-step" v-if="tutorialStep === 6">
              <h4>Getting Started</h4>
              <div class="tutorial-icon">
                <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round">
                  <polygon points="5 3 19 12 5 21 5 3"></polygon>
                </svg>
              </div>
              <p>To get started with Study Hub:</p>
              <ol>
                <li>Go to the Study Schedule tab</li>
                <li>Click "Create Schedule" to create a manual schedule or "Generate with AI" for an AI-powered schedule</li>
                <li>Add your modules and preferences</li>
                <li>Start tracking your study sessions!</li>
              </ol>
              <p>You can always access this tutorial again by clicking the "What is this?" button in the top right corner.</p>
            </div>
          </div>
          <div class="modal-footer">
            <button
                v-if="tutorialStep > 1"
                @click="tutorialStep--"
                class="tutorial-nav-btn prev-btn"
            >
              Previous
            </button>
            <button
                v-if="tutorialStep < 6"
                @click="tutorialStep++"
                class="tutorial-nav-btn next-btn"
            >
              Next
            </button>
            <button
                v-if="tutorialStep === 6"
                @click="closeTutorial"
                class="tutorial-nav-btn done-btn"
            >
              Get Started
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- CREATE SCHEDULE MODAL -->
    <div v-if="showCreateScheduleModal" class="modal-overlay" @click.self="showCreateScheduleModal = false">
      <div class="modal-container">
        <div class="modal-header">
          <h3>{{ isEditMode ? 'Edit Study Schedule' : 'Create Study Schedule' }}</h3>
          <button @click="showCreateScheduleModal = false" class="close-modal-btn">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>
        <div class="modal-body">
          <div class="schedule-form">
            <div class="form-group">
              <label>Schedule Name</label>
              <input
                  type="text"
                  v-model="scheduleForm.name"
                  placeholder="My Study Schedule"
              />
            </div>

            <div class="form-row">
              <div class="form-group">
                <label>From Date</label>
                <input
                    type="date"
                    v-model="scheduleForm.startDate"
                />
              </div>
              <div class="form-group">
                <label>To Date</label>
                <input
                    type="date"
                    v-model="scheduleForm.endDate"
                />
              </div>
            </div>

            <div class="form-group">
              <label>Preferred Study Times</label>
              <div class="checkbox-grid">
                <label v-for="time in studyTimeOptions" :key="time.value" class="checkbox-label">
                  <input
                      type="checkbox"
                      v-model="scheduleForm.preferredTimes"
                      :value="time.value"
                  />
                  {{ time.label }}
                </label>
              </div>
            </div>

            <div class="form-group">
              <label>Available Days</label>
              <div class="checkbox-grid">
                <label v-for="day in daysOfWeek" :key="day.value" class="checkbox-label">
                  <input
                      type="checkbox"
                      v-model="scheduleForm.availableDays"
                      :value="day.value"
                  />
                  {{ day.label }}
                </label>
              </div>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label>Session Duration</label>
                <select v-model="scheduleForm.sessionDuration">
                  <option value="30">30 minutes</option>
                  <option value="45">45 minutes</option>
                  <option value="60">60 minutes</option>
                  <option value="90">90 minutes</option>
                  <option value="120">2 hours</option>
                </select>
              </div>
              <div class="form-group">
                <label>Break Duration</label>
                <select v-model="scheduleForm.breakDuration">
                  <option value="5">5 minutes</option>
                  <option value="10">10 minutes</option>
                  <option value="15">15 minutes</option>
                  <option value="30">30 minutes</option>
                </select>
              </div>
            </div>

            <div class="form-group">
              <label>Maximum Study Sessions Per Day</label>
              <select v-model="scheduleForm.maxSessionsPerDay">
                <option value="1">1 session</option>
                <option value="2">2 sessions</option>
                <option value="3">3 sessions</option>
                <option value="4">4 sessions</option>
                <option value="5">5 sessions</option>
              </select>
            </div>

            <div class="form-group">
              <label>Modules to Include</label>
              <div v-if="availableModules.length === 0" class="empty-state">
                <p>No modules available. Please add modules in the Dashboard first.</p>
              </div>
              <div v-else class="module-selection">
                <label v-for="module in availableModules" :key="module.id" class="checkbox-label">
                  <input
                      type="checkbox"
                      v-model="scheduleForm.modules"
                      :value="module.id"
                  />
                  {{ module.name }} ({{ module.code }})
                </label>
              </div>
            </div>

            <div v-if="isEditMode" class="form-group">
              <label class="checkbox-label">
                <input
                    type="checkbox"
                    v-model="scheduleForm.isActive"
                />
                Set as active schedule
              </label>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button @click="showCreateScheduleModal = false" class="cancel-btn">Cancel</button>
          <button @click="saveSchedule" class="create-btn">
            {{ isEditMode ? 'Save Changes' : 'Create Schedule' }}
          </button>
        </div>
      </div>
    </div>

    <!-- AI SCHEDULE GENERATOR MODAL -->
    <div v-if="showAIScheduleModal" class="modal-overlay" @click.self="showAIScheduleModal = false">
      <div class="modal-container">
        <div class="modal-header">
          <h3>Generate AI Study Schedule</h3>
          <button @click="showAIScheduleModal = false" class="close-modal-btn">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>
        <div class="modal-body">
          <div class="ai-schedule-form">
            <div class="form-row">
              <div class="form-group">
                <label>From Date</label>
                <input
                    type="date"
                    v-model="scheduleForm.startDate"
                />
              </div>
              <div class="form-group">
                <label>To Date</label>
                <input
                    type="date"
                    v-model="scheduleForm.endDate"
                />
              </div>
            </div>

            <div class="form-group">
              <label>Preferred Study Times</label>
              <div class="checkbox-grid">
                <label v-for="time in studyTimeOptions" :key="time.value" class="checkbox-label">
                  <input
                      type="checkbox"
                      v-model="scheduleForm.preferredTimes"
                      :value="time.value"
                  />
                  {{ time.label }}
                </label>
              </div>
            </div>

            <div class="form-group">
              <label>Available Days</label>
              <div class="checkbox-grid">
                <label v-for="day in daysOfWeek" :key="day.value" class="checkbox-label">
                  <input
                      type="checkbox"
                      v-model="scheduleForm.availableDays"
                      :value="day.value"
                  />
                  {{ day.label }}
                </label>
              </div>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label>Session Duration</label>
                <select v-model="scheduleForm.sessionDuration">
                  <option value="30">30 minutes</option>
                  <option value="45">45 minutes</option>
                  <option value="60">60 minutes</option>
                  <option value="90">90 minutes</option>
                  <option value="120">2 hours</option>
                </select>
              </div>
              <div class="form-group">
                <label>Break Duration</label>
                <select v-model="scheduleForm.breakDuration">
                  <option value="5">5 minutes</option>
                  <option value="10">10 minutes</option>
                  <option value="15">15 minutes</option>
                  <option value="30">30 minutes</option>
                </select>
              </div>
            </div>

            <div class="form-group">
              <label>Maximum Study Sessions Per Day</label>
              <select v-model="scheduleForm.maxSessionsPerDay">
                <option value="1">1 session</option>
                <option value="2">2 sessions</option>
                <option value="3">3 sessions</option>
                <option value="4">4 sessions</option>
                <option value="5">5 sessions</option>
              </select>
            </div>

            <div class="form-group">
              <label>Modules to Include</label>
              <div v-if="availableModules.length === 0" class="empty-state">
                <p>No modules available. Please add modules in the Dashboard first.</p>
              </div>
              <div v-else class="module-selection">
                <label v-for="module in availableModules" :key="module.id" class="checkbox-label">
                  <input
                      type="checkbox"
                      v-model="scheduleForm.modules"
                      :value="module.id"
                  />
                  {{ module.name }} ({{ module.code }})
                </label>
              </div>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button @click="showAIScheduleModal = false" class="cancel-btn">Cancel</button>
          <button @click="generateAISchedule" class="ai-generate-btn">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path>
              <polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline>
              <line x1="12" y1="22.08" x2="12" y2="12"></line>
            </svg>
            Generate Schedule
          </button>
        </div>
      </div>
    </div>

    <!-- EVENT DETAILS MODAL -->
    <div v-if="showEventDetails" class="modal-overlay" @click.self="closeEventDetails">
      <div class="modal-container event-modal">
        <div class="modal-header">
          <h3>Study Session Details</h3>
          <button @click="closeEventDetails" class="close-modal-btn">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>
        <div class="modal-body">
          <div class="event-details">
            <div class="event-header" :class="getEventClass(selectedEvent)">
              <h4>{{ selectedEvent?.title }}</h4>
              <span class="event-module-badge">{{ getModuleName(selectedEvent?.module) }}</span>
            </div>

            <div class="event-info">
              <div class="event-info-item">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                  <line x1="16" y1="2" x2="16" y2="6"></line>
                  <line x1="8" y1="2" x2="8" y2="6"></line>
                  <line x1="3" y1="10" x2="21" y2="10"></line>
                </svg>
                <span>{{ formatEventDate(selectedEvent) }}</span>
              </div>

              <div class="event-info-item">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <circle cx="12" cy="12" r="10"></circle>
                  <polyline points="12 6 12 12 16 14"></polyline>
                </svg>
                <span>{{ formatEventTime(selectedEvent) }}</span>
              </div>

              <div class="event-description">
                <h5>Description</h5>
                <p>{{ selectedEvent?.description || 'No description provided.' }}</p>
              </div>

              <div class="event-topics">
                <h5>Topics</h5>
                <div class="topic-tags">
                  <span v-for="(topic, index) in selectedEvent?.topics" :key="index" class="topic-tag">
                    {{ topic }}
                  </span>
                  <span v-if="!selectedEvent?.topics || selectedEvent?.topics.length === 0" class="no-topics">
                    No specific topics
                  </span>
                </div>
              </div>

              <div class="event-status">
                <h5>Status</h5>
                <div class="status-badge" :class="getStatusClass(selectedEvent?.status)">
                  {{ formatStatus(selectedEvent?.status) }}
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <div v-if="!selectedEvent?.completed && selectedEvent?.status === 'planned'" class="session-actions">
            <button @click="startSession(selectedEvent)" class="start-session-btn">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polygon points="5 3 19 12 5 21 5 3"></polygon>
              </svg>
              Start Session
            </button>
            <button @click="rescheduleSession(selectedEvent)" class="reschedule-btn">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="10"></circle>
                <path d="M12 6v6l4 2"></path>
              </svg>
              Reschedule
            </button>
          </div>

          <div v-if="selectedEvent?.status === 'in_progress'" class="session-actions">
            <button @click="completeSession(selectedEvent)" class="complete-session-btn">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                <polyline points="22 4 12 14.01 9 11.01"></polyline>
              </svg>
              Complete Session
            </button>
          </div>

          <div v-if="selectedEvent?.status === 'completed'" class="session-feedback">
            <div class="feedback-item">
              <span>Productivity Rating:</span>
              <div class="rating-stars">
                <span v-for="i in 5" :key="i" class="star" :class="{ 'filled': i <= (selectedEvent?.productivity || 0) }">★</span>
              </div>
            </div>
            <div class="feedback-item">
              <span>Difficulty Rating:</span>
              <div class="rating-stars">
                <span v-for="i in 5" :key="i" class="star" :class="{ 'filled': i <= (selectedEvent?.difficulty || 0) }">★</span>
              </div>
            </div>
            <div class="xp-earned">
              <span>XP Earned:</span>
              <span class="xp-value">+{{ selectedEvent?.xpEarned || 0 }} XP</span>
            </div>
          </div>

          <button @click="closeEventDetails" class="close-btn">Close</button>
        </div>
      </div>
    </div>

    <!-- SESSION COMPLETION MODAL -->
    <div v-if="showCompletionModal" class="modal-overlay" @click.self="showCompletionModal = false">
      <div class="modal-container completion-modal">
        <div class="modal-header">
          <h3>Session Feedback</h3>
          <button @click="showCompletionModal = false" class="close-modal-btn">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>
        <div class="modal-body">
          <div class="feedback-form">
            <div class="form-group">
              <label>Productivity Rating</label>
              <div class="rating-input">
                <span
                    v-for="i in 5"
                    :key="i"
                    class="rating-star"
                    :class="{ 'selected': feedbackForm.productivity >= i }"
                    @click="feedbackForm.productivity = i"
                >★</span>
              </div>
            </div>

            <div class="form-group">
              <label>Difficulty Level</label>
              <div class="rating-input">
                <span
                    v-for="i in 5"
                    :key="i"
                    class="rating-star"
                    :class="{ 'selected': feedbackForm.difficulty >= i }"
                    @click="feedbackForm.difficulty = i"
                >★</span>
              </div>
            </div>

            <div class="form-group">
              <label>Session Notes</label>
              <textarea
                  v-model="feedbackForm.notes"
                  placeholder="What did you learn? Any challenges or observations?"
                  rows="4"
              ></textarea>
            </div>

            <div class="form-group">
              <label>Topics Covered</label>
              <div class="topic-input-container">
                <input
                    type="text"
                    v-model="newTopic"
                    @keyup.enter="addTopic"
                    placeholder="Add topic and press Enter"
                />
                <button @click="addTopic" class="add-topic-btn">Add</button>
              </div>
              <div class="topic-tags">
                <span v-for="(topic, index) in feedbackForm.topics" :key="index" class="topic-tag">
                  {{ topic }}
                  <button @click="removeTopic(index)" class="remove-topic-btn">×</button>
                </span>
              </div>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button @click="showCompletionModal = false" class="cancel-btn">Cancel</button>
          <button @click="submitFeedback" class="submit-btn">Complete Session</button>
        </div>
      </div>
    </div>

    <!-- ADD TO CALENDAR CONFIRMATION MODAL -->
    <div v-if="showCalendarModal" class="modal-overlay" @click.self="showCalendarModal = false">
      <div class="modal-container calendar-confirm-modal">
        <div class="modal-header">
          <h3>Add to Calendar</h3>
          <button @click="showCalendarModal = false" class="close-modal-btn">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>
        <div class="modal-body">
          <div class="confirmation-message">
            <div class="confirmation-icon">
              <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round">
                <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                <line x1="16" y1="2" x2="16" y2="6"></line>
                <line x1="8" y1="2" x2="8" y2="6"></line>
                <line x1="3" y1="10" x2="21" y2="10"></line>
                <line x1="12" y1="15" x2="12" y2="19"></line>
                <line x1="10" y1="17" x2="14" y2="17"></line>
              </svg>
            </div>
            <p>You're about to add <strong>{{ selectedSchedule?.name }}</strong> to your calendar.</p>
            <p>This will create {{ studySessionCount }} study session events from {{ formatDate(selectedSchedule?.start_date) }} to {{ formatDate(selectedSchedule?.end_date) }}.</p>
            <p>All events will be marked as <strong>Study Session</strong> type.</p>
            <p class="confirmation-note">Note: This action cannot be undone. You can delete individual events later if needed.</p>
          </div>
        </div>
        <div class="modal-footer">
          <button @click="showCalendarModal = false" class="cancel-btn">Cancel</button>
          <button @click="addToCalendar" class="confirm-btn">Add to Calendar</button>
        </div>
      </div>
    </div>

    <!-- DELETE SCHEDULE CONFIRMATION MODAL -->
    <div v-if="showDeleteModal" class="modal-overlay" @click.self="showDeleteModal = false">
      <div class="modal-container delete-confirm-modal">
        <div class="modal-header">
          <h3>Delete Schedule</h3>
          <button @click="showDeleteModal = false" class="close-modal-btn">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>
        <div class="modal-body">
          <div class="confirmation-message">
            <div class="confirmation-icon delete-icon">
              <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="3 6 5 6 21 6"></polyline>
                <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                <line x1="10" y1="11" x2="10" y2="17"></line>
                <line x1="14" y1="11" x2="14" y2="17"></line>
              </svg>
            </div>
            <p>Are you sure you want to delete <strong>{{ selectedSchedule?.name }}</strong>?</p>
            <p>This will permanently remove this schedule and all its associated study sessions.</p>
            <p v-if="selectedSchedule?.events_created" class="warning-text">Note: Calendar events created from this schedule will not be automatically deleted.</p>
            <p class="confirmation-note">This action cannot be undone.</p>
          </div>
        </div>
        <div class="modal-footer">
          <button @click="showDeleteModal = false" class="cancel-btn">Cancel</button>
          <button @click="deleteSchedule" class="delete-confirm-btn">Delete Schedule</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { getDarkModePreference } from "@/services/darkModeService.js";
import { userSettingsService } from '@/services/userSettingsService.js';
import DashboardNavBar from "@/components/DashboardNavBar.vue";
import ModuleTimeDistributionChart from "@/components/charts/ModuleTimeDistributionChart.vue";
import StudySessionsTimelineChart from "@/components/charts/StudySessionsTimelineChart.vue";
import ProductivityPatternsChart from "@/components/charts/ProductivityPatternsChart.vue";
import CalendarSideBar from "@/components/CalendarSideBar.vue"; // Import the sidebar component
import { notify } from "@/services/toastService.js";
import axios from 'axios';
import { API_URL } from "@/config.js";

export default {
  name: "StudyHub",
  components: {
    DashboardNavBar,
    ModuleTimeDistributionChart,
    StudySessionsTimelineChart,
    ProductivityPatternsChart,
    CalendarSideBar // Add the sidebar component
  },
  data() {
    return {
      darkMode: false,
      isMobile: false,
      activeTab: 'schedule',
      calendarView: 'month',
      isLoading: false,
      error: null,

      // Sidebar control
      showSidebar: true,
      sidebarCollapsed: false,

      // User settings
      userSettings: {
        appearance: {
          accentColor: 'purple',
          fontSize: 'medium',
          highContrast: false,
          enableAnimations: true
        },
        calendar: {
          firstDayOfWeek: 'sunday',
          timeFormat: '12h',
          dateFormat: 'MM/DD/YYYY',
          showWeekNumbers: false,
          defaultView: 'month',
          showCompleted: true,
          highlightToday: true
        },
        accessibility: {
          screenReaderOptimized: false,
          reduceMotion: false,
          colorBlindMode: 'none',
          keyboardShortcuts: true,
          focusMode: false
        }
      },

      // Tutorial state
      showTutorial: false,
      tutorialStep: 1,

      // Current date and selection
      currentDate: new Date(),
      selectedDate: new Date(),

      // Schedule Selection Modal
      showScheduleSelectionModal: false,

      // User data states
      userProfile: {
        firstName: "",
        lastName: "",
        email: "",
        avatar: null,
        university: "",
        degree: "",
        role: "Student",
        academicLevel: "",
        enrollmentType: "",
        currentYear: null
      },

      // Available modules for study
      availableModules: [],
      enrolledModules: [],

      // User's study preferences
      studyPreferences: {
        preferredTimes: [],
        sessionDuration: 60,
        availableDays: [],
        breakDuration: 15,
        maxSessionsPerDay: 3
      },

      // Schedule edit/create related states
      isEditMode: false,
      editingScheduleId: null,

      // Schedule creation form
      scheduleForm: {
        name: 'My Study Schedule',
        startDate: '',
        endDate: '',
        preferredTimes: ['afternoon', 'evening'],
        availableDays: ['monday', 'tuesday', 'wednesday', 'friday'],
        sessionDuration: 60,
        breakDuration: 15,
        maxSessionsPerDay: 3,
        modules: [],
        isActive: true
      },

      // Study session feedback form
      feedbackForm: {
        productivity: 3,
        difficulty: 3,
        notes: '',
        topics: []
      },
      newTopic: '',

      // Study data
      schedules: [],
      activeSchedule: null,
      studySessions: [],
      aiTips: [],
      studyStats: {},
      studyStreak: {},
      recentDays: [],
      achievements: [],
      moduleStudyStats: [],
      moduleTimeDistribution: {
        labels: [],
        datasets: [{
          data: [],
          backgroundColor: []
        }]
      },
      sessionsTimeline: {
        labels: [],
        datasets: [{
          label: 'Study Sessions',
          data: [],
          borderColor: '#9e78ff',
          backgroundColor: 'rgba(158, 120, 255, 0.2)',
          tension: 0.4
        }]
      },
      productivityPatterns: {
        labels: [],
        datasets: [{
          label: 'Productivity',
          data: [],
          backgroundColor: '#9e78ff'
        }]
      },

      // Weekdays for the calendar
      weekdays: ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
      weekDays: [],
      displayHours: Array.from({ length: 14 }, (_, i) => i + 8), // 8am to 9pm

      // Modal visibility controls
      showCreateScheduleModal: false,
      showAIScheduleModal: false,
      showEventDetails: false,
      showCompletionModal: false,
      showCalendarModal: false,
      showDeleteModal: false,

      // Currently selected items
      selectedEvent: null,
      selectedSchedule: null,
      studySessionCount: 0,

      // Achievement categories
      achievementCategories: [
        { value: 'all', label: 'All' },
        { value: 'consistency', label: 'Consistency' },
        { value: 'time', label: 'Time Management' },
        { value: 'mastery', label: 'Mastery' }
      ],
      selectedAchievementCategory: 'all',

      // Time indicator interval
      timeIndicatorInterval: null
    };
  },

  computed: {
    // Format weekdays list based on first day of week setting
    formattedWeekdays() {
      if (this.userSettings.calendar.firstDayOfWeek === 'monday') {
        return ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
      }
      return ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
    },

    // Check if we have any analytics data to display
    hasAnalyticsData() {
      return this.studySessions.length > 0 && this.studySessions.some(s => s.completed);
    },

    // Days for the month view
    monthDays() {
      const year = this.currentDate.getFullYear();
      const month = this.currentDate.getMonth();

      // First day of current month
      const firstDay = new Date(year, month, 1);

      // Adjust for first day of week setting
      let firstDayOfWeek = firstDay.getDay(); // 0 for Sunday
      if (this.userSettings.calendar.firstDayOfWeek === 'monday') {
        firstDayOfWeek = firstDayOfWeek === 0 ? 6 : firstDayOfWeek - 1; // Adjust for Monday start (0=Mon, 6=Sun)
      }

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

      // Add days from next month to complete the grid
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

    // Get filtered achievements based on selected category
    filteredAchievements() {
      if (this.selectedAchievementCategory === 'all') {
        return this.achievements;
      }
      return this.achievements.filter(achievement =>
          achievement.category === this.selectedAchievementCategory
      );
    },

    // Study time options
    studyTimeOptions() {
      return [
        { value: 'morning', label: 'Morning (6am-12pm)' },
        { value: 'afternoon', label: 'Afternoon (12pm-5pm)' },
        { value: 'evening', label: 'Evening (5pm-9pm)' },
        { value: 'night', label: 'Night (9pm-11pm)' }
      ];
    },

    // Days of week
    daysOfWeek() {
      return [
        { value: 'monday', label: 'Monday' },
        { value: 'tuesday', label: 'Tuesday' },
        { value: 'wednesday', label: 'Wednesday' },
        { value: 'thursday', label: 'Thursday' },
        { value: 'friday', label: 'Friday' },
        { value: 'saturday', label: 'Saturday' },
        { value: 'sunday', label: 'Sunday' }
      ];
    }
  },

  watch: {
    // Watch for changes to the selectedDate to sync with sidebar
    selectedDate(newDate, oldDate) {
      // Sync with sidebar if dates are different
      if (newDate.toDateString() !== (oldDate && oldDate.toDateString())) {
        // The sidebar will be updated through the selectedDate prop
        // Refresh events for the selected date
        this.fetchEventsForDate(newDate);
      }
    }
  },

  mounted() {
    // Initialize dates in schedule form
    this.scheduleForm.startDate = this.formatDateISO(new Date());
    this.scheduleForm.endDate = this.formatDateISO(this.getDatePlusDays(new Date(), 7));

    // Load all user settings
    this.loadUserSettings();

    // Get dark mode preference (directly handled for initial render)
    this.darkMode = getDarkModePreference();
    this.checkMobile();

    // Initialize calendar data based on settings
    this.initializeCalendarView();
    this.generateWeekDays();

    // Set up event listeners
    this.setupEventListeners();

    // Set up the current time updater for the calendar
    this.startCurrentTimeUpdates();

    // Fetch initial data
    this.fetchData();

    // Load sidebar preferences from localStorage
    this.loadSidebarPreferences();
  },

  beforeUnmount() {
    // Clean up event listeners
    this.removeEventListeners();

    // Clear time updater interval
    if (this.timeIndicatorInterval) {
      clearInterval(this.timeIndicatorInterval);
    }
  },

  methods: {
    // New methods for sidebar integration
    toggleSidebar() {
      this.showSidebar = !this.showSidebar;
      // Save preference to localStorage
      localStorage.setItem('studyHubShowSidebar', this.showSidebar);
    },

    handleSidebarCollapse(isCollapsed) {
      this.sidebarCollapsed = isCollapsed;
    },

    loadSidebarPreferences() {
      // Load sidebar visibility preference
      const sidebarVisible = localStorage.getItem('studyHubShowSidebar');
      if (sidebarVisible !== null) {
        this.showSidebar = sidebarVisible === 'true';
      } else {
        // Default to true for desktop, false for mobile
        this.showSidebar = !this.isMobile;
      }

      // Load sidebar collapsed state
      const sidebarCollapsed = localStorage.getItem('studyHubSidebarCollapsed');
      if (sidebarCollapsed !== null) {
        this.sidebarCollapsed = sidebarCollapsed === 'true';
      }
    },

    navigateToTab(tabName) {
      if (['schedule', 'analytics', 'achievements', 'profile'].includes(tabName)) {
        this.activeTab = tabName;
      }
    },

    showScheduleSelectionModal() {
      // Show modal to select active schedule
      this.showCreateScheduleModal = true;
    },

    toggleEventCompletion(event) {
      // Handle toggling event completion status
      try {
        const updatedEvent = { ...event, completed: !event.completed };

        // Call your API to update the event
        axios.put(
            `${API_URL}/calendar/events/${event.id}`,
            updatedEvent,
            { withCredentials: true }
        ).then(() => {
          // Update the event in local state
          const index = this.studySessions.findIndex(e => e.id === event.id);
          if (index !== -1) {
            this.studySessions[index].completed = !event.completed;
          }

          notify({
            type: 'success',
            message: updatedEvent.completed ? 'Event marked as completed!' : 'Event marked as incomplete!'
          });
        }).catch(error => {
          console.error('Error updating event:', error);
          notify({
            type: 'error',
            message: 'Failed to update event status'
          });
        });
      } catch (error) {
        console.error('Error toggling event completion:', error);
      }
    },

    openCreateEventModal(type = 'general') {
      // Handle opening create event modal
      this.isEditMode = false;
      this.eventToEdit = null;

      // Set default values for new event
      const defaultEvent = {
        title: '',
        description: '',
        date: this.formatDateISO(this.selectedDate),
        type: type || 'general',
        all_day: type !== 'study',
        start_time: '09:00',
        end_time: '10:00',
        color: '#7b49ff',
        completed: false
      };

      // Open event details with default data
      this.selectedEvent = defaultEvent;
      this.showEventDetails = true;
    },

    openEditEventModal(event) {
      // Handle opening edit event modal
      this.isEditMode = true;
      this.eventToEdit = event;
      this.selectedEvent = { ...event };
      this.showEventDetails = true;
    },

    // New helper method to fetch events for a specific date
    fetchEventsForDate(date) {
      const dateStr = this.formatDateISO(date);
      // Only fetch if we're in schedule tab
      if (this.activeTab === 'schedule') {
        // You can implement more specific fetching logic here if needed
        this.fetchSessions();
      }
    },

    // Settings management methods
    loadUserSettings() {
      try {
        // Get settings from the service
        const settings = userSettingsService.getUserSettings();

        if (settings) {
          // Merge received settings with defaults
          if (settings.appearance) {
            this.userSettings.appearance = { ...this.userSettings.appearance, ...settings.appearance };
          }
          if (settings.calendar) {
            this.userSettings.calendar = { ...this.userSettings.calendar, ...settings.calendar };
          }
          if (settings.accessibility) {
            this.userSettings.accessibility = { ...this.userSettings.accessibility, ...settings.accessibility };
          }
          if (settings.academic) {
            // Cache academic settings for profile display
            this.userProfile.academicLevel = settings.academic.academicLevel || this.userProfile.academicLevel;
            this.userProfile.enrollmentType = settings.academic.enrollmentType || this.userProfile.enrollmentType;
            this.userProfile.currentYear = settings.academic.currentYear || this.userProfile.currentYear;
          }
        }

        // Apply all settings
        this.applySettings();
      } catch (error) {
        console.error("Error loading user settings:", error);
        // Continue with defaults if settings can't be loaded
      }
    },

    applySettings() {
      // Apply dark mode
      document.documentElement.classList.toggle('dark-mode', this.darkMode);

      // Apply accent color
      this.applyAccentColor(this.userSettings.appearance.accentColor);

      // Apply font size
      this.applyFontSize(this.userSettings.appearance.fontSize);

      // Apply high contrast if enabled
      document.documentElement.classList.toggle('high-contrast', this.userSettings.appearance.highContrast);

      // Apply animations settings
      document.documentElement.classList.toggle('disable-animations', !this.userSettings.appearance.enableAnimations);

      // Apply accessibility settings
      this.applyAccessibilitySettings();

      // Apply calendar settings
      this.applyCalendarSettings();
    },

    applyAccentColor(colorId) {
      // Lookup the actual color value
      const accentColors = [
        { id: 'purple', value: '#7b49ff' },
        { id: 'blue', value: '#2196f3' },
        { id: 'green', value: '#4caf50' },
        { id: 'red', value: '#f44336' },
        { id: 'orange', value: '#ff9800' },
        { id: 'pink', value: '#e91e63' },
        { id: 'teal', value: '#009688' }
      ];

      const color = accentColors.find(c => c.id === colorId);
      if (color) {
        // Set primary color CSS variables
        document.documentElement.style.setProperty('--primary-color', color.value);

        // Calculate darker variant for hover states
        const darkerColor = this.adjustColor(color.value, -20);
        document.documentElement.style.setProperty('--primary-dark', darkerColor);

        // Calculate lighter variant
        const lighterColor = this.adjustColor(color.value, 20);
        document.documentElement.style.setProperty('--primary-light', lighterColor);

        // Set RGB values for transparency
        const rgb = this.hexToRgb(color.value);
        if (rgb) {
          document.documentElement.style.setProperty('--primary-color-rgb', `${rgb.r}, ${rgb.g}, ${rgb.b}`);
        }
      }
    },

    // Helper to convert hex to RGB
    hexToRgb(hex) {
      // Remove # if present
      hex = hex.replace(/^#/, '');

      // Parse hex values
      const bigint = parseInt(hex, 16);
      const r = (bigint >> 16) & 255;
      const g = (bigint >> 8) & 255;
      const b = bigint & 255;

      return { r, g, b };
    },

    adjustColor(hex, amount) {
      // Convert hex to RGB
      let r = parseInt(hex.slice(1, 3), 16);
      let g = parseInt(hex.slice(3, 5), 16);
      let b = parseInt(hex.slice(5, 7), 16);

      // In dark mode, we might want slightly different adjustment logic
      if (this.darkMode && amount < 0) {
        // For dark mode, make darker colors even more distinct
        amount = amount * 1.5;
      } else if (this.darkMode && amount > 0) {
        // For dark mode, make lighter colors more pronounced
        amount = amount * 1.2;
      }

      // Adjust colors
      r = Math.max(0, Math.min(255, r + amount));
      g = Math.max(0, Math.min(255, g + amount));
      b = Math.max(0, Math.min(255, b + amount));

      // Store RGB values as CSS variables for easier alpha adjustments
      const rgbValue = `${Math.round(r)}, ${Math.round(g)}, ${Math.round(b)}`;
      document.documentElement.style.setProperty('--primary-color-rgb', rgbValue);

      // Convert back to hex
      return `#${Math.round(r).toString(16).padStart(2, '0')}${Math.round(g).toString(16).padStart(2, '0')}${Math.round(b).toString(16).padStart(2, '0')}`;
    },

    applyFontSize(size) {
      const sizeMap = {
        'small': '14px',
        'medium': '16px',
        'large': '18px'
      };

      document.documentElement.style.setProperty('--font-size-base', sizeMap[size] || '16px');
    },

    applyAccessibilitySettings() {
      // Apply screen reader optimization if enabled
      document.documentElement.classList.toggle('sr-optimized', this.userSettings.accessibility.screenReaderOptimized);

      // Apply reduce motion if enabled
      document.documentElement.classList.toggle('reduce-motion', this.userSettings.accessibility.reduceMotion);

      // Apply focus mode if enabled
      document.documentElement.classList.toggle('focus-mode', this.userSettings.accessibility.focusMode);

      // Apply color blind mode if enabled
      this.applyColorBlindMode();
    },

    applyColorBlindMode() {
      // Remove any existing filters
      const existingFilter = document.getElementById('color-blind-filter');
      if (existingFilter) {
        existingFilter.remove();
      }

      // If no color blind mode selected, we're done
      if (this.userSettings.accessibility.colorBlindMode === 'none') {
        document.documentElement.style.filter = '';
        return;
      }

      // Create SVG filter element
      const svgFilter = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
      svgFilter.setAttribute('id', 'color-blind-filter');
      svgFilter.style.position = 'absolute';
      svgFilter.style.height = '0';
      svgFilter.style.width = '0';
      svgFilter.style.overflow = 'hidden';

      // Add filter definitions based on selected mode
      let filterContent = '';

      switch (this.userSettings.accessibility.colorBlindMode) {
        case 'protanopia':
          // Red-blind
          filterContent = `
            <filter id="protanopia">
              <feColorMatrix
                type="matrix"
                values="0.567, 0.433, 0,     0, 0
                        0.558, 0.442, 0,     0, 0
                        0,     0.242, 0.758, 0, 0
                        0,     0,     0,     1, 0"/>
            </filter>
          `;
          break;
        case 'deuteranopia':
          // Green-blind
          filterContent = `
            <filter id="deuteranopia">
              <feColorMatrix
                type="matrix"
                values="0.625, 0.375, 0,   0, 0
                        0.7,   0.3,   0,   0, 0
                        0,     0.3,   0.7, 0, 0
                        0,     0,     0,   1, 0"/>
            </filter>
          `;
          break;
        case 'tritanopia':
          // Blue-blind
          filterContent = `
            <filter id="tritanopia">
              <feColorMatrix
                type="matrix"
                values="0.95, 0.05,  0,     0, 0
                        0,    0.433, 0.567, 0, 0
                        0,    0.475, 0.525, 0, 0
                        0,    0,     0,     1, 0"/>
            </filter>
          `;
          break;
        case 'achromatopsia':
          // Monochrome
          filterContent = `
            <filter id="achromatopsia">
              <feColorMatrix
                type="matrix"
                values="0.299, 0.587, 0.114, 0, 0
                        0.299, 0.587, 0.114, 0, 0
                        0.299, 0.587, 0.114, 0, 0
                        0,     0,     0,     1, 0"/>
            </filter>
          `;
          break;
      }

      svgFilter.innerHTML = filterContent;
      document.body.appendChild(svgFilter);

      // Apply filter to the entire document
      document.documentElement.style.filter = `url(#${this.userSettings.accessibility.colorBlindMode})`;
    },

    applyCalendarSettings() {
      // Apply calendar view setting
      if (this.userSettings.calendar.defaultView) {
        // Only set on initial load, not during view changes
        if (this.calendarView === 'month') {
          this.calendarView = this.userSettings.calendar.defaultView;
        }
      }

      // Regenerate weekdays based on first day of week setting
      this.weekdays = this.formattedWeekdays;

      // Re-generate week days for current view
      this.generateWeekDays();
    },

    // Event listeners setup
    setupEventListeners() {
      window.addEventListener("resize", this.checkMobile);
      window.addEventListener('darkModeChange', this.onDarkModeChange);

      // Listen for settings changes
      window.addEventListener('fontSizeChanged', this.onFontSizeChanged);
      window.addEventListener('highContrastChanged', this.onHighContrastChanged);
      window.addEventListener('animationsChanged', this.onAnimationsChanged);
      window.addEventListener('colorBlindModeChanged', this.onColorBlindModeChanged);
      window.addEventListener('reduceMotionChanged', this.onReduceMotionChanged);
      window.addEventListener('calendarSettingsChanged', this.onCalendarSettingsChanged);
      window.addEventListener('focusModeChanged', this.onFocusModeChanged);
      window.addEventListener('yearSettingsUpdated', this.onYearSettingsUpdated);
    },

    removeEventListeners() {
      window.removeEventListener("resize", this.checkMobile);
      window.removeEventListener('darkModeChange', this.onDarkModeChange);

      // Remove settings change listeners
      window.removeEventListener('fontSizeChanged', this.onFontSizeChanged);
      window.removeEventListener('highContrastChanged', this.onHighContrastChanged);
      window.removeEventListener('animationsChanged', this.onAnimationsChanged);
      window.removeEventListener('colorBlindModeChanged', this.onColorBlindModeChanged);
      window.removeEventListener('reduceMotionChanged', this.onReduceMotionChanged);
      window.removeEventListener('calendarSettingsChanged', this.onCalendarSettingsChanged);
      window.removeEventListener('focusModeChanged', this.onFocusModeChanged);
      window.removeEventListener('yearSettingsUpdated', this.onYearSettingsUpdated);
    },

    // Check for mobile screen size
    checkMobile() {
      this.isMobile = window.innerWidth <= 768;

      // Adjust sidebar visibility based on screen size
      if (this.isMobile && localStorage.getItem('studyHubShowSidebar') === null) {
        // Default to hidden on mobile if no user preference is set
        this.showSidebar = false;
      }
    },

    // Settings change event handlers
    onDarkModeChange(event) {
      this.darkMode = event.detail.isDark;

      // When dark mode changes, reapply the accent color
      this.$nextTick(() => {
        this.applyAccentColor(this.userSettings.appearance.accentColor);
        // Reapply color blind adjustments if needed
        if (this.userSettings.accessibility.colorBlindMode !== 'none') {
          this.applyColorBlindMode();
        }
      });
    },

    onFontSizeChanged(event) {
      this.userSettings.appearance.fontSize = event.detail.size;
      this.applyFontSize(event.detail.size);
    },

    onHighContrastChanged(event) {
      this.userSettings.appearance.highContrast = event.detail.enabled;
      document.documentElement.classList.toggle('high-contrast', event.detail.enabled);
    },

    onAnimationsChanged(event) {
      this.userSettings.appearance.enableAnimations = event.detail.enabled;
      document.documentElement.classList.toggle('disable-animations', !event.detail.enabled);
    },

    onColorBlindModeChanged(event) {
      this.userSettings.accessibility.colorBlindMode = event.detail.mode;
      this.applyColorBlindMode();
    },

    onReduceMotionChanged(event) {
      this.userSettings.accessibility.reduceMotion = event.detail.enabled;
      document.documentElement.classList.toggle('reduce-motion', event.detail.enabled);
    },

    onCalendarSettingsChanged(event) {
      const calendarSettings = event.detail;

      // Update local settings
      this.userSettings.calendar = {
        ...this.userSettings.calendar,
        ...calendarSettings
      };

      // Apply calendar settings
      this.applyCalendarSettings();

      // Refresh calendar data if needed
      this.fetchSessions();
    },

    onFocusModeChanged(event) {
      this.userSettings.accessibility.focusMode = event.detail.enabled;
      document.documentElement.classList.toggle('focus-mode', event.detail.enabled);
    },

    onYearSettingsUpdated(event) {
      // Update academic year settings if needed
      if (event.detail.yearWeights) {
        this.$nextTick(() => {
          // Refresh profile data
          this.fetchUserProfile();
        });
      }
    },

    // Initialize calendar view based on settings
    initializeCalendarView() {
      // Set initial calendar view based on settings
      if (this.userSettings.calendar.defaultView) {
        this.calendarView = this.userSettings.calendar.defaultView;
      }
    },

    // Fetch all data from API
    async fetchData() {
      try {
        this.isLoading = true;
        this.error = null;

        // Fetch user profile
        await this.fetchUserProfile();

        // Fetch user modules
        await this.fetchEnrolledModules();

        // Fetch user schedules and sessions
        await this.fetchSchedules();
        await this.fetchSessions();

        // Fetch study analytics
        await this.fetchAnalytics();

        // Fetch achievements and streaks
        await this.fetchAchievements();
        await this.fetchStudyStreak();

        // Fetch AI tips
        await this.fetchAITips();

        // Check if this is the first time using Study Hub
        this.checkFirstTimeUser();

      } catch (error) {
        console.error("Error fetching data:", error);
        this.error = "Failed to load data. Please try again.";
      } finally {
        this.isLoading = false;
      }
    },

    // Handle logout event from the navbar
    handleLogout() {
      // Call logout API endpoint
      axios.post(`${API_URL}/logout`, {}, { withCredentials: true })
          .then(() => {
            // Redirect to login page
            window.location.href = '/login';
          })
          .catch(error => {
            console.error('Logout error:', error);
            notify({
              type: "error",
              message: "Failed to logout. Please try again."
            });
          });
    },

    // Generate week days for week view
    generateWeekDays() {
      // Get start of week based on settings
      const startOfWeek = this.getStartOfWeek(this.currentDate, this.userSettings.calendar.firstDayOfWeek);
      const days = [];

      for (let i = 0; i < 7; i++) {
        const date = new Date(startOfWeek);
        date.setDate(startOfWeek.getDate() + i);
        days.push({ date });
      }

      this.weekDays = days;
    },

    // Start current time indicator updates
    startCurrentTimeUpdates() {
      // Update current time indicator position every minute
      this.timeIndicatorInterval = setInterval(() => {
        if ((this.calendarView === 'week' || this.calendarView === 'day') &&
            this.isToday(this.calendarView === 'day' ? this.selectedDate : this.currentDate)) {
          this.$forceUpdate();
        }
      }, 60000); // update every minute
    },

    // Calendar navigation methods
    navigatePrevious() {
      const date = new Date(this.currentDate);

      if (this.calendarView === 'month') {
        date.setMonth(date.getMonth() - 1);
      } else if (this.calendarView === 'week') {
        date.setDate(date.getDate() - 7);
      } else if (this.calendarView === 'day') {
        date.setDate(date.getDate() - 1);
      }

      this.currentDate = date;
      this.generateWeekDays();

      // Fetch new sessions for the current view
      this.fetchSessions();
    },

    navigateNext() {
      const date = new Date(this.currentDate);

      if (this.calendarView === 'month') {
        date.setMonth(date.getMonth() + 1);
      } else if (this.calendarView === 'week') {
        date.setDate(date.getDate() + 7);
      } else if (this.calendarView === 'day') {
        date.setDate(date.getDate() + 1);
      }

      this.currentDate = date;
      this.generateWeekDays();

      // Fetch new sessions for the current view
      this.fetchSessions();
    },

    navigateToday() {
      this.currentDate = new Date();
      this.selectedDate = new Date();
      this.generateWeekDays();

      // Fetch sessions for current view
      this.fetchSessions();
    },

    // Date selection
    selectDate(date) {
      this.selectedDate = new Date(date);

      if (this.calendarView === 'month') {
        // Update current month if selected date is in a different month
        const currentMonth = this.currentDate.getMonth();
        const selectedMonth = this.selectedDate.getMonth();

        if (currentMonth !== selectedMonth) {
          this.currentDate = new Date(this.selectedDate);
          this.generateWeekDays();
          this.fetchSessions();
        }
      }

      // If day view, update the current date
      if (this.calendarView === 'day') {
        this.currentDate = new Date(this.selectedDate);
        this.generateWeekDays();
      }
    },

    // API Methods
    async fetchUserProfile() {
      try {
        const response = await axios.get(`${API_URL}/user/profile`, {
          withCredentials: true
        });

        if (response.data) {
          this.userProfile = {
            ...this.userProfile,
            ...response.data
          };

          // Keep academic settings consistency if they exist
          const settings = userSettingsService.getSettings();
          if (settings && settings.academic) {
            this.userProfile.academicLevel = settings.academic.academicLevel || this.userProfile.academicLevel;
            this.userProfile.enrollmentType = settings.academic.enrollmentType || this.userProfile.enrollmentType;
            this.userProfile.currentYear = settings.academic.currentYear || this.userProfile.currentYear;
          }
        }
      } catch (error) {
        console.error("Error fetching user profile:", error);
        throw error;
      }
    },

    async fetchEnrolledModules() {
      try {
        const response = await axios.get(`${API_URL}/modules`, {
          withCredentials: true
        });

        if (response.data) {
          this.availableModules = response.data;
          this.enrolledModules = response.data.filter(m => m.isCurrentlyEnrolled || m.status === 'in_progress');

          // Update modules in schedule form
          this.scheduleForm.modules = this.availableModules.map(m => m.id);
        }
      } catch (error) {
        console.error("Error fetching modules:", error);
        throw error;
      }
    },

    async fetchSchedules() {
      try {
        const response = await axios.get(`${API_URL}/study/schedules`, {
          withCredentials: true
        });

        if (response.data) {
          this.schedules = response.data;

          // Find active schedule if any
          this.activeSchedule = this.schedules.find(s => s.is_active) || null;
        }
      } catch (error) {
        console.error("Error fetching schedules:", error);
        throw error;
      }
    },

    async fetchSessions() {
      try {
        // Get date range for the current view
        let startDate, endDate;

        if (this.calendarView === 'month') {
          // Get first and last day of the month
          const year = this.currentDate.getFullYear();
          const month = this.currentDate.getMonth();
          startDate = new Date(year, month, 1);
          endDate = new Date(year, month + 1, 0);
        } else if (this.calendarView === 'week') {
          // Get first and last day of the week
          startDate = this.weekDays[0].date;
          endDate = this.weekDays[6].date;
        } else {
          // Day view - just use the selected date
          startDate = this.selectedDate;
          endDate = this.selectedDate;
        }

        // Query for active schedule sessions
        const params = {
          start_date: this.formatDateISO(startDate),
          end_date: this.formatDateISO(endDate),
          active_only: 'true'  // Only get sessions from active schedule
        };

        const response = await axios.get(`${API_URL}/study/sessions`, {
          params,
          withCredentials: true
        });

        if (response.data) {
          this.studySessions = response.data;
        }
      } catch (error) {
        console.error("Error fetching sessions:", error);
        throw error;
      }
    },

    async fetchAnalytics() {
      try {
        const response = await axios.get(`${API_URL}/study/analytics`, {
          withCredentials: true
        });

        if (response.data) {
          this.studyStats = response.data.studyStats || {};
          this.moduleStudyStats = response.data.moduleStudyStats || [];

          // Apply accent color to charts
          const accentColor = getComputedStyle(document.documentElement).getPropertyValue('--primary-color').trim();
          const accentLightColor = getComputedStyle(document.documentElement).getPropertyValue('--primary-light').trim();

          // Update chart colors based on theme
          this.moduleTimeDistribution = response.data.moduleTimeDistribution || {
            labels: [],
            datasets: [{
              data: [],
              backgroundColor: []
            }]
          };

          this.sessionsTimeline = response.data.sessionsTimeline || {
            labels: [],
            datasets: [{
              label: 'Study Sessions',
              data: [],
              borderColor: accentColor,
              backgroundColor: `${accentLightColor}33`, // With transparency
              tension: 0.4
            }]
          };

          this.productivityPatterns = response.data.productivityPatterns || {
            labels: [],
            datasets: [{
              label: 'Productivity',
              data: [],
              backgroundColor: accentColor
            }]
          };
        }
      } catch (error) {
        console.error("Error fetching analytics:", error);
        throw error;
      }
    },

    async fetchAchievements() {
      try {
        const response = await axios.get(`${API_URL}/study/achievements`, {
          withCredentials: true
        });

        if (response.data && response.data.achievements) {
          this.achievements = response.data.achievements;
        }
      } catch (error) {
        console.error("Error fetching achievements:", error);
        throw error;
      }
    },

    async fetchStudyStreak() {
      try {
        const response = await axios.get(`${API_URL}/study/streak`, {
          withCredentials: true
        });

        if (response.data) {
          this.studyStreak = response.data.streakData || {};
          this.recentDays = response.data.recentDays || [];
        }
      } catch (error) {
        console.error("Error fetching study streak:", error);
        throw error;
      }
    },

    async fetchAITips() {
      try {
        const response = await axios.get(`${API_URL}/study/tips`, {
          withCredentials: true
        });

        if (response.data) {
          this.aiTips = response.data;
        }
      } catch (error) {
        console.error("Error fetching AI tips:", error);
        // Not throwing the error as tips are optional
      }
    },

    // Check if this is the user's first time in Study Hub
    checkFirstTimeUser() {
      // If no schedules or sessions exist, show tutorial
      if (this.schedules.length === 0 && this.studySessions.length === 0) {
        this.showTutorial = true;
        this.tutorialStep = 1;
      }
    },

    // Close tutorial
    closeTutorial() {
      this.showTutorial = false;
      this.tutorialStep = 1;
    },

    // Date helpers
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

    formatDateISO(date) {
      const d = new Date(date);
      return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
    },

    formatDayNumber(date) {
      return date.getDate();
    },

    formatDayName(date) {
      return date.toLocaleDateString('en-US', { weekday: 'short' });
    },

    formatDayDate(date) {
      if (!date) return '';
      const d = new Date(date);
      return d.getDate().toString();
    },

    formatHour(hour) {
      // Use 12h or 24h format based on settings
      if (this.userSettings.calendar.timeFormat === '24h') {
        return `${hour}:00`;
      } else {
        const displayHour = hour % 12 || 12;
        const ampm = hour < 12 ? 'AM' : 'PM';
        return `${displayHour} ${ampm}`;
      }
    },

    formatDate(date) {
      if (!date) return '';
      let d;
      if (typeof date === 'string') {
        d = new Date(date);
      } else {
        d = date;
      }

      // Format date according to user settings
      try {
        // Simple date format implementation - should be expanded in a real app
        if (this.userSettings.calendar.dateFormat === 'DD/MM/YYYY') {
          return d.toLocaleDateString('en-GB', {
            weekday: 'long',
            day: 'numeric',
            month: 'long',
            year: 'numeric'
          });
        } else if (this.userSettings.calendar.dateFormat === 'YYYY-MM-DD') {
          const options = {
            weekday: 'long',
            year: 'numeric',
            month: 'long',
            day: 'numeric'
          };
          return d.toLocaleDateString('en-CA', options);
        } else {
          // Default MM/DD/YYYY
          return d.toLocaleDateString('en-US', {
            weekday: 'long',
            month: 'long',
            day: 'numeric',
            year: 'numeric'
          });
        }
      } catch (e) {
        // Fallback if formatting fails
        return d.toLocaleDateString('en-US', {
          weekday: 'long',
          month: 'long',
          day: 'numeric',
          year: 'numeric'
        });
      }
    },

    formatCurrentPeriod() {
      if (this.calendarView === 'month') {
        return this.currentDate.toLocaleDateString('en-US', { month: 'long', year: 'numeric' });
      } else if (this.calendarView === 'week') {
        const start = this.weekDays[0].date;
        const end = this.weekDays[6].date;

        // Format according to user date format preference
        let startStr, endStr;

        if (this.userSettings.calendar.dateFormat === 'DD/MM/YYYY') {
          startStr = start.toLocaleDateString('en-GB', { month: 'short', day: 'numeric' });
          endStr = end.toLocaleDateString('en-GB', { month: 'short', day: 'numeric', year: 'numeric' });
        } else if (this.userSettings.calendar.dateFormat === 'YYYY-MM-DD') {
          startStr = start.toLocaleDateString('en-CA', { month: 'short', day: 'numeric' });
          endStr = end.toLocaleDateString('en-CA', { month: 'short', day: 'numeric', year: 'numeric' });
        } else {
          // Default MM/DD/YYYY
          startStr = start.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
          endStr = end.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
        }

        return `${startStr} - ${endStr}`;
      } else if (this.calendarView === 'day') {
        return this.formatDate(this.currentDate);
      }

      return '';
    },

    formatEventDate(event) {
      if (!event) return '';
      return this.formatDate(event.date);
    },

    formatEventTime(event) {
      if (!event) return '';
      if (!event.startTime || !event.endTime) return 'All Day';

      const formatTime = (timeStr) => {
        const [hours, minutes] = timeStr.split(':').map(Number);
        const hour = parseInt(hours, 10);

        // Use 12h or 24h format based on settings
        if (this.userSettings.calendar.timeFormat === '24h') {
          return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}`;
        } else {
          const period = hour >= 12 ? 'PM' : 'AM';
          const hour12 = hour % 12 || 12;
          return `${hour12}:${minutes.toString().padStart(2, '0')} ${period}`;
        }
      };

      return `${formatTime(event.startTime)} - ${formatTime(event.endTime)}`;
    },

    formatStatus(status) {
      if (!status) return '';

      const statusMap = {
        'planned': 'Planned',
        'in_progress': 'In Progress',
        'completed': 'Completed',
        'missed': 'Missed'
      };

      return statusMap[status] || status;
    },

    formatPreferredTimes(times) {
      if (!times || !times.length) return 'None selected';

      const timeMap = {
        'morning': 'Morning',
        'afternoon': 'Afternoon',
        'evening': 'Evening',
        'night': 'Night'
      };

      return times.map(time => timeMap[time] || time).join(', ');
    },

    formatDuration(minutes) {
      if (!minutes) return '';
      if (minutes < 60) return `${minutes} minutes`;
      const hours = Math.floor(minutes / 60);
      const remainingMinutes = minutes % 60;
      if (remainingMinutes === 0) return `${hours} hour${hours > 1 ? 's' : ''}`;
      return `${hours} hour${hours > 1 ? 's' : ''} ${remainingMinutes} minutes`;
    },

    formatStudyDays(days) {
      if (!days || !days.length) return 'None selected';

      const dayMap = {
        'monday': 'Monday',
        'tuesday': 'Tuesday',
        'wednesday': 'Wednesday',
        'thursday': 'Thursday',
        'friday': 'Friday',
        'saturday': 'Saturday',
        'sunday': 'Sunday'
      };

      return days.map(day => dayMap[day] || day).join(', ');
    },

    formatDays(days) {
      if (!days || !days.length) return 'None';

      // Capitalize first letter of each day
      return days.map(day => day.charAt(0).toUpperCase() + day.slice(1)).join(', ');
    },

    getDatePlusDays(date, days) {
      const newDate = new Date(date);
      newDate.setDate(newDate.getDate() + days);
      return newDate;
    },

    getStartOfWeek(date, startDay = 'sunday') {
      const d = new Date(date);
      const day = d.getDay(); // 0 for Sunday

      let diff;
      if (startDay === 'monday') {
        // If we want Monday as first day
        diff = day === 0 ? -6 : 1 - day; // Handle Sunday case
      } else {
        // Default Sunday as first day
        diff = -day;
      }

      d.setDate(d.getDate() + diff);
      return d;
    },

    // User profile helpers
    getInitials(firstName, lastName) {
      let initials = '';
      if (firstName) initials += firstName.charAt(0).toUpperCase();
      if (lastName) initials += lastName.charAt(0).toUpperCase();
      return initials || 'U';
    },

    // Module helpers
    getModuleNames(moduleIds) {
      if (!moduleIds || !moduleIds.length) return ['No modules'];

      return moduleIds.map(id => {
        const module = this.availableModules.find(m => m.id === id);
        return module ? module.name : id;
      });
    },

    // Level title based on level number
    getLevelTitle(level) {
      const titles = [
        'Beginner',
        'Novice Scholar',
        'Dedicated Student',
        'Academic Adept',
        'Knowledge Master'
      ];

      if (level <= 2) return titles[0];
      if (level <= 5) return titles[1];
      if (level <= 10) return titles[2];
      if (level <= 15) return titles[3];
      return titles[4];
    },

    // Event helpers
    getEventsForDay(date) {
      const dateStr = this.formatDateISO(date);
      return this.studySessions.filter(event => event.date === dateStr);
    },

    getModuleName(moduleId) {
      if (!moduleId) return '';
      const module = this.availableModules.find(m => m.id === moduleId);
      return module ? module.name : moduleId;
    },

    getEventClass(event) {
      if (!event) return '';

      // Generate a color based on the module ID
      let className = 'event-default';

      if (event.module) {
        // Find index of module in availableModules
        const moduleIndex = this.availableModules.findIndex(m => m.id === event.module);
        if (moduleIndex !== -1) {
          // Use a fixed set of classes for visual consistency
          const moduleClasses = ['event-cs101', 'event-cs202', 'event-math201'];
          className = moduleClasses[moduleIndex % moduleClasses.length];
        }
      }

      // Add status classes
      if (event.status === 'completed' || event.completed) {
        className += ' event-completed';
      } else if (event.status === 'in_progress') {
        className += ' event-in-progress';
      } else if (event.status === 'missed') {
        className += ' event-missed';
      }

      // Add study session specific class
      if (event.type === 'study_session') {
        className += ' event-study-session';
      }

      return className;
    },

    getStatusClass(status) {
      if (!status) return '';

      const classMap = {
        'planned': 'status-planned',
        'in_progress': 'status-in-progress',
        'completed': 'status-completed',
        'missed': 'status-missed'
      };

      return classMap[status] || '';
    },

    // Event position calculation for week/day views
    calculateEventPosition(event) {
      if (!event || !event.startTime) return {};

      // Parse start and end times
      const [startHour, startMinute] = event.startTime.split(':').map(Number);
      const [endHour, endMinute] = event.endTime.split(':').map(Number);

      // Calculate top position as percentage of day height
      const dayStart = this.displayHours[0];
      const dayEnd = this.displayHours[this.displayHours.length - 1] + 1;
      const dayHeight = (dayEnd - dayStart) * 60; // total minutes in displayed day

      // Minutes from day start
      const startMinutes = (startHour - dayStart) * 60 + startMinute;

      // Calculate top position as percentage
      const top = (startMinutes / dayHeight) * 100;

      // Calculate duration in minutes
      const durationMinutes = (endHour * 60 + endMinute) - (startHour * 60 + startMinute);

      // Calculate height as percentage of day
      const height = (durationMinutes / dayHeight) * 100;

      return {
        top: `${top}%`,
        height: `${height}%`,
        maxHeight: '100%'
      };
    },

    // Calculate current time position for time indicator
    calculateCurrentTimePosition() {
      const now = new Date();
      const hours = now.getHours();
      const minutes = now.getMinutes();

      // Calculate position based on current time
      const dayStart = this.displayHours[0];
      const dayEnd = this.displayHours[this.displayHours.length - 1] + 1;
      const dayHeight = (dayEnd - dayStart) * 60; // total minutes in displayed day

      // Minutes from day start
      const currentMinutes = (hours - dayStart) * 60 + minutes;

      // Calculate position as percentage
      const position = (currentMinutes / dayHeight) * 100;

      return `${position}%`;
    },

    // Schedule management
    editSchedule(schedule) {
      this.isEditMode = true;
      this.editingScheduleId = schedule.id;

      // Populate form with schedule data
      this.scheduleForm = {
        name: schedule.name,
        startDate: schedule.start_date,
        endDate: schedule.end_date,
        preferredTimes: schedule.preferred_times || [],
        availableDays: schedule.available_days || [],
        sessionDuration: schedule.session_duration || 60,
        breakDuration: schedule.break_duration || 15,
        maxSessionsPerDay: schedule.max_sessions_per_day || 3,
        modules: schedule.modules || [],
        isActive: schedule.is_active
      };

      this.showCreateScheduleModal = true;
    },

    confirmDeleteSchedule(schedule) {
      this.selectedSchedule = schedule;
      this.showDeleteModal = true;
    },

    async deleteSchedule() {
      try {
        await axios.delete(`${API_URL}/study/schedules/${this.selectedSchedule.id}`, {
          withCredentials: true
        });

        notify({
          type: "success",
          message: "Schedule deleted successfully",
          duration: 3000
        });

        // Refresh schedules list
        await this.fetchSchedules();
        await this.fetchSessions();

        this.showDeleteModal = false;
      } catch (error) {
        console.error('Error deleting schedule:', error);
        notify({
          type: "error",
          message: error.response?.data?.error || "Failed to delete schedule",
          duration: 3000
        });
      }
    },

    async activateSchedule(scheduleId) {
      try {
        await axios.post(`${API_URL}/study/schedules/${scheduleId}/activate`, {}, {
          withCredentials: true
        });

        notify({
          type: "success",
          message: "Schedule activated successfully",
          duration: 3000
        });

        // Refresh schedules and sessions
        await this.fetchSchedules();
        await this.fetchSessions();
      } catch (error) {
        console.error('Error activating schedule:', error);
        notify({
          type: "error",
          message: error.response?.data?.error || "Failed to activate schedule",
          duration: 3000
        });
      }
    },

    showCalendarConfirmation(schedule) {
      this.selectedSchedule = schedule;

      // Get session count (could be fetched from backend or estimated)
      // For now, we'll estimate based on date range and available days
      const startDate = new Date(schedule.start_date);
      const endDate = new Date(schedule.end_date);
      const days = Math.ceil((endDate - startDate) / (1000 * 60 * 60 * 24)) + 1;
      const availableDaysCount = schedule.available_days.length;
      const maxSessionsPerDay = schedule.max_sessions_per_day;

      // Rough estimate of sessions
      this.studySessionCount = Math.min(
          days * availableDaysCount / 7 * maxSessionsPerDay,
          days * maxSessionsPerDay
      ).toFixed(0);

      this.showCalendarModal = true;
    },

    async addToCalendar() {
      try {
        await axios.post(`${API_URL}/study/schedules/${this.selectedSchedule.id}/create-events`, {}, {
          withCredentials: true
        });

        notify({
          type: "success",
          message: "Study sessions added to calendar successfully",
          duration: 3000
        });

        // Refresh schedules and sessions
        await this.fetchSchedules();
        await this.fetchSessions();

        this.showCalendarModal = false;
      } catch (error) {
        console.error('Error adding to calendar:', error);
        notify({
          type: "error",
          message: error.response?.data?.error || "Failed to add study sessions to calendar",
          duration: 3000
        });
      }
    },

    async saveSchedule() {
      try {
        // Prepare data for API
        const scheduleData = {
          name: this.scheduleForm.name,
          start_date: this.scheduleForm.startDate,
          end_date: this.scheduleForm.endDate,
          preferred_times: this.scheduleForm.preferredTimes,
          available_days: this.scheduleForm.availableDays,
          session_duration: parseInt(this.scheduleForm.sessionDuration),
          break_duration: parseInt(this.scheduleForm.breakDuration),
          max_sessions_per_day: parseInt(this.scheduleForm.maxSessionsPerDay),
          modules: this.scheduleForm.modules,
          is_active: this.scheduleForm.isActive
        };

        if (this.isEditMode) {
          // Update existing schedule
          await axios.put(
              `${API_URL}/study/schedules/${this.editingScheduleId}`,
              scheduleData,
              { withCredentials: true }
          );

          notify({
            type: "success",
            message: "Schedule updated successfully",
            duration: 3000
          });
        } else {
          // Create new schedule
          await axios.post(
              `${API_URL}/study/schedules/create`,
              scheduleData,
              { withCredentials: true }
          );

          notify({
            type: "success",
            message: "Schedule created successfully",
            duration: 3000
          });
        }

        // Refresh schedules and sessions
        await this.fetchSchedules();
        await this.fetchSessions();

        // Reset form and close modal
        this.resetScheduleForm();
        this.showCreateScheduleModal = false;
      } catch (error) {
        console.error('Error saving schedule:', error);
        notify({
          type: "error",
          message: error.response?.data?.error || "Failed to save schedule",
          duration: 3000
        });
      }
    },

    resetScheduleForm() {
      this.scheduleForm = {
        name: 'My Study Schedule',
        startDate: this.formatDateISO(new Date()),
        endDate: this.formatDateISO(this.getDatePlusDays(new Date(), 7)),
        preferredTimes: ['afternoon', 'evening'],
        availableDays: ['monday', 'tuesday', 'wednesday', 'friday'],
        sessionDuration: 60,
        breakDuration: 15,
        maxSessionsPerDay: 3,
        modules: this.availableModules.map(m => m.id),
        isActive: true
      };

      this.isEditMode = false;
      this.editingScheduleId = null;
    },

    // AI schedule generation
    async generateAISchedule() {
      try {
        // Show loading state
        this.isLoading = true;

        // Prepare data for API
        const scheduleData = {
          name: this.scheduleForm.name || "AI Generated Schedule",
          start_date: this.scheduleForm.startDate,
          end_date: this.scheduleForm.endDate,
          preferred_times: this.scheduleForm.preferredTimes,
          available_days: this.scheduleForm.availableDays,
          session_duration: parseInt(this.scheduleForm.sessionDuration),
          break_duration: parseInt(this.scheduleForm.breakDuration),
          max_sessions_per_day: parseInt(this.scheduleForm.maxSessionsPerDay),
          modules: this.scheduleForm.modules
        };

        // Submit to AI generation API
        await axios.post(
            `${API_URL}/study/schedules/generate`,
            scheduleData,
            { withCredentials: true }
        );

        notify({
          type: "success",
          message: "AI schedule generated successfully!",
          duration: 3000
        });

        // Refresh schedules and sessions
        await this.fetchSchedules();
        await this.fetchSessions();

        this.showAIScheduleModal = false;
      } catch (error) {
        console.error('Error generating AI schedule:', error);
        notify({
          type: "error",
          message: error.response?.data?.error || "Failed to generate AI schedule",
          duration: 3000
        });
      } finally {
        this.isLoading = false;
      }
    },

    // Session management
    createEventAtTime(date, hour) {
      console.log(`Create event on ${this.formatDate(date)} at ${hour}:00`);
      // Implementation for creating a new event at a specific time
      this.selectedDate = date;

      // Set default values for new event
      const defaultEvent = {
        title: 'Study Session',
        description: '',
        date: this.formatDateISO(date),
        type: 'study',
        all_day: false,
        start_time: `${hour}:00`,
        end_time: `${hour + 1}:00`,
        color: '#7b49ff',
        completed: false
      };

      // Open event details with default data
      this.selectedEvent = defaultEvent;
      this.isEditMode = false;
      this.showEventDetails = true;
    },

    showEventDetails(event) {
      this.selectedEvent = event;
      this.showEventDetails = true;
    },

    closeEventDetails() {
      this.showEventDetails = false;
      this.selectedEvent = null;
    },

    showMoreEvents(date) {
      this.selectedDate = date;
      this.calendarView = 'day';
    },

    // AI tip management
    async acceptTip(tipId) {
      try {
        // Call API to accept tip
        const response = await axios.post(
            `${API_URL}/study/tips/${tipId}/accept`,
            {},
            { withCredentials: true }
        );

        // Remove the tip from the list
        this.aiTips = this.aiTips.filter(tip => tip.id !== tipId);

        notify({
          type: "success",
          message: "Tip applied to your schedule!",
          duration: 3000
        });
      } catch (error) {
        console.error('Error accepting tip:', error);
        notify({
          type: "error",
          message: error.response?.data?.error || "Failed to apply tip",
          duration: 3000
        });
      }
    },

    async rejectTip(tipId) {
      try {
        // Call API to reject tip
        const response = await axios.post(
            `${API_URL}/study/tips/${tipId}/reject`,
            {},
            { withCredentials: true }
        );

        // Remove the tip from the list
        this.aiTips = this.aiTips.filter(tip => tip.id !== tipId);

        notify({
          type: "info",
          message: "Tip ignored",
          duration: 3000
        });
      } catch (error) {
        console.error('Error rejecting tip:', error);
        notify({
          type: "error",
          message: error.response?.data?.error || "Failed to ignore tip",
          duration: 3000
        });
      }
    }
  }
};
</script>

<style>
/* ========== Base Styles & CSS Variables ========== */
:root {
  /* Primary color with lighter/darker variants */
  --primary-color: #7c4dff;
  --primary-dark: #5e35b1;
  --primary-light: #b39ddb;
  --primary-color-rgb: 124, 77, 255;
  --primary-gradient: linear-gradient(135deg, #7c4dff, #5e35b1);

  /* Accent and semantic colors */
  --success-color: #4CAF50;
  --success-light: #e8f5e9;
  --warning-color: #ff9800;
  --warning-light: #fff3e0;
  --error-color: #f44336;
  --error-light: #ffebee;
  --info-color: #2196F3;
  --info-light: #e3f2fd;

  /* Neutral colors */
  --bg-light: #f8f9fa;
  --bg-card: #ffffff;
  --bg-input: #f5f7fa;
  --bg-hover: #eef2f7;
  --bg-muted: #f0f2f5;
  --text-primary: #2c3e50;
  --text-secondary: #6c757d;
  --text-tertiary: #95a5a6;
  --text-muted: #b4bcc2;
  --border-color: #e9ecef;
  --border-color-light: #f1f3f5;

  /* UI elements & shadows */
  --border-radius-sm: 6px;
  --border-radius: 10px;
  --border-radius-lg: 16px;
  --border-radius-xl: 24px;
  --shadow-sm: 0 2px 5px rgba(0,0,0,0.05);
  --shadow-md: 0 4px 12px rgba(0,0,0,0.08);
  --shadow-lg: 0 8px 24px rgba(0,0,0,0.12);
  --shadow-xl: 0 12px 32px rgba(0,0,0,0.16);
  --shadow-focus: 0 0 0 3px rgba(124, 77, 255, 0.25);
  --transition-fast: 0.15s ease;
  --transition-normal: 0.25s ease;
  --transition-slow: 0.4s ease;
  --font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;

  /* Event colors */
  --event-cs101: #4ecdc4;
  --event-cs202: #ff6b6b;
  --event-math201: #ffd166;

  /* Focus outline */
  --focus-outline: 0 0 0 3px rgba(124, 77, 255, 0.3);

  /* Spacing */
  --space-xs: 0.25rem;
  --space-sm: 0.5rem;
  --space-md: 1rem;
  --space-lg: 1.5rem;
  --space-xl: 2rem;
  --space-2xl: 3rem;
}

/* Dark mode variables */
.dark-mode {
  --primary-color: #9575cd;
  --primary-dark: #7e57c2;
  --primary-light: #b39ddb;
  --primary-gradient: linear-gradient(135deg, #9575cd, #7e57c2);

  --bg-light: #121212;
  --bg-card: #1e1e1e;
  --bg-input: #2a2a2a;
  --bg-hover: #333333;
  --bg-muted: #252525;
  --text-primary: #f5f5f5;
  --text-secondary: #cccccc;
  --text-tertiary: #9e9e9e;
  --text-muted: #757575;
  --border-color: #383838;
  --border-color-light: #2c2c2c;

  --shadow-sm: 0 2px 5px rgba(0,0,0,0.2);
  --shadow-md: 0 4px 12px rgba(0,0,0,0.3);
  --shadow-lg: 0 8px 24px rgba(0,0,0,0.4);
  --shadow-xl: 0 12px 32px rgba(0,0,0,0.5);
  --shadow-focus: 0 0 0 3px rgba(149, 117, 205, 0.3);

  --success-light: rgba(76, 175, 80, 0.15);
  --warning-light: rgba(255, 152, 0, 0.15);
  --error-light: rgba(244, 67, 54, 0.15);
  --info-light: rgba(33, 150, 243, 0.15);
}

/* Base and reset styles */
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: var(--font-family);
  font-size: 16px;
  line-height: 1.6;
  color: var(--text-primary);
  background-color: var(--bg-light);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

button, input, select, textarea {
  font-family: inherit;
}

/* Remove default button styling */
button {
  background: none;
  border: none;
  cursor: pointer;
}

/* ========== Main Layout Styles ========== */
.study-hub {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: var(--bg-light);
  color: var(--text-primary);
  transition: background-color var(--transition-normal),
  color var(--transition-normal);
}

:deep(.dashboard-navbar) {
  position: sticky;
  top: 0;
  z-index: 50;
  width: 100%;
}

.study-hub-layout {
  display: flex;
  flex: 1;
  height: calc(100vh - 70px); /* Adjust for navbar height */
  width: 100%;
  margin-top: 70px; /* Adjust based on the actual navbar height */
  position: relative;
  overflow: hidden;
}

:deep(.calendar-sidebar) {
  position: fixed;
  top: 70px; /* Match the top margin of study-hub-layout */
  left: 0;
  height: calc(100vh - 70px);
  z-index: 40;
}

.study-hub-container {
  flex: 1;
  overflow-y: auto;
  padding: 2rem;
  height: calc(100vh - 70px);
  margin-left: 0;
  transition: margin-left 0.3s ease;
}

.sidebar-content {
  padding: 1.25rem;
  gap: 1rem; /* Reduce gap between components */
}

.study-hub-container.with-sidebar {
  margin-left: 50px; /* Adjust based on sidebar width */
}

/* Header styles */
.study-hub-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  gap: var(--space-md);
  position: sticky;
  top: 0;
  z-index: 5;
  background-color: var(--bg-light);
  padding-bottom: var(--space-md);
  border-bottom: 1px solid var(--border-color-light);
}

.study-hub-header h1 {
  font-size: 2rem;
  font-weight: 700;
  margin: 0;
  background: var(--primary-gradient);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  color: transparent;
  letter-spacing: -0.02em;
}

/* Tab controls */
.tab-controls {
  display: flex;
  background: var(--bg-card);
  border-radius: 28px;
  padding: 0.3rem;
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--border-color);
  flex-wrap: nowrap;
  overflow-x: auto;
  -ms-overflow-style: none;
  scrollbar-width: none;
}

.tab-controls::-webkit-scrollbar {
  display: none;
}

.tab-controls button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.25rem;
  border: none;
  background: transparent;
  color: var(--text-secondary);
  border-radius: 24px;
  cursor: pointer;
  font-weight: 600;
  transition: all var(--transition-fast);
  font-size: 0.9rem;
  white-space: nowrap;
}

.tab-controls button.active {
  background: var(--primary-gradient);
  color: white;
  box-shadow: var(--shadow-sm);
}

.tab-controls button:hover:not(.active) {
  background: rgba(124, 77, 255, 0.1);
  color: var(--primary-color);
}

.tab-controls button svg {
  transition: transform var(--transition-fast);
}

.tab-controls button:hover svg {
  transform: translateY(-1px);
}

/* Header actions */
.header-actions {
  display: flex;
  gap: var(--space-md);
  align-items: center;
  margin-left: auto;
}

.toggle-sidebar-btn, .help-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.7rem 1rem;
  background-color: var(--bg-card);
  color: var(--text-primary);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  font-weight: 500;
  transition: all var(--transition-fast);
  box-shadow: var(--shadow-sm);
}

.toggle-sidebar-btn:hover, .help-button:hover {
  background-color: var(--bg-hover);
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
  border-color: var(--primary-light);
  color: var(--primary-color);
}

/* Sidebar integration */
.study-hub-sidebar {
  position: fixed;
  top: 70px;
  left: 0;
  height: calc(100vh - 70px);
  width: 200px;
  z-index: 20;
  transition: transform var(--transition-normal),
  width var(--transition-normal),
  box-shadow var(--transition-normal);
  background-color: var(--bg-card);
  border-right: 1px solid var(--border-color);
  box-shadow: var(--shadow-lg);
}

.sidebarCollapsed .study-hub-sidebar {
  width: 60px;
}

.sidebarCollapsed .study-hub-container.with-sidebar {
  margin-left: 280px;
}

.study-hub-sidebar.collapsed {
  width: 60px;
}

/* ========== Schedule Tab Styles ========== */
.schedule-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-xl);
  flex-wrap: wrap;
  gap: var(--space-md);
}

.schedule-header h2 {
  font-size: 1.75rem;
  font-weight: 700;
  margin: 0;
  color: var(--text-primary);
}

.schedule-actions {
  display: flex;
  gap: var(--space-md);
}

.schedule-btn, .ai-schedule-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.25rem;
  border-radius: var(--border-radius);
  font-weight: 600;
  cursor: pointer;
  transition: all var(--transition-normal);
  box-shadow: var(--shadow-sm);
}

.schedule-btn {
  background-color: var(--bg-card);
  color: var(--text-primary);
  border: 1px solid var(--border-color);
}

.schedule-btn:hover {
  background-color: var(--bg-hover);
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
  border-color: var(--primary-light);
  color: var(--primary-color);
}

.ai-schedule-btn {
  background: var(--primary-gradient);
  color: white;
  border: none;
  position: relative;
  overflow: hidden;
}

.ai-schedule-btn::after {
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

.ai-schedule-btn:hover {
  background: linear-gradient(135deg, var(--primary-dark), var(--primary-color));
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

@keyframes shimmer {
  0% { transform: rotate(30deg) translateX(-100%); }
  100% { transform: rotate(30deg) translateX(100%); }
}

/* Schedules List Section */
.schedules-list-section {
  margin-bottom: var(--space-xl);
  background-color: var(--bg-card);
  border-radius: var(--border-radius-lg);
  padding: var(--space-xl);
  box-shadow: var(--shadow-md);
  transition: transform var(--transition-normal),
  box-shadow var(--transition-normal);
}

.schedules-list-section:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-lg);
}

.schedules-list-section h3 {
  font-size: 1.3rem;
  font-weight: 700;
  margin-top: 0;
  margin-bottom: var(--space-lg);
  color: var(--text-primary);
  position: relative;
  display: inline-block;
  padding-bottom: var(--space-xs);
}

.schedules-list-section h3::after {
  content: "";
  position: absolute;
  left: 0;
  bottom: 0;
  height: 3px;
  width: 40px;
  background: var(--primary-gradient);
  border-radius: 3px;
}

.schedules-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: var(--space-lg);
}

/* Schedule Card */
.schedule-card {
  background-color: var(--bg-card);
  border-radius: var(--border-radius);
  border: 1px solid var(--border-color);
  overflow: hidden;
  transition: all var(--transition-normal);
  box-shadow: var(--shadow-sm);
  height: 100%;
  display: flex;
  flex-direction: column;
}

.schedule-card:hover {
  transform: translateY(-5px);
  box-shadow: var(--shadow-md);
  border-color: var(--primary-light);
}

.schedule-card.active-schedule {
  border: 2px solid var(--primary-color);
  box-shadow: 0 0 0 4px rgba(124, 77, 255, 0.1);
}

.active-schedule, .upcoming-sessions, .study-analytics {
  padding: 1rem; /* Reduce padding */
  margin-bottom: 1rem; /* Reduce margin */
}


.schedule-card-header {
  background: linear-gradient(to right, rgba(124, 77, 255, 0.05), transparent);
  padding: var(--space-md);
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid var(--border-color-light);
}




.schedule-card-header h4 {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--text-primary);
}

.schedule-badges {
  display: flex;
  gap: 0.5rem;
}

.ai-badge, .active-badge {
  font-size: 0.7rem;
  font-weight: 600;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.ai-badge {
  background-color: rgba(124, 77, 255, 0.1);
  color: var(--primary-color);
}

.active-badge {
  background-color: var(--success-light);
  color: var(--success-color);
}

.schedule-card-content {
  padding: var(--space-md);
  flex: 1;
  display: flex;
  flex-direction: column;
}

.schedule-details {
  margin-bottom: var(--space-md);
  flex: 1;
}

.schedule-detail-item {
  margin-bottom: 0.75rem;
  font-size: 0.95rem;
  display: flex;
  flex-direction: column;
}

.detail-label {
  color: var(--text-secondary);
  font-weight: 500;
  margin-bottom: 0.25rem;
}

.detail-value {
  color: var(--text-primary);
  font-weight: 500;
}

.schedule-card-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: auto;
}

.activate-btn, .calendar-btn, .edit-btn, .delete-btn {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  padding: 0.6rem;
  border-radius: var(--border-radius);
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  transition: all var(--transition-fast);
  flex: 1;
  justify-content: center;
}

.activate-btn {
  background-color: var(--success-light);
  color: var(--success-color);
  border: 1px solid rgba(76, 175, 80, 0.2);
}

.activate-btn:hover {
  background-color: var(--success-color);
  color: white;
  box-shadow: var(--shadow-sm);
}

.calendar-btn {
  background-color: rgba(124, 77, 255, 0.1);
  color: var(--primary-color);
  border: 1px solid rgba(124, 77, 255, 0.2);
}

.calendar-btn:hover {
  background-color: var(--primary-color);
  color: white;
  box-shadow: var(--shadow-sm);
}

.edit-btn {
  background-color: var(--info-light);
  color: var(--info-color);
  border: 1px solid rgba(33, 150, 243, 0.2);
}

.edit-btn:hover {
  background-color: var(--info-color);
  color: white;
  box-shadow: var(--shadow-sm);
}

.delete-btn {
  background-color: var(--error-light);
  color: var(--error-color);
  border: 1px solid rgba(244, 67, 54, 0.2);
}

.delete-btn:hover {
  background-color: var(--error-color);
  color: white;
  box-shadow: var(--shadow-sm);
}

/* Calendar Container */
.calendar-container {
  background-color: var(--bg-card);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow-md);
  overflow: hidden;
  margin-bottom: var(--space-xl);
  transition: transform var(--transition-normal),
  box-shadow var(--transition-normal);
}

.calendar-container:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-lg);
}

/* Calendar Controls */
.calendar-controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--space-md) var(--space-lg);
  border-bottom: 1px solid var(--border-color);
  background-color: var(--bg-card);
  position: sticky;
  top: 0;
  z-index: 3;
}

.view-selector {
  display: flex;
  border: 1px solid var(--border-color);
  border-radius: 24px;
  overflow: hidden;
  box-shadow: var(--shadow-sm);
}

.view-btn {
  padding: 0.6rem 1.25rem;
  background-color: var(--bg-card);
  color: var(--text-secondary);
  border: none;
  cursor: pointer;
  font-weight: 600;
  transition: all var(--transition-fast);
}

.view-btn:not(:last-child) {
  border-right: 1px solid var(--border-color);
}

.view-btn.active {
  background: var(--primary-gradient);
  color: white;
}

.view-btn:hover:not(.active) {
  background-color: var(--bg-hover);
  color: var(--primary-color);
}

.month-navigator {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.nav-btn, .today-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--bg-card);
  color: var(--text-primary);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  cursor: pointer;
  transition: all var(--transition-fast);
  box-shadow: var(--shadow-sm);
}

.nav-btn {
  width: 36px;
  height: 36px;
}

.today-btn {
  padding: 0 var(--space-md);
  height: 36px;
  font-weight: 600;
}

.nav-btn:hover, .today-btn:hover {
  background-color: var(--bg-hover);
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
  border-color: var(--primary-light);
  color: var(--primary-color);
}

.current-period {
  font-weight: 700;
  font-size: 1.1rem;
  color: var(--text-primary);
  padding: 0.5rem var(--space-md);
  background-color: var(--bg-input);
  border-radius: var(--border-radius);
}

/* Calendar Views */
.calendar-view {
  position: relative;
}

/* Month View */
.month-view {
  min-height: 600px;
}

.month-grid-header {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  background-color: var(--bg-input);
  border-bottom: 1px solid var(--border-color);
}

.day-header {
  padding: 0.75rem;
  text-align: center;
  font-weight: 600;
  color: var(--text-secondary);
}

.month-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  grid-auto-rows: minmax(100px, 1fr);
}

.day-cell {
  border-right: 1px solid var(--border-color-light);
  border-bottom: 1px solid var(--border-color-light);
  padding: 0.6rem;
  position: relative;
  cursor: pointer;
  transition: all var(--transition-fast);
}

.day-cell:hover {
  background-color: var(--bg-hover);
}

.day-cell.today {
  background-color: rgba(124, 77, 255, 0.05);
}

.day-cell.today .day-number {
  background-color: var(--primary-color);
  color: white;
  border-radius: 50%;
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 4px rgba(124, 77, 255, 0.2);
}

.day-cell.different-month {
  background-color: var(--bg-card);
  opacity: 0.7;
}

.day-cell.selected {
  background-color: rgba(124, 77, 255, 0.1);
  box-shadow: inset 0 0 0 2px var(--primary-color);
}

.day-number {
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.day-events {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  overflow: hidden;
}

.day-event-pill {
  font-size: 0.75rem;
  padding: 0.25rem 0.5rem;
  border-radius: var(--border-radius-sm);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  color: white;
  cursor: pointer;
  transition: all var(--transition-fast);
  margin-bottom: 2px;
  box-shadow: var(--shadow-sm);
}

.day-event-pill:hover {
  transform: translateY(-1px) scale(1.02);
  box-shadow: var(--shadow-md);
}

.more-events {
  font-size: 0.75rem;
  text-align: center;
  color: var(--primary-color);
  background-color: rgba(124, 77, 255, 0.1);
  padding: 0.25rem;
  border-radius: var(--border-radius-sm);
  cursor: pointer;
  transition: all var(--transition-fast);
  margin-top: 0.25rem;
}

.more-events:hover {
  background-color: rgba(124, 77, 255, 0.2);
  transform: translateY(-1px);
}

/* Week View */
.week-view {
  height: 600px;
  display: flex;
  flex-direction: column;
}

.week-grid-header {
  display: flex;
  border-bottom: 1px solid var(--border-color);
  background-color: var(--bg-input);
}

.time-column-header {
  width: 60px;
  flex-shrink: 0;
}

.day-column-header {
  flex: 1;
  text-align: center;
  padding: 0.75rem 0;
  border-left: 1px solid var(--border-color-light);
}

.day-column-header.today {
  background-color: rgba(124, 77, 255, 0.05);
}

.day-name {
  font-weight: 600;
  color: var(--text-secondary);
}

.day-number {
  font-size: 1.1rem;
  font-weight: 700;
}

.week-grid {
  flex: 1;
  display: flex;
  overflow-y: auto;
}

.time-column {
  width: 60px;
  flex-shrink: 0;
  border-right: 1px solid var(--border-color);
  background-color: var(--bg-input);
}

.time-cell {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-bottom: 1px solid var(--border-color-light);
  font-size: 0.8rem;
  color: var(--text-secondary);
  position: relative;
}

.day-columns {
  flex: 1;
  display: flex;
}

.day-column {
  flex: 1;
  border-right: 1px solid var(--border-color-light);
  position: relative;
}

.day-column:last-child {
  border-right: none;
}

.day-column.today {
  background-color: rgba(124, 77, 255, 0.05);
}

.day-column .time-cell {
  border-left: none;
  justify-content: flex-start;
  padding-left: 0.5rem;
  cursor: pointer;
}

.day-column .time-cell:hover {
  background-color: rgba(124, 77, 255, 0.05);
}

/* Event Styles */
.week-event {
  position: absolute;
  left: 4px;
  right: 4px;
  padding: 0.5rem;
  border-radius: var(--border-radius-sm);
  color: white;
  font-size: 0.85rem;
  overflow: hidden;
  cursor: pointer;
  box-shadow: var(--shadow-sm);
  transition: all var(--transition-fast);
  z-index: 5;
}

.week-event:hover {
  transform: translateY(-1px);
  box-shadow: var(--shadow-md);
  z-index: 10;
}

.event-time {
  font-size: 0.75rem;
  opacity: 0.9;
  margin-bottom: 0.25rem;
}

.event-title {
  font-weight: 600;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* Current time indicator */
.current-time-indicator {
  position: absolute;
  left: 0;
  right: 0;
  z-index: 10;
  pointer-events: none;
}

.time-dot {
  position: absolute;
  left: -4px;
  top: -4px;
  width: 8px;
  height: 8px;
  background-color: var(--error-color);
  border-radius: 50%;
}

.time-line {
  height: 2px;
  background-color: var(--error-color);
  width: 100%;
}

/* Day View */
.day-view {
  height: 600px;
  display: flex;
  flex-direction: column;
}

.day-view-header {
  padding: var(--space-md);
  text-align: center;
  border-bottom: 1px solid var(--border-color);
  background-color: var(--bg-input);
}

.current-day {
  font-size: 1.2rem;
  font-weight: 700;
  color: var(--text-primary);
}

.day-view-grid {
  flex: 1;
  display: flex;
  overflow-y: auto;
}

.events-column {
  flex: 1;
  position: relative;
}

.day-event {
  position: absolute;
  left: 60px;
  right: 12px;
  padding: 0.5rem;
  border-radius: var(--border-radius-sm);
  color: white;
  overflow: hidden;
  cursor: pointer;
  box-shadow: var(--shadow-sm);
  transition: all var(--transition-fast);
  z-index: 5;
}

.day-event:hover {
  transform: translateY(-1px);
  box-shadow: var(--shadow-md);
  z-index: 10;
}

.event-description {
  margin-top: 0.25rem;
  font-size: 0.75rem;
  opacity: 0.9;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

/* Event color styles */
.event-default {
  background: linear-gradient(135deg, var(--primary-color), var(--primary-dark));
}

.event-cs101 {
  background: linear-gradient(135deg, var(--event-cs101), #33b8b0);
}

.event-cs202 {
  background: linear-gradient(135deg, var(--event-cs202), #e05757);
}

.event-math201 {
  background: linear-gradient(135deg, var(--event-math201), #e6bd5b);
}

.event-completed {
  opacity: 0.7;
  text-decoration: line-through;
}

.event-in-progress {
  box-shadow: 0 0 0 2px var(--success-light);
}

.event-missed {
  background: linear-gradient(135deg, #bdbdbd, #9e9e9e);
  opacity: 0.7;
}

/* AI Tips Section */
.ai-tips-section {
  margin-top: var(--space-xl);
  padding: var(--space-lg);
  background-color: var(--bg-card);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow-md);
  transition: transform var(--transition-normal),
  box-shadow var(--transition-normal);
}

.ai-tips-section:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-lg);
}

.ai-tips-section h3 {
  font-size: 1.3rem;
  font-weight: 700;
  margin-top: 0;
  margin-bottom: var(--space-md);
  color: var(--text-primary);
  position: relative;
  display: inline-block;
  padding-bottom: var(--space-xs);
}

.ai-tips-section h3::after {
  content: "";
  position: absolute;
  left: 0;
  bottom: 0;
  height: 3px;
  width: 40px;
  background: var(--primary-gradient);
  border-radius: 3px;
}

.tips-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-md);
}

.tip-card {
  display: flex;
  gap: var(--space-md);
  padding: var(--space-md);
  background-color: var(--bg-input);
  border-radius: var(--border-radius);
  border-left: 3px solid var(--primary-color);
  transition: all var(--transition-fast);
}

.tip-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-sm);
  background-color: var(--bg-hover);
}

.tip-icon {
  color: var(--primary-color);
  display: flex;
  align-items: flex-start;
  justify-content: center;
}

.tip-content {
  flex: 1;
}

.tip-title {
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 0.5rem;
}

.tip-text {
  color: var(--text-secondary);
  font-size: 0.95rem;
  line-height: 1.5;
}

.tip-actions {
  display: flex;
  gap: 0.5rem;
  align-items: flex-start;
}

.accept-tip-btn, .reject-tip-btn {
  padding: 0.5rem 1rem;
  border-radius: var(--border-radius);
  cursor: pointer;
  font-weight: 600;
  font-size: 0.85rem;
  transition: all var(--transition-fast);
}

.accept-tip-btn {
  background-color: var(--primary-color);
  color: white;
  border: none;
}

.accept-tip-btn:hover {
  background-color: var(--primary-dark);
  transform: translateY(-2px);
  box-shadow: var(--shadow-sm);
}

.reject-tip-btn {
  background-color: transparent;
  color: var(--text-secondary);
  border: 1px solid var(--border-color);
}

.reject-tip-btn:hover {
  background-color: var(--bg-hover);
  color: var(--text-primary);
}

/* No Schedule Placeholder */
.no-schedule-placeholder {
  padding: var(--space-2xl);
  text-align: center;
  background-color: var(--bg-card);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow-md);
  margin: var(--space-xl) 0;
  transition: transform var(--transition-normal),
  box-shadow var(--transition-normal);
}

.no-schedule-placeholder:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-lg);
}

.no-schedule-placeholder svg {
  color: var(--primary-color);
  opacity: 0.8;
  margin-bottom: var(--space-lg);
}

.no-schedule-placeholder h3 {
  font-size: 1.5rem;
  margin-bottom: var(--space-md);
  color: var(--text-primary);
  font-weight: 700;
}

.placeholder-actions {
  display: flex;
  justify-content: center;
  gap: var(--space-md);
  flex-wrap: wrap;
  margin-top: var(--space-lg);
}

.no-schedule-placeholder p {
  color: var(--text-secondary);
  max-width: 600px;
  margin: 0 auto var(--space-xl);
  line-height: 1.6;
}

/* ========== Loading States ========== */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--space-2xl);
  text-align: center;
  min-height: 200px;
  background-color: var(--bg-card);
  border-radius: var(--border-radius-lg);
  margin: var(--space-md) 0;
  box-shadow: var(--shadow-sm);
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid rgba(124, 77, 255, 0.1);
  border-radius: 50%;
  border-top-color: var(--primary-color);
  animation: spin 1s linear infinite;
  margin-bottom: var(--space-md);
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Error States */
.error-message {
  background-color: var(--error-light);
  border-left: 4px solid var(--error-color);
  padding: var(--space-md);
  margin: var(--space-md) 0;
  border-radius: var(--border-radius);
}

.error-message p {
  color: var(--error-color);
  margin-bottom: var(--space-md);
}

.retry-btn {
  padding: 0.5rem 1rem;
  background-color: var(--error-color);
  color: white;
  border: none;
  border-radius: var(--border-radius);
  cursor: pointer;
  font-weight: 600;
  transition: all var(--transition-fast);
}

.retry-btn:hover {
  background-color: #d32f2f;
  transform: translateY(-2px);
  box-shadow: var(--shadow-sm);
}

.empty-state {
  text-align: center;
  padding: var(--space-xl);
  color: var(--text-secondary);
  background-color: var(--bg-input);
  border-radius: var(--border-radius);
  margin: var(--space-md) 0;
}

/* ========== Analytics Tab Styles ========== */
.analytics-tab h2 {
  font-size: 1.75rem;
  font-weight: 700;
  margin-bottom: var(--space-xl);
  color: var(--text-primary);
  position: relative;
  display: inline-block;
  padding-bottom: var(--space-xs);
}

.analytics-tab h2::after {
  content: "";
  position: absolute;
  left: 0;
  bottom: 0;
  height: 3px;
  width: 40px;
  background: var(--primary-gradient);
  border-radius: 3px;
}

.analytics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: var(--space-lg);
  margin-bottom: var(--space-xl);
}

.analytics-card {
  background-color: var(--bg-card);
  border-radius: var(--border-radius-lg);
  padding: var(--space-lg);
  box-shadow: var(--shadow-md);
  height: 100%;
  display: flex;
  flex-direction: column;
  transition: transform var(--transition-normal),
  box-shadow var(--transition-normal);
}

.analytics-card:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-lg);
}

.analytics-card.full-width {
  grid-column: 1 / -1;
}

.analytics-card h3 {
  font-size: 1.2rem;
  font-weight: 700;
  margin-top: 0;
  margin-bottom: var(--space-md);
  color: var(--text-primary);
  position: relative;
  display: inline-block;
  padding-bottom: var(--space-xs);
}

.analytics-card h3::after {
  content: "";
  position: absolute;
  left: 0;
  bottom: 0;
  height: 3px;
  width: 30px;
  background: var(--primary-gradient);
  border-radius: 3px;
}

.stats-overview {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--space-md);
}

.stat-item {
  text-align: center;
  background-color: rgba(255, 255, 255, 0.1);
  padding: 0.6rem 0.75rem; /* Reduce padding */
  border-radius: var(--border-radius);
  flex: 1;
  transition: all 0.3s ease;
}

.pomodoro-timer-card {
  padding: 1rem; /* Reduce padding */
  margin-bottom: 1rem; /* Reduce margin */
}

.timer-circle-container {
  width: 120px; /* Smaller timer circle */
  height: 120px;
}

.timer-value {
  font-size: 1.75rem; /* Smaller font */
}

.pomodoro-content {
  gap: 0.75rem; /* Reduce gap */
}

.timer-controls {
  gap: 0.3rem; /* Reduce gap */
}

.stat-item:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-sm);
  background-color: var(--bg-hover);
}

.stat-value {
  font-size: 1.4rem; /* Slightly smaller font */
  font-weight: 700;
  margin-bottom: 0.2rem;
}

.stat-label {
  color: var(--text-secondary);
  font-size: 0.9rem;
  font-weight: 500;
}

.chart-container {
  height: 250px;
  position: relative;
  margin-top: auto;
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Module Stats Table */
.module-stats-table {
  width: 100%;
  margin-top: var(--space-md);
  overflow-x: auto;
  border-radius: var(--border-radius);
  border: 1px solid var(--border-color-light);
}

.module-stats-header {
  display: grid;
  grid-template-columns: 2fr repeat(5, 1fr);
  padding: 0.75rem;
  background-color: var(--bg-input);
  font-weight: 600;
  color: var(--text-primary);
  position: sticky;
  top: 0;
  z-index: 2;
}

.module-stats-row {
  display: grid;
  grid-template-columns: 2fr repeat(5, 1fr);
  padding: 0.75rem;
  border-bottom: 1px solid var(--border-color-light);
  transition: background-color var(--transition-fast);
}

.module-stats-row:last-child {
  border-bottom: none;
}

.module-stats-row:hover {
  background-color: var(--bg-hover);
}

.module-name-cell {
  font-weight: 500;
}

.module-stat-cell {
  text-align: center;
}

.progress-bar-small {
  height: 6px;
  background-color: var(--bg-input);
  border-radius: 3px;
  overflow: hidden;
  margin: 0 auto;
  width: 80%;
}

.progress-value {
  height: 100%;
  background: var(--primary-gradient);
  border-radius: 3px;
  text-align: center;
  color: transparent;
  font-size: 0;
}

/* No Data Placeholder */
.no-data-placeholder {
  text-align: center;
  padding: var(--space-2xl);
  background-color: var(--bg-card);
  border-radius: var(--border-radius-lg);
  margin: var(--space-xl) 0;
  box-shadow: var(--shadow-md);
}

.no-data-placeholder svg {
  color: var(--primary-color);
  opacity: 0.7;
  margin-bottom: var(--space-lg);
}

.no-data-placeholder h3 {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: var(--space-md);
  color: var(--text-primary);
}

.no-data-placeholder p {
  color: var(--text-secondary);
  max-width: 600px;
  margin: 0 auto;
  line-height: 1.6;
}

/* ========== Achievements Tab Styles ========== */
.achievements-tab h2 {
  font-size: 1.75rem;
  font-weight: 700;
  margin-bottom: var(--space-xl);
  color: var(--text-primary);
  position: relative;
  display: inline-block;
  padding-bottom: var(--space-xs);
}

.achievements-tab h2::after {
  content: "";
  position: absolute;
  left: 0;
  bottom: 0;
  height: 3px;
  width: 40px;
  background: var(--primary-gradient);
  border-radius: 3px;
}

.streak-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: var(--space-lg);
  margin-bottom: var(--space-xl);
}

.streak-card, .level-card {
  background-color: var(--bg-card);
  border-radius: var(--border-radius-lg);
  padding: var(--space-lg);
  box-shadow: var(--shadow-md);
  transition: transform var(--transition-normal),
  box-shadow var(--transition-normal);
}

.streak-card:hover, .level-card:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-lg);
}

.streak-card h3, .level-card h3 {
  font-size: 1.2rem;
  font-weight: 700;
  margin-top: 0;
  margin-bottom: var(--space-md);
  color: var(--text-primary);
  position: relative;
  display: inline-block;
  padding-bottom: var(--space-xs);
}

.streak-card h3::after, .level-card h3::after {
  content: "";
  position: absolute;
  left: 0;
  bottom: 0;
  height: 3px;
  width: 30px;
  background: var(--primary-gradient);
  border-radius: 3px;
}

.streak-display {
  display: flex;
  gap: var(--space-lg);
  margin-bottom: var(--space-lg);
}

.streak-circle {
  width: 100px;
  height: 100px;
  background: conic-gradient(var(--primary-color) 0% 100%, var(--bg-input) 0% 0%);
  border-radius: 50%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: relative;
  box-shadow: var(--shadow-md);
}

.streak-circle::before {
  content: '';
  position: absolute;
  top: 10px;
  right: 10px;
  bottom: 10px;
  left: 10px;
  background-color: var(--bg-card);
  border-radius: 50%;
}

.streak-value {
  font-size: 2rem;
  font-weight: 800;
  color: var(--primary-color);
  z-index: 1;
  position: relative;
}

.streak-label {
  color: var(--text-secondary);
  font-size: 0.8rem;
  font-weight: 500;
  z-index: 1;
  position: relative;
}

.streak-stats {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.streak-stat {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem var(--space-md);
  background-color: var(--bg-input);
  border-radius: var(--border-radius);
  border-left: 3px solid var(--primary-color);
  transition: all var(--transition-fast);
}

.streak-stat:hover {
  transform: translateX(3px);
  background-color: var(--bg-hover);
}

.streak-calendar {
  display: flex;
  justify-content: space-between;
  padding: var(--space-md);
  background-color: var(--bg-input);
  border-radius: var(--border-radius);
}

.calendar-day {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}

.day-date {
  font-weight: 600;
  font-size: 0.8rem;
  color: var(--text-secondary);
}

.day-indicator {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  border: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--bg-card);
  transition: all var(--transition-fast);
}

.day-indicator.studied {
  background-color: var(--primary-color);
  border-color: var(--primary-color);
  color: white;
  box-shadow: var(--shadow-sm);
}

/* Level Display */
.level-display {
  display: flex;
  gap: var(--space-lg);
  align-items: center;
}

.level-badge {
  width: 100px;
  height: 100px;
  background: var(--primary-gradient);
  border-radius: 50%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
  box-shadow: var(--shadow-md);
}

.level-value {
  font-size: 2.5rem;
  font-weight: 800;
}

.level-title {
  font-size: 0.65rem;
  text-align: center;
  max-width: 90%;
  font-weight: 600;
}

.xp-info {
  flex: 1;
}

.xp-progress-bar {
  height: 1.5rem;
  background-color: var(--bg-input);
  border-radius: var(--border-radius);
  overflow: hidden;
  margin-bottom: 0.5rem;
  box-shadow: inset 0 0 0 1px var(--border-color);
}

.xp-progress {
  height: 100%;
  background: var(--primary-gradient);
  display: flex;
  align-items: center;
  justify-content: flex-end;
  color: white;
  padding-right: 0.5rem;
  font-weight: 600;
  font-size: 0.8rem;
}

.xp-text {
  display: flex;
  justify-content: space-between;
  color: var(--text-secondary);
  font-size: 0.9rem;
}

.xp-current {
  font-weight: 700;
  color: var(--primary-color);
}

.xp-next {
  color: var(--text-secondary);
}

/* Achievements */
.achievements-section {
  background-color: var(--bg-card);
  border-radius: var(--border-radius-lg);
  padding: var(--space-lg);
  box-shadow: var(--shadow-md);
  transition: transform var(--transition-normal),
  box-shadow var(--transition-normal);
  margin-bottom: var(--space-xl);
}

.achievements-section:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-lg);
}

.achievements-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-lg);
  flex-wrap: wrap;
  gap: var(--space-md);
}

.achievements-header h3 {
  font-size: 1.2rem;
  font-weight: 700;
  margin: 0;
  color: var(--text-primary);
  position: relative;
  display: inline-block;
  padding-bottom: var(--space-xs);
}

.achievements-header h3::after {
  content: "";
  position: absolute;
  left: 0;
  bottom: 0;
  height: 3px;
  width: 30px;
  background: var(--primary-gradient);
  border-radius: 3px;
}

.achievements-filter {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.achievements-filter button {
  padding: 0.5rem 1rem;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  background-color: var(--bg-input);
  color: var(--text-secondary);
  cursor: pointer;
  transition: all var(--transition-fast);
  font-size: 0.9rem;
  font-weight: 500;
}

.achievements-filter button.active {
  background: var(--primary-gradient);
  color: white;
  border-color: var(--primary-color);
}

.achievements-filter button:not(.active):hover {
  background-color: var(--bg-hover);
  color: var(--primary-color);
  border-color: var(--primary-light);
}

.achievements-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: var(--space-lg);
}

.achievement-card {
  background-color: var(--bg-card);
  border-radius: var(--border-radius);
  overflow: hidden;
  box-shadow: var(--shadow-sm);
  transition: all var(--transition-normal);
  border: 1px solid var(--border-color-light);
}

.achievement-card:hover {
  transform: translateY(-5px);
  box-shadow: var(--shadow-md);
}

.achievement-card.completed {
  border-color: var(--success-color);
}

.achievement-card.in-progress {
  border-color: var(--primary-color);
}

.achievement-icon {
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--bg-input);
  padding: var(--space-md);
}

.achievement-icon img {
  max-height: 100%;
  transition: opacity var(--transition-normal);
}

.achievement-card.locked .achievement-icon img {
  opacity: 0.3;
}

.achievement-info {
  padding: var(--space-md);
}

.achievement-info h4 {
  font-size: 1.1rem;
  font-weight: 700;
  margin-top: 0;
  margin-bottom: 0.5rem;
  color: var(--text-primary);
}

.achievement-info p {
  color: var(--text-secondary);
  font-size: 0.9rem;
  margin-bottom: var(--space-md);
  line-height: 1.5;
}

.achievement-progress {
  margin-bottom: 0.5rem;
}

.progress-bar {
  height: 8px;
  background-color: var(--bg-input);
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 0.5rem;
}

.progress {
  height: 100%;
  background: var(--primary-gradient);
  border-radius: 4px;
}

.achievement-card.completed .progress {
  background: linear-gradient(135deg, var(--success-color), #66bb6a);
}

.progress-text {
  font-size: 0.8rem;
  text-align: right;
  color: var(--text-secondary);
}

.achievement-badge {
  padding: 0.5rem var(--space-md);
  background-color: var(--bg-input);
  border-top: 1px solid var(--border-color-light);
  font-size: 0.8rem;
  text-align: center;
  font-weight: 600;
}

.achievement-card.completed .achievement-badge {
  background-color: var(--success-light);
  color: var(--success-color);
}

.achievement-card.in-progress .achievement-badge {
  background-color: rgba(124, 77, 255, 0.1);
  color: var(--primary-color);
}

.achievement-card.locked .achievement-badge {
  color: var(--text-secondary);
}

/* ========== Profile Tab Styles ========== */
.profile-tab h2 {
  font-size: 1.75rem;
  font-weight: 700;
  margin-bottom: var(--space-xl);
  color: var(--text-primary);
  position: relative;
  display: inline-block;
  padding-bottom: var(--space-xs);
}

.profile-tab h2::after {
  content: "";
  position: absolute;
  left: 0;
  bottom: 0;
  height: 3px;
  width: 40px;
  background: var(--primary-gradient);
  border-radius: 3px;
}

.profile-content {
  max-width: 800px;
  margin: 0 auto;
  width: 100%;
}

.profile-card {
  background-color: var(--bg-card);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow-md);
  padding: var(--space-xl);
  width: 100%;
  transition: transform var(--transition-normal),
  box-shadow var(--transition-normal);
}

.profile-card:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-lg);
}

.profile-header {
  display: flex;
  align-items: center;
  gap: var(--space-xl);
  margin-bottom: var(--space-xl);
  padding-bottom: var(--space-lg);
  border-bottom: 1px solid var(--border-color-light);
}

.profile-avatar {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  overflow: hidden;
  background-color: var(--bg-input);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: var(--shadow-md);
}

.profile-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-placeholder {
  width: 100%;
  height: 100%;
  background: var(--primary-gradient);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2.5rem;
  font-weight: 700;
}

.profile-info {
  flex: 1;
}

.profile-info h3 {
  font-size: 1.5rem;
  font-weight: 800;
  margin: 0 0 0.5rem;
  color: var(--text-primary);
}

.user-email {
  color: var(--primary-color);
  margin-bottom: 0.25rem;
  font-weight: 500;
}

.user-role {
  color: var(--text-primary);
  font-weight: 600;
  margin-bottom: 0.25rem;
  display: inline-block;
  padding: 0.25rem 0.75rem;
  background-color: var(--bg-input);
  border-radius: 12px;
}

.user-details {
  color: var(--text-secondary);
  font-size: 0.9rem;
  margin-top: 0.5rem;
}

.profile-details {
  margin-bottom: var(--space-xl);
}

.profile-details h4 {
  font-size: 1.1rem;
  font-weight: 700;
  margin: var(--space-lg) 0 var(--space-md);
  color: var(--text-primary);
  border-bottom: 1px solid var(--border-color-light);
  padding-bottom: 0.5rem;
  position: relative;
}

.profile-details h4::after {
  content: "";
  position: absolute;
  left: 0;
  bottom: -1px;
  height: 2px;
  width: 40px;
  background: var(--primary-gradient);
}

.module-list {
  padding: 0;
  list-style: none;
  border: 1px solid var(--border-color-light);
  border-radius: var(--border-radius);
  overflow: hidden;
}

.module-list-item {
  padding: var(--space-md);
  border-bottom: 1px solid var(--border-color-light);
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: background-color var(--transition-fast);
}

.module-list-item:last-child {
  border-bottom: none;
}

.module-list-item:hover {
  background-color: var(--bg-hover);
}

.module-info {
  display: flex;
  flex-direction: column;
}

.module-name {
  font-weight: 600;
  color: var(--text-primary);
}

.module-code {
  font-size: 0.85rem;
  color: var(--text-secondary);
  margin-top: 0.25rem;
}

.preference-value-set {
  color: var(--primary-color);
  font-weight: 600;
}

.empty-state-tip {
  font-style: italic;
  font-size: 0.9rem;
  margin-top: 0.5rem;
  color: var(--primary-color);
}

.enrolled-badge {
  background-color: var(--success-light);
  color: var(--success-color);
  font-size: 0.75rem;
  font-weight: 600;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
}

.preference-item {
  margin-bottom: 0.75rem;
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.preference-label {
  font-weight: 600;
  color: var(--text-primary);
  min-width: 200px;
}

.preference-value {
  color: var(--text-secondary);
  flex: 1;
}

.profile-actions {
  display: flex;
  justify-content: flex-end;
  gap: var(--space-md);
}

.edit-profile-btn, .update-preferences-btn {
  padding: 0.75rem 1.25rem;
  border-radius: var(--border-radius);
  font-weight: 600;
  cursor: pointer;
  transition: all var(--transition-normal);
  text-decoration: none;
  display: inline-block;
}

.edit-profile-btn {
  background-color: var(--bg-input);
  color: var(--text-primary);
  border: 1px solid var(--border-color);
}

.edit-profile-btn:hover {
  background-color: var(--bg-hover);
  transform: translateY(-2px);
  box-shadow: var(--shadow-sm);
  border-color: var(--primary-light);
  color: var(--primary-color);
}

.update-preferences-btn {
  background: var(--primary-gradient);
  color: white;
  border: none;
  box-shadow: var(--shadow-sm);
}

.update-preferences-btn:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
  background: linear-gradient(135deg, var(--primary-color), var(--primary-dark));
}

/* ========== Modal Styles ========== */
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
  padding: var(--space-md);
  backdrop-filter: blur(4px);
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.modal-container {
  background-color: var(--bg-card);
  border-radius: var(--border-radius-lg);
  width: 100%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: var(--shadow-xl);
  display: flex;
  flex-direction: column;
  animation: modalSlideIn 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes modalSlideIn {
  0% {
    opacity: 0;
    transform: translateY(20px) scale(0.95);
  }
  100% {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.modal-container::-webkit-scrollbar {
  width: 6px;
}

.modal-container::-webkit-scrollbar-track {
  background: transparent;
}

.modal-container::-webkit-scrollbar-thumb {
  background-color: var(--border-color);
  border-radius: 3px;
}

.modal-header {
  padding: var(--space-lg) var(--space-lg) var(--space-md);
  border-bottom: 1px solid var(--border-color);
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: sticky;
  top: 0;
  background-color: var(--bg-card);
  z-index: 10;
}

.modal-header h3 {
  font-size: 1.25rem;
  font-weight: 700;
  margin: 0;
  color: var(--text-primary);
}

.close-modal-btn {
  background: transparent;
  border: none;
  color: var(--text-secondary);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  transition: all var(--transition-fast);
}

.close-modal-btn:hover {
  background-color: var(--bg-hover);
  color: var(--text-primary);
  transform: rotate(90deg);
}

.modal-body {
  padding: var(--space-lg);
  overflow-y: auto;
}

.modal-footer {
  padding: var(--space-md) var(--space-lg);
  border-top: 1px solid var(--border-color);
  display: flex;
  justify-content: flex-end;
  gap: var(--space-md);
  position: sticky;
  bottom: 0;
  background-color: var(--bg-card);
  z-index: 10;
}

/* Tutorial Modal */
.tutorial-modal {
  max-width: 650px;
}

.tutorial-step {
  margin-bottom: var(--space-xl);
}

.tutorial-step h4 {
  font-size: 1.3rem;
  font-weight: 700;
  margin-bottom: var(--space-md);
  color: var(--primary-color);
}

.tutorial-step p {
  color: var(--text-secondary);
  margin-bottom: var(--space-md);
  line-height: 1.6;
}

.tutorial-step ul, .tutorial-step ol {
  margin-left: var(--space-xl);
  margin-bottom: var(--space-lg);
  color: var(--text-secondary);
}

.tutorial-step li {
  margin-bottom: var(--space-sm);
  line-height: 1.6;
}

.tutorial-icon {
  display: flex;
  justify-content: center;
  margin: var(--space-lg) 0;
}

.tutorial-icon svg {
  color: var(--primary-color);
}

.tutorial-nav-btn {
  padding: 0.75rem 1.5rem;
  border-radius: var(--border-radius);
  font-weight: 600;
  cursor: pointer;
  transition: all var(--transition-fast);
}

.prev-btn {
  background-color: var(--bg-input);
  color: var(--text-primary);
  border: 1px solid var(--border-color);
}

.prev-btn:hover {
  background-color: var(--bg-hover);
  transform: translateY(-2px);
  box-shadow: var(--shadow-sm);
}

.next-btn, .done-btn {
  background: var(--primary-gradient);
  color: white;
  border: none;
  box-shadow: var(--shadow-sm);
}


.today-summary {
  background: var(--primary-gradient);
  border-radius: var(--border-radius);
  padding: 1rem;  /* Reduce padding */
  box-shadow: 0 8px 20px rgba(158, 120, 255, 0.2);
  color: white;
  position: relative;
  overflow: hidden;
  margin-bottom: 1rem; /* Reduce margin */
  transition: all 0.3s ease;
}

.date-pill {
  background-color: rgba(255, 255, 255, 0.2);
  border-radius: 16px;
  padding: 0.3rem 0.75rem; /* Smaller padding */
  font-size: 0.85rem;
  font-weight: 700;
  display: inline-block;
  margin-bottom: 0.75rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.quick-stats {
  display: flex;
  justify-content: space-around;
  gap: 0.5rem; /* Reduce gap */
}





.daily-progress {
  margin-top: 0.75rem;
}


.next-btn:hover, .done-btn:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

/* ========== Animation Classes ========== */
.animate-fade-in {
  animation: fadeIn 0.4s ease-out;
}

.animate-slide-down {
  animation: slideDown 0.4s ease-out;
}

.animate-pop-in {
  animation: popIn 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
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

/* ========== Responsive Styles ========== */
@media (max-width: 1280px) {
  .study-hub-container {
    padding: var(--space-lg);
  }

  .study-hub-container.with-sidebar {
    margin-left: 280px;
  }

  .sidebarCollapsed .study-hub-container.with-sidebar {
    margin-left: 60px;
  }

  .study-hub-sidebar {
    width: 280px;
  }

  .sidebarCollapsed .study-hub-sidebar {
    width: 50px;
  }
}

@media (max-width: 992px) {
  .study-hub-container {
    padding: var(--space-md);
  }

  .study-hub-container.with-sidebar {
    margin-left: 0;
  }

  .study-hub-sidebar {
    transform: translateX(-100%);
    box-shadow: var(--shadow-lg);
    z-index: 40;
  }

  .showSidebar .study-hub-sidebar {
    transform: translateX(0);
  }

  .streak-section, .analytics-grid {
    grid-template-columns: 1fr;
  }

  .streak-display, .level-display {
    flex-direction: column;
    align-items: center;
  }

  .streak-stat {
    width: 100%;
  }
}

@media (max-width: 768px) {
  .study-hub-container {
    padding: 1rem;
  }

  .study-hub-container.with-sidebar {
    margin-left: 0;
  }

  .study-hub-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .tab-controls {
    width: 100%;
    overflow-x: auto;
    padding: 0.2rem;
  }

  .tab-controls button {
    padding: 0.5rem 0.75rem;
    font-size: 0.85rem;
  }

  .header-actions {
    width: 100%;
    margin-top: var(--space-sm);
  }

  .toggle-sidebar-btn, .help-button {
    width: 100%;
    justify-content: center;
  }

  .help-button {
    margin-top: var(--space-sm);
  }

  .schedule-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .schedule-actions {
    width: 100%;
    margin-top: var(--space-sm);
  }

  .schedule-btn, .ai-schedule-btn {
    width: 100%;
  }

  .schedules-list {
    grid-template-columns: 1fr;
  }

  .calendar-controls {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--space-sm);
  }

  .view-selector, .month-navigator {
    width: 100%;
  }

  .month-grid-header .day-header {
    font-size: 0.8rem;
    padding: 0.5rem 0.25rem;
  }

  .month-grid {
    grid-auto-rows: minmax(80px, 1fr);
  }

  .day-cell {
    padding: 0.4rem;
  }

  .day-event-pill {
    font-size: 0.7rem;
    padding: 0.15rem 0.3rem;
  }

  .week-view, .day-view {
    height: 450px;
  }

  .time-column {
    width: 40px;
  }

  .day-event {
    left: 40px;
  }

  .module-stats-header, .module-stats-row {
    grid-template-columns: 2fr repeat(2, 1fr);
    font-size: 0.9rem;
  }

  .module-stat-cell:nth-child(3),
  .module-stat-cell:nth-child(4),
  .module-stat-cell:nth-child(5) {
    display: none;
  }

  .profile-header {
    flex-direction: column;
    text-align: center;
  }

  .profile-avatar {
    margin: 0 auto var(--space-md);
  }

  .profile-actions {
    flex-direction: column;
    gap: var(--space-sm);
  }

  .edit-profile-btn, .update-preferences-btn {
    width: 100%;
    text-align: center;
  }

  .modal-body, .modal-header, .modal-footer {
    padding: var(--space-md);
  }

  .profile-card {
    padding: var(--space-md);
  }
}

@media (max-width: 480px) {
  .month-navigator .current-period {
    display: none;
  }

  .nav-btn, .today-btn {
    width: 100%;
  }

  .day-cell {
    padding: 0.25rem;
  }

  .achievements-filter {
    overflow-x: auto;
    padding-bottom: var(--space-sm);
    width: 100%;
  }

  .achievements-filter button {
    white-space: nowrap;
    font-size: 0.8rem;
    padding: 0.4rem 0.8rem;
  }

  .achievement-card .achievement-info h4 {
    font-size: 1rem;
  }

  .achievement-card .achievement-info p {
    font-size: 0.8rem;
  }

  .tutorial-step h4 {
    font-size: 1.1rem;
  }

  .tutorial-step ul, .tutorial-step ol {
    margin-left: var(--space-md);
  }

  .tutorial-nav-btn {
    padding: 0.6rem 1rem;
    font-size: 0.9rem;
  }
}

/* Touch Device Optimizations */
@media (hover: none) {
  .schedule-card:hover,
  .analytics-card:hover,
  .streak-card:hover,
  .level-card:hover,
  .achievement-card:hover,
  .profile-card:hover,
  .calendar-container:hover,
  .schedules-list-section:hover,
  .ai-tips-section:hover,
  .achievements-section:hover {
    transform: none;
  }

  .activate-btn:active,
  .calendar-btn:active,
  .edit-btn:active,
  .delete-btn:active,
  .schedule-btn:active,
  .ai-schedule-btn:active,
  .nav-btn:active,
  .today-btn:active,
  .view-btn:active,
  .toggle-sidebar-btn:active,
  .help-button:active {
    transform: scale(0.97);
  }
}
</style>