<template>
    <div class="module-detail-container" ref="moduleDetailContainer">
      <!-- Header with breadcrumbs -->
      <header class="module-detail-header" :class="{ 'scrolled': isScrolled }">
        <div class="breadcrumbs">
          <router-link to="/" class="breadcrumb-item">Home</router-link>
          <span class="breadcrumb-separator">/</span>
          <router-link to="/graderadar" class="breadcrumb-item">GradeRadar</router-link>
          <span class="breadcrumb-separator">/</span>
          <router-link :to="`/graderadar/university/${encodeURIComponent(moduleData.university)}`" class="breadcrumb-item">{{ moduleData.university }}</router-link>
          <span class="breadcrumb-separator">/</span>
          <router-link 
            :to="`/graderadar/modules/${encodeURIComponent(moduleData.university)}/${encodeURIComponent(moduleData.degree)}`" 
            class="breadcrumb-item"
          >
            {{ moduleData.degree }}
          </router-link>
          <span class="breadcrumb-separator">/</span>
          <span class="breadcrumb-item active">{{ moduleData.name }}</span>
        </div>
        <div class="header-actions">
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
      <main class="module-detail-main">
        <!-- Loading Indicator -->
        <div v-if="loading" class="loading-container">
          <div class="loading-spinner"></div>
          <div class="loading-text">Loading module details...</div>
        </div>
  
        <template v-if="!loading">
          <!-- Module Header Section -->
          <section class="module-header-section" data-aos="fade-up">
            <div class="module-header-content">
              <div class="module-title-area">
                <h1>{{ moduleData.name }}</h1>
                <div class="module-code">{{ moduleData.code }}</div>
                <div class="module-meta">
                  <div class="meta-item">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                      <line x1="16" y1="2" x2="16" y2="6"></line>
                      <line x1="8" y1="2" x2="8" y2="6"></line>
                      <line x1="3" y1="10" x2="21" y2="10"></line>
                    </svg>
                    <span>{{ moduleData.year || 'Unknown Year' }} - Semester {{ moduleData.semester || '?' }}</span>
                  </div>
                  <div class="meta-item">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                      <circle cx="8.5" cy="7" r="4"></circle>
                      <line x1="20" y1="8" x2="20" y2="14"></line>
                      <line x1="23" y1="11" x2="17" y2="11"></line>
                    </svg>
                    <span>{{ moduleData.credits || 0 }} credits</span>
                  </div>
                </div>
              </div>
              <div class="module-stats-summary">
                <div class="stats-item">
                  <div class="stat-title">Difficulty</div>
                  <div class="stat-value">
                    <div class="rating-stars">
                      <div class="stars-background">★★★★★</div>
                      <div class="stars-filled" :style="{ width: calculateStarWidth(moduleData.statistics?.difficulty_avg || 0) }">★★★★★</div>
                    </div>
                    <span>{{ formatRating(moduleData.statistics?.difficulty_avg) }}</span>
                  </div>
                </div>
                <div class="stats-item">
                  <div class="stat-title">Teaching</div>
                  <div class="stat-value">
                    <div class="rating-stars">
                      <div class="stars-background">★★★★★</div>
                      <div class="stars-filled" :style="{ width: calculateStarWidth(moduleData.statistics?.teaching_quality_avg || 0) }">★★★★★</div>
                    </div>
                    <span>{{ formatRating(moduleData.statistics?.teaching_quality_avg) }}</span>
                  </div>
                </div>
                <div class="stats-item">
                  <div class="stat-title">Recommendation</div>
                  <div class="stat-value">{{ formatPercentage(moduleData.statistics?.recommended_avg) }}</div>
                </div>
                <div class="stats-item">
                  <div class="stat-title">Reviews</div>
                  <div class="stat-value">{{ moduleData.statistics?.total_reviews || 0 }}</div>
                </div>
              </div>
            </div>
          </section>
          
          <!-- Overview Section -->
          <section class="module-overview-section" data-aos="fade-up">
            <div class="section-header">
              <h2>Module <span class="accent">Overview</span></h2>
            </div>
            
            <div class="overview-container">
              <div class="overview-column ratings-chart">
                <GradeRadarChart :module-data="moduleData" />
              </div>
              <div class="overview-column grade-distribution">
                <GradeDistribution :grade-data="moduleData.grade_distribution" />
              </div>
            </div>
          </section>
          
          <!-- Reviews Section -->
          <section class="module-reviews-section" data-aos="fade-up">
            <div class="section-header reviews-header">
              <h2>Student <span class="accent">Reviews</span></h2>
              <div v-if="isLoggedIn" class="add-review-btn" @click="showReviewForm = !showReviewForm">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <circle cx="12" cy="12" r="10"></circle>
                  <line x1="12" y1="8" x2="12" y2="16"></line>
                  <line x1="8" y1="12" x2="16" y2="12"></line>
                </svg>
                <span>{{ showReviewForm ? 'Cancel' : 'Add Review' }}</span>
              </div>
            </div>
            
            <!-- Review Form -->
            <div v-if="showReviewForm && isLoggedIn" class="review-form-container" data-aos="fade-up">
              <ReviewForm 
                :module-id="moduleId" 
                @review-submitted="onReviewSubmitted" 
                @form-canceled="showReviewForm = false"
              />
            </div>
            
            <!-- Review Filters -->
            <div class="review-filters">
              <div class="filter-group">
                <label>Sort By</label>
                <select v-model="reviewSortBy">
                  <option value="recent">Most Recent</option>
                  <option value="rating">Highest Rating</option>
                  <option value="useful">Most Useful</option>
                </select>
              </div>
            </div>
            
            <!-- Reviews List -->
            <div v-if="moduleData.reviews && moduleData.reviews.length > 0" class="reviews-list">
              <ReviewItem
                v-for="review in sortedReviews"
                :key="review.id"
                :review="review"
                :is-author="isReviewAuthor(review)"
                @delete-review="confirmDeleteReview"
              />
            </div>
            
            <!-- No Reviews Message -->
            <div v-else class="no-reviews">
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
              <p>No reviews yet for this module. Be the first to share your experience!</p>
              <div v-if="isLoggedIn && !showReviewForm" class="no-reviews-btn" @click="showReviewForm = true">
                <span>Add Review</span>
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M5 12h14"></path>
                  <path d="M12 5l7 7-7 7"></path>
                </svg>
              </div>
            </div>
          </section>
        </template>
      </main>
  
      <!-- Footer -->
      <Footer />
  
      <!-- Delete Confirmation Modal -->
      <div v-if="showDeleteModal" class="modal-overlay">
        <div class="modal-container">
          <div class="modal-header">
            <h3>Delete Review</h3>
            <button class="modal-close" @click="showDeleteModal = false">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <line x1="18" y1="6" x2="6" y2="18"></line>
                <line x1="6" y1="6" x2="18" y2="18"></line>
              </svg>
            </button>
          </div>
          <div class="modal-content">
            <p>Are you sure you want to delete this review? This action cannot be undone.</p>
          </div>
          <div class="modal-actions">
            <button class="cancel-btn" @click="showDeleteModal = false">Cancel</button>
            <button class="delete-btn" @click="deleteReview">Delete Review</button>
          </div>
        </div>
      </div>
  
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
  import GradeRadarChart from '@/components/GradeRadarChart.vue'
  import GradeDistribution from '@/components/GradeDistribution.vue'
  import ReviewItem from '@/components/ReviewItem.vue'
  import ReviewForm from '@/components/ReviewForm.vue'
  import AOS from 'aos'
  import 'aos/dist/aos.css'
  import { getDarkModePreference, toggleDarkMode } from '@/services/darkModeService'
  import gradeRadarService from '@/services/gradeRadarService'
  
  export default {
    name: 'ModuleDetail',
    components: { 
      Footer, 
      GradeRadarChart, 
      GradeDistribution, 
      ReviewItem, 
      ReviewForm 
    },
    data() {
      return {
        darkMode: false,
        isScrolled: false,
        loading: true,
        
        // Module data
        moduleId: null,
        moduleData: {
          id: '',
          name: '',
          code: '',
          university: '',
          degree: '',
          year: '',
          semester: '',
          credits: 0,
          statistics: {
            difficulty_avg: 0,
            teaching_quality_avg: 0,
            recommended_avg: 0,
            total_reviews: 0
          },
          reviews: [],
          grade_distribution: []
        },
        
        // Reviews
        reviewSortBy: 'recent',
        showReviewForm: false,
        
        // Delete modal
        showDeleteModal: false,
        reviewToDelete: null,
        
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
      
      // Sort reviews based on selected criteria
      sortedReviews() {
        if (!this.moduleData.reviews) return []
        
        const reviews = [...this.moduleData.reviews]
        
        switch(this.reviewSortBy) {
          case 'recent':
            return reviews.sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
          case 'rating':
            return reviews.sort((a, b) => b.teaching_quality - a.teaching_quality)
          case 'useful':
            return reviews.sort((a, b) => b.helpful_count - a.helpful_count)
          default:
            return reviews
        }
      }
    },
    methods: {
      toggleDarkMode() {
        this.darkMode = toggleDarkMode()
        this.updateGradient()
      },
      
      updateGradient() {
        const container = this.$refs.moduleDetailContainer
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
      
      // Check if the current user is the author of a review
      isReviewAuthor(review) {
        if (!this.isLoggedIn) return false
        
        // In a real app, you'd check the user ID against the review author ID
        return review.is_author === true
      },
      
      // Load module details
      async loadModuleDetails() {
        this.loading = true
        try {
          // Get module ID from route params
          this.moduleId = this.$route.params.id
          
          if (!this.moduleId) {
            this.displayToast('Module ID is required', 'error')
            this.$router.push('/graderadar')
            return
          }
          
          // Load module details
          const response = await gradeRadarService.getModuleDetails(this.moduleId)
          this.moduleData = response.data
          
          // Ensure we have an empty array for reviews if none exist
          if (!this.moduleData.reviews) {
            this.moduleData.reviews = []
          }
          
          // Ensure we have an empty array for grade distribution if none exist
          if (!this.moduleData.grade_distribution) {
            this.moduleData.grade_distribution = []
          }
        } catch (error) {
          console.error('Error loading module details:', error)
          this.displayToast('Error loading module details. Please try again.', 'error')
        } finally {
          this.loading = false
        }
      },
      
      // Handle new review submission
      onReviewSubmitted(review) {
        // Add the new review to the list and update statistics
        this.showReviewForm = false
        this.moduleData.reviews.unshift(review)
        
        // Update statistics (in a real app, this would come from the backend)
        this.loadModuleDetails()
        
        this.displayToast('Your review has been submitted successfully!', 'success')
      },
      
      // Confirm delete review
      confirmDeleteReview(reviewId) {
        this.reviewToDelete = reviewId
        this.showDeleteModal = true
      },
      
      // Delete review
      async deleteReview() {
        if (!this.reviewToDelete) return
        
        try {
          await gradeRadarService.deleteReview(this.reviewToDelete)
          
          // Remove the review from the list
          this.moduleData.reviews = this.moduleData.reviews.filter(
            review => review.id !== this.reviewToDelete
          )
          
          this.displayToast('Review deleted successfully', 'success')
        } catch (error) {
          console.error('Error deleting review:', error)
          this.displayToast('Error deleting review. Please try again.', 'error')
        } finally {
          this.showDeleteModal = false
          this.reviewToDelete = null
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
      
      // Load module details
      this.loadModuleDetails()
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
  .module-detail-container {
    min-height: 100vh;
    background: linear-gradient(to bottom, var(--bg-gradient-from), var(--bg-gradient-to));
    color: var(--text-primary);
    position: relative;
    overflow-x: hidden;
    transition: all var(--transition-medium) ease;
  }
  
  /* -------------- Header/Navigation -------------- */
  .module-detail-header {
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
  
  .module-detail-header.scrolled {
    background-color: rgba(255, 255, 255, 0.8);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    box-shadow: var(--shadow-md);
    padding: 0.75rem 2.5rem;
  }
  
  body.dark-mode .module-detail-header.scrolled {
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
  .module-detail-main {
    padding-top: 6rem;
    min-height: calc(100vh - 6rem);
  }
  
  /* -------------- Module Header Section -------------- */
  .module-header-section {
    padding: 2rem 2.5rem;
  }
  
  .module-header-content {
    max-width: 1200px;
    margin: 0 auto;
    background-color: white;
    border-radius: var(--radius-lg);
    padding: 2rem;
    box-shadow: var(--shadow-md);
  }
  
  body.dark-mode .module-header-content {
    background-color: #1e1e30;
  }
  
  .module-title-area {
    margin-bottom: 1.5rem;
  }
  
  .module-title-area h1 {
    font-size: 2rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
    color: var(--text-primary);
  }
  
  .module-code {
    display: inline-block;
    font-size: 1rem;
    font-weight: 500;
    color: var(--text-secondary);
    background-color: rgba(123, 73, 255, 0.1);
    padding: 0.25rem 0.75rem;
    border-radius: var(--radius-md);
    margin-bottom: 1rem;
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
  
  .module-stats-summary {
    display: flex;
    gap: 2rem;
    flex-wrap: wrap;
  }
  
  .stats-item {
    display: flex;
    flex-direction: column;
    min-width: 120px;
  }
  
  .stat-title {
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
  
  /* -------------- Overview Section -------------- */
  .module-overview-section {
    padding: 2rem 2.5rem;
    max-width: 1200px;
    margin: 0 auto;
  }
  
  .section-header {
    text-align: center;
    margin-bottom: 2rem;
  }
  
  .section-header h2 {
    font-size: 2rem;
    font-weight: 800;
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
  
  .overview-container {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 2rem;
    margin-bottom: 2rem;
  }
  
  .overview-column {
    background-color: white;
    border-radius: var(--radius-lg);
    padding: 1.5rem;
    box-shadow: var(--shadow-md);
  }
  
  body.dark-mode .overview-column {
    background-color: #1e1e30;
  }
  
  /* -------------- Reviews Section -------------- */
  .module-reviews-section {
    padding: 2rem 2.5rem 4rem;
    max-width: 1200px;
    margin: 0 auto;
  }
  
  .reviews-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    text-align: left;
  }
  
  .add-review-btn {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 1rem;
    background-color: var(--primary-color);
    color: white;
    border-radius: var(--radius-md);
    font-weight: 500;
    cursor: pointer;
    transition: all var(--transition-medium) ease;
  }
  
  .add-review-btn:hover {
    background-color: var(--primary-dark);
    transform: translateY(-2px);
  }
  
  .review-form-container {
    margin-bottom: 2rem;
  }
  
  .review-filters {
    display: flex;
    gap: 1rem;
    margin-bottom: 1.5rem;
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
  
  .reviews-list {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }
  
  .no-reviews {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1.5rem;
    padding: 3rem 0;
    text-align: center;
    color: var(--text-secondary);
  }
  
  .no-reviews svg {
    opacity: 0.5;
  }
  
  .no-reviews-btn {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.75rem 1.5rem;
    background-color: var(--primary-color);
    color: white;
    border-radius: var(--radius-full);
    font-weight: 500;
    cursor: pointer;
    transition: all var(--transition-medium) ease;
  }
  
  .no-reviews-btn:hover {
    background-color: var(--primary-dark);
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
  }
  
  .no-reviews-btn svg {
    opacity: 1;
    transition: transform var(--transition-medium) ease;
  }
  
  .no-reviews-btn:hover svg {
    transform: translateX(3px);
  }
  
  /* -------------- Delete Confirmation Modal -------------- */
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 100;
  }
  
  .modal-container {
    width: 95%;
    max-width: 500px;
    background-color: white;
    border-radius: var(--radius-lg);
    overflow: hidden;
    box-shadow: var(--shadow-xl);
    animation: modalFadeIn var(--transition-medium) forwards;
  }
  
  body.dark-mode .modal-container {
    background-color: #1e1e30;
  }
  
  @keyframes modalFadeIn {
    from {
      opacity: 0;
      transform: translateY(20px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
  
  .modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.25rem 1.5rem;
    border-bottom: 1px solid #e0e0e0;
  }
  
  body.dark-mode .modal-header {
    border-bottom-color: #3a3a52;
  }
  
  .modal-header h3 {
    font-size: 1.25rem;
    font-weight: 600;
    color: var(--text-primary);
  }
  
  .modal-close {
    background: transparent;
    border: none;
    color: var(--text-secondary);
    cursor: pointer;
    transition: color var(--transition-fast) ease;
  }
  
  .modal-close:hover {
    color: var(--text-primary);
  }
  
  .modal-content {
    padding: 1.5rem;
    color: var(--text-secondary);
  }
  
  .modal-actions {
    display: flex;
    justify-content: flex-end;
    gap: 1rem;
    padding: 1rem 1.5rem 1.5rem;
  }
  
  .cancel-btn,
  .delete-btn {
    padding: 0.625rem 1.25rem;
    border-radius: var(--radius-md);
    font-weight: 500;
    cursor: pointer;
    transition: all var(--transition-medium) ease;
  }
  
  .cancel-btn {
    background-color: transparent;
    color: var(--text-secondary);
    border: 1px solid #e0e0e0;
  }
  
  body.dark-mode .cancel-btn {
    border-color: #3a3a52;
  }
  
  .cancel-btn:hover {
    border-color: var(--text-primary);
    color: var(--text-primary);
  }
  
  .delete-btn {
    background-color: #ef4444;
    color: white;
    border: none;
  }
  
  .delete-btn:hover {
    background-color: #dc2626;
    box-shadow: var(--shadow-md);
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
    .module-detail-header,
    .module-detail-header.scrolled {
      padding-left: 1.5rem;
      padding-right: 1.5rem;
    }
    
    .module-header-section,
    .module-overview-section,
    .module-reviews-section {
      padding-left: 1.5rem;
      padding-right: 1.5rem;
    }
  }
  
  @media (max-width: 992px) {
    .module-detail-header {
      flex-direction: column;
      align-items: flex-start;
      gap: 1rem;
    }
    
    .header-actions {
      width: 100%;
      justify-content: flex-end;
    }
    
    .overview-container {
      grid-template-columns: 1fr;
    }
    
    .module-title-area h1 {
      font-size: 1.75rem;
    }
  }
  
  @media (max-width: 768px) {
    .module-detail-header,
    .module-detail-header.scrolled {
      padding-left: 1rem;
      padding-right: 1rem;
    }
    
    .breadcrumbs {
      font-size: 0.8rem;
      flex-wrap: wrap;
    }
    
    .module-header-section,
    .module-overview-section,
    .module-reviews-section {
      padding-left: 1rem;
      padding-right: 1rem;
    }
    
    .module-stats-summary {
      flex-direction: column;
      gap: 1rem;
    }
    
    .reviews-header {
      flex-direction: column;
      align-items: flex-start;
      gap: 1rem;
    }
    
    .section-header h2 {
      font-size: 1.5rem;
    }
  }
  
  @media (max-width: 576px) {
    .module-meta {
      flex-direction: column;
      gap: 0.5rem;
    }
    
    .modal-actions {
      flex-direction: column;
    }
    
    .module-title-area h1 {
      font-size: 1.5rem;
    }
  }
</style>