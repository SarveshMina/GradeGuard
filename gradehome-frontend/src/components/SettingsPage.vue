<template>
  <div class="settings-page" :class="{ 'dark-mode': darkMode }">
    <!-- Dashboard NavBar at the top -->
    <DashboardNavBar
        :userName="userProfile.firstName || 'User'"
        :userEmail="userProfile.email || 'user@example.com'"
        :userAvatar="userProfile.avatar"
        :isMobile="isMobile"
        @logout="handleLogout"
    />

    <div class="dashboard-layout">
      <!-- Main Content Area -->
      <div class="dashboard-main-content expanded">
        <div class="dashboard-header">
          <h1>Settings</h1>
        </div>

        <!-- Loading State -->
        <div v-if="loading" class="loading-container">
          <div class="loading-spinner"></div>
          <p>Loading settings...</p>
        </div>

        <!-- Not Logged In State -->
        <div v-else-if="notLoggedIn" class="center-content auth-prompt">
          <div class="auth-card">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
              <circle cx="12" cy="7" r="4"></circle>
            </svg>
            <h2>Welcome to GradeGuard</h2>
            <p>Please sign in to access your settings.</p>
            <a href="/login" class="login-button">Go to Login</a>
          </div>
        </div>

        <!-- Settings Content -->
        <div v-else class="settings-content">
          <!-- Settings Navigation -->
          <div class="settings-navigation">
            <button
                v-for="(section, index) in sections"
                :key="index"
                @click="activeSection = section.id"
                class="nav-button"
                :class="{ active: activeSection === section.id }"
            >
              <span class="icon" v-html="section.icon"></span>
              <span class="text">{{ section.name }}</span>
            </button>
          </div>

          <!-- Settings Panels -->
          <div class="settings-panel">
            <!-- Appearance Settings -->
            <div v-if="activeSection === 'appearance'" class="settings-section">
              <h2>Appearance Settings</h2>

              <!-- Theme Selection -->
              <div class="setting-group">
                <h3>Theme</h3>
                <div class="theme-selector">
                  <button
                      @click="setTheme('light')"
                      class="theme-option"
                      :class="{ active: !darkMode }"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <circle cx="12" cy="12" r="5"></circle>
                      <line x1="12" y1="1" x2="12" y2="3"></line>
                      <line x1="12" y1="21" x2="12" y2="23"></line>
                      <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line>
                      <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>
                      <line x1="1" y1="12" x2="3" y2="12"></line>
                      <line x1="21" y1="12" x2="23" y2="12"></line>
                      <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line>
                      <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>
                    </svg>
                    <span>Light</span>
                  </button>
                  <button
                      @click="setTheme('dark')"
                      class="theme-option"
                      :class="{ active: darkMode }"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
                    </svg>
                    <span>Dark</span>
                  </button>
                </div>
              </div>

              <!-- Accent Color -->
              <div class="setting-group">
                <h3>Accent Color</h3>
                <div class="color-options">
                  <button
                      v-for="color in accentColors"
                      :key="color.id"
                      @click="setAccentColor(color.id)"
                      class="color-option"
                      :class="{ active: settings.appearance.accentColor === color.id }"
                      :style="{ backgroundColor: color.value }"
                  ></button>
                </div>
              </div>

              <!-- Font Size -->
              <div class="setting-group">
                <h3>Font Size</h3>
                <div class="radio-options">
                  <label class="radio-option">
                    <input
                        type="radio"
                        v-model="settings.appearance.fontSize"
                        value="small"
                    />
                    <span>Small</span>
                  </label>
                  <label class="radio-option">
                    <input
                        type="radio"
                        v-model="settings.appearance.fontSize"
                        value="medium"
                    />
                    <span>Medium</span>
                  </label>
                  <label class="radio-option">
                    <input
                        type="radio"
                        v-model="settings.appearance.fontSize"
                        value="large"
                    />
                    <span>Large</span>
                  </label>
                </div>
              </div>

              <!-- High Contrast Mode -->
              <div class="setting-group">
                <h3>High Contrast Mode</h3>
                <div class="toggle-option">
                  <label class="toggle">
                    <input
                        type="checkbox"
                        v-model="settings.appearance.highContrast"
                    />
                    <span class="toggle-slider"></span>
                  </label>
                  <span>Enable high contrast for better visibility</span>
                </div>
              </div>
            </div>

            <!-- Academic Settings -->
            <div v-if="activeSection === 'academic'" class="settings-section">
              <h2>Academic Settings</h2>

              <!-- Grading Scale -->
              <div class="setting-group">
                <h3>Grading Scale</h3>
                <div class="grading-scale">
                  <div class="grade-row header">
                    <div class="grade-letter">Grade</div>
                    <div class="grade-min">Minimum %</div>
                    <div class="grade-gpa">GPA Value</div>
                  </div>
                  <div
                      v-for="(grade, index) in settings.academic.gradingScale"
                      :key="index"
                      class="grade-row"
                  >
                    <div class="grade-letter">
                      <input
                          type="text"
                          v-model="grade.letter"
                          maxlength="2"
                      />
                    </div>
                    <div class="grade-min">
                      <input
                          type="number"
                          v-model.number="grade.minPercentage"
                          min="0"
                          max="100"
                          step="0.1"
                      />
                    </div>
                    <div class="grade-gpa">
                      <input
                          type="number"
                          v-model.number="grade.gpaValue"
                          min="0"
                          max="4"
                          step="0.1"
                      />
                    </div>
                    <button
                        v-if="index > 0"
                        @click="removeGrade(index)"
                        class="remove-grade"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <line x1="18" y1="6" x2="6" y2="18"></line>
                        <line x1="6" y1="6" x2="18" y2="18"></line>
                      </svg>
                    </button>
                  </div>
                  <button @click="addGrade" class="add-grade-btn">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <line x1="12" y1="5" x2="12" y2="19"></line>
                      <line x1="5" y1="12" x2="19" y2="12"></line>
                    </svg>
                    Add Grade
                  </button>
                </div>
              </div>

              <!-- Term Dates -->
              <div class="setting-group">
                <h3>Term Dates</h3>
                <div class="term-dates">
                  <div class="form-row">
                    <div class="form-group">
                      <label for="term-start">Term Start Date</label>
                      <input
                          type="date"
                          id="term-start"
                          v-model="settings.academic.termStartDate"
                      />
                    </div>
                    <div class="form-group">
                      <label for="term-end">Term End Date</label>
                      <input
                          type="date"
                          id="term-end"
                          v-model="settings.academic.termEndDate"
                      />
                    </div>
                  </div>
                </div>
              </div>

              <!-- Holidays and Breaks -->
              <div class="setting-group">
                <h3>Holidays and Break Periods</h3>
                <div class="holidays-list">
                  <div
                      v-for="(holiday, index) in settings.academic.holidays"
                      :key="index"
                      class="holiday-item"
                  >
                    <div class="form-row">
                      <div class="form-group">
                        <input
                            type="text"
                            v-model="holiday.name"
                            placeholder="Holiday Name"
                        />
                      </div>
                      <div class="form-group">
                        <input
                            type="date"
                            v-model="holiday.startDate"
                        />
                      </div>
                      <div class="form-group">
                        <input
                            type="date"
                            v-model="holiday.endDate"
                        />
                      </div>
                      <button
                          @click="removeHoliday(index)"
                          class="remove-holiday"
                      >
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                          <line x1="18" y1="6" x2="6" y2="18"></line>
                          <line x1="6" y1="6" x2="18" y2="18"></line>
                        </svg>
                      </button>
                    </div>
                  </div>
                  <button @click="addHoliday" class="add-holiday-btn">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <line x1="12" y1="5" x2="12" y2="19"></line>
                      <line x1="5" y1="12" x2="19" y2="12"></line>
                    </svg>
                    Add Holiday or Break
                  </button>
                </div>
              </div>
            </div>

            <!-- Account & Security Settings -->
            <div v-if="activeSection === 'account'" class="settings-section">
              <h2>Account & Security</h2>

              <!-- Password Change -->
              <div class="setting-group">
                <h3>Change Password</h3>
                <form @submit.prevent="changePassword" class="password-form">
                  <div class="form-group">
                    <label for="current-password">Current Password</label>
                    <input
                        type="password"
                        id="current-password"
                        v-model="passwordForm.currentPassword"
                        required
                    />
                  </div>
                  <div class="form-group">
                    <label for="new-password">New Password</label>
                    <input
                        type="password"
                        id="new-password"
                        v-model="passwordForm.newPassword"
                        required
                    />
                    <small>Password must be at least 8 characters with a mix of letters, numbers, and symbols</small>
                  </div>
                  <div class="form-group">
                    <label for="confirm-password">Confirm New Password</label>
                    <input
                        type="password"
                        id="confirm-password"
                        v-model="passwordForm.confirmPassword"
                        required
                    />
                  </div>
                  <button
                      type="submit"
                      class="save-button"
                      :disabled="passwordForm.isSubmitting"
                  >
                    <span v-if="passwordForm.isSubmitting">Updating...</span>
                    <span v-else>Update Password</span>
                  </button>
                </form>
              </div>
            </div>

            <!-- Accessibility Settings -->
            <div v-if="activeSection === 'accessibility'" class="settings-section">
              <h2>Accessibility Features</h2>

              <!-- Screen Reader Optimization -->
              <div class="setting-group">
                <h3>Screen Reader Optimization</h3>
                <div class="toggle-option">
                  <label class="toggle">
                    <input
                        type="checkbox"
                        v-model="settings.accessibility.screenReaderOptimized"
                    />
                    <span class="toggle-slider"></span>
                  </label>
                  <span>Optimize interface for screen readers</span>
                </div>
              </div>

              <!-- Keyboard Shortcuts -->
              <div class="setting-group">
                <h3>Keyboard Shortcuts</h3>
                <div class="toggle-option">
                  <label class="toggle">
                    <input
                        type="checkbox"
                        v-model="settings.accessibility.keyboardShortcuts"
                    />
                    <span class="toggle-slider"></span>
                  </label>
                  <span>Enable keyboard shortcuts</span>
                </div>
                <div class="shortcuts-list" v-if="settings.accessibility.keyboardShortcuts">
                  <div class="shortcut-item">
                    <div class="shortcut-keys">
                      <span class="key">Alt</span> + <span class="key">D</span>
                    </div>
                    <div class="shortcut-desc">Go to Dashboard</div>
                  </div>
                  <div class="shortcut-item">
                    <div class="shortcut-keys">
                      <span class="key">Alt</span> + <span class="key">C</span>
                    </div>
                    <div class="shortcut-desc">Go to Calendar</div>
                  </div>
                  <div class="shortcut-item">
                    <div class="shortcut-keys">
                      <span class="key">Alt</span> + <span class="key">G</span>
                    </div>
                    <div class="shortcut-desc">Go to Grades</div>
                  </div>
                  <div class="shortcut-item">
                    <div class="shortcut-keys">
                      <span class="key">Alt</span> + <span class="key">S</span>
                    </div>
                    <div class="shortcut-desc">Go to Settings</div>
                  </div>
                  <div class="shortcut-item">
                    <div class="shortcut-keys">
                      <span class="key">Alt</span> + <span class="key">N</span>
                    </div>
                    <div class="shortcut-desc">Create New Event</div>
                  </div>
                </div>
              </div>

              <!-- Focus Mode -->
              <div class="setting-group">
                <h3>Focus Mode</h3>
                <div class="toggle-option">
                  <label class="toggle">
                    <input
                        type="checkbox"
                        v-model="settings.accessibility.focusMode"
                    />
                    <span class="toggle-slider"></span>
                  </label>
                  <span>Reduce UI distractions for better focus</span>
                </div>
              </div>
            </div>

            <!-- Calendar & Events Settings -->
            <div v-if="activeSection === 'calendar'" class="settings-section">
              <h2>Calendar & Events</h2>

              <!-- First Day of Week -->
              <div class="setting-group">
                <h3>First Day of Week</h3>
                <div class="radio-options">
                  <label class="radio-option">
                    <input
                        type="radio"
                        v-model="settings.calendar.firstDayOfWeek"
                        value="sunday"
                    />
                    <span>Sunday</span>
                  </label>
                  <label class="radio-option">
                    <input
                        type="radio"
                        v-model="settings.calendar.firstDayOfWeek"
                        value="monday"
                    />
                    <span>Monday</span>
                  </label>
                </div>
              </div>

              <!-- Default Event Duration -->
              <div class="setting-group">
                <h3>Default Event Duration</h3>
                <div class="select-wrapper">
                  <select v-model="settings.calendar.defaultEventDuration">
                    <option value="30">30 minutes</option>
                    <option value="60">1 hour</option>
                    <option value="90">1.5 hours</option>
                    <option value="120">2 hours</option>
                    <option value="180">3 hours</option>
                  </select>
                </div>
              </div>

              <!-- Default Event Type -->
              <div class="setting-group">
                <h3>Default Event Type</h3>
                <div class="select-wrapper">
                  <select v-model="settings.calendar.defaultEventType">
                    <option value="general">General</option>
                    <option value="study">Study Session</option>
                    <option value="assignment">Assignment</option>
                    <option value="exam">Exam</option>
                    <option value="meeting">Meeting</option>
                    <option value="celebration">Celebration</option>
                  </select>
                </div>
              </div>

              <!-- Time Format -->
              <div class="setting-group">
                <h3>Time Format</h3>
                <div class="radio-options">
                  <label class="radio-option">
                    <input
                        type="radio"
                        v-model="settings.calendar.timeFormat"
                        value="12h"
                    />
                    <span>12-hour (1:00 PM)</span>
                  </label>
                  <label class="radio-option">
                    <input
                        type="radio"
                        v-model="settings.calendar.timeFormat"
                        value="24h"
                    />
                    <span>24-hour (13:00)</span>
                  </label>
                </div>
              </div>

              <!-- Date Format -->
              <div class="setting-group">
                <h3>Date Format</h3>
                <div class="radio-options">
                  <label class="radio-option">
                    <input
                        type="radio"
                        v-model="settings.calendar.dateFormat"
                        value="MM/DD/YYYY"
                    />
                    <span>MM/DD/YYYY</span>
                  </label>
                  <label class="radio-option">
                    <input
                        type="radio"
                        v-model="settings.calendar.dateFormat"
                        value="DD/MM/YYYY"
                    />
                    <span>DD/MM/YYYY</span>
                  </label>
                  <label class="radio-option">
                    <input
                        type="radio"
                        v-model="settings.calendar.dateFormat"
                        value="YYYY-MM-DD"
                    />
                    <span>YYYY-MM-DD</span>
                  </label>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Save Button (Fixed at Bottom) -->
        <div v-if="!notLoggedIn && !loading" class="settings-actions">
          <button
              @click="resetSettings"
              class="reset-button"
          >
            Reset to Defaults
          </button>
          <button
              @click="saveSettings"
              class="save-button"
              :disabled="isSaving"
          >
            <span v-if="isSaving">Saving...</span>
            <span v-else>Save Settings</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { notify } from "@/services/toastService.js";
