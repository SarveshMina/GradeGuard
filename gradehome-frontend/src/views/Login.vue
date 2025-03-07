<template>
  <div class="auth-container" ref="authContainer">
    <!-- Custom NavBar - no longer importing external component -->
    <div class="enhanced-navbar">
      <div class="navbar-container">
        <div class="navbar-logo">
          <i class="fas fa-shield-alt logo-icon"></i>
          <span class="logo-text">GradeGuard</span>
        </div>
        <div class="navbar-links">
          <a href="/" class="nav-link"><i class="fas fa-home"></i><span>Home</span></a>
          <a href="/features" class="nav-link"><i class="fas fa-star"></i><span>Features</span></a>
          <a href="/support" class="nav-link"><i class="fas fa-headset"></i><span>Support</span></a>
        </div>
        <div class="navbar-actions">
          <button @click="toggleDarkMode" class="theme-toggle" :title="darkMode ? 'Switch to Light Mode' : 'Switch to Dark Mode'">
            <i :class="darkMode ? 'fas fa-sun' : 'fas fa-moon'"></i>
          </button>
          <div v-if="!isMobile" class="auth-nav-buttons">
            <button v-if="formMode !== 'login'" @click="switchToLogin" class="nav-btn login-btn">
              <i class="fas fa-sign-in-alt"></i> Login
            </button>
            <button v-if="formMode !== 'signup'" @click="switchToSignup" class="nav-btn signup-btn">
              <i class="fas fa-user-plus"></i> Sign Up
            </button>
          </div>
          <button v-if="isMobile" @click="toggleMobileMenu" class="mobile-menu-btn">
            <i :class="mobileMenuOpen ? 'fas fa-times' : 'fas fa-bars'"></i>
          </button>
        </div>
      </div>
      <!-- Mobile menu -->
      <div class="mobile-menu" :class="{ 'mobile-menu-open': mobileMenuOpen }" v-if="isMobile">
        <a href="/" class="mobile-nav-link"><i class="fas fa-home"></i> Home</a>
        <a href="/features" class="mobile-nav-link"><i class="fas fa-star"></i> Features</a>
        <a href="/pricing" class="mobile-nav-link"><i class="fas fa-tag"></i> Pricing</a>
        <a href="/support" class="mobile-nav-link"><i class="fas fa-headset"></i> Support</a>
        <div class="mobile-auth-buttons">
          <button v-if="formMode !== 'login'" @click="switchToLogin" class="mobile-nav-btn login-btn">
            <i class="fas fa-sign-in-alt"></i> Login
          </button>
          <button v-if="formMode !== 'signup'" @click="switchToSignup" class="mobile-nav-btn signup-btn">
            <i class="fas fa-user-plus"></i> Sign Up
          </button>
        </div>
      </div>
    </div>

    <!-- Loading overlay for auto-login -->
    <div v-if="isCheckingSession" class="session-loading-overlay">
      <div class="session-loader">
        <div class="session-spinner"></div>
        <p>Checking your session...</p>
      </div>
    </div>

    <!-- Mobile header (if applicable) -->
    <div v-if="isMobile" class="mobile-header">
      <div class="mobile-logo">GradeGuard</div>
      <p class="mobile-tagline">Secure Your Academic Success</p>
    </div>

    <!-- Authentication content wrapper - redesigned to be side-by-side without separate panel -->
    <div class="auth-content-wrapper">
      <!-- Main content area with both branding and form -->
      <div class="main-content">
        <!-- Branding elements (desktop only) -->
        <div v-if="!isMobile" class="brand-content">
          <div class="brand-logo-container">
            <div class="animated-logo">
              <i class="fas fa-shield-alt brand-icon pulse"></i>
              <h1 class="brand-logo">GradeGuard</h1>
            </div>
            <p class="brand-tagline">Secure Your Academic Success</p>
          </div>

          <div class="brand-decoration">
            <div class="decoration-circle circle-1"></div>
            <div class="decoration-circle circle-2"></div>
            <div class="decoration-circle circle-3"></div>
          </div>

          <!-- Enhanced feature boxes -->
          <div class="brand-features">
            <div class="feature">
              <div class="feature-icon-container">
                <i class="fas fa-chart-line"></i>
              </div>
              <span>Track Progress</span>
            </div>
            <div class="feature">
              <div class="feature-icon-container">
                <i class="fas fa-calculator"></i>
              </div>
              <span>Calculate GPA</span>
            </div>
            <div class="feature">
              <div class="feature-icon-container">
                <i class="fas fa-graduation-cap"></i>
              </div>
              <span>Set Goals</span>
            </div>
            <div class="feature">
              <div class="feature-icon-container">
                <i class="fas fa-bell"></i>
              </div>
              <span>Get Reminders</span>
            </div>
          </div>

        </div>

        <!-- Form container -->
        <div class="form-container">
          <!-- Main form transition -->
          <transition name="fade-slide" mode="out-in">
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
                    <div class="floating-label-group">
                      <div class="input-wrapper" :class="{ 'has-value': loginEmail.length > 0, 'has-error': loginErrors.email }">
                        <i class="fas fa-envelope input-icon"></i>
                        <input
                            type="email"
                            v-model="loginEmail"
                            id="login-email"
                            placeholder=" "
                            @focus="clearError('email')"
                            required
                        />
                        <label for="login-email">Email</label>
                        <div class="input-indicator"></div>
                      </div>
                      <p v-if="loginErrors.email" class="error-message">{{ loginErrors.email }}</p>
                    </div>
                  </div>
                  <div class="form-group">
                    <div class="floating-label-group">
                      <div class="input-wrapper" :class="{ 'has-value': loginPassword.length > 0, 'has-error': loginErrors.password }">
                        <i class="fas fa-lock input-icon"></i>
                        <input
                            :type="showPassword ? 'text' : 'password'"
                            v-model="loginPassword"
                            id="login-password"
                            placeholder=" "
                            @focus="clearError('password')"
                            required
                        />
                        <label for="login-password">Password</label>
                        <button
                            type="button"
                            class="toggle-password"
                            @click="showPassword = !showPassword"
                            :aria-label="showPassword ? 'Hide password' : 'Show password'"
                        >
                          <i :class="showPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
                        </button>
                        <div class="input-indicator"></div>
                      </div>
                      <p v-if="loginErrors.password" class="error-message">{{ loginErrors.password }}</p>
                    </div>
                  </div>
                  <div class="form-options">
                    <div class="remember-me">
                      <label class="custom-checkbox">
                        <input type="checkbox" v-model="rememberMe">
                        <span class="checkmark"></span>
                        <span class="checkbox-label">Remember me</span>
                      </label>
                    </div>
                    <a href="#" @click.prevent="switchToForgot" class="forgot-link">Forgot your password?</a>
                  </div>
                  <button
                      type="submit"
                      class="auth-button"
                      :class="{ 'loading': isLoggingIn }"
                      :disabled="isLoggingIn"
                  >
                    <span v-if="!isLoggingIn">Login</span>
                    <span v-else class="btn-loading-text">
                      <span class="dot-loader"></span>
                    </span>
                    <i v-if="!isLoggingIn" class="fas fa-arrow-right"></i>
                  </button>
                </form>
                <div class="divider">
                  <span>OR</span>
                </div>
                <div class="oauth-container">
                  <button class="google-btn" @click="loginWithGoogle" :disabled="isLoggingIn">
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
                  <transition name="fade-slide" mode="out-in">
                    <!-- Step 1: Email & Password -->
                    <div v-if="signUpStep === 1" key="signup-step1" class="signup-step">
                      <div class="step-indicator">
                        <div class="step active">1</div>
                        <div class="step-line"></div>
                        <div class="step">2</div>
                      </div>
                      <div class="form-group">
                        <div class="floating-label-group">
                          <div class="input-wrapper" :class="{ 'has-value': signUpEmail.length > 0, 'has-error': signUpErrors.email }">
                            <i class="fas fa-envelope input-icon"></i>
                            <input
                                type="email"
                                v-model="signUpEmail"
                                id="signup-email"
                                placeholder=" "
                                @focus="clearSignUpError('email')"
                                required
                            />
                            <label for="signup-email">Email</label>
                            <div class="input-indicator"></div>
                          </div>
                          <p v-if="signUpErrors.email" class="error-message">{{ signUpErrors.email }}</p>
                        </div>
                      </div>
                      <div class="form-group">
                        <div class="floating-label-group">
                          <div class="input-wrapper" :class="{ 'has-value': signUpPassword.length > 0, 'has-error': signUpErrors.password }">
                            <i class="fas fa-lock input-icon"></i>
                            <input
                                :type="showPassword ? 'text' : 'password'"
                                v-model="signUpPassword"
                                id="signup-password"
                                placeholder=" "
                                @input="checkPasswordStrength"
                                @focus="clearSignUpError('password')"
                                required
                            />
                            <label for="signup-password">Password</label>
                            <button
                                type="button"
                                class="toggle-password"
                                @click="showPassword = !showPassword"
                                :aria-label="showPassword ? 'Hide password' : 'Show password'"
                            >
                              <i :class="showPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
                            </button>
                            <div class="input-indicator"></div>
                          </div>
                          <p v-if="signUpErrors.password" class="error-message">{{ signUpErrors.password }}</p>

                          <!-- Password strength indicator -->
                          <div class="password-strength" v-if="signUpPassword.length > 0">
                            <div class="strength-bars">
                              <div class="strength-bar" :class="getStrengthClass(1)"></div>
                              <div class="strength-bar" :class="getStrengthClass(2)"></div>
                              <div class="strength-bar" :class="getStrengthClass(3)"></div>
                              <div class="strength-bar" :class="getStrengthClass(4)"></div>
                            </div>
                            <span class="strength-text">{{ passwordStrengthText }}</span>
                          </div>

                          <ul class="password-requirements" v-if="signUpPassword.length > 0">
                            <li :class="{ 'requirement-met': passwordHasLength }">
                              <i :class="passwordHasLength ? 'fas fa-check' : 'fas fa-times'"></i>
                              At least 8 characters
                            </li>
                            <li :class="{ 'requirement-met': passwordHasUpper }">
                              <i :class="passwordHasUpper ? 'fas fa-check' : 'fas fa-times'"></i>
                              At least 1 uppercase letter
                            </li>
                            <li :class="{ 'requirement-met': passwordHasNumber }">
                              <i :class="passwordHasNumber ? 'fas fa-check' : 'fas fa-times'"></i>
                              At least 1 number
                            </li>
                            <li :class="{ 'requirement-met': passwordHasSpecial }">
                              <i :class="passwordHasSpecial ? 'fas fa-check' : 'fas fa-times'"></i>
                              At least 1 special character
                            </li>
                          </ul>
                        </div>
                      </div>
                      <div class="next-btn-container">
                        <button
                            type="button"
                            class="auth-button"
                            @click="goToSignUpStep(2)"
                            :disabled="!isStep1Valid"
                            :class="{ 'disabled': !isStep1Valid }"
                        >
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
                        <div class="floating-label-group">
                          <div class="input-wrapper" :class="{ 'has-value': firstName.length > 0, 'has-error': signUpErrors.firstName }">
                            <i class="fas fa-user input-icon"></i>
                            <input
                                type="text"
                                v-model="firstName"
                                id="first-name"
                                placeholder=" "
                                @focus="clearSignUpError('firstName')"
                                required
                            />
                            <label for="first-name">First Name</label>
                            <div class="input-indicator"></div>
                          </div>
                          <p v-if="signUpErrors.firstName" class="error-message">{{ signUpErrors.firstName }}</p>
                        </div>
                      </div>

                      <!-- University selection -->
                      <div class="form-group">
                        <div class="floating-label-group">
                          <div class="selector-wrapper university-select"
                               @click="openUniversityModal"
                               :class="{ 'has-value': selectedUniversityDoc, 'has-error': signUpErrors.university }">
                            <i class="fas fa-university input-icon"></i>
                            <div class="university-selector">
                              <span v-if="selectedUniversityDoc">
                                {{ selectedUniversityDoc.name }} – {{ selectedUniversityDoc.counter }} students
                              </span>
                              <span v-else class="placeholder"></span>
                            </div>
                            <label>University/College</label>
                            <i class="fas fa-chevron-down selector-arrow"></i>
                            <div class="input-indicator"></div>
                          </div>
                          <p v-if="signUpErrors.university" class="error-message">{{ signUpErrors.university }}</p>
                        </div>
                      </div>

                      <!-- Degree (Major) selection -->
                      <div class="form-group">
                        <div class="floating-label-group">
                          <div class="selector-wrapper degree-select"
                               @click="openMajorModal"
                               :class="{ 'has-value': degree, 'has-error': signUpErrors.degree }">
                            <i class="fas fa-graduation-cap input-icon"></i>
                            <div class="university-selector">
                              <span v-if="degree">{{ degree }}</span>
                              <span v-else class="placeholder"></span>
                            </div>
                            <label>Degree</label>
                            <i class="fas fa-chevron-down selector-arrow"></i>
                            <div class="input-indicator"></div>
                          </div>
                          <p v-if="signUpErrors.degree" class="error-message">{{ signUpErrors.degree }}</p>
                        </div>
                      </div>

                      <!-- Calculator type -->
                      <div class="form-group">
                        <div class="floating-label-group">
                          <div class="selector-wrapper calc-select" :class="{ 'has-value': true }">
                            <i class="fas fa-calculator input-icon"></i>
                            <select v-model="calcType" id="calc-type" required>
                              <option value="UK Percentage">UK Percentage</option>
                              <option value="US GPA 5.0">US GPA 5.0</option>
                              <option value="US GPA 4.0">US GPA 4.0</option>
                            </select>
                            <label for="calc-type">Calculator Type</label>
                            <i class="fas fa-chevron-down selector-arrow"></i>
                            <div class="input-indicator"></div>
                          </div>
                        </div>
                      </div>

                      <div class="signup-buttons">
                        <button
                            type="submit"
                            class="auth-button"
                            :class="{ 'loading': isSigningUp }"
                            :disabled="isSigningUp || !isStep2Valid"
                        >
                          <span v-if="!isSigningUp">Create Account</span>
                          <span v-else class="btn-loading-text">
                            <span class="dot-loader"></span>
                          </span>
                          <i v-if="!isSigningUp" class="fas fa-check"></i>
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
                    <div class="floating-label-group">
                      <div class="input-wrapper" :class="{ 'has-value': forgotEmail.length > 0, 'has-error': forgotErrors.email }">
                        <i class="fas fa-envelope input-icon"></i>
                        <input
                            type="email"
                            v-model="forgotEmail"
                            id="forgot-email"
                            placeholder=" "
                            @focus="clearForgotError('email')"
                            required
                        />
                        <label for="forgot-email">Email</label>
                        <div class="input-indicator"></div>
                      </div>
                      <p v-if="forgotErrors.email" class="error-message">{{ forgotErrors.email }}</p>
                    </div>
                  </div>
                  <button
                      type="submit"
                      class="auth-button"
                      :class="{ 'loading': isResetting }"
                      :disabled="isResetting || !forgotEmail"
                  >
                    <span v-if="!isResetting">Send Reset Link</span>
                    <span v-else class="btn-loading-text">
                      <span class="dot-loader"></span>
                    </span>
                    <i v-if="!isResetting" class="fas fa-paper-plane"></i>
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
    </div>

    <!-- Enhanced footer with more info (only on desktop) -->
    <footer v-if="!isMobile" class="enhanced-footer">
      <div class="footer-container">
        <div class="footer-brand">
          <div class="footer-logo">
            <i class="fas fa-shield-alt"></i>
            <span>GradeGuard</span>
          </div>
          <p>Helping students track and achieve their academic goals since 2022.</p>
        </div>
        <div class="footer-links">
          <div class="footer-col">
            <h4>Company</h4>
            <ul>
              <li><a href="/about">About Us</a></li>
              <li><a href="/careers">Careers</a></li>
              <li><a href="/blog">Blog</a></li>
            </ul>
          </div>
          <div class="footer-col">
            <h4>Resources</h4>
            <ul>
              <li><a href="/help">Help Center</a></li>
              <li><a href="/guides">Study Guides</a></li>
              <li><a href="/tools">Academic Tools</a></li>
            </ul>
          </div>
          <div class="footer-col">
            <h4>Legal</h4>
            <ul>
              <li><a href="/privacy">Privacy Policy</a></li>
              <li><a href="/terms">Terms of Service</a></li>
              <li><a href="/cookies">Cookie Policy</a></li>
            </ul>
          </div>
        </div>
        <div class="footer-social">
          <a href="#" class="social-icon"><i class="fab fa-facebook-f"></i></a>
          <a href="#" class="social-icon"><i class="fab fa-twitter"></i></a>
          <a href="#" class="social-icon"><i class="fab fa-instagram"></i></a>
          <a href="#" class="social-icon"><i class="fab fa-linkedin-in"></i></a>
        </div>
      </div>
      <div class="footer-bottom">
        <p>&copy; 2025 GradeGuard. All rights reserved.</p>
      </div>
    </footer>

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
              <li v-if="universitySearch.trim().length >= 3 && universityDocs.length === 0" class="no-results">
                <i class="fas fa-search-minus list-icon"></i>
                <span>No universities found matching "{{ universitySearch }}"</span>
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
                <li v-if="majorSearch.trim().length > 0 && filteredMajors.length === 0" class="no-results">
                  <i class="fas fa-search-minus list-icon"></i>
                  <span>No degrees found matching "{{ majorSearch }}"</span>
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

    <!-- Success Modal -->
    <transition name="modal">
      <div v-if="showSuccessModal" class="modal-overlay success-modal-overlay">
        <div class="modal-content success-modal">
          <div class="success-icon">
            <i class="fas fa-check-circle pulse"></i>
          </div>
          <h2>{{ successMessage.title }}</h2>
          <p>{{ successMessage.message }}</p>
          <button @click="closeSuccessModal" class="auth-button">
            <span>Continue</span>
            <i class="fas fa-arrow-right"></i>
          </button>
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
import axios from 'axios'
import { notify } from '@/services/toastService.js'
import { getDarkModePreference, setDarkModePreference } from '@/services/darkModeService.js'
import { API_URL } from '/src/config.js'

