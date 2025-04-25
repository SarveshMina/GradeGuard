<template>
    <div class="review-item">
      <div class="review-header">
        <div class="review-user-info">
          <div class="user-avatar">
            {{ getUserInitial() }}
          </div>
          <div class="user-details">
            <div class="username">{{ review.user_name || 'Anonymous User' }}</div>
            <div class="review-date">{{ formatDate(review.created_at) }}</div>
          </div>
        </div>
        <div class="review-actions" v-if="isAuthor">
          <button class="delete-btn" @click="$emit('delete-review', review.id)">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="3 6 5 6 21 6"></polyline>
              <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
              <line x1="10" y1="11" x2="10" y2="17"></line>
              <line x1="14" y1="11" x2="14" y2="17"></line>
            </svg>
            <span>Delete</span>
          </button>
        </div>
      </div>
      
      <div class="review-ratings">
        <div class="rating-item">
          <div class="rating-label">Difficulty</div>
          <div class="rating-value">
            <div class="rating-stars">
              <div class="stars-background">★★★★★</div>
              <div class="stars-filled" :style="{ width: calculateStarWidth(review.difficulty) }">★★★★★</div>
            </div>
            <span>{{ review.difficulty }}</span>
          </div>
        </div>
        <div class="rating-item">
          <div class="rating-label">Teaching Quality</div>
          <div class="rating-value">
            <div class="rating-stars">
              <div class="stars-background">★★★★★</div>
              <div class="stars-filled" :style="{ width: calculateStarWidth(review.teaching_quality) }">★★★★★</div>
            </div>
            <span>{{ review.teaching_quality }}</span>
          </div>
        </div>
        <div class="rating-item">
          <div class="rating-label">Recommended</div>
          <div class="rating-value">
            <div class="recommended-indicator" :class="{ 'recommended-yes': review.recommended, 'recommended-no': !review.recommended }">
              {{ review.recommended ? 'Yes' : 'No' }}
            </div>
          </div>
        </div>
      </div>
      
      <div v-if="review.comment && review.comment.trim()" class="review-comment">
        <p>{{ review.comment }}</p>
      </div>
      
      <div class="review-footer">
        <div class="helpful-section">
          <button 
            class="helpful-btn" 
            :class="{ 'marked-helpful': review.marked_helpful }"
            @click="toggleHelpful"
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M14 9V5a3 3 0 0 0-3-3l-4 9v11h11.28a2 2 0 0 0 2-1.7l1.38-9a2 2 0 0 0-2-2.3H14z"></path>
              <path d="M7 22H4a2 2 0 0 1-2-2v-7a2 2 0 0 1 2-2h3"></path>
            </svg>
            <span>Helpful {{ review.helpful_count ? `(${review.helpful_count})` : '' }}</span>
          </button>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'ReviewItem',
    props: {
      review: {
        type: Object,
        required: true
      },
      isAuthor: {
        type: Boolean,
        default: false
      }
    },
    methods: {
      getUserInitial() {
        if (this.review.user_name) {
          return this.review.user_name.charAt(0).toUpperCase();
        }
        return 'A';
      },
      
      formatDate(dateString) {
        if (!dateString) return 'Unknown date';
        
        try {
          const options = { year: 'numeric', month: 'short', day: 'numeric' };
          return new Date(dateString).toLocaleDateString(undefined, options);
        } catch (error) {
          return dateString;
        }
      },
      
      calculateStarWidth(rating) {
        if (!rating) return '0%';
        return `${(rating / 5) * 100}%`;
      },
      
      toggleHelpful() {
        this.$emit('toggle-helpful', {
          reviewId: this.review.id,
          currentStatus: this.review.marked_helpful
        });
      }
    }
  }
  </script>
  
  <style scoped>
  .review-item {
    background-color: white;
    border-radius: var(--radius-lg);
    padding: 1.5rem;
    box-shadow: var(--shadow-md);
    transition: all var(--transition-medium) ease;
    margin-bottom: 1rem;
  }
  
  body.dark-mode .review-item {
    background-color: #1e1e30;
  }
  
  .review-item:hover {
    box-shadow: var(--shadow-lg);
    transform: translateY(-2px);
  }
  
  .review-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 1.5rem;
  }
  
  .review-user-info {
    display: flex;
    align-items: center;
    gap: 1rem;
  }
  
  .user-avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background: linear-gradient(135deg, var(--primary-color), var(--accent-pink));
    color: white;
    font-size: 1.25rem;
    font-weight: 600;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .user-details {
    display: flex;
    flex-direction: column;
  }
  
  .username {
    font-weight: 600;
    color: var(--text-primary);
  }
  
  .review-date {
    font-size: 0.875rem;
    color: var(--text-secondary);
  }
  
  .review-actions {
    display: flex;
    gap: 0.5rem;
  }
  
  .delete-btn {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.375rem 0.75rem;
    background-color: rgba(239, 68, 68, 0.1);
    color: #ef4444;
    border: none;
    border-radius: var(--radius-md);
    cursor: pointer;
    font-size: 0.875rem;
    font-weight: 500;
    transition: all var(--transition-medium) ease;
  }
  
  .delete-btn:hover {
    background-color: rgba(239, 68, 68, 0.2);
  }
  
  .review-ratings {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
    gap: 1rem;
    margin-bottom: 1.5rem;
  }
  
  .rating-item {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
  }
  
  .rating-label {
    font-size: 0.875rem;
    color: var(--text-secondary);
  }
  
  .rating-value {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-weight: 600;
    color: var(--text-primary);
  }
  
  .rating-stars {
    position: relative;
    font-size: 1.25rem;
    line-height: 1;
    display: inline-block;
  }
  
  .stars-background {
    color: #e0e0e0;
  }
  
  body.dark-mode .stars-background {
    color: #3a3a52;
  }
  
  .stars-filled {
    position: absolute;
    top: 0;
    left: 0;
    color: var(--primary-color);
    overflow: hidden;
    white-space: nowrap;
  }
  
  .recommended-indicator {
    padding: 0.25rem 0.5rem;
    border-radius: var(--radius-md);
    font-size: 0.875rem;
  }
  
  .recommended-yes {
    background-color: rgba(16, 185, 129, 0.1);
    color: #10b981;
  }
  
  .recommended-no {
    background-color: rgba(239, 68, 68, 0.1);
    color: #ef4444;
  }
  
  .review-comment {
    padding: 1.25rem;
    background-color: rgba(123, 73, 255, 0.05);
    border-radius: var(--radius-md);
    margin-bottom: 1.5rem;
    color: var(--text-primary);
    line-height: 1.6;
  }
  
  body.dark-mode .review-comment {
    background-color: rgba(123, 73, 255, 0.1);
  }
  
  .review-footer {
    display: flex;
    justify-content: flex-end;
  }
  
  .helpful-btn {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 0.75rem;
    background-color: rgba(123, 73, 255, 0.1);
    color: var(--primary-color);
    border: none;
    border-radius: var(--radius-md);
    cursor: pointer;
    font-size: 0.875rem;
    font-weight: 500;
    transition: all var(--transition-medium) ease;
  }
  
  .helpful-btn:hover {
    background-color: rgba(123, 73, 255, 0.2);
  }
  
  .helpful-btn.marked-helpful {
    background-color: var(--primary-color);
    color: white;
  }
  
  @media (max-width: 768px) {
    .review-ratings {
      grid-template-columns: 1fr 1fr;
    }
    
    .review-comment {
      padding: 1rem;
    }
  }
  
  @media (max-width: 576px) {
    .review-header {
      flex-direction: column;
      gap: 1rem;
    }
    
    .review-actions {
      width: 100%;
      justify-content: flex-end;
    }
    
    .review-ratings {
      grid-template-columns: 1fr;
    }
  }
  </style>