import DashboardNavBar from "@/components/DashboardNavBar.vue";
import { getDarkModePreference, setDarkModePreference } from "@/services/darkModeService.js";
import { API_URL } from "@/config.js";

export default {
  name: "Settings",
  components: { DashboardNavBar },
  data() {
    return {
      darkMode: false,
      notLoggedIn: false,
      loading: true,
      isMobile: false,
      isSaving: false,
      activeSection: 'appearance',

      // User profile
      userProfile: {
        firstName: "",
        email: "",
        avatar: ""
      },

      // Password change form
      passwordForm: {
        currentPassword: "",
        newPassword: "",
        confirmPassword: "",
        isSubmitting: false
      },

      // Settings sections
      sections: [
        {
          id: 'appearance',
          name: 'Appearance',
          icon: '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"></circle><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path></svg>'
        },
        {
          id: 'academic',
          name: 'Academic',
          icon: '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 10v6M2 10l10-5 10 5-10 5z"></path><path d="M6 12v5c3 3 9 3 12 0v-5"></path></svg>'
        },
        {
          id: 'account',
          name: 'Account & Security',
          icon: '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path></svg>'
        },
        {
          id: 'accessibility',
          name: 'Accessibility',
          icon: '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><path d="M12 8v4"></path><path d="M12 16h.01"></path></svg>'
        },
        {
          id: 'calendar',
          name: 'Calendar & Events',
          icon: '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>'
        }
      ],

      // Available accent colors
      accentColors: [
        { id: 'purple', value: '#7b49ff' },
        { id: 'blue', value: '#2196f3' },
        { id: 'green', value: '#4caf50' },
        { id: 'red', value: '#f44336' },
        { id: 'orange', value: '#ff9800' },
        { id: 'pink', value: '#e91e63' },
        { id: 'teal', value: '#009688' }
      ],

      // Settings object
      settings: {
        appearance: {
          accentColor: 'purple',
          fontSize: 'medium',
          highContrast: false
        },
        academic: {
          gradingScale: [
            { letter: 'A', minPercentage: 90, gpaValue: 4.0 },
            { letter: 'B', minPercentage: 80, gpaValue: 3.0 },
            { letter: 'C', minPercentage: 70, gpaValue: 2.0 },
            { letter: 'D', minPercentage: 60, gpaValue: 1.0 },
            { letter: 'F', minPercentage: 0, gpaValue: 0.0 }
          ],
          termStartDate: '',
          termEndDate: '',
          holidays: []
        },
        accessibility: {
          screenReaderOptimized: false,
          keyboardShortcuts: true,
          focusMode: false
        },
        calendar: {
          firstDayOfWeek: 'sunday',
          defaultEventDuration: '60',
          defaultEventType: 'general',
          timeFormat: '12h',
          dateFormat: 'MM/DD/YYYY'
        }
      },

      // Default settings for reset functionality
      defaultSettings: null
    };
  },
  async mounted() {
    this.darkMode = getDarkModePreference();
    this.checkMobile();

    // Add event listeners
    window.addEventListener("resize", this.checkMobile);
    window.addEventListener('darkModeChange', this.onDarkModeChange);

    // Store default settings for reset functionality
    this.defaultSettings = JSON.parse(JSON.stringify(this.settings));

    // Fetch user profile and settings
    await this.fetchUserProfile();
    await this.fetchSettings();
  },
  beforeUnmount() {
    window.removeEventListener("resize", this.checkMobile);
    window.removeEventListener('darkModeChange', this.onDarkModeChange);
  },
  methods: {
    onDarkModeChange(event) {
      this.darkMode = event.detail.isDark;
    },
    handleLogout() {
      this.notLoggedIn = true;
      this.$router.push("/login");
    },
    checkMobile() {
      this.isMobile = window.innerWidth <= 768;
    },
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
    async fetchSettings() {
      try {
        const response = await axios.get(`${API_URL}/settings`, {
          withCredentials: true,
        });

        if (response.data) {
          // Merge received settings with defaults to ensure all properties exist
          this.settings = this.mergeDeep(this.settings, response.data);

          // Apply theme
          this.darkMode = getDarkModePreference();

          // Apply accent color
          this.applyAccentColor(this.settings.appearance.accentColor);

          // Apply font size
          this.applyFontSize(this.settings.appearance.fontSize);

          // Apply high contrast if enabled
          if (this.settings.appearance.highContrast) {
            document.documentElement.classList.add('high-contrast');
          }
        }
      } catch (error) {
        console.error("Error fetching settings:", error);
        // Use defaults if settings can't be fetched
      } finally {
        this.loading = false;
      }
    },
    async saveSettings() {
      this.isSaving = true;
      try {
        await axios.put(
            `${API_URL}/settings`,
            this.settings,
            { withCredentials: true }
        );

        // Apply settings visually
        this.applyAccentColor(this.settings.appearance.accentColor);
        this.applyFontSize(this.settings.appearance.fontSize);

        // Toggle high contrast mode
        if (this.settings.appearance.highContrast) {
          document.documentElement.classList.add('high-contrast');
        } else {
          document.documentElement.classList.remove('high-contrast');
        }

        notify({ type: "success", message: "Settings saved successfully!" });
      } catch (error) {
        console.error("Error saving settings:", error);
        notify({ type: "error", message: "Failed to save settings. Please try again." });
      } finally {
        this.isSaving = false;
      }
    },
    resetSettings() {
      // Reset to default settings
      this.settings = JSON.parse(JSON.stringify(this.defaultSettings));

      // Reset theme to system preference
      this.darkMode = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
      setDarkModePreference(this.darkMode);

      // Reset visual elements
      this.applyAccentColor('purple');
      this.applyFontSize('medium');
      document.documentElement.classList.remove('high-contrast');

      notify({ type: "info", message: "Settings reset to defaults" });
    },
    setTheme(theme) {
      this.darkMode = theme === 'dark';
      setDarkModePreference(this.darkMode);

      // Dispatch dark mode change event
      window.dispatchEvent(new CustomEvent('darkModeChange', {
        detail: { isDark: this.darkMode }
      }));
    },
    setAccentColor(colorId) {
      this.settings.appearance.accentColor = colorId;
      this.applyAccentColor(colorId);
    },
    applyAccentColor(colorId) {
      const color = this.accentColors.find(c => c.id === colorId);
      if (color) {
        document.documentElement.style.setProperty('--primary-color', color.value);

        // Calculate darker variant for hover states
        const darkerColor = this.adjustColor(color.value, -20);
        document.documentElement.style.setProperty('--primary-dark', darkerColor);

        // Calculate lighter variant
        const lighterColor = this.adjustColor(color.value, 20);
        document.documentElement.style.setProperty('--primary-light', lighterColor);
      }
    },
    applyFontSize(size) {
      const sizeMap = {
        'small': '14px',
        'medium': '16px',
        'large': '18px'
      };

      document.documentElement.style.setProperty('--font-size-base', sizeMap[size] || '16px');
    },
    adjustColor(hex, amount) {
      // Convert hex to RGB
      let r = parseInt(hex.slice(1, 3), 16);
      let g = parseInt(hex.slice(3, 5), 16);
      let b = parseInt(hex.slice(5, 7), 16);

      // Adjust colors
      r = Math.max(0, Math.min(255, r + amount));
      g = Math.max(0, Math.min(255, g + amount));
      b = Math.max(0, Math.min(255, b + amount));

      // Convert back to hex
      return `#${r.toString(16).padStart(2, '0')}${g.toString(16).padStart(2, '0')}${b.toString(16).padStart(2, '0')}`;
    },
    async changePassword() {
      if (this.passwordForm.newPassword !== this.passwordForm.confirmPassword) {
        notify({ type: "error", message: "New passwords do not match" });
        return;
      }

      this.passwordForm.isSubmitting = true;
      try {
        await axios.put(
            `${API_URL}/user/password`,
            {
              current_password: this.passwordForm.currentPassword,
              new_password: this.passwordForm.newPassword
            },
            { withCredentials: true }
        );

        notify({ type: "success", message: "Password changed successfully!" });

        // Reset form
        this.passwordForm.currentPassword = "";
        this.passwordForm.newPassword = "";
        this.passwordForm.confirmPassword = "";
      } catch (error) {
        console.error("Error changing password:", error);

        if (error.response?.status === 400) {
          notify({ type: "error", message: error.response.data.message || "Current password is incorrect" });
        } else {
          notify({ type: "error", message: "Failed to change password. Please try again." });
        }
      } finally {
        this.passwordForm.isSubmitting = false;
      }
    },
    addGrade() {
      this.settings.academic.gradingScale.push({
        letter: '',
        minPercentage: 0,
        gpaValue: 0
      });
    },
    removeGrade(index) {
      this.settings.academic.gradingScale.splice(index, 1);
    },
    addHoliday() {
      this.settings.academic.holidays.push({
        name: '',
        startDate: '',
        endDate: ''
      });
    },
    removeHoliday(index) {
      this.settings.academic.holidays.splice(index, 1);
    },
    // Deep merge utility for merging settings objects
    mergeDeep(target, source) {
      const output = Object.assign({}, target);
      if (this.isObject(target) && this.isObject(source)) {
        Object.keys(source).forEach(key => {
          if (this.isObject(source[key])) {
            if (!(key in target)) {
              Object.assign(output, { [key]: source[key] });
            } else {
              output[key] = this.mergeDeep(target[key], source[key]);
            }
          } else {
            Object.assign(output, { [key]: source[key] });
          }
        });
      }
      return output;
    },
    isObject(item) {
      return (item && typeof item === 'object' && !Array.isArray(item));
    }
  }
};
</script>

