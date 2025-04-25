<template>
  <div class="graderadar-container" ref="graderadarContainer">
    <!-- Header with breadcrumbs -->
    <header class="graderadar-header" :class="{ 'scrolled': isScrolled }">
      <div class="breadcrumbs">
        <router-link to="/" class="breadcrumb-item">Home</router-link>
        <span class="breadcrumb-separator">/</span>
        <span class="breadcrumb-item active">GradeRadar</span>
      </div>
      <div class="header-actions">
        <div class="search-container">
          <input 
            type="text" 
            v-model="searchQuery" 
            @input="handleSearch" 
            placeholder="Search universities..."
            class="search-input"
          />
          <svg class="search-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="11" cy="11" r="8"></circle>
            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
          </svg>
        </div>
        <button @click="toggleDarkMode" class="theme-toggle" aria-label="Toggle dark mode">
          <svg v-if="darkMode" class="sun-icon" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
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
          <svg v-else class="moon-icon" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
          </svg>
        </button>
        <router-link v-if="!isLoggedIn" :to="{ path: '/login', query: { mode: 'login' } }" class="nav-btn">
          <span class="text">Login</span>
          <span class="hover-circle"></span>
        </router-link>
        <router-link v-if="!isLoggedIn" :to="{ path: '/login', query: { mode: 'signup' } }" class="nav-btn primary">
          <span class="text">Sign Up</span>
          <svg class="arrow-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M5 12h14"></path>
            <path d="M12 5l7 7-7 7"></path>
          </svg>
        </router-link>
      </div>
    </header>

    <!-- Main Content Section -->
    <main class="graderadar-main">
      <!-- Hero section -->
      <section class="hero-section">
        <div class="hero-content" data-aos="fade-up">
          <h1 class="hero-title">Grade<span class="accent">Radar</span></h1>
          <p class="hero-description">
            Explore course reviews, discover module insights, and share your academic experiences to help others succeed.
          </p>
          <div class="stats-preview">
            <div class="stat-item">
              <div class="stat-value">{{ totalUniversities }}</div>
              <div class="stat-label">Universities</div>
            </div>
            <div class="stat-item">
              <div class="stat-value">{{ totalDegrees }}</div>
              <div class="stat-label">Programs</div>
            </div>
            <div class="stat-item">
              <div class="stat-value">{{ totalModules }}</div>
              <div class="stat-label">Modules</div>
            </div>
            <div class="stat-item">
              <div class="stat-value">{{ totalReviews }}</div>
              <div class="stat-label">Reviews</div>
            </div>
          </div>
        </div>
      </section>

      <!-- Loading Indicator -->
      <div v-if="loading" class="loading-container">
        <div class="loading-spinner"></div>
        <div class="loading-text">Loading data...</div>
      </div>

      <!-- University Selection -->
      <section v-if="!loading" class="universities-section" data-aos="fade-up">
        <div class="section-header">
          <h2>Explore <span class="accent">Universities</span></h2>
          <p>Discover module reviews and academic insights from students worldwide</p>
        </div>

        <div class="universities-grid">
          <div 
            v-for="uni in filteredUniversities" 
            :key="uni.id" 
            class="university-card" 
            @click="navigateToUniversity(uni.name)"
            data-aos="fade-up"
            data-aos-delay="50"
          >
            <div class="university-initial">{{ uni.name.charAt(0) }}</div>
            <div class="university-details">
              <h3>{{ uni.name }}</h3>
              <div class="university-stats">
                <div class="stat">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                    <circle cx="9" cy="7" r="4"></circle>
                    <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
                    <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
                  </svg>
                  <span>{{ uni.students_count }} students</span>
                </div>
                <div class="stat">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path>
                    <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path>
                  </svg>
                  <span>{{ uni.degrees_count }} programs</span>
                </div>
              </div>
            </div>
            <svg class="arrow-icon" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M5 12h14"></path>
              <path d="M12 5l7 7-7 7"></path>
            </svg>
          </div>
        </div>
      </section>
    </main>

    <!-- Footer -->
    <Footer />

    <!-- Toast notifications -->
    <div v-if="showToast" class="toast-notification" :class="toastType">
      <svg v-if="toastType === 'success'" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
        <polyline points="22 4 12 14.01 9 11.01"></polyline>
      </svg>
      <svg v-else width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="10"></circle>
        <line x1="12" y1="8" x2="12" y2="12"></line>
        <line x1="12" y1="16" x2="12.01" y2="16"></line>
      </svg>
      <span>{{ toastMessage }}</span>
    </div>
  </div>
</template>

