<template>
    <div class="user-reviews-container" ref="userReviewsContainer">
      <!-- Header with breadcrumbs -->
      <header class="user-reviews-header" :class="{ 'scrolled': isScrolled }">
        <div class="breadcrumbs">
          <router-link to="/" class="breadcrumb-item">Home</router-link>
          <span class="breadcrumb-separator">/</span>
          <router-link to="/graderadar" class="breadcrumb-item">GradeRadar</router-link>
          <span class="breadcrumb-separator">/</span>
          <span class="breadcrumb-item active">My Reviews</span>
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
      <main class="user-reviews-main">
        <!-- Loading Indicator -->
        <div v-if="loading" class="loading-container">
          <div class="loading-spinner"></div>
          <div class="loading-text">Loading your reviews...</div>
        </div>
  
        <template v-if="!loading">
          <!-- Section Header -->
          <section class="user-reviews-heading" data-aos="fade-up">
            <h1>My <span class="accent">Reviews</span></h1>
            <p>Manage and view all the reviews you've submitted</p>
          </section>
          
          <!-- Filter controls -->
          <section class="filter-section" data-aos="fade-up">
            <div class="filter-group">
              <label>Sort By</label>
              <select v-model="sortBy">
                <option value="recent">Most Recent</option>
                <option value="university">University</option>
                <option value="module">Module Name</option>
                <option value="rating">Rating (Highest)</option>
              </select>
            </div>
            <div class="search-container">
              <input 
                type="text" 
                v-model="searchQuery" 
                @input="handleSearch" 
                placeholder="Search reviews..."
                class="search-input"
              />
              <svg class="search-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="11" cy="11" r="8"></circle>
                <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
              </svg>
            </div>
          </section>
          
          <!-- Reviews List -->
          <section class="reviews-section" data-aos="fade-up">
            <div v-if="filteredReviews.length > 0" class="reviews-list">
              <div 
                v-for="review in filteredReviews" 
                :key="review.id" 
                class="review-card"
                data-aos="fade-up"
                data-aos-delay="50"
              >
                <div class="review-header">
                  <div class="module-info">
                    <h3>{{ review.module_name }}</h3>
                    <div class="module-meta">
                      <span class="university">{{ review.university }}</span>
                      <span class="degree">{{ review.degree }}</span>
                    </div>
                  </div>
                  <div class="review-actions">
                    <button class="view-btn" @click="goToModule(review.module_id)">
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                        <circle cx="12" cy="12" r="3"></circle>
                      </svg>
                      <span>View Module</span>
                    </button>
                    <button class="delete-btn" @click="confirmDeleteReview(review.id)">
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <polyline points="3 6 5 6 21 6"></polyline>
                        <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                        <line x1="10" y1="11" x2="10" y2="17"></line>
                        <line x1="14" y1="11" x2="14" y2="17"></line>
                      </svg>
                      <span>Delete</span>
                    </button>
                  </div>
                </div>
                <div class="review-stats">
                  <div class="rating-item">
                    <div class="rating-label">Difficulty</div>
                    <div class="rating-value">
                      <div class="rating-stars">
                        <div class="stars-background">★★★★★</div>
                        <div class="stars-filled" :style="{ width: calculateStarWidth(review.difficulty) }">★★★★★</div>
                      </div>
                      <span>{{ review.difficulty }}</span>
                    </div>
                  </div>
                  <div class="rating-item">
                    <div class="rating-label">Teaching Quality</div>
                    <div class="rating-value">
                      <div class="rating-stars">
                        <div class="stars-background">★★★★★</div>
                        <div class="stars-filled" :style="{ width: calculateStarWidth(review.teaching_quality) }">★★★★★</div>
                      </div>
                      <span>{{ review.teaching_quality }}</span>
                    </div>
                  </div>
                  <div class="rating-item">
                    <div class="rating-label">Recommended</div>
                    <div class="rating-value">{{ review.recommended ? 'Yes' : 'No' }}</div>
                  </div>
                  <div class="rating-item">
                    <div class="rating-label">Date</div>
                    <div class="rating-value">{{ formatDate(review.created_at) }}</div>
                  </div>
                </div>
                <div v-if="review.comment" class="review-comment">
                  <p>{{ review.comment }}</p>
                </div>
              </div>
            </div>
            
            <!-- No Reviews Found -->
            <div v-else class="no-reviews">
              <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round">
                <path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"></path>
                <rect x="8" y="2" width="8" height="4" rx="1" ry="1"></rect>
                <circle cx="12" cy="14" r="4"></circle>
                <path d="M12 10v1"></path>
                <path d="M12 17v.01"></path>
              </svg>
              <p v-if="searchQuery">No reviews found matching your search. Try adjusting your search criteria.</p>
              <p v-else>You haven't submitted any reviews yet. Start by reviewing modules you've taken!</p>
              <router-link to="/graderadar" class="explore-btn">
                <span>Explore Modules</span>
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M5 12h14"></path>
                  <path d="M12 5l7 7-7 7"></path>
                </svg>
              </router-link>
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
  import AOS from 'aos'
  import 'aos/dist/aos.css'
  import { getDarkModePreference, toggleDarkMode } from '@/services/darkModeService'
  import gradeRadarService from '@/services/gradeRadarService'
  
  export default {
    name: 'UserReviews',
    components: { Footer },
    data() {
      return {
        darkMode: false,
        isScrolled: false,
        loading: true,
        searchQuery: '',
        
        // Reviews
        reviews: [],
        sortBy: 'recent',
        
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
      // Filter and sort reviews
      filteredReviews() {
        let filtered = [...this.reviews]
        
        // Apply search filter
        if (this.searchQuery) {
          const query = this.searchQuery.toLowerCase()
          filtered = filtered.filter(review => 
            review.module_name.toLowerCase().includes(query) || 
            review.university.toLowerCase().includes(query) || 
            review.degree.toLowerCase().includes(query) ||
            (review.comment && review.comment.toLowerCase().includes(query))
          )
        }
        
        // Apply sorting
        switch(this.sortBy) {
          case 'recent':
            filtered.sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
            break
          case 'university':
            filtered.sort((a, b) => a.university.localeCompare(b.university))
            break
          case 'module':
            filtered.sort((a, b) => a.module_name.localeCompare(b.module_name))
            break
          case 'rating':
            filtered.sort((a, b) => b.teaching_quality - a.teaching_quality)
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
        const container = this.$refs.userReviewsContainer
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
      
      // Calculate width for star rating display
      calculateStarWidth(rating) {
        return `${(rating / 5) * 100}%`
      },
      
      // Format date
      formatDate(dateString) {
        if (!dateString) return 'Unknown date'
        
        const options = { year: 'numeric', month: 'short', day: 'numeric' }
        return new Date(dateString).toLocaleDateString(undefined, options)
      },
      
      // Navigate to module details
      goToModule(moduleId) {
        if (!moduleId) return
        this.$router.push(`/graderadar/module/${moduleId}`)
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
          this.reviews = this.reviews.filter(
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
      
      // Load user reviews
      async loadUserReviews() {
        this.loading = true
        try {
          const response = await gradeRadarService.getUserReviews()
          this.reviews = response.data || []
        } catch (error) {
          console.error('Error loading user reviews:', error)
          this.displayToast('Error loading your reviews. Please try again.', 'error')
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
      
      // Load user reviews
      this.loadUserReviews()
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
  .user-reviews-container {
    min-height: 100vh;
    background: linear-gradient(to bottom, var(--bg-gradient-from), var(--bg-gradient-to));
    color: var(--text-primary);
    position: relative;
    overflow-x: hidden;
    transition: all var(--transition-medium) ease;
  }
  
  /* -------------- Header/Navigation -------------- */
  .user-reviews-header {
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
  
  .user-reviews-header.scrolled {
    background-color: rgba(255, 255, 255, 0.8);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    box-shadow: var(--shadow-md);
    padding: 0.75rem 2.5rem;
  }
  
  body.dark-mode .user-reviews-header.scrolled {
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
  .user-reviews-main {
    padding-top: 6rem;
    min-height: calc(100vh - 6rem);
    max-width: 1200px;
    margin: 0 auto;
    padding-left: 2.5rem;
    padding-right: 2.5rem;
  }
  
  .user-reviews-heading {
    text-align: center;
    margin-bottom: 2rem;
    padding-top: 2rem;
  }
  
  .user-reviews-heading h1 {
    font-size: 2.5rem;
    font-weight: 800;
    margin-bottom: 0.5rem;
    color: var(--text-primary);
  }
  
  .user-reviews-heading p {
    font-size: 1.125rem;
    color: var(--text-secondary);
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
  
  /* -------------- Filter Section -------------- */
  .filter-section {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2rem;
    flex-wrap: wrap;
    gap: 1rem;
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
    padding: 0.625rem 1rem;
    border: 1px solid #e0e0e0;
    border-radius: var(--radius-md);
    font-size: 0.95rem;
    background-color: white;
    color: var(--text-primary);
    min-width: 180px;
  }
  
  body.dark-mode .filter-group select {
    border-color: #3a3a52;
    background-color: #252538;
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
  
  /* -------------- Reviews Section -------------- */
  .reviews-section {
    margin-bottom: 4rem;
  }
  
  .reviews-list {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
  }
  
  .review-card {
    background-color: white;
    border-radius: var(--radius-lg);
    padding: 1.5rem;
    box-shadow: var(--shadow-md);
    transition: all var(--transition-medium) ease;
  }
  
  body.dark-mode .review-card {
    background-color: #1e1e30;
  }
  
  .review-card:hover {
    transform: translateY(-3px);
    box-shadow: var(--shadow-lg);
  }
  
  .review-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 1.5rem;
    flex-wrap: wrap;
    gap: 1rem;
  }
  
  .module-info h3 {
    font-size: 1.25rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
    color: var(--text-primary);
  }
  
  .module-meta {
    display: flex;
    align-items: center;
    gap: 1rem;
    color: var(--text-secondary);
    font-size: 0.875rem;
  }
  
  .university {
    font-weight: 500;
  }
  
  .degree {
    color: var(--text-secondary);
    opacity: 0.8;
  }
  
  .review-actions {
    display: flex;
    gap: 0.75rem;
  }
  
  .view-btn,
  .delete-btn {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 0.75rem;
    border-radius: var(--radius-md);
    font-size: 0.875rem;
    font-weight: 500;
    cursor: pointer;
    transition: all var(--transition-medium) ease;
  }
  
  .view-btn {
    background-color: rgba(123, 73, 255, 0.1);
    color: var(--primary-color);
    border: none;
  }
  
  .view-btn:hover {
    background-color: rgba(123, 73, 255, 0.2);
  }
  
  .delete-btn {
    background-color: rgba(239, 68, 68, 0.1);
    color: #ef4444;
    border: none;
  }
  
  .delete-btn:hover {
    background-color: rgba(239, 68, 68, 0.2);
  }
  
  .review-stats {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 1rem;
    margin-bottom: 1.5rem;
  }
  
  .rating-item {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
  }
  
  .rating-label {
    font-size: 0.875rem;
    color: var(--text-secondary);
  }
  
  .rating-value {
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
  
  .review-comment {
    padding-top: 1rem;
    border-top: 1px solid #e0e0e0;
    color: var(--text-primary);
    line-height: 1.6;
  }
  
  body.dark-mode .review-comment {
    border-top-color: #3a3a52;
  }
  
  /* -------------- No Reviews Found -------------- */
  .no-reviews {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1.5rem;
    padding: 4rem 0;
    text-align: center;
    color: var(--text-secondary);
  }
  
  .no-reviews svg {
    opacity: 0.5;
  }
  
  .explore-btn {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.75rem 1.5rem;
    background-color: var(--primary-color);
    color: white;
    border-radius: var(--radius-full);
    font-weight: 500;
    text-decoration: none;
    transition: all var(--transition-medium) ease;
  }
  
  .explore-btn:hover {
    background-color: var(--primary-dark);
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
  }
  
  .explore-btn svg {
    opacity: 1;
    transition: transform var(--transition-medium) ease;
  }
  
  .explore-btn:hover svg {
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
    .user-reviews-header,
    .user-reviews-header.scrolled {
      padding-left: 1.5rem;
      padding-right: 1.5rem;
    }
    
    .user-reviews-main {
      padding-left: 1.5rem;
      padding-right: 1.5rem;
    }
  }
  
  @media (max-width: 992px) {
    .user-reviews-header {
      flex-direction: column;
      align-items: flex-start;
      gap: 1rem;
    }
    
    .header-actions {
      width: 100%;
      justify-content: flex-end;
    }
    
    .user-reviews-heading h1 {
      font-size: 2rem;
    }
    
    .review-header {
      flex-direction: column;
      align-items: flex-start;
    }
    
    .review-actions {
      width: 100%;
      justify-content: flex-end;
    }
  }
  
  @media (max-width: 768px) {
    .user-reviews-header,
    .user-reviews-header.scrolled {
      padding-left: 1rem;
      padding-right: 1rem;
    }
    
    .breadcrumbs {
      font-size: 0.8rem;
      flex-wrap: wrap;
    }
    
    .user-reviews-main {
      padding-left: 1rem;
      padding-right: 1rem;
    }
    
    .filter-section {
      flex-direction: column;
      align-items: stretch;
    }
    
    .search-container {
      width: 100%;
    }
    
    .search-input {
      width: 100%;
    }
    
    .search-input:focus {
      width: 100%;
    }
    
    .review-stats {
      grid-template-columns: 1fr 1fr;
    }
  }
  
  @media (max-width: 576px) {
    .user-reviews-heading h1 {
      font-size: 1.75rem;
    }
    
    .review-stats {
      grid-template-columns: 1fr;
    }
    
    .modal-actions {
      flex-direction: column;
    }
  }
  </style>