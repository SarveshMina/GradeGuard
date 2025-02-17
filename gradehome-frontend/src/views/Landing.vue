<template>
  <div class="landing-container" ref="landingContainer">
    <!-- Fixed Header/Nav -->
    <header class="landing-header" ref="headerRef">
      <div class="logo">GradeHome</div>
      <nav>
        <!-- Arrow buttons for Login & Sign Up -->
        <router-link :to="{ path: '/login', query: { mode: 'login' } }" class="arrow-btn">
          <span class="text">Login</span>
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none"
               xmlns="http://www.w3.org/2000/svg">
            <path d="M4.66669 11.3334L11.3334 4.66669"
                  stroke="white" stroke-width="1.33333"
                  stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M4.66669 4.66669H11.3334V11.3334"
                  stroke="white" stroke-width="1.33333"
                  stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </router-link>

        <router-link :to="{ path: '/login', query: { mode: 'signup' } }" class="arrow-btn">
          <span class="text">Sign Up</span>
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none"
               xmlns="http://www.w3.org/2000/svg">
            <path d="M4.66669 11.3334L11.3334 4.66669"
                  stroke="white" stroke-width="1.33333"
                  stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M4.66669 4.66669H11.3334V11.3334"
                  stroke="white" stroke-width="1.33333"
                  stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </router-link>

        <!-- Dark mode toggle -->
        <button @click="toggleDarkMode" class="nav-button dark-mode-toggle">
          <i v-if="!darkMode" class="fas fa-moon"></i>
          <i v-else class="fas fa-sun"></i>
        </button>
      </nav>
    </header>

    <!-- Hero Section -->
    <section class="hero-parallax" ref="heroRef">
      <div class="hero-parallax-overlay">
        <div class="hero-content" data-aos="fade-up">
          <h1>The Grade Calculator</h1>
          <p>
            Track your university grade average, predict your degree classification, and more.
          </p>
          <div class="hero-buttons">
            <router-link :to="{ path: '/login', query: { mode: 'signup' } }" class="cta-button">
              <span class="text">Get Started</span>
              <svg width="16" height="16" viewBox="0 0 16 16" fill="none"
                   xmlns="http://www.w3.org/2000/svg">
                <path d="M4.66669 11.3334L11.3334 4.66669"
                      stroke="white" stroke-width="1.33333"
                      stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M4.66669 4.66669H11.3334V11.3334"
                      stroke="white" stroke-width="1.33333"
                      stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </router-link>
            <button class="scroll-btn" @click="scrollToCalcForm">
              Start Without Signing Up
            </button>
          </div>
        </div>
        <button v-if="showScrollDown" class="scroll-down-btn" @click="scrollToCalcForm">
          <i class="fas fa-arrow-down"></i>
        </button>
      </div>
    </section>

    <!-- Stats & Calculator Section -->
    <section class="stats-section" ref="statsSectionRef" data-aos="fade-up">
      <div class="calc-form">
        <h3>Calculate without signing up</h3>
        <label>Your University / College</label>
        <input type="text" v-model="university" placeholder="e.g. MIT" />
        <label>Your Degree</label>
        <input type="text" v-model="degree" placeholder="e.g. Computer Science" />
        <button class="start-btn" @click="handleQuickCalc">Start</button>
      </div>
      <div class="stats-card-container">
        <div class="tabs">
          <button :class="{ active: statsMode === 'percentage' }" @click="statsMode = 'percentage'">
            Percentage
          </button>
          <button :class="{ active: statsMode === 'gpa' }" @click="statsMode = 'gpa'">
            GPA
          </button>
        </div>
        <transition name="fade-scale" mode="out-in">
          <div class="stats-card" :key="statsMode">
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
                    <strong>{{ m.name }}</strong>
                    <small>({{ m.credits }} credits)</small>
                  </div>
                  <div class="module-grade">{{ m.grade }}</div>
                </div>
              </div>
            </div>
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
                    <strong>{{ m.name }}</strong>
                    <small>({{ m.credits }} credits)</small>
                  </div>
                  <div class="module-grade">{{ m.grade }}</div>
                </div>
              </div>
            </div>
          </div>
        </transition>
      </div>
    </section>

    <!-- Features Section -->
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
          <p>Keep track of your grades and calculate your average.</p>
        </div>
        <div class="feature-item">
          <h3><span class="vertical-bar"></span> Split up your years</h3>
          <p>Divide your modules into years and customise weights for each year.</p>
        </div>
        <div class="feature-item">
          <h3><span class="vertical-bar"></span> Add grade targets</h3>
          <p>Predict your final classification with degree targets.</p>
        </div>
      </div>
    </section>

    <!-- Systems Section -->
    <section class="systems-section" ref="systemsRef" data-aos="fade-up">
      <div class="system-cards">
        <div class="system-card">
          <h3>Support for Every Grading System</h3>
          <p>Universities and colleges worldwide.</p>
        </div>
        <div class="system-card">
          <h3>US GPA Calculator</h3>
          <p>Support for GPA 4.0, 5.0, etc.</p>
        </div>
        <div class="system-card">
          <h3>UK Weighted % Calculator</h3>
          <p>Handle weighted averages for final grade.</p>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <Footer />
  </div>