export default {
  name: 'Login',
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
      forgotEmail: '',
      showPassword: false,
      rememberMe: false,
      passwordStrength: 0,
      passwordStrengthText: '',
      passwordHasLength: false,
      passwordHasUpper: false,
      passwordHasNumber: false,
      passwordHasSpecial: false,
      isLoggingIn: false,
      isSigningUp: false,
      isResetting: false,
      isCheckingSession: true,
      showSuccessModal: false,
      successMessage: { title: '', message: '' },
      mobileMenuOpen: false,
      loginErrors: {
        email: '',
        password: ''
      },
      signUpErrors: {
        email: '',
        password: '',
        firstName: '',
        university: '',
        degree: ''
      },
      forgotErrors: {
        email: ''
      }
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
    },
    isStep1Valid() {
      // Validate email format
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
      const validEmail = emailRegex.test(this.signUpEmail)

      // Password should meet minimum requirements
      return validEmail && this.passwordStrength >= 2
    },
    isStep2Valid() {
      return this.firstName.trim() !== '' && this.selectedUniversityDoc && this.degree
    }
  },
  mounted() {
    // Check if user is already logged in via session
    this.checkExistingSession();

    // Initialize dark mode from the service
    this.darkMode = getDarkModePreference();

    // Listen for dark mode changes from other components
    window.addEventListener('darkModeChange', (event) => {
      this.darkMode = event.detail.isDark;
      // Apply dark mode class to the container for proper styling
      if (this.$refs.authContainer) {
        if (this.darkMode) {
          this.$refs.authContainer.classList.add('dark-mode');
        } else {
          this.$refs.authContainer.classList.remove('dark-mode');
        }
      }
    });

    // Apply initial dark mode class if needed
    if (this.darkMode && this.$refs.authContainer) {
      this.$refs.authContainer.classList.add('dark-mode');
    }

    // Check for mobile view
    this.checkMobile();
    window.addEventListener('resize', this.checkMobile);

    // Add viewport meta tag for mobile responsiveness if it doesn't exist
    this.ensureViewportMeta();

    // Check for mode in URL query params
    const mode = this.$route.query.mode;
    if (mode === 'signup') {
      this.formMode = 'signup';
      this.signUpStep = 1;
    } else if (mode === 'forgot') {
      this.formMode = 'forgot';
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
    async checkExistingSession() {
      try {
        this.isCheckingSession = true;

        // Wait to show the loading screen for at least 300ms to avoid flashing
        const minLoadingTime = new Promise(resolve => setTimeout(resolve, 300));

        // Try to get the current user session
        const sessionPromise = axios.get(`${API_URL}/user/session`, {
          withCredentials: true
        });

        // Wait for both promises to resolve
        const [sessionResponse] = await Promise.all([sessionPromise, minLoadingTime]);

        // If we got a valid user session, redirect to dashboard
        if (sessionResponse.data && sessionResponse.data.user) {
          this.$router.push('/dashboard');
          return;
        }
      } catch (error) {
        console.log('No active session found');
      } finally {
        this.isCheckingSession = false;
      }
    },
    checkMobile() {
      // Increased threshold for better mobile experience
      this.isMobile = window.innerWidth <= 992;
    },
    ensureViewportMeta() {
      // Ensures the viewport meta tag exists for proper mobile scaling
      if (!document.querySelector('meta[name="viewport"]')) {
        const meta = document.createElement('meta');
        meta.name = 'viewport';
        meta.content = 'width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no';
        document.getElementsByTagName('head')[0].appendChild(meta);
      }
    },
    toggleDarkMode() {
      this.darkMode = !this.darkMode;
      setDarkModePreference(this.darkMode);

      // Dispatch the event for other components
      window.dispatchEvent(new CustomEvent('darkModeChange', {
        detail: { isDark: this.darkMode }
      }));

      // Apply dark mode class directly to the container
      if (this.$refs.authContainer) {
        if (this.darkMode) {
          this.$refs.authContainer.classList.add('dark-mode');
        } else {
          this.$refs.authContainer.classList.remove('dark-mode');
        }
      }
    },
    toggleMobileMenu() {
      this.mobileMenuOpen = !this.mobileMenuOpen;
    },
    openUniversityModal() {
      this.showUniversityModal = true;
      this.universitySearch = '';
      this.universityDocs = [];
      this.searchOffset = 0;
      this.searchLimit = 10;
      document.body.style.overflow = 'hidden';

      // Clear university error when opening modal
      this.signUpErrors.university = '';

      // Focus on search input after a short delay (for mobile keyboards)
      setTimeout(() => {
        const searchInput = document.querySelector('.modal-content .search-input');
        if (searchInput) searchInput.focus();
      }, 300);
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
        this.signUpErrors.university = 'Please select a university first.';
        return;
      }

      this.showMajorModal = true;
      this.majorSearch = '';
      this.showCustomMajorInput = false;
      this.customMajor = '';
      document.body.style.overflow = 'hidden';

      // Clear degree error when opening modal
      this.signUpErrors.degree = '';

      // Focus on search input after a short delay (for mobile keyboards)
      setTimeout(() => {
        const searchInput = document.querySelector('.modal-content .search-input');
        if (searchInput) searchInput.focus();
      }, 300);
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

      // Focus on custom major input after transition
      setTimeout(() => {
        const customInput = document.querySelector('.modal-content .search-input');
        if (customInput) customInput.focus();
      }, 300);
    },
    saveCustomMajor() {
      if (this.customMajor.trim() !== '') {
        this.degree = this.customMajor.trim();
        this.closeMajorModal();
      } else {
        this.signUpErrors.degree = 'Please enter your degree.';
      }
    },
    checkPasswordStrength() {
      const password = this.signUpPassword;

      // Check for basic requirements
      this.passwordHasLength = password.length >= 8;
      this.passwordHasUpper = /[A-Z]/.test(password);
      this.passwordHasNumber = /[0-9]/.test(password);
      this.passwordHasSpecial = /[^A-Za-z0-9]/.test(password);

      // Calculate strength score from 0-4
      let score = 0;

      if (this.passwordHasLength) score++;
      if (this.passwordHasUpper) score++;
      if (this.passwordHasNumber) score++;
      if (this.passwordHasSpecial) score++;

      this.passwordStrength = score;

      // Set text based on strength score
      if (password.length === 0) {
        this.passwordStrengthText = '';
      } else if (score === 0) {
        this.passwordStrengthText = 'Very Weak';
      } else if (score === 1) {
        this.passwordStrengthText = 'Weak';
      } else if (score === 2) {
        this.passwordStrengthText = 'Fair';
      } else if (score === 3) {
        this.passwordStrengthText = 'Good';
      } else {
        this.passwordStrengthText = 'Strong';
      }
    },
    getStrengthClass(level) {
      if (this.passwordStrength >= level) {
        if (this.passwordStrength === 1) return 'strength-weak';
        if (this.passwordStrength === 2) return 'strength-fair';
        if (this.passwordStrength === 3) return 'strength-good';
        if (this.passwordStrength === 4) return 'strength-strong';
      }
      return '';
    },
    clearError(field) {
      this.loginErrors[field] = '';
    },
    clearSignUpError(field) {
      this.signUpErrors[field] = '';
    },
    clearForgotError(field) {
      this.forgotErrors[field] = '';
    },
    goToSignUpStep(step) {
      // Validate step 1 before proceeding
      if (step === 2) {
        // Validate email format
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(this.signUpEmail)) {
          this.signUpErrors.email = 'Please enter a valid email address.';
          return;
        }

        // Validate password strength
        if (this.signUpPassword.length < 8) {
          this.signUpErrors.password = 'Password must be at least 8 characters.';
          return;
        }

        if (this.passwordStrength < 2) {
          this.signUpErrors.password = 'Password is too weak. Please follow the requirements.';
          return;
        }
      }

      this.signUpStep = step;
    },
    async handleSignUp() {
      // Validate step 2 fields
      if (!this.firstName.trim()) {
        this.signUpErrors.firstName = 'Please enter your first name.';
        return;
      }

      if (!this.selectedUniversityDoc) {
        this.signUpErrors.university = 'Please select your university.';
        return;
      }

      if (!this.degree) {
        this.signUpErrors.degree = 'Please select your degree.';
        return;
      }

      try {
        this.isSigningUp = true;

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
        });

        // Show success message before redirect
        this.successMessage = {
          title: 'Account Created!',
          message: 'Your account has been created successfully. Welcome to GradeGuard!'
        };
        this.showSuccessModal = true;

        // Wait for user to acknowledge before redirecting
        setTimeout(() => {
          if (this.showSuccessModal) {
            this.closeSuccessModal();
            this.$router.push('/dashboard');
          }
        }, 3000);

        if (this.selectedUniversityDoc) {
          const updatedResponse = await axios.get(`${API_URL}/stats/university`, {
            params: { name: this.selectedUniversityDoc.name }
          })
          this.selectedUniversityDoc = updatedResponse.data
        }
      } catch (error) {
        console.error(error);
        const errMsg = error.response?.data?.error || error.message;

        // Check for specific error messages and set appropriate field errors
        if (errMsg.includes('email')) {
          this.signUpErrors.email = errMsg;
          this.signUpStep = 1; // Go back to email step
        } else {
          notify({ type: 'error', message: 'Sign up failed: ' + errMsg });
        }
      } finally {
        this.isSigningUp = false;
      }
    },
    async handleLogin() {
      // Validate login fields
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(this.loginEmail)) {
        this.loginErrors.email = 'Please enter a valid email address.';
        return;
      }

      if (!this.loginPassword) {
        this.loginErrors.password = 'Please enter your password.';
        return;
      }

      try {
        this.isLoggingIn = true;

        await axios.post(`${API_URL}/login`, {
          email: this.loginEmail,
          password: this.loginPassword,
          rememberMe: this.rememberMe
        }, {
          withCredentials: true
        });

        // Show success message before redirect
        this.successMessage = {
          title: 'Login Successful',
          message: 'Welcome back to GradeGuard! Redirecting to your dashboard...'
        };
        this.showSuccessModal = true;

        // Redirect after a short delay
        setTimeout(() => {
          this.closeSuccessModal();
          this.$router.push('/dashboard');
        }, 1500);
      } catch (error) {
        const errMsg = error.response?.data?.error || error.message;

        // Check for specific error types
        if (errMsg.includes('email') || errMsg.includes('user')) {
          this.loginErrors.email = 'No account found with this email address.';
        } else if (errMsg.includes('password')) {
          this.loginErrors.password = 'Incorrect password. Please try again.';
        } else {
          notify({ type: 'error', message: 'Login failed: ' + errMsg });
        }
      } finally {
        this.isLoggingIn = false;
      }
    },
    async handleForgot() {
      // Validate email
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(this.forgotEmail)) {
        this.forgotErrors.email = 'Please enter a valid email address.';
        return;
      }

      try {
        this.isResetting = true;

        await axios.post(`${API_URL}/forgot-password`, {
          email: this.forgotEmail
        });

        // Show success message
        this.successMessage = {
          title: 'Email Sent',
          message: `Password reset instructions have been sent to ${this.forgotEmail}. Please check your inbox.`
        };
        this.showSuccessModal = true;

        // Switch back to login after closing the success modal
        setTimeout(() => {
          if (this.showSuccessModal) {
            this.closeSuccessModal();
            this.switchToLogin();
          }
        }, 3000);
      } catch (error) {
        const errMsg = error.response?.data?.error || error.message;

        if (errMsg.includes('not found') || errMsg.includes('no account')) {
          this.forgotErrors.email = 'No account found with this email address.';
        } else {
          notify({ type: 'error', message: 'Password reset request failed: ' + errMsg });
        }
      } finally {
        this.isResetting = false;
      }
    },
    closeSuccessModal() {
      this.showSuccessModal = false;
    },
    switchToSignup() {
      this.formMode = 'signup';
      this.signUpStep = 1;
      this.$router.push({ path: '/login', query: { mode: 'signup' } });

      // Close mobile menu if open
      this.mobileMenuOpen = false;
    },
    switchToLogin() {
      this.formMode = 'login';
      this.$router.push({ path: '/login', query: { mode: 'login' } });

      // Close mobile menu if open
      this.mobileMenuOpen = false;
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
    },
    mobileMenuOpen(isOpen) {
      // Prevent body scrolling when mobile menu is open
      if (isOpen) {
        document.body.style.overflow = 'hidden';
      } else {
        document.body.style.overflow = '';
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
  background: linear-gradient(135deg, #f5f7fa 0%, #e4e8f0 100%); /* Light mode gradient */
  color: var(--text-primary);
  font-family: "Montserrat", sans-serif;
  transition: all var(--transition-speed) ease;
  -webkit-tap-highlight-color: transparent; /* Removes tap highlight on mobile */
  position: relative;
  overflow-x: hidden;
}

/* Dark mode specific styles */
.auth-container.dark-mode {
  background: linear-gradient(135deg, #2a2d3e 0%, #1a1c2a 100%); /* Dark mode gradient */
}

/* CSS custom properties for consistent colors */
:root {
  --primary-color: #673ab7;
  --primary-dark: #512da8;
  --primary-light: #9575cd;
  --primary-color-transparent: rgba(103, 58, 183, 0.2);
  --text-primary: #333333;
  --text-secondary: #666666;
  --text-muted: #888888;
  --border-color: #e0e0e0;
  --bg-card: #ffffff;
  --bg-input: #f5f7fa;
  --bg-muted: #f0f0f0;
  --bg-hover: #f9f9f9;
  --success-color: #4caf50;
  --warning-color: #ff9800;
  --error-color: #f44336;
  --transition-speed: 0.3s;
  --box-shadow: 0 8px 30px rgba(0, 0, 0, 0.1);
}

.dark-mode {
  --text-primary: #f5f7fa;
  --text-secondary: #d0d0d0;
  --text-muted: #a0a0a0;
  --border-color: #3f4156;
  --bg-card: #2a2d3e;
  --bg-input: #1e2030;
  --bg-muted: #323546;
  --bg-hover: #3c4052;
  --box-shadow: 0 8px 30px rgba(0, 0, 0, 0.3);
}

/* Enhanced Navbar Styles */
.enhanced-navbar {
  background-color: #ffffff;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
  padding: 0.75rem 2rem;
  position: relative;
  z-index: 100;
  transition: all 0.3s ease;
}

.dark-mode .enhanced-navbar {
  background-color: #232535;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
}

.navbar-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1400px;
  margin: 0 auto;
}

.navbar-logo {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.3rem;
  font-weight: 700;
  color: var(--primary-color);
}

.logo-icon {
  font-size: 1.5rem;
}

.navbar-links {
  display: flex;
  gap: 1.5rem;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--text-secondary);
  text-decoration: none;
  font-weight: 500;
  font-size: 0.95rem;
  padding: 0.5rem 0;
  position: relative;
  transition: all 0.3s ease;
}

.nav-link::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 0;
  height: 2px;
  background: var(--primary-color);
  transition: width 0.3s ease;
}

