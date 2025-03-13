<!-- AIStudyScheduler.vue -->
<template>
  <div class="ai-scheduler">
    <!-- Floating AI Scheduler Button - matches your calendar "Add Event" button -->
    <button @click="openSchedulerModal" class="ai-scheduler-button">
      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M12 2L2 7l10 5 10-5-10-5z"></path>
        <path d="M2 17l10 5 10-5"></path>
        <path d="M2 12l10 5 10-5"></path>
      </svg>
      <span>AI Study Scheduler</span>
    </button>

    <!-- Scheduler Modal -->
    <transition name="modal-fade">
      <div v-if="showSchedulerModal" class="modal-overlay" @click.self="closeSchedulerModal">
        <div class="modal-container scheduler-modal">
          <div class="modal-header">
            <h2>AI Study Scheduler</h2>
            <button @click="closeSchedulerModal" class="close-modal-btn">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <line x1="18" y1="6" x2="6" y2="18"></line>
                <line x1="6" y1="6" x2="18" y2="18"></line>
              </svg>
            </button>
          </div>

          <!-- Modal Body with Steps -->
          <div class="modal-body">
            <!-- Step Navigation Pills -->
            <div class="step-indicators">
              <div
                  v-for="step in totalSteps"
                  :key="step"
                  :class="['step-indicator', { active: currentStep >= step, completed: currentStep > step }]"
                  @click="goToStep(step)"
              >
                {{ step }}
              </div>
            </div>

            <!-- Step 1: Study Preferences -->
            <div v-if="currentStep === 1" class="scheduler-step animate-fade-in">
              <h3>Study Preferences</h3>
              <p>Tell us when you prefer to study so we can build your optimal schedule.</p>

              <div class="form-group">
                <label>When do you prefer to study?</label>
                <div class="checkbox-group">
                  <label class="checkbox-container" v-for="time in timeOptions" :key="time.value">
                    <input
                        type="checkbox"
                        v-model="preferences.preferred_times"
                        :value="time.value"
                    />
                    <span class="checkmark"></span>
                    {{ time.label }}
                  </label>
                </div>
              </div>

              <div class="form-group">
                <label>Which days are you available?</label>
                <div class="checkbox-group">
                  <label class="checkbox-container" v-for="day in dayOptions" :key="day.value">
                    <input
                        type="checkbox"
                        v-model="preferences.preferred_days"
                        :value="day.value"
                    />
                    <span class="checkmark"></span>
                    {{ day.label }}
                  </label>
                </div>
              </div>

              <div class="form-row">
                <div class="form-group">
                  <label for="sessionDuration">Study session duration</label>
                  <select id="sessionDuration" v-model="preferences.study_session_duration">
                    <option value="30">30 minutes</option>
                    <option value="45">45 minutes</option>
                    <option value="60">60 minutes</option>
                    <option value="90">90 minutes</option>
                    <option value="120">120 minutes</option>
                  </select>
                </div>

                <div class="form-group">
                  <label for="breakDuration">Break between sessions</label>
                  <select id="breakDuration" v-model="preferences.breaks_between_sessions">
                    <option value="5">5 minutes</option>
                    <option value="10">10 minutes</option>
                    <option value="15">15 minutes</option>
                    <option value="30">30 minutes</option>
                  </select>
                </div>
              </div>

              <div class="form-row">
                <div class="form-group">
                  <label for="maxSessions">Maximum sessions per day</label>
                  <select id="maxSessions" v-model="preferences.max_sessions_per_day">
                    <option value="1">1 session</option>
                    <option value="2">2 sessions</option>
                    <option value="3">3 sessions</option>
                    <option value="4">4 sessions</option>
                    <option value="5">5 sessions</option>
                  </select>
                </div>

                <div class="form-group">
                  <label for="minSessions">Minimum sessions per week</label>
                  <select id="minSessions" v-model="preferences.min_sessions_per_week">
                    <option value="5">5 sessions</option>
                    <option value="7">7 sessions</option>
                    <option value="10">10 sessions</option>
                    <option value="15">15 sessions</option>
                    <option value="20">20 sessions</option>
                  </select>
                </div>
              </div>

              <div v-if="activeModules.length > 0" class="form-group">
                <label>Select modules to focus on</label>
                <div class="module-selection">
                  <div v-for="module in activeModules" :key="module.id" class="module-option">
                    <label class="checkbox-container">
                      <input
                          type="checkbox"
                          v-model="selectedModules"
                          :value="module.id"
                      />
                      <span class="checkmark"></span>
                      <span class="module-name">{{ module.name }}</span>
                    </label>
                  </div>
                </div>
              </div>
              <div v-else class="no-modules-message">
                <p>No active modules found. Please add modules to your account first.</p>
              </div>
            </div>

            <!-- Step 2: Calendar Import -->
            <div v-if="currentStep === 2" class="scheduler-step animate-fade-in">
              <h3>Import Your Timetable</h3>
              <p>Import your university timetable to help us plan around your classes.</p>

              <div class="import-options">
                <div class="import-option">
                  <h4>Import from iCal URL</h4>
                  <div class="ical-url-input">
                    <input
                        type="text"
                        v-model="icalUrl"
                        placeholder="https://example.com/calendar.ics"
                    />
                    <button
                        @click="importFromUrl"
                        class="import-button"
                        :disabled="isImporting || !icalUrl"
                    >
                      <span v-if="isImporting">Importing...</span>
                      <span v-else>Import</span>
                    </button>
                  </div>
                </div>

                <div class="import-option-divider">
                  <span>OR</span>
                </div>

                <div class="import-option">
                  <h4>Upload iCal File</h4>
                  <div class="file-upload">
                    <input
                        type="file"
                        id="calendar-file"
                        ref="fileInput"
                        accept=".ics"
                        @change="handleFileChange"
                        class="file-input"
                    />
                    <label for="calendar-file" class="file-label">
                      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                        <polyline points="17 8 12 3 7 8"></polyline>
                        <line x1="12" y1="3" x2="12" y2="15"></line>
                      </svg>
                      {{ selectedFile ? selectedFile.name : 'Choose a file' }}
                    </label>
                    <button
                        @click="uploadFile"
                        class="upload-button"
                        :disabled="isUploading || !selectedFile"
                    >
                      <span v-if="isUploading">Uploading...</span>
                      <span v-else>Upload</span>
                    </button>
                  </div>
                </div>
              </div>

              <div v-if="importedCalendars.length > 0" class="imported-calendars">
                <h4>Your Imported Calendars</h4>
                <div class="calendar-list">
                  <div v-for="calendar in importedCalendars" :key="calendar.id" class="calendar-item">
                    <div class="calendar-info">
                      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                        <line x1="16" y1="2" x2="16" y2="6"></line>
                        <line x1="8" y1="2" x2="8" y2="6"></line>
                        <line x1="3" y1="10" x2="21" y2="10"></line>
                      </svg>
                      <div class="calendar-details">
                        <span class="calendar-name">{{ calendar.name }}</span>
                        <span class="calendar-date">Imported: {{ formatDate(calendar.last_sync) }}</span>
                      </div>
                    </div>
                    <button @click="syncCalendar(calendar.id)" class="sync-button">
                      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M21.5 2v6h-6M2.5 22v-6h6M2 11.5a10 10 0 0 1 18.8-4.3M22 12.5a10 10 0 0 1-18.8 4.2"></path>
                      </svg>
                      <span>Sync</span>
                    </button>
                  </div>
                </div>
              </div>
            </div>

            <!-- Step 3: Generate Schedule -->
            <div v-if="currentStep === 3" class="scheduler-step animate-fade-in">
              <h3>Generate Your Study Schedule</h3>
              <p>We'll create an optimized study schedule based on your preferences.</p>

              <div class="date-range-selection">
                <div class="form-group">
                  <label for="startDate">Start Date</label>
                  <input
                      type="date"
                      id="startDate"
                      v-model="scheduleOptions.start_date"
                  />
                </div>
                <div class="form-group">
                  <label for="daysAhead">Duration</label>
                  <select id="daysAhead" v-model="scheduleOptions.days_ahead">
                    <option value="7">1 week</option>
                    <option value="14">2 weeks</option>
                    <option value="21">3 weeks</option>
                    <option value="30">1 month</option>
                  </select>
                </div>
              </div>

              <div class="generate-actions">
                <button @click="generateSchedule" class="generate-button" :disabled="isGenerating || selectedModules.length === 0">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M12 2L2 7l10 5 10-5-10-5z"></path>
                    <path d="M2 17l10 5 10-5"></path>
                    <path d="M2 12l10 5 10-5"></path>
                  </svg>
                  <span v-if="isGenerating">Generating...</span>
                  <span v-else>Generate Study Schedule</span>
                </button>
              </div>
            </div>

            <!-- Step 4: Schedule Preview -->
            <div v-if="currentStep === 4" class="scheduler-step animate-fade-in">
              <h3>Review Your Study Schedule</h3>
              <p>Here's your AI-generated study schedule. Review before saving.</p>

              <div v-if="generatedSessions.length === 0" class="no-sessions-message">
                <p>No study sessions were generated. Please try again with different preferences.</p>
              </div>

              <div v-else class="generated-schedule">
                <div class="schedule-summary">
                  <div class="summary-item">
                    <span class="summary-label">Total Sessions:</span>
                    <span class="summary-value">{{ generatedSessions.length }}</span>
                  </div>
                  <div class="summary-item">
                    <span class="summary-label">Date Range:</span>
                    <span class="summary-value">{{ formatDateRange() }}</span>
                  </div>
                  <div class="summary-item">
                    <span class="summary-label">Modules:</span>
                    <span class="summary-value">{{ uniqueModulesCount }}</span>
                  </div>
                </div>

                <div class="sessions-list">
                  <div v-for="(session, index) in generatedSessions" :key="index" class="session-item">
                    <div class="session-header">
                      <span class="session-module">{{ session.module_name }}</span>
                      <button @click="removeSession(index)" class="remove-session-btn">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                          <line x1="18" y1="6" x2="6" y2="18"></line>
                          <line x1="6" y1="6" x2="18" y2="18"></line>
                        </svg>
                      </button>
                    </div>
                    <div class="session-details">
                      <div class="session-date">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                          <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                          <line x1="16" y1="2" x2="16" y2="6"></line>
                          <line x1="8" y1="2" x2="8" y2="6"></line>
                          <line x1="3" y1="10" x2="21" y2="10"></line>
                        </svg>
                        <span>{{ formatSessionDate(session.date) }}</span>
                      </div>
                      <div class="session-time">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                          <circle cx="12" cy="12" r="10"></circle>
                          <polyline points="12 6 12 12 16 14"></polyline>
                        </svg>
                        <span>{{ formatSessionTime(session.start_time, session.end_time) }}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Modal Footer with Actions -->
          <div class="modal-footer">
            <div class="modal-actions">
              <button
                  v-if="currentStep > 1 && currentStep < 5"
                  @click="prevStep"
                  class="back-button"
              >
                Back
              </button>
              <div class="right-actions">
                <button
                    v-if="currentStep < 4"
                    @click="nextStep"
                    class="next-button"
                    :disabled="!canProceed"
                >
                  Next
                </button>
                <button
                    v-if="currentStep === 4"
                    @click="saveSchedule"
                    class="save-button"
                    :disabled="isSaving || generatedSessions.length === 0"
                >
                  <span v-if="isSaving">Saving...</span>
                  <span v-else>Save to Calendar</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