</template>

<script>
import Footer from '@/components/Footer.vue'
import AOS from 'aos'
import 'aos/dist/aos.css'
import { gsap } from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'

export default {
  name: 'Landing',
  components: { Footer },
  data() {
    return {
      darkMode: false,
      showScrollDown: true,
      university: '',
      degree: '',
      statsMode: 'percentage',
      modulesPerc: [
        { letter: 'N', name: 'Neural Networks', credits: 20, grade: '65%', colorClass: 'n' },
        { letter: 'P', name: 'Database Systems', credits: 10, grade: '50%', colorClass: 'p' },
        { letter: 'Q', name: 'Quantum Computing', credits: 10, grade: '-', colorClass: 'q' }
      ],
      modulesGpa: [
        { letter: 'N', name: 'Neural Networks', credits: 20, grade: 'A', colorClass: 'n' },
        { letter: 'P', name: 'Database Systems', credits: 10, grade: 'B', colorClass: 'p' },
        { letter: 'Q', name: 'Quantum Computing', credits: 10, grade: '-', colorClass: 'q' }
      ]
    }
  },
  methods: {
    handleQuickCalc() {
      alert(`Calculating for ${this.university} - ${this.degree}...`)
    },
    toggleDarkMode() {
      this.darkMode = !this.darkMode
      if (this.darkMode) {
        document.body.classList.add('dark-mode')
      } else {
        document.body.classList.remove('dark-mode')
      }
      // Immediately update the gradient using a default angle (135deg)
      const container = this.$refs.landingContainer
      const angle = 135
      const gradient = this.darkMode
          ? `linear-gradient(${angle}deg, #B191FC 0%, #000000 100%)`
          : `linear-gradient(${angle}deg, #f2f2f2 0%, #b191fc 100%)`
      container.style.background = gradient
    },
    scrollToCalcForm() {
      this.$refs.statsSectionRef.scrollIntoView({ behavior: 'smooth' })
    }
  },
  mounted() {
    AOS.init({
      duration: 1000,
      offset: 120,
      once: true,
    })
    gsap.registerPlugin(ScrollTrigger)

    // Animate header in
    gsap.from(this.$refs.headerRef, {
      y: -80,
      opacity: 0,
      duration: 1,
      ease: 'power3.out',
    })
    // Animate hero content in
    gsap.from(this.$refs.heroRef, {
      x: -100,
      opacity: 0,
      duration: 1.2,
      ease: 'power2.out',
      scrollTrigger: {
        trigger: this.$refs.heroRef,
        start: 'top center',
      },
    })

    // Mouse parallax for hero background
    const heroSection = this.$refs.heroRef
    document.addEventListener('mousemove', (e) => {
      const x = e.clientX / window.innerWidth - 0.5
      const y = e.clientY / window.innerHeight - 0.5
      gsap.to(heroSection, {
        backgroundPosition: `${50 + x * 20}% ${50 + y * 20}%`,
        duration: 0.5,
        ease: 'power2.out',
      })
    })

    // Slight scroll-based parallax
    gsap.fromTo(
        heroSection,
        { y: 0 },
        {
          y: -150,
          scrollTrigger: {
            trigger: heroSection,
            start: 'top top',
            end: 'bottom top',
            scrub: 1,
          },
        }
    )

    // Keep arrow visible while hero is active
    ScrollTrigger.create({
      trigger: heroSection,
      start: 'top top',
      end: 'bottom top',
      onEnter: () => { this.showScrollDown = true },
      onLeave: () => { this.showScrollDown = false },
      onEnterBack: () => { this.showScrollDown = true },
      onLeaveBack: () => { this.showScrollDown = false },
    })

    // Mouse reactive gradient update (using the window's center for a stable reference)
    const container = this.$refs.landingContainer
    document.addEventListener('mousemove', (e) => {
      const centerX = window.innerWidth / 2;
      const centerY = window.innerHeight / 2;
      const deltaX = e.clientX - centerX;
      const deltaY = e.clientY - centerY;
      const angle = Math.atan2(deltaY, deltaX) * (180 / Math.PI);
      const gradient = this.darkMode
          ? `linear-gradient(${angle}deg, #B191FC 0%, #000000 100%)`
          : `linear-gradient(${angle}deg, #f2f2f2 0%, #b191fc 100%)`;
      container.style.background = gradient;
    })
  }
}
</script>


