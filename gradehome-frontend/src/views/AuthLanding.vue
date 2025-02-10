<template>
  <div
      class="auth-container"
      :class="isDarkMode ? 'dark-mode' : 'light-mode'"
      @mousemove="handleMouseMove"
  >
    <!-- Header with Title and Mode Toggle -->
    <header class="auth-header">
      <h1 class="app-name">GradeHome</h1>
      <button class="mode-toggle" @click="toggleDarkMode">
        {{ isDarkMode ? 'Light Mode' : 'Dark Mode' }}
      </button>
    </header>

    <!-- Content (Toggle Buttons and Authentication Panel) -->
    <div class="auth-content">
      <div class="auth-toggle">
        <button
            :class="{ active: currentView === 'login' }"
            @click="switchView('login')"
        >
          Login
        </button>
        <button
            :class="{ active: currentView === 'register' }"
            @click="switchView('register')"
        >
          Register
        </button>
      </div>

      <div class="auth-panel">
        <!-- Login Form -->
        <div v-if="currentView === 'login'">
          <h3>Login</h3>
          <form @submit.prevent="doLogin">
            <div class="form-group">
              <input
                  type="email"
                  v-model="loginEmail"
                  placeholder="Email"
                  class="auth-input"
                  required
              />
            </div>
            <div class="form-group password-group">
              <input
                  :type="showLoginPassword ? 'text' : 'password'"
                  v-model="loginPassword"
                  placeholder="Password"
                  class="auth-input"
                  required
              />
              <span class="toggle-password" @click="toggleLoginPassword">
                {{ showLoginPassword ? 'Hide' : 'Show' }}
              </span>
            </div>
            <p v-if="loginError" class="error">{{ loginError }}</p>
            <button type="submit" class="btn">Login</button>
          </form>
        </div>

        <!-- Registration Form -->
        <div v-else-if="currentView === 'register'">
          <h3>Register</h3>
          <form @submit.prevent="doRegister">
            <div class="form-group">
              <input
                  type="text"
                  v-model="registerUsername"
                  placeholder="Username"
                  class="auth-input"
                  required
              />
            </div>
            <div class="form-group">
              <input
                  type="email"
                  v-model="registerEmail"
                  placeholder="Email"
                  class="auth-input"
                  required
              />
            </div>
            <div class="form-group password-group">
              <input
                  :type="showRegisterPassword ? 'text' : 'password'"
                  v-model="registerPassword"
                  placeholder="Password"
                  class="auth-input"
                  required
              />
              <span class="toggle-password" @click="toggleRegisterPassword">
                {{ showRegisterPassword ? 'Hide' : 'Show' }}
              </span>
            </div>
            <p v-if="registerError" class="error">{{ registerError }}</p>
            <button type="submit" class="btn">Register</button>
          </form>
        </div>
      </div>
    </div>

    <!-- Footer -->
    <footer class="auth-footer">
      <p>&copy; 2025 GradeHome. All rights reserved.</p>
    </footer>
  </div>
</template>

<script>
export default {
  name: "AuthLanding",
  data() {
    return {
      currentView: "login",

      // Login form data
      loginEmail: "",
      loginPassword: "",
      loginError: "",
      showLoginPassword: false,

      // Registration form data
      registerUsername: "",
      registerEmail: "",
      registerPassword: "",
      registerError: "",
      showRegisterPassword: false,

      // Dark mode toggle
      isDarkMode: false,
    };
  },
  methods: {
    switchView(view) {
      this.currentView = view;
      this.loginError = "";
      this.registerError = "";
    },
    toggleLoginPassword() {
      this.showLoginPassword = !this.showLoginPassword;
    },
    toggleRegisterPassword() {
      this.showRegisterPassword = !this.showRegisterPassword;
    },
    handleMouseMove(event) {
      const xPercent = event.clientX / window.innerWidth;
      this.$el.style.setProperty("--gradient-angle", `${xPercent * 360}deg`);
    },
    async doLogin() {
      this.loginError = "";
      try {
        const response = await fetch("http://localhost:7071/api/login", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            email: this.loginEmail,
            password: this.loginPassword,
          }),
        });
        if (!response.ok) {
          const errorData = await response.json();
          this.loginError = errorData.error || "Login failed.";
        } else {
          const data = await response.json();
          localStorage.setItem("token", data.token);
          alert("Login successful!");
        }
      } catch (error) {
        this.loginError = "An error occurred: " + error.message;
      }
    },
    async doRegister() {
      this.registerError = "";
      try {
        const response = await fetch("http://localhost:7071/api/register", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            username: this.registerUsername,
            email: this.registerEmail,
            password: this.registerPassword,
          }),
        });
        if (!response.ok) {
          const errorData = await response.json();
          this.registerError = errorData.error || "Registration failed.";
        } else {
          const data = await response.json();
          localStorage.setItem("token", data.token);
          alert("Registration successful!");
        }
      } catch (error) {
        this.registerError = "An error occurred: " + error.message;
      }
    },
    toggleDarkMode() {
      this.isDarkMode = !this.isDarkMode;
    },
  },
};
</script>

