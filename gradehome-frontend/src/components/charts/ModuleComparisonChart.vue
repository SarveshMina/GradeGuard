<template>
  <div class="comparison-chart">
    <div v-if="loading" class="chart-loading">
      <div class="loading-spinner"></div>
      <span>Loading chart...</span>
    </div>
    <canvas ref="chartCanvas" v-show="!loading"></canvas>
  </div>
</template>

<script>
import Chart from 'chart.js/auto';

export default {
  name: 'ModuleComparisonChart',
  
  props: {
    moduleData: {
      type: Object,
      required: true
    }
  },
  
  data() {
    return {
      chart: null,
      loading: true
    };
  },
  
  watch: {
    moduleData: {
      handler() {
        // Re-render chart when the module data changes
        this.renderChart();
      },
      deep: true
    }
  },
  
  mounted() {
    // Delay chart rendering to ensure the DOM is ready
    setTimeout(() => {
      this.renderChart();
    }, 100);
  },
  
  beforeDestroy() {
    // Clean up the chart instance
    if (this.chart) {
      this.chart.destroy();
      this.chart = null;
    }
  },
  
  methods: {
    renderChart() {
      this.loading = true;
      
      // Make sure we have a valid canvas element
      if (!this.$refs.chartCanvas) {
        console.warn('Chart canvas element not found, deferring chart rendering');
        // Try again on next tick when DOM should be updated
        this.$nextTick(() => {
          setTimeout(() => this.renderChart(), 50);
        });
        return;
      }
      
      // Clean up previous chart instance if it exists
      if (this.chart) {
        this.chart.destroy();
        this.chart = null;
      }
      
      // Get the canvas context
      const ctx = this.$refs.chartCanvas.getContext('2d');
      
      // If context is still not available, try again later
      if (!ctx) {
        console.warn('Canvas context not available, deferring chart rendering');
        setTimeout(() => this.renderChart(), 100);
        return;
      }
      
      // Get module data and prepare for chart
      const { score } = this.moduleData;
      const studentScore = score || 0;
      
      // Prepare simulated class data if not available
      // In a real implementation, this would come from analytics API
      const classAverage = 65; // Example value
      const classHighest = 92; // Example value
      const classLowest = 38;  // Example value
      
      // Prepare the chart data
      const data = {
        labels: ['Your Score', 'Class Average', 'Class Highest', 'Class Lowest'],
        datasets: [{
          label: 'Scores',
          data: [studentScore, classAverage, classHighest, classLowest],
          backgroundColor: [
            'rgba(123, 73, 255, 0.7)',   // Your score - primary color
            'rgba(52, 152, 219, 0.7)',   // Class average - blue
            'rgba(46, 204, 113, 0.7)',   // Class highest - green
            'rgba(231, 76, 60, 0.7)'     // Class lowest - red
          ],
          borderColor: [
            'rgba(123, 73, 255, 1)',
            'rgba(52, 152, 219, 1)',
            'rgba(46, 204, 113, 1)',
            'rgba(231, 76, 60, 1)'
          ],
          borderWidth: 1,
          borderRadius: 4
        }]
      };
      
      // Check for dark mode
      const isDarkMode = document.body.classList.contains('dark-mode');
      
      // Chart configuration
      const options = {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: {
            beginAtZero: true,
            max: 100,
            grid: {
              color: isDarkMode ? 'rgba(255, 255, 255, 0.1)' : 'rgba(0, 0, 0, 0.1)'
            },
            ticks: {
              callback: function(value) {
                return value + '%';
              },
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
        },
        plugins: {
          legend: {
            display: false
          },
          tooltip: {
            callbacks: {
              label: function(context) {
                return context.raw + '%';
              }
            }
          }
        }
      };
      
      // Try to create the chart with error handling
      try {
        this.chart = new Chart(ctx, {
          type: 'bar',
          data: data,
          options: options
        });
        
        this.loading = false;
      } catch (error) {
        console.error('Error creating comparison chart:', error);
        this.loading = false;
      }
    },
    
    redrawChart() {
      // Public method that can be called from parent to force redraw
      // (useful after orientation changes or tab switches)
      this.renderChart();
    }
  }
};
</script>

<style scoped>
.comparison-chart {
  position: relative;
  height: 250px;
}

.chart-loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: var(--text-secondary, #667085);
}

.loading-spinner {
  width: 30px;
  height: 30px;
  border: 3px solid rgba(123, 73, 255, 0.2);
  border-radius: 50%;
  border-top-color: var(--primary-color, #7b49ff);
  animation: spin 1s ease-in-out infinite;
  margin-bottom: 0.5rem;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>