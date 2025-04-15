<template>
  <div class="study-hub" :class="{ 'dark-mode': darkMode }">
    <!-- Header with title and actions -->
    <div class="study-hub-header">
      <h1>AI Study Assistant</h1>
      <div class="tab-controls">
        <button :class="{ active: activeTab === 'schedule' }" @click="activeTab = 'schedule'">Schedule</button>
        <button :class="{ active: activeTab === 'preferences' }" @click="activeTab = 'preferences'">Study Preferences</button>
        <button :class="{ active: activeTab === 'progress' }" @click="activeTab = 'progress'">Progress</button>
        <button :class="{ active: activeTab === 'stats' }" @click="activeTab = 'stats'">Analytics</button>
      </div>
      <div class="study-hub-actions">
        <button @click="generateSchedule" class="primary-action-button">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="12" y1="8" x2="12" y2="16"></line>
            <line x1="8" y1="12" x2="16" y2="12"></line>
          </svg>
          Generate Schedule
        </button>
      </div>
    </div>

    <!-- SCHEDULE TAB -->
    <div v-if="activeTab === 'schedule'" class="study-schedule-tab">
      <!-- Schedule Configuration Section -->
      <div class="schedule-config-section">
        <div class="config-card">
          <h2>Generate Study Schedule</h2>
          <div class="config-form">
            <div class="form-group">
              <label>Date Range</label>
              <div class="date-range">
                <div class="date-input">
                  <label>From</label>
                  <input type="date" v-model="scheduleConfig.startDate" />
                </div>
                <div class="date-input">
                  <label>To</label>
                  <input type="date" v-model="scheduleConfig.endDate" />
                </div>
              </div>
            </div>

            <div class="form-group">
              <label>Modules to Include</label>
              <div class="module-selection">
                <div v-for="(module, index) in availableModules" :key="index" class="module-checkbox">
                  <label class="checkbox-container">
                    <input type="checkbox" v-model="selectedModules" :value="module.id" />
                    <span class="checkbox-label">{{ module.name }}</span>
                  </label>
                </div>
              </div>
            </div>

            <div class="config-actions">
              <button @click="generateSchedule" class="generate-button">
                Generate AI Schedule
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Schedule Calendar View -->
      <div class="schedule-calendar-section">
        <div class="schedule-tools">
          <div class="view-switcher">
            <button :class="{ active: calendarView === 'week' }" @click="calendarView = 'week'">Week</button>
            <button :class="{ active: calendarView === 'day' }" @click="calendarView = 'day'">Day</button>
          </div>
          <div class="date-navigation">
            <button class="nav-button" @click="navigateCalendar('prev')">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M15 18l-6-6 6-6" />
              </svg>
            </button>
            <span class="current-date">{{ currentDateDisplay }}</span>
            <button class="nav-button" @click="navigateCalendar('next')">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M9 18l6-6-6-6" />
              </svg>
            </button>
            <button class="today-button" @click="navigateCalendar('today')">Today</button>
          </div>
          <div class="schedule-actions">
            <button class="import-button" @click="showImportCalendarDialog">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                <polyline points="17 8 12 3 7 8"></polyline>
                <line x1="12" y1="3" x2="12" y2="15"></line>
              </svg>
              Import
            </button>
          </div>
        </div>

        <!-- Week View Calendar -->
        <div v-if="calendarView === 'week'" class="week-calendar">
          <div class="calendar-header">
            <div class="time-column"></div>
            <div v-for="day in weekDays" :key="day.date" class="day-column">
              <div class="day-header">
                <div class="day-name">{{ day.name }}</div>
                <div class="day-date">{{ day.date }}</div>
              </div>
            </div>
          </div>
          <div class="calendar-body">
            <div class="time-slots">
              <div v-for="hour in hours" :key="hour" class="time-slot">
                <div class="time-label">{{ formatHour(hour) }}</div>
                <div class="slot-row">
                  <div v-for="day in weekDays" :key="day.date" class="day-slot">
                    <!-- Study sessions for this time slot -->
                    <div
                        v-for="session in getSessionsForTimeSlot(day.dateObj, hour)"
                        :key="session.id"
                        class="study-session-item"
                        :class="getSessionClasses(session)"
                        :style="getSessionStyle(session, hour)"
                        @click="showSessionDetails(session)"
                    >
                      <div class="session-time">{{ formatSessionTime(session) }}</div>
                      <div class="session-title">{{ session.module_name }}</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Day View Calendar -->
        <div v-if="calendarView === 'day'" class="day-calendar">
          <div class="calendar-header">
            <div class="time-column"></div>
            <div class="day-column full-width">
              <div class="day-header">
                <div class="day-name">{{ selectedDay.name }}</div>
                <div class="day-date">{{ selectedDay.date }}</div>
              </div>
            </div>
          </div>
          <div class="calendar-body">
            <div class="time-slots">
              <div v-for="hour in hours" :key="hour" class="time-slot">
                <div class="time-label">{{ formatHour(hour) }}</div>
                <div class="slot-row">
                  <div class="day-slot full-width">
                    <!-- Study sessions for this time slot -->
                    <div
                        v-for="session in getSessionsForTimeSlot(selectedDay.dateObj, hour)"
                        :key="session.id"
                        class="study-session-item"
                        :class="getSessionClasses(session)"
                        :style="getSessionStyle(session, hour)"
                        @click="showSessionDetails(session)"
                    >
                      <div class="session-time">{{ formatSessionTime(session) }}</div>
                      <div class="session-title">{{ session.module_name }}</div>
                      <div class="session-details">{{ session.topics ? session.topics.join(', ') : 'General review' }}</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- AI Recommendations -->
        <div class="ai-recommendations">
          <h3>AI Recommendations</h3>
          <div class="recommendation-list">
            <div v-for="(recommendation, index) in recommendations" :key="index" class="recommendation-item">
              <div class="recommendation-icon">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <circle cx="12" cy="12" r="10"></circle>
                  <line x1="12" y1="16" x2="12" y2="12"></line>
                  <line x1="12" y1="8" x2="12.01" y2="8"></line>
                </svg>
              </div>
              <div class="recommendation-text">{{ recommendation }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- PREFERENCES TAB -->
    <div v-if="activeTab === 'preferences'" class="study-preferences-tab">
      <div class="preferences-grid">
        <!-- Study Time Preferences Card -->
        <div class="preference-card">
          <h2>Study Time Preferences</h2>
          <div class="preference-form">
            <div class="form-group">
              <label>Preferred Study Times</label>
              <div class="checkbox-grid">
                <label class="checkbox-container" v-for="time in studyTimeOptions" :key="time.value">
                  <input type="checkbox" v-model="studyPreferences.preferred_times" :value="time.value">
                  <span class="checkbox-label">{{ time.label }}</span>
                </label>
              </div>
            </div>

            <div class="form-group">
              <label>Available Days</label>
              <div class="checkbox-grid">
                <label class="checkbox-container" v-for="day in daysOfWeek" :key="day.value">
                  <input type="checkbox" v-model="studyPreferences.available_days" :value="day.value">
                  <span class="checkbox-label">{{ day.label }}</span>
                </label>
              </div>
            </div>

            <div class="form-group">
              <label>Optimal Session Duration</label>
              <select v-model="studyPreferences.session_duration">
                <option value="30">30 minutes</option>
                <option value="45">45 minutes</option>
                <option value="60">60 minutes</option>
                <option value="90">90 minutes</option>
                <option value="120">2 hours</option>
              </select>
            </div>

            <div class="form-group">
              <label>Preferred Break Duration</label>
              <select v-model="studyPreferences.break_duration">
                <option value="5">5 minutes</option>
                <option value="10">10 minutes</option>
                <option value="15">15 minutes</option>
                <option value="30">30 minutes</option>
              </select>
            </div>

            <div class="form-group">
              <label>Maximum Study Sessions Per Day</label>
              <select v-model="studyPreferences.max_sessions_per_day">
                <option value="1">1 session</option>
                <option value="2">2 sessions</option>
                <option value="3">3 sessions</option>
                <option value="4">4 sessions</option>
                <option value="5">5 sessions</option>
              </select>
            </div>
          </div>
        </div>

        <!-- Environment Preferences Card -->
        <div class="preference-card">
          <h2>Environment Preferences</h2>
          <div class="preference-form">
            <div class="form-group">
              <label>Preferred Study Environment</label>
              <select v-model="studyPreferences.environment_preference">
                <option value="silent">Silent (e.g., Library)</option>
                <option value="quiet">Quiet (e.g., Study Room)</option>
                <option value="ambient">Ambient Noise (e.g., Coffee Shop)</option>
                <option value="moderate_noise">Moderate Noise (e.g., Common Area)</option>
                <option value="busy">Busy Environment (e.g., Student Center)</option>
              </select>
            </div>

            <div class="form-group">
              <label>Focus Level by Time of Day</label>
              <div class="focus-slider" v-for="time in studyTimeOptions" :key="time.value">
                <div class="focus-label">{{ time.label }}</div>
                <input
                    type="range"
                    min="1"
                    max="10"
                    v-model.number="studyPreferences.focus_levels[time.value]"
                >
                <div class="focus-value">{{ studyPreferences.focus_levels[time.value] }}</div>
              </div>
            </div>
          </div>
        </div>

        <!-- Module Preferences Card -->
        <div class="preference-card full-width">
          <h2>Module Study Preferences</h2>
          <div class="module-preferences-list">
            <div v-for="module in availableModules" :key="module.id" class="module-preference-item">
              <div class="module-info">
                <h3>{{ module.name }}</h3>
                <span class="module-code">{{ module.code }}</span>
              </div>

              <div class="module-preference-grid">
                <div class="module-preference-field">
                  <label>Priority Level</label>
                  <select v-model="modulePreferences[module.id].priority">
                    <option value="1">Very Low</option>
                    <option value="2">Low</option>
                    <option value="3">Medium</option>
                    <option value="4">High</option>
                    <option value="5">Very High</option>
                  </select>
                </div>

                <div class="module-preference-field">
                  <label>Weekly Hours Goal</label>
                  <input type="number" min="0.5" step="0.5" v-model.number="modulePreferences[module.id].weekly_hours_goal">
                </div>

                <div class="module-preference-field">
                  <label>Difficulty Rating</label>
                  <select v-model="modulePreferences[module.id].difficulty_rating">
                    <option value="1">Very Easy</option>
                    <option value="2">Easy</option>
                    <option value="3">Medium</option>
                    <option value="4">Hard</option>
                    <option value="5">Very Hard</option>
                  </select>
                </div>

                <div class="module-preference-field full-width">
                  <label>Assessment Dates</label>
                  <div class="assessment-dates">
                    <div v-for="(date, index) in modulePreferences[module.id].assessment_dates" :key="index" class="assessment-date-item">
                      <input type="date" v-model="modulePreferences[module.id].assessment_dates[index]">
                      <button @click="removeAssessmentDate(module.id, index)" class="remove-date-btn">×</button>
                    </div>
                    <button @click="addAssessmentDate(module.id)" class="add-date-btn">
                      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <line x1="12" y1="5" x2="12" y2="19"></line>
                        <line x1="5" y1="12" x2="19" y2="12"></line>
                      </svg>
                      Add Assessment Date
                    </button>
                  </div>
                </div>

                <div class="module-preference-field full-width">
                  <label>Topics to Cover</label>
                  <div class="topic-tags">
                    <div v-for="(topic, index) in modulePreferences[module.id].topics" :key="index" class="topic-tag">
                      {{ topic }}
                      <button @click="removeTopic(module.id, index)" class="remove-topic-btn">×</button>
                    </div>
                    <input
                        type="text"
                        v-model="newTopicText[module.id]"
                        @keyup.enter="addTopic(module.id)"
                        placeholder="Add a topic and press Enter"
                        class="topic-input"
                    >
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="preferences-actions">
        <button @click="savePreferences" class="save-preferences-btn">
          Save Preferences
        </button>
      </div>
    </div>

    <!-- PROGRESS TAB (Gamification) -->
    <div v-if="activeTab === 'progress'" class="study-progress-tab">
      <div class="progress-grid">
        <!-- Study Streak Card -->
        <div class="progress-card">
          <h2>Study Streak</h2>
          <div class="streak-display">
            <div class="streak-circle">
              <div class="streak-value">{{ studyStreak.current_streak }}</div>
              <div class="streak-label">days</div>
            </div>
            <div class="streak-stats">
              <div class="streak-stat">
                <div class="stat-label">Longest Streak</div>
                <div class="stat-value">{{ studyStreak.longest_streak }} days</div>
              </div>
              <div class="streak-stat">
                <div class="stat-label">Last Study Session</div>
                <div class="stat-value">{{ formatDate(studyStreak.last_study_date) }}</div>
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

        <!-- Level Progress Card -->
        <div class="progress-card">
          <h2>Study Level</h2>
          <div class="level-display">
            <div class="level-badge">
              <div class="level-value">{{ studyStats.level }}</div>
              <div class="level-title">{{ getLevelTitle(studyStats.level) }}</div>
            </div>
            <div class="xp-info">
              <div class="xp-progress-bar">
                <div class="xp-progress" :style="{ width: studyStats.level_progress_percent + '%' }">
                  {{ studyStats.level_progress_percent }}%
                </div>
              </div>
              <div class="xp-text">
                <span class="xp-current">{{ studyStats.total_xp }} XP</span>
                <span class="xp-next">{{ studyStats.xp_for_next_level }} XP to level {{ studyStats.level + 1 }}</span>
              </div>
            </div>
          </div>
          <div class="level-perks">
            <h3>Level Perks</h3>
            <div class="perk-list">
              <div v-for="(perk, index) in levelPerks" :key="index" class="perk-item"
                   :class="{ 'perk-unlocked': perk.unlocksAtLevel <= studyStats.level }">
                <div class="perk-icon">
                  <svg v-if="perk.unlocksAtLevel <= studyStats.level" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M20 6L9 17l-5-5"></path>
                  </svg>
                  <svg v-else xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="12" cy="12" r="10"></circle>
                    <line x1="12" y1="8" x2="12" y2="16"></line>
                    <line x1="8" y1="12" x2="16" y2="12"></line>
                  </svg>
                </div>
                <div class="perk-details">
                  <div class="perk-name">{{ perk.name }}</div>
                  <div class="perk-description">{{ perk.description }}</div>
                </div>
                <div class="perk-level">Level {{ perk.unlocksAtLevel }}+</div>
              </div>
            </div>
          </div>
        </div>

        <!-- Achievements Card -->
        <div class="progress-card full-width">
          <h2>Achievements</h2>
          <div class="achievements-tabs">
            <button
                v-for="category in achievementCategories"
                :key="category.value"
                :class="{ active: activeAchievementCategory === category.value }"
                @click="activeAchievementCategory = category.value"
                class="achievement-tab-btn"
            >
              {{ category.label }}
            </button>
          </div>
          <div class="achievements-grid">
            <div
                v-for="achievement in filteredAchievements"
                :key="achievement.id"
                class="achievement-item"
                :class="{
                'completed': achievement.status === 'completed',
                'unlocked': achievement.status === 'unlocked',
                'locked': achievement.status === 'locked'
              }"
            >
              <div class="achievement-icon">
                <img :src="getAchievementIconSrc(achievement)" :alt="achievement.name">
              </div>
              <div class="achievement-info">
                <div class="achievement-name">{{ achievement.name }}</div>
                <div class="achievement-desc">{{ achievement.description }}</div>
                <div class="achievement-progress-bar">
                  <div class="achievement-progress" :style="{ width: achievement.progress_percent + '%' }"></div>
                </div>
                <div class="achievement-progress-text">
                  {{ achievement.progress }} / {{ achievement.target }}
                </div>
              </div>
              <div class="achievement-status">
                <div v-if="achievement.status === 'completed'" class="completed-tag">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M20 6L9 17l-5-5"></path>
                  </svg>
                  Completed
                </div>
                <div v-else-if="achievement.status === 'unlocked'" class="unlocked-tag">In Progress</div>
                <div v-else class="locked-tag">Locked</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- STATS TAB (Analytics) -->
    <div v-if="activeTab === 'stats'" class="study-stats-tab">
      <div class="stats-grid">
        <!-- Study Overview Card -->
        <div class="stats-card">
          <h2>Study Overview</h2>
          <div class="stats-overview">
            <div class="stat-item">
              <div class="stat-value">{{ studyStats.total_sessions_completed }}</div>
              <div class="stat-label">Sessions Completed</div>
            </div>
            <div class="stat-item">
              <div class="stat-value">{{ studyStats.total_study_hours }}</div>
              <div class="stat-label">Study Hours</div>
            </div>
            <div class="stat-item">
              <div class="stat-value">{{ studyStats.completion_rate }}%</div>
              <div class="stat-label">Completion Rate</div>
            </div>
            <div class="stat-item">
              <div class="stat-value">{{ studyStats.avg_productivity_rating }}/5</div>
              <div class="stat-label">Avg. Productivity</div>
            </div>
          </div>
        </div>

        <!-- Study Time Distribution by Module -->
        <div class="stats-card">
          <h2>Study Time by Module</h2>
          <div class="chart-container">
            <!-- Chart component would go here -->
            <ModuleTimeDistributionChart :chartData="moduleTimeDistribution" />
          </div>
        </div>

        <!-- Study Sessions Timeline -->
        <div class="stats-card">
          <h2>Study Sessions Timeline</h2>
          <div class="chart-container">
            <!-- Chart component would go here -->
            <StudySessionsTimelineChart :chartData="sessionsTimeline" />
          </div>
        </div>

        <!-- Productivity Patterns -->
        <div class="stats-card">
          <h2>Productivity Patterns</h2>
          <div class="chart-container">
            <!-- Chart component would go here -->
            <ProductivityPatternsChart :chartData="productivityPatterns" />
          </div>
        </div>

        <!-- Detailed Module Stats -->
        <div class="stats-card full-width">
          <h2>Module Study Statistics</h2>
          <div class="module-stats-table">
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
              <div class="module-stat-cell">{{ module.weekly_avg }} hrs</div>
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

    <!-- SESSION DETAILS DIALOG -->
    <div v-if="showSessionDetailsDialog" class="dialog-overlay">
      <div class="dialog-content">
        <div class="dialog-header">
          <h2>Study Session Details</h2>
          <button class="close-dialog" @click="showSessionDetailsDialog = false">×</button>
        </div>
        <div class="session-details-content">
          <div class="session-details-grid">
            <div class="session-detail-item">
              <div class="detail-label">Module</div>
              <div class="detail-value">{{ selectedSession.module_name }}</div>
            </div>
            <div class="session-detail-item">
              <div class="detail-label">Date</div>
              <div class="detail-value">{{ formatDateLong(selectedSession.start_time) }}</div>
            </div>
            <div class="session-detail-item">
              <div class="detail-label">Time</div>
              <div class="detail-value">{{ formatSessionTimeLong(selectedSession) }}</div>
            </div>
            <div class="session-detail-item">
              <div class="detail-label">Status</div>
              <div class="detail-value status-badge" :class="getStatusClass(selectedSession.status)">
                {{ selectedSession.status }}
              </div>
            </div>
          </div>

          <div class="session-topics">
            <h3>Topics</h3>
            <div class="topics-list">
              <div v-for="(topic, index) in selectedSession.topics || ['General review']" :key="index" class="topic-tag">
                {{ topic }}
              </div>
            </div>
          </div>

          <div v-if="selectedSession.status === 'planned'" class="session-actions">
            <button @click="startSession(selectedSession)" class="start-session-btn">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polygon points="5 3 19 12 5 21 5 3"></polygon>
              </svg>
              Start Session
            </button>
            <button @click="rescheduleSession(selectedSession)" class="reschedule-btn">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M1 4v6h6"></path>
                <path d="M3.51 15a9 9 0 1 0 2.13-9.36L1 10"></path>
              </svg>
              Reschedule
            </button>
          </div>

          <div v-if="selectedSession.status === 'started'" class="session-actions">
            <button @click="completeSession(selectedSession)" class="complete-session-btn">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M20 6L9 17l-5-5"></path>
              </svg>
              Complete Session
            </button>
          </div>

          <div v-if="selectedSession.status === 'completed'" class="session-feedback">
            <h3>Session Feedback</h3>
            <div class="feedback-grid">
              <div class="feedback-item">
                <div class="feedback-label">Productivity Rating</div>
                <div class="rating-stars">
                  <span v-for="i in 5" :key="i" class="star" :class="{ 'filled': i <= selectedSession.productivity_rating }">★</span>
                </div>
              </div>
              <div class="feedback-item">
                <div class="feedback-label">Difficulty Rating</div>
                <div class="rating-stars">
                  <span v-for="i in 5" :key="i" class="star" :class="{ 'filled': i <= selectedSession.difficulty_rating }">★</span>
                </div>
              </div>
              <div class="feedback-item full-width">
                <div class="feedback-label">Notes</div>
                <div class="feedback-notes">{{ selectedSession.notes || 'No notes provided' }}</div>
              </div>
              <div class="feedback-item full-width" v-if="selectedSession.points_earned">
                <div class="feedback-label">Points Earned</div>
                <div class="points-earned">{{ selectedSession.points_earned }} XP</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- FEEDBACK DIALOG -->
    <div v-if="showFeedbackDialog" class="dialog-overlay">
      <div class="dialog-content">
        <div class="dialog-header">
          <h2>Session Feedback</h2>
          <button class="close-dialog" @click="showFeedbackDialog = false">×</button>
        </div>
        <div class="feedback-form">
          <div class="form-group">
            <label>Productivity Rating</label>
            <div class="rating-input">
              <span
                  v-for="i in 5"
                  :key="i"
                  class="rating-star"
                  :class="{ 'selected': feedbackData.productivity_rating >= i }"
                  @click="feedbackData.productivity_rating = i"
              >★</span>
            </div>
          </div>
          <div class="form-group">
            <label>Difficulty Rating</label>
            <div class="rating-input">
              <span
                  v-for="i in 5"
                  :key="i"
                  class="rating-star"
                  :class="{ 'selected': feedbackData.difficulty_rating >= i }"
                  @click="feedbackData.difficulty_rating = i"
              >★</span>
            </div>
          </div>
          <div class="form-group">
            <label>Session Notes</label>
            <textarea v-model="feedbackData.notes" placeholder="How was your study session? What did you learn?"></textarea>
          </div>
          <div class="dialog-actions">
            <button @click="showFeedbackDialog = false" class="cancel-btn">Cancel</button>
            <button @click="submitFeedback" class="submit-btn">Submit Feedback</button>
          </div>
        </div>
      </div>
    </div>

    <!-- IMPORT CALENDAR DIALOG -->
    <div v-if="showImportDialog" class="dialog-overlay">
      <div class="dialog-content">
        <div class="dialog-header">
          <h2>Import Calendar</h2>
          <button class="close-dialog" @click="showImportDialog = false">×</button>
        </div>
        <div class="import-form">
          <div class="form-group">
            <label>Calendar URL (iCal)</label>
            <input type="text" v-model="importData.ical_url" placeholder="https://example.com/calendar.ics">
          </div>
          <div class="form-group">
            <label>Calendar Name</label>
            <input type="text" v-model="importData.name" placeholder="University Classes">
          </div>
          <div class="form-group">
            <label class="checkbox-container">
              <input type="checkbox" v-model="importData.save_subscription">
              <span class="checkbox-label">Save subscription for auto-sync</span>
            </label>
          </div>
          <div class="dialog-actions">
            <button @click="showImportDialog = false" class="cancel-btn">Cancel</button>
            <button @click="importCalendar" class="submit-btn">Import Calendar</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
