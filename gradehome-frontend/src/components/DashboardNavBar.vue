<template>
  <header class="dashboard-navbar">
    <div class="navbar-left">
      <div class="logo-container">
        <router-link to="/dashboard" class="logo">
          GradeGuard
        </router-link>
      </div>

      <div class="nav-links" v-if="!isMobile">
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
          <span class="user-name" v-if="!isMobile">{{ userName }}</span>
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

      <!-- Mobile menu toggle -->
      <button v-if="isMobile" @click="toggleMobileMenu" class="mobile-menu-toggle" aria-label="Toggle mobile menu">
        <svg v-if="!showMobileMenu" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <line x1="3" y1="12" x2="21" y2="12"></line>
          <line x1="3" y1="6" x2="21" y2="6"></line>
          <line x1="3" y1="18" x2="21" y2="18"></line>
        </svg>
        <svg v-else xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <line x1="18" y1="6" x2="6" y2="18"></line>
          <line x1="6" y1="6" x2="18" y2="18"></line>
        </svg>
      </button>
    </div>

    <!-- Mobile navigation menu -->
    <transition name="slide-down">
      <div v-if="isMobile && showMobileMenu" class="mobile-menu">
        <router-link to="/dashboard" class="mobile-nav-link" @click="showMobileMenu = false">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
            <polyline points="9 22 9 12 15 12 15 22"></polyline>
          </svg>
          <span>Dashboard</span>
        </router-link>

        <router-link to="/grades" class="mobile-nav-link" @click="showMobileMenu = false">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
            <polyline points="14 2 14 8 20 8"></polyline>
            <line x1="16" y1="13" x2="8" y2="13"></line>
            <line x1="16" y1="17" x2="8" y2="17"></line>
            <polyline points="10 9 9 9 8 9"></polyline>
          </svg>
          <span>Grades</span>
        </router-link>

        <router-link to="/calendar" class="mobile-nav-link" @click="showMobileMenu = false">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
            <line x1="16" y1="2" x2="16" y2="6"></line>
            <line x1="8" y1="2" x2="8" y2="6"></line>
            <line x1="3" y1="10" x2="21" y2="10"></line>
          </svg>
          <span>Calendar</span>
        </router-link>

        <router-link to="/settings" class="mobile-nav-link" @click="showMobileMenu = false">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="3"></circle>
            <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path>
          </svg>
          <span>Settings</span>
        </router-link>

        <div class="mobile-nav-divider"></div>

        <button class="mobile-nav-link logout-btn" @click="handleLogout">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
            <polyline points="16 17 21 12 16 7"></polyline>
            <line x1="21" y1="12" x2="9" y2="12"></line>
          </svg>
          <span>Logout</span>
        </button>
      </div>
    </transition>
  </header>
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
  },
  beforeUnmount() {
    // Clean up event listeners
    window.removeEventListener('darkModeChange', this.onDarkModeChange);
    document.removeEventListener('click', this.handleClickOutside);
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
      if (this.$refs.userDropdown && !this.$refs.userDropdown.contains(event.target)) {
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
};
</script>

<style scoped>
.dashboard-navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: var(--bg-light);
  border-bottom: 1px solid var(--border-color);
  padding: 0.75rem 1.5rem;
  box-shadow: var(--shadow-sm);
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  transition: background-color var(--transition-speed) ease,
  border-color var(--transition-speed) ease,
  box-shadow var(--transition-speed) ease;
}

.navbar-left {
  display: flex;
  align-items: center;
}

.logo-container {
  margin-right: 2rem;
}

.logo {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--primary-color);
  text-decoration: none;
  transition: color var(--transition-speed) ease,
  transform var(--transition-speed) ease;
}

.logo:hover {
  color: var(--primary-dark);
  transform: scale(1.05);
}

.nav-links {
  display: flex;
  gap: 1rem;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  color: var(--text-secondary);
  text-decoration: none;
  border-radius: var(--border-radius);
  transition: background-color var(--transition-speed) ease,
  color var(--transition-speed) ease;
}

.nav-link:hover, .nav-link.active {
  background-color: rgba(123, 73, 255, 0.1);
  color: var(--primary-color);
}

