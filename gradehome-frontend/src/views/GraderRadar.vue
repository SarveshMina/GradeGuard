<template>
  <div class="graderadar" :class="{ 'dark-mode': darkMode }">
    <!-- Page Header -->
    <div class="page-header">
      <h1>GradeRadar Analytics</h1>
      <p class="header-description">
        Discover insights about universities, degrees, and modules from real student data
      </p>
    </div>

    <!-- Breadcrumb Navigation -->
    <div class="breadcrumb">
      <div class="breadcrumb-item" @click="navigateTo('universities')">
        <span>Universities</span>
      </div>
      <div v-if="selectedUniversity" class="breadcrumb-separator">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <polyline points="9 18 15 12 9 6"></polyline>
        </svg>
      </div>
      <div v-if="selectedUniversity" class="breadcrumb-item" @click="navigateTo('degrees')">
        <span>{{ selectedUniversity }}</span>
      </div>
      <div v-if="selectedDegree" class="breadcrumb-separator">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <polyline points="9 18 15 12 9 6"></polyline>
        </svg>
      </div>
      <div v-if="selectedDegree" class="breadcrumb-item" @click="navigateTo('modules')">
        <span>{{ selectedDegree }}</span>
      </div>
      <div v-if="selectedModule" class="breadcrumb-separator">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <polyline points="9 18 15 12 9 6"></polyline>
        </svg>
      </div>
      <div v-if="selectedModule" class="breadcrumb-item">
        <span>{{ selectedModule }}</span>
      </div>
    </div>

    <!-- Search bar - shown when on universities screen -->
    <div v-if="currentView === 'universities'" class="search-container">
      <div class="search-bar">
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="11" cy="11" r="8"></circle>
          <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
        </svg>
        <input 
          type="text" 
          v-model="searchQuery" 
          placeholder="Search for a university..." 
          @input="debounceSearch"
          @keyup.enter="performSearch"
        />
        <button 
          v-if="searchQuery" 
          class="search-clear" 
          @click="clearSearch"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        </button>
      </div>
    </div>

    <!-- Loading Indicator -->
    <div v-if="loading" class="loading-container">
      <div class="loading-spinner"></div>
      <div class="loading-text">Loading data...</div>
    </div>

    <!-- Error Message -->
    <div v-if="error" class="error-container">
      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="10"></circle>
        <line x1="12" y1="8" x2="12" y2="12"></line>
        <line x1="12" y1="16" x2="12.01" y2="16"></line>
      </svg>
      <p>{{ error }}</p>
      <button @click="retryFetch" class="retry-button">Retry</button>
    </div>

    <!-- Search Empty State -->
    <div v-if="searchPerformed && universities.length === 0 && !loading && !error" class="empty-state">
      <div class="empty-icon">
        <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="11" cy="11" r="8"></circle>
          <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
        </svg>
      </div>
      <h2>No universities found</h2>
      <p>We couldn't find any universities matching "{{ searchQuery }}"</p>
      <button @click="clearSearch" class="action-button">Clear Search</button>
    </div>

    <!-- Main Content Sections -->
    <!-- 1. Universities View -->
    <div v-if="currentView === 'universities' && !loading && !error && universities.length > 0" class="content-section">
      <h2 class="section-title">
        {{ searchPerformed ? `Search Results for "${searchQuery}"` : 'Top Universities' }}
      </h2>
      <div class="university-grid">
        <div 
          v-for="university in universities" 
          :key="university.name"
          class="university-card"
          @click="selectUniversity(university.name)"
        >
          <div class="university-icon">
            {{ university.name.charAt(0) }}
          </div>
          <div class="university-details">
            <h3>{{ university.name }}</h3>
            <div class="university-stats">
              <div class="stat-item">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                  <circle cx="12" cy="7" r="4"></circle>
                </svg>
                <span>{{ university.studentCount }} Students</span>
              </div>
              <div class="stat-item">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M22 10v6M2 10l10-5 10 5-10 5z"></path>
                  <path d="M6 12v5c3 3 9 3 12 0v-5"></path>
                </svg>
                <span>{{ university.degreeCount }} Degrees</span>
              </div>
            </div>
          </div>
          <div class="card-arrow">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M9 18l6-6-6-6"></path>
            </svg>
          </div>
        </div>
      </div>
    </div>

    <!-- 2. Degrees View -->
    <div v-if="currentView === 'degrees' && !loading && !error && degrees.length > 0" class="content-section">
      <h2 class="section-title">
        Degrees at {{ selectedUniversity }}
      </h2>
      <div class="degree-grid">
        <div 
          v-for="degree in degrees" 
          :key="degree.name"
          class="degree-card"
          @click="selectDegree(degree.name)"
        >
          <div class="degree-header">
            <h3>{{ degree.name }}</h3>
          </div>
          <div class="degree-stats">
            <div class="stat-circle">
              <div class="stat-value">{{ degree.studentCount }}</div>
              <div class="stat-label">Students</div>
            </div>
            <div class="stat-circle">
              <div class="stat-value">{{ degree.moduleCount }}</div>
              <div class="stat-label">Modules</div>
            </div>
          </div>
          <div class="degree-footer">
            <button class="view-button">View Modules</button>
          </div>
        </div>
      </div>
    </div>

    <!-- 3. Modules View -->
    <div v-if="currentView === 'modules' && !loading && !error && moduleGroups.length > 0" class="content-section">
      <h2 class="section-title">
        {{ selectedDegree }} Modules at {{ selectedUniversity }}
      </h2>
      <div class="module-filters">
        <div class="filter-control">
          <label for="yearFilter">Filter by Year:</label>
          <select id="yearFilter" v-model="yearFilter">
            <option value="all">All Years</option>
            <option v-for="year in availableYears" :key="year" :value="year">Year {{ year }}</option>
          </select>
        </div>
        <div class="filter-control">
          <label for="sortBy">Sort by:</label>
          <select id="sortBy" v-model="sortBy">
            <option value="name">Module Name</option>
            <option value="score">Average Score</option>
            <option value="students">Student Count</option>
          </select>
        </div>
      </div>

      <div 
        v-for="group in filteredModuleGroups" 
        :key="group.year"
        class="module-year-group"
      >
        <div class="year-header">
          <h3>Year {{ group.year }}</h3>
          <div class="year-stats">{{ group.modules.length }} modules</div>
        </div>
        <div class="modules-list">
          <div 
            v-for="module in sortedModules(group.modules)" 
            :key="module.name"
            class="module-card"
            @click="selectModule(module.name)"
          >
            <div class="module-score-badge" :class="getScoreClass(module.averageScore)">
              {{ module.averageScore }}%
            </div>
            <div class="module-details">
              <h4>{{ module.name }}</h4>
              <div class="module-code" v-if="module.code">{{ module.code }}</div>
              <div class="module-stats">
                <div class="stat-item">
                  <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                    <circle cx="12" cy="7" r="4"></circle>
                  </svg>
                  <span>{{ module.studentCount }} Students</span>
                </div>
                <div class="stat-item">
                  <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                    <line x1="9" y1="3" x2="9" y2="21"></line>
                  </svg>
                  <span>{{ module.semester === 0 ? 'Full Year' : `Semester ${module.semester}` }}</span>
                </div>
              </div>
            </div>
            <div class="card-arrow">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M9 18l6-6-6-6"></path>
              </svg>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 4. Module Details View -->
    <div v-if="currentView === 'moduleDetails' && !loading && !error && moduleDetails" class="content-section">
      <div class="module-details-container">
        <div class="module-details-header">
          <div class="module-details-title">
            <h2>{{ moduleDetails.name }}</h2>
            <div v-if="moduleDetails.code" class="module-code-badge">{{ moduleDetails.code }}</div>
          </div>
          <div class="module-meta">
            <div class="meta-item">
              <span class="meta-label">Year:</span>
              <span class="meta-value">{{ moduleDetails.year }}</span>
            </div>
            <div class="meta-item">
              <span class="meta-label">Semester:</span>
              <span class="meta-value">{{ moduleDetails.semester === 0 ? 'Full Year' : moduleDetails.semester }}</span>
            </div>
            <div class="meta-item">
              <span class="meta-label">Students:</span>
              <span class="meta-value">{{ moduleDetails.studentCount }}</span>
            </div>
            <div class="meta-item">
              <span class="meta-label">Last Updated:</span>
              <span class="meta-value">{{ formatDate(moduleDetails.lastUpdated) }}</span>
            </div>
          </div>
        </div>

        <!-- Module Score Card -->
        <div class="module-metrics">
          <div class="score-card">
            <div class="score-circle" :class="getScoreClass(moduleDetails.averageScore)">
              <div class="score-value">{{ moduleDetails.averageScore }}%</div>
              <div class="score-label">Average Score</div>
            </div>
            <div class="score-stats">
              <div class="score-stat-item">
                <div class="stat-value">{{ moduleDetails.highestScore }}%</div>
                <div class="stat-label">Highest Score</div>
              </div>
              <div class="score-stat-item">
                <div class="stat-value">{{ moduleDetails.lowestScore }}%</div>
                <div class="stat-label">Lowest Score</div>
              </div>
            </div>
          </div>
        </div>

        <!-- Grade Distribution Chart -->
        <div class="chart-section">
          <h3>Grade Distribution</h3>
          <div class="chart-container grade-chart">
            <div v-if="!loading" class="grade-distribution">
              <div
                v-for="(grade, index) in moduleDetails.gradeDistribution"
                :key="index"
                class="grade-bar-container"
              >
                <div class="grade-label">{{ grade.range }}</div>
                <div class="grade-bar-wrapper">
                  <div
                    class="grade-bar"
                    :style="{
                      width: `${calculateBarPercentage(grade.count)}%`,
                      backgroundColor: getGradeColor(grade.range)
                    }"
                  ></div>
                  <div class="grade-count">{{ grade.count }}</div>
                </div>
                <div class="grade-percentage">{{ calculateGradePercentage(grade.count) }}%</div>
              </div>
            </div>
          </div>
        </div>

        <!-- Related Modules -->
        <div class="related-modules-section">
          <h3>Related Modules in {{ selectedDegree }}</h3>
          <div class="related-modules-grid">
            <div 
              v-for="module in moduleDetails.relatedModules" 
              :key="module.name"
              class="related-module-card"
              @click="selectModule(module.name)"
            >
              <div class="module-score-badge" :class="getScoreClass(module.averageScore)">
                {{ module.averageScore }}%
              </div>
              <div class="module-details">
                <h4>{{ module.name }}</h4>
                <div class="module-code" v-if="module.code">{{ module.code }}</div>
                <div class="module-stats">
                  <div class="stat-item">
                    <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                      <circle cx="12" cy="7" r="4"></circle>
                    </svg>
                    <span>{{ module.studentCount }} Students</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { getDarkModePreference } from '@/services/darkModeService.js';