import axios from "axios";
import { notify } from "@/services/toastService.js";
import { API_URL } from "@/config.js";

export default {
  name: "AIStudyScheduler",
  props: {
    events: {
      type: Array,
      required: true
    },
    userProfile: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      // Modal visibility
      showSchedulerModal: false,

      // Wizard state
      currentStep: 1,
      totalSteps: 4,

      // Loading states
      isLoading: false,
      isImporting: false,
      isUploading: false,
      isSyncing: null,
      isGenerating: false,
      isSaving: false,

      // Study preferences
      preferences: {
        preferred_times: ["morning", "afternoon", "evening"],
        preferred_days: ["monday", "tuesday", "wednesday", "thursday", "friday"],
        study_session_duration: 60,
        breaks_between_sessions: 15,
        max_sessions_per_day: 3,
        min_sessions_per_week: 10,
        focus_areas: []
      },

      // Options for preferences
      timeOptions: [
        { value: "morning", label: "Morning (8am-12pm)" },
        { value: "afternoon", label: "Afternoon (12pm-5pm)" },
        { value: "evening", label: "Evening (5pm-9pm)" },
        { value: "night", label: "Night (9pm-12am)" }
      ],
      dayOptions: [
        { value: "monday", label: "Monday" },
        { value: "tuesday", label: "Tuesday" },
        { value: "wednesday", label: "Wednesday" },
        { value: "thursday", label: "Thursday" },
        { value: "friday", label: "Friday" },
        { value: "saturday", label: "Saturday" },
        { value: "sunday", label: "Sunday" }
      ],

      // Calendar import
      icalUrl: "",
      selectedFile: null,
      importedCalendars: [],

      // Modules
      activeModules: [],
      selectedModules: [],

      // Schedule generation
      scheduleOptions: {
        start_date: new Date().toISOString().split('T')[0],
        days_ahead: 14
      },
      generatedSessions: []
    };
  },
  computed: {
    canProceed() {
      if (this.currentStep === 1) {
        // Verify at least one time, one day, and one module is selected
        return this.preferences.preferred_times.length > 0 &&
            this.preferences.preferred_days.length > 0 &&
            this.selectedModules.length > 0;
      }

      if (this.currentStep === 2) {
        return true; // Always allow proceeding from calendar import
      }

      if (this.currentStep === 3) {
        return this.scheduleOptions.start_date && this.scheduleOptions.days_ahead;
      }

      return true;
    },

    uniqueModulesCount() {
      const moduleIds = new Set(this.generatedSessions.map(session => session.module_id));
      return moduleIds.size;
    }
  },
  mounted() {
    this.fetchActiveModules();
    this.fetchStudyPreferences();
    this.fetchImportedCalendars();
  },
  methods: {
    // Modal control
    openSchedulerModal() {
      this.showSchedulerModal = true;
      this.currentStep = 1;
    },

    closeSchedulerModal() {
      this.showSchedulerModal = false;
      this.resetForm();
    },

    // Wizard navigation
    prevStep() {
      if (this.currentStep > 1) {
        this.currentStep--;
      }
    },

    nextStep() {
      if (!this.canProceed) return;

      if (this.currentStep < this.totalSteps) {
        this.currentStep++;
      }

      // If we're moving to step 2, save study preferences
      if (this.currentStep === 2) {
        this.saveStudyPreferences();
      }
    },

    goToStep(step) {
      if (step < this.currentStep) {
        this.currentStep = step;
      } else if (step > this.currentStep && this.canProceed) {
        this.currentStep = step;
      }
    },

    // API calls
    async fetchActiveModules() {
      try {
        const response = await axios.get(`${API_URL}/modules?status=active`, {
          withCredentials: true
        });
        this.activeModules = response.data;

        // Pre-select all active modules
        this.selectedModules = this.activeModules.map(module => module.id);
      } catch (error) {
        console.error("Error fetching active modules:", error);
        notify({ type: "error", message: "Failed to load your modules." });
      }
    },

    async fetchStudyPreferences() {
      try {
        const response = await axios.get(`${API_URL}/scheduler/preferences`, {
          withCredentials: true
        });

        // Merge with defaults
        this.preferences = { ...this.preferences, ...response.data };
      } catch (error) {
        console.error("Error fetching study preferences:", error);
        // Use default preferences
      }
    },

    async saveStudyPreferences() {
      try {
        // Update focus areas with selected modules
        this.preferences.focus_areas = this.selectedModules.map(moduleId => {
          const module = this.activeModules.find(m => m.id === moduleId);
          return {
            module_id: moduleId,
            module_name: module?.name || "Unknown Module",
            importance: 1 // Default importance
          };
        });

        await axios.put(`${API_URL}/scheduler/preferences`, this.preferences, {
          withCredentials: true
        });

        notify({ type: "success", message: "Study preferences saved!" });
      } catch (error) {
        console.error("Error saving study preferences:", error);
        notify({ type: "error", message: "Failed to save study preferences." });
      }
    },

    async fetchImportedCalendars() {
      try {
        const response = await axios.get(`${API_URL}/scheduler/calendars`, {
          withCredentials: true
        });
        this.importedCalendars = response.data;
      } catch (error) {
        console.error("Error fetching imported calendars:", error);
      }
    },

    // Calendar import
    handleFileChange(event) {
      const file = event.target.files[0];
      if (file) {
        this.selectedFile = file;
      }
    },

    async importFromUrl() {
      if (!this.icalUrl) return;

      this.isImporting = true;
      try {
        const response = await axios.post(`${API_URL}/scheduler/calendars/import`, {
          name: "Imported Calendar",
          url: this.icalUrl
        }, {
          withCredentials: true
        });

        // Refresh imported calendars
        await this.fetchImportedCalendars();

        notify({ type: "success", message: `Successfully imported ${response.data.events_imported} events!` });
        this.icalUrl = "";
      } catch (error) {
        console.error("Error importing calendar:", error);
        notify({ type: "error", message: "Failed to import calendar. Please check the URL." });
      } finally {
        this.isImporting = false;
      }
    },

    async uploadFile() {
      if (!this.selectedFile) return;

      this.isUploading = true;
      try {
        const formData = new FormData();
        formData.append("file", this.selectedFile);
        formData.append("name", "Uploaded Calendar");

        await axios.post(`${API_URL}/scheduler/calendars/upload`, formData, {
          withCredentials: true,
          headers: {
            "Content-Type": "multipart/form-data"
          }
        });

        // Refresh imported calendars
        await this.fetchImportedCalendars();

        notify({ type: "success", message: "Calendar uploaded successfully!" });
        this.selectedFile = null;
        if (this.$refs.fileInput) this.$refs.fileInput.value = null;
      } catch (error) {
        console.error("Error uploading calendar file:", error);
        notify({ type: "error", message: "Failed to upload calendar file." });
      } finally {
        this.isUploading = false;
      }
    },

    async syncCalendar(calendarId) {
      this.isSyncing = calendarId;
      try {
        const response = await axios.post(`${API_URL}/scheduler/calendars/${calendarId}/sync`, {}, {
          withCredentials: true
        });

        notify({
          type: "success",
          message: `Calendar synced with ${response.data.events_imported} new events!`
        });

        // Refresh imported calendars
        await this.fetchImportedCalendars();
      } catch (error) {
        console.error("Error syncing calendar:", error);
        notify({ type: "error", message: "Failed to sync calendar." });
      } finally {
        this.isSyncing = null;
      }
    },

    // Schedule generation
    async generateSchedule() {
      this.isGenerating = true;
      try {
        const response = await axios.post(`${API_URL}/scheduler/generate`, {
          start_date: this.scheduleOptions.start_date,
          days_ahead: parseInt(this.scheduleOptions.days_ahead)
        }, {
          withCredentials: true
        });

        this.generatedSessions = response.data.sessions || [];

        if (this.generatedSessions.length > 0) {
          notify({
            type: "success",
            message: `Generated ${this.generatedSessions.length} study sessions!`
          });
          this.currentStep = 4; // Move to preview step
        } else {
          notify({
            type: "warning",
            message: "No study sessions were generated. Try different preferences."
          });
        }
      } catch (error) {
        console.error("Error generating schedule:", error);
        notify({ type: "error", message: "Failed to generate study schedule." });
      } finally {
        this.isGenerating = false;
      }
    },

    removeSession(index) {
      this.generatedSessions.splice(index, 1);
    },

    async saveSchedule() {
      this.isSaving = true;
      try {
        const response = await axios.post(`${API_URL}/scheduler/save`, this.generatedSessions, {
          withCredentials: true
        });

        notify({
          type: "success",
          message: `${response.data.sessions.length} study sessions added to your calendar!`
        });

        this.closeSchedulerModal();
      } catch (error) {
        console.error("Error saving schedule:", error);
        notify({ type: "error", message: "Failed to save study schedule." });
      } finally {
        this.isSaving = false;
      }
    },

    // Utility functions
    resetForm() {
      // Reset generated sessions
      this.generatedSessions = [];

      // Reset file input
      if (this.$refs.fileInput) {
        this.$refs.fileInput.value = null;
      }
      this.selectedFile = null;

      // Reset schedule options to today + 2 weeks
      this.scheduleOptions = {
        start_date: new Date().toISOString().split('T')[0],
        days_ahead: 14
      };
    },

    formatDate(dateStr) {
      if (!dateStr) return "Unknown";

      return new Date(dateStr).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      });
    },

    formatSessionDate(dateStr) {
      if (!dateStr) return "";

      return new Date(dateStr).toLocaleDateString('en-US', {
        weekday: 'long',
        month: 'long',
        day: 'numeric'
      });
    },

    formatSessionTime(startTime, endTime) {
      if (!startTime || !endTime) return "All day";

      const formatTime = (timeStr) => {
        const [hours, minutes] = timeStr.split(':');
        const hour = parseInt(hours, 10);
        const period = hour >= 12 ? 'PM' : 'AM';
        const hour12 = hour % 12 || 12;
        return `${hour12}:${minutes} ${period}`;
      };

      return `${formatTime(startTime)} - ${formatTime(endTime)}`;
    },

    formatDateRange() {
      if (this.generatedSessions.length === 0) return "";

      // Find min and max dates in sessions
      const dates = this.generatedSessions.map(s => new Date(s.date));
      const minDate = new Date(Math.min(...dates));
      const maxDate = new Date(Math.max(...dates));

      const options = { month: 'short', day: 'numeric' };
      return `${minDate.toLocaleDateString('en-US', options)} - ${maxDate.toLocaleDateString('en-US', options)}`;
    }
  }
};
</script>

