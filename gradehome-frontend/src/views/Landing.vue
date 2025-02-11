<template>
  <!-- Dynamic binding: when darkMode is true, the .dark-mode class is applied -->
  <div :class="{ 'landing-container': true, 'dark-mode': darkMode }">
    <!-- Header -->
    <header class="landing-header" ref="headerRef">
      <div class="logo">GradeHome</div>
      <nav>
        <!-- Login and Sign Up buttons -->
        <button @click="goToLogin" class="nav-button">Login</button>
        <button @click="goToRegister" class="nav-button">Sign Up</button>
        <!-- Dark mode toggle button -->
        <button @click="toggleDarkMode" class="nav-button dark-mode-toggle">
          <i v-if="!darkMode" class="fas fa-moon"></i>
          <i v-else class="fas fa-sun"></i>
        </button>
      </nav>
    </header>

    <!-- Hero Section with Parallax and Mouse Reactive Background -->
    <section class="hero-parallax" ref="heroRef">
      <div class="hero-parallax-overlay">
        <div class="hero-content" data-aos="fade-up">
          <h1>The Grade Calculator</h1>
          <p>
            Track your university grade average, predict your degree classification, and more.
          </p>
          <div class="hero-buttons">
            <!-- Get Started button -->
            <button class="cta-button" @click="goToRegister">Get Started</button>
          </div>
        </div>
      </div>
    </section>

    <!-- Stats + "Calculate Without Signing Up" Section -->
    <section class="stats-section" ref="statsSectionRef" data-aos="fade-up">
      <div class="calc-form">
        <h3>Calculate without signing up</h3>
        <label>Your University / College</label>
        <input type="text" v-model="university" placeholder="e.g. MIT" />
        <label>Your Degree</label>
        <input type="text" v-model="degree" placeholder="e.g. Computer Science" />
        <button class="start-btn" @click="handleQuickCalc">Start</button>
      </div>

      <!-- Container for the switching stats card with fixed minimum height -->
      <div class="stats-card-container">
        <!-- Tab buttons -->
        <div class="tabs">
          <button
              :class="{ active: statsMode === 'percentage' }"
              @click="statsMode = 'percentage'"
          >
            Percentage
          </button>
          <button
              :class="{ active: statsMode === 'gpa' }"
              @click="statsMode = 'gpa'"
          >
            GPA
          </button>
        </div>

        <!-- Transition wrapper: using "fade-scale" with mode "out-in" -->
        <transition name="fade-scale" mode="out-in">
          <div class="stats-card" :key="statsMode">
            <!-- Percentage Mode -->
            <div v-if="statsMode === 'percentage'">
              <h2>60% Average</h2>
              <div class="progress-bar">
                <div class="segment achieved" style="width: 45%">45%</div>
                <div class="segment lost" style="width: 30%">30%</div>
                <div class="segment remaining" style="width: 25%">25%</div>
              </div>
              <div class="modules-list">
                <div class="module" v-for="m in modulesPerc" :key="m.name">
                  <div :class="['module-icon', m.colorClass]">{{ m.letter }}</div>
                  <div class="module-info">
                    <strong>{{ m.name }}</strong> <small>({{ m.credits }} credits)</small>
                  </div>
                  <div class="module-grade">{{ m.grade }}</div>
                </div>
              </div>
            </div>
            <!-- GPA Mode -->
            <div v-else-if="statsMode === 'gpa'">
              <h2>3.7 GPA</h2>
              <div class="progress-bar">
                <div class="segment achieved" style="width: 75%">75%</div>
                <div class="segment remaining" style="width: 25%">25%</div>
              </div>
              <div class="modules-list">
                <div class="module" v-for="m in modulesGpa" :key="m.name">
                  <div :class="['module-icon', m.colorClass]">{{ m.letter }}</div>
                  <div class="module-info">
                    <strong>{{ m.name }}</strong> <small>({{ m.credits }} credits)</small>
                  </div>
                  <div class="module-grade">{{ m.grade }}</div>
                </div>
              </div>
            </div>
          </div>
        </transition>
      </div>
    </section>

    <!-- "Easy, But Powerful" Section -->
    <section class="features-section" ref="featuresRef" data-aos="fade-up">
      <div class="features-hero">
        <h2>
          <span class="highlight">EASY,</span> BUT POWERFUL,<br />
          GRADE TRACKER
        </h2>
      </div>
      <div class="features-list">
        <div class="feature-item">
          <h3><span class="vertical-bar"></span> Track coursework and exams</h3>
          <p>
            With our weighted average calculator you can keep track of your grades and calculate your average.
            GradeHome takes an average of the exam and coursework marks for your modules.
            The credits for a module are used as weighting for your total year average.
          </p>
        </div>
        <div class="feature-item">
          <h3><span class="vertical-bar"></span> Split up your years</h3>
          <p>
            You can divide your modules into years and customise weights for each year. For most degrees,
            the first year doesn't count towards your final score. There is often a 40:60 split for your final two years but this varies by university and is handled by GradeHome's calculator.
          </p>
        </div>
        <div class="feature-item">
          <h3><span class="vertical-bar"></span> Add grade targets</h3>
          <p>
            Predict your final grade classification with degree targets. Figure out how well you need to
            score in your remaining exams to get a 1st class honours or a GPA 4.0.
          </p>
        </div>
      </div>
    </section>

    <!-- Grading Systems Section turned into 3 cards -->
    <section class="systems-section" ref="systemsRef" data-aos="fade-up">
      <div class="system-cards">
        <div class="system-card">
          <h3>Support for Every Grading System</h3>
          <p>GradeHome supports grading systems for universities and colleges from all over the world.</p>
        </div>
        <div class="system-card">
          <h3>US Grade Point Average Calculator</h3>
          <p>If your college uses GPA 4.0 or GPA 5.0, we have you covered.</p>
        </div>
        <div class="system-card">
          <h3>UK Weighted Percentage Calculator</h3>
          <p>UK universities often use a weighted average for the final Grade.</p>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="landing-footer" ref="footerRef" data-aos="fade-up">
      <div class="footer-main">
        <div class="footer-col">
          <h3>GradeHub</h3>
          <ul>
            <li><a href="#">Home</a></li>
            <li><a href="#">About</a></li>
            <li><a href="#">GPA Calculator</a></li>
            <li><a href="#">Reviews</a></li>
            <li><a href="#">Analytics</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h3>Account</h3>
          <ul>
            <li><a href="#">Login</a></li>
            <li><a href="#">Sign Up</a></li>
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
          <h3>GradeHub Robot Logo</h3>
          <p>
            <strong>GradeHome</strong><br />
            <a href="mailto:sarveshmina@outlook.com">sarveshmina@outlook.com</a><br />
            —<br />
            Made by Sarvesh Mina
          </p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script>
