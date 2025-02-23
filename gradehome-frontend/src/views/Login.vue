<template>
  <div class="auth-container" ref="authContainer">
    <!-- NavBar with isMobile passed from Login -->
    <NavBar :mode="formMode" :isMobile="isMobile" />

    <!-- Mobile header (if applicable) -->
    <div v-if="isMobile" class="mobile-header">
      <div class="mobile-logo">GradeHome</div>
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
              <input type="email" v-model="loginEmail" id="login-email" placeholder="Enter your email" required />
            </div>
            <div class="form-group">
              <label for="login-password">Password</label>
              <input type="password" v-model="loginPassword" id="login-password" placeholder="Enter your password" required />
            </div>
            <div class="forgot-container">
              <a href="#" @click.prevent="switchToForgot" class="forgot-link">Forgot your password?</a>
            </div>
            <button type="submit" class="auth-button">Login</button>
          </form>
          <div class="oauth-container">
            <button class="google-btn" @click="loginWithGoogle">
              <img src="/assets/google-logo.png" alt="Google logo" class="google-logo" />
              Sign in with Google
            </button>
          </div>
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
                  <input type="email" v-model="signUpEmail" id="signup-email" placeholder="you@example.com" required />
                </div>
                <div class="form-group">
                  <label for="signup-password">Password</label>
                  <input type="password" v-model="signUpPassword" id="signup-password" placeholder="••••••••••" required />
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
                  <input type="text" v-model="firstName" id="first-name" placeholder="Enter your first name" required />
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
                  <button type="submit" class="small-btn create-account-btn">Create Account</button>
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
          <p>Enter your email and we'll send you instructions to reset your password.</p>
          <form @submit.prevent="handleForgot">
            <div class="form-group">
              <label for="forgot-email">Email</label>
              <input type="email" v-model="forgotEmail" id="forgot-email" placeholder="Enter your email" required />
            </div>
            <button type="submit" class="auth-button">Reset Password</button>
            <p class="back-link">
              Remembered? <a href="#" @click.prevent="switchToLogin">Log in</a>
            </p>
          </form>
        </main>
      </div>
    </transition>

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
          <input type="text" v-model="universitySearch" placeholder="Search university..." class="search-input" />
          <p v-if="universitySearch && universitySearch.trim().length < 3" class="helper-text">
            Please type at least 3 letters.
          </p>
          <div class="list-container">
            <ul class="university-list">
              <li v-for="(uniDoc, index) in universityDocs" :key="index" @click="selectUniversity(uniDoc)">
                {{ uniDoc.name }} – {{ uniDoc.counter }} students
              </li>
            </ul>
            <!-- Load More Button with Loading Spinner -->
            <div v-if="canLoadMore" class="load-more-container">
              <button @click="loadMoreUniversities" class="small-btn next-btn">
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
            <input type="text" v-model="customMajor" placeholder="Enter your degree" class="search-input" />
            <div class="next-btn-container">
              <button type="button" class="small-btn next-btn" @click="saveCustomMajor">Save</button>
            </div>
          </div>
          <div v-else>
            <input type="text" v-model="majorSearch" placeholder="Search degree..." class="search-input" />
            <div class="list-container">
              <ul class="university-list">
                <li v-for="(majorObj, index) in filteredMajors" :key="index" @click="selectMajor(majorObj.major_name)">
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
import axios from 'axios'
import { notify } from '@/services/toastService.js'
import NavBar from '@/components/NavBar.vue'
import Footer from '@/components/Footer.vue'
import { getDarkModePreference, setDarkModePreference } from '@/services/darkModeService.js'
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
    this.darkMode = getDarkModePreference()
    if (this.darkMode) {
      document.body.classList.add('dark-mode')
    } else {
      document.body.classList.remove('dark-mode')
    }
    // The rest of your existing mounted code...
    this.checkMobile()
    window.addEventListener('resize', this.checkMobile)
    this.setBackgroundGradient()
  },
  beforeUnmount() {
    window.removeEventListener('resize', this.checkMobile)
    document.body.style.overflow = ''
  },
  methods: {
    checkMobile() {
      this.isMobile = window.innerWidth <= 768
    },
    setBackgroundGradient() {
      const container = this.$refs.authContainer
      if (container) {
        container.style.background = 'var(--bg-gradient)'
      }
    },
    toggleDarkMode() {
      this.darkMode = !this.darkMode
      setDarkModePreference(this.darkMode)

      if (this.darkMode) {
        document.body.classList.add('dark-mode')
      } else {
        document.body.classList.remove('dark-mode')
      }
    },
    openUniversityModal() {
      console.log("openUniversityModal triggered")
      this.showUniversityModal = true
      this.universitySearch = ''
      this.universityDocs = []
      this.searchOffset = 0
      this.searchLimit = 10
      document.body.style.overflow = 'hidden'
    },
    closeUniversityModal() {
      this.showUniversityModal = false
      document.body.style.overflow = ''
    },
    selectUniversity(uniDoc) {
      this.selectedUniversityDoc = uniDoc
      this.closeUniversityModal()
    },
    openMajorModal() {
      if (!this.selectedUniversityDoc) {
        notify({ type: 'warning', message: 'Please select a university first.' })
        return
      }
      this.showMajorModal = true
      this.majorSearch = ''
      this.showCustomMajorInput = false
      this.customMajor = ''
      document.body.style.overflow = 'hidden'
    },
    closeMajorModal() {
      this.showMajorModal = false
      this.showCustomMajorInput = false
      document.body.style.overflow = ''
    },
    selectMajor(majorName) {
      this.degree = majorName
      this.closeMajorModal()
    },
    enableCustomMajor() {
      this.showCustomMajorInput = true
      this.customMajor = ''
    },
    saveCustomMajor() {
      if (this.customMajor.trim() !== '') {
        this.degree = this.customMajor.trim()
        this.closeMajorModal()
      } else {
        notify({ type: 'warning', message: 'Please enter your degree.' })
      }
    },
    goToSignUpStep(step) {
      this.signUpStep = step
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
      notify({ type: 'info', message: 'Forgot password request sent for ' + this.forgotEmail })
    },
    switchToSignup() {
      this.formMode = 'signup'
      this.signUpStep = 1
      this.$router.push({ path: '/login', query: { mode: 'signup' } })
    },
    switchToLogin() {
      this.formMode = 'login'
      this.$router.push({ path: '/login', query: { mode: 'login' } })
    },
    switchToForgot() {
      this.formMode = 'forgot'
    },
    loginWithGoogle() {
      window.location.href = `${API_URL}/auth/google`
    },
    async searchUniversities(query, loadMore = false) {
      try {
        if (!loadMore) {
          this.searchLimit = 10
          this.searchOffset = 0
        } else {
          this.searchLimit = 20
          this.isLoadingMore = true
        }
        const response = await axios.get(`${API_URL}/universities/search`, {
          params: {
            query,
            limit: this.searchLimit,
            offset: this.searchOffset
          }
        })
        const results = response.data
        this.lastFetchedCount = results.length
        if (loadMore) {
          const newResults = results.filter(u => !this.universityDocs.some(existing => existing.id === u.id))
          this.universityDocs = this.universityDocs.concat(newResults)
          this.searchOffset += newResults.length
          this.isLoadingMore = false
        } else {
          this.universityDocs = results
          this.searchOffset = results.length
        }
      } catch (err) {
        console.error('Error searching universities:', err)
        this.isLoadingMore = false
      }
    },
    loadMoreUniversities() {
      this.searchUniversities(this.universitySearch, true)
    }
  },
  watch: {
    universitySearch(newQuery) {
      if (this.searchTimeout) clearTimeout(this.searchTimeout)
      if (newQuery.trim().length >= 3) {
        this.searchOffset = 0
        this.searchTimeout = setTimeout(() => {
          this.searchUniversities(newQuery, false)
        }, 300)
      } else {
        this.universityDocs = []
      }
    },
    '$route.query.mode'(newMode) {
      if (newMode === 'signup') {
        this.formMode = 'signup'
        this.signUpStep = 1
      } else {
        this.formMode = 'login'
      }
    }
  }
}
</script>

<style scoped>
/* (Your existing CSS remains unchanged) */
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

.dark-mode .auth-main {
  --link-color: #B191FC;
  background: #2b2b2b;
  color: #fff;
}

.dark-mode .auth-main h1,
.dark-mode .auth-main p,
.dark-mode .form-group label {
  color: #fff;
}

.dark-mode .form-group input,
.dark-mode .form-group select,
.dark-mode .university-selector {
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

.dark-mode .modal-content {
  background: rgba(0, 0, 0, 0.7);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.dark-mode .google-btn {
  background: #000;
  color: #fff;
}

.dark-mode .google-btn:hover {
  background: #000;
}
</style>
