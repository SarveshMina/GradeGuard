<template>
  <div>
    <!-- Desktop Navbar at the top -->
    <header class="dashboard-navbar" v-if="!isMobile">
      <div class="navbar-left">
        <div class="logo-container">
          <router-link to="/dashboard" class="logo">
            GradeGuard
          </router-link>
        </div>

        <div class="nav-links">
          <router-link to="/dashboard" class="nav-link" active-class="active">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
              <polyline points="9 22 9 12 15 12 15 22"></polyline>
            </svg>
            <span>Dashboard</span>
          </router-link>

          <router-link to="/grades" class="nav-link" active-class="active">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
              <polyline points="14 2 14 8 20 8"></polyline>
              <line x1="16" y1="13" x2="8" y2="13"></line>
              <line x1="16" y1="17" x2="8" y2="17"></line>
              <polyline points="10 9 9 9 8 9"></polyline>
            </svg>
            <span>Grades</span>
          </router-link>

          <router-link to="/calendar" class="nav-link" active-class="active">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
              <line x1="16" y1="2" x2="16" y2="6"></line>
              <line x1="8" y1="2" x2="8" y2="6"></line>
              <line x1="3" y1="10" x2="21" y2="10"></line>
            </svg>
            <span>Calendar</span>
          </router-link>

          <router-link to="/settings" class="nav-link" active-class="active">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="3"></circle>
              <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path>
            </svg>
            <span>Settings</span>
          </router-link>
        </div>
      </div>

      <div class="navbar-right">
        <!-- Dark mode toggle -->
        <button @click="toggleDarkMode" class="theme-toggle" aria-label="Toggle dark mode">
          <svg v-if="darkMode" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
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
          <svg v-else xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
          </svg>
        </button>

        <!-- User dropdown -->
        <div class="user-dropdown" ref="userDropdown">
          <button class="user-avatar" @click="toggleUserMenu">
            <img v-if="userAvatar" :src="userAvatar" alt="User avatar" />
            <div v-else class="avatar-placeholder">{{ userInitials }}</div>
            <span class="user-name">{{ userName }}</span>
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="6 9 12 15 18 9"></polyline>
            </svg>
          </button>

          <div class="dropdown-menu" v-if="showUserMenu">
            <div class="dropdown-header">
              <div class="user-info">
                <div class="avatar">
                  <img v-if="userAvatar" :src="userAvatar" alt="User avatar" />
                  <div v-else class="avatar-placeholder">{{ userInitials }}</div>
                </div>
                <div class="user-details">
                  <div class="user-name">{{ userName }}</div>
                  <div class="user-email">{{ userEmail }}</div>
                </div>
              </div>
            </div>

            <div class="dropdown-divider"></div>

            <div class="dropdown-items">
              <router-link to="/profile" class="dropdown-item">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                  <circle cx="12" cy="7" r="4"></circle>
                </svg>
                <span>My Profile</span>
              </router-link>

              <router-link to="/settings" class="dropdown-item">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <circle cx="12" cy="12" r="3"></circle>
                  <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path>
                </svg>
                <span>Account Settings</span>
              </router-link>

              <button class="dropdown-item logout-btn" @click="handleLogout">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
                  <polyline points="16 17 21 12 16 7"></polyline>
                  <line x1="21" y1="12" x2="9" y2="12"></line>
                </svg>
                <span>Logout</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </header>

    <!-- Mobile Bottom Navbar -->
    <div v-if="isMobile" class="mobile-bottom-navbar">
      <!-- Dark mode toggle removed from here since we moved it to the top bar -->

      <!-- Mobile Top Logo Bar -->
      <div class="mobile-top-bar">
        <div class="mobile-logo">
          <router-link to="/dashboard">GradeGuard</router-link>
        </div>
        <div class="mobile-controls">
          <!-- Dark mode toggle moved inside top bar -->
          <button @click="toggleDarkMode" class="mobile-theme-toggle" aria-label="Toggle dark mode">
            <svg v-if="darkMode" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
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
            <svg v-else xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
            </svg>
          </button>
          <div class="mobile-profile" @click="toggleUserMenu">
            <img v-if="userAvatar" :src="userAvatar" alt="User avatar" />
            <div v-else class="avatar-placeholder">{{ userInitials }}</div>
          </div>
        </div>

        <!-- Mobile user dropdown -->
        <div class="mobile-dropdown-menu" v-if="showUserMenu">
          <div class="mobile-dropdown-header">
            <div class="user-info">
              <div class="avatar">
                <img v-if="userAvatar" :src="userAvatar" alt="User avatar" />
                <div v-else class="avatar-placeholder">{{ userInitials }}</div>
              </div>
              <div class="user-details">
                <div class="user-name">{{ userName }}</div>
                <div class="user-email">{{ userEmail }}</div>
              </div>
            </div>
          </div>

          <div class="dropdown-divider"></div>

          <div class="mobile-dropdown-items">
            <router-link to="/profile" class="mobile-dropdown-item" @click="showUserMenu = false">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                <circle cx="12" cy="7" r="4"></circle>
              </svg>
              <span>My Profile</span>
            </router-link>

            <router-link to="/settings" class="mobile-dropdown-item" @click="showUserMenu = false">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="3"></circle>
                <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path>
              </svg>
              <span>Account Settings</span>
            </router-link>

            <button class="mobile-dropdown-item logout-btn" @click="handleLogout">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
                <polyline points="16 17 21 12 16 7"></polyline>
                <line x1="21" y1="12" x2="9" y2="12"></line>
              </svg>
              <span>Logout</span>
            </button>
          </div>
        </div>
      </div>

      <!-- Bottom Navigation Bar -->
      <nav class="bottom-nav">
        <router-link to="/dashboard" class="bottom-nav-item" active-class="active">
          <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
            <polyline points="9 22 9 12 15 12 15 22"></polyline>
          </svg>
          <span>Home</span>
        </router-link>

        <router-link to="/grades" class="bottom-nav-item" active-class="active">
          <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
            <polyline points="14 2 14 8 20 8"></polyline>
            <line x1="16" y1="13" x2="8" y2="13"></line>
            <line x1="16" y1="17" x2="8" y2="17"></line>
            <polyline points="10 9 9 9 8 9"></polyline>
          </svg>
          <span>Grades</span>
        </router-link>

        <router-link to="/calendar" class="bottom-nav-item" active-class="active">
          <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
            <line x1="16" y1="2" x2="16" y2="6"></line>
            <line x1="8" y1="2" x2="8" y2="6"></line>
            <line x1="3" y1="10" x2="21" y2="10"></line>
          </svg>
          <span>Calendar</span>
        </router-link>

        <router-link to="/settings" class="bottom-nav-item" active-class="active">
          <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="3"></circle>
            <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path>
          </svg>
          <span>Settings</span>
        </router-link>
      </nav>
    </div>
  </div>
