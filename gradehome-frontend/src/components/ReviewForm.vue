<template>
  <div class="review-form">
    <h3 class="form-title">Add Your Review</h3>
    
    <div class="rating-section">
      <div class="rating-group">
        <label>Difficulty Level</label>
        <div class="star-rating">
          <button 
            v-for="star in 5" 
            :key="`difficulty-${star}`"
            type="button"
            class="star-btn"
            :class="{ 'active': formData.difficulty >= star }"
            @click="setRating('difficulty', star)"
          >
            ★
          </button>
          <span class="rating-value">{{ formData.difficulty || '-' }}</span>
        </div>
        <div v-if="errors.difficulty" class="error-message">{{ errors.difficulty }}</div>
      </div>
      
      <div class="rating-group">
        <label>Teaching Quality</label>
        <div class="star-rating">
          <button 
            v-for="star in 5" 
            :key="`teaching-${star}`"
            type="button"
            class="star-btn"
            :class="{ 'active': formData.teaching_quality >= star }"
            @click="setRating('teaching_quality', star)"
          >
            ★
          </button>
          <span class="rating-value">{{ formData.teaching_quality || '-' }}</span>
        </div>
        <div v-if="errors.teaching_quality" class="error-message">{{ errors.teaching_quality }}</div>
      </div>
      
      <div class="rating-group">
        <label>Would you recommend this module?</label>
        <div class="toggle-buttons">
          <button 
            type="button"
            class="toggle-btn"
            :class="{ 'active': formData.recommended === true }"
            @click="formData.recommended = true"
          >
            Yes
          </button>
          <button 
            type="button"
            class="toggle-btn"
            :class="{ 'active': formData.recommended === false }"
            @click="formData.recommended = false"
          >
            No
          </button>
        </div>
        <div v-if="errors.recommended" class="error-message">{{ errors.recommended }}</div>
      </div>
    </div>
    
    <div class="comment-section">
      <label for="review-comment">Your comments (optional)</label>
      <textarea 
        id="review-comment"
        v-model="formData.comment"
        placeholder="Share your experience with this module..."
        rows="4"
        :maxlength="maxCommentLength"
      ></textarea>
      <div class="char-count" :class="{ 'limit-warning': isApproachingLimit }">
        {{ formData.comment.length }}/{{ maxCommentLength }}
      </div>
      <div v-if="errors.comment" class="error-message">{{ errors.comment }}</div>
    </div>
    
    <div class="form-actions">
      <button type="button" class="cancel-btn" @click="cancelForm">Cancel</button>
      <button 
        type="button" 
        class="submit-btn" 
        :disabled="!isFormValid || submitting"
        @click="submitReview"
      >
        <div v-if="submitting" class="spinner"></div>
        <span v-else>Submit Review</span>
      </button>
    </div>
  </div>
</template>

<script>
import { gradeRadarService } from '../services/gradeRadarService';

export default {
  name: 'ReviewForm',
  props: {
    moduleId: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      formData: {
        difficulty: 0,
        teaching_quality: 0,
        recommended: null,
        comment: ''
      },
      submitting: false,
      errors: {},
      maxCommentLength: 1000
    }
  },
  computed: {
    isFormValid() {
      return (
        this.formData.difficulty > 0 &&
        this.formData.teaching_quality > 0 &&
        this.formData.recommended !== null
      );
    },
    isApproachingLimit() {
      return this.formData.comment.length > this.maxCommentLength * 0.9;
    }
  },
  methods: {
    setRating(field, value) {
      // Toggle if clicking the same star
      if (this.formData[field] === value) {
        this.formData[field] = 0;
      } else {
        this.formData[field] = value;
      }
      
      // Clear any error for this field
      if (this.errors[field]) {
        this.$delete(this.errors, field);
      }
    },
    
    cancelForm() {
      this.$emit('form-canceled');
    },
    
    validateForm() {
      let isValid = true;
      this.errors = {};
      
      if (!this.formData.difficulty) {
        this.errors.difficulty = 'Please rate the module difficulty';
        isValid = false;
      }
      
      if (!this.formData.teaching_quality) {
        this.errors.teaching_quality = 'Please rate the teaching quality';
        isValid = false;
      }
      
      if (this.formData.recommended === null) {
        this.errors.recommended = 'Please indicate if you would recommend this module';
        isValid = false;
      }
      
      if (this.formData.comment.length > this.maxCommentLength) {
        this.errors.comment = `Comment must not exceed ${this.maxCommentLength} characters`;
        isValid = false;
      }
      
      return isValid;
    },
    
    async submitReview() {
      if (this.submitting) return;
      
      if (!this.validateForm()) {
        return;
      }
      
      this.submitting = true;
      
      try {
        // Prepare review data
        const reviewData = {
          module_id: this.moduleId,
          difficulty: this.formData.difficulty,
          teaching_quality: this.formData.teaching_quality,
          recommended: this.formData.recommended,
          comment: this.formData.comment.trim()
        };
        
        // Submit to API
        const response = await gradeRadarService.submitReview(reviewData);
        
        // Emit success event with the new review data
        this.$emit('review-submitted', response.data);
        
        // Reset form
        this.resetForm();
      } catch (error) {
        console.error('Error submitting review:', error);
        
        // Handle validation errors if returned from the API
        if (error.response && error.response.data && error.response.data.errors) {
          this.errors = error.response.data.errors;
        } else {
          // Generic error
          this.errors = {
            general: 'Failed to submit review. Please try again later.'
          };
        }
      } finally {
        this.submitting = false;
      }
    },
    
    resetForm() {
      this.formData = {
        difficulty: 0,
        teaching_quality: 0,
        recommended: null,
        comment: ''
      };
      this.errors = {};
    }
  }
}
</script>

