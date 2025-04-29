<template>
  <div class="analytics-page">
    <!-- Analytics Header Section -->
    <div class="analytics-header">
      <h1>Module Analytics</h1>
      <p class="subtitle">View and compare module performance across universities</p>
    </div>

    <!-- University Search Section -->
    <div class="search-section">
      <div class="search-card">
        <h2>Search for a University</h2>
        <div class="search-form">
          <div class="input-group">
            <input 
              type="text" 
              v-model="searchQuery" 
              placeholder="Enter university name..." 
              @keyup.enter="searchUniversity"
              :disabled="isSearching"
            />
            <button
              @click="searchUniversity"
              :disabled="isSearching || !searchQuery.trim()"
              class="search-button"
            >
              <template v-if="isSearching">
                <div class="button-spinner"></div>
              </template>
              <template v-else>
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="16"
                  height="16"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                >
                  <circle cx="11" cy="11" r="8"></circle>
                  <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                </svg>
                Search
              </template>
            </button>
          </div>
        </div>
        
        <!-- University Selection -->
        <div v-if="universities.length > 0" class="university-results">
          <h3>Select a University</h3>
          <div class="university-list">
            <div 
              v-for="university in universities" 
              :key="university.id" 
              class="university-item"
              :class="{ active: selectedUniversity && selectedUniversity.id === university.id }"
              @click="selectUniversity(university)"
            >
              <div class="university-name">{{ university.name }}</div>
              <div class="university-info">{{ getDegreesCount(university) }} degrees</div>
            </div>
          </div>
        </div>
        
        <!-- Degree Selection (shown after university is selected) -->
        <div v-if="selectedUniversity && degrees.length > 0" class="degree-selection">
          <h3>Select a Degree</h3>
          <div class="degree-list">
            <div 
              v-for="degree in degrees" 
              :key="degree"
              class="degree-item"
              :class="{ active: selectedDegree === degree }"
              @click="selectDegree(degree)"
            >
              {{ degree }}
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loading-container">
      <div class="loading-spinner"></div>
      <p>Loading analytics data...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="error-container">
      <div class="error-icon">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="12" cy="12" r="10"></circle>
          <line x1="12" y1="8" x2="12" y2="12"></line>
          <line x1="12" y1="16" x2="12.01" y2="16"></line>
        </svg>
      </div>
      <h3>Error Loading Analytics</h3>
      <p>{{ errorMessage }}</p>
      <button @click="retryFetch" class="retry-button">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M21 2v6h-6"></path>
          <path d="M3 12a9 9 0 0 1 15-6.7l3-3"></path>
          <path d="M3 22v-6h6"></path>
          <path d="M21 12a9 9 0 0 1-15 6.7l-3 3"></path>
        </svg>
        Try Again
      </button>
    </div>

    <!-- Empty State -->
    <div v-else-if="selectedDegree && !hasModules" class="empty-container">
      <div class="empty-icon">
        <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
          <line x1="9" y1="9" x2="15" y2="15"></line>
          <line x1="15" y1="9" x2="9" y2="15"></line>
        </svg>
      </div>
      <h3>No Analytics Available</h3>
      <p>We don't have enough data to show analytics for modules in this degree program yet.</p>
    </div>
    
    <!-- Analytics Content -->
    <div v-else-if="selectedDegree && hasModules" class="analytics-content">
      <!-- Filter controls for modules -->
      <div class="filter-controls">
        <div class="filter-group">
          <label for="sortBy">Sort By:</label>
          <select id="sortBy" v-model="sortMethod">
            <option value="name">Module Name</option>
            <option value="code">Module Code</option>
            <option value="average-desc">Average Score (High to Low)</option>
            <option value="average-asc">Average Score (Low to High)</option>
            <option value="popularity">Number of Students</option>
          </select>
        </div>
      </div>

      <!-- New Module Cards Grid -->
      <div class="module-cards-container">
        <div class="module-header">
          <h2>Module Analytics for {{ selectedDegree }}</h2>
          <p class="university-tag">{{ selectedUniversity.name }}</p>
        </div>
        
        <div class="module-cards-grid">
          <div v-for="module in sortedModules" :key="module.code" class="module-card">
            <div class="module-card-header">
              <h3>{{ module.name }} <span class="module-code-pill">{{ module.code }}</span></h3>
              <div class="back-button">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M19 12H5M12 19l-7-7 7-7"></path>
                </svg>
              </div>
            </div>
            
            <div class="module-card-content">
              <div class="module-details">
                <h4>Module Details</h4>
                <div class="detail-item">
                  <span class="label">University:</span>
                  <span class="value">{{ selectedUniversity.name }}</span>
                </div>
                <div class="detail-item">
                  <span class="label">Number of Students:</span>
                  <span class="value">{{ module.student_counter }}</span>
                </div>
                <div class="detail-item">
                  <span class="label">Average Score:</span>
                  <span class="value">{{ module.average_score }}%</span>
                </div>
              </div>
              
              <div class="module-gradeometer">
                <h4>GRADEOMETER</h4>
                <div class="gradeometer-content">
                  <div class="gradeometer-icon">
                    <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#7b49ff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M12 2v1M12 21v1M4.2 4.2l.8.8M19 19l.8.8M2 12h1M21 12h1M6 18.75l-.5.75M18.5 5l-.5.75"></path>
                      <circle cx="12" cy="12" r="4"></circle>
                    </svg>
                  </div>
                  <div class="gradeometer-percentage">
                    <span class="percentage-value">{{ module.average_score }}%</span>
                    <span class="students-count">{{ module.student_counter }} students</span>
                  </div>
                </div>
                
                <div class="gradeometer-metrics">
                  <div class="metric">
                    <div class="metric-label">Difficulty</div>
                    <div class="metric-bar-container">
                      <div class="metric-bar" :style="{ width: getDifficultyPercentage(module.average_score) + '%' }"></div>
                    </div>
                    <div class="metric-value">{{ getDifficultyRating(module.average_score) }}%</div>
                  </div>
                  
                  <div class="metric">
                    <div class="metric-label">Teaching Quality</div>
                    <div class="metric-bar-container">
                      <div class="metric-bar" :style="{ width: getTeachingQualityPercentage(module.average_score) + '%' }"></div>
                    </div>
                    <div class="metric-value">{{ getTeachingQualityRating(module.average_score) }}%</div>
                  </div>
                  
                  <div class="metric">
                    <div class="metric-label">Recommended</div>
                    <div class="metric-bar-container">
                      <div class="metric-bar" :style="{ width: getRecommendedPercentage(module.average_score) + '%' }"></div>
                    </div>
                    <div class="metric-value">{{ getRecommendedRating(module.average_score) }}%</div>
                  </div>
                </div>
              </div>
              
              <div class="student-averages">
                <h4>Student Averages</h4>
                <div class="averages-chart">
                  <div class="chart-bars">
                    <div v-for="(count, range) in module.grade_distribution" :key="range" class="chart-bar-container">
                      <div class="chart-bar" :style="{ height: calculateBarHeight(count, module.student_counter) + '%' }">
                        <div class="bar-count">{{ count }}</div>
                      </div>
                      <div class="bar-label">{{ formatGradeRange(range) }}</div>
                    </div>
                    
                    <!-- Empty bars if less than 5 distribution ranges -->
                    <div v-for="i in getEmptyBarsCount(module.grade_distribution)" :key="'empty-'+i" class="chart-bar-container empty">
                      <div class="chart-bar empty"></div>
                      <div class="bar-label">-</div>
                    </div>
                  </div>
                  
                  <div class="chart-axis">
                    <div v-for="n in 6" :key="n" class="axis-mark">{{ (n - 1) * 20 }}%</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- University Stats Summary -->
      <div class="university-stats" v-if="hasModules">
        <h2>University Module Statistics</h2>
        
        <div class="stats-cards">
          <div class="stats-card">
            <div class="stat-icon difficulty">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 20v-6M12 14l-2.5-2"></path>
                <path d="M12 14l2.5-2"></path>
                <path d="M12 4v6"></path>
                <path d="M12 10l-2.5 2"></path>
                <path d="M12 10l2.5 2"></path>
              </svg>
            </div>
            <div class="stat-content">
              <h3>Module Difficulty</h3>
              <p>
                {{ getDifficultyAssessment() }}
              </p>
            </div>
          </div>
          
          <div class="stats-card">
            <div class="stat-icon distribution">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M2 20h20"></path>
                <path d="M5 20v-4"></path>
                <path d="M9 20v-8"></path>
                <path d="M13 20V10"></path>
                <path d="M17 20v-6"></path>
                <path d="M21 20V6"></path>
              </svg>
            </div>
            <div class="stat-content">
              <h3>Grade Distribution</h3>
              <p>
                {{ getGradeDistributionInsight() }}
              </p>
            </div>
          </div>
          
          <div class="stats-card">
            <div class="stat-icon popularity">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                <circle cx="9" cy="7" r="4"></circle>
                <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
                <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
              </svg>
            </div>
            <div class="stat-content">
              <h3>Student Participation</h3>
              <p>
                {{ getParticipationInsight() }}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { API_URL } from '@/config.js';