.nav-link:hover {
  color: var(--primary-color);
}

.nav-link:hover::after {
  width: 100%;
}

.navbar-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.theme-toggle {
  background: none;
  border: none;
  color: var(--text-secondary);
  font-size: 1.1rem;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.theme-toggle:hover {
  background-color: var(--bg-muted);
  color: var(--primary-color);
  transform: rotate(15deg);
}

.auth-nav-buttons {
  display: flex;
  gap: 0.75rem;
}

.nav-btn {
  padding: 0.6rem 1.2rem;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
}

.login-btn {
  border: 1px solid var(--primary-color);
  background: transparent;
  color: var(--primary-color);
}

.login-btn:hover {
  background: rgba(103, 58, 183, 0.1);
  transform: translateY(-2px);
}

.signup-btn {
  border: none;
  background: var(--primary-color);
  color: white;
}

.signup-btn:hover {
  background: var(--primary-dark);
  transform: translateY(-2px);
  box-shadow: 0 4px 10px rgba(103, 58, 183, 0.3);
}

.mobile-menu-btn {
  background: none;
  border: none;
  font-size: 1.2rem;
  color: var(--text-primary);
  cursor: pointer;
  padding: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Mobile Menu */
.mobile-menu {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background-color: var(--bg-card);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  transform: translateY(-20px);
  opacity: 0;
  pointer-events: none;
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  z-index: 90;
}

.mobile-menu-open {
  transform: translateY(0);
  opacity: 1;
  pointer-events: auto;
}

.mobile-nav-link {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem;
  color: var(--text-primary);
  text-decoration: none;
  font-weight: 500;
  border-radius: 8px;
}

.mobile-nav-link:hover,
.mobile-nav-link:active {
  background-color: var(--bg-muted);
  color: var(--primary-color);
}

.mobile-auth-buttons {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-top: 0.5rem;
  padding-top: 0.75rem;
  border-top: 1px solid var(--border-color);
}

.mobile-nav-btn {
  width: 100%;
  padding: 0.8rem;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

/* Auto-login loading overlay */
.session-loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(255, 255, 255, 0.9);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.dark-mode .session-loading-overlay {
  background-color: rgba(30, 32, 48, 0.9);
}

.session-loader {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.session-spinner {
  width: 50px;
  height: 50px;
  border: 4px solid rgba(103, 58, 183, 0.3);
  border-radius: 50%;
  border-top-color: var(--primary-color);
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Content wrapper */
.auth-content-wrapper {
  display: flex;
  flex: 1;
  justify-content: center;
  align-items: center;
  padding: 2rem;
}

/* Main content area - branding elements and form side by side */
.main-content {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 4rem;
  max-width: 1200px;
  width: 100%;
}

/* Branding content */
.brand-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  color: var(--primary-color);
  position: relative;
  z-index: 1;
}

.animated-logo {
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
}

.brand-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.pulse {
  animation: pulse-animation 2s infinite;
}

@keyframes pulse-animation {
  0% {
    transform: scale(1);
    text-shadow: 0 0 0 rgba(103, 58, 183, 0);
  }
  50% {
    transform: scale(1.05);
    text-shadow: 0 0 15px rgba(103, 58, 183, 0.5);
  }
  100% {
    transform: scale(1);
    text-shadow: 0 0 0 rgba(103, 58, 183, 0);
  }
}

.brand-decoration {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  overflow: hidden;
  pointer-events: none;
  z-index: -1;
}

.decoration-circle {
  position: absolute;
  border-radius: 50%;
  background: linear-gradient(135deg, rgba(103, 58, 183, 0.1), rgba(156, 39, 176, 0.1));
}

.circle-1 {
  width: 250px;
  height: 250px;
  top: -50px;
  left: -100px;
  animation: float 8s ease-in-out infinite;
}

.circle-2 {
  width: 180px;
  height: 180px;
  bottom: 60px;
  right: -50px;
  animation: float 6s ease-in-out infinite reverse;
}

.circle-3 {
  width: 120px;
  height: 120px;
  top: 50%;
  left: 20px;
  animation: float 10s ease-in-out infinite 1s;
}

@keyframes float {
  0% {
    transform: translate(0, 0);
  }
  50% {
    transform: translate(15px, 15px);
  }
  100% {
    transform: translate(0, 0);
  }
}

.brand-logo-container {
  margin-bottom: 2rem;
}

.brand-logo {
  font-size: 2.5rem;
  font-weight: 700;
  margin: 0 0 0.5rem;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
}

.brand-tagline {
  font-size: 1.2rem;
  opacity: 0.9;
  margin: 0;
}

/* Enhanced Feature boxes */
.brand-features {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 1.5rem;
  margin-top: 3rem;
}

.feature {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: rgba(103, 58, 183, 0.08);
  border-radius: 16px;
  padding: 1.5rem;
  width: 140px;
  height: 140px;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  position: relative;
  overflow: hidden;
}

.dark-mode .feature {
  background: rgba(103, 58, 183, 0.15);
}

.feature::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 3px;
  background: linear-gradient(90deg, var(--primary-color), var(--primary-light));
  transform: scaleX(0);
  transition: transform 0.5s ease;
  transform-origin: left;
}

.feature:hover {
  transform: translateY(-15px) rotate(2deg);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.1);
}

.dark-mode .feature:hover {
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.3);
}

.feature:hover::after {
  transform: scaleX(1);
}

.feature-icon-container {
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--primary-color), var(--primary-light));
  margin-bottom: 1rem;
  color: white;
  font-size: 1.5rem;
  transition: all 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);
  box-shadow: 0 5px 15px rgba(103, 58, 183, 0.3);
}

