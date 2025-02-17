<template>
  <header class="auth-header">
    <div class="logo">GradeHome</div>
    <nav>
      <!-- When in login mode, show a Sign Up link; otherwise, show Login -->
      <router-link
          v-if="mode === 'login'"
          :to="{ path: '/login', query: { mode: 'signup' } }"
          class="arrow-btn"
      >
        <span class="text">Sign Up</span>
        <svg
            width="16"
            height="16"
            viewBox="0 0 16 16"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
        >
          <path
              d="M4.66669 11.3334L11.3334 4.66669"
              stroke="white"
              stroke-width="1.33333"
              stroke-linecap="round"
              stroke-linejoin="round"
          />
          <path
              d="M4.66669 4.66669H11.3334V11.3334"
              stroke="white"
              stroke-width="1.33333"
              stroke-linecap="round"
              stroke-linejoin="round"
          />
        </svg>
      </router-link>

      <router-link
          v-else
          :to="{ path: '/login', query: { mode: 'login' } }"
          class="arrow-btn"
      >
        <span class="text">Login</span>
        <svg
            width="16"
            height="16"
            viewBox="0 0 16 16"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
        >
          <path
              d="M4.66669 11.3334L11.3334 4.66669"
              stroke="white"
              stroke-width="1.33333"
              stroke-linecap="round"
              stroke-linejoin="round"
          />
          <path
              d="M4.66669 4.66669H11.3334V11.3334"
              stroke="white"
              stroke-width="1.33333"
              stroke-linecap="round"
              stroke-linejoin="round"
          />
        </svg>
      </router-link>

      <!-- Dark mode toggle button -->
      <button @click="toggleDarkMode" class="nav-button dark-mode-toggle">
        <i v-if="!darkMode" class="fas fa-moon"></i>
        <i v-else class="fas fa-sun"></i>
      </button>
    </nav>
  </header>
</template>

<script>
export default {
  name: "NavBar",
  props: {
    // Accepts "login", "signup", or "forgot" to indicate the current mode
    mode: {
      type: String,
      default: "login"
    }
  },
  data() {
    return {
      darkMode: false
    }
  },
  methods: {
    toggleDarkMode() {
      this.darkMode = !this.darkMode;
      if (this.darkMode) {
        document.body.classList.add("dark-mode");
      } else {
        document.body.classList.remove("dark-mode");
      }
    }
  }
};
</script>

<style scoped>
.auth-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  background: var(--header-bg);
  box-shadow: none;
}
.logo {
  font-size: 2rem;
  font-weight: bold;
  color: #512da8;
}
nav {
  display: flex;
  align-items: center;
}

/* Arrow button styling (for Sign Up / Login links) */
.arrow-btn {
  font-size: 16px;
  font-weight: 600;
  background-color: #512da8;
  color: #fff;
  text-decoration: none;
  padding: 0.6rem 1.8rem 0.6rem 1.2rem;
  border-radius: 99px;
  position: relative;
  border: none;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  transition: 0.4s ease;
  margin-left: 0.5rem;
}
.arrow-btn .text {
  line-height: 1;
  margin-right: 2rem;
  position: relative;
  z-index: 5;
}
.arrow-btn::before {
  content: '';
  background-color: #b39ddb;
  width: 28px;
  height: 28px;
  border-radius: 99px;
  position: absolute;
  top: 50%;
  right: 10px;
  transform: translateY(-50%);
  transition: all 0.4s ease;
  z-index: 1;
}
.arrow-btn svg {
  width: 14px;
  height: 14px;
  position: absolute;
  right: 16px;
  top: 50%;
  transform: translateY(-50%) rotate(0deg);
  transform-origin: center;
  transition: 0.4s ease;
  z-index: 5;
}
.arrow-btn:hover svg {
  transform: translateY(-50%) rotate(45deg);
}
.arrow-btn:hover::before {
  width: 100%;
  height: 100%;
  right: 0;
}

/* Dark mode toggle button styling */
.nav-button {
  margin: 0 0.5rem;
  padding: 0.8rem 1.2rem;
  border: 2px solid #000;
  background: transparent;
  color: #000;
  border-radius: 24px;
  cursor: pointer;
  transition: 0.3s;
  font-weight: 600;
  text-decoration: none;
  box-shadow: 0 0 8px rgba(0,0,0,0.2);
}
.nav-button:hover {
  background: #000;
  color: #fff;
  transform: translateY(-2px);
  box-shadow: 0 0 12px rgba(0,0,0,0.4);
}
</style>
