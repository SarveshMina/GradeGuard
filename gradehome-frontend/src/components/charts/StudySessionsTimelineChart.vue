<template>
  <div class="chart-wrapper">
    <canvas ref="chartCanvas"></canvas>
  </div>
</template>

<script>
import { Chart, registerables } from 'chart.js';
Chart.register(...registerables);

export default {
  name: 'StudySessionsTimelineChart',
  props: {
    chartData: {
      type: Object,
      required: true,
      default: () => ({
        labels: [],
        datasets: []
      })
    }
  },
  data() {
    return {
      chart: null
    };
  },
  mounted() {
    this.createChart();
  },
  methods: {
    createChart() {
      const ctx = this.$refs.chartCanvas.getContext('2d');

      this.chart = new Chart(ctx, {
        type: 'line',
        data: this.chartData,
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            y: {
              beginAtZero: true,
              ticks: {
                stepSize: 1,
                color: getComputedStyle(document.documentElement).getPropertyValue('--text-secondary')
              },
              grid: {
                color: getComputedStyle(document.documentElement).getPropertyValue('--border-color-light')
              },
              title: {
                display: true,
                text: 'Number of Sessions',
                color: getComputedStyle(document.documentElement).getPropertyValue('--text-secondary')
              }
            },
            x: {
              ticks: {
                color: getComputedStyle(document.documentElement).getPropertyValue('--text-secondary')
              },
              grid: {
                color: getComputedStyle(document.documentElement).getPropertyValue('--border-color-light')
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
                  const value = context.raw || 0;
                  return value === 1 ? '1 session' : `${value} sessions`;
                }
              }
            }
          },
          elements: {
            point: {
              radius: 5,
              hoverRadius: 7
            },
            line: {
              tension: 0.4,
            }
          }
        }
      });
    }
  },
  watch: {
    chartData: {
      handler() {
        if (this.chart) {
          this.chart.data = this.chartData;
          this.chart.update();
        }
      },
      deep: true
    }
  },
  beforeUnmount() {
    if (this.chart) {
      this.chart.destroy();
    }
  }
};
</script>

<style scoped>
.chart-wrapper {
  width: 100%;
  height: 100%;
}
</style>