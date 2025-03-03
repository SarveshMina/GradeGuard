<template>
  <div class="dashboard" :class="{ 'dark-mode': darkMode }">
    <!-- Dashboard NavBar at the top - use this instead of the regular NavBar -->
    <DashboardNavBar
        :userName="userProfile.firstName || 'User'"
        :userEmail="userProfile.email || 'user@example.com'"
        :userAvatar="userProfile.avatar"
        :isMobile="isMobile"
        @logout="handleLogout"
    />

    <!-- Layout container: main content and sidebar -->
    <div class="dashboard-layout">
      <!-- Floating collapse button that appears when sidebar is hidden -->
      <button
          v-if="!sidebarVisible"
          @click="toggleSidebar"
          class="sidebar-toggle sidebar-show-button"
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
          <h1>My Dashboard</h1>
        </div>

        <!-- If not logged in -->
        <div v-if="notLoggedIn" class="center-content auth-prompt">
          <div class="auth-card">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
              <circle cx="12" cy="7" r="4"></circle>
            </svg>
            <h2>Welcome to GradeGuard</h2>
            <p>Please sign in to access your personalized dashboard.</p>
            <a href="/login" class="login-button">Go to Login</a>
          </div>
        </div>

        <!-- Otherwise, show the wizard(s) or the final calculator -->
        <div v-else class="center-content">
          <!-- Wizard Step 1: Basic User Preferences -->
          <div v-if="showSetupWizard" class="setup-wizard">
            <div class="wizard-card">
              <div class="wizard-header">
                <div class="step-indicator">Step 1 of 2</div>
                <h2>Welcome! Let's set up your preferences</h2>
                <p>Please select an option for each question to personalize your experience.</p>
              </div>

              <!-- Academic Level -->
              <div class="form-group">
                <label>What is your current academic level?</label>
                <div class="select-group">
                  <button class="select-btn"
                          :class="{ active: userConfig.academicLevel === 'Undergraduate' }"
                          @click="userConfig.academicLevel = 'Undergraduate'">
                    <span class="btn-icon">🎓</span>
                    <span class="btn-text">Undergraduate</span>
                  </button>
                  <button class="select-btn"
                          :class="{ active: userConfig.academicLevel === 'Postgraduate (Masters)' }"
                          @click="userConfig.academicLevel = 'Postgraduate (Masters)'">
                    <span class="btn-icon">🧑‍🎓</span>
                    <span class="btn-text">Masters</span>
                  </button>
                  <button class="select-btn"
                          :class="{ active: userConfig.academicLevel === 'Postgraduate (PhD)' }"
                          @click="userConfig.academicLevel = 'Postgraduate (PhD)'">
                    <span class="btn-icon">👨‍🎓</span>
                    <span class="btn-text">PhD</span>
                  </button>
                </div>
              </div>

              <!-- Enrollment Type -->
              <div class="form-group">
                <label>Are you full-time or part-time?</label>
                <div class="select-group">
                  <button class="select-btn"
                          :class="{ active: userConfig.enrollmentType === 'Full time' }"
                          @click="userConfig.enrollmentType = 'Full time'">
                    <span class="btn-icon">✅</span>
                    <span class="btn-text">Full time</span>
                  </button>
                  <button class="select-btn"
                          :class="{ active: userConfig.enrollmentType === 'Part time' }"
                          @click="userConfig.enrollmentType = 'Part time'">
                    <span class="btn-icon">⏳</span>
                    <span class="btn-text">Part time</span>
                  </button>
                </div>
              </div>

              <!-- Study Preference -->
              <div class="form-group">
                <label>What describes your study preferences best?</label>
                <div class="select-group">
                  <button class="select-btn"
                          :class="{ active: userConfig.studyPreference === 'Mornings are best' }"
                          @click="userConfig.studyPreference = 'Mornings are best'">
                    <span class="btn-icon">🌅</span>
                    <span class="btn-text">Mornings</span>
                  </button>
                  <button class="select-btn"
                          :class="{ active: userConfig.studyPreference === 'Afternoons are best' }"
                          @click="userConfig.studyPreference = 'Afternoons are best'">
                    <span class="btn-icon">☀️</span>
                    <span class="btn-text">Afternoons</span>
                  </button>
                  <button class="select-btn"
                          :class="{ active: userConfig.studyPreference === 'Evenings are best' }"
                          @click="userConfig.studyPreference = 'Evenings are best'">
                    <span class="btn-icon">🌆</span>
                    <span class="btn-text">Evenings</span>
                  </button>
                  <button class="select-btn"
                          :class="{ active: userConfig.studyPreference === 'Late night' }"
                          @click="userConfig.studyPreference = 'Late night'">
                    <span class="btn-icon">🌙</span>
                    <span class="btn-text">Late Night</span>
                  </button>
                </div>
              </div>

              <!-- Save Preferences -->
              <button @click="saveUserConfig" class="save-button">
                <span>Continue to Step 2</span>
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M5 12h14"></path>
                  <path d="M12 5l7 7-7 7"></path>
                </svg>
              </button>
            </div>
          </div>

          <!-- Wizard Step 2: Degree Configuration -->
          <div v-else-if="showNextConfig" class="next-config">
            <div class="wizard-card">
              <div class="wizard-header">
                <div class="step-indicator">Step 2 of 2</div>
                <h2>Degree Configuration</h2>
                <p>Please provide the details for your degree program.</p>
              </div>

              <!-- (A) How many years? -->
              <div class="form-group">
                <label>How many years in your degree program?</label>
                <div class="select-group">
                  <button class="select-btn"
                          :class="{ active: nextConfig.numYears === 1 }"
                          @click="nextConfig.numYears = 1">
                    1
                  </button>
                  <button class="select-btn"
                          :class="{ active: nextConfig.numYears === 2 }"
                          @click="nextConfig.numYears = 2">
                    2
                  </button>
                  <button class="select-btn"
                          :class="{ active: nextConfig.numYears === 3 }"
                          @click="nextConfig.numYears = 3">
                    3
                  </button>
                  <button class="select-btn"
                          :class="{ active: nextConfig.numYears === 4 }"
                          @click="nextConfig.numYears = 4">
                    4
                  </button>
                  <button class="select-btn"
                          :class="{ active: nextConfig.numYears === 'other' }"
                          @click="nextConfig.numYears = 'other'">
                    Other
                  </button>
                </div>
                <input v-if="nextConfig.numYears === 'other'"
                       type="number"
                       min="1"
                       placeholder="Enter number of years"
                       v-model.number="nextConfig.customYears" />
              </div>

              <!-- (B) Semesters per year -->
              <div class="form-group">
                <label>How many semesters in one academic year?</label>
                <div class="select-group">
                  <button class="select-btn"
                          :class="{ active: nextConfig.semesters === 1 }"
                          @click="nextConfig.semesters = 1">
                    1
                  </button>
                  <button class="select-btn"
                          :class="{ active: nextConfig.semesters === 2 }"
                          @click="nextConfig.semesters = 2">
                    2
                  </button>
                  <button class="select-btn"
                          :class="{ active: nextConfig.semesters === 3 }"
                          @click="nextConfig.semesters = 3">
                    3
                  </button>
                  <button class="select-btn"
                          :class="{ active: nextConfig.semesters === 4 }"
                          @click="nextConfig.semesters = 4">
                    4
                  </button>
                  <button class="select-btn"
                          :class="{ active: nextConfig.semesters === 'other' }"
                          @click="nextConfig.semesters = 'other'">
                    Other
                  </button>
                </div>
                <input v-if="nextConfig.semesters === 'other'"
                       type="number"
                       min="1"
                       placeholder="Enter number of semesters"
                       v-model.number="nextConfig.customSemesters" />
              </div>

              <!-- (C) Credits per year -->
              <div class="form-group">
                <label>How many credits per academic year?</label>
                <div class="select-group">
                  <button class="select-btn"
                          :class="{ active: nextConfig.credits === 30 }"
                          @click="nextConfig.credits = 30">
                    30
                  </button>
                  <button class="select-btn"
                          :class="{ active: nextConfig.credits === 50 }"
                          @click="nextConfig.credits = 50">
                    50
                  </button>
                  <button class="select-btn"
                          :class="{ active: nextConfig.credits === 90 }"
                          @click="nextConfig.credits = 90">
                    90
                  </button>
                  <button class="select-btn"
                          :class="{ active: nextConfig.credits === 120 }"
                          @click="nextConfig.credits = 120">
                    120
                  </button>
                  <button class="select-btn"
                          :class="{ active: nextConfig.credits === 'other' }"
                          @click="nextConfig.credits = 'other'">
                    Other
                  </button>
                </div>
                <input v-if="nextConfig.credits === 'other'"
                       type="number"
                       min="1"
                       placeholder="Enter number of credits"
                       v-model.number="nextConfig.customCredits" />
              </div>

              <div class="button-group">
                <button class="back-button" @click="goBackToStep1">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M19 12H5"></path>
                    <path d="M12 19l-7-7 7-7"></path>
                  </svg>
                  <span>Back</span>
                </button>
                <button class="save-button" @click="saveDegreeConfig">
                  <span>Complete Setup</span>
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M20 6L9 17l-5-5"></path>
                  </svg>
                </button>
              </div>
            </div>
          </div>

          <!-- Final Dashboard: Calculator Setup -->
          <div v-else class="dashboard-content">
            <div class="welcome-banner">
              <div class="banner-content">
                <h2>Welcome to GradeGuard</h2>
                <p>Configure your years below to start tracking your academic performance.</p>
              </div>
              <div class="banner-decoration">
                <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M22 10v6M2 10l10-5 10 5-10 5z"></path>
                  <path d="M6 12v5c3 3 9 3 12 0v-5"></path>
                </svg>
              </div>
            </div>

            <div class="calculator-card">
              <h2>Degree Year Configuration</h2>
              <p class="card-description">Set up your academic years to enable GPA calculation and grade tracking.</p>

              <div class="table-container">
                <table class="years-table">
                  <thead>
                  <tr>
                    <th>Active</th>
                    <th>Year</th>
                    <th># Credits</th>
                    <th>Semesters</th>
                    <th>% Weight</th>
                  </tr>
                  </thead>
                  <tbody>
                  <tr v-for="(y, index) in calculatorConfig.years" :key="index">
                    <td>
                      <label class="toggle">
                        <input type="checkbox" v-model="y.active" />
                        <span class="toggle-slider"></span>
                      </label>
                    </td>
                    <td>{{ y.year }}</td>
                    <td>
                      <input type="number" v-model.number="y.credits" min="0" @input="onCreditsChange(index)" />
                    </td>
                    <td>
                      <input type="number" v-model.number="y.semesters" min="1" @input="onSemestersChange(index)" />
                    </td>
                    <td>
                      <input type="number" v-model.number="y.weight" min="0" max="100" @input="onWeightChange(index)" />
                    </td>
                  </tr>
                  </tbody>
                </table>
              </div>

              <div class="total-weight">
                <div class="weight-label">Total Weight:</div>
                <div class="weight-value" :class="{ 'warning': totalWeight !== 100 }">
                  {{ totalWeight }}%
                  <span v-if="totalWeight !== 100" class="weight-note">
                    (Should equal 100%)
                  </span>
                </div>
              </div>

              <button class="save-button" @click="saveCalculator">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"></path>
                  <polyline points="17 21 17 13 7 13 7 21"></polyline>
                  <polyline points="7 3 7 8 15 8"></polyline>
                </svg>
                <span>Save Configuration</span>
              </button>
            </div>
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
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M9 18l6-6-6-6" />
            </svg>
            <span class="toggle-text">Hide</span>
          </button>
          <CalendarSidebar />
        </aside>
      </transition>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { notify } from "@/services/toastService.js";
