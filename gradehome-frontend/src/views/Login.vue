<template>
  <div class="auth-container" ref="authContainer">
    <!-- Example NavBar (optional) -->
    <NavBar v-if="!isMobile" :mode="formMode" />

    <!-- Mobile header -->
    <div v-if="isMobile" class="mobile-header">
      <div class="mobile-logo">GradeHome</div>
    </div>

    <!-- Dark mode toggle -->
    <div class="dark-mode-toggle-container">
      <button @click="toggleDarkMode" class="nav-button dark-mode-toggle">
        <i v-if="!darkMode" class="fas fa-moon"></i>
        <i v-else class="fas fa-sun"></i>
      </button>
    </div>

    <!-- Main form transition -->
    <transition name="fade" mode="out-in">
      <!-- Login Form -->
      <div v-if="formMode === 'login'" key="login" class="auth-wrapper">
        <main class="auth-main">
          <h1>Login</h1>
          <p>
            Don’t have an account?
            <a href="#" @click.prevent="switchToSignup">Sign up</a>
          </p>
          <form @submit.prevent="handleLogin">
            <div class="form-group">
              <label for="login-email">Email</label>
              <input
                  type="email"
                  v-model="loginEmail"
                  id="login-email"
                  placeholder="Enter your email"
                  required
              />
            </div>
            <div class="form-group">
              <label for="login-password">Password</label>
              <input
                  type="password"
                  v-model="loginPassword"
                  id="login-password"
                  placeholder="Enter your password"
                  required
              />
            </div>
            <div class="forgot-container">
              <a href="#" @click.prevent="switchToForgot" class="forgot-link">
                Forgot your password?
              </a>
            </div>
            <button type="submit" class="auth-button">Login</button>
          </form>
        </main>
      </div>

      <!-- Sign Up Form -->
      <div v-else-if="formMode === 'signup'" key="signup" class="auth-wrapper">
        <main class="auth-main">
          <h1>Create Account</h1>
          <p>
            Already have an account?
            <a href="#" @click.prevent="switchToLogin">Log in</a>
          </p>
          <form @submit.prevent="handleSignUp">
            <transition name="fade" mode="out-in">
              <!-- Step 1: Email & Password -->
              <div v-if="signUpStep === 1" key="signup-step1" class="signup-step">
                <div class="form-group">
                  <label for="signup-email">Email</label>
                  <input
                      type="email"
                      v-model="signUpEmail"
                      id="signup-email"
                      placeholder="you@example.com"
                      required
                  />
                </div>
                <div class="form-group">
                  <label for="signup-password">Password</label>
                  <input
                      type="password"
                      v-model="signUpPassword"
                      id="signup-password"
                      placeholder="••••••••••"
                      required
                  />
                </div>
                <div class="next-btn-container">
                  <button type="button" class="small-btn next-btn" @click="goToSignUpStep(2)">
                    Next <i class="fas fa-arrow-right"></i>
                  </button>
                </div>
              </div>

              <!-- Step 2: Additional Info -->
              <div v-else key="signup-step2" class="signup-step">
                <div class="signup-back">
                  <a href="#" @click.prevent="goToSignUpStep(1)">Back</a>
                </div>
                <div class="form-group">
                  <label for="first-name">First Name</label>
                  <input
                      type="text"
                      v-model="firstName"
                      id="first-name"
                      placeholder="Enter your first name"
                      required
                  />
                </div>

                <!-- University selection -->
                <div class="form-group">
                  <label>University/College</label>
                  <div class="university-selector" @click="openUniversityModal">
                    <span v-if="selectedUniversityDoc">
                      {{ selectedUniversityDoc.name }} – {{ selectedUniversityDoc.counter }} students
                    </span>
                    <span v-else class="placeholder">Select your University/College</span>
                  </div>
                </div>

                <!-- Degree (Major) selection -->
                <div class="form-group">
                  <label>Degree</label>
                  <div class="university-selector" @click="openMajorModal">
                    <span v-if="degree">{{ degree }}</span>
                    <span v-else class="placeholder">Select your Degree</span>
                  </div>
                </div>

                <!-- Calculator type -->
                <div class="form-group">
                  <label for="calc-type">Select Calculator Type</label>
                  <select v-model="calcType" id="calc-type" required>
                    <option value="UK Percentage">UK Percentage</option>
                    <option value="US GPA 5.0">US GPA 5.0</option>
                    <option value="US GPA 4.0">US GPA 4.0</option>
                  </select>
                </div>

                <div class="signup-buttons">
                  <button type="submit" class="small-btn create-account-btn">
                    Create Account
                  </button>
                </div>
              </div>
            </transition>
          </form>
        </main>
      </div>

      <!-- Forgot Password Form -->
      <div v-else-if="formMode === 'forgot'" key="forgot" class="auth-wrapper">
        <main class="auth-main">
          <h1>Forgot Password</h1>
          <p>
            Enter your email and we'll send you instructions to reset your password.
          </p>
          <form @submit.prevent="handleForgot">
            <div class="form-group">
              <label for="forgot-email">Email</label>
              <input
                  type="email"
                  v-model="forgotEmail"
                  id="forgot-email"
                  placeholder="Enter your email"
                  required
              />
            </div>
            <button type="submit" class="auth-button">Reset Password</button>
            <p class="back-link">
              Remembered? <a href="#" @click.prevent="switchToLogin">Log in</a>
            </p>
          </form>
        </main>
      </div>
    </transition>

    <!-- Footer (optional) -->
    <Footer v-if="!isMobile" />

    <!-- University Selection Modal -->
    <transition name="modal">
      <div v-if="showUniversityModal" class="modal-overlay" @click.self="closeUniversityModal">
        <div class="modal-content">
          <h2>Select Your University</h2>
          <input
              type="text"
              v-model="universitySearch"
              placeholder="Search university..."
              class="search-input"
          />
          <!-- Only the list is scrollable -->
          <div class="list-container">
            <ul class="university-list">
              <li
                  v-for="(uniDoc, index) in filteredUniversities"
                  :key="index"
                  @click="selectUniversity(uniDoc)"
              >
                {{ uniDoc.name }} – {{ uniDoc.counter }} students
              </li>
            </ul>
          </div>
        </div>
      </div>
    </transition>

    <!-- Major (Degree) Selection Modal -->
    <transition name="modal">
      <div v-if="showMajorModal" class="modal-overlay" @click.self="closeMajorModal">
        <div class="modal-content">
          <h2>Select Your Degree</h2>
          <!-- If user wants to add a custom degree, show an input field -->
          <div v-if="showCustomMajorInput">
            <input
                type="text"
                v-model="customMajor"
                placeholder="Enter your degree"
                class="search-input"
            />
            <div class="next-btn-container">
              <button type="button" class="small-btn next-btn" @click="saveCustomMajor">
                Save
              </button>
            </div>
          </div>
          <!-- Otherwise, show the search and list of majors with counters -->
          <div v-else>
            <input
                type="text"
                v-model="majorSearch"
                placeholder="Search degree..."
                class="search-input"
            />
            <!-- Only the list is scrollable -->
            <div class="list-container">
              <ul class="university-list">
                <li
                    v-for="(majorObj, index) in filteredMajors"
                    :key="index"
                    @click="selectMajor(majorObj.major_name)"
                >
                  {{ majorObj.major_name }} – {{ majorObj.counter }} students
                </li>
                <li class="custom-option" @click="enableCustomMajor">
                  Not Listed? Click to add custom degree
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
import axios from 'axios';
import NavBar from '@/components/NavBar.vue';
import Footer from '@/components/Footer.vue';