import axios from "axios";
import { notify } from "@/services/toastService.js";
import { getDarkModePreference } from "@/services/darkModeService.js";
import { API_URL } from "@/config.js";

// Import chart components - you'll need to create these separately
import ModuleTimeDistributionChart from "@/components/charts/ModuleTimeDistributionChart.vue";
import StudySessionsTimelineChart from "@/components/charts/StudySessionsTimelineChart.vue";
import ProductivityPatternsChart from "@/components/charts/ProductivityPatternsChart.vue";

export default {
  name: "StudyHub",
  components: {
    ModuleTimeDistributionChart,
    StudySessionsTimelineChart,
    ProductivityPatternsChart
  },
  data() {
    return {
      // UI control
      darkMode: false,
      activeTab: 'schedule',
      calendarView: 'week',
      activeAchievementCategory: 'all',

      // Dialog controls
      showSessionDetailsDialog: false,
      showFeedbackDialog: false,
      showImportDialog: false,

      // User data
      availableModules: [],
      selectedModules: [],

      // Calendar data
      currentWeekStart: new Date(),
      weekDays: [],
      selectedDay: {},
      hours: Array.from({ length: 14 }, (_, i) => i + 8), // 8am to 9pm

      // Study sessions
      studySessions: [],
      selectedSession: null,

      // AI recommendations
      recommendations: [],

      // Schedule config
      scheduleConfig: {
        startDate: this.formatDateValue(new Date()),
        endDate: this.formatDateValue(this.getDatePlusDays(new Date(), 7))
      },

      // Study preferences
      studyPreferences: {
        preferred_times: ['morning', 'afternoon'],
        available_days: ['monday', 'tuesday', 'wednesday', 'thursday', 'friday'],
        session_duration: 60,
        break_duration: 15,
        max_sessions_per_day: 3,
        environment_preference: 'quiet',
        focus_levels: {
          morning: 8,
          afternoon: 6,
          evening: 7,
          night: 4
        }
      },

      // Module preferences
      modulePreferences: {},
      newTopicText: {},

      // Study streak
      studyStreak: {
        current_streak: 0,
        longest_streak: 0,
        last_study_date: null,
        history: {}
      },
      recentDays: [],

      // Study stats
      studyStats: {
        total_sessions_planned: 0,
        total_sessions_completed: 0,
        total_study_time_minutes: 0,
        total_study_hours: 0,
        completion_rate: 0,
        avg_productivity_rating: 0,
        level: 1,
        total_xp: 0,
        level_progress_percent: 0,
        xp_for_next_level: 1000
      },

      // Module study stats
      moduleStudyStats: [],

      // Chart data
      moduleTimeDistribution: {
        labels: [],
        datasets: []
      },
      sessionsTimeline: {
        labels: [],
        datasets: []
      },
      productivityPatterns: {
        labels: [],
        datasets: []
      },

      // Achievements
      achievements: [],

      // Import data
      importData: {
        ical_url: '',
        name: 'Imported Calendar',
        save_subscription: true
      },

      // Feedback data
      feedbackData: {
        productivity_rating: 3,
        difficulty_rating: 3,
        notes: ''
      },

      // Level perks
      levelPerks: [
        { name: "AI Topic Suggestions", description: "Get AI-powered topic suggestions for each study session", unlocksAtLevel: 1 },
        { name: "Calendar Integration", description: "Import events from external calendars", unlocksAtLevel: 2 },
        { name: "Enhanced Analytics", description: "Unlock detailed study pattern analysis", unlocksAtLevel: 3 },
        { name: "Custom Session Templates", description: "Create and save custom study session templates", unlocksAtLevel: 5 },
        { name: "Advanced Planning", description: "Plan study schedules up to a semester ahead", unlocksAtLevel: 7 },
        { name: "Study Group Features", description: "Create and manage study groups", unlocksAtLevel: 10 }
      ]
    };
  },
  computed: {
    // Study time options
    studyTimeOptions() {
      return [
        { value: 'morning', label: 'Morning (6am-12pm)' },
        { value: 'afternoon', label: 'Afternoon (12pm-5pm)' },
        { value: 'evening', label: 'Evening (5pm-9pm)' },
        { value: 'night', label: 'Night (9pm-11pm)' }
      ];
    },

    // Days of week options
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
    },

    // Achievement categories
    achievementCategories() {
      return [
        { value: 'all', label: 'All' },
        { value: 'consistency', label: 'Consistency' },
        { value: 'time', label: 'Time Management' },
        { value: 'study', label: 'Study Goals' },
        { value: 'module', label: 'Modules' },
        { value: 'hours', label: 'Study Hours' }
      ];
    },

    // Filtered achievements based on selected category
    filteredAchievements() {
      if (this.activeAchievementCategory === 'all') {
        return this.achievements;
      }
      return this.achievements.filter(a => a.category === this.activeAchievementCategory);
    },

    // Current date display for calendar navigation
    currentDateDisplay() {
      const options = { month: 'long', year: 'numeric' };
      if (this.calendarView === 'week') {
        const weekEndDate = this.getDatePlusDays(this.currentWeekStart, 6);
        return `${this.formatDateDisplay(this.currentWeekStart)} - ${this.formatDateDisplay(weekEndDate)}`;
      } else {
        return this.formatDateDisplay(this.selectedDay.dateObj, options);
      }
    }
  },
  watch: {
    // Watch for tab changes to load required data
    activeTab(newTab) {
      if (newTab === 'schedule') {
        this.generateWeekDays();
        this.fetchStudySessions();
      } else if (newTab === 'preferences') {
        this.fetchStudyPreferences();
        this.fetchModulePreferences();
      } else if (newTab === 'progress') {
        this.fetchStudyStreak();
        this.fetchAchievements();
        this.generateRecentDays();
      } else if (newTab === 'stats') {
        this.fetchStudyStats();
        this.prepareChartData();
      }
    },

    // Watch for calendar view changes
    calendarView(newView) {
      if (newView === 'day' && (!this.selectedDay.dateObj || !this.selectedDay.date)) {
        this.selectedDay = this.weekDays[0] || {
          name: this.getDayName(new Date()),
          date: this.formatDateDisplay(new Date()),
          dateObj: new Date()
        };
      }
      this.fetchStudySessions();
    },

    // Watch for changes in selected modules to initialize preferences
    availableModules: {
      handler(modules) {
        modules.forEach(module => {
          if (!this.modulePreferences[module.id]) {
            this.modulePreferences[module.id] = {
              module_id: module.id,
              priority: 3,
              weekly_hours_goal: 3,
              difficulty_rating: 3,
              assessment_dates: [],
              topics: []
            };
            this.newTopicText[module.id] = '';
          }
        });
      },
      deep: true
    }
  },
  async mounted() {
    // Load dark mode preference
    this.darkMode = getDarkModePreference();

    // Initialize calendar dates
    this.generateWeekDays();

    // Fetch initial data
    await this.fetchAvailableModules();
    await this.fetchStudySessions();

    // Listen for dark mode changes
    window.addEventListener('darkModeChange', this.onDarkModeChange);
  },
  beforeUnmount() {
    window.removeEventListener('darkModeChange', this.onDarkModeChange);
  },
  methods: {
    // === DATE AND TIME FORMATTING ===
    formatDateValue(date) {
      const d = new Date(date);
      return d.toISOString().split('T')[0];
    },

    formatDateDisplay(date, options = { month: 'short', day: 'numeric' }) {
      const d = new Date(date);
      return d.toLocaleDateString(undefined, options);
    },

    formatDateLong(dateString) {
      const date = new Date(dateString);
      return date.toLocaleDateString(undefined, {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      });
    },

    formatDayDate(date) {
      const d = new Date(date);
      return d.getDate().toString();
    },

    formatHour(hour) {
      const displayHour = hour % 12 || 12;
      const ampm = hour < 12 ? 'AM' : 'PM';
      return `${displayHour} ${ampm}`;
    },

    formatSessionTime(session) {
      if (!session.start_time || !session.end_time) return '';

      const start = new Date(session.start_time);
      const end = new Date(session.end_time);

      const startHours = start.getHours();
      const startMinutes = start.getMinutes();
      const endHours = end.getHours();
      const endMinutes = end.getMinutes();

      const startFormatted = `${startHours % 12 || 12}:${startMinutes.toString().padStart(2, '0')}${startHours < 12 ? 'am' : 'pm'}`;
      const endFormatted = `${endHours % 12 || 12}:${endMinutes.toString().padStart(2, '0')}${endHours < 12 ? 'am' : 'pm'}`;

      return `${startFormatted} - ${endFormatted}`;
    },

    formatSessionTimeLong(session) {
      if (!session.start_time || !session.end_time) return '';

      const start = new Date(session.start_time);
      const end = new Date(session.end_time);

      const options = { hour: 'numeric', minute: '2-digit', hour12: true };
      return `${start.toLocaleTimeString(undefined, options)} - ${end.toLocaleTimeString(undefined, options)}`;
    },

    getDayName(date, options = { weekday: 'short' }) {
      return new Date(date).toLocaleDateString(undefined, options);
    },

    getDatePlusDays(date, days) {
      const newDate = new Date(date);
      newDate.setDate(newDate.getDate() + days);
      return newDate;
    },

    // === CALENDAR GENERATION ===
    generateWeekDays() {
      this.weekDays = [];

      for (let i = 0; i < 7; i++) {
        const day = this.getDatePlusDays(this.currentWeekStart, i);
        this.weekDays.push({
          name: this.getDayName(day),
          date: this.formatDateDisplay(day),
          dateObj: new Date(day)
        });
      }

      // Set selected day to first day of week by default
      if (this.calendarView === 'day' && this.weekDays.length > 0) {
        this.selectedDay = this.weekDays[0];
      }
    },

    navigateCalendar(action) {
      if (action === 'prev') {
        if (this.calendarView === 'week') {
          this.currentWeekStart = this.getDatePlusDays(this.currentWeekStart, -7);
          this.generateWeekDays();
        } else {
          this.selectedDay.dateObj = this.getDatePlusDays(this.selectedDay.dateObj, -1);
          this.selectedDay.name = this.getDayName(this.selectedDay.dateObj);
          this.selectedDay.date = this.formatDateDisplay(this.selectedDay.dateObj);
        }
      } else if (action === 'next') {
        if (this.calendarView === 'week') {
          this.currentWeekStart = this.getDatePlusDays(this.currentWeekStart, 7);
          this.generateWeekDays();
        } else {
          this.selectedDay.dateObj = this.getDatePlusDays(this.selectedDay.dateObj, 1);
          this.selectedDay.name = this.getDayName(this.selectedDay.dateObj);
          this.selectedDay.date = this.formatDateDisplay(this.selectedDay.dateObj);
        }
      } else if (action === 'today') {
        const today = new Date();
        // Calculate the start of the current week (Sunday)
        const startOfWeek = new Date(today);
        startOfWeek.setDate(today.getDate() - today.getDay());

        this.currentWeekStart = startOfWeek;
        this.generateWeekDays();

        if (this.calendarView === 'day') {
          const todayIndex = today.getDay();
          this.selectedDay = this.weekDays[todayIndex];
        }
      }

      this.fetchStudySessions();
    },

    // === SESSION MANAGEMENT ===
    getSessionsForTimeSlot(date, hour) {
      const dateString = this.formatDateValue(date);

      // For week view, we only want sessions that start in this hour
      return this.studySessions.filter(session => {
        const sessionDate = new Date(session.start_time);
        const sessionDateString = this.formatDateValue(sessionDate);

        if (sessionDateString !== dateString) return false;

        const sessionHour = sessionDate.getHours();
        return sessionHour === hour;
      });
    },

    getSessionClasses(session) {
      return {
        'planned': session.status === 'planned',
        'started': session.status === 'started',
        'completed': session.status === 'completed',
        'missed': session.status === 'missed',
        'rescheduled': session.status === 'rescheduled'
      };
    },

    getSessionStyle(session, slotHour) {
      // Calculate height based on duration
      const start = new Date(session.start_time);
      const end = new Date(session.end_time);

      const durationHours = (end - start) / (1000 * 60 * 60);

      // TODO: Handle sessions that span multiple hours
      // For now, just limit to the current hour's cell
      return {
        height: `${Math.min(durationHours, 1) * 100}%`
      };
    },

    getStatusClass(status) {
      return {
        'planned': status === 'planned',
        'started': status === 'started',
        'completed': status === 'completed',
        'missed': status === 'missed',
        'rescheduled': status === 'rescheduled'
      };
    },

    showSessionDetails(session) {
      this.selectedSession = session;
      this.showSessionDetailsDialog = true;
    },

    // === SESSION ACTIONS ===
    async startSession(session) {
      try {
        const response = await axios.put(
            `${API_URL}/study/sessions/${session.id}/status`,
            { status: 'started' },
            { withCredentials: true }
        );

        if (response.data) {
          notify({ type: "success", message: "Study session started!" });
          // Update session in list
          const index = this.studySessions.findIndex(s => s.id === session.id);
          if (index !== -1) {
            this.studySessions[index].status = 'started';
            this.selectedSession = this.studySessions[index];
          }
        }
      } catch (error) {
        console.error("Error starting session:", error);
        notify({ type: "error", message: "Failed to start study session" });
      }
    },

    async completeSession(session) {
      // Show feedback dialog and store session to complete
      this.selectedSession = session;
      this.feedbackData = {
        productivity_rating: 3,
        difficulty_rating: 3,
        notes: ''
      };
      this.showSessionDetailsDialog = false;
      this.showFeedbackDialog = true;
    },

    async submitFeedback() {
      try {
        const response = await axios.put(
            `${API_URL}/study/sessions/${this.selectedSession.id}/status`,
            {
              status: 'completed',
              productivity_rating: this.feedbackData.productivity_rating,
              difficulty_rating: this.feedbackData.difficulty_rating,
              notes: this.feedbackData.notes
            },
            { withCredentials: true }
        );

        if (response.data) {
          notify({ type: "success", message: "Study session completed!" });

          // Update session in list
          const index = this.studySessions.findIndex(s => s.id === this.selectedSession.id);
          if (index !== -1) {
            this.studySessions[index].status = 'completed';
            this.studySessions[index].productivity_rating = this.feedbackData.productivity_rating;
            this.studySessions[index].difficulty_rating = this.feedbackData.difficulty_rating;
            this.studySessions[index].notes = this.feedbackData.notes;
            this.studySessions[index].points_earned = response.data.points_earned || 0;
          }

          // Update study streak and stats
          await this.fetchStudyStreak();
          await this.fetchStudyStats();

          this.showFeedbackDialog = false;
        }
      } catch (error) {
        console.error("Error completing session:", error);
        notify({ type: "error", message: "Failed to complete study session" });
      }
    },

    async rescheduleSession(session) {
      // TODO: Implement rescheduling functionality
      notify({ type: "info", message: "Rescheduling is not implemented yet" });
    },

    // === API CALLS ===
    async fetchAvailableModules() {
      try {
        const response = await axios.get(`${API_URL}/modules`, { withCredentials: true });
        this.availableModules = response.data.filter(module => module.isCurrentlyEnrolled);

        // Initialize selected modules with all available modules
        this.selectedModules = this.availableModules.map(module => module.id);
      } catch (error) {
        console.error("Error fetching modules:", error);
        notify({ type: "error", message: "Failed to load modules" });
      }
    },

    async fetchStudySessions() {
      try {
        // Define date range based on current view
        let startDate, endDate;

        if (this.calendarView === 'week') {
          startDate = this.formatDateValue(this.currentWeekStart);
          endDate = this.formatDateValue(this.getDatePlusDays(this.currentWeekStart, 6));
        } else {
          startDate = this.formatDateValue(this.selectedDay.dateObj);
          endDate = startDate;
        }

        const response = await axios.get(
            `${API_URL}/study/sessions?start_date=${startDate}&end_date=${endDate}`,
            { withCredentials: true }
        );

        this.studySessions = response.data;
      } catch (error) {
        console.error("Error fetching study sessions:", error);
        notify({ type: "error", message: "Failed to load study sessions" });
      }
    },

    async fetchStudyPreferences() {
      try {
        const response = await axios.get(`${API_URL}/study/preferences`, { withCredentials: true });

        if (response.data) {
          // Merge with defaults to ensure all properties exist
          this.studyPreferences = {
            ...this.studyPreferences,
            ...response.data
          };
        }
      } catch (error) {
        console.error("Error fetching study preferences:", error);
        notify({ type: "error", message: "Failed to load study preferences" });
      }
    },

    async fetchModulePreferences() {
      try {
        const response = await axios.get(`${API_URL}/study/module-preferences`, { withCredentials: true });

        if (response.data && response.data.length) {
          // Create a map for easy access
          const prefMap = {};
          response.data.forEach(pref => {
            prefMap[pref.module_id] = pref;

            // Initialize topic input for this module
            this.newTopicText[pref.module_id] = '';
          });

          // Merge with existing preferences
          for (const moduleId in prefMap) {
            this.modulePreferences[moduleId] = {
              ...this.modulePreferences[moduleId] || {
                module_id: moduleId,
                priority: 3,
                weekly_hours_goal: 3,
                difficulty_rating: 3,
                assessment_dates: [],
                topics: []
              },
              ...prefMap[moduleId]
            };
          }
        }
      } catch (error) {
        console.error("Error fetching module preferences:", error);
        notify({ type: "error", message: "Failed to load module preferences" });
      }
    },

    async fetchStudyStreak() {
      try {
        const response = await axios.get(`${API_URL}/study/streak`, { withCredentials: true });

        if (response.data) {
          this.studyStreak = response.data;
          this.generateRecentDays();
        }
      } catch (error) {
        console.error("Error fetching study streak:", error);
        notify({ type: "error", message: "Failed to load study streak" });
      }
    },

    async fetchAchievements() {
      try {
        const response = await axios.get(`${API_URL}/study/achievements`, { withCredentials: true });

        if (response.data) {
          if (typeof response.data === 'object' && !Array.isArray(response.data)) {
            // Handle case where achievements are grouped by category
            const allAchievements = [];
            for (const category in response.data) {
              allAchievements.push(...response.data[category]);
            }
            this.achievements = allAchievements;
          } else {
            this.achievements = response.data;
          }
        }
      } catch (error) {
        console.error("Error fetching achievements:", error);
        notify({ type: "error", message: "Failed to load achievements" });
      }
    },

    async fetchStudyStats() {
      try {
        const response = await axios.get(`${API_URL}/study/stats`, { withCredentials: true });

        if (response.data) {
          this.studyStats = {
            ...this.studyStats,
            ...response.data
          };

          // Extract module stats from the response
          if (response.data.modules_stats) {
            this.moduleStudyStats = Object.keys(response.data.modules_stats).map(moduleId => {
              const stats = response.data.modules_stats[moduleId];
              const module = this.availableModules.find(m => m.id === moduleId) || { name: 'Unknown Module' };

              return {
                id: moduleId,
                name: module.name,
                sessions: stats.total_sessions || 0,
                hours: Math.round((stats.total_minutes || 0) / 60 * 10) / 10,
                weekly_avg: Math.round((stats.total_minutes || 0) / 60 / 4 * 10) / 10, // Assuming 4 weeks
                productivity: stats.avg_productivity || 0,
                progress: Math.min(100, Math.round((stats.total_minutes || 0) / (this.modulePreferences[moduleId]?.weekly_hours_goal * 60 * 4) * 100)) // 4 weeks
              };
            });
          }

          this.prepareChartData();
        }
      } catch (error) {
        console.error("Error fetching study stats:", error);
        notify({ type: "error", message: "Failed to load study statistics" });
      }
    },

    // === UI ACTIONS ===
    async savePreferences() {
      try {
        // Save study preferences
        await axios.put(
            `${API_URL}/study/preferences`,
            this.studyPreferences,
            { withCredentials: true }
        );

        // Save module preferences for each module
        for (const moduleId in this.modulePreferences) {
          await axios.post(
              `${API_URL}/study/module-preferences`,
              this.modulePreferences[moduleId],
              { withCredentials: true }
          );
        }

        notify({ type: "success", message: "Study preferences saved successfully" });
      } catch (error) {
        console.error("Error saving preferences:", error);
        notify({ type: "error", message: "Failed to save preferences" });
      }
    },

    async generateSchedule() {
      try {
        if (this.selectedModules.length === 0) {
          notify({ type: "warning", message: "Please select at least one module" });
          return;
        }

        // Prepare request data
        const requestData = {
          start_date: this.scheduleConfig.startDate,
          end_date: this.scheduleConfig.endDate,
          module_ids: this.selectedModules
        };

        // Show loading notification
        notify({ type: "info", message: "Generating AI schedule... This may take a moment" });

        const response = await axios.post(
            `${API_URL}/study/generate-schedule`,
            requestData,
            { withCredentials: true }
        );

        if (response.data) {
          // Update sessions
          await this.fetchStudySessions();

          // Store recommendations
          this.recommendations = response.data.recommendations || [];

          notify({ type: "success", message: `Schedule generated with ${response.data.sessions.length} study sessions` });
        }
      } catch (error) {
        console.error("Error generating schedule:", error);
        notify({ type: "error", message: "Failed to generate schedule" });
      }
    },

    async importCalendar() {
      try {
        if (!this.importData.ical_url) {
          notify({ type: "warning", message: "Please enter a calendar URL" });
          return;
        }

        const response = await axios.post(
            `${API_URL}/study/calendar/import`,
            this.importData,
            { withCredentials: true }
        );

        if (response.data) {
          notify({ type: "success", message: `Imported ${response.data.imported_events} events` });
          this.showImportDialog = false;

          // Refresh sessions to show any conflicts
          await this.fetchStudySessions();
        }
      } catch (error) {
        console.error("Error importing calendar:", error);
        notify({ type: "error", message: "Failed to import calendar" });
      }
    },

    // === MODULE PREFERENCE MANAGEMENT ===
    addAssessmentDate(moduleId) {
      if (!this.modulePreferences[moduleId].assessment_dates) {
        this.modulePreferences[moduleId].assessment_dates = [];
      }

      const today = new Date();
      const nextMonth = new Date(today);
      nextMonth.setMonth(today.getMonth() + 1);

      this.modulePreferences[moduleId].assessment_dates.push(
          this.formatDateValue(nextMonth)
      );
    },

    removeAssessmentDate(moduleId, index) {
      this.modulePreferences[moduleId].assessment_dates.splice(index, 1);
    },

    addTopic(moduleId) {
      if (!this.newTopicText[moduleId] || this.newTopicText[moduleId].trim() === '') return;

      if (!this.modulePreferences[moduleId].topics) {
        this.modulePreferences[moduleId].topics = [];
      }

      this.modulePreferences[moduleId].topics.push(this.newTopicText[moduleId].trim());
      this.newTopicText[moduleId] = '';
    },

    removeTopic(moduleId, index) {
      this.modulePreferences[moduleId].topics.splice(index, 1);
    },

    // === UTILS ===
    showImportCalendarDialog() {
      this.importData = {
        ical_url: '',
        name: 'Imported Calendar',
        save_subscription: true
      };
      this.showImportDialog = true;
    },

    generateRecentDays() {
      this.recentDays = [];
      const today = new Date();
      const history = this.studyStreak.history || {};

      // Generate last 14 days
      for (let i = 13; i >= 0; i--) {
        const day = this.getDatePlusDays(today, -i);
        const dateStr = this.formatDateValue(day);

        this.recentDays.push({
          date: day,
          studied: history[dateStr] === true
        });
      }
    },

    getLevelTitle(level) {
      const titles = [
        'Beginner',
        'Novice Scholar',
        'Dedicated Student',
        'Academic Adept',
        'Knowledge Master',
        'Academic Legend'
      ];

      if (level <= 5) return titles[0];
      if (level <= 15) return titles[1];
      if (level <= 30) return titles[2];
      if (level <= 50) return titles[3];
      return titles[4];
    },

    getAchievementIconSrc(achievement) {
      // You would implement this to return the proper icon path based on the achievement
      // For now, return a placeholder
      return achievement.badge_icon || `/icons/achievements/${achievement.category}_default.svg`;
    },

    prepareChartData() {
      // Module Time Distribution
      this.moduleTimeDistribution = {
        labels: this.moduleStudyStats.map(m => m.name),
        datasets: [{
          label: 'Study Hours',
          data: this.moduleStudyStats.map(m => m.hours),
          backgroundColor: [
            'rgba(123, 73, 255, 0.7)',
            'rgba(46, 204, 113, 0.7)',
            'rgba(52, 152, 219, 0.7)',
            'rgba(155, 89, 182, 0.7)',
            'rgba(241, 196, 15, 0.7)',
            'rgba(230, 126, 34, 0.7)',
            'rgba(231, 76, 60, 0.7)'
          ]
        }]
      };

      // Session Timeline
      // Generate labels for last 7 days
      const labels = [];
      const sessionCounts = [];
      const today = new Date();

      for (let i = 6; i >= 0; i--) {
        const day = this.getDatePlusDays(today, -i);
        labels.push(this.formatDateDisplay(day));

        // Count sessions on this day
        const dateStr = this.formatDateValue(day);
        const count = this.studySessions.filter(session => {
          const sessionDate = this.formatDateValue(new Date(session.start_time));
          return sessionDate === dateStr && session.status === 'completed';
        }).length;

        sessionCounts.push(count);
      }

      this.sessionsTimeline = {
        labels: labels,
        datasets: [{
          label: 'Completed Sessions',
          data: sessionCounts,
          backgroundColor: 'rgba(123, 73, 255, 0.2)',
          borderColor: 'rgba(123, 73, 255, 1)',
          borderWidth: 2,
          tension: 0.3
        }]
      };

      // Productivity Patterns
      this.productivityPatterns = {
        labels: ['Morning', 'Afternoon', 'Evening', 'Night'],
        datasets: [{
          label: 'Average Productivity',
          data: [
            this.calculateAvgProductivity('morning'),
            this.calculateAvgProductivity('afternoon'),
            this.calculateAvgProductivity('evening'),
            this.calculateAvgProductivity('night')
          ],
          backgroundColor: 'rgba(46, 204, 113, 0.2)',
          borderColor: 'rgba(46, 204, 113, 1)',
          borderWidth: 2
        }]
      };
    },

    calculateAvgProductivity(timeOfDay) {
      // Filter completed sessions by time of day
      const sessions = this.studySessions.filter(session => {
        if (session.status !== 'completed' || !session.productivity_rating) return false;

        const sessionHour = new Date(session.start_time).getHours();

        if (timeOfDay === 'morning') return sessionHour >= 6 && sessionHour < 12;
        if (timeOfDay === 'afternoon') return sessionHour >= 12 && sessionHour < 17;
        if (timeOfDay === 'evening') return sessionHour >= 17 && sessionHour < 21;
        if (timeOfDay === 'night') return sessionHour >= 21 || sessionHour < 6;

        return false;
      });

      if (sessions.length === 0) return 0;

      // Calculate average
      const total = sessions.reduce((sum, session) => sum + session.productivity_rating, 0);
      return Math.round((total / sessions.length) * 10) / 10;
    },

    // Handle dark mode change
    onDarkModeChange(event) {
      this.darkMode = event.detail.isDark;
    }
  }
};
</script>

