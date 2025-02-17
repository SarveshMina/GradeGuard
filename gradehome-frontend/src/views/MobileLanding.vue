<template>
  <div class="mobile-landing">
    <!-- GradeHome Logo -->
    <div class="mobile-logo">GradeHome</div>

    <!-- (Optional Hero image removed for now) -->

    <h1>Connect your content</h1>
    <p>
      A short tagline about your app. Keep it concise for a mobile screen.
    </p>

    <div class="buttons">
      <!-- Sign up goes to your login page in signup mode -->
      <router-link
          :to="{ path: '/login', query: { mode: 'signup' } }"
          class="btn sign-up"
      >
        Sign up
      </router-link>

      <!-- Log in goes to your login page in login mode -->
      <router-link
          :to="{ path: '/login', query: { mode: 'login' } }"
          class="btn login"
      >
        Log in
      </router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: 'MobileLanding',
}
</script>

<style scoped>
.mobile-landing {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  /* Purple to white gradient background */
  background: linear-gradient(160deg, #B191FC, #ffffff);
  color: #000;
  text-align: center;
  padding: 1rem;
}

/* Updated logo style: larger and dark purple */
.mobile-logo {
  position: absolute;
  top: 40px;
  font-size: 50px;       /* Increased size */
  font-weight: 700;
  color: #512DA8;        /* Dark purple */
}

h1 {
  font-size: 24px;
  margin-bottom: 12px;
}

p {
  font-size: 16px;
  max-width: 260px;
  line-height: 1.4;
  margin-bottom: 32px;
  color: #000;
}

.buttons {
  display: flex;
  flex-direction: column;
  width: 100%;
  max-width: 280px;
  gap: 16px;
}

.btn {
  display: block;
  text-decoration: none;
  text-align: center;
  font-size: 16px;
  padding: 12px;
  border-radius: 8px;
  font-weight: 600;
}

/* Sign-up button: white background with dark purple text */
.sign-up {
  background: #fff;
  color: #512DA8;
}

/* Login button: transparent background with dark purple border and text */
.login {
  background: transparent;
  border: 2px solid #512DA8;
  color: #512DA8;
}
</style>
