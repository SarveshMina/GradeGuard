<template>
  <div class="dashboard" ref="dashboardRef">
    <!-- NavBar at the very top -->
    <NavBar mode="dashboard" :isMobile="isMobile" />

    <!-- Dashboard content starts below NavBar -->
    <div class="dashboard-content-wrapper">
      <h1>Dashboard</h1>

      <!-- If not logged in -->
      <div v-if="notLoggedIn" class="center-content">
        <p>You are not logged in!</p>
        <p><a href="/login">Go to Login</a></p>
      </div>

      <!-- Otherwise -->
      <div v-else class="center-content">
        <!-- 1. Setup Wizard for multi-choice preferences -->
        <div v-if="showSetupWizard" class="setup-wizard">
          <h2>Welcome! Let’s set up your preferences</h2>
          <p>Please select an option for each question.</p>

          <!-- Academic Level -->
          <div class="form-group">
            <label>What is your current academic level?</label>
            <div class="select-group">
              <button
                  class="select-btn"
                  :class="{ active: userConfig.academicLevel === 'Undergraduate' }"
                  @click="userConfig.academicLevel = 'Undergraduate'"
              >
                🎓 Undergraduate
              </button>
              <button
                  class="select-btn"
                  :class="{ active: userConfig.academicLevel === 'Postgraduate (Masters)' }"
                  @click="userConfig.academicLevel = 'Postgraduate (Masters)'"
              >
                🧑‍🎓 Masters
              </button>
              <button
                  class="select-btn"
                  :class="{ active: userConfig.academicLevel === 'Postgraduate (PhD)' }"
                  @click="userConfig.academicLevel = 'Postgraduate (PhD)'"
              >
                👨‍🎓 PhD
              </button>
            </div>
          </div>

          <!-- Enrollment Type -->
          <div class="form-group">
            <label>Are you full-time or part-time?</label>
            <div class="select-group">
              <button
                  class="select-btn"
                  :class="{ active: userConfig.enrollmentType === 'Full time' }"
                  @click="userConfig.enrollmentType = 'Full time'"
              >
                ✅ Full time
              </button>
              <button
                  class="select-btn"
                  :class="{ active: userConfig.enrollmentType === 'Part time' }"
                  @click="userConfig.enrollmentType = 'Part time'"
              >
                ⏳ Part time
              </button>
            </div>
          </div>

          <!-- Study Preference -->
          <div class="form-group">
            <label>What describes your study preferences best?</label>
            <div class="select-group">
              <button
                  class="select-btn"
                  :class="{ active: userConfig.studyPreference === 'Mornings are best' }"
                  @click="userConfig.studyPreference = 'Mornings are best'"
              >
                🌅 Mornings
              </button>
              <button
                  class="select-btn"
                  :class="{ active: userConfig.studyPreference === 'Afternoons are best' }"
                  @click="userConfig.studyPreference = 'Afternoons are best'"
              >
                ☀️ Afternoons
              </button>
              <button
                  class="select-btn"
                  :class="{ active: userConfig.studyPreference === 'Evenings are best' }"
                  @click="userConfig.studyPreference = 'Evenings are best'"
              >
                🌆 Evenings
              </button>
              <button
                  class="select-btn"
                  :class="{ active: userConfig.studyPreference === 'Late night' }"
                  @click="userConfig.studyPreference = 'Late night'"
              >
                🌙 Late Night
              </button>
            </div>
          </div>

          <!-- Save Preferences -->
          <button @click="saveUserConfig" class="save-button">
            Save Preferences
          </button>
        </div>

        <!-- 2. Normal Dashboard (Calculator UI, etc.) -->
        <div v-else class="dashboard-content">
          <h2>Select your Years</h2>
          <table class="years-table">
            <thead>
            <tr>
              <th>Active</th>
              <th>Year</th>
              <th># Credits</th>
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
                <input
                    type="number"
                    v-model.number="y.credits"
                    min="0"
                    @input="onCreditsChange(index)"
                />
              </td>
              <td>
                <input
                    type="number"
                    v-model.number="y.weight"
                    min="0"
                    max="100"
                    @input="onWeightChange(index)"
                />
              </td>
            </tr>
            </tbody>
          </table>
          <button class="save-button" @click="saveYears">
            Save Years
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { notify } from "@/services/toastService.js";
import NavBar from "@/components/NavBar.vue";
import { getDarkModePreference, setDarkModePreference } from "@/services/darkModeService.js";
import { API_URL } from "@/config.js";