<style scoped>
/* ========== Base Study Hub Styles ========== */
.study-hub {
  min-height: 100vh;
  background-color: var(--bg-light);
  color: var(--text-primary);
  transition: background-color var(--transition-speed) ease,
  color var(--transition-speed) ease;
  --bg-light: #f8f9fa;
  --bg-card: #ffffff;
  --bg-accent: #f1f3f9;
  --bg-input: #ffffff;
  --text-primary: #333333;
  --text-secondary: #667085;
  --text-muted: #94a3b8;
  --primary-color: #7b49ff;
  --primary-dark: #6038cc;
  --primary-light: #9a73ff;
  --success-color: #22c55e;
  --info-color: #3b82f6;
  --warning-color: #f59e0b;
  --danger-color: #ef4444;
  --border-color: #e2e8f0;
  --border-color-light: #f1f5f9;
  --border-radius: 8px;
  --border-radius-lg: 12px;
  --transition-speed: 0.3s;
  --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 12px rgba(0, 0, 0, 0.07);
  --shadow-lg: 0 10px 25px rgba(0, 0, 0, 0.1);
  --font-main: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
}

.study-hub.dark-mode {
  --bg-light: #111827;
  --bg-card: #1f2937;
  --bg-accent: #2d3748;
  --bg-input: #374151;
  --text-primary: #f1f5f9;
  --text-secondary: #cbd5e1;
  --text-muted: #94a3b8;
  --primary-color: #8b5cf6;
  --primary-dark: #7c3aed;
  --primary-light: #a78bfa;
  --border-color: #374151;
  --border-color-light: #4b5563;
}

