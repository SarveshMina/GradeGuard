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

    <div class="study-hub-container">
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
        <button @click="showTutorial = true" class="help-button" title="What is this?">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10"></circle>
            <path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"></path>
            <line x1="12" y1="17" x2="12.01" y2="17"></line>
          </svg>
          What is this?
        </button>
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
        <div v-if="!isLoading && !error && studySessions.length === 0" class="no-schedule-placeholder">
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

      <!-- PROFILE TAB - Updated to display user's profile data -->
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

    <!-- CREATE SCHEDULE MODAL -->
    <div v-if="showCreateScheduleModal" class="modal-overlay" @click.self="showCreateScheduleModal = false">
      <div class="modal-container">
        <div class="modal-header">
          <h3>Create Study Schedule</h3>
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
          </div>
        </div>
        <div class="modal-footer">
          <button @click="showCreateScheduleModal = false" class="cancel-btn">Cancel</button>
          <button @click="createSchedule" class="create-btn">Create Schedule</button>
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
  </div>
</template>

<script>
import { getDarkModePreference } from "@/services/darkModeService.js";
import DashboardNavBar from "@/components/DashboardNavBar.vue";
import ModuleTimeDistributionChart from "@/components/charts/ModuleTimeDistributionChart.vue";
import StudySessionsTimelineChart from "@/components/charts/StudySessionsTimelineChart.vue";
import ProductivityPatternsChart from "@/components/charts/ProductivityPatternsChart.vue";
import { notify } from "@/services/toastService.js";
import axios from 'axios';
import { API_URL } from "@/config.js";