import AOS from "aos";
import "aos/dist/aos.css";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

export default {
  name: "Landing",
  data() {
    return {
      darkMode: false, // dark mode state
      university: "",
      degree: "",
      statsMode: "percentage",
      modulesPerc: [
        { letter: "N", name: "Neural Networks", credits: 20, grade: "65%", colorClass: "n" },
        { letter: "P", name: "Database Systems", credits: 10, grade: "50%", colorClass: "p" },
        { letter: "Q", name: "Quantum Computing", credits: 10, grade: "-", colorClass: "q" },
      ],
      modulesGpa: [
        { letter: "N", name: "Neural Networks", credits: 20, grade: "A", colorClass: "n" },
        { letter: "P", name: "Database Systems", credits: 10, grade: "B", colorClass: "p" },
        { letter: "Q", name: "Quantum Computing", credits: 10, grade: "-", colorClass: "q" },
      ],
    };
  },
  methods: {
    goToLogin() {
      this.$router.push("/login");
    },
    goToRegister() {
      this.$router.push("/register");
    },
    handleQuickCalc() {
      alert(`Calculating for ${this.university} - ${this.degree}...`);
    },
    toggleDarkMode() {
      this.darkMode = !this.darkMode;
    },
  },
  mounted() {
    AOS.init({
      duration: 1000,
      offset: 120,
      once: true,
    });
    gsap.registerPlugin(ScrollTrigger);
    gsap.from(this.$refs.headerRef, {
      y: -80,
      opacity: 0,
      duration: 1,
      ease: "power3.out",
    });
    gsap.from(this.$refs.heroRef, {
      x: -100,
      opacity: 0,
      duration: 1.2,
      ease: "power2.out",
      scrollTrigger: {
        trigger: this.$refs.heroRef,
        start: "top center",
      },
    });
    // Mouse reactive background for hero section
    const heroSection = this.$refs.heroRef;
    document.addEventListener("mousemove", (e) => {
      const x = e.clientX / window.innerWidth - 0.5;
      const y = e.clientY / window.innerHeight - 0.5;
      gsap.to(heroSection, {
        backgroundPosition: `${50 + x * 10}% ${50 + y * 10}%`,
        duration: 0.5,
        ease: "power2.out",
      });
    });
  },
};
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&display=swap");
@import url("https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css");
@import "aos/dist/aos.css";