.feature:hover .feature-icon-container {
  transform: scale(1.1) rotate(-5deg);
}

.feature span {
  font-size: 1rem;
  font-weight: 600;
  text-align: center;
  color: var(--text-primary);
  transition: all 0.3s ease;
}

.feature:hover span {
  color: var(--primary-color);
}

/* Social proof section */
.social-proof {
  margin-top: 3rem;
  background-color: var(--bg-card);
  padding: 1.2rem;
  border-radius: 12px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
  width: 100%;
  max-width: 300px;
  transition: all 0.3s ease;
}

.dark-mode .social-proof {
  background-color: rgba(42, 45, 62, 0.7);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

.social-proof:hover {
  transform: scale(1.05);
}

.ratings {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}

.stars {
  color: #FFD700;
  font-size: 1.2rem;
  letter-spacing: 2px;
}

.ratings span {
  font-size: 0.85rem;
  color: var(--text-secondary);
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

.mobile-tagline {
  color: rgba(255, 255, 255, 0.9);
  margin: 0.5rem 0 0;
  font-size: 1rem;
}

/* Form container */
.form-container {
  width: 100%;
  max-width: 420px;
}

.auth-wrapper {
  width: 100%;
  animation: fadeInUp 0.7s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

/* Form styling */
.auth-main {
  background: var(--bg-card);
  padding: 2.5rem;
  border-radius: 16px;
  box-shadow: var(--box-shadow);
  width: 100%;
  color: var(--text-primary);
  transition: all var(--transition-speed) ease;
  position: relative;
  overflow: hidden;
}

.auth-main::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 5px;
  background: linear-gradient(90deg, var(--primary-color), var(--primary-light));
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
  width: 0;
  height: 4px;
  background: var(--primary-color);
  margin: 0.5rem auto 0;
  border-radius: 2px;
  transition: width 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  animation: titleUnderline 0.8s 0.3s forwards;
}

@keyframes titleUnderline {
  0% { width: 0; }
  100% { width: 60px; }
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
  position: relative;
}

.text-link::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 100%;
  height: 1px;
  background: var(--primary-color);
  transform: scaleX(0);
  transition: transform 0.3s ease;
  transform-origin: right;
}

.text-link:hover::after {
  transform: scaleX(1);
  transform-origin: left;
}

.auth-form {
  margin-bottom: 1rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

/* Floating Label Group */
.floating-label-group {
  position: relative;
}

.error-message {
  color: var(--error-color);
  font-size: 0.8rem;
  margin-top: 0.25rem;
  margin-left: 0.5rem;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.error-message::before {
  content: '\f071'; /* Font Awesome exclamation triangle */
  font-family: 'Font Awesome 5 Free';
  font-weight: 900;
}

/* Enhanced Input Wrapper */
.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
  overflow: hidden;
  border: 1px solid var(--border-color);
  border-radius: 12px;
  background: var(--bg-input);
  transition: all 0.3s ease;
}

.input-wrapper.has-error {
  border-color: var(--error-color);
}

.input-wrapper.has-value label,
.input-wrapper input:focus ~ label {
  transform: translateY(-130%) scale(0.8);
  color: var(--primary-color);
}

.input-wrapper label {
  position: absolute;
  left: 2.8rem;
  color: var(--text-muted);
  pointer-events: none;
  transform-origin: left;
  transition: all 0.3s ease;
}

.input-wrapper .input-indicator {
  position: absolute;
  bottom: 0;
  left: 0;
  height: 2px;
  width: 100%;
  background: linear-gradient(90deg, var(--primary-color), var(--primary-light));
  transform: scaleX(0);
  transition: transform 0.3s ease;
  transform-origin: left;
}

.input-wrapper.has-error .input-indicator {
  background: var(--error-color);
  transform: scaleX(1);
}

.input-wrapper input:focus ~ .input-indicator {
  transform: scaleX(1);
}

.input-icon {
  position: absolute;
  left: 1rem;
  font-size: 0.9rem;
  color: var(--text-muted);
  transition: all 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);
  pointer-events: none;
}

.input-wrapper.has-error .input-icon {
  color: var(--error-color);
}

.input-wrapper.has-value .input-icon,
.input-wrapper input:focus ~ .input-icon {
  color: var(--primary-color);
  transform: scale(1.2);
}

.input-wrapper input {
  width: 100%;
  padding: 0.9rem 2.8rem;
  border: none;
  font-size: 1rem;
  color: var(--text-primary);
  background: transparent;
  transition: all 0.3s ease;
}

.input-wrapper input:focus {
  outline: none;
}

/* Password Toggle Button */
.toggle-password {
  position: absolute;
  right: 1rem;
  background: none;
  border: none;
  color: var(--text-muted);
  cursor: pointer;
  padding: 0.5rem;
  font-size: 0.9rem;
  transition: all 0.3s ease;
  z-index: 2;
}

.toggle-password:hover {
  color: var(--primary-color);
}

/* Password Strength Indicator */
.password-strength {
  margin-top: 0.5rem;
}

.strength-bars {
  display: flex;
  gap: 0.25rem;
  margin-bottom: 0.25rem;
}

.strength-bar {
  height: 4px;
  flex: 1;
  background-color: var(--border-color);
  border-radius: 2px;
  transition: all 0.3s ease;
}

.strength-weak {
  background-color: var(--error-color);
}

.strength-fair {
  background-color: var(--warning-color);
}

.strength-good {
  background-color: #2196F3;
}

.strength-strong {
  background-color: var(--success-color);
}

.strength-text {
  font-size: 0.75rem;
  color: var(--text-muted);
}

/* Password Requirements */
.password-requirements {
  list-style: none;
  padding: 0;
  margin: 0.5rem 0 0;
  font-size: 0.75rem;
  color: var(--text-muted);
}

.password-requirements li {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.25rem;
}

.requirement-met {
  color: var(--success-color);
}

/* Form Options (Remember Me and Forgot Password) */
.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

/* Custom Checkbox */
.custom-checkbox {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  user-select: none;
  position: relative;
  padding: 0.25rem 0;
}

.custom-checkbox input {
  position: absolute;
  opacity: 0;
  cursor: pointer;
  height: 0;
  width: 0;
}

.checkmark {
  position: relative;
  height: 18px;
  width: 18px;
  background-color: var(--bg-input);
  border: 1px solid var(--border-color);
  border-radius: 4px;
  transition: all 0.3s ease;
}

.custom-checkbox:hover input ~ .checkmark {
  border-color: var(--primary-color);
}

.custom-checkbox input:checked ~ .checkmark {
  background-color: var(--primary-color);
  border-color: var(--primary-color);
}

.checkmark:after {
  content: "";
  position: absolute;
  display: none;
  left: 6px;
  top: 2px;
  width: 5px;
  height: 10px;
  border: solid white;
  border-width: 0 2px 2px 0;
  transform: rotate(45deg);
}

.custom-checkbox input:checked ~ .checkmark:after {
  display: block;
}

.checkbox-label {
  font-size: 0.85rem;
  color: var(--text-secondary);
}

.forgot-link {
  font-size: 0.85rem;
  color: var(--primary-color);
  text-decoration: none;
  transition: all 0.3s ease;
  font-weight: 500;
  display: inline-block;
  padding: 0.25rem 0;
}

.forgot-link:hover {
  text-decoration: underline;
}

/* Enhanced Auth Button */
.auth-button {
  width: 100%;
  padding: 0.9rem 1.5rem;
  border: none;
  border-radius: 12px;
  background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-dark) 100%);
  background-size: 200% 100%;
  background-position: right bottom;
  color: white;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 0.5rem;
  box-shadow: 0 4px 12px rgba(103, 58, 183, 0.3);
  position: relative;
  overflow: hidden;
  min-height: 3.5rem;
}