.navbar-right {
  display: flex;
  align-items: center;
  gap: 1rem;
}

/* Theme toggle button */
.theme-toggle {
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: transparent;
  color: var(--text-primary);
  width: 40px;
  height: 40px;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  transition: background-color var(--transition-speed) ease,
  transform var(--transition-speed) ease;
}

.theme-toggle:hover {
  background-color: rgba(123, 73, 255, 0.1);
  transform: scale(1.1);
}

/* User dropdown */
.user-dropdown {
  position: relative;
}

.user-avatar {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background-color: transparent;
  border: none;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: var(--border-radius);
  transition: background-color var(--transition-speed) ease;
}

.user-avatar:hover {
  background-color: rgba(123, 73, 255, 0.1);
}

.avatar-placeholder {
  width: 32px;
  height: 32px;
  background-color: var(--primary-color);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
}

.user-name {
  font-weight: 500;
  color: var(--text-primary);
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  right: 0;
  width: 280px;
  background-color: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  box-shadow: var(--shadow-md);
  z-index: 1000;
  margin-top: 0.5rem;
  animation: fadeIn 0.2s ease;
}

.dropdown-header {
  padding: 1rem;
  border-bottom: 1px solid var(--border-color);
}

.user-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.avatar img, .avatar .avatar-placeholder {
  width: 40px;
  height: 40px;
}

.user-details {
  flex: 1;
}

.user-details .user-name {
  font-weight: 600;
  margin-bottom: 0.25rem;
}

.user-details .user-email {
  font-size: 0.85rem;
  color: var(--text-secondary);
}

.dropdown-divider {
  height: 1px;
  background-color: var(--border-color);
  margin: 0.5rem 0;
}

.dropdown-items {
  padding: 0.5rem;
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  color: var(--text-primary);
  text-decoration: none;
  border-radius: var(--border-radius);
  transition: background-color var(--transition-speed) ease;
  cursor: pointer;
  border: none;
  background: none;
  width: 100%;
  text-align: left;
  font-family: "Montserrat", sans-serif;
  font-size: 0.9rem;
}

.dropdown-item:hover {
  background-color: rgba(123, 73, 255, 0.1);
}

.dropdown-item.logout-btn {
  color: var(--error-color);
}

.dropdown-item.logout-btn:hover {
  background-color: rgba(244, 67, 54, 0.1);
}

/* Mobile menu */
.mobile-menu-toggle {
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: transparent;
  color: var(--text-primary);
  width: 40px;
  height: 40px;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  transition: background-color var(--transition-speed) ease;
}

.mobile-menu-toggle:hover {
  background-color: rgba(123, 73, 255, 0.1);
}

.mobile-menu {
  position: fixed;
  top: 60px; /* Height of the navbar */
  left: 0;
  right: 0;
  background-color: var(--bg-light);
  border-bottom: 1px solid var(--border-color);
  box-shadow: var(--shadow-md);
  padding: 1rem;
  z-index: 999;
}

.mobile-nav-link {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.875rem 1rem;
  color: var(--text-primary);
  text-decoration: none;
  border-radius: var(--border-radius);
  transition: background-color var(--transition-speed) ease;
  margin-bottom: 0.5rem;
  cursor: pointer;
  border: none;
  background: none;
  width: 100%;
  text-align: left;
  font-family: "Montserrat", sans-serif;
  font-size: 1rem;
}

.mobile-nav-link:hover {
  background-color: rgba(123, 73, 255, 0.1);
}

.mobile-nav-link.logout-btn {
  color: var(--error-color);
}

.mobile-nav-divider {
  height: 1px;
  background-color: var(--border-color);
  margin: 0.5rem 0 1rem;
}

/* Slide down animation for mobile menu */
.slide-down-enter-active,
.slide-down-leave-active {
  transition: transform var(--transition-speed) ease,
  opacity var(--transition-speed) ease;
}

.slide-down-enter-from,
.slide-down-leave-to {
  transform: translateY(-20px);
  opacity: 0;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .dashboard-navbar {
    padding: 0.5rem 1rem;
  }

  .logo {
    font-size: 1.3rem;
  }
}
</style>