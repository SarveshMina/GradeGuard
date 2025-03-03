<!-- src/views/DashBoard.vue (Updated) -->
<template>
  <div class="dashboard">
    <!-- NavBar at the very top -->
    <NavBar mode="dashboard" :isMobile="isMobile" />

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
        <span class="toggle-text">View Calendar</span>
      </button>

      <!-- Main Content Area -->
      <div class="dashboard-main-content" :class="{ 'expanded': !sidebarVisible }">
        <h1>Dashboard</h1>

        <!-- If not logged in -->
        <div v-if="notLoggedIn" class="center-content">
          <p>You are not logged in!</p>
          <p><a href="/login">Go to Login</a></p>
        </div>

        <!-- Otherwise, show the wizard(s) or the final calculator -->
        <div v-else class="center-content">
          <!-- Wizard Step 1: Basic User Preferences -->
          <div v-if="showSetupWizard" class="setup-wizard">
            <h2>Welcome! Let's set up your preferences</h2>
            <p>Please select an option for each question.</p>

            <!-- Academic Level -->
            <div class="form-group">
              <label>What is your current academic level?</label>
              <div class="select-group">
                <button class="select-btn"
                        :class="{ active: userConfig.academicLevel === 'Undergraduate' }"
                        @click="userConfig.academicLevel = 'Undergraduate'">
                  🎓 Undergraduate
                </button>
                <button class="select-btn"
                        :class="{ active: userConfig.academicLevel === 'Postgraduate (Masters)' }"
                        @click="userConfig.academicLevel = 'Postgraduate (Masters)'">
                  🧑‍🎓 Masters
                </button>
                <button class="select-btn"
                        :class="{ active: userConfig.academicLevel === 'Postgraduate (PhD)' }"
                        @click="userConfig.academicLevel = 'Postgraduate (PhD)'">
                  👨‍🎓 PhD
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
                  ✅ Full time
                </button>
                <button class="select-btn"
                        :class="{ active: userConfig.enrollmentType === 'Part time' }"
                        @click="userConfig.enrollmentType = 'Part time'">
                  ⏳ Part time
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
                  🌅 Mornings
                </button>
                <button class="select-btn"
                        :class="{ active: userConfig.studyPreference === 'Afternoons are best' }"
                        @click="userConfig.studyPreference = 'Afternoons are best'">
                  ☀️ Afternoons
                </button>
                <button class="select-btn"
                        :class="{ active: userConfig.studyPreference === 'Evenings are best' }"
                        @click="userConfig.studyPreference = 'Evenings are best'">
                  🌆 Evenings
                </button>
                <button class="select-btn"
                        :class="{ active: userConfig.studyPreference === 'Late night' }"
                        @click="userConfig.studyPreference = 'Late night'">
                  🌙 Late Night
                </button>
              </div>
            </div>

            <!-- Save Preferences -->
            <button @click="saveUserConfig" class="save-button">
              Save Preferences
            </button>
          </div>

          <!-- Wizard Step 2: Degree Configuration -->
          <div v-else-if="showNextConfig" class="next-config">
            <h2>Degree Configuration</h2>
            <p>Please provide the details for your degree.</p>

            <!-- (A) How many years? -->
            <div class="form-group">
              <label>How many years do you have in your Degree?</label>
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
                     placeholder="Enter # of years"
                     v-model.number="nextConfig.customYears" />
            </div>

            <!-- (B) Semesters per year -->
            <div class="form-group">
              <label>How many semesters do you have in 1 Year?</label>
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
                     placeholder="Enter # of semesters"
                     v-model.number="nextConfig.customSemesters" />
            </div>

            <!-- (C) Credits per year -->
            <div class="form-group">
              <label>How many credits each year has?</label>
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
                     placeholder="Enter # of credits"
                     v-model.number="nextConfig.customCredits" />
            </div>

            <button class="save-button" @click="saveDegreeConfig">
              Save Configuration
            </button>
          </div>

          <!-- Final Dashboard: Calculator Setup -->
          <div v-else class="dashboard-content">
            <h2>Calculator Setup</h2>
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
                  <input type="checkbox" v-model="y.active" />
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
            <button class="save-button" @click="saveCalculator">
              Save Years
            </button>
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
            <span class="toggle-text">Hide Calendar</span>
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
import NavBar from "@/components/NavBar.vue";
import CalendarSidebar from "@/components/CalendarSidebar.vue";
import { getDarkModePreference } from "@/services/darkModeService.js";
import { API_URL } from "@/config.js";