<style scoped>
.review-form {
  background-color: var(--bg-color, white);
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
}

.form-title {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  color: var(--text-color, #333);
}

.rating-section {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.rating-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.rating-group label {
  font-size: 0.95rem;
  font-weight: 500;
  color: var(--text-color, #333);
}

.star-rating {
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.star-btn {
  background: transparent;
  border: none;
  color: #e0e0e0;
  font-size: 1.75rem;
  cursor: pointer;
  transition: color 0.2s ease;
  padding: 0;
  line-height: 1;
}

.star-btn:hover {
  color: var(--primary-light, #9061ff);
}

.star-btn.active {
  color: var(--primary-color, #7b49ff);
}

.rating-value {
  margin-left: 0.5rem;
  font-weight: 600;
  color: var(--text-color, #333);
  min-width: 1.5rem;
}

.toggle-buttons {
  display: flex;
  gap: 0.5rem;
}

.toggle-btn {
  padding: 0.5rem 1rem;
  border: 1px solid #e0e0e0;
  background-color: white;
  border-radius: 8px;
  font-size: 0.95rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  flex: 1;
  max-width: 120px;
}

.toggle-btn:hover {
  border-color: var(--primary-color, #7b49ff);
}

.toggle-btn.active {
  background-color: var(--primary-color, #7b49ff);
  border-color: var(--primary-color, #7b49ff);
  color: white;
}

.comment-section {
  margin-bottom: 1.5rem;
  position: relative;
}

.comment-section label {
  display: block;
  font-size: 0.95rem;
  font-weight: 500;
  margin-bottom: 0.5rem;
  color: var(--text-color, #333);
}

textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  resize: vertical;
  font-family: inherit;
  font-size: 0.95rem;
  background-color: var(--bg-color, white);
  color: var(--text-color, #333);
  min-height: 120px;
}

textarea:focus {
  outline: none;
  border-color: var(--primary-color, #7b49ff);
  box-shadow: 0 0 0 3px rgba(123, 73, 255, 0.2);
}

.char-count {
  position: absolute;
  bottom: 0.5rem;
  right: 0.75rem;
  font-size: 0.75rem;
  color: var(--text-secondary, #666);
  pointer-events: none;
}

.limit-warning {
  color: #ef4444;
}

.error-message {
  color: #ef4444;
  font-size: 0.875rem;
  margin-top: 0.25rem;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
}

.cancel-btn,
.submit-btn {
  padding: 0.625rem 1.25rem;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.cancel-btn {
  background-color: transparent;
  color: var(--text-secondary, #666);
  border: 1px solid #e0e0e0;
}

.cancel-btn:hover {
  border-color: var(--text-color, #333);
  color: var(--text-color, #333);
}

.submit-btn {
  background-color: var(--primary-color, #7b49ff);
  color: white;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 120px;
}

.submit-btn:hover:not(:disabled) {
  background-color: var(--primary-dark, #6234e0);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.submit-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

@media (max-width: 768px) {
  .rating-section {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .form-actions {
    flex-direction: column-reverse;
  }
  
  .submit-btn,
  .cancel-btn {
    width: 100%;
    text-align: center;
  }
}
</style>