import DashboardNavBar from "@/components/DashboardNavBar.vue";
import CalendarSidebar from "@/components/CalendarSidebar.vue";
import { getDarkModePreference } from "@/services/darkModeService.js";
import { API_URL } from "@/config.js";

export default {
  name: "Dashboard",
  components: { DashboardNavBar, CalendarSidebar },
  data() {
    return {
      darkMode: false,
      notLoggedIn: false,
      sidebarVisible: true, // Sidebar is visible by default
      // Wizard states
      showSetupWizard: false,
      showNextConfig: false,
      // Basic user preferences
      userConfig: {
        academicLevel: "",
        enrollmentType: "",
        studyPreference: "",
      },
      // Calculator config from wizard
      calculatorConfig: {
        years: [],
      },
      // Next wizard step (degree config)
      nextConfig: {
        numYears: 0,
        semesters: 0,
        credits: 0,
        customYears: 0,
        customSemesters: 0,
        customCredits: 0,
      },
      isMobile: false,
      // User profile information
      userProfile: {
        firstName: "",
        email: "",
        avatar: ""
      }
    };
  },
  computed: {
    totalWeight() {
      return this.calculatorConfig.years.reduce((sum, year) => {
        return sum + (year.active ? year.weight : 0);
      }, 0);
    }
  },
  async mounted() {
    await this.checkLoginAndFetchConfig();

    // Handle dark mode
    this.darkMode = getDarkModePreference();

    // Check for mobile
    this.checkMobile();
    window.addEventListener("resize", this.checkMobile);

    // Try to load sidebar preference from localStorage
    const storedSidebarState = localStorage.getItem('sidebarVisible');
    if (storedSidebarState !== null) {
      this.sidebarVisible = storedSidebarState === 'true';
    }

    // Listen for dark mode changes from other components
    window.addEventListener('darkModeChange', this.onDarkModeChange);
  },
  beforeUnmount() {
    window.removeEventListener("resize", this.checkMobile);
    window.removeEventListener('darkModeChange', this.onDarkModeChange);
  },
  methods: {
    toggleSidebar() {
      this.sidebarVisible = !this.sidebarVisible;
      // Save preference to localStorage
      localStorage.setItem('sidebarVisible', this.sidebarVisible);
    },
    onDarkModeChange(event) {
      this.darkMode = event.detail.isDark;
    },
    handleLogout() {
      // This method is here to handle the logout event from the navbar
      // The actual logout functionality is in the navbar component
      this.notLoggedIn = true;
    },
    async checkLoginAndFetchConfig() {
      try {
        // Get user profile information
        const userProfileResponse = await axios.get(`${API_URL}/user/profile`, {
          withCredentials: true,
        });

        if (userProfileResponse.data) {
          this.userProfile = userProfileResponse.data;
        }

        // Get user configuration
        const userConfigResponse = await axios.get(`${API_URL}/user/config`, {
          withCredentials: true,
        });

        if (userConfigResponse.data) {
          this.userConfig = userConfigResponse.data;
        }

        // Show wizard if no basic preferences yet
        if (!this.userConfig.academicLevel || !this.userConfig.enrollmentType) {
          this.showSetupWizard = true;
          return;
        }

        // Fetch calculator config if it exists
        const calcResponse = await axios.get(`${API_URL}/calculator`, {
          withCredentials: true,
        });

        if (calcResponse.data?.years?.length) {
          this.calculatorConfig = calcResponse.data;
        } else {
          this.showNextConfig = true;
        }
      } catch (error) {
        console.error("Error fetching config:", error);
        if (error.response?.status === 401) {
          this.notLoggedIn = true;
          this.$router.push("/login");
        }
      }
    },
    saveUserConfig() {
      if (!this.userConfig.academicLevel || !this.userConfig.enrollmentType || !this.userConfig.studyPreference) {
        notify({ type: "warning", message: "Please complete all preference fields." });
        return;
      }

      axios
          .put(
              `${API_URL}/user/config`,
              {
                academicLevel: this.userConfig.academicLevel,
                enrollmentType: this.userConfig.enrollmentType,
                studyPreference: this.userConfig.studyPreference,
              },
              { withCredentials: true }
          )
          .then(() => {
            notify({ type: "success", message: "Preferences saved successfully!" });
            this.showSetupWizard = false;
            this.showNextConfig = true;
          })
          .catch((error) => {
            console.error("Error saving user config:", error);
            notify({ type: "error", message: "Failed to save your preferences." });
          });
    },
    goBackToStep1() {
      this.showNextConfig = false;
      this.showSetupWizard = true;
    },
    saveDegreeConfig() {
      const yearsCount =
          this.nextConfig.numYears === "other" ? this.nextConfig.customYears : this.nextConfig.numYears;
      const semCount =
          this.nextConfig.semesters === "other"
              ? this.nextConfig.customSemesters
              : this.nextConfig.semesters;
      const credCount =
          this.nextConfig.credits === "other" ? this.nextConfig.customCredits : this.nextConfig.credits;

      if (!yearsCount || !semCount || !credCount) {
        notify({
          type: "warning",
          message: "Please fill all degree details (years, semesters, credits).",
        });
        return;
      }

      const newYears = [];
      for (let i = 0; i < yearsCount; i++) {
        newYears.push({
          year: `Year ${i + 1}`,
          active: true,
          credits: credCount,
          semesters: semCount,
          weight: Math.floor(100 / yearsCount), // Distribute weight evenly
        });
      }
      this.calculatorConfig.years = newYears;

      axios
          .put(`${API_URL}/calculator/update`, this.calculatorConfig, { withCredentials: true })
          .then(() => {
            notify({ type: "success", message: "Degree configuration saved successfully!" });
            this.showNextConfig = false;
          })
          .catch((error) => {
            console.error("Error saving degree configuration:", error);
            notify({ type: "error", message: "Failed to save degree configuration." });
          });
    },
    onCreditsChange(index) {
      if (this.calculatorConfig.years[index].credits < 0) {
        this.calculatorConfig.years[index].credits = 0;
      }
    },
    onSemestersChange(index) {
      if (this.calculatorConfig.years[index].semesters < 1) {
        this.calculatorConfig.years[index].semesters = 1;
      }
    },
    onWeightChange(index) {
      if (this.calculatorConfig.years[index].weight < 0) {
        this.calculatorConfig.years[index].weight = 0;
      }
      if (this.calculatorConfig.years[index].weight > 100) {
        this.calculatorConfig.years[index].weight = 100;
      }
    },
    saveCalculator() {
      if (this.totalWeight !== 100 && this.calculatorConfig.years.some(y => y.active)) {
        notify({
          type: "warning",
          message: "The total weight of active years should equal 100%.",
        });
        return;
      }

      axios
          .put(`${API_URL}/calculator/update`, this.calculatorConfig, { withCredentials: true })
          .then(() => {
            notify({ type: "success", message: "Calculator configuration saved successfully!" });
          })
          .catch((error) => {
            console.error("Error saving calculator configuration:", error);
            notify({ type: "error", message: "Failed to save calculator configuration." });
          });
    },
    checkMobile() {
      this.isMobile = window.innerWidth <= 768;
      if (this.isMobile && this.sidebarVisible) {
        this.sidebarVisible = false;
        localStorage.setItem('sidebarVisible', 'false');
      }
    },
  },
};
</script>