/* ========== Header Styles ========== */
.study-hub-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  margin-bottom: 2rem;
  gap: 1rem;
}

.study-hub-header h1 {
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--primary-dark);
  margin: 0;
  letter-spacing: -0.5px;
  position: relative;
}

.study-hub-header h1::after {
  content: '';
  position: absolute;
  bottom: -8px;
  left: 0;
  width: 40px;
  height: 3px;
  background: var(--primary-color);
  border-radius: 4px;
}

.dark-mode .study-hub-header h1 {
  color: var(--primary-light);
}

.tab-controls {
  display: flex;
  gap: 0.5rem;
  background: var(--bg-card);
  border-radius: 24px;
  padding: 0.25rem;
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--border-color-light);
}

.tab-controls button {
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

.study-hub-actions {
  display: flex;
  gap: 0.75rem;
}

.primary-action-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.6rem 1.25rem;
  background: var(--primary-color);
  color: white;
  border: none;
  border-radius: var(--border-radius);
  font-weight: 600;
  cursor: pointer;
  transition: all 0.25s ease;
  box-shadow: 0 3px 10px rgba(123, 73, 255, 0.2);
}

.primary-action-button:hover {
  background: var(--primary-dark);
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(123, 73, 255, 0.3);
}

.primary-action-button svg {
  flex-shrink: 0;
}

