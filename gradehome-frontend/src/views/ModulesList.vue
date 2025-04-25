<template>
    <div class="modules-list-container" ref="modulesListContainer">
      <!-- Header with breadcrumbs -->
      <header class="modules-list-header" :class="{ 'scrolled': isScrolled }">
        <div class="breadcrumbs">
          <router-link to="/" class="breadcrumb-item">Home</router-link>
          <span class="breadcrumb-separator">/</span>
          <router-link to="/graderadar" class="breadcrumb-item">GradeRadar</router-link>
          <span class="breadcrumb-separator">/</span>
          <router-link :to="`/graderadar/university/${encodeURIComponent(universityName)}`" class="breadcrumb-item">{{ universityName }}</router-link>
          <span class="breadcrumb-separator">/</span>
          <span class="breadcrumb-item active">{{ degreeName }}</span>
        </div>
        <div class="header-actions">
          <div class="search-container">
            <input 
              type="text" 
              v-model="searchQuery" 
              @input="handleSearch" 
              placeholder="Search modules..."
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
      <main class="modules-list-main">
        <!-- Loading Indicator -->
        <div v-if="loading" class="loading-container">
          <div class="loading-spinner"></div>
          <div class="loading-text">Loading modules...</div>
        </div>
  
        <!-- Modules Section -->
        <section v-if="!loading" class="modules-section" data-aos="fade-up">
          <div class="section-header">
            <h1>{{ degreeName }} <span class="accent">Modules</span></h1>
            <p>Browse and explore modules for this degree program</p>
          </div>
  
          <!-- Module filters -->
          <div class="module-filters">
            <div class="filter-group">
              <label>Year</label>
              <select v-model="filterYear">
                <option value="">All Years</option>
                <option v-for="year in availableYears" :key="year" :value="year">{{ year }}</option>
              </select>
            </div>
            <div class="filter-group">
              <label>Semester</label>
              <select v-model="filterSemester">
                <option value="">All Semesters</option>
                <option v-for="semester in availableSemesters" :key="semester" :value="semester">Semester {{ semester }}</option>
              </select>
            </div>
            <div class="filter-group">
              <label>Sort By</label>
              <select v-model="sortBy">
                <option value="name">Module Name</option>
                <option value="rating">Rating (Highest)</option>
                <option value="difficulty">Difficulty (Lowest)</option>
                <option value="reviews">Most Reviews</option>
              </select>
            </div>
          </div>
  
          <!-- Modules list -->
          <div class="modules-list">
            <div 
              v-for="module in filteredModules" 
              :key="module.id" 
              class="module-card" 
              @click="navigateToModule(module.id)"
              data-aos="fade-up"
              data-aos-delay="50"
            >
              <div class="module-header">
                <h3>{{ module.name }}</h3>
                <div class="module-code">{{ module.code }}</div>
              </div>
              <div class="module-stats">
                <div class="stats-row">
                  <div class="stat-item">
                    <div class="stat-label">Difficulty</div>
                    <div class="stat-value">
                      <div class="rating-stars">
                        <div class="stars-background">★★★★★</div>
                        <div class="stars-filled" :style="{ width: calculateStarWidth(module.statistics?.difficulty_avg || 0) }">★★★★★</div>
                      </div>
                      <span>{{ formatRating(module.statistics?.difficulty_avg) }}</span>
                    </div>
                  </div>
                  <div class="stat-item">
                    <div class="stat-label">Teaching</div>
                    <div class="stat-value">
                      <div class="rating-stars">
                        <div class="stars-background">★★★★★</div>
                        <div class="stars-filled" :style="{ width: calculateStarWidth(module.statistics?.teaching_quality_avg || 0) }">★★★★★</div>
                      </div>
                      <span>{{ formatRating(module.statistics?.teaching_quality_avg) }}</span>
                    </div>
                  </div>
                </div>
                <div class="stats-row">
                  <div class="stat-item">
                    <div class="stat-label">Recommended</div>
                    <div class="stat-value">{{ formatPercentage(module.statistics?.recommended_avg) }}</div>
                  </div>
                  <div class="stat-item">
                    <div class="stat-label">Reviews</div>
                    <div class="stat-value">{{ module.statistics?.total_reviews || 0 }}</div>
                  </div>
                </div>
              </div>
              <div class="module-meta">
                <div class="meta-item">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                    <line x1="16" y1="2" x2="16" y2="6"></line>
                    <line x1="8" y1="2" x2="8" y2="6"></line>
                    <line x1="3" y1="10" x2="21" y2="10"></line>
                  </svg>
                  <span>{{ module.year || 'Unknown Year' }} - Semester {{ module.semester || '?' }}</span>
                </div>
                <div class="meta-item">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                    <circle cx="8.5" cy="7" r="4"></circle>
                    <line x1="20" y1="8" x2="20" y2="14"></line>
                    <line x1="23" y1="11" x2="17" y2="11"></line>
                  </svg>
                  <span>{{ module.credits || 0 }} credits</span>
                </div>
              </div>
              <svg class="arrow-icon" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M5 12h14"></path>
                <path d="M12 5l7 7-7 7"></path>
              </svg>
            </div>
          </div>
  
          <!-- No modules message -->
          <div v-if="filteredModules.length === 0" class="no-modules">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round">
              <rect x="2" y="2" width="20" height="20" rx="2.18" ry="2.18"></rect>
              <line x1="7" y1="2" x2="7" y2="22"></line>
              <line x1="17" y1="2" x2="17" y2="22"></line>
              <line x1="2" y1="12" x2="22" y2="12"></line>
              <line x1="2" y1="7" x2="7" y2="7"></line>
              <line x1="2" y1="17" x2="7" y2="17"></line>
              <line x1="17" y1="17" x2="22" y2="17"></line>
              <line x1="17" y1="7" x2="22" y2="7"></line>
            </svg>
            <p v-if="searchQuery">No modules found matching your search criteria. Try adjusting your filters.</p>
            <p v-else>No modules found for this degree program.</p>
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
    name: 'ModulesList',
    components: { Footer },
    data() {
      return {
        darkMode: false,
        isScrolled: false,
        loading: true,
        searchQuery: '',
        
        // URL parameters
        universityName: '',
        degreeName: '',
        
        // Module data
        modules: [],
        
        // Filtering and sorting
        filterYear: '',
        filterSemester: '',
        sortBy: 'name',
        
        // Toast state
        showToast: false,
        toastMessage: '',
        toastType: 'success'
      }
    },
    computed: {
      // Filter available years from modules
      availableYears() {
        const years = new Set()
        this.modules.forEach(module => {
          if (module.year) years.add(module.year)
        })
        return Array.from(years).sort()
      },
      
      // Filter available semesters from modules
      availableSemesters() {
        const semesters = new Set()
        this.modules.forEach(module => {
          if (module.semester) semesters.add(module.semester)
        })
        return Array.from(semesters).sort((a, b) => a - b)
      },
      
      // Filter and sort modules based on selected criteria
      filteredModules() {
        let filtered = [...this.modules]
        
        // Apply search filter
        if (this.searchQuery) {
          const query = this.searchQuery.toLowerCase()
          filtered = filtered.filter(module => 
            module.name.toLowerCase().includes(query) || 
            (module.code && module.code.toLowerCase().includes(query))
          )
        }
        
        // Apply year filter
        if (this.filterYear) {
          filtered = filtered.filter(module => module.year === this.filterYear)
        }
        
        // Apply semester filter
        if (this.filterSemester) {
          filtered = filtered.filter(module => module.semester == this.filterSemester)
        }
        
        // Apply sorting
        switch(this.sortBy) {
          case 'name':
            filtered.sort((a, b) => a.name.localeCompare(b.name))
            break
          case 'rating':
            filtered.sort((a, b) => {
              const aRating = a.statistics?.teaching_quality_avg || 0
              const bRating = b.statistics?.teaching_quality_avg || 0
              return bRating - aRating
            })
            break
          case 'difficulty':
            filtered.sort((a, b) => {
              const aDiff = a.statistics?.difficulty_avg || 0
              const bDiff = b.statistics?.difficulty_avg || 0
              return aDiff - bDiff
            })
            break
          case 'reviews':
            filtered.sort((a, b) => {
              const aReviews = a.statistics?.total_reviews || 0
              const bReviews = b.statistics?.total_reviews || 0
              return bReviews - aReviews
            })
            break
        }
        
        return filtered
      }
    },
    methods: {
      toggleDarkMode() {
        this.darkMode = toggleDarkMode()
        this.updateGradient()
      },
      
      updateGradient() {
        const container = this.$refs.modulesListContainer
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
      
      // Navigate to module details page
      navigateToModule(moduleId) {
        this.$router.push(`/graderadar/module/${moduleId}`)
      },
      
      // Calculate width for star rating display
      calculateStarWidth(rating) {
        return `${(rating / 5) * 100}%`
      },
      
      // Format rating
      formatRating(rating) {
        if (rating === null || rating === undefined) return 'N/A'
        return rating.toFixed(1)
      },
      
      // Format percentage
      formatPercentage(value) {
        if (value === null || value === undefined) return 'N/A'
        return `${value.toFixed(0)}%`
      },
      
      // Load modules data
      async loadModules() {
        this.loading = true
        try {
          // Get parameters from route
          this.universityName = decodeURIComponent(this.$route.params.university || '')
          this.degreeName = decodeURIComponent(this.$route.params.degree || '')
          
          if (!this.universityName || !this.degreeName) {
            this.displayToast('University and degree names are required', 'error')
            this.$router.push('/graderadar')
            return
          }
          
          // Load modules for the degree
          const response = await gradeRadarService.getDegreeModules(this.universityName, this.degreeName)
          this.modules = response.data.modules || []
          
          // Reset filters
          this.filterYear = ''
          this.filterSemester = ''
          this.sortBy = 'name'
        } catch (error) {
          console.error('Error loading modules:', error)
          this.displayToast('Error loading modules. Please try again.', 'error')
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
      
      // Load modules data
      this.loadModules()
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
  .modules-list-container {
    min-height: 100vh;
    background: linear-gradient(to bottom, var(--bg-gradient-from), var(--bg-gradient-to));
    color: var(--text-primary);
    position: relative;
    overflow-x: hidden;
    transition: all var(--transition-medium) ease;
  }
  
  /* -------------- Header/Navigation -------------- */
  .modules-list-header {
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
  
  .modules-list-header.scrolled {
    background-color: rgba(255, 255, 255, 0.8);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    box-shadow: var(--shadow-md);
    padding: 0.75rem 2.5rem;
  }
  
  body.dark-mode .modules-list-header.scrolled {
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
  .modules-list-main {
    padding-top: 6rem;
    min-height: calc(100vh - 6rem);
  }
  
  /* -------------- Modules Section -------------- */
  .modules-section {
    padding: 2rem 2.5rem 4rem;
    max-width: 1200px;
    margin: 0 auto;
  }
  
  .section-header {
    text-align: center;
    margin-bottom: 3rem;
  }
  
  .section-header h1 {
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
  
  /* Module filters */
  .module-filters {
    display: flex;
    gap: 1rem;
    margin-bottom: 2rem;
    flex-wrap: wrap;
  }
  
  .filter-group {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .filter-group label {
    font-size: 0.875rem;
    font-weight: 500;
    color: var(--text-secondary);
  }
  
  .filter-group select {
    padding: 0.5rem 1rem;
    border: 1px solid #e0e0e0;
    border-radius: var(--radius-md);
    font-size: 0.95rem;
    background-color: white;
    color: var(--text-primary);
    min-width: 150px;
  }
  
  body.dark-mode .filter-group select {
    border-color: #3a3a52;
    background-color: #252538;
  }
  
  /* Modules list */
  .modules-list {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }
  
  .module-card {
    background-color: white;
    border-radius: var(--radius-lg);
    padding: 1.5rem;
    box-shadow: var(--shadow-md);
    cursor: pointer;
    transition: all var(--transition-medium) ease;
    position: relative;
  }
  
  body.dark-mode .module-card {
    background-color: #1e1e30;
  }
  
  .module-card:hover {
    transform: translateY(-3px);
    box-shadow: var(--shadow-lg);
  }
  
  .module-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
  }
  
  .module-header h3 {
    font-size: 1.25rem;
    font-weight: 600;
    color: var(--text-primary);
  }
  
  .module-code {
    font-size: 0.95rem;
    font-weight: 500;
    color: var(--text-secondary);
    background-color: rgba(123, 73, 255, 0.1);
    padding: 0.25rem 0.75rem;
    border-radius: var(--radius-md);
  }
  
  .module-stats {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    margin-bottom: 1rem;
  }
  
  .stats-row {
    display: flex;
    gap: 2rem;
  }
  
  .stat-item {
    flex: 1;
  }
  
  .stat-label {
    font-size: 0.875rem;
    color: var(--text-secondary);
    margin-bottom: 0.25rem;
  }
  
  .stat-value {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-weight: 600;
    color: var(--text-primary);
  }
  
  .rating-stars {
    position: relative;
    font-size: 1.25rem;
    line-height: 1;
    display: inline-block;
  }
  
  .stars-background {
    color: #e0e0e0;
  }
  
  body.dark-mode .stars-background {
    color: #3a3a52;
  }
  
  .stars-filled {
    position: absolute;
    top: 0;
    left: 0;
    color: var(--primary-color);
    overflow: hidden;
    white-space: nowrap;
  }
  
  .module-meta {
    display: flex;
    gap: 1.5rem;
  }
  
  .meta-item {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.875rem;
    color: var(--text-secondary);
  }
  
  .module-card .arrow-icon {
    position: absolute;
    right: 1.5rem;
    top: 50%;
    transform: translateY(-50%) translateX(-10px);
    color: var(--text-secondary);
    opacity: 0;
    transition: all var(--transition-medium) ease;
  }
  
  .module-card:hover .arrow-icon {
    opacity: 1;
    transform: translateY(-50%) translateX(0);
    color: var(--primary-color);
  }
  
  /* No modules message */
  .no-modules {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1rem;
    padding: 4rem 0;
    color: var(--text-secondary);
    text-align: center;
  }
  
  .no-modules svg {
    opacity: 0.5;
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
    .modules-list-header,
    .modules-list-header.scrolled {
      padding-left: 1.5rem;
      padding-right: 1.5rem;
    }
    
    .search-input {
      width: 200px;
    }
    
    .search-input:focus {
      width: 250px;
    }
    
    .modules-section {
      padding-left: 1.5rem;
      padding-right: 1.5rem;
    }
  }
  
  @media (max-width: 992px) {
    .modules-list-header {
      flex-direction: column;
      align-items: flex-start;
      gap: 1rem;
    }
    
    .header-actions {
      width: 100%;
      justify-content: space-between;
    }
    
    .section-header h1 {
      font-size: 1.75rem;
    }
    
    .stats-row {
      flex-direction: column;
      gap: 0.75rem;
    }
  }
  
  @media (max-width: 768px) {
    .modules-list-header,
    .modules-list-header.scrolled {
      padding-left: 1rem;
      padding-right: 1rem;
    }
    
    .search-input {
      width: 150px;
    }
    
    .search-input:focus {
      width: 200px;
    }
    
    .modules-section {
      padding-left: 1rem;
      padding-right: 1rem;
    }
    
    .module-filters {
      flex-direction: column;
    }
    
    .module-header {
      flex-direction: column;
      align-items: flex-start;
      gap: 0.5rem;
    }
    
    .module-meta {
      flex-direction: column;
      gap: 0.5rem;
    }
  }
  
  @media (max-width: 576px) {
    .breadcrumbs {
      font-size: 0.8rem;
      flex-wrap: wrap;
    }
  }
  </style>