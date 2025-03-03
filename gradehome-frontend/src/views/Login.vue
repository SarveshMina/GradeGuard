<template>
  <div class="auth-container" ref="authContainer">
    <!-- Use the improved NavBar component - pass the correct mode -->
    <NavBar :mode="formMode" :isMobile="isMobile" />

    <!-- Authentication content wrapper -->
    <div class="auth-content-wrapper">
      <!-- Left side branding panel (desktop only) -->
      <div v-if="!isMobile" class="brand-panel">
        <div class="brand-content">
          <div class="logo-container">
            <h1 class="brand-logo">GradeGuard</h1>
          </div>
          <div class="brand-tagline">
            <h2>Secure Your Academic Success</h2>
            <p>Track, analyze, and improve your grades with our powerful platform.</p>
          </div>
          <div class="brand-features">
            <div class="feature">
              <div class="feature-icon">
                <i class="fas fa-chart-line"></i>
              </div>
              <div class="feature-text">
                <h3>Track Progress</h3>
                <p>Monitor your academic journey in real-time</p>
              </div>
            </div>
            <div class="feature">
              <div class="feature-icon">
                <i class="fas fa-calculator"></i>
              </div>
              <div class="feature-text">
                <h3>Calculate GPA</h3>
                <p>Accurate grade calculations for your institution</p>
              </div>
            </div>
            <div class="feature">
              <div class="feature-icon">
                <i class="fas fa-graduation-cap"></i>
              </div>
              <div class="feature-text">
                <h3>Set Goals</h3>
                <p>Define and achieve your academic targets</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Mobile header (if applicable) -->
      <div v-if="isMobile" class="mobile-header">
        <div class="mobile-logo">GradeGuard</div>
      </div>

      <!-- Main form container -->
      <div class="form-container">
        <!-- Main form transition -->
        <transition name="slide-fade" mode="out-in">
          <!-- Login Form -->
          <div v-if="formMode === 'login'" key="login" class="auth-wrapper">
            <main class="auth-main">
              <h1 class="form-title">Welcome Back</h1>
              <p class="form-subtitle">
                Don't have an account?
                <a href="#" @click.prevent="switchToSignup" class="text-link">Sign up</a>
              </p>
              <form @submit.prevent="handleLogin" class="auth-form">
                <div class="form-group">
                  <label for="login-email">Email</label>
                  <div class="input-wrapper">
                    <i class="fas fa-envelope input-icon"></i>
                    <input type="email" v-model="loginEmail" id="login-email" placeholder="Enter your email" required />
                  </div>
                </div>
                <div class="form-group">
                  <label for="login-password">Password</label>
                  <div class="input-wrapper">
                    <i class="fas fa-lock input-icon"></i>
                    <input type="password" v-model="loginPassword" id="login-password" placeholder="Enter your password" required />
                  </div>
                </div>
                <div class="forgot-container">
                  <a href="#" @click.prevent="switchToForgot" class="forgot-link">Forgot your password?</a>
                </div>
                <button type="submit" class="auth-button">
                  <span>Login</span>
                  <i class="fas fa-arrow-right"></i>
                </button>
              </form>
              <div class="divider">
                <span>OR</span>
              </div>
              <div class="oauth-container">
                <button class="google-btn" @click="loginWithGoogle">
                  <img src="/assets/google-logo.png" alt="Google logo" class="google-logo" />
                  <span>Sign in with Google</span>
                </button>
              </div>
            </main>
          </div>

          <!-- Sign Up Form -->
          <div v-else-if="formMode === 'signup'" key="signup" class="auth-wrapper">
            <main class="auth-main">
              <h1 class="form-title">Create Account</h1>
              <p class="form-subtitle">
                Already have an account?
                <a href="#" @click.prevent="switchToLogin" class="text-link">Log in</a>
              </p>
              <form @submit.prevent="handleSignUp" class="auth-form">
                <transition name="slide-fade" mode="out-in">
                  <!-- Step 1: Email & Password -->
                  <div v-if="signUpStep === 1" key="signup-step1" class="signup-step">
                    <div class="step-indicator">
                      <div class="step active">1</div>
                      <div class="step-line"></div>
                      <div class="step">2</div>
                    </div>
                    <div class="form-group">
                      <label for="signup-email">Email</label>
                      <div class="input-wrapper">
                        <i class="fas fa-envelope input-icon"></i>
                        <input type="email" v-model="signUpEmail" id="signup-email" placeholder="you@example.com" required />
                      </div>
                    </div>
                    <div class="form-group">
                      <label for="signup-password">Password</label>
                      <div class="input-wrapper">
                        <i class="fas fa-lock input-icon"></i>
                        <input type="password" v-model="signUpPassword" id="signup-password" placeholder="••••••••••" required />
                      </div>
                    </div>
                    <div class="next-btn-container">
                      <button type="button" class="auth-button" @click="goToSignUpStep(2)">
                        <span>Continue</span>
                        <i class="fas fa-arrow-right"></i>
                      </button>
                    </div>
                  </div>

                  <!-- Step 2: Additional Info -->
                  <div v-else key="signup-step2" class="signup-step">
                    <div class="step-indicator">
                      <div class="step completed">1</div>
                      <div class="step-line completed"></div>
                      <div class="step active">2</div>
                    </div>
                    <div class="signup-back">
                      <a href="#" @click.prevent="goToSignUpStep(1)" class="back-link">
                        <i class="fas fa-chevron-left"></i> Back
                      </a>
                    </div>
                    <div class="form-group">
                      <label for="first-name">First Name</label>
                      <div class="input-wrapper">
                        <i class="fas fa-user input-icon"></i>
                        <input type="text" v-model="firstName" id="first-name" placeholder="Enter your first name" required />
                      </div>
                    </div>

                    <!-- University selection -->
                    <div class="form-group">
                      <label>University/College</label>
                      <div class="selector-wrapper" @click="openUniversityModal">
                        <i class="fas fa-university input-icon"></i>
                        <div class="university-selector">
                          <span v-if="selectedUniversityDoc">
                            {{ selectedUniversityDoc.name }} – {{ selectedUniversityDoc.counter }} students
                          </span>
                          <span v-else class="placeholder">Select your University/College</span>
                        </div>
                        <i class="fas fa-chevron-down selector-arrow"></i>
                      </div>
                    </div>

                    <!-- Degree (Major) selection -->
                    <div class="form-group">
                      <label>Degree</label>
                      <div class="selector-wrapper" @click="openMajorModal">
                        <i class="fas fa-graduation-cap input-icon"></i>
                        <div class="university-selector">
                          <span v-if="degree">{{ degree }}</span>
                          <span v-else class="placeholder">Select your Degree</span>
                        </div>
                        <i class="fas fa-chevron-down selector-arrow"></i>
                      </div>
                    </div>

                    <!-- Calculator type -->
                    <div class="form-group">
                      <label for="calc-type">Select Calculator Type</label>
                      <div class="selector-wrapper">
                        <i class="fas fa-calculator input-icon"></i>
                        <select v-model="calcType" id="calc-type" required>
                          <option value="UK Percentage">UK Percentage</option>
                          <option value="US GPA 5.0">US GPA 5.0</option>
                          <option value="US GPA 4.0">US GPA 4.0</option>
                        </select>
                        <i class="fas fa-chevron-down selector-arrow"></i>
                      </div>
                    </div>

                    <div class="signup-buttons">
                      <button type="submit" class="auth-button">
                        <span>Create Account</span>
                        <i class="fas fa-check"></i>
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
              <h1 class="form-title">Reset Password</h1>
              <p class="form-subtitle">Enter your email and we'll send you instructions to reset your password.</p>
              <form @submit.prevent="handleForgot" class="auth-form">
                <div class="form-group">
                  <label for="forgot-email">Email</label>
                  <div class="input-wrapper">
                    <i class="fas fa-envelope input-icon"></i>
                    <input type="email" v-model="forgotEmail" id="forgot-email" placeholder="Enter your email" required />
                  </div>
                </div>
                <button type="submit" class="auth-button">
                  <span>Send Reset Link</span>
                  <i class="fas fa-paper-plane"></i>
                </button>
                <p class="back-link-container">
                  <a href="#" @click.prevent="switchToLogin" class="back-link">
                    <i class="fas fa-chevron-left"></i> Back to login
                  </a>
                </p>
              </form>
            </main>
          </div>
        </transition>
      </div>
    </div>

    <!-- Footer (only on desktop) -->
    <Footer v-if="!isMobile" />

    <!-- University Selection Modal -->
    <transition name="modal">
      <div v-if="showUniversityModal" class="modal-overlay" @click.self="closeUniversityModal">
        <div class="modal-content">
          <div class="modal-header">
            <h2>Select Your University</h2>
            <button class="close-button" @click="closeUniversityModal">&times;</button>
          </div>
          <div class="search-container">
            <i class="fas fa-search search-icon"></i>
            <input type="text" v-model="universitySearch" placeholder="Search university..." class="search-input" />
          </div>
          <p v-if="universitySearch && universitySearch.trim().length < 3" class="helper-text">
            Please type at least 3 letters.
          </p>
          <div class="list-container">
            <ul class="university-list">
              <li v-for="(uniDoc, index) in universityDocs" :key="index" @click="selectUniversity(uniDoc)">
                <i class="fas fa-university list-icon"></i>
                <div class="uni-info">
                  <span class="uni-name">{{ uniDoc.name }}</span>
                  <span class="uni-count">{{ uniDoc.counter }} students</span>
                </div>
              </li>
            </ul>
            <!-- Load More Button with Loading Spinner -->
            <div v-if="canLoadMore" class="load-more-container">
              <button @click="loadMoreUniversities" class="load-more-btn">
                <span v-if="!isLoadingMore">Load More</span>
                <span v-else class="spinner"></span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </transition>

    <!-- Major (Degree) Selection Modal -->
    <transition name="modal">
      <div v-if="showMajorModal" class="modal-overlay" @click.self="closeMajorModal">
        <div class="modal-content">
          <div class="modal-header">
            <h2>Select Your Degree</h2>
            <button class="close-button" @click="closeMajorModal">&times;</button>
          </div>
          <div v-if="showCustomMajorInput">
            <div class="search-container">
              <i class="fas fa-graduation-cap search-icon"></i>
              <input type="text" v-model="customMajor" placeholder="Enter your degree" class="search-input" />
            </div>
            <div class="next-btn-container">
              <button type="button" class="auth-button" @click="saveCustomMajor">
                <span>Save Degree</span>
                <i class="fas fa-check"></i>
              </button>
            </div>
          </div>
          <div v-else>
            <div class="search-container">
              <i class="fas fa-search search-icon"></i>
              <input type="text" v-model="majorSearch" placeholder="Search degree..." class="search-input" />
            </div>
            <div class="list-container">
              <ul class="university-list">
                <li v-for="(majorObj, index) in filteredMajors" :key="index" @click="selectMajor(majorObj.major_name)">
                  <i class="fas fa-graduation-cap list-icon"></i>
                  <div class="uni-info">
                    <span class="uni-name">{{ majorObj.major_name }}</span>
                    <span class="uni-count">{{ majorObj.counter }} students</span>
                  </div>
                </li>
                <li class="custom-option" @click="enableCustomMajor">
                  <i class="fas fa-plus-circle"></i>
                  <span>Not Listed? Click to add custom degree</span>
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
import axios from 'axios'
import { notify } from '@/services/toastService.js'
import NavBar from '@/components/NavBar.vue'
import Footer from '@/components/Footer.vue'
import { getDarkModePreference } from '@/services/darkModeService.js'
import { API_URL } from '/src/config.js'


