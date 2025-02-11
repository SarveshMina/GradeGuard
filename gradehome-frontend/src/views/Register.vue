<template>
  <div class="auth-page">
    <header class="auth-header">
      <h1>Sign Up for GradeHome</h1>
    </header>

    <form class="auth-form" @submit.prevent="doRegister">
      <div class="form-group">
        <input
            type="text"
            v-model="registerUsername"
            placeholder="Username"
            required
        />
      </div>
      <div class="form-group">
        <input
            type="email"
            v-model="registerEmail"
            placeholder="Email"
            required
        />
      </div>
      <div class="form-group">
        <input
            :type="showPassword ? 'text' : 'password'"
            v-model="registerPassword"
            placeholder="Password"
            required
        />
        <button type="button" class="toggle-btn" @click="togglePassword">
          {{ showPassword ? 'Hide' : 'Show' }}
        </button>
      </div>
      <p v-if="registerError" class="error">{{ registerError }}</p>
      <button class="submit-btn" type="submit">Register</button>
    </form>
  </div>
</template>

<script>
export default {
  name: "Register",
  data() {
    return {
      registerUsername: "",
      registerEmail: "",
      registerPassword: "",
      showPassword: false,
      registerError: "",
    };
  },
  methods: {
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
          // Possibly redirect to a login or dashboard
          // this.$router.push("/login");
        }
      } catch (error) {
        this.registerError = "An error occurred: " + error.message;
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
