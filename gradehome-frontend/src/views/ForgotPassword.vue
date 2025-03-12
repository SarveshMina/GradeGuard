<template>
  <div class="forgot-password-container">
    <div class="card">
      <h1>Reset Your Password</h1>

      <div v-if="!emailSent">
        <p>Enter your email address and we'll send you a link to reset your password.</p>

        <form @submit.prevent="submitRequest">
          <div class="form-group">
            <label for="email">Email Address</label>
            <input
                type="email"
                id="email"
                v-model="email"
                required
                placeholder="Enter your email address"
            />
            <p v-if="error" class="error-message">{{ error }}</p>
          </div>

          <div class="button-group">
            <button type="submit" class="primary-button" :disabled="isSubmitting">
              <span v-if="isSubmitting">
                <i class="fa fa-spinner fa-spin"></i> Sending...
              </span>
              <span v-else>Send Reset Link</span>
            </button>
            <router-link to="/login" class="secondary-button">Back to Login</router-link>
          </div>
        </form>
      </div>

      <div v-else class="success-message">
        <i class="fa fa-check-circle"></i>
        <h2>Email Sent</h2>
        <p>A password reset link has been sent to <strong>{{ email }}</strong>.</p>
        <p>Please check your email inbox and follow the instructions to reset your password.</p>
        <p class="note">If you don't see the email, check your spam folder.</p>
        <router-link to="/login" class="primary-button">Return to Login</router-link>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { API_URL } from '@/config.js';

export default {
  name: 'ForgotPassword',
  data() {
    return {
      email: '',
      isSubmitting: false,
      emailSent: false,
      error: null
    }
  },
  methods: {
    async submitRequest() {
      this.isSubmitting = true;
      this.error = null;

      try {
        await axios.post(`${API_URL}/password/forgot`, {
          email: this.email
        });

        this.emailSent = true;
      } catch (error) {
        console.error('Error:', error);
        this.error = error.response?.data?.error || 'An error occurred. Please try again.';
      } finally {
        this.isSubmitting = false;
      }
    }
  }
}
</script>

<style scoped>
.forgot-password-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  padding: 2rem;
  background-color: #f5f7fa;
}

.card {
  background: white;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  padding: 2rem;
  width: 100%;
  max-width: 500px;
}

h1 {
  margin-top: 0;
  color: #333;
  font-size: 1.8rem;
  text-align: center;
  margin-bottom: 1.5rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.button-group {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  margin-top: 1.5rem;
}

.primary-button, .secondary-button {
  padding: 0.75rem 1.5rem;
  border-radius: 4px;
  font-weight: 500;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.primary-button {
  background-color: #4f46e5;
  color: white;
  border: none;
  flex: 1;
}

.primary-button:hover {
  background-color: #4338ca;
}

.secondary-button {
  background-color: transparent;
  color: #4f46e5;
  border: 1px solid #4f46e5;
  text-decoration: none;
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.secondary-button:hover {
  background-color: rgba(79, 70, 229, 0.1);
}

.error-message {
  color: #e53e3e;
  margin-top: 0.5rem;
  font-size: 0.875rem;
}

.success-message {
  text-align: center;
  padding: 1rem 0;
}

.success-message i {
  font-size: 3rem;
  color: #48bb78;
  margin-bottom: 1rem;
}

.success-message h2 {
  color: #48bb78;
  margin-bottom: 1rem;
}

.note {
  font-size: 0.875rem;
  font-style: italic;
  color: #666;
  margin-bottom: 1.5rem;
}

button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}
</style>