export default {
  name: 'AnalyticsPage',
  data() {
    return {
      // Search and selection
      searchQuery: '',
      isSearching: false,
      universities: [],
      selectedUniversity: null,
      degrees: [],
      selectedDegree: null,
      
      // Analytics data
      loading: false,
      error: false,
      errorMessage: '',
      analyticsData: [],
      
      // Sorting
      sortMethod: 'name'
    };
  },
  computed: {
    hasModules() {
      return this.analyticsData && this.analyticsData.length > 0;
    },
    sortedModules() {
      if (!this.analyticsData) return [];
      
      return [...this.analyticsData].sort((a, b) => {
        switch (this.sortMethod) {
          case 'name':
            return a.name.localeCompare(b.name);
          case 'code':
            return a.code.localeCompare(b.code);
          case 'average-desc':
            return b.average_score - a.average_score;
          case 'average-asc':
            return a.average_score - b.average_score;
          case 'popularity':
            return b.student_counter - a.student_counter;
          default:
            return 0;
        }
      });
    },
    topModulesToShow() {
      // Display top 4 modules with most students for distribution overview
      return [...this.sortedModules]
        .sort((a, b) => b.student_counter - a.student_counter)
        .slice(0, 4);
    },
    averageModuleScore() {
      if (!this.analyticsData || this.analyticsData.length === 0) return 0;
      
      const sum = this.analyticsData.reduce((total, module) => total + module.average_score, 0);
      return Math.round((sum / this.analyticsData.length) * 10) / 10;
    },
    totalStudents() {
      if (!this.analyticsData || this.analyticsData.length === 0) return 0;
      
      // Find the module with the most students as an estimate of total students
      return Math.max(...this.analyticsData.map(m => m.student_counter));
    }
  },
  methods: {
    searchUniversity() {
      if (!this.searchQuery.trim() || this.isSearching) return;
      
      this.isSearching = true;
      this.error = false;
      this.universities = [];
      this.selectedUniversity = null;
      this.degrees = [];
      this.selectedDegree = null;
      this.analyticsData = [];
      
      // Simulate API call to search universities
      setTimeout(() => {
        // Mock university search - in a real app, this would be an API call
        // Normally you'd use axios.get(`${API_URL}/universities?search=${this.searchQuery}`)
        this.searchUniversityAPI(this.searchQuery)
          .then(response => {
            this.universities = response.data || [];
            if (this.universities.length === 0) {
              this.error = true;
              this.errorMessage = 'No universities found matching your search.';
            }
          })
          .catch(error => {
            console.error("Error searching universities:", error);
            this.error = true;
            this.errorMessage = error.response?.data?.error || 
                              'Failed to search for universities. Please try again.';
          })
          .finally(() => {
            this.isSearching = false;
          });
      }, 800); // Simulate network delay
    },
    
    async searchUniversityAPI(query) {
      try {
        // In a real implementation, you'd call an actual API endpoint
        // Mock the API by returning a hardcoded university that matches the query
        const mockUniversities = [
          {
            id: "University of Southampton",
            name: "University of Southampton",
            counter: 1
          },
          {
            id: "University of Cambridge",
            name: "University of Cambridge",
            counter: 0
          },
          {
            id: "University of Oxford",
            name: "University of Oxford",
            counter: 0
          },
          {
            id: "University of Edinburgh",
            name: "University of Edinburgh",
            counter: 3
          }
        ];
        
        const filteredUniversities = mockUniversities.filter(uni => 
          uni.name.toLowerCase().includes(query.toLowerCase())
        );
        
        return { data: filteredUniversities };
      } catch (error) {
        console.error("Error in searchUniversityAPI:", error);
        throw error;
      }
    },
    
    getDegreesCount(university) {
      // In a real app, this might come from the university object
      // For now, just use a placeholder value
      return university.counter || 0;
    },
    
    selectUniversity(university) {
      this.selectedUniversity = university;
      this.selectedDegree = null;
      this.analyticsData = [];
      this.loading = true;
      this.error = false;
      
      // Fetch degrees for this university
      this.fetchUniversityDegrees(university.id)
        .then(response => {
          this.degrees = response.data || [];
          if (this.degrees.length === 0) {
            this.error = true;
            this.errorMessage = 'No degrees found for this university.';
          }
        })
        .catch(error => {
          console.error("Error fetching university degrees:", error);
          this.error = true;
          this.errorMessage = error.response?.data?.error || 
                            'Failed to load degree programs. Please try again.';
        })
        .finally(() => {
          this.loading = false;
        });
    },
    
    async fetchUniversityDegrees(universityId) {
      try {
        // In a real app, you'd call:
        // return axios.get(`${API_URL}/universities/${universityId}/degrees`);
        
        // Mock response for University of Southampton
        if (universityId === "University of Southampton") {
          return { 
            data: ["COMPUTER SCIENCE", "ENGINEERING", "MATHEMATICS"] 
          };
        }
        
        // Mock response for Edinburgh
        if (universityId === "University of Edinburgh") {
          return { 
            data: ["COMPUTER SCIENCE", "ENGINEERING", "MATHEMATICS", "ACCOUNTING"] 
          };
        }
        
        // Mock response for other universities
        return { data: ["COMPUTER SCIENCE"] };
      } catch (error) {
        console.error("Error in fetchUniversityDegrees:", error);
        throw error;
      }
    },
    
    selectDegree(degree) {
      this.selectedDegree = degree;
      this.loading = true;
      this.error = false;
      this.analyticsData = [];
      
      // Fetch analytics data for this university and degree
      this.fetchModuleAnalytics(this.selectedUniversity.id, degree)
        .then(response => {
          this.analyticsData = response.data || [];
          if (this.analyticsData.length === 0) {
            this.error = true;
            this.errorMessage = 'No analytics data available for this degree program.';
          }
        })
        .catch(error => {
          console.error("Error fetching module analytics:", error);
          this.error = true;
          this.errorMessage = error.response?.data?.error || 
                            'Failed to load analytics data. Please try again.';
        })
        .finally(() => {
          this.loading = false;
        });
    },
    
    async fetchModuleAnalytics(universityId, degree) {
      try {
        // In a real app, you'd call:
        // return axios.get(`${API_URL}/universities/${universityId}/degrees/${degree}/analytics`);
        
        // For demo purposes, use the provided university data
        if (universityId === "University of Southampton" && degree === "COMPUTER SCIENCE") {
          const mockData = [
            {
              "name": "Programming I",
              "code": "COMP1001",
              "average_score": 82,
              "student_counter": 32,
              "grade_distribution": {
                "81-90%": 15,
                "71-80%": 10,
                "61-70%": 5,
                "51-60%": 2
              }
            },
            {
              "name": "Programming II",
              "code": "COMP1002",
              "average_score": 75,
              "student_counter": 29,
              "grade_distribution": {
                "71-80%": 14,
                "61-70%": 8,
                "51-60%": 4,
                "81-90%": 3
              }
            },
            {
              "name": "Databases",
              "code": "COMP2007",
              "average_score": 68,
              "student_counter": 26,
              "grade_distribution": {
                "61-70%": 12,
                "71-80%": 8,
                "51-60%": 4,
                "41-50%": 2
              }
            },
            {
              "name": "Web Development",
              "code": "COMP2011",
              "average_score": 71,
              "student_counter": 28,
              "grade_distribution": {
                "71-80%": 13,
                "61-70%": 9,
                "81-90%": 4,
                "51-60%": 2
              }
            }
          ];
          
          return { data: mockData };
        }
        
        // Mock data for Edinburgh ACCOUNTING
        if (universityId === "University of Edinburgh" && degree === "ACCOUNTING") {
          const mockData = [
            {
              "name": "Accountancy 1A",
              "code": "ACCT1001",
              "average_score": 59.5,
              "student_counter": 12,
              "grade_distribution": {
                "51-60%": 3,
                "61-70%": 3,
                "71-80%": 4,
                "81-90%": 1,
                "41-50%": 1
              }
            },
            {
              "name": "Accountancy 1B",
              "code": "ACCT1002",
              "average_score": 62,
              "student_counter": 11,
              "grade_distribution": {
                "51-60%": 2,
                "61-70%": 5,
                "71-80%": 3,
                "41-50%": 1
              }
            }
          ];
          
          return { data: mockData };
        }
        
        // Empty response for other combinations
        return { data: [] };
      } catch (error) {
        console.error("Error in fetchModuleAnalytics:", error);
        throw error;
      }
    },
    
    retryFetch() {
      if (this.selectedDegree) {
        this.selectDegree(this.selectedDegree);
      } else if (this.selectedUniversity) {
        this.selectUniversity(this.selectedUniversity);
      } else {
        this.searchUniversity();
      }
    },
    
    // New methods for the Gradeometer and Student Averages
    getDifficultyPercentage(score) {
      // Invert the score - higher score means lower difficulty
      return Math.max(0, Math.min(100, 100 - score)); 
    },
    
    getDifficultyRating(score) {
      return Math.round(100 - score);
    },
    
    getTeachingQualityPercentage(score) {
      // Teaching quality correlates with score
      return Math.max(0, Math.min(100, score));
    },
    
    getTeachingQualityRating(score) {
      return Math.round(score);
    },
    
    getRecommendedPercentage(score) {
      // Recommendation percentage based on score
      if (score >= 80) return 90;
      if (score >= 70) return 75;
      if (score >= 60) return 60;
      if (score >= 50) return 40;
      return 20;
    },
    
    getRecommendedRating(score) {
      return this.getRecommendedPercentage(score);
    },
    
    calculateBarHeight(count, totalStudents) {
      if (!totalStudents) return 0;
      return Math.min(100, Math.max(10, (count / totalStudents) * 100));
    },
    
    formatGradeRange(range) {
      // Convert "71-80%" to "70%"
      const parts = range.split('-');
      if (parts.length === 2) {
        return parts[0] + '%';
      }
      return range;
    },
    
    getEmptyBarsCount(distribution) {
      // If we have less than 5 distribution ranges, add empty bars
      const count = Object.keys(distribution).length;
      return Math.max(0, 5 - count);
    },
    
    getDifficultyAssessment() {
      if (!this.analyticsData || this.analyticsData.length === 0) return '';
      
      if (this.averageModuleScore >= 75) {
        return `Modules in this degree program have an average score of ${this.averageModuleScore}%, which suggests students generally find them manageable.`;
      } else if (this.averageModuleScore >= 65) {
        return `Modules in this degree program have a moderate difficulty level with an average score of ${this.averageModuleScore}%.`;
      } else if (this.averageModuleScore >= 55) {
        return `Modules in this degree program appear to be somewhat challenging with an average score of ${this.averageModuleScore}%.`;
      } else {
        return `Modules in this degree program seem to be difficult for many students, with a relatively low average score of ${this.averageModuleScore}%.`;
      }
    },
    
    getGradeDistributionInsight() {
      if (!this.analyticsData || this.analyticsData.length === 0) return '';
      
      // Count total students in each grade range across all modules
      const totalDistribution = {};
      let totalStudents = 0;
      
      this.analyticsData.forEach(module => {
        Object.entries(module.grade_distribution || {}).forEach(([range, count]) => {
          totalDistribution[range] = (totalDistribution[range] || 0) + count;
          totalStudents += count;
        });
      });
      
      if (totalStudents === 0) return 'No grade distribution data is available yet.';
      
      // Find most common grade range
      const mostCommonRange = Object.entries(totalDistribution)
        .sort((a, b) => b[1] - a[1])[0];
      
      const percentage = Math.round((mostCommonRange[1] / totalStudents) * 100);
      
      return `Most students (${percentage}%) scored in the ${mostCommonRange[0]} range across all modules in this degree program.`;
    },
    
    getParticipationInsight() {
      if (!this.analyticsData || this.analyticsData.length === 0) return '';
      
      const moduleCount = this.analyticsData.length;
      const averageStudents = this.analyticsData.reduce((sum, module) => 
        sum + module.student_counter, 0) / moduleCount;
      
      const roundedAvg = Math.round(averageStudents * 10) / 10;
      
      if (roundedAvg >= 50) {
        return `This degree program has high participation with an average of ${roundedAvg} students per module.`;
      } else if (roundedAvg >= 20) {
        return `This degree program has moderate participation with an average of ${roundedAvg} students per module.`;
      } else if (roundedAvg >= 5) {
        return `This degree program has low participation with an average of ${roundedAvg} students per module.`;
      } else {
        return `This degree program has very few participants with an average of ${roundedAvg} students per module.`;
      }
    }
  },
  mounted() {
    // Check if university and degree were passed in URL params
    const universityId = this.$route.query.universityId;
    const degree = this.$route.query.degree;
    
    if (universityId) {
      // Fetch university info and then select it
      this.loading = true;
      // In a real app, you'd fetch the university details
      // For now, just create a mock university object
      setTimeout(() => {
        const university = {
          id: universityId,
          name: universityId,
          counter: 1
        };
        
        this.universities = [university];
        this.selectUniversity(university);
        
        // If degree was also specified, select it after university details are loaded
        if (degree) {
          const checkDegree = () => {
            if (this.degrees.includes(degree)) {
              this.selectDegree(degree);
            }
          };
          
          // Wait for degrees to load
          const interval = setInterval(() => {
            if (this.degrees.length > 0) {
              checkDegree();
              clearInterval(interval);
            }
          }, 100);
          
          // Safety timeout
          setTimeout(() => clearInterval(interval), 5000);
        }
      }, 500);
    }
  }
};
</script>

