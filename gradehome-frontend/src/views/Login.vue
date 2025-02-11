<template>
  <div class="auth-page">
    <header class="auth-header">
      <h1>Login to GradeHome</h1>
    </header>

    <form class="auth-form" @submit.prevent="doLogin">
      <div class="form-group">
        <input
            type="email"
            v-model="loginEmail"
            placeholder="Email"
            required
        />
      </div>
      <div class="form-group">
        <input
            :type="showPassword ? 'text' : 'password'"
            v-model="loginPassword"
            placeholder="Password"
            required
        />
        <button type="button" class="toggle-btn" @click="togglePassword">
          {{ showPassword ? 'Hide' : 'Show' }}
        </button>
      </div>
      <p v-if="loginError" class="error">{{ loginError }}</p>
      <button class="submit-btn" type="submit">Login</button>
    </form>
  </div>
</template>

<script>
export default {
  name: "Login",
  data() {
    return {
      loginEmail: "",
      loginPassword: "",
      showPassword: false,
      loginError: "",
    };
  },
  methods: {
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
          // Possibly redirect somewhere:
          // this.$router.push("/dashboard");
        }
      } catch (error) {
        this.loginError = "An error occurred: " + error.message;
      }
    },
    togglePassword() {
      this.showPassword = !this.showPassword;
    },
  },
};
</script>

<style scoped>
.auth-page {
  max-width: 400px;
  margin: 3rem auto;
  padding: 2rem;
  background: #fff;
  border-radius: 8px;
}
.auth-header {
  text-align: center;
  margin-bottom: 1rem;
}
.auth-form .form-group {
  margin-bottom: 1rem;
}
.auth-form input {
  width: 100%;
  padding: 10px;
  box-sizing: border-box;
}
.toggle-btn {
  margin-top: 0.5rem;
}
.submit-btn {
  width: 100%;
  padding: 12px;
  background: #646cff;
  color: #fff;
  border: none;
  cursor: pointer;
  font-weight: bold;
  border-radius: 6px;
}
.error {
  color: #e74c3c;
  margin-bottom: 1rem;
}
</style>
