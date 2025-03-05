<template>
  <div class="chart-wrapper">
    <canvas ref="chartCanvas"></canvas>
    <div v-if="loading" class="chart-loading">
      <div class="spinner"></div>
      <span>Loading chart...</span>
    </div>
    <div v-if="error" class="chart-error">
      <span>{{ error }}</span>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, watch, computed } from 'vue';

export default {
  name: 'GradeDistributionChart',
  props: {
    // Accept either module data or direct score distribution
    moduleData: {
      type: Array,
      default: () => []
    },
    scoreDistribution: {
      type: Array,
      default: () => []
    }
  },
  setup(props) {
    const chartCanvas = ref(null);
    const chart = ref(null);
    const loading = ref(true);
    const error = ref(null);

    // Computed property to process the module data into grade distribution
    const distributionData = computed(() => {
      // If direct score distribution is provided, use it
      if (props.scoreDistribution && props.scoreDistribution.length > 0) {
        return props.scoreDistribution;
      }

      // Otherwise calculate from module data
      if (!props.moduleData || props.moduleData.length === 0) {
        return [];
      }

      const ranges = [
        { name: '0-39%', range: [0, 39], color: '#e74c3c' },
        { name: '40-49%', range: [40, 49], color: '#e67e22' },
        { name: '50-59%', range: [50, 59], color: '#f1c40f' },
        { name: '60-69%', range: [60, 69], color: '#3498db' },
        { name: '70-100%', range: [70, 100], color: '#2ecc71' }
      ];

      const scores = props.moduleData.map(m => m.score);

      return ranges.map(range => {
        return {
          name: range.name,
          count: scores.filter(score => score >= range.range[0] && score <= range.range[1]).length,
          color: range.color
        };
      });
    });

    // Function to create and render the chart
    const renderChart = async () => {
      if (!chartCanvas.value) return;

      loading.value = true;
      error.value = null;

      try {
        // Clean up previous chart if it exists
        if (chart.value) {
          chart.value.destroy();
        }

        // Dynamic import of Chart.js
        const { Chart, registerables } = await import('chart.js');
        Chart.register(...registerables);

        const data = distributionData.value;

        if (!data || data.length === 0) {
          error.value = "No data available to display";
          loading.value = false;
          return;
        }

        const ctx = chartCanvas.value.getContext('2d');

        chart.value = new Chart(ctx, {
          type: 'bar',
          data: {
            labels: data.map(d => d.name),
            datasets: [{
              label: 'Number of Modules',
              data: data.map(d => d.count),
              backgroundColor: data.map(d => d.color || '#7b49ff'),
              borderColor: data.map(d => d.color ? d.color + '80' : '#6739ef'),
              borderWidth: 1,
              borderRadius: 6,
              barThickness: 40,
            }]
          },
          options: {
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
                    return `Modules: ${context.raw}`;
                  }
                }
              }
            },
            scales: {
              y: {
                beginAtZero: true,
                ticks: {
                  precision: 0, // Only show integers
                  stepSize: 1,
                },
                grid: {
                  display: true,
                  drawBorder: false,
                }
              },
              x: {
                grid: {
                  display: false,
                  drawBorder: false,
                }
              }
            },
            animation: {
              duration: 1000,
              easing: 'easeOutQuart'
            }
          }
        });

        loading.value = false;
      } catch (err) {
        console.error('Error rendering chart:', err);
        error.value = "Failed to load chart";
        loading.value = false;
      }
    };

    // Initialize chart when component is mounted
    onMounted(() => {
      renderChart();
    });

    // Re-render chart when data changes
    watch(() => props.moduleData, () => {
      renderChart();
    }, { deep: true });

    watch(() => props.scoreDistribution, () => {
      renderChart();
    }, { deep: true });

    return {
      chartCanvas,
      loading,
      error
    };
  }
};
</script>

<style scoped>
.chart-wrapper {
  position: relative;
  width: 100%;
  height: 100%;
  min-height: 250px;
}

.chart-loading,
.chart-error {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: rgba(var(--bg-card-rgb), 0.7);
  color: var(--text-secondary);
  font-size: 0.9rem;
}

.spinner {
  width: 30px;
  height: 30px;
  border: 3px solid rgba(var(--primary-color-rgb), 0.3);
  border-radius: 50%;
  border-top-color: var(--primary-color);
  animation: spin 1s ease-in-out infinite;
  margin-bottom: 10px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.chart-error {
  color: var(--error-color);
}

/* Light/dark mode adaptations */
:deep(.chartjs-tooltip) {
  background-color: var(--bg-card) !important;
  color: var(--text-primary) !important;
  border: 1px solid var(--border-color) !important;
  border-radius: var(--border-radius) !important;
  padding: 8px 12px !important;
  box-shadow: var(--shadow-md) !important;
  font-size: 12px !important;
}
</style>