<style>
.analytics-page {
  padding: 2rem;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  color: #333333;
  background-color: #f8f9fa;
  min-height: calc(100vh - 70px);
}

.analytics-header {
  margin-bottom: 2rem;
}

.analytics-header h1 {
  margin: 0 0 0.5rem;
  font-size: 2.2rem;
  font-weight: 800;
  color: #6038cc;
  letter-spacing: -0.5px;
  position: relative;
}

.analytics-header h1::after {
  content: '';
  position: absolute;
  bottom: -8px;
  left: 0;
  width: 60px;
  height: 4px;
  background: #7b49ff;
  border-radius: 4px;
}

.subtitle {
  color: #667085;
  font-size: 1.1rem;
  margin-top: 1rem;
  margin-bottom: 1.5rem;
}

/* Search Section Styles */
.search-section {
  margin-bottom: 2rem;
}

.search-card {
  background-color: #ffffff;
  border-radius: 12px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.08);
  padding: 2rem;
  border: 1px solid #e2e8f0;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.search-card:hover {
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.1);
  transform: translateY(-5px);
}

.search-card h2 {
  margin: 0 0 1.5rem;
  font-size: 1.5rem;
  font-weight: 700;
  color: #333333;
}

.search-form {
  margin-bottom: 1.5rem;
}