</template>

<script>
import { getDarkModePreference, toggleDarkMode } from '@/services/darkModeService.js';

export default {
  name: "DashboardNavBar",
  props: {
    userName: {
      type: String,
      default: 'User',
    },
    userEmail: {
      type: String,
      default: 'user@example.com',
    },
    userAvatar: {
      type: String,
      default: '',
    },
    isMobile: {
      type: Boolean,
      default: false,
    }
  },
  data() {
    return {
      darkMode: getDarkModePreference(),
      showUserMenu: false,
      showMobileMenu: false,
    };
  },
  computed: {
    userInitials() {
      if (!this.userName) return 'U';

      const names = this.userName.split(' ');
      if (names.length === 1) return names[0].charAt(0).toUpperCase();

      return (names[0].charAt(0) + names[names.length - 1].charAt(0)).toUpperCase();
    }
  },
  mounted() {
    // Initialize dark mode state
    this.darkMode = getDarkModePreference();

    // Listen for dark mode changes from other components
    window.addEventListener('darkModeChange', this.onDarkModeChange);

    // Add click outside listener for user dropdown
    document.addEventListener('click', this.handleClickOutside);

    // Check if body has mobile-padding class
    if (this.isMobile) {
      document.body.classList.add('mobile-padding-bottom');
    } else {
      document.body.classList.remove('mobile-padding-bottom');
    }
  },
  beforeUnmount() {
    // Clean up event listeners
    window.removeEventListener('darkModeChange', this.onDarkModeChange);
    document.removeEventListener('click', this.handleClickOutside);
    document.body.classList.remove('mobile-padding-bottom');
  },
  methods: {
    toggleDarkMode() {
      this.darkMode = toggleDarkMode();
    },
    onDarkModeChange(event) {
      this.darkMode = event.detail.isDark;
    },
    toggleUserMenu() {
      this.showUserMenu = !this.showUserMenu;
    },
    toggleMobileMenu() {
      this.showMobileMenu = !this.showMobileMenu;
    },
    handleClickOutside(event) {
      // For desktop dropdown
      if (this.$refs.userDropdown && !this.$refs.userDropdown.contains(event.target)) {
        this.showUserMenu = false;
      }

      // For mobile dropdown (ensure click outside also closes mobile dropdown)
      if (this.isMobile && this.showUserMenu &&
          !event.target.closest('.mobile-profile') &&
          !event.target.closest('.mobile-dropdown-menu')) {
        this.showUserMenu = false;
      }
    },
    handleLogout() {
      // Clear local storage or cookies used for authentication
      localStorage.removeItem("user");
      localStorage.removeItem("token");

      // Emit event so parent components can react
      this.$emit('logout');

      // Redirect to login page
      this.$router.push('/login');
    },
  },
  watch: {
    // Watch for mobile changes to update body class
    isMobile(newVal) {
      if (newVal) {
        document.body.classList.add('mobile-padding-bottom');
      } else {
        document.body.classList.remove('mobile-padding-bottom');
      }
    }
  }
};
</script>