/* ========== Schedule Tab Styles ========== */
.study-schedule-tab {
  display: grid;
  grid-template-columns: 300px 1fr;
  gap: 1.5rem;
}

/* ========== Schedule Config Styles ========== */
.schedule-config-section {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.config-card {
  background: var(--bg-card);
  border-radius: var(--border-radius-lg);
  padding: 1.5rem;
  box-shadow: var(--shadow-md);
  border: 1px solid var(--border-color-light);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.config-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

.config-card h2 {
  margin: 0 0 1.5rem;
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--primary-dark);
  position: relative;
  display: inline-block;
}

.config-card h2::after {
  content: '';
  position: absolute;
  bottom: -6px;
  left: 0;
  width: 30px;
  height: 3px;
  background: var(--primary-color);
  border-radius: 4px;
}

.config-form {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}

.form-group label {
  font-weight: 600;
  color: var(--text-primary);
  font-size: 0.9rem;
}

.date-range {
  display: flex;
  gap: 0.75rem;
}

.date-input {
  flex: 1;
}

.date-input label {
  font-size: 0.8rem;
  color: var(--text-secondary);
  margin-bottom: 0.25rem;
  display: block;
}

.date-input input {
  width: 100%;
  padding: 0.6rem 0.75rem;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  font-size: 0.9rem;
  background-color: var(--bg-input);
  color: var(--text-primary);
  transition: all var(--transition-speed) ease;
}

.date-input input:focus {
  border-color: var(--primary-color);
  outline: none;
  box-shadow: 0 0 0 3px rgba(123, 73, 255, 0.15);
}

.module-selection {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  max-height: 200px;
  overflow-y: auto;
  background: var(--bg-accent);
  border-radius: var(--border-radius);
  padding: 0.75rem;
}

.module-checkbox {
  display: flex;
  align-items: center;
}

.checkbox-container {
  display: flex;
  align-items: center;
  cursor: pointer;
  font-size: 0.9rem;
  color: var(--text-primary);
}

.checkbox-container input[type="checkbox"] {
  margin-right: 0.5rem;
  cursor: pointer;
  accent-color: var(--primary-color);
}

.config-actions {
  margin-top: 1rem;
}

.generate-button {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  padding: 0.75rem 1rem;
  background: var(--primary-color);
  color: white;
  border: none;
  border-radius: var(--border-radius);
  font-weight: 600;
  cursor: pointer;
  transition: all 0.25s ease;
  box-shadow: 0 3px 10px rgba(123, 73, 255, 0.2);
}

.generate-button:hover {
  background: var(--primary-dark);
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(123, 73, 255, 0.3);
}

/* ========== Calendar Styles ========== */
.schedule-calendar-section {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  flex: 1;
}

.schedule-tools {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: var(--bg-card);
  border-radius: var(--border-radius-lg);
  padding: 1rem 1.5rem;
  box-shadow: var(--shadow-md);
  border: 1px solid var(--border-color-light);
}

.view-switcher {
  display: flex;
  gap: 0.5rem;
  background: var(--bg-accent);
  border-radius: 20px;
  padding: 0.25rem;
}

.view-switcher button {
  padding: 0.5rem 1rem;
  border: none;
  background: transparent;
  color: var(--text-secondary);
  border-radius: 16px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s ease;
  font-size: 0.85rem;
}

.view-switcher button.active {
  background: var(--primary-color);
  color: white;
  box-shadow: 0 2px 6px rgba(123, 73, 255, 0.25);
}

.view-switcher button:hover:not(.active) {
  background: rgba(123, 73, 255, 0.1);
  color: var(--primary-color);
}

.date-navigation {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.nav-button {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  border: 1px solid var(--border-color);
  background: var(--bg-card);
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.2s ease;
}

.nav-button:hover {
  background: var(--primary-color);
  color: white;
  border-color: var(--primary-color);
  transform: translateY(-2px);
  box-shadow: 0 3px 8px rgba(123, 73, 255, 0.25);
}

.current-date {
  font-weight: 600;
  color: var(--text-primary);
  min-width: 200px;
  text-align: center;
}

.today-button {
  padding: 0.4rem 0.85rem;
  border: 1px solid var(--border-color);
  border-radius: 16px;
  background: var(--bg-accent);
  color: var(--text-secondary);
  font-size: 0.85rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.today-button:hover {
  background: var(--primary-color);
  color: white;
  border-color: var(--primary-color);
  transform: translateY(-2px);
  box-shadow: 0 3px 8px rgba(123, 73, 255, 0.25);
}

.import-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  background: var(--bg-card);
  color: var(--text-secondary);
  font-size: 0.85rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.import-button:hover {
  background: rgba(123, 73, 255, 0.1);
  color: var(--primary-color);
  border-color: var(--primary-color);
  transform: translateY(-2px);
}

/* Week Calendar Styles */
.week-calendar, .day-calendar {
  background: var(--bg-card);
  border-radius: var(--border-radius-lg);
  overflow: hidden;
  box-shadow: var(--shadow-md);
  border: 1px solid var(--border-color-light);
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 600px;
}

.calendar-header {
  display: flex;
  border-bottom: 1px solid var(--border-color);
}

.time-column {
  width: 60px;
  flex-shrink: 0;
  border-right: 1px solid var(--border-color-light);
}

.day-column {
  flex: 1;
  min-width: 0;
  border-right: 1px solid var(--border-color-light);
}

.day-column:last-child {
  border-right: none;
}

.full-width {
  width: 100%;
}

.day-header {
  padding: 0.75rem;
  text-align: center;
  background: var(--bg-accent);
}

.day-name {
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 0.25rem;
}

.day-date {
  font-size: 0.85rem;
  color: var(--text-secondary);
}

.calendar-body {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
}

.time-slots {
  display: flex;
  flex-direction: column;
  flex: 1;
}

.time-slot {
  display: flex;
  min-height: 60px;
  border-bottom: 1px solid var(--border-color-light);
}

.time-slot:last-child {
  border-bottom: none;
}

.time-label {
  width: 60px;
  padding: 0.5rem;
  text-align: center;
  font-size: 0.8rem;
  color: var(--text-secondary);
  font-weight: 500;
  border-right: 1px solid var(--border-color-light);
}

.slot-row {
  display: flex;
  flex: 1;
}

.day-slot {
  flex: 1;
  border-right: 1px solid var(--border-color-light);
  position: relative;
  padding: 0.25rem;
  min-width: 0;
}

.day-slot:last-child {
  border-right: none;
}

/* Study Session Styles */
.study-session-item {
  position: absolute;
  left: 2px;
  right: 2px;
  padding: 0.5rem;
  border-radius: var(--border-radius);
  background: rgba(123, 73, 255, 0.1);
  border-left: 3px solid var(--primary-color);
  cursor: pointer;
  overflow: hidden;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  z-index: 1;
}

.study-session-item:hover {
  transform: translateY(-2px) scale(1.02);
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.1);
  z-index: 10;
}

.study-session-item.planned {
  background: rgba(123, 73, 255, 0.1);
  border-left-color: var(--primary-color);
}

.study-session-item.started {
  background: rgba(46, 204, 113, 0.1);
  border-left-color: var(--success-color);
}

.study-session-item.completed {
  background: rgba(52, 152, 219, 0.1);
  border-left-color: var(--info-color);
}

.study-session-item.missed {
  background: rgba(231, 76, 60, 0.1);
  border-left-color: var(--danger-color);
}

.study-session-item.rescheduled {
  background: rgba(241, 196, 15, 0.1);
  border-left-color: var(--warning-color);
}

.session-time {
  font-size: 0.75rem;
  color: var(--text-secondary);
  font-weight: 500;
  margin-bottom: 0.25rem;
}

.session-title {
  font-weight: 600;
  color: var(--text-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.session-details {
  font-size: 0.75rem;
  color: var(--text-secondary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  margin-top: 0.25rem;
}

/* AI Recommendations */
.ai-recommendations {
  background: var(--bg-card);
  border-radius: var(--border-radius-lg);
  padding: 1.5rem;
  box-shadow: var(--shadow-md);
  border: 1px solid var(--border-color-light);
}

.ai-recommendations h3 {
  margin: 0 0 1.25rem;
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--primary-dark);
  position: relative;
  display: inline-block;
}

.ai-recommendations h3::after {
  content: '';
  position: absolute;
  bottom: -6px;
  left: 0;
  width: 25px;
  height: 3px;
  background: var(--primary-color);
  border-radius: 4px;
}

.recommendation-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.recommendation-item {
  display: flex;
  gap: 0.75rem;
  padding: 1rem;
  background: var(--bg-accent);
  border-radius: var(--border-radius);
  border-left: 3px solid var(--primary-color);
  transition: transform 0.2s ease;
}

.recommendation-item:hover {
  transform: translateX(5px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.recommendation-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  flex-shrink: 0;
  border-radius: 50%;
  background: rgba(123, 73, 255, 0.1);
  color: var(--primary-color);
}

.recommendation-text {
  font-size: 0.9rem;
  color: var(--text-primary);
  line-height: 1.5;
}

/* ========== Preferences Tab Styles ========== */
.study-preferences-tab {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.preferences-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
}

.preference-card {
  background: var(--bg-card);
  border-radius: var(--border-radius-lg);
  padding: 1.5rem;
  box-shadow: var(--shadow-md);
  border: 1px solid var(--border-color-light);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.preference-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

.preference-card h2 {
  margin: 0 0 1.5rem;
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--primary-dark);
  position: relative;
  display: inline-block;
}

.preference-card h2::after {
  content: '';
  position: absolute;
  bottom: -6px;
  left: 0;
  width: 30px;
  height: 3px;
  background: var(--primary-color);
  border-radius: 4px;
}

.full-width {
  grid-column: 1 / -1;
}

.preference-form {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.checkbox-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.75rem;
}

.form-group select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  background-color: var(--bg-input);
  color: var(--text-primary);
  font-size: 0.95rem;
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='%23666' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 0.75rem center;
  background-size: 16px;
}

.form-group select:focus {
  border-color: var(--primary-color);
  outline: none;
  box-shadow: 0 0 0 3px rgba(123, 73, 255, 0.15);
}

.focus-slider {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 0.5rem;
}

.focus-label {
  width: 100px;
  font-size: 0.9rem;
  color: var(--text-secondary);
}

.focus-slider input[type="range"] {
  flex: 1;
  accent-color: var(--primary-color);
}

.focus-value {
  width: 25px;
  text-align: center;
  font-weight: 600;
  color: var(--primary-color);
}

/* Module Preferences Styles */
.module-preferences-list {
  display: flex;
  flex-direction: column;
  gap: 2rem;
  max-height: 600px;
  overflow-y: auto;
  padding-right: 0.5rem;
}

.module-preference-item {
  background: var(--bg-accent);
  border-radius: var(--border-radius);
  padding: 1.25rem;
  border-left: 3px solid var(--primary-color);
}

.module-info {
  margin-bottom: 1.25rem;
}

.module-info h3 {
  margin: 0 0 0.5rem;
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--text-primary);
}

.module-code {
  font-size: 0.85rem;
  color: var(--text-secondary);
  background: var(--bg-card);
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
  font-weight: 500;
}

.module-preference-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
}

.module-preference-field {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.module-preference-field.full-width {
  grid-column: 1 / -1;
}

.module-preference-field label {
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--text-primary);
}

.module-preference-field input[type="number"] {
  padding: 0.75rem;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  background-color: var(--bg-input);
  color: var(--text-primary);
  font-size: 0.95rem;
}

.module-preference-field input[type="number"]:focus {
  border-color: var(--primary-color);
  outline: none;
  box-shadow: 0 0 0 3px rgba(123, 73, 255, 0.15);
}

.assessment-dates {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.assessment-date-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.assessment-date-item input[type="date"] {
  flex: 1;
  padding: 0.6rem 0.75rem;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  font-size: 0.9rem;
  background-color: var(--bg-input);
  color: var(--text-primary);
}

.assessment-date-item input[type="date"]:focus {
  border-color: var(--primary-color);
  outline: none;
  box-shadow: 0 0 0 3px rgba(123, 73, 255, 0.15);
}

.remove-date-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  border: none;
  background: var(--danger-color);
  color: white;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.remove-date-btn:hover {
  background: var(--danger-color);
  transform: scale(1.1);
}

.add-date-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.6rem;
  background: transparent;
  color: var(--primary-color);
  border: 1px dashed var(--primary-color);
  border-radius: var(--border-radius);
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.add-date-btn:hover {
  background: rgba(123, 73, 255, 0.05);
  transform: scale(1.02);
}

.topic-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  align-items: center;
}

.topic-tag {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  padding: 0.35rem 0.75rem;
  background: rgba(123, 73, 255, 0.1);
  color: var(--primary-color);
  border-radius: 16px;
  font-size: 0.85rem;
  font-weight: 500;
}

.remove-topic-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  border: none;
  background: var(--primary-color);
  color: white;
  font-size: 0.75rem;
  cursor: pointer;
  transition: all 0.2s ease;
  line-height: 1;
}

.remove-topic-btn:hover {
  background: var(--primary-dark);
  transform: scale(1.1);
}

.topic-input {
  flex: 1;
  min-width: 200px;
  padding: 0.5rem 0.75rem;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  font-size: 0.9rem;
  background-color: var(--bg-input);
  color: var(--text-primary);
}

.topic-input:focus {
  border-color: var(--primary-color);
  outline: none;
  box-shadow: 0 0 0 3px rgba(123, 73, 255, 0.15);
}

.preferences-actions {
  display: flex;
  justify-content: center;
  margin-top: 1rem;
}

.save-preferences-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0.85rem 2rem;
  background: var(--primary-color);
  color: white;
  border: none;
  border-radius: var(--border-radius);
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.25s ease;
  box-shadow: 0 3px 10px rgba(123, 73, 255, 0.2);
}