<style scoped>
.settings-page {
  min-height: 100vh;
  background-color: var(--bg-light);
  color: var(--text-primary);
  transition: background-color var(--transition-speed) ease,
  color var(--transition-speed) ease;
}

.dashboard-layout {
  display: flex;
  flex-direction: row;
  position: relative;
  padding-top: 70px; /* Space for fixed navbar */
  min-height: calc(100vh - 70px);
}

.dashboard-main-content {
  flex: 1;
  padding: 2rem;
  transition: all var(--transition-speed) ease;
  margin-bottom: 80px; /* Space for fixed bottom buttons */
}

.dashboard-header {
  margin-bottom: 2rem;
}

.dashboard-header h1 {
  font-size: 1.75rem;
  font-weight: 600;
  color: var(--primary-dark);
  margin: 0;
}

/* Loading state */
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

/* Auth prompt */
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

/* Settings content */
.settings-content {
  display: flex;
  gap: 2rem;
}

/* Settings navigation */
.settings-navigation {
  width: 220px;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  background-color: var(--bg-card);
  border-radius: var(--border-radius-lg);
  padding: 1rem;
  box-shadow: var(--shadow-md);
  align-self: flex-start;
  position: sticky;
  top: 85px; /* Stick below navbar */
}

.nav-button {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  border-radius: var(--border-radius);
  background: transparent;
  border: none;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.2s ease;
  text-align: left;
  font-size: 0.9rem;
}