<style scoped>
/* Dashboard Navbar - Enhanced Styles */
:root {
  --primary-color: #673ab7;
  --primary-dark: #512da8;
  --primary-light: #9575cd;
  --primary-color-transparent: rgba(103, 58, 183, 0.15);
  --text-primary: #333333;
  --text-secondary: #666666;
  --text-muted: #888888;
  --border-color: #e0e0e0;
  --bg-light: #ffffff;
  --bg-card: #ffffff;
  --bg-input: #f5f7fa;
  --bg-muted: #f0f0f0;
  --bg-hover: #f9f9f9;
  --success-color: #4caf50;
  --warning-color: #ff9800;
  --error-color: #f44336;
  --transition-speed: 0.3s;
  --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 16px rgba(0, 0, 0, 0.1);
  --shadow-lg: 0 8px 24px rgba(0, 0, 0, 0.12);
  --border-radius: 12px;
  --bottom-nav-height: 64px;
}

.dark-mode {
  --text-primary: #f5f7fa;
  --text-secondary: #d0d0d0;
  --text-muted: #a0a0a0;
  --border-color: #3f4156;
  --bg-light: #232535;
  --bg-card: #2a2d3e;
  --bg-input: #1e2030;
  --bg-muted: #323546;
  --bg-hover: #3c4052;
  --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.2);
  --shadow-md: 0 4px 16px rgba(0, 0, 0, 0.3);
  --shadow-lg: 0 8px 24px rgba(0, 0, 0, 0.4);
}

/* Body adjustment for mobile bottom nav */
body.mobile-padding-bottom {
  padding-bottom: var(--bottom-nav-height);
  padding-top: 60px; /* Adjust for mobile top bar */
}

/* Support for iOS safe area */
@supports (padding: max(0px)) {
  body.mobile-padding-bottom {
    padding-bottom: max(var(--bottom-nav-height), env(safe-area-inset-bottom, var(--bottom-nav-height)));
  }
}

/* ==================== DESKTOP NAVBAR STYLES ==================== */
.dashboard-navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: var(--bg-light);
  border-bottom: 1px solid var(--border-color);
  padding: 0.75rem 2rem;
  box-shadow: var(--shadow-sm);
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  transition: all var(--transition-speed) ease;
  height: 70px;
}

.dark-mode .dashboard-navbar {
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.2);
}

.dashboard-navbar::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 3px;
  background: linear-gradient(90deg, var(--primary-color), var(--primary-light));
  opacity: 0;
  transition: opacity var(--transition-speed) ease;
}

.dashboard-navbar:hover::before {
  opacity: 1;
}

.navbar-left {
  display: flex;
  align-items: center;
}

.logo-container {
  margin-right: 2.5rem;
  position: relative;
}

