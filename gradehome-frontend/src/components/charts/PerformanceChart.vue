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
  name: 'PerformanceChart',
  props: {
    performanceData: {
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

        if (!props.performanceData || props.performanceData.length === 0) {
          error.value = "No performance data available to display";
          loading.value = false;
          return;
        }

        const ctx = chartCanvas.value.getContext('2d');

        // Create fill gradient
        const gradientFill = ctx.createLinearGradient(0, 0, 0, 400);
        gradientFill.addColorStop(0, 'rgba(123, 73, 255, 0.4)');
        gradientFill.addColorStop(1, 'rgba(123, 73, 255, 0.0)');

        chart.value = new Chart(ctx, {
          type: 'line',
          data: {
            labels: props.performanceData.map(d => d.name),
            datasets: [
              {
                label: 'Average Grade',
                data: props.performanceData.map(d => d.average),
                borderColor: 'rgba(123, 73, 255, 1)',
                backgroundColor: gradientFill,
                borderWidth: 3,
                tension: 0.4,
                fill: true,
                pointBackgroundColor: 'white',
                pointBorderColor: 'rgba(123, 73, 255, 1)',
                pointBorderWidth: 2,
                pointRadius: 5,
                pointHoverRadius: 7
              },
              {
                label: 'Highest Grade',
                data: props.performanceData.map(d => d.highest),
                borderColor: 'rgba(46, 204, 113, 0.8)',
                borderWidth: 2,
                borderDash: [5, 5],
                tension: 0.4,
                pointStyle: 'rectRot',
                pointRadius: 4,
                pointBackgroundColor: 'rgba(46, 204, 113, 0.8)',
                fill: false
              },
              {
                label: 'Lowest Grade',
                data: props.performanceData.map(d => d.lowest),
                borderColor: 'rgba(231, 76, 60, 0.8)',
                borderWidth: 2,
                borderDash: [5, 5],
                tension: 0.4,
                pointStyle: 'rectRot',
                pointRadius: 4,
                pointBackgroundColor: 'rgba(231, 76, 60, 0.8)',
                fill: false
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
                position: 'top',
                labels: {
                  usePointStyle: true,
                  boxWidth: 8
                }
              },
              tooltip: {
                backgroundColor: 'rgba(255, 255, 255, 0.9)',
                titleColor: '#333',
                bodyColor: '#666',
                borderColor: 'rgba(123, 73, 255, 0.3)',
                borderWidth: 1,
                padding: 12,
                cornerRadius: 8,
                caretSize: 6,
                callbacks: {
                  label: function(context) {
                    let label = context.dataset.label || '';
                    if (label) {
                      label += ': ';
                    }
                    label += context.parsed.y.toFixed(1) + '%';
                    return label;
                  },
                  footer: function(tooltipItems) {
                    const dataIndex = tooltipItems[0].dataIndex;
                    const moduleCount = props.performanceData[dataIndex]?.count || 0;
                    return `Number of modules: ${moduleCount}`;
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
                min: Math.min(...props.performanceData.map(d => d.lowest)) - 5 || 0,
                max: Math.max(100, ...props.performanceData.map(d => d.highest) + 5),
                ticks: {
                  callback: function(value) {
                    return value + '%';
                  }
                },
                grid: {
                  color: 'rgba(200, 200, 200, 0.1)',
                  drawBorder: false
                }
              }
            },
            animation: {
              duration: 1500,
              easing: 'easeOutQuart'
            },
            elements: {
              point: {
                hoverBorderWidth: 3
              }
            }
          }
        });

        loading.value = false;
      } catch (err) {
        console.error('Error rendering chart:', err);
        error.value = "Failed to load performance chart";
        loading.value = false;
      }
    };

    // Initialize chart when component is mounted
    onMounted(() => {
      renderChart();
    });

    // Re-render chart when data changes
    watch(() => props.performanceData, () => {
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
  min-height: 300px;
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