<style scoped>
.dashboard {
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

/* Center content container */
.center-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
}

/* Authentication prompt */
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

/* Wizard styles */
.wizard-card {
  background-color: var(--bg-card);
  border-radius: var(--border-radius-lg);
  padding: 2rem;
  box-shadow: var(--shadow-md);
  max-width: 700px;
  width: 100%;
  margin: 0 auto;
  transition: all var(--transition-speed) ease;
}

.wizard-header {
  text-align: center;
  margin-bottom: 2rem;
}

.step-indicator {
  display: inline-block;
  background-color: var(--primary-color);
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 500;
  margin-bottom: 1rem;
}

.wizard-header h2 {
  margin: 0 0 0.5rem;
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--primary-dark);
}

.wizard-header p {
  margin: 0;
  color: var(--text-secondary);
}

/* Form styling */
.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: var(--text-primary);
}

.form-group input[type="number"] {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  font-size: 1rem;
  background-color: var(--bg-input);
  color: var(--text-primary);
  transition: border-color var(--transition-speed) ease;
}

.form-group input[type="number"]:focus {
  border-color: var(--primary-color);
  outline: none;
}

.select-group {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  justify-content: center;
  margin-bottom: 1rem;
}

.select-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  border: 2px solid var(--primary-color);
  background: transparent;
  color: var(--primary-color);
  padding: 0.75rem 1.25rem;
  border-radius: var(--border-radius);
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 500;
  transition: all 0.3s ease;
}