import { API_URL } from '@/config.js';

export default {
  name: 'GradeRadar',
  data() {
    return {
      // UI state
      loading: false,
      error: null,
      darkMode: false,
      currentView: 'universities', // universities, degrees, modules, moduleDetails
      
      // Data
      universities: [],
      degrees: [],
      modules: [],
      moduleGroups: [],
      moduleDetails: null,
      
      // Selection tracking
      selectedUniversity: null,
      selectedDegree: null,
      selectedModule: null,
      
      // Search
      searchQuery: '',
      searchPerformed: false,
      searchTimeout: null,
      
      // Filters and sorting
      yearFilter: 'all',
      sortBy: 'name',
    };
  },
  
  computed: {
    availableYears() {
      // Extract unique years from modules
      if (!this.moduleGroups || this.moduleGroups.length === 0) return [];
      return this.moduleGroups.map(group => group.year).sort((a, b) => a - b);
    },
    
    filteredModuleGroups() {
      if (this.yearFilter === 'all') {
        return this.moduleGroups;
      } else {
        return this.moduleGroups.filter(group => group.year === parseInt(this.yearFilter));
      }
    }
  },
  
  methods: {
    // Navigation methods
    navigateTo(view) {
      switch(view) {
        case 'universities':
          this.currentView = 'universities';
          this.selectedUniversity = null;
          this.selectedDegree = null;
          this.selectedModule = null;
          this.fetchTopUniversities();
          break;
        case 'degrees':
          if (this.selectedUniversity) {
            this.currentView = 'degrees';
            this.selectedDegree = null;
            this.selectedModule = null;
            this.fetchUniversityDegrees(this.selectedUniversity);
          }
          break;
        case 'modules':
          if (this.selectedUniversity && this.selectedDegree) {
            this.currentView = 'modules';
            this.selectedModule = null;
            this.fetchDegreeModules(this.selectedUniversity, this.selectedDegree);
          }
          break;
      }
    },
    
    selectUniversity(universityName) {
      this.selectedUniversity = universityName;
      this.fetchUniversityDegrees(universityName);
    },
    
    selectDegree(degreeName) {
      this.selectedDegree = degreeName;
      this.fetchDegreeModules(this.selectedUniversity, degreeName);
    },
    
    selectModule(moduleName) {
      this.selectedModule = moduleName;
      this.fetchModuleDetails(this.selectedUniversity, this.selectedDegree, moduleName);
    },
    
    // Search methods
    debounceSearch() {
      clearTimeout(this.searchTimeout);
      this.searchTimeout = setTimeout(() => {
        if (this.searchQuery.length >= 2) {
          this.performSearch();
        } else if (this.searchQuery.length === 0 && this.searchPerformed) {
          this.clearSearch();
        }
      }, 300);
    },
    
    performSearch() {
      if (this.searchQuery.length >= 2) {
        this.searchPerformed = true;
        this.fetchSearchResults(this.searchQuery);
      }
    },
    
    clearSearch() {
      this.searchQuery = '';
      this.searchPerformed = false;
      this.fetchTopUniversities();
    },
    
    // API methods
    async fetchTopUniversities() {
      this.loading = true;
      this.error = null;
      this.currentView = 'universities';
      
      try {
        const response = await axios.get(`${API_URL}/api/analytics/top-universities`);
        this.universities = response.data;
        this.loading = false;
      } catch (err) {
        this.error = 'Failed to load universities. Please try again.';
        this.loading = false;
        console.error('Error fetching top universities:', err);
      }
    },
    
    async fetchSearchResults(query) {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await axios.get(`${API_URL}/api/analytics/search-university`, {
          params: { query }
        });
        this.universities = response.data;
        this.loading = false;
      } catch (err) {
        this.error = 'Failed to search universities. Please try again.';
        this.loading = false;
        console.error('Error searching universities:', err);
      }
    },
    
    async fetchUniversityDegrees(university) {
      this.loading = true;
      this.error = null;
      this.currentView = 'degrees';
      
      try {
        const response = await axios.get(`${API_URL}/api/analytics/university-degrees`, {
          params: { university }
        });
        this.degrees = response.data;
        this.loading = false;
      } catch (err) {
        this.error = `Failed to load degrees for ${university}. Please try again.`;
        this.loading = false;
        console.error('Error fetching university degrees:', err);
      }
    },
    
    async fetchDegreeModules(university, degree) {
      this.loading = true;
      this.error = null;
      this.currentView = 'modules';
      
      try {
        const response = await axios.get(`${API_URL}/api/analytics/degree-modules`, {
          params: { university, degree }
        });
        
        // Response should have both grouped and flat module lists
        this.moduleGroups = response.data.byYear;
        this.modules = response.data.modules;
        
        // Reset filters
        this.yearFilter = 'all';
        this.sortBy = 'name';
        
        this.loading = false;
      } catch (err) {
        this.error = `Failed to load modules for ${degree} at ${university}. Please try again.`;
        this.loading = false;
        console.error('Error fetching degree modules:', err);
      }
    },
    
    async fetchModuleDetails(university, degree, module) {
      this.loading = true;
      this.error = null;
      this.currentView = 'moduleDetails';
      
      try {
        const response = await axios.get(`${API_URL}/api/analytics/module-details`, {
          params: { university, degree, module }
        });
        this.moduleDetails = response.data;
        this.loading = false;
      } catch (err) {
        this.error = `Failed to load details for ${module}. Please try again.`;
        this.loading = false;
        console.error('Error fetching module details:', err);
      }
    },
    
    retryFetch() {
      switch(this.currentView) {
        case 'universities':
          this.fetchTopUniversities();
          break;
        case 'degrees':
          this.fetchUniversityDegrees(this.selectedUniversity);
          break;
        case 'modules':
          this.fetchDegreeModules(this.selectedUniversity, this.selectedDegree);
          break;
        case 'moduleDetails':
          this.fetchModuleDetails(this.selectedUniversity, this.selectedDegree, this.selectedModule);
          break;
      }
    },
    
    // Utility methods
    getScoreClass(score) {
      if (score >= 70) return 'excellent';
      if (score >= 60) return 'good';
      if (score >= 50) return 'average';
      if (score >= 40) return 'pass';
      return 'fail';
    },
    
    formatDate(dateString) {
      if (!dateString) return 'Unknown';
      
      const date = new Date(dateString);
      return date.toLocaleDateString('en-GB', {
        day: 'numeric',
        month: 'short',
        year: 'numeric'
      });
    },
    
    sortedModules(modules) {
      if (!modules) return [];
      
      // Create a copy to avoid modifying the original array
      const sorted = [...modules];
      
      switch(this.sortBy) {
        case 'name':
          return sorted.sort((a, b) => a.name.localeCompare(b.name));
        case 'score':
          return sorted.sort((a, b) => b.averageScore - a.averageScore);
        case 'students':
          return sorted.sort((a, b) => b.studentCount - a.studentCount);
        default:
          return sorted;
      }
    },
    
    calculateBarPercentage(count) {
      if (!this.moduleDetails || !this.moduleDetails.studentCount || this.moduleDetails.studentCount === 0) return 0;
      
      // Calculate percentage based on total students
      return Math.min(100, Math.round((count / this.moduleDetails.studentCount) * 100));
    },
    
    calculateGradePercentage(count) {
      if (!this.moduleDetails || !this.moduleDetails.studentCount || this.moduleDetails.studentCount === 0) return 0;
      
      // Calculate percentage of students in this grade range
      return Math.round((count / this.moduleDetails.studentCount) * 100);
    },
    
    getGradeColor(range) {
      // Extract the first number from the range string (e.g., "70-100%" -> 70)
      const lowerBound = parseInt(range.split('-')[0]);
      
      if (lowerBound >= 70) return '#2ecc71'; // Excellent - green
      if (lowerBound >= 60) return '#3498db'; // Good - blue
      if (lowerBound >= 50) return '#f1c40f'; // Average - yellow
      if (lowerBound >= 40) return '#e67e22'; // Pass - orange
      return '#e74c3c'; // Fail - red
    }
  },
  
  created() {
    // Check dark mode preference
    this.darkMode = getDarkModePreference();
    
    // Add event listener for dark mode changes
    window.addEventListener('darkModeChange', (e) => {
      this.darkMode = e.detail.isDark;
    });
  },
  
  mounted() {
    // Fetch initial data
    this.fetchTopUniversities();
  },
  
  beforeDestroy() {
    // Remove event listener
    window.removeEventListener('darkModeChange');
  }
};
</script>