<style scoped>
/* AI Scheduler Button */
.ai-scheduler-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background-color: var(--primary-color);
  color: white;
  border: none;
  border-radius: var(--border-radius);
  padding: 0.6rem 1.25rem;
  cursor: pointer;
  transition: all 0.2s ease;
  font-weight: 500;
  box-shadow: 0 2px 4px rgba(123, 73, 255, 0.2);
}

.ai-scheduler-button:hover {
  background-color: var(--primary-dark);
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(123, 73, 255, 0.3);
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
  backdrop-filter: blur(2px);
}

.modal-container {
  background-color: var(--bg-card);
  border-radius: var(--border-radius-lg);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
  width: 90%;
  max-width: 700px;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  border: 1px solid var(--border-color);
}

.scheduler-modal {
  max-width: 700px;
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
  transition: all 0.3s ease;
}

.close-modal-btn:hover {
  background-color: var(--bg-hover);
  color: var(--text-primary);
}

.modal-body {
  padding: 0;
  overflow-y: auto;
  max-height: calc(90vh - 130px);
  scrollbar-width: thin;
}

.modal-body::-webkit-scrollbar {
  width: 6px;
}

.modal-body::-webkit-scrollbar-track {
  background: transparent;
}

.modal-body::-webkit-scrollbar-thumb {
  background-color: var(--border-color);
  border-radius: 6px;
}