export default {
  name: 'Login',
  components: { NavBar, Footer },
  data() {
    return {
      darkMode: false,
      isMobile: false,
      formMode: 'login',
      signUpStep: 1,
      loginEmail: '',
      loginPassword: '',
      signUpEmail: '',
      signUpPassword: '',
      firstName: '',
      calcType: 'UK Percentage',
      degree: '',
      universityDocs: [],
      selectedUniversityDoc: null,
      universitySearch: '',
      showUniversityModal: false,
      searchTimeout: null,
      searchOffset: 0,
      searchLimit: 10,
      lastFetchedCount: 0,
      isLoadingMore: false,
      majorSearch: '',
      showMajorModal: false,
      showCustomMajorInput: false,
      customMajor: '',
      forgotEmail: ''
    }
  },
  computed: {
    filteredMajors() {
      if (!this.selectedUniversityDoc) return []
      const term = this.majorSearch.toLowerCase()
      return this.selectedUniversityDoc.majors.filter(m =>
          m.major_name.toLowerCase().includes(term)
      )
    },
    canLoadMore() {
      return this.universitySearch.trim().length >= 3 && this.lastFetchedCount === this.searchLimit
    }
  },
  mounted() {
    // Initialize dark mode from the service
    this.darkMode = getDarkModePreference();

    // Listen for dark mode changes from other components
    window.addEventListener('darkModeChange', (event) => {
      this.darkMode = event.detail.isDark;
    });

    // Check for mobile view
    this.checkMobile();
    window.addEventListener('resize', this.checkMobile);

    // Set background gradient
    this.setBackgroundGradient();

    // Check for mode in URL query params
    const mode = this.$route.query.mode;
    if (mode === 'signup') {
      this.formMode = 'signup';
      this.signUpStep = 1;
    } else {
      this.formMode = 'login';
    }
  },
  beforeUnmount() {
    window.removeEventListener('resize', this.checkMobile);
    window.removeEventListener('darkModeChange', this.onDarkModeChange);
    document.body.style.overflow = '';
  },
  methods: {
    checkMobile() {
      this.isMobile = window.innerWidth <= 768;
    },
    setBackgroundGradient() {
      const container = this.$refs.authContainer;
      if (container) {
        container.style.background = 'var(--bg-gradient)';
      }
    },
    openUniversityModal() {
      console.log("openUniversityModal triggered")
      this.showUniversityModal = true;
      this.universitySearch = '';
      this.universityDocs = [];
      this.searchOffset = 0;
      this.searchLimit = 10;
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
        notify({ type: 'warning', message: 'Please select a university first.' });
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
        notify({ type: 'warning', message: 'Please enter your degree.' });
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
        }
        const response = await axios.post(`${API_URL}/register`, payload, {
          withCredentials: true
        })
        notify({ type: 'success', message: 'Sign up successful: ' + response.data.message })
        if (this.selectedUniversityDoc) {
          const updatedResponse = await axios.get(`${API_URL}/stats/university`, {
            params: { name: this.selectedUniversityDoc.name }
          })
          this.selectedUniversityDoc = updatedResponse.data
        }
        // Redirect to dashboard after successful signup
        this.$router.push('/dashboard');
      } catch (error) {
        console.error(error)
        const errMsg = error.response?.data?.error || error.message
        notify({ type: 'error', message: 'Sign up failed: ' + errMsg })
      }
    },
    async handleLogin() {
      try {
        await axios.post(`${API_URL}/login`, {
          email: this.loginEmail,
          password: this.loginPassword,
        }, {
          withCredentials: true
        })
        notify({ type: 'success', message: 'Login successful.' })
        this.$router.push('/dashboard')
      } catch (error) {
        notify({ type: 'error', message: 'Login failed: ' + (error.response?.data?.error || error.message) })
      }
    },
    async handleForgot() {
      // In a real application, call the API to request a password reset
      try {
        await axios.post(`${API_URL}/forgot-password`, {
          email: this.forgotEmail
        });
        notify({ type: 'success', message: 'Password reset instructions sent to ' + this.forgotEmail });
        this.switchToLogin();
      } catch (error) {
        notify({ type: 'error', message: 'Password reset request failed: ' + (error.response?.data?.error || error.message) });
      }
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
      this.$router.push({ path: '/login', query: { mode: 'forgot' } });
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
            offset: this.searchOffset
          }
        })
        const results = response.data;
        this.lastFetchedCount = results.length;
        if (loadMore) {
          const newResults = results.filter(u => !this.universityDocs.some(existing => existing.id === u.id));
          this.universityDocs = this.universityDocs.concat(newResults);
          this.searchOffset += newResults.length;
          this.isLoadingMore = false;
        } else {
          this.universityDocs = results;
          this.searchOffset = results.length;
        }
      } catch (err) {
        console.error('Error searching universities:', err);
        this.isLoadingMore = false;
      }
    },
    loadMoreUniversities() {
      this.searchUniversities(this.universitySearch, true);
    }
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
    '$route.query.mode'(newMode) {
      if (newMode === 'signup') {
        this.formMode = 'signup';
        this.signUpStep = 1;
      } else if (newMode === 'forgot') {
        this.formMode = 'forgot';
      } else {
        this.formMode = 'login';
      }
    }
  }
}
</script>