.landing-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  font-family: "Poppins", sans-serif;
  color: #000;
  background-color: #fff;
  overflow-x: hidden;
}

/* Text glow for headings/important text */
h1,
h2,
h3,
.logo,
.highlight {
  text-shadow: 0 0 6px rgba(0, 0, 0, 0.1);
}

/* Header */
.landing-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  background: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
.logo {
  font-size: 1.6rem;
  font-weight: bold;
}

/* Buttons */
.nav-button,
.start-btn {
  margin: 0 0.5rem;
  padding: 0.6rem 1.2rem;
  border: 2px solid #000;
  background: transparent;
  color: #000;
  border-radius: 24px;
  cursor: pointer;
  transition: 0.3s;
  font-weight: 600;
  box-shadow: 0 0 8px rgba(0, 0, 0, 0.2);
}
.nav-button:hover,
.start-btn:hover {
  background: #000;
  color: #fff;
  transform: translateY(-2px);
  box-shadow: 0 0 12px rgba(0, 0, 0, 0.4);
}

/* Special Get Started button */
.cta-button {
  margin: 0 0.5rem;
  padding: 0.6rem 1.2rem;
  border: 2px solid #fff;
  background: transparent;
  color: #fff;
  border-radius: 24px;
  cursor: pointer;
  transition: 0.3s;
  font-weight: 600;
  box-shadow: 0 0 8px rgba(0, 0, 0, 0.2);
}
.cta-button:hover {
  background: #fff;
  color: #000;
  transform: translateY(-2px);
  box-shadow: 0 0 12px rgba(0, 0, 0, 0.4);
}

/* Hero / Parallax */
.hero-parallax {
  min-height: 60vh;
  background: #000;
  background-attachment: fixed;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  background-size: 200%;
}
.hero-parallax-overlay {
  background-color: rgba(0, 0, 0, 0.4);
  width: 100%;
  padding: 3rem 1rem;
}
.hero-content {
  text-align: center;
  color: #fff;
}
.hero-content h1 {
  font-size: 3rem;
  margin-bottom: 1rem;
}

/* Stats + Calculator Form */
.stats-section {
  display: flex;
  gap: 2rem;
  padding: 2rem;
  max-width: 1100px;
  margin: 0 auto;
}
.calc-form {
  flex: 1 1 300px;
  background: #f9f9f9;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}
.calc-form h3 {
  margin-bottom: 1rem;
}
.calc-form label {
  display: block;
  margin: 0.5rem 0 0.25rem;
}
.calc-form input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 1rem;
  margin-bottom: 1rem;
  outline: none;
}

/* Container for the switching stats card; fixed min-height prevents layout shift */
.stats-card-container {
  flex: 1 1 500px;
  min-height: 300px; /* Adjust this value if needed */
}

/* Stats Card */
.stats-card {
  background: #fff;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 1px 5px rgba(0, 0, 0, 0.05);
}

/* Transition for switching cards: fade and slight scale */
.fade-scale-enter-active,
.fade-scale-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}
.fade-scale-enter,
.fade-scale-leave-to {
  opacity: 0;
  transform: scale(0.95);
}

/* Progress Bar & Modules */
.progress-bar {
  display: flex;
  height: 24px;
  margin-bottom: 1.5rem;
  border-radius: 6px;
  overflow: hidden;
  background: #eee;
}
.segment {
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
}
.achieved {
  background: #000;
}
.lost {
  background: #555;
  color: #fff;
}
.remaining {
  background: #ccc;
  color: #000;
}
.modules-list .module {
  display: flex;
  align-items: center;
  padding: 0.5rem 0;
  border-bottom: 1px solid #f0f0f0;
}
.modules-list .module:last-child {
  border-bottom: none;
}
.module-icon {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  color: #fff;
  font-weight: bold;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 1rem;
}
.n {
  background: #ADD8E6;
}
.p {
  background: #FFB6C1;
}
.q {
  background: #E6E6FA;
}
.module-info {
  flex: 1;
}
.module-grade {
  font-weight: bold;
}