.modal-footer {
  padding: 1.25rem 1.5rem;
  border-top: 1px solid var(--border-color);
  background-color: var(--bg-card);
}

.scheduler-step {
  padding: 1.5rem;
}

.scheduler-step h3 {
  margin-top: 0;
  margin-bottom: 0.75rem;
  color: var(--text-primary);
  font-size: 1.2rem;
  font-weight: 600;
}

.scheduler-step p {
  margin-top: 0;
  margin-bottom: 1.5rem;
  color: var(--text-secondary);
  line-height: 1.5;
}

/* Step Indicators */
.step-indicators {
  display: flex;
  justify-content: center;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
  padding: 0.75rem;
  border-bottom: 1px solid var(--border-color);
}

.step-indicator {
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  font-weight: 500;
  background-color: var(--bg-input);
  color: var(--text-secondary);
  border: 1px solid var(--border-color);
  cursor: pointer;
  transition: all 0.2s ease;
}

.step-indicator.active {
  background-color: var(--primary-color);
  color: white;
  border-color: var(--primary-color);
}

.step-indicator.completed {
  background-color: var(--primary-light);
  color: white;
  border-color: var(--primary-light);
}

.step-indicator:hover:not(.active) {
  border-color: var(--primary-color);
  background-color: var(--bg-hover);
}