<style scoped>
@import url("https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css");
@import "aos/dist/aos.css";

/* Use the CSS variable defined in global styles */
.landing-container {
  min-height: 100vh;
  background: var(--bg-gradient);
  color: #000;
  position: relative;
  overflow-x: hidden;
  transition: background 0s;
}

/* (Rest of your component styles remain unchanged) */

/* Hero section exactly 100vh */
.hero-parallax {
  min-height: 100vh;
  background: transparent;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

/* Pull the hero overlay up by 40px so the scroll arrow appears higher */
.hero-parallax-overlay {
  background: none;
  width: 100%;
  max-width: 1200px;
  margin: -40px auto 0 auto;
  padding: 3rem 1rem;
  display: flex;
  justify-content: center;
}

/* Hero content styles */
.hero-content {
  text-align: center;
  color: #000;
  padding: 4rem 2rem;
  font-size: 1.1rem;
}
.hero-content h1 {
  font-size: 3.2rem;
  margin-bottom: 1rem;
}
.hero-content p {
  margin-bottom: 2rem;
  font-size: 1.2rem;
  line-height: 1.6;
}

/* Scroll-down arrow with bounce animation */
.scroll-down-btn {
  position: absolute;
  bottom: 2rem;
  left: 50%;
  transform: translateX(-50%);
  background: transparent;
  border: 2px solid #7b49ff;
  color: #7b49ff;
  font-size: 22px;
  padding: 0.6rem 1rem;
  border-radius: 50px;
  cursor: pointer;
  transition: 0.3s;
  box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}
.scroll-down-btn i {
  animation: bounce 1.5s infinite;
}
@keyframes bounce {
  0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
  40% { transform: translateY(5px); }
  60% { transform: translateY(3px); }
}
.scroll-down-btn:hover {
  background: #7b49ff;
  color: #fff;
  transform: translateX(-50%) scale(1.05);
}
.dark-mode .scroll-down-btn {
  border-color: #b39ddb;
  color: #b39ddb;
}
.dark-mode .scroll-down-btn:hover {
  background: #b39ddb;
  color: #333;
  transform: translateX(-50%) scale(1.05);
}

/* Sticky header */
.landing-header {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: transparent;
  z-index: 999;
}
.logo {
  font-size: 2rem;
  font-weight: bold;
  color: #512DA8;
}

/* Arrow buttons for Login/Sign Up */
.arrow-btn {
  font-size: 20px;
  font-weight: 600;
  background-color: #512da8;
  color: #fff;
  text-decoration: none;
  padding: 0.6rem 1.5rem 0.6rem 1.2rem;
  border-radius: 99px;
  position: relative;
  border: none;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  margin-left: 0.5rem;
  transition: 0.4s ease;
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
  right: 12px;
  transform: translateY(-50%);
  transition: 0.4s ease;
  z-index: 1;
}
.arrow-btn svg {
  width: 14px;
  height: 14px;
  position: absolute;
  right: 18px;
  top: 50%;
  transform: translateY(-50%) rotate(0deg);
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

/* Dark mode toggle button */
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

/* Hero buttons container */
.hero-buttons {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  margin-top: 1rem;
}

/* CTA button (Get Started) */
.cta-button {
  font-size: 16px;
  font-weight: 600;
  background-color: #512da8;
  padding: 0.75rem 1.5rem 0.75rem 2rem;
  display: inline-flex;
  align-items: center;
  border-radius: 99px;
  position: relative;
  text-decoration: none;
  transition: all 0.5s;
}
.cta-button .text {
  color: #fff;
  margin-right: 2rem;
  position: relative;
  z-index: 5;
}
.cta-button::before {
  content: '';
  background-color: #b39ddb;
  width: 28px;
  height: 28px;
  border-radius: 99px;
  position: absolute;
  top: 50%;
  right: 8px;
  transform: translateY(-50%);
  transition: all 0.5s;
  z-index: 1;
}
.cta-button svg {
  width: 14px;
  height: 14px;
  position: absolute;
  right: 14px;
  top: 50%;
  transform: translateY(-50%) rotate(0deg);
  transition: all 0.5s;
  z-index: 5;
}
.cta-button:hover svg {
  transform: translateY(-50%) rotate(45deg);
}
.cta-button:hover::before {
  width: 100%;
  height: 100%;
  right: 0;
}
.cta-button:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 10px rgba(0,0,0,0.2);
}

/* "Start Without Signing Up" button */
.scroll-btn {
  padding: 0.75rem 1.5rem;
  font-size: 16px;
  font-weight: 600;
  border-radius: 24px;
  border: 2px solid #7b49ff;
  background: transparent;
  color: #7b49ff;
  cursor: pointer;
  transition: 0.3s;
}
.scroll-btn:hover {
  background: #7b49ff;
  color: #fff;
}

/* Stats & Calculator Section */
.stats-section {
  display: flex;
  gap: 2rem;
  padding: 2rem;
  max-width: 1100px;
  margin: 0 auto;
}
.stats-section {
  margin-top: -40px;
}
.calc-form {
  flex: 1 1 300px;
  background: rgba(255,255,255,0.9);
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}
.calc-form h3 {
  margin-bottom: 1rem;
}
.calc-form label {
  display: block;
  margin: 0.5rem 0 0.25rem;
  color: #000;
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
.calc-form .start-btn {
  margin-left: auto;
  display: block;
  background: #512da8;
  color: #fff;
  border: none;
  padding: 0.6rem 1rem;
  border-radius: 24px;
  font-size: 1rem;
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.calc-form .start-btn:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 10px rgba(0,0,0,0.2);
}
.stats-card-container {
  flex: 1 1 500px;
  min-height: 300px;
}
.stats-card {
  background: rgba(255,255,255,0.9);
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 1px 5px rgba(0,0,0,0.05);
}

/* Fade-scale transition */
.fade-scale-enter-active,
.fade-scale-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}
.fade-scale-enter,
.fade-scale-leave-to {
  opacity: 0;
  transform: scale(0.95);
}

/* Progress bar inside stats */
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
}
.remaining {
  background: #999;
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
.modules-list .module-info {
  flex: 1;
}
.modules-list .module-grade {
  font-weight: bold;
}
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
  transition: transform 0.3s ease, background-color 0.3s ease;
}
.tabs button:hover {
  transform: scale(1.05);
}
.tabs button.active {
  background: #000;
  border-color: #000;
  color: #fff;
}