.save-preferences-btn:hover {
  background: var(--primary-dark);
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(123, 73, 255, 0.3);
}

/* ========== Progress Tab Styles ========== */
.study-progress-tab {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.progress-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
}

.progress-card {
  background: var(--bg-card);
  border-radius: var(--border-radius-lg);
  padding: 1.5rem;
  box-shadow: var(--shadow-md);
  border: 1px solid var(--border-color-light);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.progress-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

.progress-card h2 {
  margin: 0 0 1.5rem;
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--primary-dark);
  position: relative;
  display: inline-block;
}

.progress-card h2::after {
  content: '';
  position: absolute;
  bottom: -6px;
  left: 0;
  width: 30px;
  height: 3px;
  background: var(--primary-color);
  border-radius: 4px;
}

/* Streak Display */
.streak-display {
  display: flex;
  align-items: center;
  gap: 2rem;
  margin-bottom: 1.5rem;
}

.streak-circle {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  background: conic-gradient(
      var(--primary-color) 0deg,
      rgba(123, 73, 255, 0.2) 1deg
  );
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  position: relative;
}

.streak-circle::before {
  content: '';
  position: absolute;
  top: 10px;
  left: 10px;
  right: 10px;
  bottom: 10px;
  border-radius: 50%;
  background: var(--bg-card);
  box-shadow: inset 0 2px 8px rgba(0, 0, 0, 0.1);
}