.auth-button::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(to right, rgba(255,255,255,0) 0%, rgba(255,255,255,0.2) 50%, rgba(255,255,255,0) 100%);
  transform: translateX(-100%);
  transition: transform 0.6s ease;
}

.auth-button:not(.disabled):not(:disabled):hover {
  box-shadow: 0 6px 22px rgba(103, 58, 183, 0.5);
  transform: translateY(-3px) scale(1.01);
  background-position: left bottom;
}

.auth-button:not(.disabled):not(:disabled):hover::after {
  transform: translateX(100%);
}

.auth-button:not(.disabled):not(:disabled):active {
  transform: translateY(1px) scale(0.98);
  box-shadow: 0 2px 8px rgba(103, 58, 183, 0.4);
  transition: all 0.1s ease;
}

.auth-button i {
  font-size: 0.9rem;
  transition: transform 0.3s ease;
}

.auth-button:not(.disabled):not(:disabled):hover i {
  transform: translateX(5px) rotate(5deg);
  transition: transform 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

.auth-button.disabled,
.auth-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

/* Loading Button */
.auth-button.loading {
  background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-dark) 100%);
  color: transparent;
  pointer-events: none;
}

.btn-loading-text {
  display: flex;
  justify-content: center;
  align-items: center;
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.dot-loader {
  position: relative;
  width: 10px;
  height: 10px;
  border-radius: 5px;
  background-color: white;
  color: white;
  animation: dotFlashing 1s infinite linear alternate;
  animation-delay: .5s;
}

.dot-loader::before, .dot-loader::after {
  content: '';
  display: inline-block;
  position: absolute;
  top: 0;
  width: 10px;
  height: 10px;
  border-radius: 5px;
  background-color: white;
  color: white;
  animation: dotFlashing 1s infinite alternate;
}

.dot-loader::before {
  left: -15px;
  animation-delay: 0s;
}

.dot-loader::after {
  left: 15px;
  animation-delay: 1s;
}

@keyframes dotFlashing {
  0% {
    background-color: white;
  }
  50%,
  100% {
    background-color: rgba(255, 255, 255, 0.2);
  }
}

/* Enhanced Divider */
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
  min-height: 3.5rem;
  position: relative;
  overflow: hidden;
}