.input-group {
  display: flex;
  gap: 0.75rem;
}

.input-group input {
  flex: 1;
  padding: 1rem 1.25rem;
  border: 2px solid #e2e8f0;
  border-radius: 10px;
  font-size: 1rem;
  background-color: #ffffff;
  color: #333333;
  transition: all 0.3s ease;
}

.input-group input:focus {
  border-color: #7b49ff;
  outline: none;
  box-shadow: 0 0 0 4px rgba(123, 73, 255, 0.15);
}

.search-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0 1.5rem;
  background: #7b49ff;
  color: white;
  border: none;
  border-radius: 10px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.search-button:hover:not(:disabled) {
  background: #6038cc;
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(123, 73, 255, 0.25);
}

.search-button:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.button-spinner {
  width: 18px;
  height: 18px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* University Results */
.university-results,
.degree-selection {
  margin-top: 2rem;
}

.university-results h3,
.degree-selection h3 {
  margin: 0 0 1rem;
  font-size: 1.2rem;
  font-weight: 700;
  color: #333333;
}

.university-list,
.degree-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1.25rem;
}

.university-item,
.degree-item {
  padding: 1.5rem;
  background: #f1f3f9;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.university-item:hover,
.degree-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.08);
  background: #e6eaf3;
}

.university-item.active,
.degree-item.active {
  border-color: #7b49ff;
  background: rgba(123, 73, 255, 0.08);
}