export default {
  name: "StudyHub",
  components: {
    DashboardNavBar,
    ModuleTimeDistributionChart,
    StudySessionsTimelineChart,
    ProductivityPatternsChart
  },
  data() {
    return {
      darkMode: false,
      isMobile: false,
      activeTab: 'schedule',
      calendarView: 'month',
      isLoading: false,
      error: null,

      // Tutorial state
      showTutorial: false,
      tutorialStep: 1,

      // Current date and selection
      currentDate: new Date(),
      selectedDate: new Date(),

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
        modules: []
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

      // Currently selected event
      selectedEvent: null,

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

  mounted() {
    // Initialize dates in schedule form
    this.scheduleForm.startDate = this.formatDateISO(new Date());
    this.scheduleForm.endDate = this.formatDateISO(this.getDatePlusDays(new Date(), 7));

    // Get dark mode preference
    this.darkMode = getDarkModePreference();
    this.checkMobile();

    // Initialize calendar data
    this.generateWeekDays();

    // Set up event listeners
    window.addEventListener("resize", this.checkMobile);
    window.addEventListener('darkModeChange', this.onDarkModeChange);

    // Set up the current time updater for the calendar
    this.startCurrentTimeUpdates();

    // Fetch initial data
    this.fetchData();
  },

  beforeUnmount() {
    // Clean up event listeners
    window.removeEventListener("resize", this.checkMobile);
    window.removeEventListener('darkModeChange', this.onDarkModeChange);

    // Clear time updater interval
    if (this.timeIndicatorInterval) {
      clearInterval(this.timeIndicatorInterval);
    }
  },

  methods: {
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

    // API Methods
    async fetchUserProfile() {
      try {
        const response = await axios.get(`${API_URL}/user/profile`, {
          withCredentials: true
        });

        if (response.data) {
          this.userProfile = response.data;
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

        const response = await axios.get(`${API_URL}/study/sessions`, {
          params: {
            start_date: this.formatDateISO(startDate),
            end_date: this.formatDateISO(endDate)
          },
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
          this.moduleTimeDistribution = response.data.moduleTimeDistribution || { labels: [], datasets: [{ data: [], backgroundColor: [] }] };
          this.sessionsTimeline = response.data.sessionsTimeline || { labels: [], datasets: [{ label: 'Study Sessions', data: [], borderColor: '#9e78ff', backgroundColor: 'rgba(158, 120, 255, 0.2)', tension: 0.4 }] };
          this.productivityPatterns = response.data.productivityPatterns || { labels: [], datasets: [{ label: 'Productivity', data: [], backgroundColor: '#9e78ff' }] };
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

    // Handle dark mode changes
    onDarkModeChange(event) {
      this.darkMode = event.detail.isDark;
    },

    // Check for mobile screen size
    checkMobile() {
      this.isMobile = window.innerWidth <= 768;
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
      const startOfWeek = this.getStartOfWeek(this.currentDate);
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
      const displayHour = hour % 12 || 12;
      const ampm = hour < 12 ? 'AM' : 'PM';
      return `${displayHour} ${ampm}`;
    },

    formatDate(date) {
      if (!date) return '';
      let d;
      if (typeof date === 'string') {
        d = new Date(date);
      } else {
        d = date;
      }
      return d.toLocaleDateString('en-US', {
        weekday: 'long',
        month: 'long',
        day: 'numeric',
        year: 'numeric'
      });
    },

    formatCurrentPeriod() {
      if (this.calendarView === 'month') {
        return this.currentDate.toLocaleDateString('en-US', { month: 'long', year: 'numeric' });
      } else if (this.calendarView === 'week') {
        const start = this.weekDays[0].date;
        const end = this.weekDays[6].date;

        // Format like "Mar 1 - Mar 7, 2023"
        const startStr = start.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
        const endStr = end.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });

        return `${startStr} - ${endStr}`;
      } else if (this.calendarView === 'day') {
        return this.currentDate.toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric', year: 'numeric' });
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
        const [hours, minutes] = timeStr.split(':');
        const hour = parseInt(hours, 10);
        const period = hour >= 12 ? 'PM' : 'AM';
        const hour12 = hour % 12 || 12;
        return `${hour12}:${minutes} ${period}`;
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

    getDatePlusDays(date, days) {
      const newDate = new Date(date);
      newDate.setDate(newDate.getDate() + days);
      return newDate;
    },

    getStartOfWeek(date) {
      const d = new Date(date);
      const day = d.getDay(); // 0 for Sunday, 1 for Monday, etc.
      const diff = d.getDate() - day;
      return new Date(d.setDate(diff));
    },

    // User profile helpers
    getInitials(firstName, lastName) {
      let initials = '';
      if (firstName) initials += firstName.charAt(0).toUpperCase();
      if (lastName) initials += lastName.charAt(0).toUpperCase();
      return initials || 'U';
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

    // Create event at specific time
    createEventAtTime(date, hour) {
      console.log(`Create event on ${this.formatDate(date)} at ${hour}:00`);

      // Prepare default end time (1 hour later)
      const endHour = hour + 1;

      // Open create schedule modal with pre-filled date and time
      this.selectedDate = new Date(date);
      this.showCreateScheduleModal = true;
    },

    // Show event details
    showEventDetails(event) {
      this.selectedEvent = event;
      this.showEventDetails = true;
    },

    // Close event details modal
    closeEventDetails() {
      this.showEventDetails = false;
      this.selectedEvent = null;
    },

    // Show more events for a day
    showMoreEvents(date) {
      this.selectedDate = date;
      this.calendarView = 'day';
    },

    // Schedule creation and management
    async createSchedule() {
      try {
        // Convert form data to API format
        const scheduleData = {
          name: this.scheduleForm.name,
          start_date: this.scheduleForm.startDate,
          end_date: this.scheduleForm.endDate,
          preferred_times: this.scheduleForm.preferredTimes,
          available_days: this.scheduleForm.availableDays,
          session_duration: parseInt(this.scheduleForm.sessionDuration),
          break_duration: parseInt(this.scheduleForm.breakDuration),
          max_sessions_per_day: parseInt(this.scheduleForm.maxSessionsPerDay),
          modules: this.scheduleForm.modules
        };

        // Submit to API
        const response = await axios.post(
            `${API_URL}/study/schedules/create`,
            scheduleData,
            { withCredentials: true }
        );

        notify({
          type: "success",
          message: "Schedule created successfully!",
          duration: 3000
        });

        // Refresh schedules and sessions
        await this.fetchSchedules();
        await this.fetchSessions();

        this.showCreateScheduleModal = false;
      } catch (error) {
        console.error('Error creating schedule:', error);
        notify({
          type: "error",
          message: error.response?.data?.error || "Failed to create schedule",
          duration: 3000
        });
      }
    },

    async generateAISchedule() {
      try {
        // Show loading state
        this.isLoading = true;

        // Convert form data to API format
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
        const response = await axios.post(
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
    async startSession(event) {
      try {
        // Call start session API
        const response = await axios.post(
            `${API_URL}/study/sessions/${event.id}/start`,
            {},
            { withCredentials: true }
        );

        notify({
          type: "success",
          message: "Study session started!",
          duration: 3000
        });

        // Update session in local state
        const index = this.studySessions.findIndex(s => s.id === event.id);
        if (index !== -1) {
          this.studySessions[index].status = 'in_progress';
          this.studySessions[index].started_at = new Date().toISOString();
        }

        this.closeEventDetails();
      } catch (error) {
        console.error('Error starting session:', error);
        notify({
          type: "error",
          message: error.response?.data?.error || "Failed to start session",
          duration: 3000
        });
      }
    },

    async completeSession(event) {
      try {
        // Set up feedback form with default values
        this.feedbackForm = {
          productivity: 3,
          difficulty: 3,
          notes: '',
          topics: event.topics || []
        };
        this.newTopic = '';

        // Show completion feedback modal
        this.closeEventDetails();
        this.selectedEvent = event;
        this.showCompletionModal = true;
      } catch (error) {
        console.error('Error preparing completion form:', error);
        notify({
          type: "error",
          message: "Error preparing session completion form",
          duration: 3000
        });
      }
    },

    async rescheduleSession(event) {
      try {
        // Show reschedule modal or form
        notify({
          type: "info",
          message: "Rescheduling feature coming soon",
          duration: 3000
        });

        this.closeEventDetails();
      } catch (error) {
        console.error('Error rescheduling session:', error);
        notify({
          type: "error",
          message: error.response?.data?.error || "Failed to reschedule session",
          duration: 3000
        });
      }
    },

    // Feedback form management
    addTopic() {
      if (!this.newTopic.trim()) return;

      if (!this.feedbackForm.topics.includes(this.newTopic.trim())) {
        this.feedbackForm.topics.push(this.newTopic.trim());
      }

      this.newTopic = '';
    },

    removeTopic(index) {
      this.feedbackForm.topics.splice(index, 1);
    },

    async submitFeedback() {
      try {
        // Submit feedback to API
        const response = await axios.post(
            `${API_URL}/study/sessions/${this.selectedEvent.id}/complete`,
            this.feedbackForm,
            { withCredentials: true }
        );

        notify({
          type: "success",
          message: "Session completed! You earned XP!",
          duration: 3000
        });

        // Refresh sessions and analytics
        await this.fetchSessions();
        await this.fetchAnalytics();
        await this.fetchAchievements();
        await this.fetchStudyStreak();

        this.showCompletionModal = false;
      } catch (error) {
        console.error('Error submitting feedback:', error);
        notify({
          type: "error",
          message: error.response?.data?.error || "Failed to complete session",
          duration: 3000
        });
      }
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
  --event-cs101: #4ecdc4;
  --event-cs202: #ff6b6b;
  --event-math201: #ffd166;
}

.study-hub {
  min-height: 100vh;
  background-color: var(--bg-light);
  color: var(--text-primary);
  transition: background-color var(--transition-speed) ease,
  color var(--transition-speed) ease;
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

@keyframes shimmer {
  0% {
    background-position: -100% 0;
  }
  100% {
    background-position: 100% 0;
  }
}

/* ========== Layout Styles ========== */
.study-hub-container {
  padding: 2rem;
  margin-top: 70px; /* Space for fixed navbar */
}

.study-hub-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.study-hub-header h1 {
  font-size: 2rem;
  font-weight: 700;
  margin: 0;
  background: linear-gradient(to right, var(--primary-color), var(--primary-dark));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  color: transparent;
}

.tab-controls {
  display: flex;
  background: var(--bg-card);
  border-radius: 24px;
  padding: 0.25rem;
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--border-color-light);
}

.tab-controls button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1.25rem;
  border: none;
  background: transparent;
  color: var(--text-secondary);
  border-radius: 20px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s ease;
  font-size: 0.9rem;
}

.tab-controls button.active {
  background: var(--primary-color);
  color: white;
  box-shadow: 0 2px 8px rgba(123, 73, 255, 0.25);
}

.tab-controls button:hover:not(.active) {
  background: rgba(123, 73, 255, 0.1);
  color: var(--primary-color);
}

/* Help Button */
.help-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background-color: var(--bg-input);
  color: var(--text-primary);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s ease;
}

.help-button:hover {
  background-color: var(--bg-hover);
  transform: translateY(-2px);
  box-shadow: var(--shadow-sm);
}

/* ========== Loading and Error States ========== */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem;
  text-align: center;
  min-height: 200px;
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

.error-message {
  background-color: rgba(244, 67, 54, 0.1);
  border-left: 4px solid var(--error-color);
  padding: 1rem;
  margin-bottom: 1.5rem;
  border-radius: var(--border-radius);
}

.error-message p {
  color: var(--error-color);
  margin-bottom: 1rem;
}

.retry-btn {
  padding: 0.5rem 1rem;
  background-color: var(--error-color);
  color: white;
  border: none;
  border-radius: var(--border-radius);
  cursor: pointer;
  font-weight: 500;
}

.empty-state {
  text-align: center;
  padding: 2rem;
  color: var(--text-secondary);
  background-color: var(--bg-input);
  border-radius: var(--border-radius);
  margin: 1rem 0;
}

/* ========== Study Schedule Tab Styles ========== */
.schedule-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.schedule-header h2 {
  font-size: 1.5rem;
  font-weight: 600;
  margin: 0;
  color: var(--text-primary);
}

.schedule-actions {
  display: flex;
  gap: 1rem;
}

.schedule-btn, .ai-schedule-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.25rem;
  border-radius: var(--border-radius);
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.schedule-btn {
  background-color: var(--bg-input);
  color: var(--text-primary);
  border: 1px solid var(--border-color);
}

.schedule-btn:hover {
  background-color: var(--bg-hover);
  box-shadow: var(--shadow-sm);
  transform: translateY(-2px);
}

.ai-schedule-btn {
  background-color: var(--primary-color);
  color: white;
  border: none;
  box-shadow: 0 2px 5px rgba(123, 73, 255, 0.2);
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
  background-color: var(--primary-dark);
  transform: translateY(-2px);
  box-shadow: 0 4px 10px rgba(123, 73, 255, 0.3);
}

/* Calendar container */
.calendar-container {
  background-color: var(--bg-card);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow-md);
  overflow: hidden;
  margin-bottom: 2rem;
}

.calendar-controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.5rem;
  border-bottom: 1px solid var(--border-color);
  flex-wrap: wrap;
  gap: 1rem;
}

.view-selector {
  display: flex;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  overflow: hidden;
}

.view-btn {
  padding: 0.5rem 1.25rem;
  background-color: var(--bg-card);
  color: var(--text-secondary);
  border: none;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s ease;
}

.view-btn:not(:last-child) {
  border-right: 1px solid var(--border-color);
}

.view-btn.active {
  background-color: var(--primary-color);
  color: white;
}

.view-btn:hover:not(.active) {
  background-color: var(--bg-hover);
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
  background-color: var(--bg-input);
  color: var(--text-primary);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  cursor: pointer;
  transition: all 0.2s ease;
}

.nav-btn {
  width: 36px;
  height: 36px;
}

.today-btn {
  padding: 0 1rem;
  height: 36px;
  font-weight: 500;
}

.nav-btn:hover, .today-btn:hover {
  background-color: var(--bg-hover);
  transform: translateY(-1px);
  box-shadow: var(--shadow-sm);
}

.current-period {
  font-weight: 600;
  font-size: 1.1rem;
  color: var(--text-primary);
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
  padding: 0.5rem;
  position: relative;
  cursor: pointer;
  transition: all 0.2s ease;
}

.day-cell:hover {
  background-color: var(--bg-hover);
}

.day-cell.today {
  background-color: rgba(123, 73, 255, 0.05);
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
  box-shadow: 0 2px 4px rgba(123, 73, 255, 0.2);
}

.day-cell.different-month {
  background-color: var(--bg-card);
  opacity: 0.7;
}

.day-cell.selected {
  background-color: rgba(123, 73, 255, 0.1);
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
  border-radius: var(--border-radius);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  color: white;
  cursor: pointer;
  transition: transform 0.2s ease;
}

.day-event-pill:hover {
  transform: translateY(-1px) scale(1.02);
  box-shadow: var(--shadow-sm);
}

.more-events {
  font-size: 0.75rem;
  text-align: center;
  color: var(--primary-color);
  background-color: rgba(123, 73, 255, 0.1);
  padding: 0.25rem;
  border-radius: var(--border-radius);
  cursor: pointer;
}

.more-events:hover {
  background-color: rgba(123, 73, 255, 0.2);
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
  background-color: rgba(123, 73, 255, 0.05);
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
  background-color: rgba(123, 73, 255, 0.05);
}

.day-column .time-cell {
  border-left: none;
  justify-content: flex-start;
  padding-left: 0.5rem;
  cursor: pointer;
}

.day-column .time-cell:hover {
  background-color: rgba(123, 73, 255, 0.05);
}

/* Event Styles */
.week-event {
  position: absolute;
  left: 4px;
  right: 4px;
  padding: 0.5rem;
  border-radius: var(--border-radius);
  color: white;
  font-size: 0.8rem;
  overflow: hidden;
  cursor: pointer;
  box-shadow: var(--shadow-sm);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  z-index: 5;
}

.week-event:hover {
  transform: translateY(-1px);
  box-shadow: var(--shadow-md);
  z-index: 10;
}

.event-time {
  font-size: 0.7rem;
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
  padding: 1rem;
  text-align: center;
  border-bottom: 1px solid var(--border-color);
  background-color: var(--bg-input);
}

.current-day {
  font-size: 1.2rem;
  font-weight: 600;
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
  border-radius: var(--border-radius);
  color: white;
  overflow: hidden;
  cursor: pointer;
  box-shadow: var(--shadow-sm);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
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
  background-color: var(--primary-color);
}

.event-cs101 {
  background-color: var(--event-cs101);
}

.event-cs202 {
  background-color: var(--event-cs202);
}

.event-math201 {
  background-color: var(--event-math201);
}

.event-completed {
  opacity: 0.7;
  text-decoration: line-through;
}

.event-in-progress {
  box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.5);
}

.event-missed {
  background-color: #ccc;
  opacity: 0.7;
}

/* AI Tips section */
.ai-tips-section {
  margin-top: 2rem;
  padding: 1.5rem;
  background-color: var(--bg-card);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow-md);
}

.ai-tips-section h3 {
  font-size: 1.2rem;
  font-weight: 600;
  margin-top: 0;
  margin-bottom: 1rem;
  color: var(--text-primary);
}

.tips-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.tip-card {
  display: flex;
  gap: 1rem;
  padding: 1rem;
  background-color: var(--bg-input);
  border-radius: var(--border-radius);
  border-left: 3px solid var(--primary-color);
  transition: transform 0.2s ease;
}

.tip-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-sm);
}

.tip-icon {
  color: var(--primary-color);
  display: flex;
  align-items: center;
  justify-content: center;
}

.tip-content {
  flex: 1;
}

.tip-title {
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 0.5rem;
}

.tip-text {
  color: var(--text-secondary);
  font-size: 0.9rem;
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
  font-weight: 500;
  font-size: 0.8rem;
  transition: all 0.2s ease;
}

.accept-tip-btn {
  background-color: var(--primary-color);
  color: white;
  border: none;
}

.accept-tip-btn:hover {
  background-color: var(--primary-dark);
}

.reject-tip-btn {
  background-color: transparent;
  color: var(--text-secondary);
  border: 1px solid var(--border-color);
}

.reject-tip-btn:hover {
  background-color: var(--bg-hover);
}

/* No Schedule Placeholder */
.no-schedule-placeholder {
  padding: 3rem;
  text-align: center;
  background-color: var(--bg-card);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow-md);
  margin-top: 2rem;
}

.no-schedule-placeholder svg {
  color: var(--primary-color);
  opacity: 0.7;
  margin-bottom: 1.5rem;
}

.no-schedule-placeholder h3 {
  font-size: 1.5rem;
  margin-bottom: 1rem;
  color: var(--text-primary);
}

.no-schedule-placeholder p {
  color: var(--text-secondary);
  max-width: 600px;
  margin: 0 auto 2rem;
  line-height: 1.6;
}

.placeholder-actions {
  display: flex;
  justify-content: center;
  gap: 1rem;
}

/* ========== Analytics Tab Styles ========== */
.analytics-tab h2 {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  color: var(--text-primary);
}

.analytics-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
}

.analytics-card {
  background-color: var(--bg-card);
  border-radius: var(--border-radius-lg);
  padding: 1.5rem;
  box-shadow: var(--shadow-md);
}

.analytics-card.full-width {
  grid-column: 1 / -1;
}

.analytics-card h3 {
  font-size: 1.1rem;
  font-weight: 600;
  margin-top: 0;
  margin-bottom: 1rem;
  color: var(--text-primary);
  border-bottom: 1px solid var(--border-color-light);
  padding-bottom: 0.75rem;
}

.stats-overview {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
}

.stat-item {
  padding: 1rem;
  background-color: var(--bg-input);
  border-radius: var(--border-radius);
  text-align: center;
  transition: transform 0.2s ease;
}

.stat-item:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-sm);
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--primary-color);
  margin-bottom: 0.5rem;
}

