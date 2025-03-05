<template>
  <v-app :theme="darkMode ? 'dark' : 'light'" :class="{ 'dark-mode': darkMode, 'high-contrast': highContrast, 'font-size-small': fontSize === 'small', 'font-size-large': fontSize === 'large' }">
    <!-- Our toast manager sits on top, so it can show notifications any time -->
    <ToastManager />
    <router-view />
  </v-app>
</template>

<script>
import ToastManager from '@/components/ToastManager.vue'
import { getDarkModePreference } from '@/services/darkModeService.js';

export default {
  name: 'App',
  components: {
    ToastManager
  },
  data() {
    return {
      darkMode: false,
      highContrast: false,
      fontSize: 'medium',
      keyboardShortcutsEnabled: true
    };
  },
  mounted() {
    // Initialize dark mode state
    this.darkMode = getDarkModePreference();

    // Initialize other settings from localStorage
    this.loadSettings();

    // Listen for dark mode changes from any component
    window.addEventListener('darkModeChange', this.onDarkModeChange);

    // Listen for settings changes
    window.addEventListener('settingsChange', this.onSettingsChange);

    // Listen for keyboard shortcuts
    window.addEventListener('keydown', this.handleKeyboardShortcuts);

    // Apply dark mode to Vuetify
    this.updateVuetifyTheme();
  },
  beforeUnmount() {
    // Clean up event listeners
    window.removeEventListener('darkModeChange', this.onDarkModeChange);
    window.removeEventListener('settingsChange', this.onSettingsChange);
    window.removeEventListener('keydown', this.handleKeyboardShortcuts);
  },
  methods: {
    onDarkModeChange(event) {
      this.darkMode = event.detail.isDark;
      this.updateVuetifyTheme();
    },
    onSettingsChange(event) {
      // Handle settings change events from components
      const { setting, value } = event.detail;

      switch(setting) {
        case 'highContrast':
          this.highContrast = value;
          break;
        case 'fontSize':
          this.fontSize = value;
          break;
        case 'keyboardShortcuts':
          this.keyboardShortcutsEnabled = value;
          break;
      }
    },
    loadSettings() {
      // Load settings from localStorage or defaults
      try {
        const savedSettings = localStorage.getItem('appSettings');
        if (savedSettings) {
          const settings = JSON.parse(savedSettings);
          this.highContrast = settings.appearance?.highContrast || false;
          this.fontSize = settings.appearance?.fontSize || 'medium';
          this.keyboardShortcutsEnabled = settings.accessibility?.keyboardShortcuts !== false;
        }
      } catch (error) {
        console.error('Error loading settings:', error);
      }
    },
    updateVuetifyTheme() {
      // If you need to do any additional Vuetify theme configuration
      // You can add it here
    },
    handleKeyboardShortcuts(event) {
      // Only handle shortcuts if enabled in settings
      if (!this.keyboardShortcutsEnabled) return;

      // Handle Alt key combinations
      if (event.altKey) {
        switch(event.key.toLowerCase()) {
          case 'd':
            this.$router.push('/dashboard');
            break;
          case 'c':
            this.$router.push('/calendar');
            break;
          case 'g':
            this.$router.push('/grades');
            break;
          case 's':
            this.$router.push('/settings');
            break;
          case 'n':
            // Trigger create event if on calendar page
            if (this.$route.path === '/calendar') {
              window.dispatchEvent(new CustomEvent('createNewEvent'));
            }
            break;
        }
      }
    }
  }
};
</script>

<style>
/* Add transition for smooth dark mode toggle */
.v-application {
  transition: background-color 0.3s ease, color 0.3s ease;
}

/* Define CSS variables that can be used throughout the app */
:root {
  /* Light theme colors - these will be overridden in dark mode */
  --primary-color: #7b49ff;
  --primary-light: #9170ff;
  --primary-dark: #512da8;
  --secondary-color: #b39ddb;
  --text-primary: #333333;
  --text-secondary: #666666;
  --bg-light: #ffffff;
  --bg-card: #ffffff;
  --bg-input: #f5f5f8;
  --bg-hover: #f0f0f5;
  --border-color: #e0e0e0;
  --border-color-light: #eeeeee;
  --shadow-color: rgba(123, 73, 255, 0.1);
  --shadow-sm: 0 2px 4px rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 8px rgba(0, 0, 0, 0.08);
  --shadow-lg: 0 8px 16px rgba(0, 0, 0, 0.1);
  --error-color: #f44336;
  --success-color: #4caf50;
  --warning-color: #ff9800;
  --border-radius: 8px;
  --border-radius-lg: 12px;
  --transition-speed: 0.3s;
  --font-size-base: 16px;
}

/* Dark mode overrides */
.dark-mode {
  --primary-color: #9170ff;
  --primary-light: #b39ddb;
  --primary-dark: #5e35b1;
  --secondary-color: #d1c4e9;
  --text-primary: #e0e0e0;
  --text-secondary: #b0b0b0;
  --bg-light: #121212;
  --bg-card: #1e1e30;
  --bg-input: #2a2a3c;
  --bg-hover: #2c2c40;
  --border-color: #333333;
  --border-color-light: #333333;
  --shadow-color: rgba(0, 0, 0, 0.25);
}

/* High contrast mode overrides */
.high-contrast {
  --text-primary: #000000;
  --text-secondary: #222222;
  --bg-light: #ffffff;
  --bg-card: #ffffff;
  --bg-input: #ffffff;
  --border-color: #000000;
  --border-radius: 4px;
  --border-radius-lg: 4px;
  --shadow-sm: none;
  --shadow-md: none;
  --shadow-lg: none;
}

.dark-mode.high-contrast {
  --text-primary: #ffffff;
  --text-secondary: #dddddd;
  --bg-light: #000000;
  --bg-card: #000000;
  --bg-input: #111111;
  --border-color: #ffffff;
}

/* Font size adjustments */
.font-size-small {
  --font-size-base: 14px;
}

.font-size-large {
  --font-size-base: 18px;
}

/* Base font size */
html {
  font-size: var(--font-size-base);
}

/* Additional accessibility styles */
.focus-mode .dashboard-sidebar,
.focus-mode .nav-links a:not(.active) {
  opacity: 0.5;
  transition: opacity 0.3s ease;
}

.focus-mode .dashboard-sidebar:hover,
.focus-mode .nav-links a:hover {
  opacity: 1;
}

/* Keyboard focus styles for accessibility */
*:focus {
  outline: 2px solid var(--primary-color);
  outline-offset: 2px;
}

.high-contrast *:focus {
  outline: 3px solid #000000;
  outline-offset: 2px;
}

.dark-mode.high-contrast *:focus {
  outline: 3px solid #ffffff;
  outline-offset: 2px;
}
</style>