.select-btn:hover {
  background: rgba(123, 73, 255, 0.1);
}

.select-btn.active {
  background: var(--primary-color);
  color: white;
}

.btn-icon {
  font-size: 1.1rem;
}

/* Button styling */
.save-button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  margin-top: 1.5rem;
  padding: 0.75rem 1.5rem;
  font-weight: 500;
  background-color: var(--primary-color);
  color: white;
  border: none;
  border-radius: var(--border-radius);
  cursor: pointer;
  transition: all 0.3s ease;
  width: 100%;
  max-width: 300px;
  margin-left: auto;
  margin-right: auto;
}

.save-button:hover {
  background-color: var(--primary-dark);
  transform: translateY(-2px);
}

.button-group {
  display: flex;
  gap: 1rem;
  margin-top: 1.5rem;
}

.back-button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  font-weight: 500;
  background-color: transparent;
  color: var(--primary-color);
  border: 2px solid var(--primary-color);
  border-radius: var(--border-radius);
  cursor: pointer;
  transition: all 0.3s ease;
}

.back-button:hover {
  background-color: rgba(123, 73, 255, 0.1);
}

/* Welcome banner */
.welcome-banner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-light) 100%);
  color: white;
  padding: 2rem;
  border-radius: var(--border-radius-lg);
  margin-bottom: 2rem;
  box-shadow: var(--shadow-md);
}