.stat-label {
  color: var(--text-secondary);
  font-size: 0.9rem;
}

.chart-container {
  height: 250px;
  position: relative;
}

/* Module Stats Table */
.module-stats-table {
  width: 100%;
  margin-top: 1rem;
}

.module-stats-header {
  display: grid;
  grid-template-columns: 2fr repeat(5, 1fr);
  padding: 0.75rem;
  background-color: var(--bg-input);
  border-radius: var(--border-radius) var(--border-radius) 0 0;
  font-weight: 600;
  color: var(--text-primary);
}

.module-stats-row {
  display: grid;
  grid-template-columns: 2fr repeat(5, 1fr);
  padding: 0.75rem;
  border-bottom: 1px solid var(--border-color-light);
  transition: background-color 0.2s ease;
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
  background-color: var(--primary-color);
  border-radius: 3px;
  text-align: center;
  color: transparent;
  font-size: 0;
}

/* ========== Achievements Tab Styles ========== */
.achievements-tab h2 {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  color: var(--text-primary);
}

.streak-section {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.streak-card, .level-card {
  background-color: var(--bg-card);
  border-radius: var(--border-radius-lg);
  padding: 1.5rem;
  box-shadow: var(--shadow-md);
}

.streak-card h3, .level-card h3 {
  font-size: 1.1rem;
  font-weight: 600;
  margin-top: 0;
  margin-bottom: 1rem;
  color: var(--text-primary);
}

.streak-display {
  display: flex;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
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
  font-weight: 700;
  color: var(--primary-color);
  z-index: 1;
  position: relative;
}

.streak-label {
  color: var(--text-secondary);
  font-size: 0.8rem;
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
  padding: 0.5rem 1rem;
  background-color: var(--bg-input);
  border-radius: var(--border-radius);
  border-left: 3px solid var(--primary-color);
}

.streak-calendar {
  display: flex;
  justify-content: space-between;
  padding: 1rem;
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
}

.day-indicator {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  border: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  justify-content: center;
}

.day-indicator.studied {
  background-color: var(--primary-color);
  border-color: var(--primary-color);
  color: white;
}

/* Level Display */
.level-display {
  display: flex;
  gap: 1.5rem;
  align-items: center;
}

.level-badge {
  width: 100px;
  height: 100px;
  background: linear-gradient(135deg, var(--primary-color), var(--primary-dark));
  border-radius: 50%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
}

.level-value {
  font-size: 2.5rem;
  font-weight: 700;
}

.level-title {
  font-size: 0.65rem;
  text-align: center;
  max-width: 90%;
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
}

.xp-progress {
  height: 100%;
  background: linear-gradient(to right, var(--primary-color), var(--primary-dark));
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
  font-weight: 600;
  color: var(--primary-color);
}

/* Achievements */
.achievements-section {
  background-color: var(--bg-card);
  border-radius: var(--border-radius-lg);
  padding: 1.5rem;
  box-shadow: var(--shadow-md);
}

.achievements-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.achievements-header h3 {
  font-size: 1.1rem;
  font-weight: 600;
  margin: 0;
  color: var(--text-primary);
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
  transition: all 0.2s ease;
  font-size: 0.9rem;
}

.achievements-filter button.active {
  background-color: var(--primary-color);
  color: white;
  border-color: var(--primary-color);
}

.achievements-filter button:not(.active):hover {
  background-color: var(--bg-hover);
}

.achievements-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.achievement-card {
  background-color: var(--bg-card);
  border-radius: var(--border-radius);
  overflow: hidden;
  box-shadow: var(--shadow-sm);
  transition: transform 0.2s ease;
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
  padding: 1rem;
}

.achievement-icon img {
  max-height: 100%;
  opacity: 0.7;
}

.achievement-card.locked .achievement-icon img {
  opacity: 0.3;
}

.achievement-info {
  padding: 1rem;
}

.achievement-info h4 {
  font-size: 1rem;
  font-weight: 600;
  margin-top: 0;
  margin-bottom: 0.5rem;
  color: var(--text-primary);
}

.achievement-info p {
  color: var(--text-secondary);
  font-size: 0.9rem;
  margin-bottom: 1rem;
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
  background-color: var(--primary-color);
  border-radius: 4px;
}

.achievement-card.completed .progress {
  background-color: var(--success-color);
}

.progress-text {
  font-size: 0.8rem;
  text-align: right;
  color: var(--text-secondary);
}

.achievement-badge {
  padding: 0.5rem 1rem;
  background-color: var(--bg-input);
  border-top: 1px solid var(--border-color-light);
  font-size: 0.8rem;
  text-align: center;
  font-weight: 600;
}

.achievement-card.completed .achievement-badge {
  background-color: rgba(76, 175, 80, 0.1);
  color: var(--success-color);
}

.achievement-card.in-progress .achievement-badge {
  background-color: rgba(123, 73, 255, 0.1);
  color: var(--primary-color);
}

.achievement-card.locked .achievement-badge {
  color: var(--text-secondary);
}

/* ========== Profile Tab Styles ========== */
.profile-tab h2 {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  color: var(--text-primary);
}

.profile-content {
  max-width: 800px;
  margin: 0 auto;
}

.profile-card {
  background-color: var(--bg-card);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow-md);
  padding: 2rem;
  margin-bottom: 2rem;
}