.google-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, rgba(103, 58, 183, 0.05), rgba(103, 58, 183, 0), rgba(103, 58, 183, 0.05));
  transform: translateX(-100%);
  transition: transform 0.8s ease;
}

.google-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.1);
  border-color: var(--primary-color);
}

.google-btn:hover::before {
  transform: translateX(100%);
}

.google-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
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
  position: relative;
  z-index: 1;
}

.step.active {
  background: var(--primary-color);
  color: white;
  box-shadow: 0 0 0 3px rgba(103, 58, 183, 0.3);
  animation: pulseStep 1.5s infinite alternate;
}

.step.completed {
  background: var(--success-color);
  color: white;
  animation: scaleStep 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

@keyframes pulseStep {
  0% {
    box-shadow: 0 0 0 3px rgba(103, 58, 183, 0.3);
  }
  100% {
    box-shadow: 0 0 0 6px rgba(103, 58, 183, 0.1);
  }
}

@keyframes scaleStep {
  0% {
    transform: scale(0.5);
  }
  50% {
    transform: scale(1.2);
  }
  100% {
    transform: scale(1);
  }
}

.step-line {
  flex: 1;
  height: 3px;
  background: var(--border-color);
  margin: 0 10px;
  position: relative;
  overflow: hidden;
}

.step-line.completed {
  background: var(--success-color);
}

.step-line.completed::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, rgba(255, 255, 255, 0), rgba(255, 255, 255, 0.5), rgba(255, 255, 255, 0));
  animation: shimmer 2s infinite;
}