.logo {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--primary-color);
  text-decoration: none;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  display: inline-block;
  position: relative;
}

.logo::after {
  content: '';
  position: absolute;
  bottom: -4px;
  left: 0;
  width: 100%;
  height: 2px;
  background: linear-gradient(90deg, var(--primary-color), var(--primary-light));
  transform: scaleX(0);
  transform-origin: right;
  transition: transform 0.3s ease;
}

.logo:hover {
  color: var(--primary-dark);
  transform: scale(1.05);
  text-shadow: 0 2px 10px rgba(103, 58, 183, 0.2);
}

.logo:hover::after {
  transform: scaleX(1);
  transform-origin: left;
}

.nav-links {
  display: flex;
  gap: 0.75rem;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.7rem 1.2rem;
  color: var(--text-secondary);
  text-decoration: none;
  border-radius: var(--border-radius);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  font-weight: 500;
}

.nav-link::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, rgba(103, 58, 183, 0.05), rgba(103, 58, 183, 0.15));
  border-radius: var(--border-radius);
  transform: translateX(-100%);
  transition: transform 0.5s ease;
  z-index: -1;
}

.nav-link:hover::before {
  transform: translateX(0);
}

.nav-link:hover {
  color: var(--primary-color);
  transform: translateY(-2px);
}

.nav-link.active {
  background-color: var(--primary-color-transparent);
  color: var(--primary-color);
  box-shadow: 0 4px 8px rgba(103, 58, 183, 0.1);
  font-weight: 600;
}

.nav-link svg {
  transition: transform 0.3s ease;
}

.nav-link:hover svg {
  transform: scale(1.2);
}

.navbar-right {
  display: flex;
  align-items: center;
  gap: 1.25rem;
}

/* Theme toggle button */
.theme-toggle {
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--bg-muted);
  color: var(--text-primary);
  width: 42px;
  height: 42px;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  box-shadow: var(--shadow-sm);
  position: relative;
  overflow: hidden;
}

.theme-toggle::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle, rgba(103, 58, 183, 0.2) 0%, rgba(255, 255, 255, 0) 70%);
  transform: scale(0);
  transition: transform 0.4s ease;
}

.theme-toggle:hover::before {
  transform: scale(1.5);
}

.theme-toggle:hover {
  background-color: var(--bg-hover);
  transform: scale(1.1) rotate(15deg);
  box-shadow: 0 6px 15px rgba(103, 58, 183, 0.2);
  color: var(--primary-color);
}

.theme-toggle svg {
  transition: transform 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55);
  position: relative;
  z-index: 1;
}

.theme-toggle:hover svg {
  transform: rotate(-15deg);
}

/* User dropdown */
.user-dropdown {
  position: relative;
}

.user-avatar {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  background-color: var(--bg-muted);
  border: none;
  cursor: pointer;
  padding: 0.6rem 1rem 0.6rem 0.6rem;
  border-radius: 50px;
  transition: all 0.3s ease;
  box-shadow: var(--shadow-sm);
}

.user-avatar:hover {
  background-color: var(--primary-color-transparent);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(103, 58, 183, 0.15);
}

.user-avatar img {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid transparent;
  transition: all 0.3s ease;
}

.user-avatar:hover img {
  border-color: var(--primary-color);
}

.avatar-placeholder {
  width: 36px;
  height: 36px;
  background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-dark) 100%);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 0.9rem;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(103, 58, 183, 0.2);
}

.user-avatar:hover .avatar-placeholder {
  transform: scale(1.05);
  box-shadow: 0 4px 12px rgba(103, 58, 183, 0.3);
}

.user-name {
  font-weight: 500;
  color: var(--text-primary);
  transition: color 0.3s ease;
}

.user-avatar:hover .user-name {
  color: var(--primary-color);
}

.user-avatar svg {
  color: var(--text-muted);
  transition: transform 0.3s ease;
}

.user-avatar:hover svg {
  color: var(--primary-color);
  transform: translateY(3px);
}

.dropdown-menu {
  position: absolute;
  top: calc(100% + 8px);
  right: 0;
  width: 280px;
  background-color: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  box-shadow: var(--shadow-lg);
  z-index: 1000;
  overflow: hidden;
  animation: fadeInDown 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  transform-origin: top right;
}