.profile-header {
  display: flex;
  align-items: center;
  gap: 2rem;
  margin-bottom: 2rem;
  padding-bottom: 1.5rem;
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
}

.profile-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-placeholder {
  width: 100%;
  height: 100%;
  background-color: var(--primary-color);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2.5rem;
  font-weight: 600;
}

.profile-info {
  flex: 1;
}

.profile-info h3 {
  font-size: 1.5rem;
  font-weight: 600;
  margin: 0 0 0.5rem;
  color: var(--primary-color);
}

.user-email {
  color: var(--text-secondary);
  margin-bottom: 0.25rem;
}

.user-role {
  color: var(--text-primary);
  font-weight: 500;
  margin-bottom: 0.25rem;
}

.user-details {
  color: var(--text-secondary);
  font-size: 0.9rem;
}

.profile-details {
  margin-bottom: 2rem;
}

.profile-details h4 {
  font-size: 1.1rem;
  font-weight: 600;
  margin: 1.5rem 0 1rem;
  color: var(--text-primary);
  border-bottom: 1px solid var(--border-color-light);
  padding-bottom: 0.5rem;
}

.module-list {
  border: 1px solid var(--border-color-light);
  border-radius: var(--border-radius);
  overflow: hidden;
}

.module-list li {
  padding: 0.75rem;
  border-bottom: 1px solid var(--border-color-light);
  display: flex;
  justify-content: space-between;
}

