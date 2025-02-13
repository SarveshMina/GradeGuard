<template>
  <footer class="auth-footer">
    <div class="footer-main">
      <div class="footer-col">
        <h3>GradeHome</h3>
        <ul>
          <li><router-link to="/">Home</router-link></li>
          <li><router-link to="/">About</router-link></li>
          <li><router-link to="/">GPA Calculator</router-link></li>
          <li><router-link to="/">Reviews</router-link></li>
          <li><router-link to="/">Analytics</router-link></li>
        </ul>
      </div>
      <div class="footer-col">
        <h3>Account</h3>
        <ul>
          <li><router-link to="/login">Login</router-link></li>
          <li><router-link to="/register">Sign Up</router-link></li>
        </ul>
      </div>
      <div class="footer-col">
        <h3>Legal</h3>
        <ul>
          <li><a href="#">Privacy Policy</a></li>
          <li><a href="#">Terms of Service</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h3>Contact</h3>
        <p>
          <strong>GradeHome</strong><br />
          <a href="mailto:sarveshmina@outlook.com">sarveshmina@outlook.com</a><br />
          Made by Sarvesh Mina
        </p>
      </div>
    </div>
  </footer>
</template>

<script>
export default {
  name: "Footer"
};
</script>

<style scoped>
.auth-footer {
  background: var(--footer-bg);
  text-align: center;
  padding: 1rem;
  margin-top: auto;
  box-shadow: 0 -2px 4px rgba(0, 0, 0, 0.1);
}
.footer-main {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 2rem;
}
.footer-col {
  flex: 1 1 200px;
  min-width: 150px;
}
.footer-col h3 {
  margin-bottom: 0.6rem;
  font-size: 1.1rem;
}
.footer-col ul {
  list-style: none;
  padding: 0;
  margin: 0;
}
.footer-col ul li {
  margin-bottom: 0.3rem;
}
.footer-col a {
  color: var(--link-color);
  text-decoration: none;
  transition: 0.3s;
}
.footer-col a:hover {
  text-decoration: underline;
}
.footer-col p {
  line-height: 1.4;
}
</style>