@keyframes fadeInDown {
  0% {
    opacity: 0;
    transform: translateY(-10px) scale(0.95);
  }
  100% {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.dropdown-header {
  padding: 1.25rem;
  border-bottom: 1px solid var(--border-color);
  background: linear-gradient(to bottom, var(--bg-hover), var(--bg-card));
}

.user-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.avatar img {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid var(--primary-color);
  box-shadow: 0 2px 8px rgba(103, 58, 183, 0.2);
}

.avatar .avatar-placeholder {
  width: 48px;
  height: 48px;
  font-size: 1.1rem;
}

.user-details {
  flex: 1;
}

.user-details .user-name {
  font-weight: 600;
  margin-bottom: 0.25rem;
  color: var(--text-primary);
  font-size: 1.1rem;
}

.user-details .user-email {
  font-size: 0.85rem;
  color: var(--text-secondary);
}

.dropdown-divider {
  height: 1px;
  background-color: var(--border-color);
  margin: 0;
}

.dropdown-items {
  padding: 0.75rem;
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.9rem 1.1rem;
  color: var(--text-primary);
  text-decoration: none;
  border-radius: var(--border-radius);
  transition: all 0.3s ease;
  cursor: pointer;
  border: none;
  background: none;
  width: 100%;
  text-align: left;
  font-family: inherit;
  font-size: 0.95rem;
  position: relative;
  overflow: hidden;
}

.dropdown-item::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, rgba(103, 58, 183, 0.05), rgba(103, 58, 183, 0));
  border-radius: var(--border-radius);
  transform: translateX(-100%);
  transition: transform 0.5s ease;
  z-index: -1;
}

.dropdown-item:hover::before {
  transform: translateX(0);
}

.dropdown-item:hover {
  background-color: var(--primary-color-transparent);
  transform: translateX(5px);
}

.dropdown-item svg {
  transition: transform 0.3s ease;
  color: var(--text-secondary);
}

.dropdown-item:hover svg {
  transform: scale(1.15);
  color: var(--primary-color);
}

.dropdown-item.logout-btn {
  color: var(--error-color);
}

.dropdown-item.logout-btn:hover {
  background-color: rgba(244, 67, 54, 0.1);
}

.dropdown-item.logout-btn svg {
  color: var(--error-color);
}

/* ==================== MOBILE BOTTOM NAVBAR STYLES ==================== */
.mobile-bottom-navbar {
  position: fixed;
  width: 100%;
  z-index: 1000;
}

/* Mobile Theme Toggle Button */
.mobile-theme-toggle {
  position: fixed;
  top: 0.75rem;
  right: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--bg-muted);
  color: var(--text-primary);
  width: 40px;
  height: 40px;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: var(--shadow-sm);
  z-index: 1010;
}

.mobile-theme-toggle:active {
  transform: scale(0.9);
}

/* Mobile Top Bar */
.mobile-top-bar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 1rem;
  background-color: var(--bg-light);
  border-bottom: 1px solid var(--border-color);
  box-shadow: var(--shadow-sm);
  z-index: 1000;
  height: 60px;
}

.mobile-top-bar::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 3px;
  background: linear-gradient(90deg, var(--primary-color), var(--primary-light));
}

.mobile-logo {
  margin-left: 0.5rem;
}

.mobile-logo a {
  font-size: 1.4rem;
  font-weight: 700;
  color: var(--primary-color);
  text-decoration: none;
  letter-spacing: -0.5px;
}

/* Mobile controls container for theme toggle and profile */
.mobile-controls {
  display: flex;
  align-items: center;
  gap: 1rem; /* Ensure at least 1rem gap between toggle and profile */
}

.mobile-profile {
  width: 40px;
  height: 40px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background-color: var(--bg-muted);
  box-shadow: var(--shadow-sm);
  position: relative;
  z-index: 1010;
  transition: transform 0.3s ease;
}

.mobile-profile:active {
  transform: scale(0.95);
}

.mobile-profile img {
  width: 38px;
  height: 38px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid var(--primary-color);
}

.mobile-profile .avatar-placeholder {
  width: 38px;
  height: 38px;
  font-size: 1rem;
}

