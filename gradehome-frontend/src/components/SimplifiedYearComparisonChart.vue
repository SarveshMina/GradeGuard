SimplifiedYearComparisonChart<template>
    <div class="year-comparison-chart-container">
      <!-- Static fallback UI that will definitely display -->
      <div v-if="isShowingFallback" class="fallback-display">
        <h4>Year Comparison</h4>
        <div v-if="hasData" class="fallback-data">
          <div v-for="(year, index) in yearData" :key="index" class="fallback-year">
            <h5>{{ year.name }}</h5>
            <div class="fallback-stats">
              <div class="stat">
                <div class="label">Average:</div>
                <div class="value">{{ year.average }}%</div>
              </div>
              <div class="stat">
                <div class="label">Highest:</div>
                <div class="value">{{ year.highest }}%</div>
              </div>
              <div class="stat">
                <div class="label">Lowest:</div>
                <div class="value">{{ year.lowest }}%</div>
              </div>
            </div>
          </div>
        </div>
        <p v-else>No year comparison data available yet.</p>
        <button @click="tryChartAgain" class="try-chart-button">Try Chart View</button>
      </div>
      
      <!-- Actual chart (shown only when not in fallback mode) -->
      <div v-else>
        <div v-if="loading" class="chart-loading">
          <div class="loading-spinner"></div>
          <span>Loading chart...</span>
        </div>
        <div v-else-if="error" class="chart-error">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="12" y1="8" x2="12" y2="12"></line>
            <line x1="12" y1="16" x2="12.01" y2="16"></line>
          </svg>
          <p>{{ error }}</p>
          <div class="button-group">
            <button @click="tryChartAgain" class="retry-button">Retry</button>
            <button @click="showFallback" class="fallback-button">Show Simple View</button>
          </div>
        </div>
        <div v-else-if="!hasData" class="no-data-message">
          <p>No year comparison data available yet. Add modules from different years to see a comparison.</p>
        </div>
        <div v-else class="chart-wrapper" ref="chartWrapper"></div>
      </div>
    </div>
  </template>
  
  <script>
  import Chart from 'chart.js/auto';
  
  export default {
    name: 'YearComparisonChart',
    
    props: {
      yearData: {
        type: Array,
        default: () => []
      }
    },
    
    data() {
      return {
        chart: null,
        loading: true,
        error: null,
        renderAttempts: 0,
        maxRenderAttempts: 5,
        canvasCreated: false,
        chartCanvas: null,
        renderTimer: null,
        isShowingFallback: false, // New property to control fallback view
        debugInfo: {
          wrapperWidth: 0,
          wrapperHeight: 0,
          dataCount: 0
        }
      };
    },
    
    computed: {
      hasData() {
        return this.yearData && this.yearData.length > 0;
      }
    },
    
    watch: {
      yearData: {
        handler(newData) {
          // Update debug info
          this.debugInfo.dataCount = newData ? newData.length : 0;
          console.log(`YearComparisonChart: yearData updated with ${this.debugInfo.dataCount} items`);
          
          // Only try to render chart if not in fallback mode
          if (!this.isShowingFallback) {
            this.renderAttempts = 0;
            this.renderChart();
          }
        },
        deep: true
      }
    },
    
    mounted() {
      console.log("YearComparisonChart mounted");
      
      // Log the container dimensions to help debug
      this.$nextTick(() => {
        const container = this.$el;
        console.log("Chart container dimensions:", {
          width: container.clientWidth,
          height: container.clientHeight,
          offsetWidth: container.offsetWidth,
          offsetHeight: container.offsetHeight
        });
      });
      
      // Try chart rendering first
      setTimeout(() => {
        if (!this.isShowingFallback) {
          this.createCanvas();
          this.renderChart();
        }
      }, 200);
      
      // Add a fallback that switches to text view if chart doesn't render
      setTimeout(() => {
        if (this.loading && !this.chart && !this.isShowingFallback) {
          console.log("Chart still loading after delay, switching to fallback view");
          this.showFallback();
        }
      }, 2000);
    },
    
    beforeDestroy() {
      if (this.renderTimer) {
        clearTimeout(this.renderTimer);
      }
      this.destroyChart();
    },
    
    methods: {
      // Method to switch to fallback view
      showFallback() {
        this.isShowingFallback = true;
        this.destroyChart();
        console.log("Switched to fallback view");
      },
      
      // Method to try chart view again
      tryChartAgain() {
        this.isShowingFallback = false;
        this.error = null;
        this.loading = true;
        this.renderAttempts = 0;
        
        // Reset and try again
        this.$nextTick(() => {
          this.createCanvas();
          this.renderChart();
        });
        
        console.log("Attempting to show chart view again");
      },
      
      createCanvas() {
        const wrapper = this.$refs.chartWrapper;
        if (!wrapper) {
          console.warn("Chart wrapper not found, deferring canvas creation");
          this.$nextTick(() => {
            setTimeout(() => this.createCanvas(), 100);
          });
          return;
        }
        
        // Log wrapper dimensions for debugging
        this.debugInfo.wrapperWidth = wrapper.clientWidth;
        this.debugInfo.wrapperHeight = wrapper.clientHeight;
        console.log("Chart wrapper dimensions:", this.debugInfo);
        
        // Ensure wrapper has a minimum height
        if (wrapper.clientHeight < 200) {
          wrapper.style.height = '300px';
          console.log("Forced minimum height on wrapper");
        }
        
        // Create canvas element
        this.chartCanvas = document.createElement('canvas');
        this.chartCanvas.style.width = '100%';
        this.chartCanvas.style.height = '100%';
        wrapper.appendChild(this.chartCanvas);
        this.canvasCreated = true;
        console.log("Canvas created successfully");
      },
      
      destroyChart() {
        if (this.chart) {
          try {
            this.chart.destroy();
          } catch (error) {
            console.error("Error destroying chart:", error);
          }
          this.chart = null;
        }
      },
      
      renderChart() {
        // Don't try to render in fallback mode
        if (this.isShowingFallback) {
          this.loading = false;
          return;
        }
        
        this.loading = true;
        this.error = null;
        
        console.log("Rendering chart attempt", this.renderAttempts + 1);
        
        // Don't try to render if we don't have data
        if (!this.hasData) {
          console.log("No year data available, skipping chart render");
          this.loading = false;
          return;
        }
        
        // Make sure canvas is created
        if (!this.canvasCreated) {
          this.createCanvas();
          
          if (this.renderAttempts >= this.maxRenderAttempts) {
            this.error = "Failed to create chart canvas. Try the simple view instead.";
            this.loading = false;
            return;
          }
          
          console.warn(`Year chart canvas not created yet, attempt ${this.renderAttempts + 1}/${this.maxRenderAttempts}`);
          this.renderAttempts++;
          
          this.renderTimer = setTimeout(() => {
            this.renderChart();
          }, 200);
          return;
        }
        
        // Make sure the wrapper exists in the DOM
        const wrapper = this.$refs.chartWrapper;
        if (!wrapper) {
          if (this.renderAttempts >= this.maxRenderAttempts) {
            this.error = "Failed to find chart container. Try the simple view instead.";
            this.loading = false;
            return;
          }
          
          console.warn(`Chart wrapper not found, attempt ${this.renderAttempts + 1}/${this.maxRenderAttempts}`);
          this.renderAttempts++;
          
          this.renderTimer = setTimeout(() => {
            this.renderChart();
          }, 200);
          return;
        }
        
        // Clean up any existing chart
        this.destroyChart();
        
        try {
          const ctx = this.chartCanvas.getContext('2d');
          
          if (!ctx) {
            if (this.renderAttempts >= this.maxRenderAttempts) {
              this.error = "Failed to get canvas context. Try the simple view instead.";
              this.loading = false;
              return;
            }
            
            console.warn(`Canvas context not available, attempt ${this.renderAttempts + 1}/${this.maxRenderAttempts}`);
            this.renderAttempts++;
            
            this.renderTimer = setTimeout(() => {
              this.renderChart();
            }, 250);
            return;
          }
          
          // Set explicit dimensions
          const parentWidth = wrapper.clientWidth || 300;
          const parentHeight = wrapper.clientHeight || 300;
          
          console.log("Setting canvas dimensions:", parentWidth, "x", parentHeight);
          this.chartCanvas.width = parentWidth;
          this.chartCanvas.height = parentHeight;
          
          // Prepare chart data
          const labels = this.yearData.map(year => year.name);
          const averageData = this.yearData.map(year => year.average);
          const highestData = this.yearData.map(year => year.highest || 0);
          const lowestData = this.yearData.map(year => year.lowest || 0);
          
          // Get dark mode status to adjust chart colors
          const isDarkMode = document.body.classList.contains('dark-mode');
          
          // Create the chart with a simpler configuration
          this.chart = new Chart(ctx, {
            type: 'bar',
            data: {
              labels: labels,
              datasets: [
                {
                  label: 'Average',
                  data: averageData,
                  backgroundColor: 'rgba(123, 73, 255, 0.7)', // Primary color
                  borderColor: 'rgba(123, 73, 255, 1)',
                  borderWidth: 1
                },
                {
                  label: 'Highest',
                  data: highestData,
                  backgroundColor: 'rgba(46, 204, 113, 0.7)', // Green
                  borderColor: 'rgba(46, 204, 113, 1)',
                  borderWidth: 1
                },
                {
                  label: 'Lowest',
                  data: lowestData,
                  backgroundColor: 'rgba(231, 76, 60, 0.7)', // Red
                  borderColor: 'rgba(231, 76, 60, 1)',
                  borderWidth: 1
                }
              ]
            },
            options: {
              responsive: true,
              maintainAspectRatio: false,
              plugins: {
                legend: {
                  display: true,
                  position: 'top'
                }
              }
            }
          });
          
          // Chart successfully created
          this.renderAttempts = 0;
          this.loading = false;
          console.log("Year comparison chart rendered successfully");
        } catch (error) {
          console.error('Error creating year comparison chart:', error);
          
          if (this.renderAttempts >= this.maxRenderAttempts) {
            this.error = "Failed to create chart due to an error. Try the simple view instead.";
            this.loading = false;
            return;
          }
          
          // Try again after a delay
          this.renderAttempts++;
          this.renderTimer = setTimeout(() => {
            this.renderChart();
          }, 300);
        }
      },
      
      redrawChart() {
        if (this.isShowingFallback) {
          return; // Don't attempt redraw in fallback mode
        }
        
        this.renderAttempts = 0;
        this.renderChart();
      }
    }
  };
  </script>
  
  <style scoped>
  .year-comparison-chart-container {
    width: 100%;
    height: 100%;
    min-height: 300px !important;
    position: relative;
    background-color: var(--bg-card, #ffffff);
    border-radius: var(--border-radius, 8px);
    overflow: hidden;
  }
  
  /* Ensure the container has a visible background */
  .chart-wrapper {
    width: 100%;
    height: 100%;
    min-height: 300px !important;
    background-color: var(--bg-card, #ffffff);
  }
  
  /* Fallback display styling */
  .fallback-display {
    padding: 1.5rem;
    height: 100%;
    min-height: 300px;
    display: flex;
    flex-direction: column;
    color: var(--text-primary, #333333);
  }
  
  .fallback-display h4 {
    margin-top: 0;
    margin-bottom: 1.5rem;
    font-size: 1.25rem;
    font-weight: 700;
    color: var(--text-primary, #333333);
    border-bottom: 2px solid var(--primary-color, #7b49ff);
    padding-bottom: 0.5rem;
    display: inline-block;
  }
  
  .fallback-data {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    flex: 1;
  }
  
  .fallback-year {
    background-color: var(--bg-accent, #f1f3f9);
    padding: 1rem;
    border-radius: var(--border-radius, 8px);
    border-left: 4px solid var(--primary-color, #7b49ff);
  }
  
  .fallback-year h5 {
    margin-top: 0;
    margin-bottom: 0.75rem;
    font-size: 1rem;
    font-weight: 600;
  }
  
  .fallback-stats {
    display: flex;
    gap: 1rem;
    flex-wrap: wrap;
  }
  
  .stat {
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }
  
  .label {
    font-weight: 500;
    color: var(--text-secondary, #667085);
  }
  
  .value {
    font-weight: 700;
    color: var(--text-primary, #333333);
  }
  
  .try-chart-button {
    align-self: center;
    margin-top: 1.5rem;
    padding: 0.75rem 1.5rem;
    background-color: var(--primary-color, #7b49ff);
    color: white;
    border: none;
    border-radius: 20px;
    cursor: pointer;
    font-weight: 500;
    box-shadow: 0 2px 6px rgba(123, 73, 255, 0.3);
    transition: all 0.3s ease;
  }
  
  .try-chart-button:hover {
    background-color: var(--primary-dark, #6038cc);
    transform: translateY(-2px);
    box-shadow: 0 4px 10px rgba(123, 73, 255, 0.4);
  }
  
  /* Styling for chart view */
  .chart-loading,
  .chart-error,
  .no-data-message {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    min-height: 300px;
    text-align: center;
    padding: 2rem;
    color: var(--text-secondary, #667085);
  }
  
  .chart-error {
    color: var(--danger-color, #ef4444);
  }
  
  .button-group {
    display: flex;
    gap: 1rem;
    margin-top: 1rem;
  }
  
  .retry-button, 
  .fallback-button {
    padding: 0.5rem 1rem;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-weight: 500;
    transition: all 0.2s ease;
  }
  
  .retry-button {
    background-color: var(--primary-color, #7b49ff);
    color: white;
  }
  
  .retry-button:hover {
    background-color: var(--primary-dark, #6038cc);
  }
  
  .fallback-button {
    background-color: #f1f3f9;
    color: #333;
    border: 1px solid #ccc;
  }
  
  .fallback-button:hover {
    background-color: #e5e7eb;
  }
  
  .no-data-message {
    background-color: var(--bg-accent, #f1f3f9);
    border-radius: var(--border-radius, 8px);
    border: 1px dashed var(--border-color, #e2e8f0);
  }
  
  .loading-spinner {
    width: 36px;
    height: 36px;
    border: 3px solid rgba(123, 73, 255, 0.2);
    border-radius: 50%;
    border-top-color: var(--primary-color, #7b49ff);
    animation: spin 1s ease-in-out infinite;
    margin-bottom: 1rem;
  }
  
  @keyframes spin {
    to { transform: rotate(360deg); }
  }
  </style>