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
import { ref, onMounted, watch } from 'vue';

export default {
  name: 'StrengthsRadarChart',
  props: {
    strengthsData: {
      type: Array,
      default: () => []
    }
  },
  setup(props) {
    const chartCanvas = ref(null);
    const chart = ref(null);
    const loading = ref(true);
    const error = ref(null);

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

        if (!props.strengthsData || props.strengthsData.length === 0) {
          error.value = "No strengths data available to display";
          loading.value = false;
          return;
        }

        const ctx = chartCanvas.value.getContext('2d');

        chart.value = new Chart(ctx, {
          type: 'radar',
          data: {
            labels: props.strengthsData.map(d => d.subject),
            datasets: [
              {
                label: 'Your Strengths',
                data: props.strengthsData.map(d => d.score),
                backgroundColor: 'rgba(123, 73, 255, 0.3)',
                borderColor: 'rgba(123, 73, 255, 0.8)',
                borderWidth: 2,
                pointBackgroundColor: 'rgba(123, 73, 255, 1)',
                pointBorderColor: '#fff',
                pointHoverBackgroundColor: '#fff',
                pointHoverBorderColor: 'rgba(123, 73, 255, 1)',
                pointRadius: 4,
                pointHoverRadius: 6
              }
            ]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
              r: {
                min: 0,
                max: 100,
                ticks: {
                  stepSize: 20,
                  display: false,
                  backdropColor: 'transparent'
                },
                pointLabels: {
                  font: {
                    family: 'inherit',
                    size: 12,
                    weight: '500'
                  },
                  color: 'var(--text-primary)'
                },
                grid: {
                  color: 'rgba(200, 200, 200, 0.15)'
                },
                angleLines: {
                  color: 'rgba(200, 200, 200, 0.25)'
                }
              }
            },
            plugins: {
              legend: {
                display: false
              },
              tooltip: {
                backgroundColor: 'rgba(255, 255, 255, 0.9)',
                titleColor: '#333',
                bodyColor: '#666',
                borderColor: 'rgba(123, 73, 255, 0.3)',
                borderWidth: 1,
                padding: 10,
                callbacks: {
                  label: function(context) {
                    return `Score: ${context.parsed.r}%`;
                  }
                }
              }
            },
            elements: {
              line: {
                tension: 0.1
              }
            },
            animation: {
              duration: 1200,
              easing: 'easeOutQuart'
            }
          }
        });

        loading.value = false;
      } catch (err) {
        console.error('Error rendering radar chart:', err);
        error.value = "Failed to load strengths chart";
        loading.value = false;
      }
    };

    // Initialize chart when component is mounted
    onMounted(() => {
      renderChart();
    });

    // Re-render chart when data changes
    watch(() => props.strengthsData, () => {
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
</style>