.university-name {
  font-weight: 700;
  font-size: 1.1rem;
  margin-bottom: 0.5rem;
}

.university-info {
  font-size: 0.9rem;
  color: #667085;
}

.degree-item {
  font-weight: 600;
  text-align: center;
}

/* Loading, Error, and Empty States */
.loading-container,
.error-container,
.empty-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 3rem;
  background-color: #ffffff;
  border-radius: 12px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.08);
  margin: 1rem 0;
  min-height: 320px;
  border: 1px solid #e2e8f0;
}

.loading-spinner {
  width: 64px;
  height: 64px;
  border: 5px solid rgba(123, 73, 255, 0.2);
  border-radius: 50%;
  border-top-color: #7b49ff;
  animation: spin 1.2s linear infinite;
  margin-bottom: 2rem;
}

.error-icon,
.empty-icon {
  margin-bottom: 1.5rem;
  color: #667085;
}

.error-icon svg,
.empty-icon svg {
  stroke: currentColor;
}

.error-container h3,
.empty-container h3 {
  margin: 0 0 0.75rem;
  font-size: 1.5rem;
  font-weight: 700;
}

.retry-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-top: 1.5rem;
  padding: 0.85rem 1.5rem;
  background-color: #7b49ff;
  color: white;
  border: none;
  border-radius: 10px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.retry-button:hover {
  background-color: #6038cc;
  transform: translateY(-3px);
  box-shadow: 0 6px 16px rgba(123, 73, 255, 0.25);
}