<style scoped>
.graderadar {
  padding: 2rem;
  background-color: var(--bg-light);
  color: var(--text-primary);
  transition: background-color 0.3s ease, color 0.3s ease;
  min-height: calc(100vh - 70px);
  font-family: var(--font-main, 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif);
  --bg-light: #f8f9fa;
  --bg-card: #ffffff;
  --bg-accent: #f1f3f9;
  --bg-input: #ffffff;
  --text-primary: #333333;
  --text-secondary: #667085;
  --text-muted: #94a3b8;
  --primary-color: #7b49ff;
  --primary-dark: #6038cc;
  --primary-light: #9a73ff;
  --success-color: #22c55e;
  --info-color: #3b82f6;
  --warning-color: #f59e0b;
  --danger-color: #ef4444;
  --border-color: #e2e8f0;
  --border-color-light: #f1f5f9;
  --border-radius: 8px;
  --border-radius-lg: 12px;
  --transition-speed: 0.3s;
  --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 12px rgba(0, 0, 0, 0.07);
  --shadow-lg: 0 10px 25px rgba(0, 0, 0, 0.1);
}

.graderadar.dark-mode {
  --bg-light: #111827;
  --bg-card: #1f2937;
  --bg-accent: #2d3748;
  --bg-input: #374151;
  --text-primary: #f1f5f9;
  --text-secondary: #cbd5e1;
  --text-muted: #94a3b8;
  --primary-color: #8b5cf6;
  --primary-dark: #7c3aed;
  --primary-light: #a78bfa;
  --border-color: #374151;
  --border-color-light: #4b5563;
}