.streak-value {
  position: relative;
  font-size: 2.5rem;
  font-weight: 800;
  color: var(--primary-dark);
  margin-bottom: 0.25rem;
  line-height: 1;
}

.streak-label {
  position: relative;
  font-size: 0.85rem;
  color: var(--text-secondary);
  font-weight: 500;
}

.streak-stats {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  flex: 1;
}

.streak-stat {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.85rem 1.25rem;
  background: var(--bg-accent);
  border-radius: var(--border-radius);
  transition: all 0.25s ease;
  border-left: 3px solid var(--primary-color);
}

.streak-stat:hover {
  transform: translateX(5px);
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.05);
}

.stat-label {
  font-weight: 500;
  color: var(--text-secondary);
}

.stat-value {
  font-weight: 700;
  color: var(--primary-dark);
  font-size: 1rem;
}

.streak-calendar {
  display: flex;
  justify-content: space-between;
  background: var(--bg-accent);
  border-radius: var(--border-radius);
  padding: 1rem;
  overflow-x: auto;
}

.calendar-day {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem;
  min-width: 35px;
}

.day-date {
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--text-primary);
}

.day-indicator {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  justify-content: center;
}

.day-indicator.studied {
  background: var(--primary-color);
  border-color: var(--primary-color);
  color: white;
}

/* Level Display */
.level-display {
  display: flex;
  align-items: center;
  gap: 2rem;
  margin-bottom: 1.5rem;
}

.level-badge {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 120px;
  height: 120px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--primary-color), var(--primary-light));
  color: white;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
}

.level-value {
  font-size: 3rem;
  font-weight: 800;
  line-height: 1;
  margin-bottom: 0.5rem;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.level-title {
  font-size: 0.8rem;
  font-weight: 600;
  text-align: center;
  max-width: 90%;
}

.xp-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.xp-progress-bar {
  height: 1.75rem;
  background: var(--bg-accent);
  border-radius: var(--border-radius);
  overflow: hidden;
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.05);
}

.xp-progress {
  height: 100%;
  background: linear-gradient(to right, var(--primary-color), var(--primary-light));
  color: white;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  padding-right: 0.85rem;
  font-weight: 700;
  font-size: 0.9rem;
  transition: width 0.5s ease;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}

.xp-text {
  display: flex;
  justify-content: space-between;
}

.xp-current {
  font-weight: 700;
  color: var(--primary-dark);
}

.xp-next {
  color: var(--text-secondary);
  font-size: 0.9rem;
}

.level-perks {
  margin-top: 2rem;
}

.level-perks h3 {
  margin: 0 0 1rem;
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--text-primary);
}

.perk-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  background: var(--bg-accent);
  border-radius: var(--border-radius);
  padding: 0.75rem;
  max-height: 250px;
  overflow-y: auto;
}

.perk-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem;
  border-radius: var(--border-radius);
  background: var(--bg-card);
  border-left: 3px solid var(--border-color);
  transition: all 0.2s ease;
}

.perk-item:hover {
  transform: translateX(5px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.perk-item.perk-unlocked {
  border-left-color: var(--success-color);
}

.perk-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  flex-shrink: 0;
  border-radius: 50%;
  color: var(--text-muted);
}

.perk-unlocked .perk-icon {
  background: rgba(46, 204, 113, 0.1);
  color: var(--success-color);
}

.perk-details {
  flex: 1;
  min-width: 0;
}

.perk-name {
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 0.25rem;
}

.perk-description {
  font-size: 0.85rem;
  color: var(--text-secondary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.perk-level {
  font-size: 0.8rem;
  color: var(--text-muted);
  padding: 0.25rem 0.5rem;
  background: var(--bg-accent);
  border-radius: 12px;
  font-weight: 500;
}

.perk-unlocked .perk-level {
  background: rgba(46, 204, 113, 0.1);
  color: var(--success-color);
}

/* Achievements Styles */
.achievements-tabs {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1.25rem;
  overflow-x: auto;
  padding-bottom: 0.5rem;
}

.achievement-tab-btn {
  padding: 0.5rem 1rem;
  border: none;
  background: var(--bg-accent);
  color: var(--text-secondary);
  border-radius: 20px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s ease;
  font-size: 0.9rem;
  white-space: nowrap;
}

.achievement-tab-btn.active {
  background: var(--primary-color);
  color: white;
  box-shadow: 0 2px 6px rgba(123, 73, 255, 0.25);
}

.achievement-tab-btn:hover:not(.active) {
  background: rgba(123, 73, 255, 0.1);
  color: var(--primary-color);
}

.achievements-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.25rem;
  max-height: 500px;
  overflow-y: auto;
  padding-right: 0.5rem;
}

.achievement-item {
  display: flex;
  flex-direction: column;
  border-radius: var(--border-radius);
  background: var(--bg-accent);
  overflow: hidden;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  position: relative;
}

.achievement-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

.achievement-item.completed {
  border: 1px solid rgba(46, 204, 113, 0.3);
}

.achievement-item.unlocked {
  border: 1px solid rgba(123, 73, 255, 0.3);
}

.achievement-item.locked {
  border: 1px solid var(--border-color);
  opacity: 0.8;
}

.achievement-icon {
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, var(--bg-card), var(--bg-accent));
  padding: 1rem;
}

.achievement-icon img {
  max-height: 100%;
  max-width: 100%;
  opacity: 1;
}

.achievement-item.locked .achievement-icon img {
  opacity: 0.5;
  filter: grayscale(100%);
}

.achievement-info {
  padding: 1rem;
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.achievement-name {
  font-weight: 700;
  color: var(--text-primary);
}

.achievement-desc {
  font-size: 0.85rem;
  color: var(--text-secondary);
  margin-bottom: 0.5rem;
  line-height: 1.4;
}

.achievement-progress-bar {
  height: 6px;
  background: var(--bg-card);
  border-radius: 3px;
  overflow: hidden;
  box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.05);
}

.achievement-progress {
  height: 100%;
  background: linear-gradient(to right, var(--primary-color), var(--primary-light));
  border-radius: 3px;
  transition: width 0.5s ease;
}

.achievement-item.completed .achievement-progress {
  background: linear-gradient(to right, var(--success-color), #27ae60);
}

.achievement-progress-text {
  font-size: 0.75rem;
  color: var(--text-muted);
  text-align: right;
}

.achievement-status {
  padding: 0.5rem 1rem;
  background: var(--bg-card);
  border-top: 1px solid var(--border-color-light);
}

.completed-tag, .unlocked-tag, .locked-tag {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
}

.completed-tag {
  background: rgba(46, 204, 113, 0.1);
  color: var(--success-color);
}

.unlocked-tag {
  background: rgba(123, 73, 255, 0.1);
  color: var(--primary-color);
}

.locked-tag {
  background: var(--bg-accent);
  color: var(--text-muted);
}

/* ========== Stats Tab Styles ========== */
.study-stats-tab {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
}

.stats-card {
  background: var(--bg-card);
  border-radius: var(--border-radius-lg);
  padding: 1.5rem;
  box-shadow: var(--shadow-md);
  border: 1px solid var(--border-color-light);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.stats-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

.stats-card h2 {
  margin: 0 0 1.5rem;
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--primary-dark);
  position: relative;
  display: inline-block;
}

.stats-card h2::after {
  content: '';
  position: absolute;
  bottom: -6px;
  left: 0;
  width: 30px;
  height: 3px;
  background: var(--primary-color);
  border-radius: 4px;
}

.stats-overview {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.25rem;
  padding: 1rem;
}

.stat-item {
  text-align: center;
  padding: 1.25rem;
  background: var(--bg-accent);
  border-radius: var(--border-radius);
  transition: transform 0.2s ease;
}

.stat-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
}

.stat-item:nth-child(1) { border-top: 3px solid var(--primary-color); }
.stat-item:nth-child(2) { border-top: 3px solid var(--success-color); }
.stat-item:nth-child(3) { border-top: 3px solid var(--info-color); }
.stat-item:nth-child(4) { border-top: 3px solid var(--warning-color); }

.stat-value {
  font-size: 1.75rem;
  font-weight: 800;
  color: var(--primary-dark);
  margin-bottom: 0.5rem;
}

.stat-label {
  font-size: 0.9rem;
  color: var(--text-secondary);
  font-weight: 500;
}

.chart-container {
  height: 300px;
  position: relative;
}

/* Module Stats Table */
.module-stats-table {
  overflow-x: auto;
}

.module-stats-header {
  display: grid;
  grid-template-columns: 2fr repeat(5, 1fr);
  background: var(--bg-accent);
  font-weight: 600;
  color: var(--text-primary);
  padding: 0.75rem;
  border-radius: var(--border-radius) var(--border-radius) 0 0;
}

.module-stats-row {
  display: grid;
  grid-template-columns: 2fr repeat(5, 1fr);
  padding: 0.75rem;
  border-bottom: 1px solid var(--border-color-light);
  align-items: center;
  transition: background-color 0.2s ease;
}

.module-stats-row:last-child {
  border-bottom: none;
  border-radius: 0 0 var(--border-radius) var(--border-radius);
}

.module-stats-row:hover {
  background-color: rgba(123, 73, 255, 0.03);
}

.module-name-cell {
  font-weight: 600;
  color: var(--text-primary);
  padding-right: 1rem;
}

.module-stat-cell {
  text-align: center;
  color: var(--text-secondary);
}

.progress-bar-small {
  height: 6px;
  background: var(--bg-accent);
  border-radius: 3px;
  overflow: hidden;
  box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.05);
  width: 80%;
  margin: 0 auto;
}

