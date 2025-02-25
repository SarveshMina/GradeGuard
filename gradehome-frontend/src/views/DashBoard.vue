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

      <!-- Otherwise, show dashboard content -->
      <div v-else class="center-content">
        <!-- 1. Setup Wizard for basic preferences -->
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

        <!-- 2. Next Config Section: Detailed Degree Setup -->
        <div v-else-if="showNextConfig" class="next-config">
          <h2>Degree Configuration</h2>
          <p>Please provide the details for your degree.</p>
          <div class="form-group">
            <label>Number of Years in your Degree</label>
            <input
                type="number"
                v-model.number="nextConfig.numYears"
                min="1"
                placeholder="e.g., 4"
                @input="initNextConfig"
            />
          </div>
          <div v-for="(yearConfig, index) in nextConfig.years" :key="index" class="year-config">
            <h3>Year {{ index + 1 }}</h3>
            <div class="form-group">
              <label># Credits</label>
              <input
                  type="number"
                  v-model.number="yearConfig.credits"
                  min="0"
              />
            </div>
            <div class="form-group">
              <label># Semesters</label>
              <input
                  type="number"
                  v-model.number="yearConfig.semesters"
                  min="1"
              />
            </div>
            <div class="form-group">
              <label>Required Passing %</label>
              <input
                  type="number"
                  v-model.number="yearConfig.passPercentage"
                  min="0"
                  max="100"
              />
            </div>
          </div>
          <button class="save-button" @click="saveYears">
            Save Configuration
          </button>
        </div>

        <!-- 3. Normal Dashboard (Calculator UI, etc.) -->
        <div v-else class="dashboard-content">
          <h2>Calculator Setup</h2>
          <table class="years-table">
            <thead>
            <tr>
              <th>Active</th>
              <th>Year</th>
              <th># Credits</th>
              <th>Semesters</th>
              <th>Pass %</th>
              <th>% Weight</th>
            </tr>
            </thead>
            <tbody>
            <tr v-for="(y, index) in calculatorConfig.years" :key="index">
              <td><input type="checkbox" v-model="y.active" /></td>
              <td>{{ y.year }}</td>
              <td><input type="number" v-model.number="y.credits" min="0" @input="onCreditsChange(index)" /></td>
              <td><input type="number" v-model.number="y.semesters" min="1" @input="onSemestersChange(index)" /></td>
              <td><input type="number" v-model.number="y.passPercentage" min="0" max="100" @input="onPassPercentageChange(index)" /></td>
              <td><input type="number" v-model.number="y.weight" min="0" max="100" @input="onWeightChange(index)" /></td>
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
import { getDarkModePreference } from "@/services/darkModeService.js";
import { API_URL } from "@/config.js";

