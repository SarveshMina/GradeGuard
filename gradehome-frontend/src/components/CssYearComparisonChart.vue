<template>
    <div class="css-year-comparison-chart">
      <!-- Removed duplicate title - the parent component already has an h3 title -->
      
      <div v-if="!hasData" class="empty-state">
        <p>No year comparison data available yet. Add modules from different years to see a comparison.</p>
      </div>
      
      <div v-else class="chart-content">
        <!-- Legend -->
        <div class="chart-legend">
          <div class="legend-item">
            <div class="legend-color average-color"></div>
            <div class="legend-label">Average</div>
          </div>
          <div class="legend-item">
            <div class="legend-color highest-color"></div>
            <div class="legend-label">Highest</div>
          </div>
          <div class="legend-item">
            <div class="legend-color lowest-color"></div>
            <div class="legend-label">Lowest</div>
          </div>
        </div>
        
        <!-- CSS Bars -->
        <div class="chart-bars-container">
          <div 
            v-for="(year, index) in yearData" 
            :key="index" 
            class="year-group"
          >
            <div class="year-label">{{ year.name }}</div>
            
            <div class="bars-group">
              <!-- Average Bar -->
              <div class="bar-container">
                <div class="bar average-bar" :style="{ width: `${Math.min(year.average, 100)}%` }">
                  <span class="bar-value">{{ year.average }}%</span>
                </div>
              </div>
              
              <!-- Highest Bar -->
              <div class="bar-container">
                <div class="bar highest-bar" :style="{ width: `${Math.min(year.highest || 0, 100)}%` }">
                  <span class="bar-value">{{ year.highest || 0 }}%</span>
                </div>
              </div>
              
              <!-- Lowest Bar -->
              <div class="bar-container">
                <div class="bar lowest-bar" :style="{ width: `${Math.min(year.lowest || 0, 100)}%` }">
                  <span class="bar-value">{{ year.lowest || 0 }}%</span>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Credits and Module Count - Made more compact -->
        <div class="chart-footer">
          <div 
            v-for="(year, index) in yearData" 
            :key="`info-${index}`" 
            class="year-info"
          >
            <div class="year-name">{{ year.name }}</div>
            <div class="year-stats">
              <span>{{ year.credits || 0 }} cr</span>
              <span>•</span>
              <span>{{ year.modules || 0 }} mod</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'CssYearComparisonChart',
    
    props: {
      yearData: {
        type: Array,
        default: () => []
      }
    },
    
    computed: {
      hasData() {
        return this.yearData && this.yearData.length > 0;
      }
    },
    
    methods: {
      redrawChart() {
        console.log("CSS chart refresh requested (no action needed)");
        return true;
      }
    }
  };
  </script>
  
  <style scoped>
  .css-year-comparison-chart {
    width: 100%;
    height: 100%;
    min-height: 200px;
    max-height: 300px; /* Added max-height to prevent overflow */
    background-color: var(--bg-card, #1f2937); /* Updated for dark mode */
    border-radius: var(--border-radius, 8px);
    padding: 1rem; /* Reduced padding */
    display: flex;
    flex-direction: column;
    color: var(--text-primary, #f1f5f9); /* Updated for dark mode */
    overflow: hidden; /* Prevent overflow */
    box-sizing: border-box; /* Include padding in size calculation */
  }
  
  .chart-content {
    display: flex;
    flex-direction: column;
    height: 100%;
    overflow: hidden;
  }
  
  .empty-state {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100%;
    background-color: var(--bg-accent, #2d3748); /* Updated for dark mode */
    border-radius: var(--border-radius, 8px);
    padding: 1rem;
    text-align: center;
    color: var(--text-secondary, #cbd5e1); /* Updated for dark mode */
    border: 1px dashed var(--border-color, #4b5563); /* Updated for dark mode */
  }
  
  .chart-legend {
    display: flex;
    gap: 1rem;
    margin-bottom: 0.75rem;
    justify-content: center;
  }
  
  .legend-item {
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }
  
  .legend-color {
    width: 12px;
    height: 12px;
    border-radius: 3px;
  }
  
  .average-color {
    background-color: rgba(139, 92, 246, 0.9); /* Purple for dark mode */
  }
  
  .highest-color {
    background-color: rgba(16, 185, 129, 0.9); /* Green for dark mode */
  }
  
  .lowest-color {
    background-color: rgba(239, 68, 68, 0.9); /* Red for dark mode */
  }
  
  .legend-label {
    font-size: 0.75rem;
    color: var(--text-secondary, #cbd5e1); /* Updated for dark mode */
    font-weight: 500;
  }
  
  .chart-bars-container {
    display: flex;
    flex-direction: column;
    gap: 1.25rem;
    margin-bottom: 0.75rem;
    flex: 1;
    overflow-y: auto; /* Allow scrolling if many years */
    padding-right: 0.5rem; /* Space for scrollbar */
  }
  
  .year-group {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
  }
  
  .year-label {
    font-weight: 600;
    color: var(--text-primary, #f1f5f9); /* Updated for dark mode */
    margin-bottom: 0.25rem;
    font-size: 0.9rem;
  }
  
  .bars-group {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .bar-container {
    height: 20px; /* Smaller height */
    background-color: var(--bg-accent, #374151); /* Updated for dark mode */
    border-radius: 10px;
    overflow: hidden;
    position: relative;
    width: 100%; /* Ensure it's constrained to parent width */
  }
  
  .bar {
    height: 100%;
    border-radius: 10px;
    position: relative;
    transition: width 0.5s ease;
    display: flex;
    align-items: center;
    justify-content: flex-end;
    padding-right: 8px;
    max-width: 100%; /* Ensure bars don't overflow */
  }
  
  .average-bar {
    background: linear-gradient(to right, rgba(139, 92, 246, 0.7), rgba(139, 92, 246, 0.9)); /* Purple for dark mode */
  }
  
  .highest-bar {
    background: linear-gradient(to right, rgba(16, 185, 129, 0.7), rgba(16, 185, 129, 0.9)); /* Green for dark mode */
  }
  
  .lowest-bar {
    background: linear-gradient(to right, rgba(239, 68, 68, 0.7), rgba(239, 68, 68, 0.9)); /* Red for dark mode */
  }
  
  .bar-value {
    color: white;
    font-weight: 600;
    font-size: 0.75rem;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
    white-space: nowrap;
  }
  
  .chart-footer {
    display: flex;
    gap: 1rem;
    justify-content: center;
    padding-top: 0.5rem;
    border-top: 1px solid var(--border-color, #4b5563); /* Updated for dark mode */
    flex-wrap: wrap;
    font-size: 0.75rem;
    max-height: 40px; /* Limit height */
    overflow: hidden;
  }
  
  .year-info {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
  }
  
  .year-name {
    font-weight: 600;
    color: var(--text-primary, #f1f5f9); /* Updated for dark mode */
    margin-bottom: 0.15rem;
    font-size: 0.75rem;
  }
  
  .year-stats {
    display: flex;
    gap: 0.35rem;
    font-size: 0.7rem;
    color: var(--text-secondary, #9ca3af); /* Updated for dark mode */
  }
  
  /* Light mode adjustments */
  :global(.light-mode) .css-year-comparison-chart {
    background-color: #ffffff;
    color: #333333;
  }
  
  :global(.light-mode) .empty-state {
    background-color: #f1f3f9;
    color: #667085;
    border-color: #e2e8f0;
  }
  
  :global(.light-mode) .year-label,
  :global(.light-mode) .year-name {
    color: #333333;
  }
  
  :global(.light-mode) .bar-container {
    background-color: #f1f3f9;
  }
  
  :global(.light-mode) .chart-footer {
    border-color: #e2e8f0;
  }
  
  :global(.light-mode) .year-stats {
    color: #667085;
  }
  
  /* Responsive adjustments */
  @media (max-width: 768px) {
    .css-year-comparison-chart {
      padding: 0.75rem;
      min-height: 180px;
    }
    
    .chart-legend {
      flex-wrap: wrap;
      justify-content: flex-start;
    }
    
    .bar-container {
      height: 18px;
    }
    
    .bar-value {
      font-size: 0.7rem;
    }
  }
  </style>