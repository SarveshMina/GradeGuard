// src/main.js
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './style.css'  // your global styles
import vuetify from './plugins/vuetify'
import { setupAxios } from './plugins/axios'
import { initDarkMode } from './services/darkModeService'
import { authService } from './services/authService'

// Import the default VCalendar stylesheet
import 'v-calendar/style.css'

// Import VCalendar
import VCalendar from 'v-calendar'

// Set up enhanced axios with fallback auth mechanisms
setupAxios()

// Add navigation guard for authentication
router.beforeEach(async (to, from, next) => {
  console.log(`Navigation from ${from.path} to ${to.path}`);
  
  // Check if route requires authentication
  if (to.matched.some(record => record.meta.requiresAuth)) {
    try {
      console.log('Route requires auth, checking authentication');
      const isAuthenticated = await authService.isAuthenticated();

      if (!isAuthenticated) {
        // Not authenticated, redirect to login with a return URL
        console.log('Not authenticated, redirecting to login');
        next({ 
          path: '/login', 
          query: { redirect: to.fullPath } 
        });
      } else {
        // User is authenticated, proceed
        console.log('Authentication confirmed, proceeding');
        next();
      }
    } catch (error) {
      console.error('Auth check failed:', error);
      next({ 
        path: '/login', 
        query: { redirect: to.fullPath } 
      });
    }
  } else {
    // No auth required, just proceed
    next();
  }
});

const app = createApp(App)

initDarkMode()
app.use(router)
app.use(vuetify)

// Register VCalendar with a component prefix
app.use(VCalendar, {
    componentPrefix: 'vc', // Use <vc-calendar />, <vc-date-picker />, etc.
})

// Add global property for easier access to auth service in components
app.config.globalProperties.$auth = authService

// Mount the app
app.mount('#app')