/* Page Header */
.page-header {
  margin-bottom: 2rem;
}

.page-header h1 {
  font-size: 2.25rem;
  font-weight: 800;
  margin: 0 0 0.5rem;
  background: linear-gradient(90deg, var(--primary-color), var(--primary-light));
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  display: inline-block;
}

.header-description {
  color: var(--text-secondary);
  font-size: 1.1rem;
  margin: 0;
}

/* Breadcrumb Navigation */
.breadcrumb {
  display: flex;
  align-items: center;
  margin-bottom: 1.5rem;
  padding: 0.75rem 1rem;
  background-color: var(--bg-card);
  border-radius: var(--border-radius);
  box-shadow: var(--shadow-sm);
  overflow-x: auto;
  white-space: nowrap;
  border: 1px solid var(--border-color-light);
}

.breadcrumb-item {
  display: flex;
  align-items: center;
  font-weight: 500;
  cursor: pointer;
  padding: 0.25rem 0.5rem;
  border-radius: var(--border-radius);
  transition: all 0.2s ease;
}

.breadcrumb-item:hover {
  background-color: var(--bg-accent);
  color: var(--primary-color);
}

.breadcrumb-item:last-child {
  font-weight: 600;
  color: var(--primary-color);
  cursor: default;
}

.breadcrumb-item:last-child:hover {
  background-color: transparent;
}