.module-list li span {
  color: var(--text-secondary);
  font-size: 0.9rem;
}

.module-list-item {
  padding: 1rem;
  transition: background-color 0.2s ease;
}

.module-list-item:hover {
  background-color: rgba(123, 73, 255, 0.05);
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
  background-color: var(--primary-color);
  color: white;
  font-size: 0.75rem;
  font-weight: 600;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  box-shadow: 0 2px 4px rgba(123, 73, 255, 0.2);
}

.module-score {
  font-weight: 700;
  font-size: 1.1rem;
}

.excellent-score {
  color: #2ecc71;
}

.good-score {
  color: #3498db;
}

.average-score {
  color: #f1c40f;
}

.pass-score {
  color: #e67e22;
}

.fail-score {
  color: #e74c3c;
}

.empty-state {
  padding: 1rem;
  background-color: var(--bg-input);
  border-radius: var(--border-radius);
  text-align: center;
  color: var(--text-secondary);
  font-style: italic;
  margin-bottom: 1.5rem;
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
  gap: 1rem;
}

.edit-profile-btn, .update-preferences-btn {
  padding: 0.75rem 1.25rem;
  border-radius: var(--border-radius);
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
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
}

.update-preferences-btn {
  background-color: var(--primary-color);
  color: white;
  border: none;
}