<style scoped>
/* Base Styles */
.auth-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background: var(--bg-gradient);
  color: var(--text-primary);
  font-family: "Montserrat", sans-serif;
  transition: all var(--transition-speed) ease;
}

/* Two-panel layout */
.auth-content-wrapper {
  display: flex;
  flex: 1;
  position: relative;
}

/* Branding panel (left side) */
.brand-panel {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-dark) 100%);
  color: white;
  width: 40%;
  padding: 2rem;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  position: relative;
  overflow: hidden;
}

.brand-panel::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('/assets/pattern.svg') center/cover;
  opacity: 0.07;
  pointer-events: none;
}

.brand-content {
  position: relative;
  z-index: 1;
  max-width: 400px;
}

.logo-container {
  margin-bottom: 3rem;
  text-align: center;
}

.brand-logo {
  font-size: 3rem;
  font-weight: 700;
  margin: 0;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
}

.brand-tagline {
  margin-bottom: 3rem;
  text-align: center;
}

.brand-tagline h2 {
  font-size: 1.8rem;
  margin-bottom: 1rem;
  font-weight: 600;
}

.brand-tagline p {
  font-size: 1.1rem;
  opacity: 0.9;
  line-height: 1.6;
}

.brand-features {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.feature {
  display: flex;
  align-items: center;
  gap: 1rem;
  background: rgba(255, 255, 255, 0.1);
  padding: 1rem;
  border-radius: 12px;
  backdrop-filter: blur(5px);
  transition: transform 0.3s ease, background 0.3s ease;
}

.feature:hover {
  transform: translateY(-5px);
  background: rgba(255, 255, 255, 0.15);
}

.feature-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.2);
  font-size: 1.5rem;
}