/* Mobile Dropdown Menu */
.mobile-dropdown-menu {
  position: fixed;
  top: 60px;
  right: 0;
  width: 80%;
  max-width: 300px;
  background-color: var(--bg-card);
  border-left: 1px solid var(--border-color);
  border-bottom: 1px solid var(--border-color);
  border-bottom-left-radius: var(--border-radius);
  box-shadow: var(--shadow-lg);
  z-index: 1000;
  overflow: hidden;
  animation: slideInRight 0.3s ease;
  height: auto;
  max-height: calc(100vh - 60px - var(--bottom-nav-height));
  overflow-y: auto;
}

@keyframes slideInRight {
  0% {
    transform: translateX(100%);
    opacity: 0;
  }
  100% {
    transform: translateX(0);
    opacity: 1;
  }
}

.mobile-dropdown-header {
  padding: 1.25rem;
  border-bottom: 1px solid var(--border-color);
  background: linear-gradient(to bottom, var(--bg-hover), var(--bg-card));
}

.mobile-dropdown-items {
  padding: 0.75rem;
}

.mobile-dropdown-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem;
  color: var(--text-primary);
  text-decoration: none;
  border-radius: var(--border-radius);
  transition: all 0.3s ease;
  cursor: pointer;
  border: none;
  background: none;
  width: 100%;
  text-align: left;
  font-family: inherit;
  font-size: 1rem;
  margin-bottom: 0.5rem;
}

.mobile-dropdown-item:active {
  background-color: var(--primary-color-transparent);
  transform: scale(0.98);
}

.mobile-dropdown-item svg {
  color: var(--text-secondary);
}

.mobile-dropdown-item.logout-btn {
  color: var(--error-color);
}

.mobile-dropdown-item.logout-btn svg {
  color: var(--error-color);
}

/* Bottom Navigation Bar */
.bottom-nav {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  display: flex;
  justify-content: space-around;
  align-items: center;
  background-color: var(--bg-card);
  border-top: 1px solid var(--border-color);
  box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.05);
  height: var(--bottom-nav-height);
  padding: 0 0.5rem;
  padding-bottom: env(safe-area-inset-bottom, 0);
  z-index: 1000;
}

.dark-mode .bottom-nav {
  box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.2);
}

.bottom-nav-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.25rem;
  color: var(--text-secondary);
  text-decoration: none;
  padding: 0.5rem;
  border-radius: 12px;
  transition: all 0.3s ease;
  flex: 1;
  text-align: center;
  height: 100%;
  position: relative;
}

.bottom-nav-item span {
  font-size: 0.85rem;
  font-weight: 500;
  transition: all 0.3s ease;
}

.bottom-nav-item svg {
  transition: all 0.3s ease;
}

.bottom-nav-item::before {
  content: '';
  position: absolute;
  bottom: 8px;
  left: 50%;
  transform: translateX(-50%) scale(0);
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background-color: var(--primary-color);
  transition: all 0.3s ease;
  opacity: 0;
}

.bottom-nav-item:active {
  transform: scale(0.95);
}

.bottom-nav-item.active {
  color: var(--primary-color);
}

.bottom-nav-item.active::before {
  transform: translateX(-50%) scale(1);
  opacity: 1;
  bottom: 2px;
}

.bottom-nav-item.active svg {
  transform: translateY(-4px);
  filter: drop-shadow(0 3px 5px rgba(103, 58, 183, 0.3));
}

.bottom-nav-item.active span {
  transform: translateY(-2px);
  font-weight: 600;
}

/* Additional mobile styles for Capacitor/iOS */
@supports (padding: max(0px)) {
  .mobile-top-bar {
    padding-top: max(0.75rem, env(safe-area-inset-top, 0.75rem));
    height: calc(60px + env(safe-area-inset-top, 0px));
  }

  .mobile-dropdown-menu {
    top: calc(60px + env(safe-area-inset-top, 0px));
    height: calc(100vh - 60px - var(--bottom-nav-height) - env(safe-area-inset-top, 0px) - env(safe-area-inset-bottom, 0px));
  }
}

@media (max-width: 368px) {
  .bottom-nav-item span {
    font-size: 0.75rem;
  }

  .mobile-logo a {
    font-size: 1.2rem;
  }
}
</style>