export default {
  name: "Dashboard",
  components: { NavBar, CalendarSidebar },
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
    };
  },
  async mounted() {
    await this.checkLoginAndFetchConfig();

    // Handle dark mode
    this.darkMode = getDarkModePreference();
    if (this.darkMode) {
      document.body.classList.add("dark-mode");
    } else {
      document.body.classList.remove("dark-mode");
    }

    this.checkMobile();
    window.addEventListener("resize", this.checkMobile);

    // Try to load sidebar preference from localStorage
    const storedSidebarState = localStorage.getItem('sidebarVisible');
    if (storedSidebarState !== null) {
      this.sidebarVisible = storedSidebarState === 'true';
    }
  },
  beforeUnmount() {
    window.removeEventListener("resize", this.checkMobile);
  },
  methods: {
    toggleSidebar() {
      this.sidebarVisible = !this.sidebarVisible;
      // Save preference to localStorage
      localStorage.setItem('sidebarVisible', this.sidebarVisible);
    },
    async checkLoginAndFetchConfig() {
      try {
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
          active: false,
          credits: credCount,
          semesters: semCount,
          weight: 0,
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
    },
  },
};
</script>

<style scoped>
.center-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.dashboard {
  padding: 2rem;
  text-align: center;
}

/* Flex layout for main content and sidebar */
.dashboard-layout {
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  position: relative; /* For absolutely positioned toggle button */
}

/* Main content styles */
.dashboard-main-content {
  flex: 1;
  padding: 2rem;
  transition: all 0.3s ease-in-out;
}

.dashboard-main-content.expanded {
  margin-right: 0;
}

/* Sidebar toggle buttons */
.sidebar-toggle {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  background-color: #7b49ff;
  color: white;
  border: none;
  border-radius: 99px; /* Match the Navbar button style */
  padding: 0.6rem 1.2rem;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(123, 73, 255, 0.4);
  transition: all 0.2s ease;
  z-index: 10;
}

.toggle-text {
  font-size: 16px;
  font-weight: 600;
  /* Match the text style from the Navbar */
}

.sidebar-toggle:hover {
  background-color: #512da8;
  transform: scale(1.05);
}

.close-button {
  position: absolute;
  right: 10px;
  top: 10px;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background-color: #7b49ff;
  color: white;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(123, 73, 255, 0.2);
  transition: all 0.2s ease;
  z-index: 10;
  padding: 0;
}

.close-button:hover {
  background-color: #512da8;
  transform: scale(1.1);
}

.sidebar-show-button {
  position: absolute;
  right: 2rem; /* Match the NavBar padding */
  top: 0; /* Position at the top of dashboard-layout */
  animation: pulse 2s infinite;
  margin-top: 1rem; /* Add some space from the top */
}

@keyframes pulse {
  0% {
    box-shadow: 0 0 0 0 rgba(123, 73, 255, 0.7);
  }
  70% {
    box-shadow: 0 0 0 10px rgba(123, 73, 255, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(123, 73, 255, 0);
  }
}

/* Sidebar styles */
.dashboard-sidebar {
  position: relative;
  border-left: 1px solid #ccc;
  background-color: var(--form-bg);
  min-height: 80vh;
  padding: 1rem;
}

body.dark-mode .dashboard-sidebar {
  border-color: #e0e0e0;
  background-color: #2c2c2c;
}

/* Slide transition for sidebar */
.slide-enter-active,
.slide-leave-active {
  transition: transform 0.3s ease, opacity 0.3s ease;
}

.slide-enter-from,
.slide-leave-to {
  transform: translateX(100%);
  opacity: 0;
}

/* Wizard steps styling */
.setup-wizard,
.next-config {
  margin: 2rem auto;
  max-width: 600px;
  text-align: center;
}

.form-group {
  margin-bottom: 1rem;
}
.form-group label {
  display: block;
  margin-bottom: 0.25rem;
  font-weight: 600;
}

.form-group input[type="number"] {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 1rem;
  margin-top: 0.5rem;
}

.select-group {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  justify-content: center;
  margin-bottom: 1rem;
}

.select-btn {
  border: 2px solid var(--link-color);
  background: transparent;
  color: var(--link-color);
  padding: 0.5rem 1rem;
  border-radius: 24px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background 0.3s ease, color 0.3s ease;
}

.select-btn:hover,
.select-btn.active {
  background: var(--link-color);
  color: #fff;
}

.save-button {
  margin-top: 1rem;
  padding: 0.75rem 1.5rem;
  font-weight: bold;
  background-color: #512da8;
  color: #fff;
  border: none;
  border-radius: 24px;
  cursor: pointer;
  transition: 0.3s;
}
.save-button:hover {
  background-color: #3f1e8c;
  transform: scale(1.02);
}

.dashboard-content {
  margin-top: 2rem;
}

.years-table {
  margin: 2rem auto;
  border-collapse: collapse;
  width: 80%;
  max-width: 600px;
}

.years-table th,
.years-table td {
  border: 1px solid #ccc;
  padding: 0.75rem;
  text-align: center;
}

.years-table th {
  background-color: #f2f2f2;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .dashboard-layout {
    flex-direction: column;
  }

  .dashboard-sidebar {
    width: 100%;
    border-left: none;
    border-top: 1px solid #ccc;
  }

  .sidebar-hide-button {
    right: 10px;
    top: 10px;
  }

  .sidebar-show-button {
    right: 10px;
    top: 10px;
  }

  .slide-enter-from,
  .slide-leave-to {
    transform: translateY(100%);
  }
}
</style>