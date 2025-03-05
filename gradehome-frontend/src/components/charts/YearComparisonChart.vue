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
  name: 'YearComparisonChart',
  props: {
    yearData: {
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

        if (!props.yearData || props.yearData.length === 0) {
          error.value = "No data available to display";
          loading.value = false;
          return;
        }

        const ctx = chartCanvas.value.getContext('2d');

        // Generate gradient for the bars
        const gradient = ctx.createLinearGradient(0, 0, 0, 400);
        gradient.addColorStop(0, 'rgba(123, 73, 255, 0.8)'); // Primary color
        gradient.addColorStop(1, 'rgba(123, 73, 255, 0.3)');

        chart.value = new Chart(ctx, {
          type: 'bar',
          data: {
            labels: props.yearData.map(y => y.name),
            datasets: [
              {
                label: 'Average Grade (%)',
                data: props.yearData.map(y => y.average),
                backgroundColor: gradient,
                borderColor: 'rgba(123, 73, 255, 1)',
                borderWidth: 1,
                borderRadius: 6,
                barThickness: 50,
                order: 1
              },
              {
                label: 'Credits Completed',
                data: props.yearData.map(y => y.credits),
                type: 'line',
                borderColor: '#3498db',
                backgroundColor: 'rgba(52, 152, 219, 0.3)',
                pointBackgroundColor: '#3498db',
                pointBorderColor: '#fff',
                pointRadius: 5,
                fill: false,
                tension: 0.2,
                yAxisID: 'y1',
                order: 0
              }
            ]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
              intersect: false,
              mode: 'index'
            },
            plugins: {
              legend: {
                position: 'bottom',
                labels: {
                  usePointStyle: true,
                  boxWidth: 6
                }
              },
              tooltip: {
                padding: 12,
                caretSize: 6,
                callbacks: {
                  label: function(context) {
                    let label = context.dataset.label || '';
                    if (label) {
                      label += ': ';
                    }
                    if (context.datasetIndex === 0) {
                      label += context.raw.toFixed(1) + '%';
                    } else {
                      label += context.raw;
                    }
                    return label;
                  }
                }
              }
            },
            scales: {
              x: {
                grid: {
                  display: false,
                  drawBorder: false
                }
              },
              y: {
                beginAtZero: true,
                max: 100,
                title: {
                  display: true,
                  text: 'Average Grade (%)'
                },
                grid: {
                  display: true,
                  drawBorder: false
                }
              },
              y1: {
                position: 'right',
                beginAtZero: true,
                max: Math.max(...props.yearData.map(y => y.credits)) * 1.2 || 120, // 20% headroom
                title: {
                  display: true,
                  text: 'Credits'
                },
                grid: {
                  display: false,
                  drawBorder: false
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
    watch(() => props.yearData, () => {
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