<script>
import Footer from '@/components/Footer.vue'
import AOS from 'aos'
import 'aos/dist/aos.css'
import { getDarkModePreference, toggleDarkMode } from '@/services/darkModeService'
import gradeRadarService from '@/services/gradeRadarService'

export default {
  name: 'GradeRadar',
  components: { Footer },
  data() {
    return {
      darkMode: false,
      isScrolled: false,
      loading: true,
      searchQuery: '',
      
      // Data
      universities: [],
      
      // Stats for hero section
      totalUniversities: 0,
      totalDegrees: 0,
      totalModules: 0,
      totalReviews: 0,
      
      // Toast state
      showToast: false,
      toastMessage: '',
      toastType: 'success'
    }
  },
  computed: {
    // Check if user is logged in
    isLoggedIn() {
      return localStorage.getItem('token') !== null
    },
    
    // Filter universities based on search query
    filteredUniversities() {
      if (!this.searchQuery) return this.universities
      
      const query = this.searchQuery.toLowerCase()
      return this.universities.filter(uni => 
        uni.name.toLowerCase().includes(query)
      )
    }
  },
  methods: {
    toggleDarkMode() {
      this.darkMode = toggleDarkMode()
      this.updateGradient()
    },
    
    updateGradient() {
      const container = this.$refs.graderadarContainer
      if (!container) return
      
      // Set gradient based on dark mode state
      if (this.darkMode) {
        container.style.setProperty('--bg-gradient-from', '#1a1a2e')
        container.style.setProperty('--bg-gradient-to', '#0f0f1a')
      } else {
        container.style.setProperty('--bg-gradient-from', '#f9f9ff')
        container.style.setProperty('--bg-gradient-to', '#f0f0ff')
      }
    },
    
    handleScroll() {
      this.isScrolled = window.scrollY > 20
    },
    
    // Handle search input
    handleSearch() {
      // The filtering is done by the computed property
    },
    
    // Navigate to university details page
    navigateToUniversity(university) {
      this.$router.push(`/graderadar/university/${encodeURIComponent(university)}`)
    },
    
    // Load universities data
    async loadUniversities() {
      this.loading = true
      try {
        const response = await gradeRadarService.getUniversities()
        this.universities = response.data
        this.totalUniversities = this.universities.length
        
        // Initialize totals
        let degreesCount = 0
        let modulesCount = 0
        let reviewsCount = 0
        
        // Calculate totals
        for (const uni of this.universities) {
          degreesCount += uni.degrees_count || 0
          modulesCount += uni.degrees_count * 5 // estimate 5 modules per degree
          reviewsCount += uni.students_count * 0.5 // estimate 0.5 reviews per student
        }
        
        this.totalDegrees = degreesCount
        this.totalModules = modulesCount
        this.totalReviews = Math.floor(reviewsCount)
      } catch (error) {
        console.error('Error loading universities:', error)
        this.displayToast('Error loading universities. Please try again.', 'error')
      } finally {
        this.loading = false
      }
    },
    
    // Display toast notification
    displayToast(message, type = 'success') {
      this.toastMessage = message
      this.toastType = type
      this.showToast = true
      
      setTimeout(() => {
        this.showToast = false
      }, 3000)
    }
  },
  mounted() {
    // Initialize dark mode from the service
    this.darkMode = getDarkModePreference()

    // Listen for dark mode changes from other components
    window.addEventListener('darkModeChange', (event) => {
      this.darkMode = event.detail.isDark
      this.updateGradient()
    })

    // Add scroll listener
    window.addEventListener('scroll', this.handleScroll)

    // Initialize AOS (Animate on Scroll)
    AOS.init({
      duration: 800,
      offset: 100,
      once: true,
      easing: 'ease-out-cubic'
    })

    // Set initial gradient
    this.updateGradient()
    
    // Load initial data
    this.loadUniversities()
  },
  beforeUnmount() {
    // Clean up event listeners
    window.removeEventListener('darkModeChange', this.onDarkModeChange)
    window.removeEventListener('scroll', this.handleScroll)
  }
}
</script>

<style scoped>
/* Custom CSS Variables */
:root {
  --primary-hue: 265;
  --primary-color: #7b49ff;
  --primary-light: #9061ff;
  --primary-dark: #6234e0;
  --bg-gradient-from: #f9f9ff;
  --bg-gradient-to: #f0f0ff;

  /* Text colors */
  --text-primary: #333;
  --text-secondary: #555;

  /* Accent colors */
  --accent-blue: #4f46e5;
  --accent-purple: #9061ff;
  --accent-pink: #ec4899;

  /* Animation timings */
  --transition-fast: 0.2s;
  --transition-medium: 0.3s;
  --transition-slow: 0.5s;

  /* Border radius */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-xl: 24px;
  --radius-full: 9999px;

  /* Shadows */
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.07);
  --shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.08);
  --shadow-xl: 0 20px 25px rgba(0, 0, 0, 0.1);
}