const API_URL = 'http://localhost:7071/api'; // Your Azure Functions backend

export default {
  name: 'Login',
  components: { NavBar, Footer },
  data() {
    return {
      // Basic UI state
      isMobile: false,
      darkMode: false,
      formMode: 'login',
      signUpStep: 1,

      // Login fields
      loginEmail: '',
      loginPassword: '',

      // Sign-up fields
      signUpEmail: '',
      signUpPassword: '',
      firstName: '',
      calcType: 'UK Percentage',
      degree: '',

      // University data
      universityDocs: [],
      selectedUniversityDoc: null,
      universitySearch: '',
      showUniversityModal: false,

      // Major data
      majorSearch: '',
      showMajorModal: false,
      showCustomMajorInput: false,
      customMajor: '',

      // Forgot Password
      forgotEmail: ''
    };
  },
  computed: {
    filteredUniversities() {
      const term = this.universitySearch.toLowerCase();
      return this.universityDocs.filter(doc =>
          doc.name.toLowerCase().includes(term)
      );
    },
    filteredMajors() {
      if (!this.selectedUniversityDoc) return [];
      const term = this.majorSearch.toLowerCase();
      return this.selectedUniversityDoc.majors.filter(m =>
          m.major_name.toLowerCase().includes(term)
      );
    }
  },
  mounted() {
    this.checkMobile();
    window.addEventListener('resize', this.checkMobile);
    this.setBackgroundGradient();
    this.fetchAllUniversities();
  },
  beforeUnmount() {
    window.removeEventListener('resize', this.checkMobile);
    document.body.style.overflow = '';
  },
  methods: {
    checkMobile() {
      this.isMobile = window.innerWidth <= 768;
    },
    setBackgroundGradient() {
      const container = this.$refs.authContainer;
      if (container) {
        container.style.background = 'linear-gradient(160deg, #B191FC, #ffffff)';
      }
    },
    toggleDarkMode() {
      this.darkMode = !this.darkMode;
      document.body.classList.toggle('dark-mode', this.darkMode);
    },
    async fetchAllUniversities() {
      try {
        const response = await axios.get(`${API_URL}/stats/universities`);
        this.universityDocs = response.data;
      } catch (err) {
        console.error('Error fetching universities:', err);
      }
    },
    openUniversityModal() {
      this.showUniversityModal = true;
      this.universitySearch = '';
      document.body.style.overflow = 'hidden';
    },
    closeUniversityModal() {
      this.showUniversityModal = false;
      document.body.style.overflow = '';
    },
    selectUniversity(uniDoc) {
      this.selectedUniversityDoc = uniDoc;
      this.closeUniversityModal();
    },
    openMajorModal() {
      if (!this.selectedUniversityDoc) {
        alert("Please select a university first.");
        return;
      }
      this.showMajorModal = true;
      this.majorSearch = '';
      this.showCustomMajorInput = false;
      this.customMajor = '';
      document.body.style.overflow = 'hidden';
    },
    closeMajorModal() {
      this.showMajorModal = false;
      this.showCustomMajorInput = false;
      document.body.style.overflow = '';
    },
    selectMajor(majorName) {
      this.degree = majorName;
      this.closeMajorModal();
    },
    enableCustomMajor() {
      this.showCustomMajorInput = true;
      this.customMajor = '';
    },
    saveCustomMajor() {
      if (this.customMajor.trim() !== '') {
        this.degree = this.customMajor.trim();
        this.closeMajorModal();
      } else {
        alert('Please enter your degree.');
      }
    },
    goToSignUpStep(step) {
      this.signUpStep = step;
    },
    async handleSignUp() {
      try {
        const payload = {
          firstName: this.firstName,
          email: this.signUpEmail,
          password: this.signUpPassword,
          university: this.selectedUniversityDoc ? this.selectedUniversityDoc.name : '',
          degree: this.degree,
          calcType: this.calcType
        };
        const response = await axios.post(`${API_URL}/register`, payload);
        alert("Sign up successful: " + response.data.message);

        // Fetch updated counters
        if (this.selectedUniversityDoc) {
          const updatedResponse = await axios.get(`${API_URL}/stats/university`, {
            params: { name: this.selectedUniversityDoc.name }
          });
          this.selectedUniversityDoc = updatedResponse.data;
        }
      } catch (error) {
        console.error(error);
        const errMsg = error.response?.data?.error || error.message;
        alert("Sign up failed: " + errMsg);
      }
    },
    async handleLogin() {
      try {
        const response = await axios.post(`${API_URL}/login`, {
          email: this.loginEmail,
          password: this.loginPassword,
        });
        alert("Login successful: " + response.data.message);
      } catch (error) {
        alert("Login failed: " + (error.response?.data?.error || error.message));
      }
    },
    async handleForgot() {
      // Example only
      alert("Forgot password request sent for " + this.forgotEmail);
    },
    switchToSignup() {
      this.formMode = 'signup';
      this.signUpStep = 1;
      this.$router.push({ path: '/login', query: { mode: 'signup' } });
    },
    switchToLogin() {
      this.formMode = 'login';
      this.$router.push({ path: '/login', query: { mode: 'login' } });
    },
    switchToForgot() {
      this.formMode = 'forgot';
    },
  },
  watch: {
    '$route.query.mode': {
      handler(newMode) {
        if (newMode === 'signup') {
          this.formMode = 'signup';
          this.signUpStep = 1;
        } else {
          this.formMode = 'login';
        }
      },
      immediate: true,
    },
  },
};
</script>