<style scoped>
/* Global Box-Sizing */
*,
*::before,
*::after {
  box-sizing: border-box;
}

/* LIGHT MODE Variables */
.auth-container.light-mode {
  --text-color: #000;
  --primary-color: #000; /* Black */
  --container-bg: #fff;  /* White */
  --glow-color: rgba(0, 0, 0, 0.5); /* Black glow */
}

/* DARK MODE Variables */
.auth-container.dark-mode {
  --text-color: #fff;
  --primary-color: #fff; /* White */
  --container-bg: #444;  /* Dark gray */
  --glow-color: rgba(255, 255, 255, 0.5); /* White glow */
}

/* Outer Container */
.auth-container {
  position: relative;
  min-height: 100vh;
  overflow: hidden;
  background-color: var(--container-bg);
  transition: background-color 0.3s ease;
  font-family: 'Roboto', sans-serif;
  padding: 20px;
  color: var(--text-color);
  /* Glow effect on the container */
  box-shadow: 0 0 20px 10px var(--glow-color);
}

/* Content Container */
.auth-content {
  max-width: 420px;
  margin: 0 auto;
}

/* Header */
.auth-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
.app-name {
  font-size: 2.5rem;
  font-weight: 700;
  letter-spacing: 1px;
  color: var(--text-color);
}
.mode-toggle {
  background: transparent;
  border: 1px solid transparent;
  font-size: 1rem;
  cursor: pointer;
  color: var(--text-color);
  padding: 8px 12px;
  transition: border-color 0.3s;
}
.mode-toggle:hover {
  border-color: var(--primary-color);
}

/* Toggle Buttons */
.auth-toggle {
  display: flex;
  justify-content: center;
  margin-bottom: 25px;
}
.auth-toggle button {
  background: transparent;
  border: none;
  font-size: 1.1rem;
  padding: 10px 25px;
  cursor: pointer;
  transition: all 0.3s ease;
  color: var(--text-color);
  border-bottom: 2px solid transparent;
}
.auth-toggle button:hover {
  color: var(--primary-color);
}
.auth-toggle button.active {
  color: var(--primary-color);
  border-color: var(--primary-color);
}

/* Authentication Panel/Form */
.auth-panel h3 {
  text-align: center;
  margin-bottom: 25px;
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--text-color);
}
.form-group {
  margin-bottom: 20px;
}
.auth-input {
  width: 100%;
  padding: 14px 18px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
  outline: none;
  transition: border-color 0.3s ease, box-shadow 0.3s ease;
  background: #fff;
  color: var(--text-color);
}
.auth-input:focus {
  border-color: var(--primary-color);
  box-shadow: 0 0 8px rgba(0, 0, 0, 0.3);
}
.password-group {
  position: relative;
}
.toggle-password {
  position: absolute;
  top: 50%;
  right: 18px;
  transform: translateY(-50%);
  cursor: pointer;
  font-size: 0.9rem;
  user-select: none;
  color: var(--primary-color);
}

/* Error Message */
.error {
  color: #e74c3c;
  text-align: center;
  margin-bottom: 15px;
  font-size: 0.9rem;
}

/* Submit Button styled like the CV Button using black/white scheme */
.btn {
  display: inline-block;
  width: 100%;
  padding: 0.75rem 1.5rem;
  border: 2px solid var(--primary-color);
  border-radius: 25px;
  background: transparent;
  color: var(--primary-color);
  font-size: 1rem;
  font-family: 'Roboto', sans-serif;
  font-weight: bold;
  text-decoration: none;
  transition: background-color 0.3s, color 0.3s, transform 0.3s, box-shadow 0.3s;
}
.btn:hover {
  background-color: var(--primary-color);
  color: #fff;
  transform: scale(1.05);
  box-shadow: 0 0 8px var(--primary-color);
}

/* Footer */
.auth-footer {
  margin-top: 25px;
  font-size: 0.9rem;
  text-align: center;
  color: var(--text-color);
}
</style>