.nav-button .icon {
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-secondary);
}

.nav-button:hover {
  background-color: var(--bg-hover);
  color: var(--text-primary);
}

.nav-button.active {
  background-color: var(--primary-color);
  color: white;
}

.nav-button.active .icon {
  color: white;
}

/* Settings panel */
.settings-panel {
  flex: 1;
  background-color: var(--bg-card);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow-md);
  padding: 2rem;
  overflow: hidden;
}

.settings-section {
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.settings-section h2 {
  margin: 0 0 1.5rem;
  font-size: 1.35rem;
  font-weight: 600;
  color: var(--primary-dark);
  padding-bottom: 0.75rem;
  border-bottom: 1px solid var(--border-color);
}

.setting-group {
  margin-bottom: 2rem;
}

.setting-group:last-child {
  margin-bottom: 0;
}

.setting-group h3 {
  margin: 0 0 1rem;
  font-size: 1.1rem;
  font-weight: 500;
  color: var(--text-primary);
}

/* Theme selection */
.theme-selector {
  display: flex;
  gap: 1rem;
}

.theme-option {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  border-radius: var(--border-radius);
  background-color: var(--bg-input);
  border: 1px solid var(--border-color);
  color: var(--text-primary);
  cursor: pointer;
  transition: all 0.2s ease;
}

.theme-option:hover {
  background-color: var(--bg-hover);
}

.theme-option.active {
  border-color: var(--primary-color);
  background-color: rgba(123, 73, 255, 0.1);
}

.dark-mode .theme-option.active {
  background-color: rgba(123, 73, 255, 0.2);
}

/* Color options */
.color-options {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}

.color-option {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  cursor: pointer;
  border: 2px solid transparent;
  transition: all 0.2s ease;
  position: relative;
}

.color-option:hover {
  transform: scale(1.1);
}

.color-option.active {
  border-color: var(--text-primary);
}

.color-option.active::after {
  content: "";
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 16px;
  height: 16px;
  background-color: white;
  border-radius: 50%;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
}

/* Toggle switch */
.toggle-option {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.toggle {
  position: relative;
  display: inline-block;
  width: 48px;
  height: 24px;
}

.toggle input {
  opacity: 0;
  width: 0;
  height: 0;
}

.toggle-slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  transition: .4s;
  border-radius: 24px;
}

.toggle-slider:before {
  position: absolute;
  content: "";
  height: 18px;
  width: 18px;
  left: 3px;
  bottom: 3px;
  background-color: white;
  transition: .4s;
  border-radius: 50%;
}

input:checked + .toggle-slider {
  background-color: var(--primary-color);
}

input:focus + .toggle-slider {
  box-shadow: 0 0 1px var(--primary-color);
}

input:checked + .toggle-slider:before {
  transform: translateX(24px);
}

/* Radio options */
.radio-options {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}

.radio-option {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
}

/* Form elements */
.form-row {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
}

.form-group {
  flex: 1;
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
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
  font-size: 1rem;
  transition: all 0.2s ease;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  border-color: var(--primary-color);
  outline: none;
}

.form-group small {
  display: block;
  margin-top: 0.25rem;
  font-size: 0.75rem;
  color: var(--text-secondary);
}

.select-wrapper {
  position: relative;
}

.select-wrapper::after {
  content: '';
  position: absolute;
  top: 50%;
  right: 12px;
  transform: translateY(-50%);
  width: 0;
  height: 0;
  border-left: 5px solid transparent;
  border-right: 5px solid transparent;
  border-top: 5px solid var(--text-secondary);
  pointer-events: none;
}

.select-wrapper select {
  appearance: none;
  padding-right: 30px;
}

/* Grading scale */
.grading-scale {
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  overflow: hidden;
}

.grade-row {
  display: flex;
  border-bottom: 1px solid var(--border-color);
  align-items: center;
}

.grade-row:last-child {
  border-bottom: none;
}

.grade-row.header {
  background-color: var(--bg-hover);
  font-weight: 500;
  color: var(--text-primary);
}

.grade-letter,
.grade-min,
.grade-gpa {
  padding: 0.75rem;
  flex: 1;
  text-align: center;
}

.grade-row input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid transparent;
  border-radius: var(--border-radius);
  text-align: center;
  background-color: transparent;
}