.update-preferences-btn:hover {
  background-color: var(--primary-dark);
  transform: translateY(-2px);
}

/* Tutorial Styles */
.tutorial-modal {
  max-width: 650px;
}

.tutorial-step {
  margin-bottom: 20px;
}

.tutorial-step h4 {
  font-size: 1.2rem;
  margin-bottom: 10px;
  color: var(--primary-color);
}

.tutorial-step ul,
.tutorial-step ol {
  margin-left: 20px;
  margin-bottom: 15px;
}

.tutorial-step li {
  margin-bottom: 8px;
}

.tutorial-icon {
  display: flex;
  justify-content: center;
  margin: 20px 0;
}

.tutorial-icon svg {
  color: var(--primary-color);
}

.tutorial-nav-btn {
  padding: 8px 16px;
  border-radius: var(--border-radius);
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.prev-btn {
  background-color: var(--bg-input);
  color: var(--text-primary);
  border: 1px solid var(--border-color);
}

.next-btn, .done-btn {
  background-color: var(--primary-color);
  color: white;
  border: none;
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
  padding: 1rem;
  backdrop-filter: blur(2px);
}

.modal-container {
  background-color: var(--bg-card);
  border-radius: var(--border-radius-lg);
  width: 100%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: var(--shadow-lg);
  display: flex;
  flex-direction: column;
}

.modal-header {
  padding: 1.25rem 1.5rem;
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
  font-weight: 600;
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
  transition: all 0.2s ease;
}

.close-modal-btn:hover {
  background-color: var(--bg-hover);
  color: var(--text-primary);
}

.modal-body {
  padding: 1.5rem;
}

.modal-footer {
  padding: 1.25rem 1.5rem;
  border-top: 1px solid var(--border-color);
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  position: sticky;
  bottom: 0;
  background-color: var(--bg-card);
  z-index: 10;
}

/* Form styles */
.form-group {
  margin-bottom: 1.25rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: var(--text-primary);
}

.form-row {
  display: flex;
  gap: 1.25rem;
  margin-bottom: 1.25rem;
}

.form-row .form-group {
  flex: 1;
  margin-bottom: 0;
}

.checkbox-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 0.75rem;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
}

.checkbox-label input[type="checkbox"] {
  accent-color: var(--primary-color);
}

