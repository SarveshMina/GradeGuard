<template>
    <div class="university-view-container" ref="universityViewContainer">
      <!-- Header with breadcrumbs -->
      <header class="university-header" :class="{ 'scrolled': isScrolled }">
        <div class="breadcrumbs">
          <router-link to="/" class="breadcrumb-item">Home</router-link>
          <span class="breadcrumb-separator">/</span>
          <router-link to="/graderadar" class="breadcrumb-item">GradeRadar</router-link>
          <span class="breadcrumb-separator">/</span>
          <span class="breadcrumb-item active">{{ universityName }}</span>
        </div>
        <div class="header-actions">
          <div class="search-container">
            <input 
              type="text" 
              v-model="searchQuery" 
              @input="handleSearch" 
              placeholder="Search degrees..."
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
        </div>
      </header>
  
      <!-- Main Content Section -->
      <main class="university-main">
        <!-- Loading Indicator -->
        <div v-if="loading" class="loading-container">
          <div class="loading-spinner"></div>
          <div class="loading-text">Loading data...</div>
        </div>
  
        <!-- University Overview -->
        <section v-if="!loading" class="university-overview-section" data-aos="fade-up">
          <div class="university-info">
            <div class="university-logo">
              <div class="university-initial">{{ universityName.charAt(0) }}</div>
            </div>
            <div class="university-details">
              <h1>{{ universityName }}</h1>
              <div class="university-stats">
                <div class="stat-item">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                    <circle cx="9" cy="7" r="4"></circle>
                    <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
                    <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
                  </svg>
                  <span>{{ universityData.students_count || 0 }} students</span>
                </div>
                <div class="stat-item">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path>
                    <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path>
                  </svg>
                  <span>{{ universityDegrees.length }} degree programs</span>
                </div>
              </div>
            </div>
          </div>
        </section>
  
        <!-- Degrees Section -->
        <section v-if="!loading" class="degrees-section" data-aos="fade-up">
          <div class="section-header">
            <h2>Degree <span class="accent">Programs</span></h2>
            <p>Explore modules and student reviews for each degree program</p>
          </div>
  
          <div class="degrees-grid">
            <div 
              v-for="degree in filteredDegrees" 
              :key="degree.name" 
              class="degree-card" 
              @click="navigateToDegree(degree.name)"
              data-aos="fade-up"
              data-aos-delay="50"
            >
              <div class="degree-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M22 10v6M2 10l10-5 10 5-10 5z"></path>
                  <path d="M6 12v5c3 3 9 3 12 0v-5"></path>
                </svg>
              </div>
              <div class="degree-details">
                <h3>{{ degree.name }}</h3>
                <div class="degree-stats">
                  <div class="stat">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"></path>
                      <rect x="8" y="2" width="8" height="4" rx="1" ry="1"></rect>
                    </svg>
                    <span>{{ degree.modules_count }} modules</span>
                  </div>
                  <div class="stat">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                      <circle cx="9" cy="7" r="4"></circle>
                    </svg>
                    <span>{{ degree.students_count }} students</span>
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
    name: 'UniversityView',
    components: { Footer },
    data() {
      return {
        darkMode: false,
        isScrolled: false,
        loading: true,
        searchQuery: '',
        
        // University data
        universityName: '',
        universityData: {},
        universityDegrees: [],
        
        // Toast state
        showToast: false,
        toastMessage: '',
        toastType: 'success'
      }
    },
    computed: {
      // Filter degrees based on search query
      filteredDegrees() {
        if (!this.searchQuery) return this.universityDegrees
        
        const query = this.searchQuery.toLowerCase()
        return this.universityDegrees.filter(degree => 
          degree.name.toLowerCase().includes(query)
        )
      }
    },
    methods: {
      toggleDarkMode() {
        this.darkMode = toggleDarkMode()
        this.updateGradient()
      },
      
      updateGradient() {
        const container = this.$refs.universityViewContainer
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
      
      // Navigate to degree modules page
      navigateToDegree(degree) {
        this.$router.push(`/graderadar/modules/${encodeURIComponent(this.universityName)}/${encodeURIComponent(degree)}`)
      },
      
      // Load university data
      async loadUniversityData() {
        this.loading = true
        try {
          // Get university name from route params
          this.universityName = decodeURIComponent(this.$route.params.university || '')
          
          if (!this.universityName) {
            this.displayToast('University name is required', 'error')
            this.$router.push('/graderadar')
            return
          }
          
          // Load university degrees
          const response = await gradeRadarService.getUniversityDegrees(this.universityName)
          this.universityData = {
            name: response.data.name,
            students_count: response.data.students_count
          }
          this.universityDegrees = response.data.degrees || []
        } catch (error) {
          console.error('Error loading university data:', error)
          this.displayToast('Error loading university data. Please try again.', 'error')
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
      
      // Load university data
      this.loadUniversityData()
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
  .university-view-container {
    min-height: 100vh;
    background: linear-gradient(to bottom, var(--bg-gradient-from), var(--bg-gradient-to));
    color: var(--text-primary);
    position: relative;
    overflow-x: hidden;
    transition: all var(--transition-medium) ease;
  }
  
  /* -------------- Header/Navigation -------------- */
  .university-header {
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
  
  .university-header.scrolled {
    background-color: rgba(255, 255, 255, 0.8);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    box-shadow: var(--shadow-md);
    padding: 0.75rem 2.5rem;
  }
  
  body.dark-mode .university-header.scrolled {
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
  
  /* -------------- Main Content Section -------------- */
  .university-main {
    padding-top: 6rem;
    min-height: calc(100vh - 6rem);
  }
  
  /* -------------- University Overview Section -------------- */
  .university-overview-section {
    padding: 2rem 2.5rem;
  }
  
  .university-info {
    display: flex;
    align-items: center;
    gap: 2rem;
    max-width: 1200px;
    margin: 0 auto;
  }
  
  .university-logo {
    flex-shrink: 0;
  }
  
  .university-initial {
    width: 100px;
    height: 100px;
    border-radius: var(--radius-lg);
    background: linear-gradient(135deg, var(--primary-color), var(--accent-pink));
    color: white;
    font-size: 3rem;
    font-weight: 700;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .university-details {
    flex: 1;
  }
  
  .university-details h1 {
    font-size: 2.5rem;
    font-weight: 800;
    margin-bottom: 1rem;
    color: var(--text-primary);
  }
  
  .university-stats {
    display: flex;
    gap: 2rem;
  }
  
  .stat-item {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 1rem;
    color: var(--text-secondary);
  }
  
  /* -------------- Degrees Section -------------- */
  .degrees-section {
    padding: 2rem 2.5rem 4rem;
  }
  
  .section-header {
    text-align: center;
    max-width: 700px;
    margin: 0 auto 3rem;
  }
  
  .section-header h2 {
    font-size: 2.25rem;
    font-weight: 800;
    margin-bottom: 1rem;
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
    height: 4px;
    border-radius: 2px;
    background: linear-gradient(90deg, var(--primary-color), var(--accent-pink));
    opacity: 0.3;
    transform: translateY(4px);
  }
  
  .section-header p {
    font-size: 1.125rem;
    color: var(--text-secondary);
  }
  
  .degrees-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 1.5rem;
    max-width: 1200px;
    margin: 0 auto;
  }
  
  .degree-card {
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
  
  body.dark-mode .degree-card {
    background-color: #1e1e30;
  }
  
  .degree-card:hover {
    transform: translateY(-5px);
    box-shadow: var(--shadow-lg);
  }
  
  .degree-icon {
    width: 50px;
    height: 50px;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: rgba(123, 73, 255, 0.1);
    color: var(--primary-color);
    border-radius: var(--radius-md);
    transition: all var(--transition-medium) ease;
  }
  
  .degree-card:hover .degree-icon {
    background: linear-gradient(135deg, var(--primary-color), var(--accent-pink));
    color: white;
  }
  
  .degree-details {
    flex: 1;
  }
  
  .degree-details h3 {
    font-size: 1.125rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
    color: var(--text-primary);
  }
  
  .degree-stats {
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
  
  .degree-card .arrow-icon {
    position: absolute;
    right: 1.5rem;
    color: var(--text-secondary);
    opacity: 0;
    transform: translateX(-10px);
    transition: all var(--transition-medium) ease;
  }
  
  .degree-card:hover .arrow-icon {
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
    .university-header,
    .university-header.scrolled {
      padding-left: 1.5rem;
      padding-right: 1.5rem;
    }
    
    .search-input {
      width: 200px;
    }
    
    .search-input:focus {
      width: 250px;
    }
    
    .university-overview-section,
    .degrees-section {
      padding-left: 1.5rem;
      padding-right: 1.5rem;
    }
  }
  
  @media (max-width: 992px) {
    .university-header {
      flex-direction: column;
      align-items: flex-start;
      gap: 1rem;
    }
    
    .header-actions {
      width: 100%;
      justify-content: space-between;
    }
    
    .university-info {
      flex-direction: column;
      align-items: center;
      text-align: center;
      gap: 1.5rem;
    }
    
    .university-details h1 {
      font-size: 2.25rem;
    }
    
    .university-stats {
      justify-content: center;
    }
  }
  
  @media (max-width: 768px) {
    .university-header,
    .university-header.scrolled {
      padding-left: 1rem;
      padding-right: 1rem;
    }
    
    .search-input {
      width: 150px;
    }
    
    .search-input:focus {
      width: 200px;
    }
    
    .university-overview-section,
    .degrees-section {
      padding-left: 1rem;
      padding-right: 1rem;
    }
    
    .section-header h2 {
      font-size: 1.75rem;
    }
    
    .section-header p {
      font-size: 1rem;
    }
    
    .degrees-grid {
      grid-template-columns: 1fr;
    }
  }
  
  @media (max-width: 576px) {
    .university-details h1 {
      font-size: 1.75rem;
    }
    
    .university-initial {
      width: 80px;
      height: 80px;
      font-size: 2.5rem;
    }
    
    .university-stats {
      flex-direction: column;
      gap: 0.5rem;
    }
  }
  </style>