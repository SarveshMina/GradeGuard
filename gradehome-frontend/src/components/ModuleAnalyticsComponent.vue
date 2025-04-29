<template>
    <div class="module-analytics">
      <div v-if="loading" class="loading-indicator">
        <div class="spinner"></div>
        <p>Loading analytics data...</p>
      </div>
      
      <div v-else-if="error" class="error-message">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="12" cy="12" r="10"></circle>
          <line x1="12" y1="8" x2="12" y2="12"></line>
          <line x1="12" y1="16" x2="12.01" y2="16"></line>
        </svg>
        <p>{{ error }}</p>
      </div>
      
      <div v-else class="analytics-content">
        <!-- Summary Section -->
        <div class="analytics-summary">
          <div class="summary-card student-count">
            <div class="card-icon">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                <circle cx="9" cy="7" r="4"></circle>
                <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
                <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
              </svg>
            </div>
            <div class="card-content">
              <div class="card-value">{{ analytics.studentCount }}</div>
              <div class="card-label">Students</div>
            </div>
          </div>
          
          <div class="summary-card average-score">
            <div class="card-icon">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                <polyline points="22 4 12 14.01 9 11.01"></polyline>
              </svg>
            </div>
            <div class="card-content">
              <div class="card-value">{{ analytics.averageScore }}%</div>
              <div class="card-label">Average Score</div>
            </div>
          </div>
          
          <div class="summary-card median-score">
            <div class="card-icon">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <line x1="18" y1="20" x2="18" y2="10"></line>
                <line x1="12" y1="20" x2="12" y2="4"></line>
                <line x1="6" y1="20" x2="6" y2="14"></line>
              </svg>
            </div>
            <div class="card-content">
              <div class="card-value">{{ analytics.medianScore }}%</div>
              <div class="card-label">Median Score</div>
            </div>
          </div>
          
          <div class="summary-card updated">
            <div class="card-icon">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="10"></circle>
                <polyline points="12 6 12 12 16 14"></polyline>
              </svg>
            </div>
            <div class="card-content">
              <div class="card-value">{{ formatDate(analytics.lastUpdated) }}</div>
              <div class="card-label">Last Updated</div>
            </div>
          </div>
        </div>
        
        <!-- Grade Distribution Chart -->
        <div class="chart-section">
          <h3>Grade Distribution</h3>
          <div class="chart-container">
            <canvas ref="gradeDistributionChart"></canvas>
          </div>
        </div>
        
        <!-- Comparison to Your Score -->
        <div v-if="yourScore !== null" class="your-score-section">
          <h3>Your Performance</h3>
          <div class="score-comparison">
            <div class="your-score" :class="getScoreClass(yourScore)">
              <div class="score-value">{{ yourScore }}%</div>
              <div class="score-label">Your Score</div>
            </div>
            
            <div class="score-difference" :class="getDifferenceClass(yourScore - analytics.averageScore)">
              <div class="diff-value">
                <span v-if="yourScore >= analytics.averageScore">+</span>{{ (yourScore - analytics.averageScore).toFixed(1) }}%
              </div>
              <div class="diff-label">Compared to Average</div>
            </div>
            
            <div class="percentile">
              <div class="percentile-value">{{ calculatePercentile(yourScore) }}%</div>
              <div class="percentile-label">Percentile</div>
            </div>
          </div>
        </div>
        
        <!-- Module Stats Table -->
        <div class="stats-section">
          <h3>Detailed Statistics</h3>
          <div class="stats-grid">
            <div class="stat-item">
              <div class="stat-label">Highest Score</div>
              <div class="stat-value">{{ analytics.highestScore }}%</div>
            </div>
            <div class="stat-item">
              <div class="stat-label">Lowest Score</div>
              <div class="stat-value">{{ analytics.lowestScore }}%</div>
            </div>
            <div class="stat-item">
              <div class="stat-label">Standard Deviation</div>
              <div class="stat-value">{{ analytics.standardDeviation.toFixed(1) }}</div>
            </div>
            <div class="stat-item">
              <div class="stat-label">Pass Rate</div>
              <div class="stat-value">{{ analytics.passRate }}%</div>
            </div>
            <div class="stat-item">
              <div class="stat-label">First Class Rate</div>
              <div class="stat-value">{{ analytics.firstClassRate }}%</div>
            </div>
            <div class="stat-item">
              <div class="stat-label">Year</div>
              <div class="stat-value">{{ analytics.year }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import Chart from 'chart.js/auto';
  import analyticsService from '@/services/analyticsService';
  
  export default {
    name: 'ModuleAnalyticsComponent',
    props: {
      moduleId: {
        type: String,
        required: true
      },
      yourScore: {
        type: Number,
        default: null
      }
    },
    data() {
      return {
        loading: true,
        error: null,
        analytics: {
          studentCount: 0,
          averageScore: 0,
          medianScore: 0,
          highestScore: 0,
          lowestScore: 0,
          standardDeviation: 0,
          passRate: 0,
          firstClassRate: 0,
          lastUpdated: new Date(),
          year: '',
          gradeDistribution: []
        },
        chart: null
      };
    },
    async mounted() {
      await this.fetchAnalytics();
      // Add a small delay to ensure the DOM is fully rendered
      setTimeout(() => {
        this.renderGradeDistributionChart();
      }, 100);
    },
    beforeDestroy() {
      if (this.chart) {
        this.chart.destroy();
      }
    },
    methods: {
      async fetchAnalytics() {
        this.loading = true;
        this.error = null;
        
        try {
          const response = await analyticsService.getModuleDetails(this.moduleId);
          this.analytics = {
            studentCount: response.studentCount || 0,
            averageScore: response.averageScore || 0,
            medianScore: response.medianScore || 0,
            highestScore: response.highestScore || 0,
            lowestScore: response.lowestScore || 0,
            standardDeviation: response.standardDeviation || 0,
            passRate: response.passRate || 0,
            firstClassRate: response.firstClassRate || 0,
            lastUpdated: new Date(response.lastUpdated || Date.now()),
            year: response.year || '',
            gradeDistribution: response.gradeDistribution || []
          };
          
          this.$nextTick(() => {
            this.renderGradeDistributionChart();
          });
        } catch (error) {
          console.error('Error fetching module analytics:', error);
          this.error = 'Failed to load analytics data. Please try again later.';
        } finally {
          this.loading = false;
        }
      },
      
      renderGradeDistributionChart() {
        // Make sure the canvas element exists before attempting to render
        if (!this.$refs.gradeDistributionChart) {
          console.warn('Chart canvas element not found, deferring chart rendering');
          // Try again on next tick when DOM should be updated
          this.$nextTick(() => {
            setTimeout(() => this.renderGradeDistributionChart(), 50);
          });
          return;
        }
        
        // Clean up previous chart instance if it exists
        if (this.chart) {
          this.chart.destroy();
          this.chart = null;
        }
        
        const ctx = this.$refs.gradeDistributionChart.getContext('2d');
        
        // If context is still not available, try again later
        if (!ctx) {
          console.warn('Canvas context not available, deferring chart rendering');
          setTimeout(() => this.renderGradeDistributionChart(), 100);
          return;
        }
        
        // Default distribution if none is provided
        const distribution = this.analytics.gradeDistribution.length > 0 ? 
          this.analytics.gradeDistribution : 
          [
            { range: '0-10%', count: 0 },
            { range: '11-20%', count: 0 },
            { range: '21-30%', count: 0 },
            { range: '31-40%', count: 0 },
            { range: '41-50%', count: 0 },
            { range: '51-60%', count: 0 },
            { range: '61-70%', count: 0 },
            { range: '71-80%', count: 0 },
            { range: '81-90%', count: 0 },
            { range: '91-100%', count: 0 }
          ];
        
        // Get dark mode status to adjust chart colors
        const isDarkMode = document.body.classList.contains('dark-mode');
        
        const chartData = {
          labels: distribution.map(item => item.range),
          datasets: [{
            label: 'Number of Students',
            data: distribution.map(item => item.count),
            backgroundColor: distribution.map((_, index) => {
              // Generate colors for each bar - gradient from red to green
              const hue = index * 12; // 0 to 120 (red to green)
              return `hsla(${hue}, 80%, 60%, 0.7)`;
            }),
            borderColor: distribution.map((_, index) => {
              const hue = index * 12; 
              return `hsla(${hue}, 80%, 50%, 1)`;
            }),
            borderWidth: 1,
            borderRadius: 4
          }]
        };
        
        // Create a base configuration without annotations
        const chartOptions = {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              display: false
            },
            tooltip: {
              callbacks: {
                title: function(tooltipItems) {
                  return tooltipItems[0].label;
                },
                label: function(context) {
                  return `${context.parsed.y} students`;
                }
              }
            }
          },
          scales: {
            y: {
              beginAtZero: true,
              grid: {
                color: isDarkMode ? 'rgba(255, 255, 255, 0.1)' : 'rgba(0, 0, 0, 0.1)'
              },
              ticks: {
                precision: 0,
                color: isDarkMode ? '#cbd5e1' : '#333333'
              }
            },
            x: {
              grid: {
                display: false
              },
              ticks: {
                color: isDarkMode ? '#cbd5e1' : '#333333'
              }
            }
          }
        };
        
        // Add your score marker if provided - use Chart.js annotation plugin more safely
        if (this.yourScore !== null) {
          try {
            // We'll use a line on the chart as a visual marker instead of the annotations plugin
            // which might not be registered properly
            
            // Find which bin your score falls into
            const binSize = 10;
            const binIndex = Math.min(Math.floor(this.yourScore / binSize), 9); // Cap at 9 (91-100%)
            
            // Add a vertical line dataset instead of using annotations
            chartData.datasets.push({
              type: 'line',
              label: 'Your Score',
              data: Array(distribution.length).fill(null).map((_, i) => 
                i === binIndex ? Math.max(...distribution.map(d => d.count)) * 1.1 : null),
              borderColor: '#ff6b6b',
              borderWidth: 2,
              pointBackgroundColor: '#ff6b6b',
              pointRadius: i => i === binIndex ? 6 : 0,
              pointHoverRadius: i => i === binIndex ? 8 : 0,
              tension: 0
            });
          } catch (error) {
            console.warn('Failed to add score marker to chart:', error);
          }
        }
        
        // Safely create chart with try/catch
        try {
          this.chart = new Chart(ctx, {
            type: 'bar',
            data: chartData,
            options: chartOptions
          });
        } catch (error) {
          console.error('Error creating chart:', error);
        }
      },
      
      formatDate(date) {
        // Simple date formatter - customize as needed
        const options = { year: 'numeric', month: 'short', day: 'numeric' };
        return new Date(date).toLocaleDateString(undefined, options);
      },
      
      getScoreClass(score) {
        if (score >= 70) return 'excellent-score';
        if (score >= 60) return 'good-score';
        if (score >= 50) return 'average-score';
        if (score >= 40) return 'pass-score';
        return 'fail-score';
      },
      
      getDifferenceClass(difference) {
        if (difference >= 10) return 'diff-excellent';
        if (difference > 0) return 'diff-good';
        if (difference >= -5) return 'diff-average';
        return 'diff-below';
      },
      
      calculatePercentile(score) {
        // Calculate what percentile your score is in
        if (!this.analytics || !this.analytics.gradeDistribution) return 0;
        
        // Count students below your score
        let totalStudents = 0;
        let studentsBelow = 0;
        
        this.analytics.gradeDistribution.forEach(item => {
          // Extract the upper bound of the range (e.g., from "71-80%" get 80)
          const upperBound = parseInt(item.range.split('-')[1]);
          totalStudents += item.count;
          
          // If your score is higher than the upper bound, all students in this bin are below you
          if (score > upperBound) {
            studentsBelow += item.count;
          } 
          // If your score is within this range, assume half the students in this bin are below you
          else if (score >= parseInt(item.range.split('-')[0])) {
            studentsBelow += item.count / 2;
          }
        });
        
        return totalStudents > 0 ? Math.round((studentsBelow / totalStudents) * 100) : 0;
      }
    }
  };
  </script>
  
  <style scoped>
  .module-analytics {
    width: 100%;
    padding: 1.5rem;
    font-family: var(--font-main, 'Inter', sans-serif);
  }
  
  .loading-indicator {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 2rem;
  }
  
  .spinner {
    width: 40px;
    height: 40px;
    border: 4px solid rgba(123, 73, 255, 0.2);
    border-radius: 50%;
    border-top-color: var(--primary-color, #7b49ff);
    animation: spin 1s ease-in-out infinite;
    margin-bottom: 1rem;
  }
  
  @keyframes spin {
    to { transform: rotate(360deg); }
  }
  
  .error-message {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 2rem;
    color: var(--danger-color, #ef4444);
    text-align: center;
  }
  
  .error-message svg {
    color: var(--danger-color, #ef4444);
    margin-bottom: 1rem;
  }
  
  /* Summary Cards */
  .analytics-summary {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1.25rem;
    margin-bottom: 2rem;
  }
  
  .summary-card {
    display: flex;
    align-items: center;
    gap: 1rem;
    background-color: var(--bg-card, #ffffff);
    padding: 1.25rem;
    border-radius: var(--border-radius, 8px);
    box-shadow: var(--shadow-sm, 0 1px 3px rgba(0, 0, 0, 0.05));
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    border: 1px solid var(--border-color-light, #f1f5f9);
  }
  
  .summary-card:hover {
    transform: translateY(-3px);
    box-shadow: var(--shadow-md, 0 4px 12px rgba(0, 0, 0, 0.07));
  }
  
  .card-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 48px;
    height: 48px;
    border-radius: 12px;
    background: rgba(123, 73, 255, 0.1);
    color: var(--primary-color, #7b49ff);
  }
  
  .card-content {
    flex: 1;
  }
  
  .card-value {
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--text-primary, #333333);
    line-height: 1.2;
  }
  
  .card-label {
    font-size: 0.875rem;
    color: var(--text-secondary, #667085);
    font-weight: 500;
  }
  
  /* Student Count Card */
  .student-count .card-icon {
    background: rgba(52, 152, 219, 0.1);
    color: #3498db;
  }
  
  /* Average Score Card */
  .average-score .card-icon {
    background: rgba(46, 204, 113, 0.1);
    color: #2ecc71;
  }
  
  /* Median Score Card */
  .median-score .card-icon {
    background: rgba(241, 196, 15, 0.1);
    color: #f1c40f;
  }
  
  /* Updated Card */
  .updated .card-icon {
    background: rgba(155, 89, 182, 0.1);
    color: #9b59b6;
  }
  
  /* Chart Section */
  .chart-section {
    background-color: var(--bg-card, #ffffff);
    padding: 1.5rem;
    border-radius: var(--border-radius, 8px);
    box-shadow: var(--shadow-sm, 0 1px 3px rgba(0, 0, 0, 0.05));
    margin-bottom: 2rem;
    border: 1px solid var(--border-color-light, #f1f5f9);
  }
  
  .chart-section h3 {
    margin-top: 0;
    margin-bottom: 1.25rem;
    font-size: 1.25rem;
    font-weight: 700;
    color: var(--text-primary, #333333);
  }
  
  .chart-container {
    height: 300px;
    position: relative;
  }
  
  /* Your Score Section */
  .your-score-section {
    background-color: var(--bg-card, #ffffff);
    padding: 1.5rem;
    border-radius: var(--border-radius, 8px);
    box-shadow: var(--shadow-sm, 0 1px 3px rgba(0, 0, 0, 0.05));
    margin-bottom: 2rem;
    border: 1px solid var(--border-color-light, #f1f5f9);
  }
  
  .your-score-section h3 {
    margin-top: 0;
    margin-bottom: 1.25rem;
    font-size: 1.25rem;
    font-weight: 700;
    color: var(--text-primary, #333333);
  }
  
  .score-comparison {
    display: flex;
    justify-content: space-around;
    text-align: center;
  }
  
  .your-score,
  .score-difference,
  .percentile {
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  
  .score-value,
  .diff-value,
  .percentile-value {
    font-size: 2rem;
    font-weight: 800;
    margin-bottom: 0.5rem;
  }
  
  .score-label,
  .diff-label,
  .percentile-label {
    font-size: 0.875rem;
    color: var(--text-secondary, #667085);
    font-weight: 500;
  }
  
  /* Score classes */
  .excellent-score .score-value {
    color: #2ecc71;
  }
  
  .good-score .score-value {
    color: #3498db;
  }
  
  .average-score .score-value {
    color: #f1c40f;
  }
  
  .pass-score .score-value {
    color: #e67e22;
  }
  
  .fail-score .score-value {
    color: #e74c3c;
  }
  
  /* Difference classes */
  .diff-excellent .diff-value {
    color: #2ecc71;
  }
  
  .diff-good .diff-value {
    color: #3498db;
  }
  
  .diff-average .diff-value {
    color: #f1c40f;
  }
  
  .diff-below .diff-value {
    color: #e74c3c;
  }
  
  /* Stats Section */
  .stats-section {
    background-color: var(--bg-card, #ffffff);
    padding: 1.5rem;
    border-radius: var(--border-radius, 8px);
    box-shadow: var(--shadow-sm, 0 1px 3px rgba(0, 0, 0, 0.05));
    border: 1px solid var(--border-color-light, #f1f5f9);
  }
  
  .stats-section h3 {
    margin-top: 0;
    margin-bottom: 1.25rem;
    font-size: 1.25rem;
    font-weight: 700;
    color: var(--text-primary, #333333);
  }
  
  .stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 1rem;
  }
  
  .stat-item {
    padding: 1rem;
    background-color: var(--bg-accent, #f1f3f9);
    border-radius: var(--border-radius, 8px);
    transition: transform 0.3s ease;
  }
  
  .stat-item:hover {
    transform: translateY(-3px);
    box-shadow: var(--shadow-sm, 0 1px 3px rgba(0, 0, 0, 0.05));
  }
  
  .stat-label {
    font-size: 0.875rem;
    color: var(--text-secondary, #667085);
    font-weight: 500;
    margin-bottom: 0.5rem;
  }
  
  .stat-value {
    font-size: 1.25rem;
    font-weight: 700;
    color: var(--text-primary, #333333);
  }
  
  /* Responsive Adjustments */
  @media (max-width: 768px) {
    .module-analytics {
      padding: 1rem;
    }
    
    .analytics-summary {
      grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
      gap: 1rem;
    }
    
    .card-value {
      font-size: 1.25rem;
    }
    
    .chart-container {
      height: 250px;
    }
    
    .score-comparison {
      flex-direction: column;
      gap: 1.5rem;
    }
    
    .score-value,
    .diff-value,
    .percentile-value {
      font-size: 1.5rem;
    }
    
    .stats-grid {
      grid-template-columns: 1fr;
    }
  }
  </style>