.grade-row input:focus {
  border-color: var(--primary-color);
  background-color: var(--bg-input);
  outline: none;
}

.remove-grade {
  background: transparent;
  border: none;
  color: var(--error-color);
  cursor: pointer;
  padding: 0.5rem;
  opacity: 0.7;
  transition: opacity 0.2s ease;
}

.remove-grade:hover {
  opacity: 1;
}

.add-grade-btn,
.add-holiday-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  width: 100%;
  padding: 0.75rem;
  background-color: transparent;
  border: 1px dashed var(--border-color);
  border-radius: var(--border-radius);
  color: var(--primary-color);
  cursor: pointer;
  margin-top: 1rem;
  transition: all 0.2s ease;
}

.add-grade-btn:hover,
.add-holiday-btn:hover {
  background-color: rgba(123, 73, 255, 0.05);
  border-color: var(--primary-color);
}

/* Holiday items */
.holiday-item {
  margin-bottom: 1rem;
  padding: 1rem;
  background-color: var(--bg-light);
  border-radius: var(--border-radius);
  position: relative;
}

.remove-holiday {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  background: transparent;
  border: none;
  color: var(--error-color);
  cursor: pointer;
  padding: 0.5rem;
}

/* Password form */
.password-form {
  max-width: 500px;
}