.feature-text h3 {
  font-size: 1.1rem;
  margin: 0 0 0.25rem;
  font-weight: 600;
}

.feature-text p {
  font-size: 0.9rem;
  margin: 0;
  opacity: 0.8;
}

/* Mobile header */
.mobile-header {
  background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-dark) 100%);
  padding: 1.5rem;
  text-align: center;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.mobile-logo {
  font-size: 2.2rem;
  font-weight: 700;
  color: white;
  text-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

/* Form container (right side) */
.form-container {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  background-color: var(--bg-body);
}

.auth-wrapper {
  width: 100%;
  max-width: 420px;
  animation: fadeInUp 0.5s ease;
}

/* Form styling */
.auth-main {
  background: var(--bg-card);
  padding: 2.5rem;
  border-radius: 16px;
  box-shadow: var(--shadow-lg);
  width: 100%;
  color: var(--text-primary);
  transition: all var(--transition-speed) ease;
  position: relative;
  overflow: hidden;
}

.auth-main::before {
  content: "";
  position: absolute;
  top: 0;
  right: 0;
  width: 100px;
  height: 100px;
  background: linear-gradient(135deg, var(--primary-color-transparent) 0%, transparent 70%);
  border-radius: 0 16px 0 100%;
  opacity: 0.5;
}

.form-title {
  font-size: 1.8rem;
  font-weight: 700;
  margin-bottom: 1rem;
  text-align: center;
  color: var(--text-primary);
  position: relative;
}

.form-title::after {
  content: "";
  display: block;
  width: 40px;
  height: 4px;
  background: var(--primary-color);
  margin: 0.5rem auto 0;
  border-radius: 2px;
}

.form-subtitle {
  text-align: center;
  font-size: 0.95rem;
  margin-bottom: 2rem;
  color: var(--text-secondary);
}

.text-link {
  color: var(--primary-color);
  text-decoration: none;
  font-weight: 600;
  transition: color var(--transition-speed) ease;
}

.text-link:hover {
  color: var(--primary-dark);
  text-decoration: underline;
}

.auth-form {
  margin-bottom: 1rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--text-secondary);
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.input-icon {
  position: absolute;
  left: 1rem;
  font-size: 0.9rem;
  color: var(--text-muted);
  transition: all 0.3s ease;
}

.input-wrapper input:focus + .input-icon,
.selector-wrapper:hover .input-icon {
  color: var(--primary-color);
}

.input-wrapper input,
.form-group select {
  width: 100%;
  padding: 0.9rem 1rem 0.9rem 2.8rem;
  border: 1px solid var(--border-color);
  border-radius: 12px;
  font-size: 1rem;
  color: var(--text-primary);
  background: var(--bg-input);
  box-sizing: border-box;
  transition: all 0.3s ease;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.input-wrapper input:focus,
.form-group select:focus {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px var(--primary-color-transparent);
  outline: none;
}

.selector-wrapper {
  position: relative;
  cursor: pointer;
  display: flex;
  align-items: center;
}

.selector-arrow {
  position: absolute;
  right: 1rem;
  font-size: 0.8rem;
  color: var(--text-muted);
  transition: transform 0.3s ease;
  pointer-events: none;
}

.selector-wrapper:hover .selector-arrow {
  transform: translateY(2px);
  color: var(--primary-color);
}

.university-selector {
  flex: 1;
  padding: 0.9rem 1rem 0.9rem 2.8rem;
  border: 1px solid var(--border-color);
  border-radius: 12px;
  cursor: pointer;
  background: var(--bg-input);
  color: var(--text-primary);
  transition: all 0.3s ease;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.selector-wrapper:hover .university-selector {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px var(--primary-color-transparent);
}

.university-selector .placeholder {
  color: var(--text-muted);
}

.forgot-container {
  text-align: right;
  margin-bottom: 1.5rem;
}

.forgot-link {
  font-size: 0.85rem;
  color: var(--primary-color);
  text-decoration: none;
  position: relative;
  transition: all 0.3s ease;
  font-weight: 500;
}

.forgot-link:hover {
  color: var(--primary-dark);
  text-decoration: underline;
}

.auth-button {
  width: 100%;
  padding: 0.9rem 1.5rem;
  border: none;
  border-radius: 12px;
  background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-dark) 100%);
  color: white;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 0.5rem;
  box-shadow: 0 4px 12px var(--primary-color-transparent);
}

.auth-button i {
  font-size: 0.9rem;
  transition: transform 0.3s ease;
}

.auth-button:hover {
  box-shadow: 0 6px 18px var(--primary-color-transparent);
  transform: translateY(-2px);
}

.auth-button:hover i {
  transform: translateX(3px);
}

.auth-button:active {
  transform: translateY(0);
  box-shadow: 0 2px 8px var(--primary-color-transparent);
}

/* Divider */
.divider {
  display: flex;
  align-items: center;
  margin: 1.5rem 0;
  color: var(--text-muted);
  font-size: 0.85rem;
}

.divider::before,
.divider::after {
  content: "";
  flex: 1;
  height: 1px;
  background: var(--border-color);
}

.divider span {
  padding: 0 1rem;
  text-transform: uppercase;
  font-weight: 600;
  letter-spacing: 1px;
}

/* OAuth button */
.oauth-container {
  margin-top: 1.5rem;
}

.google-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  width: 100%;
  padding: 0.9rem 1.5rem;
  border: 1px solid var(--border-color);
  border-radius: 12px;
  background: var(--bg-card);
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
  cursor: pointer;
  transition: all 0.3s ease;
  color: var(--text-primary);
  font-weight: 500;
}

