<template>
  <footer class="enhanced-footer">
    <div class="footer-content">
      <div class="footer-main">
        <div class="footer-col brand-col">
          <div class="footer-logo">GradeGuard</div>
          <p class="footer-tagline">Your intelligent academic companion</p>
          <div class="social-links">
            <a href="https://github.com/SarveshMina" target="_blank" rel="noopener noreferrer" aria-label="GitHub">
              <svg viewBox="0 0 24 24" width="22" height="22" stroke="currentColor" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"></path>
              </svg>
            </a>
            <a href="mailto:sarveshmina@outlook.com" aria-label="Email">
              <svg viewBox="0 0 24 24" width="22" height="22" stroke="currentColor" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path>
                <polyline points="22,6 12,13 2,6"></polyline>
              </svg>
            </a>
          </div>
        </div>

        <div class="footer-col">
          <h3>Navigation</h3>
          <ul>
            <li><router-link to="/">Home</router-link></li>
            <li><router-link to="/">About</router-link></li>
            <li><router-link to="/">GPA Calculator</router-link></li>
            <li><router-link to="/">Analytics</router-link></li>
          </ul>
        </div>

        <div class="footer-col">
          <h3>Account</h3>
          <ul>
            <li><router-link to="/login">Login</router-link></li>
            <li><router-link to="/register">Sign Up</router-link></li>
            <li><router-link to="/">Dashboard</router-link></li>
            <li><router-link to="/">Settings</router-link></li>
          </ul>
        </div>

        <div class="footer-col">
          <h3>Resources</h3>
          <ul>
            <li><a href="#">Privacy Policy</a></li>
            <li><a href="#">Terms of Service</a></li>
            <li><a href="#">Support</a></li>
            <li><a href="#">FAQ</a></li>
          </ul>
        </div>
      </div>
    </div>

    <div class="footer-bottom">
      <div class="footer-divider"></div>
      <div class="copyright">
        <p>&copy; {{ new Date().getFullYear() }} GradeGuard. All rights reserved.</p>
        <p class="creator">Designed & Developed with 💜 by <a href="https://github.com/SarveshMina" target="_blank" rel="noopener noreferrer">Sarvesh Mina</a></p>
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
.enhanced-footer {
  background: var(--footer-bg, #161625);
  color: var(--footer-text, #e0e0e0);
  padding: 4rem 2rem 1.5rem;
  margin-top: auto;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
}

.footer-main {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  gap: 3rem;
  margin-bottom: 3rem;
}

.footer-col {
  flex: 1;
  min-width: 160px;
}

.brand-col {
  flex: 1.5;
}

.footer-logo {
  font-size: 1.75rem;
  font-weight: 800;
  margin-bottom: 0.75rem;
  background: linear-gradient(135deg, var(--primary-color, #7b49ff), var(--accent-pink, #ec4899));
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  display: inline-block;
}

.footer-tagline {
  color: var(--text-secondary, #a0a0a0);
  margin-bottom: 1.5rem;
  font-size: 0.95rem;
  line-height: 1.5;
}

.social-links {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
}

.social-links a {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: rgba(255, 255, 255, 0.05);
  color: var(--text-secondary, #a0a0a0);
  transition: all 0.3s ease;
}

.social-links a:hover {
  background-color: var(--primary-color, #7b49ff);
  color: white;
  transform: translateY(-3px);
}

.footer-col h3 {
  color: var(--text-primary, #ffffff);
  margin-bottom: 1.2rem;
  font-size: 1.1rem;
  font-weight: 600;
  position: relative;
  padding-bottom: 0.5rem;
}

.footer-col h3::after {
  content: "";
  position: absolute;
  bottom: 0;
  left: 0;
  width: 30px;
  height: 2px;
  background: linear-gradient(90deg, var(--primary-color, #7b49ff), var(--accent-pink, #ec4899));
  border-radius: 2px;
}

.footer-col ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.footer-col ul li {
  margin-bottom: 0.75rem;
}

.footer-col a {
  color: var(--text-secondary, #a0a0a0);
  text-decoration: none;
  transition: all 0.3s ease;
  font-size: 0.95rem;
  position: relative;
  display: inline-block;
}

.footer-col a:hover {
  color: var(--primary-color, #7b49ff);
  transform: translateX(3px);
}

.footer-divider {
  height: 1px;
  background: linear-gradient(to right, transparent, rgba(255, 255, 255, 0.1), transparent);
  margin-bottom: 1.5rem;
}

.footer-bottom {
  text-align: center;
}

.copyright {
  color: var(--text-secondary, #a0a0a0);
  font-size: 0.9rem;
}

.copyright p {
  margin: 0.5rem 0;
}

.creator {
  margin-top: 0.5rem;
  font-size: 0.85rem;
}

.creator a {
  color: var(--primary-color, #7b49ff);
  text-decoration: none;
  transition: color 0.3s ease;
}

.creator a:hover {
  color: var(--accent-pink, #ec4899);
}

/* Dark mode adjustments */
body.dark-mode .enhanced-footer {
  background: #121220;
}

body.dark-mode .social-links a:hover {
  background-color: var(--primary-color, #7b49ff);
}

/* Media queries for responsiveness */
@media (max-width: 768px) {
  .enhanced-footer {
    padding: 3rem 1.5rem 1rem;
  }

  .footer-main {
    gap: 2rem;
  }

  .footer-col {
    min-width: 140px;
  }

  .brand-col {
    flex: 100%;
  }
}

@media (max-width: 576px) {
  .footer-main {
    flex-direction: column;
    gap: 2rem;
  }

  .footer-col {
    width: 100%;
    min-width: 100%;
  }

  .footer-col h3 {
    text-align: center;
  }

  .footer-col h3::after {
    left: 50%;
    transform: translateX(-50%);
    width: 40px;
  }

  .footer-col ul {
    text-align: center;
  }

  .social-links {
    justify-content: center;
  }

  .footer-logo, .footer-tagline {
    text-align: center;
  }
}
</style>