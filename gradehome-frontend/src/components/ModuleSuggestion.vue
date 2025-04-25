<template>
    <div class="module-suggestion-container">
      <div class="input-container">
        <input
          type="text"
          v-model="query"
          @input="handleInput"
          @focus="isFocused = true"
          @blur="handleBlur"
          :placeholder="placeholder"
          class="suggestion-input"
          ref="inputElement"
        />
        <div class="input-icons">
          <svg 
            v-if="query && !loading" 
            class="clear-icon" 
            @click="clearInput" 
            width="18" 
            height="18" 
            viewBox="0 0 24 24" 
            fill="none" 
            stroke="currentColor" 
            stroke-width="2" 
            stroke-linecap="round" 
            stroke-linejoin="round"
          >
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="15" y1="9" x2="9" y2="15"></line>
            <line x1="9" y1="9" x2="15" y2="15"></line>
          </svg>
          <div v-if="loading" class="spinner"></div>
          <svg 
            v-if="!loading && !query" 
            class="search-icon" 
            width="18" 
            height="18" 
            viewBox="0 0 24 24" 
            fill="none" 
            stroke="currentColor" 
            stroke-width="2" 
            stroke-linecap="round" 
            stroke-linejoin="round"
          >
            <circle cx="11" cy="11" r="8"></circle>
            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
          </svg>
        </div>
      </div>
      
      <!-- Dropdown suggestions -->
      <div v-if="showSuggestions && suggestions.length > 0" class="suggestions-dropdown">
        <!-- User's degree modules -->
        <div v-if="userDegreeModules.length > 0" class="suggestion-group">
          <div class="group-header">Your Degree</div>
          <div 
            v-for="module in userDegreeModules" 
            :key="module.id" 
            class="suggestion-item"
            @mousedown="selectSuggestion(module)"
          >
            <div class="suggestion-content">
              <div class="suggestion-name">{{ module.name }}</div>
              <div class="suggestion-meta">
                <span class="suggestion-code">{{ module.code }}</span>
                <span class="suggestion-year">Year {{ module.year }}</span>
                <span class="suggestion-semester">Semester {{ module.semester }}</span>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Other degree modules -->
        <div v-if="otherDegreeModules.length > 0" class="suggestion-group">
          <div class="group-header">Other Degrees</div>
          <div 
            v-for="module in otherDegreeModules" 
            :key="module.id" 
            class="suggestion-item"
            @mousedown="selectSuggestion(module)"
          >
            <div class="suggestion-content">
              <div class="suggestion-name">{{ module.name }}</div>
              <div class="suggestion-meta">
                <span class="suggestion-code">{{ module.code }}</span>
                <span class="suggestion-degree">{{ module.degree }}</span>
                <span class="suggestion-year">Year {{ module.year }}</span>
                <span class="suggestion-semester">Semester {{ module.semester }}</span>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Duplicate warning if needed -->
        <div v-if="isDuplicate" class="duplicate-warning">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="12" y1="8" x2="12" y2="12"></line>
            <line x1="12" y1="16" x2="12.01" y2="16"></line>
          </svg>
          <span>This module already exists in your selections</span>
        </div>
      </div>
      
      <!-- No results message -->
      <div v-if="showSuggestions && query && !loading && suggestions.length === 0" class="no-results">
        <p>No modules found matching "{{ query }}"</p>
      </div>
    </div>
  </template>
  
  <script>
  import { debounce } from 'lodash'
  import gradeRadarService from '@/services/gradeRadarService'
  
  export default {
    name: 'ModuleSuggestion',
    props: {
      placeholder: {
        type: String,
        default: 'Search for a module...'
      },
      university: {
        type: String,
        default: ''
      },
      existingModules: {
        type: Array,
        default: () => []
      },
      userDegree: {
        type: String,
        default: ''
      }
    },
    data() {
      return {
        query: '',
        suggestions: [],
        loading: false,
        isFocused: false,
        isDuplicate: false,
        isAuthenticated: false
      }
    },
    computed: {
      // Show suggestions if input is focused and not empty, or if there are suggestions
      showSuggestions() {
        return this.isFocused && (this.suggestions.length > 0 || this.query.length > 0)
      },
      
      // Filter modules from user's degree
      userDegreeModules() {
        if (!this.userDegree) return []
        return this.suggestions.filter(module => module.degree === this.userDegree)
      },
      
      // Filter modules from other degrees
      otherDegreeModules() {
        if (!this.userDegree) return this.suggestions
        return this.suggestions.filter(module => module.degree !== this.userDegree)
      }
    },
    created() {
      // Create debounced search function
      this.debouncedSearch = debounce(this.fetchSuggestions, 300)
      
      // Check authentication status
      this.isAuthenticated = localStorage.getItem('token') !== null
    },
    methods: {
      // Handle input changes
      handleInput() {
        if (this.query.length >= 2) {
          this.loading = true
          this.isDuplicate = false
          this.debouncedSearch()
        } else {
          this.suggestions = []
          this.loading = false
        }
      },
      
      // Handle blur event
      handleBlur() {
        // Delay hiding suggestions to allow for selection clicks
        setTimeout(() => {
          this.isFocused = false
        }, 200)
      },
      
      // Clear input
      clearInput() {
        this.query = ''
        this.suggestions = []
        this.$refs.inputElement.focus()
      },
      
      // Fetch module suggestions
      async fetchSuggestions() {
        if (this.query.length < 2) return
        
        try {
          let response
          
          // Use appropriate API endpoint based on auth status
          if (this.isAuthenticated) {
            response = await gradeRadarService.getModuleSuggestions(this.query)
          } else if (this.university) {
            response = await gradeRadarService.getAnonymousModuleSuggestions(this.university, this.query)
          } else {
            this.suggestions = []
            this.loading = false
            return
          }
          
          this.suggestions = response.data || []
          
          // Check for duplicates with existing modules
          if (this.existingModules && this.existingModules.length > 0) {
            this.checkForDuplicates()
          }
        } catch (error) {
          console.error('Error fetching module suggestions:', error)
          this.suggestions = []
        } finally {
          this.loading = false
        }
      },
      
      // Check if any suggestions are duplicates of existing modules
      checkForDuplicates() {
        const existingModuleIds = this.existingModules.map(m => m.id)
        this.suggestions.forEach(suggestion => {
          suggestion.isDuplicate = existingModuleIds.includes(suggestion.id)
        })
        
        // Check if the current query exactly matches a module name
        this.isDuplicate = this.existingModules.some(
          module => module.name.toLowerCase() === this.query.toLowerCase()
        )
      },
      
      // Select a suggestion
      selectSuggestion(module) {
        if (module.isDuplicate) {
          // Emit a duplicate event if needed
          this.$emit('duplicate', module)
          return
        }
        
        // Update input value
        this.query = module.name
        
        // Emit selected module
        this.$emit('selected', module)
        
        // Clear suggestions
        this.suggestions = []
      }
    }
  }
  </script>
  
  <style scoped>
  /* Module Suggestion Container */
  .module-suggestion-container {
    position: relative;
    width: 100%;
  }
  
  /* Input Container */
  .input-container {
    position: relative;
    width: 100%;
  }
  
  .suggestion-input {
    width: 100%;
    padding: 0.75rem 2.5rem 0.75rem 1rem;
    font-size: 0.95rem;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    transition: all 0.3s ease;
    background-color: white;
    color: #333;
  }
  
  :deep(body.dark-mode) .suggestion-input {
    background-color: #1e1e30;
    border-color: #3a3a52;
    color: #f0f0f0;
  }
  
  .suggestion-input:focus {
    outline: none;
    border-color: #7b49ff;
    box-shadow: 0 0 0 3px rgba(123, 73, 255, 0.2);
  }
  
  .input-icons {
    position: absolute;
    top: 50%;
    right: 1rem;
    transform: translateY(-50%);
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }
  
  .clear-icon,
  .search-icon {
    color: #555;
    cursor: pointer;
    opacity: 0.6;
    transition: opacity 0.2s ease;
  }
  
  :deep(body.dark-mode) .clear-icon,
  :deep(body.dark-mode) .search-icon {
    color: #aaa;
  }
  
  .clear-icon:hover,
  .search-icon:hover {
    opacity: 1;
  }
  
  /* Loading Spinner */
  .spinner {
    width: 16px;
    height: 16px;
    border: 2px solid rgba(123, 73, 255, 0.3);
    border-radius: 50%;
    border-top-color: #7b49ff;
    animation: spin 0.8s linear infinite;
  }
  
  @keyframes spin {
    to {
      transform: rotate(360deg);
    }
  }
  
  /* Suggestions Dropdown */
  .suggestions-dropdown {
    position: absolute;
    top: calc(100% + 4px);
    left: 0;
    width: 100%;
    max-height: 320px;
    overflow-y: auto;
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    z-index: 20;
    border: 1px solid #e0e0e0;
  }
  
  :deep(body.dark-mode) .suggestions-dropdown {
    background-color: #1e1e30;
    border-color: #3a3a52;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  }
  
  .suggestion-group {
    padding-bottom: 0.5rem;
  }
  
  .suggestion-group:not(:last-child) {
    border-bottom: 1px solid #eee;
  }
  
  :deep(body.dark-mode) .suggestion-group:not(:last-child) {
    border-bottom-color: #3a3a52;
  }
  
  .group-header {
    padding: 0.625rem 1rem;
    font-size: 0.75rem;
    font-weight: 600;
    color: #7b49ff;
    background-color: rgba(123, 73, 255, 0.05);
  }
  
  .suggestion-item {
    padding: 0.75rem 1rem;
    cursor: pointer;
    transition: background-color 0.2s ease;
  }
  
  .suggestion-item:hover {
    background-color: rgba(123, 73, 255, 0.1);
  }
  
  .suggestion-content {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
  }
  
  .suggestion-name {
    font-weight: 500;
    color: #333;
  }
  
  :deep(body.dark-mode) .suggestion-name {
    color: #f0f0f0;
  }
  
  .suggestion-meta {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 0.5rem;
    font-size: 0.75rem;
    color: #666;
  }
  
  :deep(body.dark-mode) .suggestion-meta {
    color: #aaa;
  }
  
  .suggestion-code {
    padding: 0.125rem 0.375rem;
    background-color: rgba(123, 73, 255, 0.1);
    border-radius: 4px;
    color: #7b49ff;
  }
  
  :deep(body.dark-mode) .suggestion-code {
    background-color: rgba(123, 73, 255, 0.2);
  }
  
  .suggestion-degree,
  .suggestion-year,
  .suggestion-semester {
    opacity: 0.8;
  }
  
  /* Duplicate Warning */
  .duplicate-warning {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.75rem 1rem;
    background-color: rgba(239, 68, 68, 0.1);
    color: #ef4444;
    font-size: 0.875rem;
  }
  
  /* No Results */
  .no-results {
    position: absolute;
    top: calc(100% + 4px);
    left: 0;
    width: 100%;
    padding: 1rem;
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    z-index: 20;
    text-align: center;
    color: #666;
    font-size: 0.875rem;
    border: 1px solid #e0e0e0;
  }
  
  :deep(body.dark-mode) .no-results {
    background-color: #1e1e30;
    border-color: #3a3a52;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    color: #aaa;
  }
</style>