export default {
  name: "Dashboard",
  components: { NavBar },
  data() {
    return {
      darkMode: false,
      notLoggedIn: false,
      showSetupWizard: false,
      userConfig: {
        academicLevel: "",
        enrollmentType: "",
        studyPreference: "",
      },
      calculatorConfig: {
        years: [
          { year: "Year 1", active: false, credits: 120, weight: 0 },
          { year: "Year 2", active: false, credits: 120, weight: 0 },
          { year: "Year 3", active: false, credits: 120, weight: 0 },
          { year: "Year 4", active: false, credits: 120, weight: 0 },
          { year: "Masters", active: false, credits: 180, weight: 0 },
        ],
      },
      // Modal-related variables (for university & degree selection)
      universityDocs: [],
      selectedUniversityDoc: null,
      universitySearch: "",
      showUniversityModal: false,
      searchTimeout: null,
      searchOffset: 0,
      searchLimit: 10,
      lastFetchedCount: 0,
      isLoadingMore: false,
      majorSearch: "",
      showMajorModal: false,
      showCustomMajorInput: false,
      customMajor: "",
      forgotEmail: "",
      isMobile: false,
    };
  },
  async mounted() {
    await this.checkLoginAndFetchConfig();
    // Initialize dark mode from stored preference
    this.darkMode = getDarkModePreference();
    if (this.darkMode) {
      document.body.classList.add("dark-mode");
    } else {
      document.body.classList.remove("dark-mode");
    }
    // Immediately update the background gradient using default center coordinates
    this.updateBackgroundGradient();
    // Also attach the mousemove listener for reactive gradient changes
    this.initMouseReactiveGradient();
    // Set up mobile detection
    this.checkMobile();
    window.addEventListener("resize", this.checkMobile);
    // Listen to localStorage changes (in case dark mode is toggled elsewhere)
    window.addEventListener("storage", this.onStorageChange);
  },
  beforeUnmount() {
    window.removeEventListener("resize", this.checkMobile);
    window.removeEventListener("storage", this.onStorageChange);
    document.body.style.overflow = "";
  },
  methods: {
    initMouseReactiveGradient() {
      const container = this.$refs.dashboardRef;
      if (container) {
        container.addEventListener("mousemove", (e) => {
          const rect = container.getBoundingClientRect();
          const x = e.clientX - rect.left;
          const y = e.clientY - rect.top;
          const percentX = (x / rect.width) * 100;
          const percentY = (y / rect.height) * 100;
          const gradient = this.darkMode
              ? `radial-gradient(circle at ${percentX}% ${percentY}%, #444, #000)`
              : `radial-gradient(circle at ${percentX}% ${percentY}%, #b191fc, #f2f2f2)`;
          container.style.background = gradient;
        });
      }
    },
    updateBackgroundGradient() {
      const container = this.$refs.dashboardRef;
      if (container) {
        // Use center coordinates (50%,50%) for initial gradient update
        const gradient = this.darkMode
            ? `radial-gradient(circle at 50% 50%, #444, #000)`
            : `radial-gradient(circle at 50% 50%, #b191fc, #f2f2f2)`;
        container.style.background = gradient;
      }
    },
    onStorageChange(e) {
      if (e.key === "darkMode") {
        this.darkMode = e.newValue === "true";
        if (this.darkMode) {
          document.body.classList.add("dark-mode");
        } else {
          document.body.classList.remove("dark-mode");
        }
        this.updateBackgroundGradient();
      }
    },
    async checkLoginAndFetchConfig() {
      try {
        const userConfigResponse = await axios.get(`${API_URL}/user/config`, { withCredentials: true });
        if (userConfigResponse.data) {
          this.userConfig = userConfigResponse.data;
        }
        if (!this.userConfig.academicLevel || !this.userConfig.enrollmentType) {
          this.showSetupWizard = true;
        }
        const calcResponse = await axios.get(`${API_URL}/calculator`, { withCredentials: true });
        if (calcResponse.data && calcResponse.data.years) {
          this.calculatorConfig = calcResponse.data;
        }
      } catch (error) {
        console.error("Error fetching config:", error);
        if (error.response && error.response.status === 401) {
          this.notLoggedIn = true;
          this.$router.push("/login");
        }
      }
    },
    async saveUserConfig() {
      try {
        await axios.put(`${API_URL}/user/config`, this.userConfig, { withCredentials: true });
        notify({ type: "success", message: "Preferences saved successfully!" });
        this.showSetupWizard = false;
      } catch (error) {
        console.error("Error saving user config:", error);
        notify({ type: "error", message: "Failed to save your preferences." });
      }
    },
    async saveYears() {
      try {
        await axios.put(`${API_URL}/calculator`, this.calculatorConfig, { withCredentials: true });
        notify({ type: "success", message: "Calculator configuration saved successfully!" });
      } catch (error) {
        console.error("Error saving calculator config:", error);
        notify({ type: "error", message: "Failed to save calculator configuration." });
      }
    },
    onCreditsChange(index) {
      if (this.calculatorConfig.years[index].credits < 0) {
        this.calculatorConfig.years[index].credits = 0;
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
    // Modal functions for university & degree selection (unchanged)
    openUniversityModal() {
      console.log("openUniversityModal triggered");
      this.showUniversityModal = true;
      this.universitySearch = "";
      this.universityDocs = [];
      this.searchOffset = 0;
      this.searchLimit = 10;
      document.body.style.overflow = "hidden";
    },
    closeUniversityModal() {
      this.showUniversityModal = false;
      document.body.style.overflow = "";
    },
    selectUniversity(uniDoc) {
      this.selectedUniversityDoc = uniDoc;
      this.closeUniversityModal();
    },
    openMajorModal() {
      if (!this.selectedUniversityDoc) {
        notify({ type: "warning", message: "Please select a university first." });
        return;
      }
      this.showMajorModal = true;
      this.majorSearch = "";
      this.showCustomMajorInput = false;
      this.customMajor = "";
      document.body.style.overflow = "hidden";
    },
    closeMajorModal() {
      this.showMajorModal = false;
      this.showCustomMajorInput = false;
      document.body.style.overflow = "";
    },
    selectMajor(majorName) {
      this.degree = majorName;
      this.closeMajorModal();
    },
    enableCustomMajor() {
      this.showCustomMajorInput = true;
      this.customMajor = "";
    },
    saveCustomMajor() {
      if (this.customMajor.trim() !== "") {
        this.degree = this.customMajor.trim();
        this.closeMajorModal();
      } else {
        notify({ type: "warning", message: "Please enter your degree." });
      }
    },
    async handleSignUp() {
      try {
        const payload = {
          firstName: this.firstName,
          email: this.signUpEmail,
          password: this.signUpPassword,
          university: this.selectedUniversityDoc ? this.selectedUniversityDoc.name : "",
          degree: this.degree,
          calcType: this.calcType,
        };
        const response = await axios.post(`${API_URL}/register`, payload, { withCredentials: true });
        notify({ type: "success", message: "Sign up successful: " + response.data.message });
        if (this.selectedUniversityDoc) {
          const updatedResponse = await axios.get(`${API_URL}/stats/university`, { params: { name: this.selectedUniversityDoc.name } });
          this.selectedUniversityDoc = updatedResponse.data;
        }
      } catch (error) {
        console.error(error);
        const errMsg = error.response?.data?.error || error.message;
        notify({ type: "error", message: "Sign up failed: " + errMsg });
      }
    },
    async handleLogin() {
      try {
        await axios.post(`${API_URL}/login`, {
          email: this.loginEmail,
          password: this.loginPassword,
        }, { withCredentials: true });
        notify({ type: "success", message: "Login successful." });
        this.$router.push("/dashboard");
      } catch (error) {
        notify({ type: "error", message: "Login failed: " + (error.response?.data?.error || error.message) });
      }
    },
    async handleForgot() {
      notify({ type: "info", message: "Forgot password request sent for " + this.forgotEmail });
    },
    switchToSignup() {
      this.formMode = "signup";
      this.signUpStep = 1;
      this.$router.push({ path: "/login", query: { mode: "signup" } });
    },
    switchToLogin() {
      this.formMode = "login";
      this.$router.push({ path: "/login", query: { mode: "login" } });
    },
    switchToForgot() {
      this.formMode = "forgot";
    },
    loginWithGoogle() {
      window.location.href = `${API_URL}/auth/google`;
    },
    async searchUniversities(query, loadMore = false) {
      try {
        if (!loadMore) {
          this.searchLimit = 10;
          this.searchOffset = 0;
        } else {
          this.searchLimit = 20;
          this.isLoadingMore = true;
        }
        const response = await axios.get(`${API_URL}/universities/search`, {
          params: {
            query,
            limit: this.searchLimit,
            offset: this.searchOffset,
          },
        });
        const results = response.data;
        this.lastFetchedCount = results.length;
        if (loadMore) {
          const newResults = results.filter(
              (u) => !this.universityDocs.some((existing) => existing.id === u.id)
          );
          this.universityDocs = this.universityDocs.concat(newResults);
          this.searchOffset += newResults.length;
          this.isLoadingMore = false;
        } else {
          this.universityDocs = results;
          this.searchOffset = results.length;
        }
      } catch (err) {
        console.error("Error searching universities:", err);
        this.isLoadingMore = false;
      }
    },
    loadMoreUniversities() {
      this.searchUniversities(this.universitySearch, true);
    },
  },
  watch: {
    universitySearch(newQuery) {
      if (this.searchTimeout) clearTimeout(this.searchTimeout);
      if (newQuery.trim().length >= 3) {
        this.searchOffset = 0;
        this.searchTimeout = setTimeout(() => {
          this.searchUniversities(newQuery, false);
        }, 300);
      } else {
        this.universityDocs = [];
      }
    },
    "$route.query.mode"(newMode) {
      if (newMode === "signup") {
        this.formMode = "signup";
        this.signUpStep = 1;
      } else {
        this.formMode = "login";
      }
    },
    // Watch darkMode and update the background gradient immediately
    darkMode(newVal) {
      this.updateBackgroundGradient();
    },
  },
};
</script>

<style scoped>
/* Center content */
.center-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

/* Dashboard container */
.dashboard {
  padding: 2rem;
  text-align: center;
}

/* Wrapper to push content below NavBar */
.dashboard-content-wrapper {
  margin-top: 5rem; /* Adjust spacing as needed */
}

/* Setup Wizard */
.setup-wizard {
  margin: 2rem auto;
  max-width: 500px;
  text-align: center;
}

/* Form group and labels */
.form-group {
  margin-bottom: 1rem;
}
.form-group label {
  display: block;
  margin-bottom: 0.25rem;
  font-weight: 600;
}

/* Select-group styles */
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
.select-btn:hover {
  background: var(--link-color);
  color: #fff;
}
.select-btn.active {
  background: var(--link-color);
  color: #fff;
}

/* Save button */
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

/* Table styling */
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

.years-table td {
  border: 1px solid #ccc;
  padding: 0.75rem;
  text-align: center;
}

/* Existing styles remain unchanged */
.auth-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background: var(--bg-gradient);
  color: var(--text-color);
  font-family: "Montserrat", sans-serif;
}

.dark-mode-toggle-container {
  display: flex;
  justify-content: flex-end;
  padding: 1rem;
}

.mobile-header {
  text-align: center;
  padding: 1rem;
}

.mobile-header .mobile-logo {
  font-size: 50px;
  font-weight: 700;
  color: #512DA8;
}

/* Remove Footer styling for Dashboard */

.auth-main {
  --link-color: #512da8;
  background: #ffffff;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 8px 16px rgba(0,0,0,0.1);
  width: 100%;
  max-width: 360px;
  color: #000;
  padding-bottom: 2.5rem;
}

.auth-main h1 {
  margin-bottom: 1.5rem;
  text-align: center;
  font-size: 1.5rem;
  color: #000;
}

.auth-main p {
  text-align: center;
  font-size: 0.9rem;
  margin-bottom: 1.5rem;
  color: #000;
}

.auth-main p a {
  color: var(--link-color);
  text-decoration: none;
  transition: color 0.3s ease;
}

.auth-main p a:hover {
  text-decoration: underline;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 1rem;
  color: #333;
  background: #fff;
  box-sizing: border-box;
  transition: border 0.2s ease;
}

.form-group input:focus,
.form-group select:focus {
  border-color: var(--link-color);
  outline: none;
}

.university-selector {
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  cursor: pointer;
  background: #fff;
}

.university-selector:hover {
  border-color: var(--link-color);
}

.university-selector .placeholder {
  color: #aaa;
}

.forgot-container {
  text-align: right;
  margin-bottom: 1.5rem;
}

.forgot-link {
  font-size: 0.85rem;
  color: var(--link-color);
  text-decoration: none;
  position: relative;
  transition: color 0.3s ease;
}

.forgot-link::after {
  content: "";
  position: absolute;
  left: 0;
  bottom: -2px;
  width: 0;
  height: 2px;
  background: var(--link-color);
  transition: width 0.3s ease;
}

.forgot-link:hover::after {
  width: 100%;
}

.auth-button {
  width: 100%;
  padding: 0.75rem;
  border: none;
  border-radius: 24px;
  background: var(--link-color);
  color: #fff;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.auth-button:hover {
  transform: scale(1.03);
  box-shadow: 0 4px 12px rgba(0,0,0,0.2);
}

.small-btn {
  background: var(--link-color);
  color: #fff;
  border: none;
  border-radius: 20px;
  padding: 0.4rem 0.8rem;
  font-size: 0.85rem;
  cursor: pointer;
  transition: background 0.3s ease;
  margin-top: 0.5rem;
}

.small-btn:hover {
  background: #000;
}

.next-btn-container {
  text-align: right;
}

.signup-buttons {
  display: flex;
  justify-content: flex-end;
  margin-top: 1rem;
}

.signup-back {
  text-align: left;
  margin-bottom: 1rem;
}

.signup-back a {
  color: var(--link-color);
  text-decoration: none;
  font-size: 0.9rem;
  transition: color 0.3s ease;
}

.signup-back a:hover {
  text-decoration: underline;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s ease;
}
.fade-enter, .fade-leave-to {
  opacity: 0;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2000;
  padding: 1rem;
  overflow: hidden;
}

.modal-content {
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid rgba(0, 0, 0, 0.1);
  box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37),
  0 0 20px 5px rgba(81,45,168,0.6);
  border-radius: 16px;
  padding: 1.5rem;
  width: 100%;
  max-width: 400px;
  overflow: hidden;
  transition: transform 0.3s ease;
  position: relative;
  box-sizing: border-box;
  max-height: 70vh;
}