.progress-value {
  height: 100%;
  background: linear-gradient(to right, var(--primary-color), var(--primary-light));
  border-radius: 3px;
  font-size: 0.7rem;
  color: white;
  text-align: right;
  padding-right: 0.25rem;
  text-shadow: 0 1px 1px rgba(0, 0, 0, 0.2);
  white-space: nowrap;
  overflow: hidden;
}

/* ========== Dialog Styles ========== */
.dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
  backdrop-filter: blur(4px);
}

.dialog-content {
  background: var(--bg-card);
  border-radius: var(--border-radius-lg);
  width: 100%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: var(--shadow-lg);
  border: 1px solid var(--border-color);
  animation: dialog-fade-in 0.3s ease;
}

@keyframes dialog-fade-in {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.dialog-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid var(--border-color);
  background: linear-gradient(to right, var(--bg-card), rgba(123, 73, 255, 0.05));
}

.dialog-header h2 {
  margin: 0;
  font-size: 1.4rem;
  font-weight: 700;
  color: var(--primary-dark);
}

.close-dialog {
  background: transparent;
  border: none;
  color: var(--text-secondary);
  font-size: 1.5rem;
  cursor: pointer;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: all 0.2s ease;
}

.close-dialog:hover {
  background: var(--bg-accent);
  color: var(--danger-color);
}

/* Session Details Dialog */
.session-details-content {
  padding: 1.5rem;
}

.session-details-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.session-detail-item {
  background: var(--bg-accent);
  padding: 1rem;
  border-radius: var(--border-radius);
  border-left: 3px solid var(--primary-color);
}

.detail-label {
  font-size: 0.85rem;
  color: var(--text-secondary);
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.detail-value {
  font-weight: 600;
  color: var(--text-primary);
  font-size: 1.05rem;
}

.status-badge {
  display: inline-block;
  padding: 0.35rem 0.75rem;
  border-radius: 16px;
  font-size: 0.85rem;
  font-weight: 600;
}

.status-badge.planned {
  background: rgba(123, 73, 255, 0.1);
  color: var(--primary-color);
}

.status-badge.started {
  background: rgba(46, 204, 113, 0.1);
  color: var(--success-color);
}

.status-badge.completed {
  background: rgba(52, 152, 219, 0.1);
  color: var(--info-color);
}

.status-badge.missed {
  background: rgba(231, 76, 60, 0.1);
  color: var(--danger-color);
}

.status-badge.rescheduled {
  background: rgba(241, 196, 15, 0.1);
  color: var(--warning-color);
}

.session-topics {
  margin-bottom: 1.5rem;
}

.session-topics h3 {
  margin: 0 0 1rem;
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--text-primary);
}

.topics-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.session-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1.5rem;
}

.start-session-btn, .complete-session-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.25rem;
  background: var(--success-color);
  color: white;
  border: none;
  border-radius: var(--border-radius);
  font-weight: 600;
  cursor: pointer;
  transition: all 0.25s ease;
  flex: 1;
  justify-content: center;
}

.start-session-btn:hover, .complete-session-btn:hover {
  background: #27ae60;
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(46, 204, 113, 0.3);
}

.reschedule-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.25rem;
  background: transparent;
  color: var(--primary-color);
  border: 1px solid var(--primary-color);
  border-radius: var(--border-radius);
  font-weight: 600;
  cursor: pointer;
  transition: all 0.25s ease;
  flex: 1;
  justify-content: center;
}

.reschedule-btn:hover {
  background: rgba(123, 73, 255, 0.1);
  transform: translateY(-2px);
}

.session-feedback {
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid var(--border-color-light);
}

.session-feedback h3 {
  margin: 0 0 1rem;
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--text-primary);
}

.feedback-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
}

.feedback-item {
  background: var(--bg-accent);
  padding: 1rem;
  border-radius: var(--border-radius);
}

.feedback-item.full-width {
  grid-column: 1 / -1;
}

.feedback-label {
  font-size: 0.85rem;
  color: var(--text-secondary);
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.rating-stars {
  display: flex;
  gap: 0.2rem;
}

.star {
  font-size: 1.25rem;
  color: var(--border-color);
}

.star.filled {
  color: var(--warning-color);
}

.feedback-notes {
  color: var(--text-primary);
  background: var(--bg-card);
  padding: 0.75rem;
  border-radius: var(--border-radius);
  font-size: 0.9rem;
  min-height: 50px;
  line-height: 1.4;
}

.points-earned {
  color: var(--primary-color);
  font-weight: 700;
  font-size: 1.2rem;
}

/* Feedback Dialog */
.feedback-form {
  padding: 1.5rem;
}

.rating-input {
  display: flex;
  gap: 0.4rem;
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

.feedback-form textarea {
  width: 100%;
  height: 120px;
  padding: 0.85rem;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  font-size: 1rem;
  background-color: var(--bg-input);
  color: var(--text-primary);
  resize: vertical;
}

.feedback-form textarea:focus {
  border-color: var(--primary-color);
  outline: none;
  box-shadow: 0 0 0 3px rgba(123, 73, 255, 0.15);
}

.dialog-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1.5rem;
}

.cancel-btn {
  padding: 0.75rem 1.25rem;
  background: transparent;
  color: var(--text-secondary);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  font-weight: 600;
  cursor: pointer;
  transition: all 0.25s ease;
}

.cancel-btn:hover {
  background: var(--bg-accent);
  transform: translateY(-2px);
}

.submit-btn {
  padding: 0.75rem 1.25rem;
  background: var(--primary-color);
  color: white;
  border: none;
  border-radius: var(--border-radius);
  font-weight: 600;
  cursor: pointer;
  transition: all 0.25s ease;
  box-shadow: 0 3px 10px rgba(123, 73, 255, 0.2);
}

.submit-btn:hover {
  background: var(--primary-dark);
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(123, 73, 255, 0.3);
}

/* Import Dialog */
.import-form {
  padding: 1.5rem;
}

/* ========== Responsive Styles ========== */
@media (max-width: 1200px) {
  .study-schedule-tab {
    grid-template-columns: 1fr;
  }

  .stats-grid,
  .progress-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 992px) {
  .study-hub-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .tab-controls {
    width: 100%;
    overflow-x: auto;
    justify-content: flex-start;
  }

  .preferences-grid {
    grid-template-columns: 1fr;
  }

  .module-preference-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .achievement-grid {
    grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  }
}

@media (max-width: 768px) {
  .streak-display,
  .level-display {
    flex-direction: column;
    align-items: center;
    gap: 1.5rem;
  }

  .xp-info {
    width: 100%;
  }

  .session-details-grid,
  .feedback-grid {
    grid-template-columns: 1fr;
  }

  .module-stats-header,
  .module-stats-row {
    grid-template-columns: 2fr repeat(2, 1fr);
  }

  .module-stat-cell:nth-child(4),
  .module-stat-cell:nth-child(5) {
    display: none;
  }
}

@media (max-width: 576px) {
  .module-preference-grid {
    grid-template-columns: 1fr;
  }

  .schedule-tools {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
  }

  .view-switcher,
  .date-navigation {
    width: 100%;
  }

  .day-header .day-name {
    font-size: 0.8rem;
  }

  .day-header .day-date {
    font-size: 0.7rem;
  }

  .module-stats-header,
  .module-stats-row {
    grid-template-columns: 1fr 1fr;
  }

  .module-stat-cell:nth-child(3) {
    display: none;
  }
}

/* Additional styles for mobile optimization */
@media (max-width: 480px) {
  .study-hub-header h1 {
    font-size: 1.5rem;
  }

  .tab-controls button {
    padding: 0.4rem 0.8rem;
    font-size: 0.8rem;
  }

  .streak-circle,
  .level-badge {
    width: 100px;
    height: 100px;
  }

  .streak-value,
  .level-value {
    font-size: 2rem;
  }

  .calendar-day {
    min-width: 25px;
    padding: 0.25rem;
  }

  .day-date {
    font-size: 0.75rem;
  }

  .day-indicator {
    width: 20px;
    height: 20px;
  }

  .achievements-grid {
    grid-template-columns: 1fr;
  }
}
</style>