/* Main container */
.graderadar-container {
  min-height: 100vh;
  background: linear-gradient(to bottom, var(--bg-gradient-from), var(--bg-gradient-to));
  color: var(--text-primary);
  position: relative;
  overflow-x: hidden;
  transition: all var(--transition-medium) ease;
}

/* -------------- Header/Navigation -------------- */
.graderadar-header {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.25rem 2.5rem;
  background-color: transparent;
  backdrop-filter: blur(0);
  -webkit-backdrop-filter: blur(0);
  z-index: 50;
  transition: all var(--transition-medium) ease;
}

.graderadar-header.scrolled {
  background-color: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  box-shadow: var(--shadow-md);
  padding: 0.75rem 2.5rem;
}

body.dark-mode .graderadar-header.scrolled {
  background-color: rgba(20, 20, 30, 0.8);
}

.breadcrumbs {
  display: flex;
  align-items: center;
  font-size: 0.95rem;
  font-weight: 500;
}

.breadcrumb-item {
  color: var(--text-primary);
  text-decoration: none;
  transition: color var(--transition-fast) ease;
}

.breadcrumb-item:not(.active):hover {
  color: var(--primary-color);
}

.breadcrumb-item.active {
  color: var(--primary-color);
  font-weight: 600;
}

.breadcrumb-separator {
  margin: 0 0.5rem;
  color: var(--text-secondary);
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.search-container {
  position: relative;
}

.search-input {
  width: 250px;
  padding: 0.625rem 2.5rem 0.625rem 1rem;
  border: 1px solid #e0e0e0;
  border-radius: var(--radius-full);
  font-size: 0.95rem;
  transition: all var(--transition-medium) ease;
  background-color: rgba(255, 255, 255, 0.8);
  color: var(--text-primary);
}

body.dark-mode .search-input {
  border-color: #3a3a52;
  background-color: rgba(30, 30, 48, 0.8);
}

.search-input:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(123, 73, 255, 0.2);
  width: 300px;
}

.search-icon {
  position: absolute;
  right: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-secondary);
  pointer-events: none;
}

.theme-toggle {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  background: transparent;
  color: var(--text-primary);
  border: none;
  border-radius: 50%;
  cursor: pointer;
  transition: all var(--transition-medium) ease;
}

.theme-toggle:hover {
  background-color: rgba(123, 73, 255, 0.1);
  transform: scale(1.05);
}

.sun-icon, .moon-icon {
  transition: transform var(--transition-medium) ease, opacity var(--transition-medium) ease;
}

.theme-toggle:hover .sun-icon,
.theme-toggle:hover .moon-icon {
  transform: rotate(15deg);
}

.nav-btn {
  position: relative;
  padding: 0.625rem 1.25rem;
  font-size: 0.95rem;
  font-weight: 500;
  color: var(--text-primary);
  text-decoration: none;
  border-radius: var(--radius-full);
  transition: all var(--transition-medium) ease;
  overflow: hidden;
}

.nav-btn .hover-circle {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  border-radius: 50%;
  background-color: rgba(123, 73, 255, 0.1);
  transform: translate(-50%, -50%);
  transition: width var(--transition-medium) ease-out,
  height var(--transition-medium) ease-out;
  z-index: -1;
}

.nav-btn:hover .hover-circle {
  width: 250%;
  height: 300%;
}

.nav-btn.primary {
  color: white;
  background-color: var(--primary-color);
  padding-right: 2.75rem;
  font-weight: 600;
}

.nav-btn.primary:hover {
  background-color: var(--primary-dark);
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.arrow-icon {
  position: absolute;
  right: 0.75rem;
  top: 50%;
  transform: translateY(-50%) translateX(0);
  transition: transform var(--transition-medium) ease;
}

.nav-btn.primary:hover .arrow-icon {
  transform: translateY(-50%) translateX(3px);
}

/* -------------- Main Content Section -------------- */
.graderadar-main {
  padding-top: 6rem;
  min-height: calc(100vh - 6rem);
}

/* -------------- Hero Section -------------- */
.hero-section {
  min-height: 50vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  text-align: center;
}

.hero-title {
  font-size: 3.75rem;
  font-weight: 800;
  line-height: 1.1;
  margin-bottom: 1.5rem;
  letter-spacing: -0.02em;
  color: var(--text-primary);
}

.accent {
  color: var(--primary-color);
  position: relative;
}

.accent::after {
  content: "";
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 6px;
  border-radius: 3px;
  background: linear-gradient(90deg, var(--primary-color), var(--accent-pink));
  opacity: 0.3;
  transform: translateY(4px);
}

.hero-description {
  font-size: 1.25rem;
  line-height: 1.6;
  color: var(--text-secondary);
  margin-bottom: 2rem;
  max-width: 700px;
  margin-left: auto;
  margin-right: auto;
}

.stats-preview {
  display: flex;
  justify-content: center;
  gap: 3rem;
  margin-top: 3rem;
}

.stat-item {
  text-align: center;
}

.stat-value {
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--primary-color);
  margin-bottom: 0.25rem;
}