.google-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  border-color: var(--primary-color);
}

.google-logo {
  width: 20px;
  height: 20px;
}

/* Step indicator for signup */
.step-indicator {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1.5rem;
}

.step {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background: var(--bg-muted);
  color: var(--text-muted);
  font-weight: 600;
  font-size: 0.8rem;
}

.step.active {
  background: var(--primary-color);
  color: white;
  box-shadow: 0 0 0 3px var(--primary-color-transparent);
}

.step.completed {
  background: var(--success-color);
  color: white;
}

.step-line {
  flex: 1;
  height: 2px;
  background: var(--border-color);
  margin: 0 10px;
}

.step-line.completed {
  background: var(--success-color);
}

.signup-back {
  margin-bottom: 1.5rem;
}

.back-link {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  color: var(--text-secondary);
  text-decoration: none;
  font-size: 0.9rem;
  transition: color 0.3s ease;
}

.back-link:hover {
  color: var(--primary-color);
}

.back-link i {
  font-size: 0.7rem;
}

.back-link-container {
  text-align: center;
  margin-top: 1.5rem;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(5px);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2000;
  padding: 1rem;
  overflow: hidden;
}

.modal-content {
  background: var(--bg-card);
  border: none;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  border-radius: 16px;
  padding: 1.5rem;
  width: 100%;
  max-width: 400px;
  overflow: hidden;
  transition: all 0.3s ease;
  position: relative;
  box-sizing: border-box;
  max-height: 70vh;
  color: var(--text-primary);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--border-color);
}

