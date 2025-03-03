<template>
  <header class="app-header" :class="{ 'dashboard-header': isDashboard }">
    <!-- Clickable Logo -->
    <router-link to="/" class="logo">
      GradeGuard
    </router-link>

    <nav>
      <!-- Only show Login/Sign Up links if not in dashboard mode -->
      <template v-if="!isDashboard">
        <router-link
            v-if="mode === 'login'"
            :to="{ path: '/login', query: { mode: 'signup' } }"
            class="arrow-btn"
        >
          <span class="text">Sign Up</span>
          <svg
              width="16"
              height="16"
              viewBox="0 0 16 16"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
          >
            <path
                d="M4.66669 11.3334L11.3334 4.66669"
                stroke="white"
                stroke-width="1.33333"
                stroke-linecap="round"
                stroke-linejoin="round"
            />
            <path
                d="M4.66669 4.66669H11.3334V11.3334"
                stroke="white"
                stroke-width="1.33333"
                stroke-linecap="round"
                stroke-linejoin="round"
            />
          </svg>
        </router-link>

        <router-link
            v-else
            :to="{ path: '/login', query: { mode: 'login' } }"
            class="arrow-btn"
        >
          <span class="text">Login</span>
          <svg
              width="16"
              height="16"
              viewBox="0 0 16 16"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
          >
            <path
                d="M4.66669 11.3334L11.3334 4.66669"
                stroke="white"
                stroke-width="1.33333"
                stroke-linecap="round"
                stroke-linejoin="round"
            />
            <path
                d="M4.66669 4.66669H11.3334V11.3334"
                stroke="white"
                stroke-width="1.33333"
                stroke-linecap="round"
                stroke-linejoin="round"
            />
          </svg>
        </router-link>
      </template>

      <!-- Dashboard-specific controls -->
      <template v-if="isDashboard">
        <div class="dashboard-controls">
          <!-- User name/avatar could go here -->
          <div class="user-info" v-if="userName">
            <span class="welcome-text">Welcome, {{ userName }}</span>
          </div>
        </div>
      </template>

      <!-- Dark/Light Mode Toggle (visible on all screens) -->
      <button
          @click="toggleDarkMode"
          class="theme-toggle"
          aria-label="Toggle dark mode"
      >
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

      <!-- Logout Button (only visible in dashboard mode) -->
      <button v-if="isDashboard" @click="handleLogout" class="logout-btn">
        <span>Logout</span>
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
          <polyline points="16 17 21 12 16 7"></polyline>
          <line x1="21" y1="12" x2="9" y2="12"></line>
        </svg>
      </button>
    </nav>
  </header>
</template>

<script>
import { getDarkModePreference, setDarkModePreference, toggleDarkMode } from '@/services/darkModeService.js';

export default {
  name: "NavBar",
  props: {
    mode: {
      type: String,
      default: "login",
    },
    isMobile: {
      type: Boolean,
      default: false,
    },
    userName: {
      type: String,
      default: '',
    }
  },
  data() {
    return {
      darkMode: getDarkModePreference(),
    };
  },
  computed: {
    isDashboard() {
      return this.mode === 'dashboard';
    }
  },
  mounted() {
    // Initialize dark mode from stored preference
    this.darkMode = getDarkModePreference();

    // Listen for dark mode changes from other components
    window.addEventListener('darkModeChange', this.onDarkModeChange);
  },
  beforeUnmount() {
    // Clean up event listener
    window.removeEventListener('darkModeChange', this.onDarkModeChange);
  },
  methods: {
    toggleDarkMode() {
      this.darkMode = toggleDarkMode();
    },
    onDarkModeChange(event) {
      this.darkMode = event.detail.isDark;
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
/* Base header styles */
.app-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  width: 100%;
  z-index: 1000;
  transition: all 0.3s ease;
}

/* Dashboard-specific header styling */
.dashboard-header {
  background-color: var(--bg-light, #ffffff);
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

body.dark-mode .dashboard-header {
  background-color: var(--bg-dark, #1a1a2e);
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
}

/* Logo styles */
.logo {
  font-size: 1.8rem;
  font-weight: 700;
  text-decoration: none;
  color: var(--primary-dark, #512da8);
  transition: color 0.3s ease, transform 0.3s ease;
}

.logo:hover {
  color: var(--primary-color, #7b49ff);
  transform: scale(1.05);
}

body.dark-mode .logo {
  color: var(--primary-light, #b39ddb);
}

/* NavBar content */
nav {
  display: flex;
  align-items: center;
  gap: 1rem;
}

/* User info */
.user-info {
  margin-right: 1rem;
}

.welcome-text {
  font-weight: 500;
}

/* Arrow button styles */
.arrow-btn {
  font-size: 16px;
  font-weight: 600;
  background-color: var(--primary-dark, #512da8);
  color: white;
  text-decoration: none;
  padding: 0.6rem 1.8rem 0.6rem 1.2rem;
  border-radius: 99px;
  position: relative;
  border: none;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  transition: 0.4s ease;
}

.arrow-btn .text {
  line-height: 1;
  margin-right: 2rem;
  position: relative;
  z-index: 5;
}

.arrow-btn::before {
  content: "";
  background-color: var(--secondary-color, #b39ddb);
  width: 28px;
  height: 28px;
  border-radius: 99px;
  position: absolute;
  top: 50%;
  right: 10px;
  transform: translateY(-50%);
  transition: all 0.4s ease;
  z-index: 1;
}

.arrow-btn svg {
  width: 14px;
  height: 14px;
  position: absolute;
  right: 16px;
  top: 50%;
  transform: translateY(-50%) rotate(0deg);
  transform-origin: center;
  transition: 0.4s ease;
  z-index: 5;
}

.arrow-btn:hover svg {
  transform: translateY(-50%) rotate(45deg);
}

.arrow-btn:hover::before {
  width: 100%;
  height: 100%;
  right: 0;
}

/* Theme toggle button */
.theme-toggle {
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: transparent;
  color: var(--text-primary, #333333);
  width: 40px;
  height: 40px;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.3s ease;
}

.theme-toggle:hover {
  background-color: rgba(123, 73, 255, 0.1);
  transform: scale(1.1);
}

body.dark-mode .theme-toggle {
  color: var(--text-primary, #e0e0e0);
}

body.dark-mode .theme-toggle:hover {
  background-color: rgba(177, 156, 217, 0.2);
}

/* Logout button */
.logout-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background-color: var(--primary-color, #7b49ff);
  color: white;
  border: none;
  padding: 0.6rem 1.2rem;
  border-radius: 24px;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.3s ease;
}

.logout-btn:hover {
  background-color: var(--primary-dark, #512da8);
  transform: translateY(-2px);
}

.logout-btn svg {
  transition: transform 0.3s ease;
}

.logout-btn:hover svg {
  transform: translateX(3px);
}

/* Media queries for responsive design */
@media (max-width: 768px) {
  .app-header {
    padding: 0.8rem 1.5rem;
  }

  .logo {
    font-size: 1.6rem;
  }

  .welcome-text {
    display: none;
  }

  .logout-btn span {
    display: none;
  }

  .logout-btn {
    width: 40px;
    height: 40px;
    padding: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
  }
}
</style>