.breadcrumb-separator {
  margin: 0 0.25rem;
  color: var(--text-muted);
  display: flex;
  align-items: center;
}

/* Search Bar */
.search-container {
  margin-bottom: 2rem;
}

.search-bar {
  display: flex;
  align-items: center;
  background-color: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-lg);
  padding: 0 1rem;
  box-shadow: var(--shadow-sm);
  transition: all 0.2s ease;
}

.search-bar:focus-within {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 2px rgba(123, 73, 255, 0.1);
}

.search-bar svg {
  color: var(--text-muted);
  margin-right: 0.75rem;
}

.search-bar input {
  flex: 1;
  padding: 0.85rem 0;
  border: none;
  background: transparent;
  color: var(--text-primary);
  font-size: 1rem;
  outline: none;
}

.search-bar input::placeholder {
  color: var(--text-muted);
}

.search-clear {
  background: transparent;
  border: none;
  color: var(--text-muted);
  cursor: pointer;
  display: flex;
  align-items: center;
  padding: 0.5rem;
  border-radius: 50%;
  transition: all 0.2s ease;
}

.search-clear:hover {
  background-color: var(--bg-accent);
  color: var(--text-primary);
}

/* Loading Indicator */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem;
  text-align: center;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid rgba(123, 73, 255, 0.1);
  border-radius: 50%;
  border-top: 4px solid var(--primary-color);
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-text {
  color: var(--text-secondary);
  font-weight: 500;
}