@keyframes shimmer {
  0% {
    transform: translateX(-100%);
  }
  100% {
    transform: translateX(100%);
  }
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
  padding: 0.5rem 0;
}

.back-link:hover, .back-link:active {
  color: var(--primary-color);
}

.back-link i {
  font-size: 0.7rem;
  transition: transform 0.3s ease;
}

.back-link:hover i {
  transform: translateX(-3px);
}

.back-link-container {
  text-align: center;
  margin-top: 1.5rem;
}

/* Enhanced Selector Wrapper */
.selector-wrapper {
  position: relative;
  cursor: pointer;
  border: 1px solid var(--border-color);
  border-radius: 12px;
  background: var(--bg-input);
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  overflow: hidden;
}

.selector-wrapper.has-error {
  border-color: var(--error-color);
}

.selector-wrapper.has-value label,
.selector-wrapper:focus-within label {
  transform: translateY(-130%) scale(0.8);
  color: var(--primary-color);
}

.selector-wrapper label {
  position: absolute;
  left: 2.8rem;
  color: var(--text-muted);
  pointer-events: none;
  transform-origin: left;
  transition: all 0.3s ease;
}

.selector-wrapper .input-indicator {
  position: absolute;
  bottom: 0;
  left: 0;
  height: 2px;
  width: 100%;
  background: linear-gradient(90deg, var(--primary-color), var(--primary-light));
  transform: scaleX(0);
  transition: transform 0.3s ease;
  transform-origin: left;
}

.selector-wrapper.has-error .input-indicator {
  background: var(--error-color);
  transform: scaleX(1);
}

.selector-wrapper:hover .input-indicator {
  transform: scaleX(1);
}

.selector-arrow {
  position: absolute;
  right: 1rem;
  font-size: 0.9rem;
  color: var(--text-muted);
  transition: transform 0.3s ease;
  pointer-events: none;
}

.selector-wrapper:hover .selector-arrow {
  color: var(--primary-color);
  transform: translateY(2px);
}

.university-selector {
  flex: 1;
  padding: 0.9rem 2.8rem 0.9rem 2.8rem;
  cursor: pointer;
  color: var(--text-primary);
  min-height: 3.5rem;
  display: flex;
  align-items: center;
}

.university-selector .placeholder {
  color: transparent;
}

.selector-wrapper select {
  width: 100%;
  padding: 0.9rem 2.8rem;
  border: none;
  background: transparent;
  appearance: none;
  color: var(--text-primary);
  font-size: 1rem;
  cursor: pointer;
  z-index: 1;
}

.selector-wrapper select:focus {
  outline: none;
}

/* Enhanced Footer */
.enhanced-footer {
  background-color: #f8f9fa;
  padding: 3rem 2rem 1rem;
  color: var(--text-secondary);
  border-top: 1px solid var(--border-color);
  transition: all 0.3s ease;
}