/* Filter Controls */
.filter-controls {
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
  background-color: #ffffff;
  padding: 1.25rem 1.5rem;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  border: 1px solid #e2e8f0;
  margin-bottom: 2rem;
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 0.85rem;
}

.filter-group label {
  font-weight: 600;
  white-space: nowrap;
  color: #333333;
}

.filter-group select {
  padding: 0.75rem 1.25rem;
  border: 2px solid #e2e8f0;
  border-radius: 10px;
  background-color: #ffffff;
  font-size: 0.95rem;
  min-width: 200px;
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='%23666' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 0.85rem center;
  background-size: 16px;
  color: #333333;
  transition: all 0.3s ease;
  cursor: pointer;
}

.filter-group select:focus {
  border-color: #7b49ff;
  outline: none;
  box-shadow: 0 0 0 4px rgba(123, 73, 255, 0.15);
}

/* Module Cards Grid */
.module-cards-container {
  margin-bottom: 2.5rem;
}

.module-header {
  margin-bottom: 2rem;
}

.module-header h2 {
  margin: 0 0 0.5rem;
  font-size: 1.8rem;
  font-weight: 700;
  color: #333333;
}

.university-tag {
  color: #667085;
  font-style: italic;
  font-size: 1.1rem;
}

.module-cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(420px, 1fr));
  gap: 2rem;
}