.modal-header h2 {
  margin: 0;
  font-size: 1.25rem;
  color: var(--text-primary);
}

.close-button {
  background: var(--bg-muted);
  border: none;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  cursor: pointer;
  color: var(--text-primary);
  transition: all 0.2s ease;
}

.close-button:hover {
  background: var(--bg-hover);
  transform: rotate(90deg);
}

.search-container {
  position: relative;
  margin-bottom: 1rem;
}

.search-icon {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-muted);
}

.search-input {
  width: 100%;
  padding: 0.9rem 1rem 0.9rem 2.8rem;
  border: 1px solid var(--border-color);
  border-radius: 12px;
  background: var(--bg-input);
  color: var(--text-primary);
  transition: all 0.3s ease;
}

.search-input:focus {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px var(--primary-color-transparent);
  outline: none;
}

.list-container {
  max-height: 40vh;
  overflow-y: auto;
  margin-top: 1rem;
  padding-right: 0.5rem;
  scrollbar-width: thin;
  scrollbar-color: var(--border-color) transparent;
}

.list-container::-webkit-scrollbar {
  width: 6px;
}

.list-container::-webkit-scrollbar-track {
  background: transparent;
}

.list-container::-webkit-scrollbar-thumb {
  background-color: var(--border-color);
  border-radius: 6px;
}