/* Error Message */
.error-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem;
  text-align: center;
  background-color: rgba(239, 68, 68, 0.05);
  border-radius: var(--border-radius-lg);
  border: 1px solid rgba(239, 68, 68, 0.2);
  margin-bottom: 2rem;
}

.error-container svg {
  color: var(--danger-color);
  margin-bottom: 1rem;
}

.error-container p {
  color: var(--text-primary);
  font-weight: 500;
  margin-bottom: 1.5rem;
}

.retry-button {
  padding: 0.6rem 1.5rem;
  background-color: var(--primary-color);
  color: white;
  border: none;
  border-radius: var(--border-radius);
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.retry-button:hover {
  background-color: var(--primary-dark);
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

/* Empty State */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  text-align: center;
  background-color: var(--bg-card);
  border-radius: var(--border-radius-lg);
  border: 1px solid var(--border-color);
  margin-bottom: 2rem;
}

.empty-icon {
  color: var(--text-muted);
  margin-bottom: 1.5rem;
}

.empty-state h2 {
  font-size: 1.5rem;
  font-weight: 700;
  margin: 0 0 0.75rem;
  color: var(--text-primary);
}

.empty-state p {
  color: var(--text-secondary);
  margin-bottom: 1.5rem;
}

.action-button {
  padding: 0.6rem 1.5rem;
  background-color: var(--bg-accent);
  color: var(--primary-color);
  border: 1px solid var(--primary-color);
  border-radius: var(--border-radius);
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.action-button:hover {
  background-color: rgba(123, 73, 255, 0.1);
  transform: translateY(-2px);
}

/* Content Sections */
.content-section {
  margin-bottom: 3rem;
}

.section-title {
  font-size: 1.5rem;
  font-weight: 700;
  margin: 0 0 1.5rem;
  color: var(--text-primary);
  position: relative;
  padding-bottom: 0.75rem;
}

.section-title::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 50px;
  height: 3px;
  background-color: var(--primary-color);
  border-radius: 3px;
}

/* University Grid */
.university-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.university-card {
  display: flex;
  align-items: center;
  background-color: var(--bg-card);
  border-radius: var(--border-radius-lg);
  padding: 1.5rem;
  box-shadow: var(--shadow-md);
  transition: all 0.2s ease;
  cursor: pointer;
  border: 1px solid var(--border-color-light);
}

.university-card:hover {
  transform: translateY(-5px);
  box-shadow: var(--shadow-lg);
  border-color: var(--primary-light);
}

.university-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, var(--primary-color), var(--primary-light));
  color: white;
  font-size: 1.75rem;
  font-weight: 700;
  border-radius: var(--border-radius);
  margin-right: 1.25rem;
  flex-shrink: 0;
  box-shadow: 0 4px 10px rgba(123, 73, 255, 0.3);
}

.university-details {
  flex: 1;
}

.university-details h3 {
  margin: 0 0 0.75rem;
  font-size: 1.15rem;
  font-weight: 700;
  color: var(--text-primary);
}

.university-stats {
  display: flex;
  gap: 1rem;
}

.stat-item {
  display: flex;
  align-items: center;
  color: var(--text-secondary);
  font-size: 0.9rem;
}

.stat-item svg {
  margin-right: 0.35rem;
}

.card-arrow {
  color: var(--text-muted);
  margin-left: 1rem;
  transition: all 0.2s ease;
}

.university-card:hover .card-arrow {
  transform: translateX(5px);
  color: var(--primary-color);
}

/* Degree Grid */
.degree-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1.5rem;
}

.degree-card {
  background-color: var(--bg-card);
  border-radius: var(--border-radius-lg);
  overflow: hidden;
  box-shadow: var(--shadow-md);
  transition: all 0.2s ease;
  cursor: pointer;
  border: 1px solid var(--border-color-light);
  display: flex;
  flex-direction: column;
}

.degree-card:hover {
  transform: translateY(-5px);
  box-shadow: var(--shadow-lg);
  border-color: var(--primary-light);
}

