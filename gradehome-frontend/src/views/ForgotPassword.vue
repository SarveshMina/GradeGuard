<template>
  <div class="auth-container">
    <NavBar mode="forgot" />
    <main class="auth-main">
      <h1>Password Reset</h1>
      <form @submit.prevent="handleReset">
        <div class="form-group">
          <label for="email">Email:</label>
          <input
              type="email"
              v-model="email"
              id="email"
              placeholder="Enter your email"
              required
          />
        </div>
        <button type="submit" class="auth-button">Get OTP</button>
      </form>
    </main>
    <Footer />
  </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue'
import Footer from '@/components/Footer.vue'

export default {
  name: 'ForgotPassword',
  components: { NavBar, Footer },
  data() {
    return {
      email: ''
    }
  },
  methods: {
    handleReset() {
      alert(`OTP sent to ${this.email}`);
    }
  }
}
</script>

<style scoped>
.auth-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background: linear-gradient(135deg, #fcfcff 0%, #b191fc 100%);
  color: var(--text-color);
  font-family: "Montserrat", sans-serif;
}

.auth-main {
  flex: 1;
  padding: 1rem;
  max-width: 500px;
  margin: 1rem auto;
  background: var(--form-bg);
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.auth-main h1 {
  margin-bottom: 0.5rem;
  text-align: center;
}

.form-group {
  margin-bottom: 0.75rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
}

.form-group input {
  width: 100%;
  padding: 0.65rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 0.9rem;
}

.auth-button {
  width: 100%;
  padding: 0.75rem;
  border: none;
  background: #512da8;
  color: #fff;
  border-radius: 24px;
  cursor: pointer;
  font-weight: 600;
  margin-top: 1rem;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.auth-button:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 10px rgba(0,0,0,0.2);
}
</style>