.dark-mode .modal-content {
  background: rgba(0, 0, 0, 0.7);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h2 {
  margin: 0;
}

.close-button {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
}

.list-container {
  max-height: 40vh;
  overflow-y: auto;
  margin-top: 1rem;
}

.list-container::-webkit-scrollbar {
  width: 8px;
}

.list-container::-webkit-scrollbar-track {
  background: transparent;
}

.list-container::-webkit-scrollbar-thumb {
  background-color: var(--link-color);
  border-radius: 4px;
}

.list-container::-webkit-scrollbar-thumb:hover {
  background-color: #555;
}

.modal-enter-active {
  animation: scaleIn 0.3s forwards;
}

@keyframes scaleIn {
  from {
    transform: scale(0.8);
    opacity: 0;
  }
  to {
    transform: scale(1);
    opacity: 1;
  }
}

.search-input {
  width: 100%;
  padding: 0.5rem;
  margin-bottom: 1rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  transition: all 0.3s ease;
}

.university-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.university-list li {
  padding: 0.5rem;
  border-bottom: 1px solid #eee;
  cursor: pointer;
  transition: background 0.2s ease;
}

.university-list li:hover {
  background: #f0f0f0;
  color: #000;
}

.university-list li.custom-option {
  font-style: italic;
  color: var(--link-color);
}

.spinner {
  display: inline-block;
  width: 20px;
  height: 20px;
  border: 3px solid rgba(0, 0, 0, 0.3);
  border-radius: 50%;
  border-top-color: #000;
  animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.oauth-container {
  margin-top: 1rem;
  display: flex;
  justify-content: center;
}

.google-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 24px;
  background: #fff;
  box-shadow: 0 2px 4px rgba(0,0,0,0.2);
  cursor: pointer;
  transition: background 0.3s ease;
  margin-top: 1rem;
}

.google-btn:hover {
  background: #f7f7f7;
}

.google-logo {
  width: 20px;
  height: 20px;
  margin-right: 0.5rem;
}
</style>