.dark-mode .enhanced-footer {
  background-color: #1e2030;
  border-top-color: #2c2e3d;
}

.footer-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  max-width: 1400px;
  margin: 0 auto;
  gap: 2rem;
}

.footer-brand {
  flex: 1;
  min-width: 250px;
}

.footer-logo {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--primary-color);
  font-size: 1.2rem;
  font-weight: 700;
  margin-bottom: 1rem;
}

.footer-brand p {
  color: var(--text-secondary);
  line-height: 1.5;
  font-size: 0.95rem;
}

.footer-links {
  display: flex;
  gap: 2rem;
  flex: 2;
  justify-content: space-around;
}

.footer-col {
  min-width: 120px;
}

.footer-col h4 {
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: 1.2rem;
  color: var(--text-primary);
}

.footer-col ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.footer-col ul li {
  margin-bottom: 0.75rem;
}

.footer-col ul li a {
  color: var(--text-secondary);
  text-decoration: none;
  font-size: 0.9rem;
  transition: color 0.3s ease;
}

.footer-col ul li a:hover {
  color: var(--primary-color);
}

.footer-social {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
}

.social-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background-color: var(--bg-muted);
  color: var(--text-secondary);
  transition: all 0.3s ease;
}

.social-icon:hover {
  background-color: var(--primary-color);
  color: white;
  transform: translateY(-3px);
}

.footer-bottom {
  text-align: center;
  padding-top: 2rem;
  margin-top: 2rem;
  border-top: 1px solid var(--border-color);
  color: var(--text-muted);
  font-size: 0.85rem;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(3px);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  padding: 1rem;
}

.modal-content {
  background: var(--bg-card);
  border-radius: 16px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
  width: 100%;
  max-width: 400px;
  max-height: 80vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  animation: modalEntrance 0.5s cubic-bezier(0.17, 0.67, 0.35, 1.2);
}

@keyframes modalEntrance {
  0% {
    opacity: 0;
    transform: scale(0.8) translateY(30px);
  }
  100% {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid var(--border-color);
}

.modal-header h2 {
  font-size: 1.2rem;
  font-weight: 700;
  margin: 0;
  color: var(--text-primary);
}

.close-button {
  background: var(--bg-muted);
  border: none;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  font-size: 1.5rem;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.3s ease;
}

.close-button:hover {
  background-color: var(--primary-color);
  color: white;
  transform: rotate(90deg);
}

.search-container {
  position: relative;
  padding: 0 1.5rem;
  margin: 1.5rem 0;
}

.search-icon {
  position: absolute;
  left: 2.5rem;
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
  font-size: 1rem;
  transition: all 0.3s ease;
}

.search-input:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px var(--primary-color-transparent);
}

.helper-text {
  font-size: 0.85rem;
  color: var(--text-muted);
  margin: -0.5rem 0 0.5rem 1.5rem;
}

.list-container {
  flex: 1;
  overflow-y: auto;
  padding: 0 1.5rem 1.5rem;
}

.university-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.university-list li {
  display: flex;
  align-items: center;
  padding: 0.9rem 1rem;
  margin-bottom: 0.5rem;
  border-radius: 12px;
  background: var(--bg-card);
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  gap: 0.75rem;
}

.university-list li:hover {
  background: var(--bg-hover);
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.dark-mode .university-list li:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
}

.list-icon {
  color: var(--primary-color);
  font-size: 1.2rem;
}

.uni-info {
  flex: 1;
  overflow: hidden;
}

.uni-name {
  font-weight: 600;
  color: var(--text-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.uni-count {
  font-size: 0.8rem;
  color: var(--text-muted);
}

.custom-option {
  color: var(--primary-color) !important;
}

.custom-option i {
  font-size: 1.2rem;
}

.no-results {
  color: var(--text-muted) !important;
  cursor: default !important;
  justify-content: center;
  padding: 2rem 1rem !important;
}

.no-results:hover {
  transform: none !important;
  box-shadow: none !important;
  background: var(--bg-card) !important;
}

.load-more-container {
  display: flex;
  justify-content: center;
  margin-top: 1rem;
}

.load-more-btn {
  background: var(--bg-muted);
  color: var(--text-primary);
  border: none;
  padding: 0.6rem 1.5rem;
  border-radius: 12px;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.load-more-btn:hover {
  background: var(--bg-hover);
  color: var(--primary-color);
}

.spinner {
  display: inline-block;
  width: 20px;
  height: 20px;
  border: 3px solid rgba(103, 58, 183, 0.3);
  border-radius: 50%;
  border-top-color: var(--primary-color);
  animation: spin 1s linear infinite;
}

/* Success Modal */
.success-modal-overlay {
  z-index: 1010;
}

.success-modal {
  padding: 2rem;
  align-items: center;
  text-align: center;
}

.success-icon {
  font-size: 4rem;
  color: var(--success-color);
  margin-bottom: 1.5rem;
}

.success-modal h2 {
  font-size: 1.5rem;
  margin-bottom: 1rem;
}

.success-modal p {
  color: var(--text-secondary);
  margin-bottom: 1.5rem;
}

.success-modal .auth-button {
  max-width: 200px;
}

/* Transitions */
.fade-slide-enter-active {
  transition: all 0.3s cubic-bezier(0.17, 0.67, 0.35, 1.2);
}

.fade-slide-leave-active {
  transition: all 0.2s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

.fade-slide-enter-from {
  opacity: 0;
  transform: translateY(30px) scale(0.95);
}

.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(-30px) scale(0.95);
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
  0% {
    opacity: 0;
    transform: translateY(30px) scale(0.95);
  }
  70% {
    opacity: 1;
    transform: translateY(-5px) scale(1.02);
  }
  100% {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

/* Responsive Styles */
@media (max-width: 1024px) {
  .main-content {
    gap: 2rem;
  }

  .footer-container {
    flex-direction: column;
    gap: 2rem;
  }

  .footer-links {
    flex-wrap: wrap;
    gap: 2rem 4rem;
  }
}

@media (max-width: 992px) {
  .brand-content {
    display: none;
  }

  .navbar-links {
    display: none;
  }

  .auth-content-wrapper {
    padding: 1rem 0;
  }

  .form-container {
    max-width: 480px;
    width: 90%;
    margin: 0 auto;
  }
}

@media (max-width: 768px) {
  .enhanced-navbar {
    padding: 0.75rem 1rem;
  }

  .form-options {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .forgot-link {
    align-self: flex-end;
  }

  .auth-main {
    padding: 2rem 1.5rem;
  }
}

@media (max-width: 480px) {
  .auth-main {
    padding: 1.5rem 1.25rem;
  }

  .form-title {
    font-size: 1.5rem;
  }

  .mobile-menu-btn {
    font-size: 1.5rem;
  }

  .modal-content {
    max-width: 100%;
    max-height: 90vh;
  }

  .modal-header {
    padding: 1.25rem;
  }

  .search-container {
    padding: 0 1.25rem;
    margin: 1.25rem 0;
  }

  .list-container {
    padding: 0 1.25rem 1.25rem;
  }
}

/* Fix for iOS input zooming */
@media screen and (-webkit-min-device-pixel-ratio:0) {
  select,
  textarea,
  input {
    font-size: 16px; /* Prevents iOS zoom on focus */
  }
}

/* Ensure hardware acceleration for smoother transitions */
.auth-container,
.auth-main,
.modal-content,
.auth-button,
.university-list li,
.feature {
  -webkit-transform: translateZ(0);
  -moz-transform: translateZ(0);
  -ms-transform: translateZ(0);
  -o-transform: translateZ(0);
  transform: translateZ(0);
  backface-visibility: hidden;
}
</style>