<style scoped>
.auth-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background: linear-gradient(160deg, #B191FC, #ffffff);
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

.nav-button {
  margin: 0 0.5rem;
  padding: 0.8rem 1.2rem;
  border: 2px solid #000;
  background: transparent;
  color: #000;
  border-radius: 24px;
  cursor: pointer;
  transition: 0.3s;
  font-weight: 600;
  text-decoration: none;
  box-shadow: 0 0 8px rgba(0,0,0,0.2);
}

.nav-button:hover {
  background: #000;
  color: #fff;
  transform: translateY(-2px);
  box-shadow: 0 0 12px rgba(0,0,0,0.4);
}

.auth-wrapper {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 3rem;
}

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

.form-group {
  margin-bottom: 1.25rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
  color: #555;
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

/* Glassmorphism Modal Styles */
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
  /* No scrolling on the overlay itself */
  padding: 1rem;
  overflow: hidden;
}

.modal-content {
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid rgba(0, 0, 0, 0.1);
  box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
  border-radius: 16px;
  padding: 1.5rem;
  width: 100%;
  max-width: 400px;
  /* We remove vertical scroll from the entire modal content */
  overflow: hidden; /* or remove altogether if you want a fallback */
  transition: transform 0.3s ease;
  position: relative;
  box-sizing: border-box;
  max-height: 70vh;
}

/* The scrollable container for the lists */
.list-container {
  max-height: 40vh; /* Adjust as needed */
  overflow-y: auto;
  margin-top: 1rem; /* Spacing above the list */
  /* optional border-top or spacing for separation:
     border-top: 1px solid #eee;
     padding-top: 1rem;
  */
}

/* Scrollbar Styling for .list-container */
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

/* Modal scale-in animation */
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
}

