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
import { ref, onMounted, onBeforeUnmount, watch, nextTick } from 'vue';

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
    let resizeObserver = null;
    let chartJsLoaded = false;
    let chartModules = null;

    // Preload Chart.js when component is created
    const preloadChartJs = async () => {
      try {
        chartModules = await import('chart.js');
        chartJsLoaded = true;
        return chartModules;
      } catch (err) {
        console.error('Failed to load Chart.js:', err);
        error.value = "Failed to load chart library";
        loading.value = false;
        return null;
      }
    };

    // Function to create and render the chart
    const renderChart = async () => {
      if (!chartCanvas.value) return;
      
      // Make sure we wait until the next DOM update cycle
      await nextTick();
      
      loading.value = true;
      error.value = null;

      try {
        // Ensure Chart.js is loaded
        if (!chartJsLoaded) {
          chartModules = await preloadChartJs();
          if (!chartModules) return;
        }
        
        const { Chart, registerables } = chartModules;
        Chart.register(...registerables);

        // Clean up previous chart if it exists
        if (chart.value) {
          chart.value.destroy();
          chart.value = null;
        }

        if (!props.yearData || props.yearData.length === 0) {
          error.value = "No data available to display";
          loading.value = false;
          return;
        }

        // Make sure the canvas has dimensions before drawing
        const canvas = chartCanvas.value;
        const container = canvas.parentElement;
        if (!canvas.offsetWidth || !canvas.offsetHeight) {
          // Force dimensions if needed
          canvas.style.width = '100%';
          canvas.style.height = container.offsetHeight + 'px';
          // Set explicit width and height attributes
          canvas.setAttribute('width', container.offsetWidth);
          canvas.setAttribute('height', container.offsetHeight || 250);
        }

        const ctx = canvas.getContext('2d');
        if (!ctx) {
          error.value = "Unable to get canvas context";
          loading.value = false;
          return;
        }

        // Generate gradient for the bars
        const gradient = ctx.createLinearGradient(0, 0, 0, 400);
        gradient.addColorStop(0, 'rgba(123, 73, 255, 0.8)'); // Primary color
        gradient.addColorStop(1, 'rgba(123, 73, 255, 0.3)');

        // Determine max credits for y-axis
        const maxCredits = Math.max(...props.yearData.map(y => y.credits || 0)) || 120;

        chart.value = new Chart(ctx, {
          type: 'bar',
          data: {
            labels: props.yearData.map(y => y.name || ''),
            datasets: [
              {
                label: 'Average Grade (%)',
                data: props.yearData.map(y => y.average || 0),
                backgroundColor: gradient,
                borderColor: 'rgba(123, 73, 255, 1)',
                borderWidth: 1,
                borderRadius: 6,
                barThickness: 40, // Reduced from 50
                maxBarThickness: 50,
                order: 1
              },
              {
                label: 'Credits Completed',
                data: props.yearData.map(y => y.credits || 0),
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
                },
                ticks: {
                  maxRotation: 45,
                  minRotation: 0
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
                max: maxCredits * 1.2, // 20% headroom
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
              duration: 800, // Reduced from 1000
              easing: 'easeOutQuart'
            }
          }
        });

        loading.value = false;
      } catch (err) {
        console.error('Error rendering chart:', err);
        error.value = "Failed to load chart: " + err.message;
        loading.value = false;
      }
    };

    // Method to redraw chart on container resize
    const resizeChart = () => {
      if (chart.value) {
        chart.value.resize();
      }
    };

    // Add redraw method for external calls
    const redrawChart = () => {
      // Delay rendering to ensure DOM is updated
      setTimeout(() => {
        renderChart();
      }, 100);
    };

    // Initialize chart when component is mounted
    onMounted(async () => {
      await preloadChartJs();
      
      // Wait for DOM to fully render
      setTimeout(() => {
        renderChart();
      }, 200);
      
      // Create resize observer to handle container resizing
      if (window.ResizeObserver) {
        resizeObserver = new ResizeObserver(() => {
          resizeChart();
        });
        
        if (chartCanvas.value?.parentElement) {
          resizeObserver.observe(chartCanvas.value.parentElement);
        }
      } else {
        // Fallback for browsers that don't support ResizeObserver
        window.addEventListener('resize', resizeChart);
      }
    });

    // Clean up when component is unmounted
    onBeforeUnmount(() => {
      if (chart.value) {
        chart.value.destroy();
        chart.value = null;
      }
      
      if (resizeObserver) {
        resizeObserver.disconnect();
      } else {
        window.removeEventListener('resize', resizeChart);
      }
    });

    // Re-render chart when data changes
    watch(() => props.yearData, () => {
      // Add a slight delay to ensure the DOM is updated
      setTimeout(() => {
        renderChart();
      }, 100);
    }, { deep: true });

    return {
      chartCanvas,
      loading,
      error,
      redrawChart
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
  background: rgba(255, 255, 255, 0.7);
  color: #666;
  font-size: 0.9rem;
  z-index: 10;
}

.dark-mode .chart-loading,
.dark-mode .chart-error {
  background: rgba(31, 41, 55, 0.7);
  color: #cbd5e1;
}

.spinner {
  width: 30px;
  height: 30px;
  border: 3px solid rgba(123, 73, 255, 0.3);
  border-radius: 50%;
  border-top-color: #7b49ff;
  animation: spin 1s ease-in-out infinite;
  margin-bottom: 10px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.chart-error {
  color: #e74c3c;
}

.dark-mode .chart-error {
  color: #f87171;
}
</style>