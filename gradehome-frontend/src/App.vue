<template>
  <v-app :theme="darkMode ? 'dark' : 'light'" :class="{ 'dark-mode': darkMode }">
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
      darkMode: false
    };
  },
  mounted() {
    // Initialize dark mode state
    this.darkMode = getDarkModePreference();

    // Listen for dark mode changes from any component
    window.addEventListener('darkModeChange', this.onDarkModeChange);

    // Apply dark mode to Vuetify
    this.updateVuetifyTheme();
  },
  beforeUnmount() {
    // Clean up event listener
    window.removeEventListener('darkModeChange', this.onDarkModeChange);
  },
  methods: {
    onDarkModeChange(event) {
      this.darkMode = event.detail.isDark;
      this.updateVuetifyTheme();
    },
    updateVuetifyTheme() {
      // If you need to do any additional Vuetify theme configuration
      // You can add it here
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
  --border-color: #e0e0e0;
  --shadow-color: rgba(123, 73, 255, 0.1);
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
  --border-color: #333333;
  --shadow-color: rgba(0, 0, 0, 0.25);
}
</style>