.banner-content h2 {
  margin: 0 0 0.5rem;
  font-size: 1.5rem;
  font-weight: 600;
}

.banner-content p {
  margin: 0;
  opacity: 0.9;
}

.banner-decoration svg {
  opacity: 0.6;
}

/* Calculator card */
.calculator-card {
  background-color: var(--bg-card);
  border-radius: var(--border-radius-lg);
  padding: 2rem;
  box-shadow: var(--shadow-md);
}

.calculator-card h2 {
  margin: 0 0 0.5rem;
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--primary-dark);
}

.card-description {
  color: var(--text-secondary);
  margin-bottom: 2rem;
}

.table-container {
  overflow-x: auto;
  margin-bottom: 1.5rem;
}

.years-table {
  width: 100%;
  border-collapse: collapse;
  border-spacing: 0;
}

.years-table th,
.years-table td {
  padding: 1rem;
  text-align: center;
  border-bottom: 1px solid var(--border-color);
}

.years-table th {
  background-color: rgba(123, 73, 255, 0.05);
  color: var(--primary-dark);
  font-weight: 500;
}

.years-table input[type="number"] {
  width: 80px;
  padding: 0.5rem;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  text-align: center;
  background-color: var(--bg-input);
  color: var(--text-primary);
}

.years-table input[type="number"]:focus {
  border-color: var(--primary-color);
  outline: none;
}