export default {
  name: "Dashboard",
  components: { NavBar },
  data() {
    return {
      darkMode: false,
      notLoggedIn: false,
      // Which section to show:
      // showSetupWizard (basic preferences) > showNextConfig (detailed degree setup) > normal dashboard view
      showSetupWizard: false,
      showNextConfig: false,
      userConfig: {
        academicLevel: "",
        enrollmentType: "",
        studyPreference: "",
      },
      // Default calculator config (if exists, fetched from backend)
      calculatorConfig: {
        years: [
          { year: "Year 1", active: false, credits: 120, semesters: 2, passPercentage: 50, weight: 0 },
          { year: "Year 2", active: false, credits: 120, semesters: 2, passPercentage: 50, weight: 0 },
          { year: "Year 3", active: false, credits: 120, semesters: 2, passPercentage: 50, weight: 0 },
          { year: "Year 4", active: false, credits: 120, semesters: 2, passPercentage: 50, weight: 0 },
        ],
      },
      // Next Config for detailed degree setup
      nextConfig: {
        numYears: 0,
        years: [],
      },
      isMobile: false,
    };
  },
  async mounted() {
    await this.checkLoginAndFetchConfig();
    this.darkMode = getDarkModePreference();
    if (this.darkMode) {
      document.body.classList.add("dark-mode");
    } else {
      document.body.classList.remove("dark-mode");
    }
    this.updateBackgroundGradient();
    this.checkMobile();
    window.addEventListener("resize", this.checkMobile);
  },
  beforeUnmount() {
    window.removeEventListener("resize", this.checkMobile);
    document.body.style.overflow = "";
  },
  methods: {
    async checkLoginAndFetchConfig() {
      try {
        // Fetch user configuration (basic preferences)
        const userConfigResponse = await axios.get(`${API_URL}/user/config`, { withCredentials: true });
        if (userConfigResponse.data) {
          this.userConfig = userConfigResponse.data;
        }
        if (!this.userConfig.academicLevel || !this.userConfig.enrollmentType) {
          this.showSetupWizard = true;
        } else {
          // Fetch calculator configuration
          const calcResponse = await axios.get(`${API_URL}/calculator`, { withCredentials: true });
          if (calcResponse.data && calcResponse.data.years) {
            this.calculatorConfig = calcResponse.data;
            // If detailed fields (semesters/passPercentage) are missing, show detailed config
            if (!this.calculatorConfig.years[0].semesters || !this.calculatorConfig.years[0].passPercentage) {
              this.showNextConfig = true;
              this.nextConfig.numYears = 0;
              this.nextConfig.years = [];
            }
          }
        }
      } catch (error) {
        console.error("Error fetching config:", error);
        if (error.response && error.response.status === 401) {
          this.notLoggedIn = true;
          this.$router.push("/login");
        }
      }
    },
    saveUserConfig() {
      axios
          .put(`${API_URL}/user/config`, this.userConfig, { withCredentials: true })
          .then(() => {
            notify({ type: "success", message: "Preferences saved successfully!" });
            this.showSetupWizard = false;
            // After basic preferences are saved, show detailed degree config
            this.showNextConfig = true;
          })
          .catch((error) => {
            console.error("Error saving user config:", error);
            notify({ type: "error", message: "Failed to save your preferences." });
          });
    },
    initNextConfig() {
      // When user enters the number of years, initialize the nextConfig.years array
      this.nextConfig.years = [];
      for (let i = 0; i < this.nextConfig.numYears; i++) {
        this.nextConfig.years.push({
          credits: 0,
          semesters: 2,
          passPercentage: 50,
          weight: 0,
        });
      }
    },
    saveYears() {
      // If detailed config is being set up, merge nextConfig into calculatorConfig
      if (this.showNextConfig) {
        this.calculatorConfig.years = this.nextConfig.years.map((config, index) => ({
          year: `Year ${index + 1}`,
          active: false,
          credits: config.credits,
          semesters: config.semesters,
          passPercentage: config.passPercentage,
          weight: config.weight,
        }));
      }
      axios
          .put(`${API_URL}/calculator`, this.calculatorConfig, { withCredentials: true })
          .then(() => {
            notify({ type: "success", message: "Calculator configuration saved successfully!" });
            this.showNextConfig = false;
          })
          .catch((error) => {
            console.error("Error saving calculator config:", error);
            notify({ type: "error", message: "Failed to save calculator configuration." });
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
    onPassPercentageChange(index) {
      if (this.calculatorConfig.years[index].passPercentage < 0) {
        this.calculatorConfig.years[index].passPercentage = 0;
      }
      if (this.calculatorConfig.years[index].passPercentage > 100) {
        this.calculatorConfig.years[index].passPercentage = 100;
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
    checkMobile() {
      this.isMobile = window.innerWidth <= 768;
    },
    updateBackgroundGradient() {
      const container = this.$refs.dashboardRef;
      if (container) {
        const gradient = this.darkMode
            ? `radial-gradient(circle at 50% 50%, #444, #000)`
            : `radial-gradient(circle at 50% 50%, #b191fc, #f2f2f2)`;
        container.style.background = gradient;
      }
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

/* Push content below NavBar */
.dashboard-content-wrapper {
  margin-top: 5rem;
}

/* Setup Wizard styles */
.setup-wizard,
.next-config {
  margin: 2rem auto;
  max-width: 600px;
  text-align: center;
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
.year-config {
  margin: 1rem 0;
  border: 1px solid #ddd;
  padding: 1rem;
  border-radius: 8px;
  text-align: left;
}
.year-config h3 {
  margin-bottom: 0.5rem;
}
.form-group {
  margin-bottom: 1rem;
}
.form-group label {
  display: block;
  margin-bottom: 0.25rem;
  font-weight: 600;
}
.form-group input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 1rem;
  margin-bottom: 1rem;
}
</style>
