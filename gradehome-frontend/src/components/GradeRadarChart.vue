<template>
    <div class="radar-chart-container">
      <h3 class="chart-title">Module Rating Analysis</h3>
      <div v-if="!hasData" class="no-data-message">
        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="12" cy="12" r="10"></circle>
          <line x1="12" y1="8" x2="12" y2="12"></line>
          <line x1="12" y1="16" x2="12.01" y2="16"></line>
        </svg>
        <p>No rating data available for this module yet.</p>
      </div>
      <div v-else ref="chartContainer" class="chart-area">
        <svg width="100%" height="100%" viewBox="0 0 300 300" xmlns="http://www.w3.org/2000/svg">
          <!-- Base circles -->
          <g class="radar-grid">
            <circle v-for="(circle, i) in radarCircles" :key="`circle-${i}`" 
              :cx="150" :cy="150" :r="circle.radius" 
              stroke="#e0e0e0" stroke-width="1" fill="none" 
              class="radar-grid-circle" />
            
            <!-- Axis lines -->
            <line v-for="(axis, i) in radarAxes" :key="`axis-${i}`"
              :x1="150" :y1="150" :x2="axis.x" :y2="axis.y"
              stroke="#e0e0e0" stroke-width="1" class="radar-grid-line" />
            
            <!-- Axis labels -->
            <text v-for="(label, i) in axisLabels" :key="`label-${i}`"
              :x="label.x" :y="label.y" 
              text-anchor="middle" dominant-baseline="middle" 
              font-size="12" class="radar-axis-label">
              {{ label.text }}
            </text>
          </g>
          
          <!-- Data polygon -->
          <polygon :points="dataPoints" 
            class="radar-data-polygon" />
          
          <!-- Data points -->
          <circle v-for="(point, i) in dataPointsArray" :key="`point-${i}`"
            :cx="point.x" :cy="point.y" r="4" 
            class="radar-data-point" />
        </svg>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'GradeRadarChart',
    props: {
      moduleData: {
        type: Object,
        required: true
      }
    },
    computed: {
      hasData() {
        const stats = this.moduleData.statistics || {};
        return stats.teaching_quality_avg > 0 || stats.difficulty_avg > 0;
      },
      chartData() {
        const stats = this.moduleData.statistics || {};
        
        return [
          { axis: 'Teaching', value: stats.teaching_quality_avg || 0 },
          { axis: 'Organization', value: stats.organization_avg || 0 },
          { axis: 'Content', value: stats.content_quality_avg || 0 },
          { axis: 'Engagement', value: stats.engagement_avg || 0 },
          { axis: 'Value', value: stats.value_avg || 0 },
          { axis: 'Difficulty', value: 5 - (stats.difficulty_avg || 0) } // Inverted so lower difficulty is better
        ];
      },
      radarCircles() {
        const radius = 120;
        return [1, 2, 3, 4, 5].map(i => ({
          radius: radius * (i / 5)
        }));
      },
      radarAxes() {
        const radius = 120;
        const numAxes = 6;
        
        return Array.from({ length: numAxes }, (_, i) => {
          const angle = (Math.PI * 2 * i) / numAxes - Math.PI / 2;
          return {
            x: 150 + radius * Math.cos(angle),
            y: 150 + radius * Math.sin(angle)
          };
        });
      },
      axisLabels() {
        const radius = 140;
        const numAxes = 6;
        
        return this.chartData.map((d, i) => {
          const angle = (Math.PI * 2 * i) / numAxes - Math.PI / 2;
          return {
            text: d.axis,
            x: 150 + radius * Math.cos(angle),
            y: 150 + radius * Math.sin(angle)
          };
        });
      },
      dataPointsArray() {
        const radius = 120;
        const numAxes = 6;
        
        return this.chartData.map((d, i) => {
          const angle = (Math.PI * 2 * i) / numAxes - Math.PI / 2;
          const value = Math.max(0, Math.min(5, d.value)); // Clamp between 0-5
          const distance = (value / 5) * radius;
          
          return {
            x: 150 + distance * Math.cos(angle),
            y: 150 + distance * Math.sin(angle)
          };
        });
      },
      dataPoints() {
        return this.dataPointsArray.map(p => `${p.x},${p.y}`).join(' ');
      }
    }
  }
  </script>
  
  <style scoped>
  .radar-chart-container {
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
    width: 100%;
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
  
  .radar-grid-circle {
    stroke: var(--text-secondary);
    stroke-opacity: 0.2;
  }
  
  .radar-grid-line {
    stroke: var(--text-secondary);
    stroke-opacity: 0.3;
  }
  
  .radar-axis-label {
    fill: var(--text-primary);
  }
  
  .radar-data-polygon {
    fill: var(--primary-color);
    fill-opacity: 0.2;
    stroke: var(--primary-color);
    stroke-width: 2;
  }
  
  .radar-data-point {
    fill: var(--primary-color);
  }
  
  @media (max-width: 768px) {
    .chart-area {
      height: 250px;
    }
  }
  </style>