/* Form Styling */
.form-group {
  margin-bottom: 1.25rem;
}

.form-row {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.25rem;
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
  transition: border-color 0.3s ease, box-shadow 0.3s ease;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  border-color: var(--primary-color);
  outline: none;
  box-shadow: 0 0 0 2px rgba(123, 73, 255, 0.1);
}

/* Checkbox Styling */
.checkbox-group {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 1rem;
}

.checkbox-container {
  position: relative;
  padding-left: 28px;
  cursor: pointer;
  user-select: none;
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
  transition: all 0.2s ease;
}

.checkbox-container:hover input ~ .checkmark {
  border-color: var(--primary-color);
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
}

/* Module Selection Styles */
.module-selection {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 0.75rem;
  max-height: 200px;
  overflow-y: auto;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  padding: 0.75rem;
  background-color: var(--bg-input);
  scrollbar-width: thin;
}

.module-name {
  font-size: 0.9rem;
  margin-left: 0.5rem;
}

.no-modules-message {
  padding: 1rem;
  background-color: rgba(255, 193, 7, 0.1);
  border: 1px solid rgba(255, 193, 7, 0.3);
  border-radius: var(--border-radius);
  color: #FF9800;
  text-align: center;
}

/* Import options styling */
.import-options {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.import-option {
  padding: 1.25rem;
  background-color: var(--bg-input);
  border-radius: var(--border-radius);
  border: 1px solid var(--border-color);
}

.import-option h4 {
  margin-top: 0;
  margin-bottom: 1rem;
  color: var(--text-primary);
  font-size: 1rem;
  font-weight: 600;
}

.import-option-divider {
  display: flex;
  align-items: center;
  text-align: center;
  color: var(--text-secondary);
}

.import-option-divider::before,
.import-option-divider::after {
  content: '';
  flex: 1;
  border-bottom: 1px solid var(--border-color);
}

.import-option-divider::before {
  margin-right: 1rem;
}

.import-option-divider::after {
  margin-left: 1rem;
}

.ical-url-input {
  display: flex;
  gap: 0.5rem;
}

.ical-url-input input {
  flex: 1;
}

/* File upload styles */
.file-input {
  display: none;
}

.file-label {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem;
  background-color: var(--bg-card);
  border: 1px dashed var(--border-color);
  border-radius: var(--border-radius);
  cursor: pointer;
  transition: all 0.2s ease;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.file-label:hover {
  border-color: var(--primary-color);
  background-color: rgba(123, 73, 255, 0.05);
}

.file-upload {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.upload-button, .import-button {
  padding: 0.75rem 1rem;
  background-color: var(--primary-color);
  color: white;
  border: none;
  border-radius: var(--border-radius);
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.upload-button:hover, .import-button:hover {
  background-color: var(--primary-dark);
}

.upload-button:disabled, .import-button:disabled {
  background-color: var(--border-color);
  cursor: not-allowed;
}

/* Imported calendars styles */
.imported-calendars {
  margin-top: 1.5rem;
  padding: 1.25rem;
  background-color: var(--bg-input);
  border-radius: var(--border-radius);
  border: 1px solid var(--border-color);
}

.imported-calendars h4 {
  margin-top: 0;
  margin-bottom: 1rem;
  color: var(--text-primary);
  font-size: 1rem;
  font-weight: 600;
}

.calendar-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.calendar-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem;
  background-color: var(--bg-card);
  border-radius: var(--border-radius);
  border: 1px solid var(--border-color);
}

.calendar-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.calendar-info svg {
  color: var(--primary-color);
}

.calendar-details {
  display: flex;
  flex-direction: column;
}

.calendar-name {
  font-weight: 500;
  color: var(--text-primary);
}

.calendar-date {
  font-size: 0.85rem;
  color: var(--text-secondary);
}

.sync-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background-color: var(--bg-card);
  color: var(--primary-color);
  border: 1px solid var(--primary-color);
  border-radius: var(--border-radius);
  cursor: pointer;
  transition: all 0.2s ease;
}

.sync-button:hover {
  background-color: rgba(123, 73, 255, 0.1);
}

/* Generate schedule styles */
.date-range-selection {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
}

.date-range-selection .form-group {
  flex: 1;
}

.generate-actions {
  display: flex;
  justify-content: center;
  margin-top: 1.5rem;
}

.generate-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background-color: var(--primary-color);
  color: white;
  border: none;
  border-radius: var(--border-radius);
  cursor: pointer;
  transition: all 0.2s ease;
  font-weight: 500;
  font-size: 1rem;
}

.generate-button:hover {
  background-color: var(--primary-dark);
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(123, 73, 255, 0.2);
}

.generate-button:disabled {
  background-color: var(--border-color);
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

/* Schedule Preview styles */
.no-sessions-message {
  padding: 1.5rem;
  text-align: center;
  color: var(--text-secondary);
  background-color: var(--bg-input);
  border-radius: var(--border-radius);
  border: 1px solid var(--border-color);
}

.generated-schedule {
  background-color: var(--bg-card);
  border-radius: var(--border-radius);
  border: 1px solid var(--border-color);
  overflow: hidden;
}

.schedule-summary {
  display: flex;
  justify-content: space-between;
  padding: 1rem;
  background-color: var(--bg-input);
  border-bottom: 1px solid var(--border-color);
}

.summary-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.summary-label {
  font-size: 0.85rem;
  color: var(--text-secondary);
  margin-bottom: 0.25rem;
}

.summary-value {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--primary-color);
}

.sessions-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  max-height: 300px;
  overflow-y: auto;
  padding: 1rem;
}