.degree-header {
  padding: 1.25rem;
  background: linear-gradient(to right, var(--bg-card), var(--bg-accent));
  border-bottom: 1px solid var(--border-color-light);
}

.degree-header h3 {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--text-primary);
}

.degree-stats {
  display: flex;
  justify-content: space-around;
  padding: 1.25rem;
  flex: 1;
}

.stat-circle {
  text-align: center;
}

.stat-value {
  font-size: 1.75rem;
  font-weight: 800;
  color: var(--primary-color);
  line-height: 1;
  margin-bottom: 0.5rem;
}

.stat-label {
  font-size: 0.85rem;
  color: var(--text-secondary);
  font-weight: 500;
}

.degree-footer {
  padding: 1.25rem;
  text-align: center;
  border-top: 1px solid var(--border-color-light);
}

.view-button {
  padding: 0.6rem 1.25rem;
  background-color: var(--primary-color);
  color: white;
  border: none;
  border-radius: var(--border-radius);
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  width: 100%;
}

.view-button:hover {
  background-color: var(--primary-dark);
  transform: translateY(-2px);
  box-shadow: 0 3px 8px rgba(123, 73, 255, 0.3);
}

/* Module Filters */
.module-filters {
  display: flex;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
  padding: 1rem;
  background-color: var(--bg-card);
  border-radius: var(--border-radius);
  border: 1px solid var(--border-color-light);
}

.filter-control {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.filter-control label {
  font-weight: 600;
  color: var(--text-primary);
  white-space: nowrap;
}

.filter-control select {
  padding: 0.5rem 1rem;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  background-color: var(--bg-input);
  color: var(--text-primary);
  font-size: 0.95rem;
  outline: none;
  transition: all 0.2s ease;
  cursor: pointer;
}

.filter-control select:focus {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(123, 73, 255, 0.1);
}

/* Module Year Group */
.module-year-group {
  margin-bottom: 2.5rem;
}

.year-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid var(--border-color-light);
}

.year-header h3 {
  margin: 0;
  font-size: 1.3rem;
  font-weight: 700;
  color: var(--text-primary);
}

.year-stats {
  color: var(--text-secondary);
  font-weight: 500;
  font-size: 0.95rem;
}

/* Modules List */
.modules-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1rem;
}

.module-card {
  display: flex;
  align-items: center;
  background-color: var(--bg-card);
  border-radius: var(--border-radius);
  padding: 1.25rem;
  box-shadow: var(--shadow-sm);
  transition: all 0.2s ease;
  cursor: pointer;
  border: 1px solid var(--border-color-light);
}

.module-card:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-md);
  border-color: var(--primary-light);
}

