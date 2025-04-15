<template>
  <div class="chart-wrapper">
    <canvas ref="chartCanvas"></canvas>
  </div>
</template>

<script>
import { Chart, registerables } from 'chart.js';
Chart.register(...registerables);

export default {
  name: 'ProductivityPatternsChart',
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
        type: 'bar',
        data: this.chartData,
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            y: {
              beginAtZero: true,
              max: 5,
              ticks: {
                stepSize: 1,
                color: getComputedStyle(document.documentElement).getPropertyValue('--text-secondary')
              },
              grid: {
                color: getComputedStyle(document.documentElement).getPropertyValue('--border-color-light')
              },
              title: {
                display: true,
                text: 'Average Productivity (1-5)',
                color: getComputedStyle(document.documentElement).getPropertyValue('--text-secondary')
              }
            },
            x: {
              ticks: {
                color: getComputedStyle(document.documentElement).getPropertyValue('--text-secondary')
              },
              grid: {
                display: false
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
                  return `Productivity: ${value.toFixed(1)}/5`;
                }
              }
            }
          },
          borderRadius: 4,
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