.module-selection {
  max-height: 200px;
  overflow-y: auto;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  padding: 0.75rem;
}

.module-selection .checkbox-label {
  padding: 0.5rem;
  border-bottom: 1px solid var(--border-color-light);
}

.module-selection .checkbox-label:last-child {
  border-bottom: none;
}

input[type="text"],
input[type="date"],
select,
textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  background-color: var(--bg-input);
  color: var(--text-primary);
  font-size: 1rem;
}

textarea {
  resize: vertical;
  min-height: 100px;
}

input:focus,
select:focus,
textarea:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 2px rgba(123, 73, 255, 0.1);
}

/* Event details modal */
.event-modal {
  max-width: 500px;
}

.event-details {
  display: flex;
  flex-direction: column;
}

.event-header {
  padding: 1.25rem;
  border-radius: var(--border-radius);
  color: white;
  margin-bottom: 1.25rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.event-header h4 {
  font-size: 1.2rem;
  font-weight: 600;
  margin: 0;
}

.event-module-badge {
  font-size: 0.8rem;
  padding: 0.25rem 0.5rem;
  background-color: rgba(255, 255, 255, 0.2);
  border-radius: 12px;
}

.event-info {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.event-info-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  color: var(--text-primary);
}

.event-info-item svg {
  color: var(--primary-color);
}

.event-description h5,
.event-topics h5,
.event-status h5 {
  font-size: 1rem;
  font-weight: 600;
  margin: 0 0 0.5rem;
  color: var(--text-primary);
}

.event-topics .topic-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.topic-tag {
  font-size: 0.8rem;
  padding: 0.25rem 0.5rem;
  background-color: var(--bg-input);
  border-radius: 12px;
  color: var(--text-secondary);
}

.no-topics {
  color: var(--text-secondary);
  font-size: 0.9rem;
  font-style: italic;
}

.status-badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  font-size: 0.8rem;
  border-radius: 12px;
  font-weight: 500;
}

.status-planned {
  background-color: rgba(123, 73, 255, 0.1);
  color: var(--primary-color);
}

.status-in-progress {
  background-color: rgba(76, 175, 80, 0.1);
  color: var(--success-color);
}

.status-completed {
  background-color: rgba(3, 169, 244, 0.1);
  color: #03a9f4;
}

.status-missed {
  background-color: rgba(244, 67, 54, 0.1);
  color: var(--error-color);
}

.session-actions {
  display: flex;
  gap: 1rem;
  margin-right: auto;
}

.start-session-btn,
.reschedule-btn,
.complete-session-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border-radius: var(--border-radius);
  font-weight: 500;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.start-session-btn {
  background-color: var(--success-color);
  color: white;
  border: none;
}

.start-session-btn:hover {
  background-color: #2e9c39;
}

.reschedule-btn {
  background-color: transparent;
  color: var(--text-secondary);
  border: 1px solid var(--border-color);
}

.reschedule-btn:hover {
  background-color: var(--bg-hover);
}

.complete-session-btn {
  background-color: var(--primary-color);
  color: white;
  border: none;
}

.complete-session-btn:hover {
  background-color: var(--primary-dark);
}

