<template>
  <div class="auth-container">
    <NavBar mode="register" />
    <main class="auth-main">
      <h1>Create Account</h1>
      <p>
        Already have an account?
        <router-link to="/login">Log in</router-link>
      </p>
      <form @submit.prevent="handleRegister">
        <div class="form-group">
          <label for="email">Email</label>
          <input
              type="email"
              v-model="email"
              id="email"
              placeholder="minasarvesh@gmail.com"
              required
          />
        </div>
        <div class="form-group">
          <label for="password">Password</label>
          <input
              type="password"
              v-model="password"
              id="password"
              placeholder="•••••••••••"
              required
          />
        </div>
        <div class="form-group">
          <label for="firstName">First Name</label>
          <input
              type="text"
              v-model="firstName"
              id="firstName"
              placeholder="Enter your first name"
              required
          />
        </div>
        <div class="form-group">
          <label for="university">University/College</label>
          <input
              type="text"
              v-model="university"
              id="university"
              placeholder="University/College"
              required
          />
        </div>
        <div class="form-group">
          <label for="degree">Degree</label>
          <input
              type="text"
              v-model="degree"
              id="degree"
              placeholder="Your degree"
              required
          />
        </div>
        <div class="form-group">
          <label for="calcType">Select Calculator Type</label>
          <select v-model="calcType" id="calcType" required>
            <option value="" disabled>Select type</option>
            <option value="uk-percentage">UK Percentage</option>
            <option value="us-gpa-4">US GPA 4.0</option>
            <option value="us-gpa-5">US GPA 5.0</option>
          </select>
        </div>
        <button type="submit" class="auth-button">Create Account</button>
      </form>
    </main>
    <Footer />
  </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue'
import Footer from '@/components/Footer.vue'

export default {
  name: 'Register',
  components: { NavBar, Footer },
  data() {
    return {
      email: '',
      password: '',
      firstName: '',
      university: '',
      degree: '',
      calcType: ''
    }
  },
  methods: {
    handleRegister() {
      alert(`Registering ${this.email}`);
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

.auth-main p {
  text-align: center;
  margin-bottom: 1rem;
}

.auth-main p router-link {
  text-decoration: none;
  color: var(--link-color);
}

.form-group {
  margin-bottom: 0.75rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
}

.form-group input,
.form-group select {
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