/* Features Section */
.features-section {
  display: flex;
  gap: 2rem;
  max-width: 1100px;
  margin: 0 auto;
  padding: 2rem;
}
.features-hero {
  flex: 1 1 300px;
}
.features-list {
  flex: 1 1 500px;
}
.features-hero h2 {
  font-size: 2.2rem;
  line-height: 1.2;
  margin-bottom: 1rem;
  color: #000;
}
.highlight {
  color: #ffeb3b;
}
.feature-item h3 {
  margin-bottom: 0.3rem;
  font-size: 1.2rem;
  color: #000;
}
.vertical-bar {
  display: inline-block;
  background: #000;
  width: 4px;
  height: 1rem;
  margin-right: 6px;
}
.feature-item p {
  color: #333;
}

/* Systems Section */
.systems-section {
  max-width: 1100px;
  margin: 0 auto;
  padding: 2rem 3rem;
}
.system-cards {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
}
.system-card {
  flex: 1;
  background: rgba(255,255,255,0.9);
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
  text-align: center;
}
.system-card h3 {
  margin-bottom: 0.75rem;
}

/* Footer */
.landing-footer {
  background: var(--footer-bg);
  text-align: center;
  padding: 1rem;
  margin-top: auto;
  box-shadow: 0 -2px 4px rgba(0,0,0,0.1);
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
.contact-info {
  margin-top: 2rem;
  font-size: 0.9rem;
  text-align: center;
}
.contact-info a {
  color: var(--link-color);
  text-decoration: none;
  transition: 0.3s;
}
.contact-info a:hover {
  text-decoration: underline;
}

/* DARK MODE OVERRIDES */
.dark-mode .landing-container {
  background: linear-gradient(135deg, #000000 10%, #5d5d5d 90%);
  color: #e0e0e0;
}
.dark-mode .hero-content {
  color: #e0e0e0;
}
.dark-mode .features-hero h2,
.dark-mode .feature-item h3,
.dark-mode .feature-item p {
  color: #ccc;
}
.dark-mode .vertical-bar {
  background: #ccc;
}
.dark-mode .highlight {
  color: #bbb;
}
.dark-mode .hero-parallax {
  background: transparent;
}
.dark-mode .hero-parallax-overlay {
  background: none;
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
.dark-mode .calc-form {
  background: rgba(44,44,44,0.9);
  color: #e0e0e0;
}
.dark-mode .calc-form label {
  background: rgba(44,44,44,0.9);
  color: #e0e0e0;
}
.dark-mode .calc-form input {
  background: #444;
  border-color: #555;
  color: #e0e0e0;
}
.dark-mode .stats-card {
  background: rgba(44,44,44,0.9);
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
  background: rgba(44,44,44,0.9);
  color: #e0e0e0;
}
.dark-mode .landing-footer {
  background: #2b2b2b;
  color: #ccc;
  box-shadow: 0 -2px 4px rgba(34,34,34,0.5);
}
.dark-mode .footer-col a,
.dark-mode .contact-info a {
  color: #ccc;
}

/* MOBILE ADJUSTMENTS */
@media only screen and (max-width: 768px) {
  .landing-container {
    padding: 0 1rem;
  }
  .hero-parallax {
    min-height: 80vh;
  }
  .hero-content h1 {
    font-size: 2.5rem;
  }
  .hero-content p {
    font-size: 1rem;
  }
  .hero-buttons {
    gap: 0.75rem;
  }
  .cta-button {
    font-size: 14px;
    padding: 0.65rem 1.2rem;
  }
  .scroll-btn {
    font-size: 14px;
    padding: 0.5rem 1rem;
  }
  .stats-section {
    flex-direction: column;
    gap: 1rem;
    margin-top: -20px;
    padding: 1rem;
  }
  .calc-form {
    padding: 1rem;
  }
  .calc-form .start-btn {
    width: auto;
    margin: 1rem 0 0 auto;
  }
  .stats-card-container {
    margin-top: 1rem;
  }
  .tabs button {
    padding: 0.5rem;
    font-size: 14px;
  }
}
</style>