.stat-label {
  font-size: 1rem;
  color: var(--text-secondary);
  font-weight: 500;
}

/* -------------- Section Headers -------------- */
.section-header {
  text-align: center;
  max-width: 700px;
  margin: 0 auto 3rem;
}

.section-header h2 {
  font-size: 2.5rem;
  font-weight: 800;
  margin-bottom: 1rem;
  color: var(--text-primary);
}

.section-header p {
  font-size: 1.125rem;
  color: var(--text-secondary);
}

/* -------------- University Selection -------------- */
.universities-section {
  padding: 4rem 2rem;
}

.universities-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
  max-width: 1200px;
  margin: 0 auto;
}

.university-card {
  background-color: white;
  border-radius: var(--radius-lg);
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  box-shadow: var(--shadow-md);
  cursor: pointer;
  transition: all var(--transition-medium) ease;
  position: relative;
}

body.dark-mode .university-card {
  background-color: #1e1e30;
}

.university-card:hover {
  transform: translateY(-5px);
  box-shadow: var(--shadow-lg);
}

.university-initial {
  width: 60px;
  height: 60px;
  border-radius: var(--radius-md);
  background: linear-gradient(135deg, var(--primary-color), var(--accent-pink));
  color: white;
  font-size: 1.75rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
}

.university-details {
  flex: 1;
}

.university-card h3 {
  font-size: 1.125rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: var(--text-primary);
}

.university-stats {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.stat {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: var(--text-secondary);
}

.university-card .arrow-icon {
  position: absolute;
  right: 1.5rem;
  color: var(--text-secondary);
  opacity: 0;
  transform: translateX(-10px);
  transition: all var(--transition-medium) ease;
}

.university-card:hover .arrow-icon {
  opacity: 1;
  transform: translateX(0);
  color: var(--primary-color);
}

/* -------------- Loading Indicator -------------- */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  padding: 4rem 0;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid rgba(123, 73, 255, 0.3);
  border-radius: 50%;
  border-top-color: var(--primary-color);
  animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.loading-text {
  font-size: 0.95rem;
  color: var(--text-secondary);
}

/* -------------- Toast Notifications -------------- */
.toast-notification {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem 1.5rem;
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-lg);
  animation: slideIn var(--transition-medium) forwards;
  z-index: 100;
}

.toast-notification.success {
  background-color: #10b981;
  color: white;
}

.toast-notification.error {
  background-color: #ef4444;
  color: white;
}

@keyframes slideIn {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

/* -------------- Responsive Styles -------------- */
@media (max-width: 1200px) {
  .graderadar-header,
  .graderadar-header.scrolled {
    padding-left: 1.5rem;
    padding-right: 1.5rem;
  }
  
  .search-input {
    width: 200px;
  }
  
  .search-input:focus {
    width: 250px;
  }
}

@media (max-width: 992px) {
  .graderadar-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  
  .header-actions {
    width: 100%;
    justify-content: space-between;
  }
  
  .hero-title {
    font-size: 3rem;
  }
  
  .stats-preview {
    gap: 1.5rem;
  }
  
  .stat-value {
    font-size: 2rem;
  }
}

@media (max-width: 768px) {
  .graderadar-header,
  .graderadar-header.scrolled {
    padding-left: 1rem;
    padding-right: 1rem;
  }
  
  .search-input {
    width: 150px;
  }
  
  .search-input:focus {
    width: 200px;
  }
  
  .hero-title {
    font-size: 2.5rem;
  }
  
  .hero-description {
    font-size: 1.125rem;
  }
  
  .stats-preview {
    flex-wrap: wrap;
    gap: 2rem;
  }
  
  .stat-item {
    flex: 1;
    min-width: 120px;
  }
  
  .universities-section {
    padding: 2rem 1rem;
  }
  
  .universities-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 576px) {
  .hero-title {
    font-size: 2rem;
  }
  
  .stat-value {
    font-size: 1.75rem;
  }
  
  .stat-label {
    font-size: 0.875rem;
  }
  
  .section-header h2 {
    font-size: 1.75rem;
  }
}
</style>