/* Keyboard shortcuts */
.shortcuts-list {
  margin-top: 1rem;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  overflow: hidden;
}

.shortcut-item {
  display: flex;
  justify-content: space-between;
  padding: 0.75rem 1rem;
  border-bottom: 1px solid var(--border-color);
}

.shortcut-item:last-child {
  border-bottom: none;
}

.shortcut-keys {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.key {
  display: inline-block;
  padding: 0.25rem 0.5rem;
  background-color: var(--bg-input);
  border: 1px solid var(--border-color);
  border-radius: 4px;
  font-size: 0.8rem;
  font-family: monospace;
}

/* Fixed bottom actions */
.settings-actions {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background-color: var(--bg-card);
  border-top: 1px solid var(--border-color);
  padding: 1rem 2rem;
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  z-index: 100;
  box-shadow: var(--shadow-md);
}

.reset-button,
.save-button {
  padding: 0.75rem 1.5rem;
  border-radius: var(--border-radius);
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.reset-button {
  background-color: transparent;
  border: 1px solid var(--border-color);
  color: var(--text-secondary);
}

.reset-button:hover {
  background-color: var(--bg-hover);
}

.save-button {
  background-color: var(--primary-color);
  border: none;
  color: white;
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

/* Responsive styles */
@media (max-width: 768px) {
  .dashboard-main-content {
    padding: 1rem;
  }

  .settings-content {
    flex-direction: column;
  }

  .settings-navigation {
    width: 100%;
    flex-direction: row;
    overflow-x: auto;
    padding: 0.5rem;
    position: relative;
    top: 0;
  }

  .nav-button {
    white-space: nowrap;
    padding: 0.5rem 0.75rem;
    font-size: 0.8rem;
  }

  .settings-panel {
    padding: 1rem;
  }

  .theme-selector,
  .color-options,
  .radio-options {
    flex-wrap: wrap;
  }

  .form-row {
    flex-direction: column;
  }

  .grade-row {
    font-size: 0.8rem;
  }

  .settings-actions {
    padding: 1rem;
  }
}
</style>