/* Light mode hover: white background, black text */
.university-list li:hover {
  background: #f0f0f0;
  color: #000;
}

.university-list li.custom-option {
  font-style: italic;
  color: var(--link-color);
}

/* Dark Mode Adjustments */
.dark-mode .auth-main {
  --link-color: #B191FC;
  background: #2b2b2b;
  color: #fff;
}

.dark-mode .auth-main h1 {
  color: #fff;
}

.dark-mode .auth-main p {
  color: #fff;
}

.dark-mode .form-group label {
  color: #fff;
}

.dark-mode .form-group input,
.dark-mode .form-group select {
  background: #444;
  color: #fff;
  border: 1px solid #555;
}

.dark-mode .form-group input:focus,
.dark-mode .form-group select:focus {
  border-color: var(--link-color);
  outline: none;
}

.dark-mode .forgot-link,
.dark-mode .auth-main p a {
  color: var(--link-color);
}

.dark-mode .university-selector {
  background: #444;
  border: 1px solid #555;
  color: #fff;
}

.dark-mode .university-selector .placeholder {
  color: #bbb;
}

/* Dark mode modal background */
.dark-mode .modal-content {
  background: rgba(0, 0, 0, 0.7);
  border: 1px solid rgba(255, 255, 255, 0.2);
  overflow: hidden; /* keep consistent with normal mode */
}

/* Dark mode hover: darker background, white text */
.dark-mode .university-list li:hover {
  background: #444;
  color: #fff;
}

/* Dark mode .list-container scrollbar styling */
.dark-mode .list-container::-webkit-scrollbar-thumb {
  background-color: #B191FC;
}
</style>