.close-btn {
  padding: 0.5rem 1rem;
  border-radius: var(--border-radius);
  background-color: var(--bg-input);
  color: var(--text-primary);
  border: 1px solid var(--border-color);
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.close-btn:hover {
  background-color: var(--bg-hover);
}

.session-feedback {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-right: auto;
}

.feedback-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.rating-stars {
  display: flex;
  gap: 0.25rem;
}

.star {
  color: var(--border-color);
  font-size: 1.25rem;
}

.star.filled {
  color: var(--warning-color);
}

.xp-earned {
  font-weight: 600;
}

.xp-value {
  color: var(--primary-color);
}

/* Completion modal */
.completion-modal {
  max-width: 550px;
}

.feedback-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.rating-input {
  display: flex;
  gap: 0.5rem;
}

.rating-star {
  font-size: 1.75rem;
  color: var(--border-color);
  cursor: pointer;
  transition: all 0.2s ease;
}

.rating-star:hover {
  transform: scale(1.2);
}

.rating-star.selected {
  color: var(--warning-color);
}

.topic-input-container {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
}

.add-topic-btn {
  padding: 0.75rem 1rem;
  background-color: var(--bg-input);
  color: var(--text-primary);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  cursor: pointer;
  transition: all 0.2s ease;
}

.add-topic-btn:hover {
  background-color: var(--bg-hover);
}

.topic-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.topic-tag {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.35rem 0.75rem;
  background-color: var(--bg-input);
  border-radius: 12px;
  font-size: 0.85rem;
}

.remove-topic-btn {
  background: none;
  border: none;
  color: var(--text-secondary);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  transition: all 0.2s ease;
  padding: 0;
}

.remove-topic-btn:hover {
  background-color: rgba(0, 0, 0, 0.1);
  color: var(--error-color);
}

/* Modal footer buttons */
.cancel-btn,
.create-btn,
.ai-generate-btn,
.submit-btn {
  padding: 0.75rem 1.25rem;
  border-radius: var(--border-radius);
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  min-width: 100px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.cancel-btn {
  background-color: var(--bg-input);
  color: var(--text-secondary);
  border: 1px solid var(--border-color);
}

.cancel-btn:hover {
  background-color: var(--bg-hover);
  color: var(--text-primary);
}

.create-btn,
.ai-generate-btn,
.submit-btn {
  background-color: var(--primary-color);
  color: white;
  border: none;
  box-shadow: 0 2px 4px rgba(123, 73, 255, 0.2);
}

.create-btn:hover,
.ai-generate-btn:hover,
.submit-btn:hover {
  background-color: var(--primary-dark);
  transform: translateY(-1px);
  box-shadow: 0 3px 6px rgba(123, 73, 255, 0.3);
}

.ai-generate-btn svg {
  color: white;
}

/* No data placeholder */
.no-data-placeholder {
  padding: 3rem;
  text-align: center;
  background-color: var(--bg-card);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow-md);
  margin-top: 2rem;
}

.no-data-placeholder svg {
  color: var(--primary-color);
  opacity: 0.7;
  margin-bottom: 1.5rem;
}

.no-data-placeholder h3 {
  font-size: 1.5rem;
  margin-bottom: 1rem;
  color: var(--text-primary);
}

.no-data-placeholder p {
  color: var(--text-secondary);
  max-width: 600px;
  margin: 0 auto 2rem;
  line-height: 1.6;
}

/* ========== Responsive Styles ========== */
@media (max-width: 768px) {
  .study-hub-container {
    padding: 1rem;
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

  .schedule-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .schedule-actions {
    width: 100%;
    justify-content: space-between;
  }

  .calendar-controls {
    flex-direction: column;
    align-items: flex-start;
  }

  .view-selector, .month-navigator {
    width: 100%;
  }

  .month-navigator {
    display: grid;
    grid-template-columns: auto 1fr auto;
    gap: 0.5rem;
  }

  .today-btn {
    grid-column: span 3;
  }

  .current-period {
    text-align: center;
  }

  .month-grid-header {
    grid-template-columns: repeat(7, 1fr);
  }

  .day-header {
    padding: 0.5rem 0.25rem;
    font-size: 0.8rem;
  }

  .month-grid {
    grid-auto-rows: minmax(60px, 1fr);
  }

  .day-cell {
    padding: 0.25rem;
  }

  .day-event-pill {
    padding: 0.15rem 0.35rem;
    font-size: 0.7rem;
  }

  .week-view, .day-view {
    height: 500px;
  }

  .analytics-grid {
    grid-template-columns: 1fr;
  }

  .stats-overview {
    grid-template-columns: repeat(2, 1fr);
  }

  .module-stats-header, .module-stats-row {
    grid-template-columns: 2fr repeat(3, 1fr);
  }

  .module-stat-cell:nth-child(4), .module-stat-cell:nth-child(5) {
    display: none;
  }

  .streak-section {
    grid-template-columns: 1fr;
  }

  .streak-display {
    flex-direction: column;
    align-items: center;
  }

  .level-display {
    flex-direction: column;
    align-items: center;
  }

  .achievements-grid {
    grid-template-columns: 1fr;
  }

  .profile-header {
    flex-direction: column;
    text-align: center;
  }

  .profile-avatar {
    margin: 0 auto;
  }

  .preference-item {
    flex-direction: column;
    gap: 0.25rem;
  }

  .preference-label {
    min-width: 0;
  }

  .form-row {
    flex-direction: column;
    gap: 1.25rem;
  }

  .ai-tips-section {
    padding: 1rem;
  }

  .tip-card {
    flex-direction: column;
  }

  .tip-actions {
    justify-content: center;
  }

  .modal-container {
    width: 95%;
    max-height: 85vh;
  }

  .module-list-item {
    flex-direction: column;
    align-items: flex-start;
  }

  .enrolled-badge,
  .module-score {
    margin-top: 0.5rem;
    align-self: flex-start;
  }

  .tutorial-modal {
    width: 95%;
  }
}

@media (max-width: 480px) {
  .study-hub-header h1 {
    font-size: 1.6rem;
  }

  .schedule-actions {
    flex-direction: column;
    gap: 0.5rem;
  }

  .schedule-btn, .ai-schedule-btn {
    width: 100%;
    justify-content: center;
  }

  .nav-btn, .today-btn {
    font-size: 0.8rem;
  }

  .current-period {
    font-size: 0.9rem;
  }

  .stats-overview {
    grid-template-columns: 1fr;
  }

  .streak-calendar {
    overflow-x: auto;
    justify-content: flex-start;
  }

  .calendar-day {
    min-width: 40px;
  }

  .achievements-filter {
    overflow-x: auto;
    padding-bottom: 0.5rem;
  }

  .achievements-filter button {
    white-space: nowrap;
  }

  .module-stats-header, .module-stats-row {
    grid-template-columns: 2fr 1fr;
  }

  .module-stat-cell:nth-child(3) {
    display: none;
  }

  .checkbox-grid {
    grid-template-columns: 1fr;
  }

  .session-actions {
    flex-direction: column;
    width: 100%;
  }

  .start-session-btn, .reschedule-btn, .complete-session-btn {
    width: 100%;
    justify-content: center;
  }

  .modal-body {
    padding: 1rem;
  }

  .modal-header {
    padding: 1rem;
  }

  .modal-footer {
    padding: 1rem;
    flex-direction: column;
  }

  .cancel-btn, .create-btn, .ai-generate-btn, .submit-btn {
    width: 100%;
  }

  .help-button {
    width: 100%;
    justify-content: center;
    margin-top: 0.5rem;
  }
}
</style>