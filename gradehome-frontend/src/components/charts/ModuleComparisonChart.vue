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
  name: 'ModuleComparisonChart',
  props: {
    moduleData: {
      type: Object,
      required: true
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

        if (!props.moduleData || !props.moduleData.assessments) {
          error.value = "No module data available to display";
          loading.value = false;
          return;
        }

        const ctx = chartCanvas.value.getContext('2d');

        // Mock class average data - in a real app this would come from the backend
        // Here we're just creating some realistic comparison data
        const mockClassAverages = props.moduleData.assessments.map(assessment => {
          // Generate class average that's typically 5-15% lower than the student's score
          const variance = Math.random() * 10 + 5;
          // Occasionally have the class average be higher
          const isHigher = Math.random() > 0.8;
          return isHigher
              ? Math.min(100, assessment.score + Math.random() * 5)
              : Math.max(0, assessment.score - variance);
        });

        chart.value = new Chart(ctx, {
          type: 'bar',
          data: {
            labels: props.moduleData.assessments.map(a => a.name),
            datasets: [
              {
                label: 'Your Score',
                data: props.moduleData.assessments.map(a => a.score),
                backgroundColor: 'rgba(123, 73, 255, 0.7)',
                borderColor: 'rgba(123, 73, 255, 1)',
                borderWidth: 1,
                borderRadius: 6,
                barPercentage: 0.5,
                categoryPercentage: 0.8
              },
              {
                label: 'Class Average',
                data: mockClassAverages.map(avg => Math.round(avg * 10) / 10),
                backgroundColor: 'rgba(149, 165, 166, 0.5)',
                borderColor: 'rgba(149, 165, 166, 0.8)',
                borderWidth: 1,
                borderRadius: 6,
                barPercentage: 0.5,
                categoryPercentage: 0.8
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
                align: 'end',
                labels: {
                  boxWidth: 15,
                  usePointStyle: true,
                  pointStyle: 'rectRounded'
                }
              },
              tooltip: {
                padding: 10,
                callbacks: {
                  label: function(context) {
                    let label = context.dataset.label || '';
                    if (label) {
                      label += ': ';
                    }
                    label += context.parsed.y.toFixed(1) + '%';
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
                min: 0,
                max: 100,
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
              duration: 1000
            }
          }
        });

        loading.value = false;
      } catch (err) {
        console.error('Error rendering module comparison chart:', err);
        error.value = "Failed to load comparison chart";
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