/* Toggle switch */
.toggle {
  position: relative;
  display: inline-block;
  width: 40px;
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
  transition: 0.4s;
  border-radius: 24px;
}

.toggle-slider:before {
  position: absolute;
  content: "";
  height: 16px;
  width: 16px;
  left: 4px;
  bottom: 4px;
  background-color: white;
  transition: 0.4s;
  border-radius: 50%;
}

input:checked + .toggle-slider {
  background-color: var(--primary-color);
}

input:focus + .toggle-slider {
  box-shadow: 0 0 1px var(--primary-color);
}

input:checked + .toggle-slider:before {
  transform: translateX(16px);
}

/* Total weight display */
.total-weight {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  margin-bottom: 1.5rem;
}

.weight-label {
  font-weight: 500;
  margin-right: 0.5rem;
}

.weight-value {
  font-weight: 600;
  color: var(--success-color);
}

.weight-value.warning {
  color: var(--warning-color);
}

.weight-note {
  font-size: 0.8rem;
  font-weight: normal;
  opacity: 0.7;
  margin-left: 0.5rem;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .dashboard-layout {
    flex-direction: column;
    padding-top: 60px; /* Smaller navbar height */
  }

  .dashboard-main-content {
    padding: 1.5rem;
  }

  .dashboard-sidebar {
    width: 100%;
    position: fixed;
    top: 60px;
    left: 0;
    right: 0;
    bottom: 0;
    z-index: 100;
    border-radius: 0;
    border-left: none;
  }

  .sidebar-hide-button {
    top: 1rem;
    right: 1rem;
  }

  .sidebar-show-button {
    right: 1rem;
    bottom: 1rem;
    top: auto;
  }

  .select-group {
    flex-direction: column;
  }

  .select-btn {
    width: 100%;
  }

  .button-group {
    flex-direction: column;
  }

  .slide-enter-from,
  .slide-leave-to {
    transform: translateY(100%);
  }

  .welcome-banner {
    flex-direction: column;
    text-align: center;
    gap: 1rem;
  }
}

/* Small screen adjustments */
@media (max-width: 480px) {
  .dashboard-layout,
  .dashboard-main-content {
    padding: 1rem;
  }

  .wizard-card,
  .calculator-card {
    padding: 1.5rem;
  }

  .years-table th,
  .years-table td {
    padding: 0.75rem 0.5rem;
  }

  .total-weight {
    flex-direction: column;
    align-items: flex-end;
  }
}
</style>