.module-card {
  background-color: #ffffff;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  border: 1px solid #e2e8f0;
}

.module-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 16px 32px rgba(0, 0, 0, 0.12);
}

.module-card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.25rem 1.5rem;
  background-color: #7b49ff;
  color: #ffffff;
}

.module-card-header h3 {
  margin: 0;
  font-size: 1.3rem;
  font-weight: 700;
}

.module-code-pill {
  display: inline-block;
  font-size: 0.85rem;
  padding: 0.25rem 0.75rem;
  margin-left: 0.75rem;
  background-color: rgba(255, 255, 255, 0.2);
  border-radius: 1rem;
  vertical-align: middle;
}

.back-button {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.back-button:hover {
  background-color: rgba(255, 255, 255, 0.3);
}

.module-card-content {
  padding: 1.5rem;
}

/* Module Details Section */
.module-details {
  margin-bottom: 2rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid #e2e8f0;
}

.module-details h4 {
  margin: 0 0 1rem;
  font-size: 1.1rem;
  font-weight: 700;
  color: #333333;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  padding: 0.75rem 0;
  border-bottom: 1px solid #f1f3f9;
}

.detail-item:last-child {
  border-bottom: none;
}

.detail-item .label {
  color: #667085;
  font-weight: 500;
}

.detail-item .value {
  font-weight: 600;
  color: #333333;
}

/* Gradeometer Section */
.module-gradeometer {
  margin-bottom: 2rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid #e2e8f0;
}

.module-gradeometer h4 {
  margin: 0 0 1rem;
  font-size: 1.1rem;
  font-weight: 700;
  color: #333333;
  text-align: center;
  letter-spacing: 0.5px;
}

.gradeometer-content {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.gradeometer-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 72px;
  height: 72px;
  background-color: rgba(123, 73, 255, 0.1);
  border-radius: 50%;
}

.gradeometer-percentage {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.percentage-value {
  font-size: 2.5rem;
  font-weight: 800;
  color: #333333;
  line-height: 1;
}

.students-count {
  font-size: 0.85rem;
  color: #667085;
  margin-top: 0.4rem;
}

.gradeometer-metrics {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.metric {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}

.metric-label {
  width: 120px;
  font-size: 0.9rem;
  font-weight: 600;
  color: #667085;
}

.metric-bar-container {
  flex: 1;
  height: 10px;
  background-color: #f1f3f9;
  border-radius: 5px;
  overflow: hidden;
}

.metric-bar {
  height: 100%;
  background: linear-gradient(to right, #7b49ff, #9a73ff);
  border-radius: 5px;
  transition: width 0.5s ease;
}

.metric-value {
  width: 40px;
  font-size: 0.9rem;
  font-weight: 600;
  text-align: right;
  color: #333333;
}

/* Student Averages Section */
.student-averages {
  margin-bottom: 1rem;
}

.student-averages h4 {
  margin: 0 0 1.25rem;
  font-size: 1.1rem;
  font-weight: 700;
  color: #333333;
  text-align: center;
}

.averages-chart {
  height: 220px;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.chart-bars {
  display: flex;
  height: 180px;
  align-items: flex-end;
  gap: 0.5rem;
  padding-bottom: 24px;
  position: relative;
}

.chart-axis {
  display: flex;
  justify-content: space-between;
  padding: 0 0.5rem;
  font-size: 0.75rem;
  color: #667085;
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
}

.axis-mark {
  transform: translateX(-50%);
}

.chart-bar-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  height: 100%;
  position: relative;
}

.chart-bar-container.empty .chart-bar {
  background-color: transparent;
  border: 1px dashed #e2e8f0;
}

.chart-bar {
  width: 100%;
  background-color: #7b49ff;
  border-radius: 4px 4px 0 0;
  position: relative;
  display: flex;
  justify-content: center;
  align-items: flex-start;
  transition: height 0.5s ease;
}

.bar-count {
  position: absolute;
  top: -20px;
  font-weight: 600;
  font-size: 0.8rem;
  color: #333333;
}

.bar-label {
  margin-top: 0.5rem;
  font-size: 0.8rem;
  color: #667085;
  text-align: center;
  position: absolute;
  bottom: -24px;
  width: 100%;
}

/* University Stats */
.university-stats {
  background-color: #ffffff;
  border-radius: 16px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
  padding: 2rem;
  overflow: hidden;
  border: 1px solid #e2e8f0;
}

.university-stats h2 {
  margin: 0 0 1.5rem;
  font-size: 1.6rem;
  font-weight: 700;
  color: #333333;
}

.stats-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 1.5rem;
}

.stats-card {
  display: flex;
  gap: 1.25rem;
  padding: 1.75rem;
  background-color: #f8f9fa;
  border-radius: 12px;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  border: 1px solid #e2e8f0;
}

.stats-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.08);
  background-color: #f1f3f9;
}

.stat-icon {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.stat-icon.difficulty {
  background-color: rgba(241, 196, 15, 0.15);
  color: #f1c40f;
}

.stat-icon.distribution {
  background-color: rgba(52, 152, 219, 0.15);
  color: #3498db;
}

.stat-icon.popularity {
  background-color: rgba(46, 204, 113, 0.15);
  color: #2ecc71;
}

.stat-content {
  flex: 1;
}

.stat-content h3 {
  margin: 0 0 0.75rem;
  font-size: 1.2rem;
  font-weight: 700;
  color: #333333;
}

.stat-content p {
  margin: 0;
  color: #667085;
  line-height: 1.6;
  font-size: 0.95rem;
}

/* Responsive Adjustments */
@media (max-width: 1100px) {
  .module-cards-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 900px) {
  .analytics-page {
    padding: 1.5rem;
  }
  
  .stats-cards {
    grid-template-columns: 1fr;
  }

  .university-stats {
    padding: 1.5rem;
  }
}

@media (max-width: 600px) {
  .analytics-page {
    padding: 1rem;
  }
  
  .search-card {
    padding: 1.5rem;
  }

  .analytics-header h1 {
    font-size: 1.8rem;
  }
  
  .filter-controls {
    flex-direction: column;
    align-items: stretch;
    gap: 1rem;
    padding: 1rem;
  }
  
  .filter-group {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
  
  .filter-group select {
    width: 100%;
  }
  
  .input-group {
    flex-direction: column;
    gap: 1rem;
  }
  
  .university-list,
  .degree-list {
    grid-template-columns: 1fr;
  }
  
  .stats-card {
    flex-direction: column;
    align-items: center;
    text-align: center;
    padding: 1.25rem;
  }

  .metric {
    flex-direction: column;
    gap: 0.5rem;
  }

  .metric-label, .metric-value {
    width: 100%;
    text-align: center;
  }

  .gradeometer-content {
    flex-direction: column;
  }
}

/* Dark mode adjustments */
.dark-mode .analytics-page {
  background-color: #111827;
  color: #f1f5f9;
}

.dark-mode .search-card,
.dark-mode .module-card,
.dark-mode .university-stats,
.dark-mode .filter-controls,
.dark-mode .loading-container,
.dark-mode .error-container,
.dark-mode .empty-container {
  background-color: #1f2937;
  border-color: #374151;
}

.dark-mode .university-item,
.dark-mode .degree-item,
.dark-mode .stats-card {
  background-color: #2d3748;
}

.dark-mode .detail-item {
  border-color: #374151;
}

.dark-mode .detail-item .label {
  color: #9ca3af;
}

.dark-mode .detail-item .value,
.dark-mode .analytics-header h1,
.dark-mode .module-header h2,
.dark-mode .percentage-value,
.dark-mode .metric-value {
  color: #f1f5f9;
}

.dark-mode .module-details,
.dark-mode .module-gradeometer,
.dark-mode .student-averages {
  border-color: #374151;
}

.dark-mode .metric-bar-container,
.dark-mode .chart-bar-container.empty .chart-bar {
  background-color: #374151;
  border-color: #4b5563;
}

.dark-mode .input-group input,
.dark-mode .filter-group select {
  background-color: #374151;
  color: #f1f5f9;
  border-color: #4b5563;
}

.dark-mode .subtitle,
.dark-mode .university-info,
.dark-mode .students-count,
.dark-mode .bar-label,
.dark-mode .metric-label {
  color: #9ca3af;
}
</style>