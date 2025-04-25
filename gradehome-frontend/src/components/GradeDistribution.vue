<template>
  <div class="grade-distribution-container">
    <h3 class="chart-title">Grade Distribution</h3>
    <div v-if="!hasData" class="no-data-message">
      <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round">
        <path d="M21.21 15.89A10 10 0 1 1 8 2.83"></path>
        <path d="M22 12A10 10 0 0 0 12 2v10z"></path>
      </svg>
      <p>No grade distribution data available for this module yet.</p>
    </div>
    <div v-else class="chart-area">
      <div class="bar-chart">
        <div v-for="(item, index) in formattedGradeData" :key="index" class="bar-container">
          <div class="bar-label">{{ item.grade }}</div>
          <div class="bar-wrapper">
            <div class="bar" :style="{ height: `${calculateBarHeight(item.count)}%` }">
              <div v-if="item.count > 0" class="bar-value">{{ item.count }}</div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="chart-legend">
        <div class="legend-item">
          <div class="legend-color"></div>
          <div class="legend-label">Number of students achieving each grade</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'GradeDistribution',
  props: {
    gradeData: {
      type: Array,
      default: () => []
    }
  },
  computed: {
    hasData() {
      return this.gradeData && this.gradeData.length > 0 && 
        this.gradeData.some(item => item.count > 0);
    },
    formattedGradeData() {
      // Standard grades to ensure consistent display
      const standardGrades = ['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D', 'F'];
      
      // If no data, use empty data set
      if (!this.hasData) {
        return standardGrades.map(grade => ({ grade, count: 0 }));
      }
      
      // Create a map with data from props
      const gradeMap = {};
      this.gradeData.forEach(item => {
        gradeMap[item.grade] = item.count || 0;
      });
      
      // Convert map to array with standard order
      return standardGrades.map(grade => ({
        grade,
        count: gradeMap[grade] || 0
      }));
    },
    maxCount() {
      if (!this.hasData) return 10;
      return Math.max(...this.formattedGradeData.map(item => item.count), 1);
    }
  },
  methods: {
    calculateBarHeight(count) {
      if (this.maxCount === 0) return 0;
      return (count / this.maxCount) * 90; // Max height 90% to leave room for labels
    }
  }
}
</script>

<style scoped>
.grade-distribution-container {
  width: 100%;
  height: 100%;
  position: relative;
}

.chart-title {
  font-size: 1.25rem;
  font-weight: 600;
  text-align: center;
  margin-bottom: 1rem;
  color: var(--text-primary);
}

.chart-area {
  display: flex;
  flex-direction: column;
  height: 300px;
}

.no-data-message {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 300px;
  color: var(--text-secondary);
  text-align: center;
  padding: 1rem;
}

.no-data-message svg {
  opacity: 0.5;
  margin-bottom: 1rem;
}

.bar-chart {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  height: 250px;
  margin-bottom: 0.5rem;
  border-bottom: 1px solid var(--text-secondary);
  border-left: 1px solid var(--text-secondary);
  position: relative;
}

.bar-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex: 1;
  max-width: 50px;
  min-width: 30px;
}

.bar-label {
  margin-top: 0.5rem;
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--text-primary);
}

.bar-wrapper {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: flex-end;
}

.bar {
  width: 70%;
  background-color: var(--primary-color);
  border-radius: 4px 4px 0 0;
  position: relative;
  transition: height 0.3s ease;
}

.bar-value {
  position: absolute;
  top: -20px;
  left: 50%;
  transform: translateX(-50%);
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--text-primary);
}

.chart-legend {
  display: flex;
  justify-content: center;
  margin-top: 1rem;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.legend-color {
  width: 12px;
  height: 12px;
  background-color: var(--primary-color);
  border-radius: 2px;
}

.legend-label {
  font-size: 0.875rem;
  color: var(--text-secondary);
}

/* Grid lines */
.bar-chart::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  background-size: 100% 25%;
  background-image: linear-gradient(to bottom, 
    transparent 24%, 
    rgba(var(--text-secondary-rgb, 85, 85, 85), 0.1) 24%, 
    rgba(var(--text-secondary-rgb, 85, 85, 85), 0.1) 25%, 
    transparent 25%
  );
  pointer-events: none;
}

@media (max-width: 768px) {
  .chart-area {
    height: 250px;
  }
  
  .bar-chart {
    height: 200px;
  }
  
  .bar-label {
    font-size: 0.75rem;
  }
}

@media (max-width: 576px) {
  .bar-container {
    min-width: 20px;
  }
  
  .bar {
    width: 80%;
  }
}
</style>