.module-score-badge {
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 50px;
  height: 50px;
  border-radius: var(--border-radius);
  color: white;
  font-weight: 700;
  font-size: 0.95rem;
  margin-right: 1rem;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.module-score-badge.excellent {
  background: linear-gradient(135deg, #2ecc71, #27ae60);
}

.module-score-badge.good {
  background: linear-gradient(135deg, #3498db, #2980b9);
}

.module-score-badge.average {
  background: linear-gradient(135deg, #f1c40f, #f39c12);
}

.module-score-badge.pass {
  background: linear-gradient(135deg, #e67e22, #d35400);
}

.module-score-badge.fail {
  background: linear-gradient(135deg, #e74c3c, #c0392b);
}

.module-details {
  flex: 1;
}

.module-details h4 {
  margin: 0 0 0.35rem;
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-primary);
}

.module-code {
  font-size: 0.85rem;
  color: var(--text-muted);
  margin-bottom: 0.5rem;
  font-family: monospace;
}

/* Module Details View */
.module-details-container {
  background-color: var(--bg-card);
  border-radius: var(--border-radius-lg);
  overflow: hidden;
  box-shadow: var(--shadow-md);
  border: 1px solid var(--border-color-light);
}

.module-details-header {
  padding: 1.75rem;
  background: linear-gradient(to right, var(--bg-card), rgba(123, 73, 255, 0.05));
  border-bottom: 1px solid var(--border-color);
}

.module-details-title {
  display: flex;
  align-items: center;
  margin-bottom: 1rem;
}

.module-details-title h2 {
  margin: 0;
  font-size: 1.8rem;
  font-weight: 800;
  color: var(--text-primary);
}

.module-code-badge {
  display: inline-block;
  margin-left: 1rem;
  padding: 0.35rem 0.75rem;
  background-color: var(--bg-accent);
  border-radius: 20px;
  font-size: 0.85rem;
  color: var(--text-secondary);
  font-family: monospace;
  border: 1px solid var(--border-color-light);
}

.module-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.meta-label {
  font-weight: 600;
  color: var(--text-secondary);
  font-size: 0.9rem;
}

.meta-value {
  color: var(--text-primary);
  font-size: 0.9rem;
}

/* Module Metrics */
.module-metrics {
  padding: 1.75rem;
  border-bottom: 1px solid var(--border-color-light);
}

.score-card {
  display: flex;
  align-items: center;
  gap: 2.5rem;
}

.score-circle {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
}

.score-circle.excellent {
  background: linear-gradient(135deg, #2ecc71, #27ae60);
}

.score-circle.good {
  background: linear-gradient(135deg, #3498db, #2980b9);
}

.score-circle.average {
  background: linear-gradient(135deg, #f1c40f, #f39c12);
}

.score-circle.pass {
  background: linear-gradient(135deg, #e67e22, #d35400);
}

.score-circle.fail {
  background: linear-gradient(135deg, #e74c3c, #c0392b);
}

.score-circle .score-value {
  font-size: 2.25rem;
  font-weight: 800;
  color: white;
  margin-bottom: 0.25rem;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.score-circle .score-label {
  font-size: 0.85rem;
  color: rgba(255, 255, 255, 0.9);
  font-weight: 500;
}

.score-stats {
  display: flex;
  gap: 2rem;
}

.score-stat-item {
  padding: 1rem;
  background-color: var(--bg-accent);
  border-radius: var(--border-radius);
  min-width: 100px;
  text-align: center;
  box-shadow: var(--shadow-sm);
}

.score-stat-item .stat-value {
  font-size: 1.5rem;
  margin-bottom: 0.25rem;
}

/* Chart Section */
.chart-section {
  padding: 1.75rem;
  border-bottom: 1px solid var(--border-color-light);
}

.chart-section h3 {
  margin: 0 0 1.25rem;
  font-size: 1.3rem;
  font-weight: 700;
  color: var(--text-primary);
}

.chart-container {
  background-color: var(--bg-accent);
  border-radius: var(--border-radius);
  padding: 1.5rem;
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.05);
}

.grade-distribution {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.grade-bar-container {
  display: grid;
  grid-template-columns: 70px 1fr 50px;
  align-items: center;
  gap: 1rem;
}

.grade-label {
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--text-secondary);
  text-align: right;
}

.grade-bar-wrapper {
  height: 24px;
  background-color: var(--bg-card);
  border-radius: 4px;
  overflow: hidden;
  position: relative;
  box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.05);
  display: flex;
  align-items: center;
}

.grade-bar {
  height: 100%;
  border-radius: 4px;
  transition: width 0.5s ease;
}

.grade-count {
  position: absolute;
  left: 10px;
  color: white;
  font-size: 0.8rem;
  font-weight: 600;
  text-shadow: 0 1px 1px rgba(0, 0, 0, 0.2);
}

.grade-percentage {
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--text-primary);
}

/* Related Modules */
.related-modules-section {
  padding: 1.75rem;
}

.related-modules-section h3 {
  margin: 0 0 1.25rem;
  font-size: 1.3rem;
  font-weight: 700;
  color: var(--text-primary);
}

.related-modules-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1rem;
}

.related-module-card {
  display: flex;
  align-items: center;
  background-color: var(--bg-accent);
  border-radius: var(--border-radius);
  padding: 1rem;
  transition: all 0.2s ease;
  cursor: pointer;
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--border-color-light);
}

.related-module-card:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-md);
  background-color: var(--bg-card);
}

/* Responsive Design */
@media (max-width: 768px) {
  .graderadar {
    padding: 1rem;
  }

  .page-header h1 {
    font-size: 1.75rem;
  }

  .header-description {
    font-size: 1rem;
  }

  .university-grid, 
  .degree-grid, 
  .modules-list, 
  .related-modules-grid {
    grid-template-columns: 1fr;
  }

  .module-filters {
    flex-direction: column;
    gap: 1rem;
  }

  .score-card {
    flex-direction: column;
    align-items: center;
    gap: 1.5rem;
  }

  .score-stats {
    width: 100%;
    justify-content: space-around;
  }

  .grade-bar-container {
    grid-template-columns: 60px 1fr 40px;
    gap: 0.5rem;
  }

  .module-meta {
    gap: 1rem;
  }

  .meta-item {
    flex: 0 0 48%;
  }
}

@media (max-width: 480px) {
  .breadcrumb {
    padding: 0.5rem;
    font-size: 0.85rem;
  }

  .module-details-title {
    flex-direction: column;
    align-items: flex-start;
  }

  .module-code-badge {
    margin: 0.5rem 0 0;
  }

  .meta-item {
    flex: 0 0 100%;
  }
}
</style>