.helper-text {
  font-size: 0.85rem;
  color: var(--text-muted);
  margin-top: -0.5rem;
  margin-bottom: 0.5rem;
}

.university-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.university-list li {
  padding: 0.75rem 1rem;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
  color: var(--text-primary);
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 0.5rem;
}

.university-list li:hover {
  background: var(--bg-hover);
  transform: translateX(5px);
}

.list-icon {
  font-size: 1rem;
  color: var(--primary-color);
  opacity: 0.8;
}

.uni-info {
  display: flex;
  flex-direction: column;
}

.uni-name {
  font-weight: 500;
}

.uni-count {
  font-size: 0.8rem;
  color: var(--text-muted);
}

.custom-option {
  color: var(--primary-color) !important;
  font-weight: 500;
}

.load-more-container {
  text-align: center;
  margin-top: 1rem;
  margin-bottom: 0.5rem;
}

.load-more-btn {
  background: var(--bg-muted);
  color: var(--text-primary);
  border: none;
  border-radius: 12px;
  padding: 0.6rem 1.2rem;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.load-more-btn:hover {
  background: var(--bg-hover);
}

.spinner {
  display: inline-block;
  width: 20px;
  height: 20px;
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Transitions */
.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: all 0.3s ease;
}

.slide-fade-enter-from {
  opacity: 0;
  transform: translateY(20px);
}

.slide-fade-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}

.modal-enter-active,
.modal-leave-active {
  transition: all 0.3s ease;
}

.modal-enter-from {
  opacity: 0;
  transform: scale(0.9);
}

.modal-leave-to {
  opacity: 0;
  transform: scale(0.9);
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Responsive styles */
@media (max-width: 1024px) {
  .brand-panel {
    padding: 1.5rem;
  }

  .form-container {
    padding: 1.5rem;
  }
}

@media (max-width: 768px) {
  .brand-panel {
    display: none;
  }

  .auth-content-wrapper {
    padding-top: 0;
  }

  .form-container {
    padding: 1rem;
  }

  .auth-main {
    padding: 1.5rem;
    border-radius: 12px;
  }

  .form-title {
    font-size: 1.5rem;
  }

  .auth-button,
  .input-wrapper input,
  .university-selector {
    padding: 0.75rem 1rem 0.75rem 2.6rem;
  }
}
</style>