/* Tabs */
.tabs {
  margin-bottom: 1rem;
}
.tabs button {
  border: 1px solid #ccc;
  background: #eee;
  padding: 0.5rem 1rem;
  margin-right: 0.5rem;
  cursor: pointer;
  border-radius: 24px;
  transition: 0.3s;
}
.tabs button.active {
  background: #000;
  border-color: #000;
  color: #fff;
}

/* Features */
.features-section {
  display: flex;
  flex-wrap: wrap;
  padding: 1.5rem 15rem;
  gap: 0.25rem;
}
.features-hero {
  flex: 1 1 250px;
}
.features-list {
  flex: 2 1 400px;
}
.features-hero h2 {
  font-size: 2.2rem;
  line-height: 1.2;
  margin-bottom: 1rem;
}
.highlight {
  color: #000;
}
.feature-item h3 {
  margin-bottom: 0.3rem;
  font-size: 1.2rem;
}
.vertical-bar {
  display: inline-block;
  background: #000;
  width: 4px;
  height: 1rem;
  margin-right: 6px;
}

/* Systems Section */
.systems-section {
  padding: 2rem 3rem;
}
.system-cards {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
}
.system-card {
  flex: 1;
  background: #fff;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  text-align: center;
}
.system-card h3 {
  margin-bottom: 0.75rem;
}

/* Footer */
.landing-footer {
  background: #fff;
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
  color: #000;
  text-decoration: none;
  transition: 0.3s;
}
.footer-col a:hover {
  text-decoration: underline;
}
.footer-col p {
  line-height: 1.4;
}
.contact-info {
  margin-top: 2rem;
  font-size: 0.9rem;
  text-align: center;
}
.contact-info a {
  color: #000;
  text-decoration: none;
  transition: 0.3s;
}
.contact-info a:hover {
  text-decoration: underline;
}

/* =================== */
/* Dark Mode Styles  */
/* =================== */
.dark-mode {
  background-color: #121212;
  color: #e0e0e0;
}
.dark-mode .landing-header {
  background: #2b2b2b;
  box-shadow: 0 2px 4px rgba(34, 34, 34, 0.5);
}
.dark-mode .logo {
  color: #e0e0e0;
}
.dark-mode .nav-button,
.dark-mode .start-btn {
  border-color: #e0e0e0;
  color: #e0e0e0;
}
.dark-mode .nav-button:hover,
.dark-mode .start-btn:hover {
  background: #e0e0e0;
  color: #121212;
}
/* Hero section dark mode uses grey instead of black */
.dark-mode .hero-parallax {
  background-color: #555;
}
.dark-mode .hero-parallax-overlay {
  background-color: rgba(85, 85, 85, 0.7);
}
.dark-mode .calc-form {
  background: #2c2c2c;
  color: #e0e0e0;
}
.dark-mode .calc-form input {
  background: #444;
  border-color: #555;
  color: #e0e0e0;
}
.dark-mode .stats-card {
  background: #2c2c2c;
  border-color: #444;
}
.dark-mode .tabs button {
  background: #444;
  border-color: #555;
  color: #e0e0e0;
}
.dark-mode .tabs button.active {
  background: #e0e0e0;
  color: #121212;
}
.dark-mode .progress-bar {
  background: #444;
}
.dark-mode .progress-bar .segment.achieved {
  background: #0d6efd;
}
.dark-mode .progress-bar .segment.lost {
  background: #6c757d;
}
.dark-mode .progress-bar .segment.remaining {
  background: #adb5bd;
}
.dark-mode .system-card {
  background: #2c2c2c;
  color: #e0e0e0;
}
.dark-mode .landing-footer {
  background: #2b2b2b;
  color: #ccc;
  box-shadow: 0 -2px 4px rgba(34, 34, 34, 0.5);
}
.dark-mode .footer-col a,
.dark-mode .contact-info a {
  color: #ccc;
}

/* New overrides: In dark mode, only the "EASY," text and the vertical bar (bullet) become light grey */
.dark-mode .highlight {
  color: #ccc;
}
.dark-mode .vertical-bar {
  background: #ccc;
}
</style>