.session-item {
  padding: 1rem;
  background-color: var(--bg-input);
  border-radius: var(--border-radius);
  border-left: 3px solid var(--primary-color);
  transition: all 0.2s ease;
}

.session-item:hover {
  transform: translateX(2px);
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
}

.session-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.session-module {
  font-weight: 600;
  color: var(--primary-color);
}

.remove-session-btn {
  background: transparent;
  color: var(--error-color);
  border: none;
  padding: 0.25rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
  opacity: 0.6;
}

.remove-session-btn:hover {
  opacity: 1;
  background-color: rgba(244, 67, 54, 0.1);
}

.session-details {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.session-date, .session-time {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
  color: var(--text-secondary);
}

.session-date svg, .session-time svg {
  color: var(--text-secondary);
}

/* Modal Actions */
.modal-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.right-actions {
  display: flex;
  gap: 0.75rem;
}

.back-button, .next-button, .save-button {
  padding: 0.75rem 1.25rem;
  border-radius: var(--border-radius);
  cursor: pointer;
  transition: all 0.2s ease;
  font-weight: 500;
}

.back-button {
  background-color: var(--bg-input);
  color: var(--text-primary);
  border: 1px solid var(--border-color);
}

.back-button:hover {
  background-color: var(--bg-hover);
}

.next-button, .save-button {
  background-color: var(--primary-color);
  color: white;
  border: none;
}

.next-button:hover, .save-button:hover {
  background-color: var(--primary-dark);
}

.next-button:disabled, .save-button:disabled {
  background-color: var(--border-color);
  cursor: not-allowed;
}

/* Animation Classes */
.animate-fade-in {
  animation: fadeIn 0.4s ease-out;
}

@keyframes fadeIn {
  0% { opacity: 0; }
  100% { opacity: 1; }
}

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

/* Responsive Styles */
@media (max-width: 768px) {
  .scheduler-modal {
    width: 95%;
    max-height: 95vh;
  }

  .form-row {
    flex-direction: column;
    gap: 1rem;
  }

  .date-range-selection {
    flex-direction: column;
  }

  .modal-actions {
    flex-direction: column-reverse;
    gap: 1rem;
    align-items: stretch;
  }

  .right-actions {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }

  .modal-actions button {
    width: 100%;
  }

  .session-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }

  .remove-session-btn {
    align-self: flex-end;
  }
}
</style>